from django.contrib import admin
from .models import BlogPost, Category, Author, Contact
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms

class ContactAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name', 'email', 'subject', 'message']
    readonly_fields = ['created_at']
    ordering = ['-created_at']

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    ordering = ['name']

class AuthorAdmin(admin.ModelAdmin):
    list_display = ['user', 'website', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'user__first_name', 'user__last_name', 'bio']
    readonly_fields = ['created_at', 'updated_at']

class BlogPostForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget())
    class Meta:
        model = BlogPost
        fields = '__all__'

class BlogPostAdmin(admin.ModelAdmin):
    form = BlogPostForm
    list_display = ['title', 'author', 'category', 'is_published', 'featured', 'published_date', 'views', 'created_at']
    list_filter = ['is_published', 'featured', 'category', 'published_date', 'created_at']
    search_fields = ['title', 'content', 'excerpt', 'author__user__username']
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ['views', 'created_at', 'updated_at']
    list_editable = ['is_published', 'featured']
    ordering = ['-published_date', '-created_at']
    fieldsets = (
        ('Content', {
            'fields': ('title', 'slug', 'content', 'excerpt', 'cover_image')
        }),
        ('Relationships', {
            'fields': ('author', 'category', 'tags')
        }),
        ('Publication', {
            'fields': ('is_published', 'published_date', 'featured')
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_description'),
            'classes': ('collapse',)
        }),
        ('Statistics', {
            'fields': ('views', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    def save_model(self, request, obj, form, change):
        if not obj.author_id:
            try:
                author = Author.objects.get(user=request.user)
                obj.author = author
            except Author.DoesNotExist:
                pass
        super().save_model(request, obj, form, change)

admin.site.register(Category, CategoryAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(BlogPost, BlogPostAdmin)
admin.site.register(Contact, ContactAdmin)

admin.site.site_title = "Blog Admin Panel"
admin.site.site_header = "Blog Admin Panel"
admin.site.index_title = "Welcome to the Blog Admin Panel" 