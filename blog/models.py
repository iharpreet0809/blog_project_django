from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify
from ckeditor.fields import RichTextField
from taggit.managers import TaggableManager
from django.utils import timezone



class Contact(models.Model):
    """
    Contact Form Model
    
    Stores contact form submissions from visitors.
    Used for the main contact form on the portfolio homepage.
    """
    name = models.CharField(max_length=100)  # Visitor's full name
    email = models.EmailField()  # Visitor's email address
    subject = models.CharField(max_length=200)  # Subject line of the message
    message = models.TextField()  # The actual message content
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp when message was sent

    def __str__(self):
        """String representation for admin interface"""
        return f"{self.name} - {self.subject}"

    class Meta:
        verbose_name = "Contact Form Submission"
        verbose_name_plural = "Contact Form Submissions"


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ['name']

class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='authors/', blank=True, null=True)
    website = models.URLField(blank=True)
    twitter = models.URLField(blank=True)
    linkedin = models.URLField(blank=True)
    github = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.get_full_name() or self.user.username

    class Meta:
        verbose_name = "Author"
        verbose_name_plural = "Authors"

class BlogPost(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
    ]
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    content = RichTextField(config_name='blog')
    excerpt = models.TextField(max_length=500, blank=True, help_text="Brief summary of the post")
    cover_image = models.ImageField(upload_to='blog_covers/', blank=True, null=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='blog_posts')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='blog_posts')
    tags = TaggableManager(blank=True)
    is_published = models.BooleanField(default=False)
    published_date = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    meta_title = models.CharField(max_length=60, blank=True, help_text="SEO title (max 60 characters)")
    meta_description = models.CharField(max_length=160, blank=True, help_text="SEO description (max 160 characters)")
    views = models.PositiveIntegerField(default=0)
    featured = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        if self.is_published and not self.published_date:
            self.published_date = timezone.now()
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog_detail', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Blog Post"
        verbose_name_plural = "Blog Posts"
        ordering = ['-published_date', '-created_at']

    @property
    def reading_time(self):
        words_per_minute = 200
        word_count = len(self.content.split())
        minutes = word_count // words_per_minute
        return max(1, minutes)

    def increment_views(self):
        self.views += 1
        self.save(update_fields=['views']) 