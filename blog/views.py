from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.http import JsonResponse, HttpResponseNotAllowed
from .models import BlogPost, Category
from .forms import BlogSearchForm,ContactForm

from django.contrib import messages
from datetime import datetime
from django.core.mail import EmailMessage, BadHeaderError
from smtplib import SMTPException


def contact(request):
    """
    Handle contact form submission from the footer on any page.
    On POST: process the form, show a success message, and redirect back to the referring page (or home if not available).
    On GET: return 405 (method not allowed), since the form is always rendered in the footer.
    """
    if request.method == 'POST':
        # Process form submission
        form = ContactForm(request.POST)
        if form.is_valid():
            # Save form data to database
            form.save()
            # Extract form data for email
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']

            # Prepare email content
            full_message = f"""
New Query Submission on your Blog website- "www.digitaldiary.iharpreet.com":

Name: {name}
Email: {email}
Subject: {subject}

Message:
{message}
"""
            try:
                # Send email notification to site owner
                email_message = EmailMessage(
                    subject=f"{subject}-[Contact Form]",
                    body=full_message,
                    from_email='From Blogging <talkwithharpreet@gmail.com>',
                    to=['talkwithharpreet@gmail.com'],
                    reply_to=[email],  # Allow direct reply to visitor
                )
                email_message.send(fail_silently=False)
                messages.success(request, 'Your message has been sent successfully!')
                return redirect('/#contact-msg')# redirect to the contact-msg section
                
            except (BadHeaderError, SMTPException):
                messages.error(request, 'There was an error sending the email.')
            # Redirect back to the referring page, or home if not available
            return redirect(request.META.get('HTTP_REFERER', '/'))
        else:
            messages.error(request, 'Please correct the errors in the form.')
            return redirect(request.META.get('HTTP_REFERER', '/'))
    else:
        return HttpResponseNotAllowed(['POST'])


def blog_list(request):
    """
    Display list of published blog posts with filtering and search functionality.
    
    This view handles the main blog listing page. It supports:
    - Text search across title, content, excerpt, and tags
    - Category filtering
    - Tag filtering
    - Date range filtering
    - Featured posts filtering
    - Pagination (6 posts per page)
    
    Args:
        request: HTTP request object with optional GET parameters for filtering
        
    Returns:
        HttpResponse: Rendered blog list page with filtered posts
    """
    # Get all published posts with related author and category data
    posts = BlogPost.objects.filter(is_published=True).select_related('author', 'category')
    
    # Initialize search form with GET parameters
    search_form = BlogSearchForm(request.GET)
    
    if search_form.is_valid():
        # Handle text search
        query = search_form.cleaned_data.get('q')
        if query:
            # Search across multiple fields using Q objects for OR conditions
            posts = posts.filter(
                Q(title__icontains=query) |  # Search in title
                Q(content__icontains=query) |  # Search in content
                Q(excerpt__icontains=query) |  # Search in excerpt
                Q(tags__name__icontains=query)  # Search in tag names
            ).distinct()  # Remove duplicates from tag search
        
        # Handle category filtering
        category = search_form.cleaned_data.get('category')
        if category:
            posts = posts.filter(category=category)
        
        # Handle tag filtering (comma-separated tags)
        tags_query = search_form.cleaned_data.get('tags')
        if tags_query:
            # Split comma-separated tags and filter
            tag_names = [tag.strip() for tag in tags_query.split(',') if tag.strip()]
            posts = posts.filter(tags__name__in=tag_names).distinct()
        
        # Handle date range filtering
        date_from = search_form.cleaned_data.get('date_from')
        date_to = search_form.cleaned_data.get('date_to')
        
        if date_from:
            posts = posts.filter(published_date__date__gte=date_from)
        if date_to:
            posts = posts.filter(published_date__date__lte=date_to)
        
        # Handle featured posts filtering
        featured_only = search_form.cleaned_data.get('featured_only')
        if featured_only:
            posts = posts.filter(featured=True)
    
    # Get categories and tags for sidebar display
    categories = Category.objects.all()
    all_tags = BlogPost.tags.all()
    
    # Implement pagination (6 posts per page)
    paginator = Paginator(posts, 6)
    page = request.GET.get('page')
    
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range, deliver last page
        posts = paginator.page(paginator.num_pages)
    
    # Prepare context for template
    context = {
        'posts': posts,
        'search_form': search_form,
        'categories': categories,
        'all_tags': all_tags,
        'featured_posts': BlogPost.objects.filter(is_published=True, featured=True)[:3],  # Top 3 featured posts
    }
    
    return render(request, 'blog/blog_list.html', context)

