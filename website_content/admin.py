from django.contrib import admin
from .models import (
    NavbarItem,
    Footer,
    AboutUs,
    Blog,
    Testimonial,
    Gallery,
    ContactUs,
    FAQ,
    NewsletterSubscription,
    SocialMedia,
    Event,
    Analytics,
)
from jet.admin import CompactInline
# from jet.filters import DateRangeFilter

class NavbarItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'link')
    search_fields = ('title', 'link')
    ordering = ('title',)

class FooterAdmin(admin.ModelAdmin):
    list_display = ('content',)

class AboutUsAdmin(admin.ModelAdmin):
    list_display = ('title', 'content')
    search_fields = ('title', 'content')

class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('name', 'title', 'content')
    search_fields = ('name', 'title', 'content')
    ordering = ('name',)

class GalleryAdmin(admin.ModelAdmin):
    list_display = ('title', 'image_desc', 'created_at')
    search_fields = ('title', 'image_desc')
    list_filter = ('created_at',)
    ordering = ('-created_at',)

class ContactUsAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'created_at')
    search_fields = ('name', 'email', 'subject')
    list_filter = ('created_at',)
    ordering = ('-created_at',)

class FAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'category', 'updated_at')
    search_fields = ('question', 'category')
    list_filter = ('category', 'updated_at')
    ordering = ('category', 'question')

class NewsletterSubscriptionAdmin(admin.ModelAdmin):
    list_display = ('email',)
    search_fields = ('email',)
    ordering = ('email',)

class SocialMediaAdmin(admin.ModelAdmin):
    list_display = ('platform', 'link')
    search_fields = ('platform', 'link')
    ordering = ('platform',)

class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'location', 'organizer', 'start_date', 'end_date')
    search_fields = ('title', 'location', 'organizer')
    list_filter = ('start_date', 'end_date')
    ordering = ('-start_date',)

class AnalyticsAdmin(admin.ModelAdmin):
    list_display = ('page', 'views', 'unique_visitors', 'date', 'time', 'source', 'bounce_rate', 'time_on_page')
    search_fields = ('page', 'source')
    list_filter = ('date', 'time', 'source')
    ordering = ('-date', '-time', 'page')

# class AnalyticsInline(CompactInline):
#     model = Analytics
#     extra = 0
#     fk_name = 'blog'

class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author', 'created_at', 'updated_at')
    search_fields = ('title', 'slug', 'author')
    # list_filter = (('created_at', DateRangeFilter), ('updated_at', DateRangeFilter),)
    list_filter = ('created_at', 'updated_at')
    # inlines = [AnalyticsInline]
    ordering = ('-created_at',)

admin.site.register(NavbarItem, NavbarItemAdmin)
admin.site.register(Footer, FooterAdmin)
admin.site.register(AboutUs, AboutUsAdmin)
admin.site.register(Blog, BlogAdmin)
admin.site.register(Testimonial, TestimonialAdmin)
admin.site.register(Gallery, GalleryAdmin)
admin.site.register(ContactUs, ContactUsAdmin)
admin.site.register(FAQ, FAQAdmin)
admin.site.register(NewsletterSubscription, NewsletterSubscriptionAdmin)
admin.site.register(SocialMedia, SocialMediaAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Analytics, AnalyticsAdmin)
