from rest_framework import serializers
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


class NavbarItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = NavbarItem
        fields = ("title", "link")


class FooterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Footer
        fields = ("content",)


class AboutUsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AboutUs
        fields = ("title", "content")


class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = ("title", "slug", "content", "author", "created_at", "updated_at")


class TestimonialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Testimonial
        fields = ("name", "title", "content")


class GallerySerializer(serializers.ModelSerializer):
    class Meta:
        model = Gallery
        fields = ("title", "image_desc", "image", "created_at")


class ContactUsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactUs
        fields = ("name", "email", "subject", "message", "created_at")


class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = ("question", "category", "answer", "updated_at")


class NewsletterSubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsletterSubscription
        fields = ("email",)


class SocialMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialMedia
        fields = ("platform", "link")


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = (
            "title",
            "description",
            "location",
            "image",
            "organizer",
            "registration_link",
            "start_date",
            "end_date",
        )


class AnalyticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Analytics
        fields = (
            "page",
            "views",
            "unique_visitors",
            "date",
            "time",
            "source",
            "bounce_rate",
            "time_on_page",
        )