def blog_detail(request, slug):
    post = get_object_or_404(BlogPost, slug=slug, is_published=True)
    post.increment_views()
    related_posts = BlogPost.objects.filter(
        category=post.category, is_published=True
    ).exclude(id=post.id)[:3]
    recent_posts = BlogPost.objects.filter(is_published=True).order_by('-published_date')[:5]
    context = {
        'post': post,
        'related_posts': related_posts,
        'recent_posts': recent_posts,
    }
    return render(request, 'blog/blog_detail.html', context)


def blog_category(request, slug):
    """
    Display posts filtered by category.
    
    Shows all published posts from a specific category with pagination.
    
    Args:
        request: HTTP request object
        slug: URL slug of the category
        
    Returns:
        HttpResponse: Rendered category page with filtered posts
    """
    # Get the category or return 404
    category = get_object_or_404(Category, slug=slug)
    
    # Get all published posts from this category
    posts = BlogPost.objects.filter(
        is_published=True,
        category=category
    ).select_related('author', 'category')
    
    # Implement pagination
    paginator = Paginator(posts, 6)  # 6 posts per page
    page = request.GET.get('page')
    
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    
    context = {
        'posts': posts,
        'category': category,
        'categories': Category.objects.all(),  # For sidebar
        'all_tags': BlogPost.tags.all(),  # For sidebar
    }
    
    return render(request, 'blog/blog_category.html', context)

def blog_tag(request, tag_slug):
    """
    Display posts filtered by tag.
    
    Shows all published posts that have a specific tag with pagination.
    
    Args:
        request: HTTP request object
        tag_slug: URL slug of the tag
        
    Returns:
        HttpResponse: Rendered tag page with filtered posts
    """
    from taggit.models import Tag
    
    # Get the tag or return 404
    tag = get_object_or_404(Tag, slug=tag_slug)
    
    # Get all published posts with this tag
    posts = BlogPost.objects.filter(
        is_published=True,
        tags__name__in=[tag.name]
    ).select_related('author', 'category')
    
    # Implement pagination
    paginator = Paginator(posts, 6)  # 6 posts per page
    page = request.GET.get('page')
    
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    
    context = {
        'posts': posts,
        'tag': tag,
        'categories': Category.objects.all(),  # For sidebar
        'all_tags': BlogPost.tags.all(),  # For sidebar
    }
    
    return render(request, 'blog/blog_tag.html', context)

@require_http_methods(["GET"])
def blog_search_ajax(request):
    """
    AJAX endpoint for blog search functionality.
    
    This view provides real-time search results via AJAX requests.
    It returns JSON data for dynamic search without page reload.
    
    Args:
        request: HTTP request object with GET parameters (q, category, tags)
        
    Returns:
        JsonResponse: JSON data containing search results
    """
    # Get search parameters from request
    query = request.GET.get('q', '')
    category_id = request.GET.get('category', '')
    tags = request.GET.get('tags', '')
    
    # Start with all published posts
    posts = BlogPost.objects.filter(is_published=True).select_related('author', 'category')
    
    # Apply text search filter
    if query:
        posts = posts.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(excerpt__icontains=query)
        )
    
    # Apply category filter
    if category_id:
        posts = posts.filter(category_id=category_id)
    
    # Apply tag filter
    if tags:
        tag_names = [tag.strip() for tag in tags.split(',') if tag.strip()]
        posts = posts.filter(tags__name__in=tag_names).distinct()
    
    # Limit results for AJAX response (performance)
    posts = posts[:10]
    
    # Prepare JSON data
    data = []
    for post in posts:
        data.append({
            'title': post.title,
            'excerpt': post.excerpt,
            'author': post.author.user.get_full_name() or post.author.user.username,
            'category': post.category.name,
            'published_date': post.published_date.strftime('%B %d, %Y') if post.published_date else '',
            'url': post.get_absolute_url(),
            'cover_image': post.cover_image.url if post.cover_image else '',
        })
    
    return JsonResponse({'posts': data})




def blog_rss_feed(request):
    posts = BlogPost.objects.filter(is_published=True).order_by('-published_date')[:20]
    site_name = 'Blog'
    site_url = request.build_absolute_uri('/')
    return render(request, 'blog/rss_feed.xml', {
        'posts': posts,
        'site_name': site_name,
        'site_url': site_url,
        'request': request,
    }, content_type='application/rss+xml') 