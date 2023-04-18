from rest_framework import generics
from contextlib import contextmanager

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
from .serializers import (
    NavbarItemSerializer,
    FooterSerializer,
    AboutUsSerializer,
    BlogSerializer,
    TestimonialSerializer,
    GallerySerializer,
    ContactUsSerializer,
    FAQSerializer,
    NewsletterSubscriptionSerializer,
    SocialMediaSerializer,
    EventSerializer,
    AnalyticsSerializer,
)
from django.utils.translation import get_language, activate

class NavbarItemList(generics.ListAPIView):
    queryset = NavbarItem.objects.all()
    serializer_class = NavbarItemSerializer


class FooterList(generics.ListAPIView):
    queryset = Footer.objects.all()
    serializer_class = FooterSerializer


class AboutUsList(generics.ListAPIView):
    # queryset = AboutUs.objects.all()
    serializer_class = AboutUsSerializer
    def get_queryset(self):
        language = self.request.query_params.get('lang', None)

        if language:
            with use_language(language):
                return AboutUs.objects.all()
        else:
            return AboutUs.objects.all()

class BlogList(generics.ListAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer


class BlogDetail(generics.RetrieveAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    lookup_field = "slug"


class TestimonialList(generics.ListAPIView):
    queryset = Testimonial.objects.all()
    serializer_class = TestimonialSerializer


class GalleryList(generics.ListAPIView):
    queryset = Gallery.objects.all()
    serializer_class = GallerySerializer


class ContactUsList(generics.ListAPIView):
    queryset = ContactUs.objects.all()
    serializer_class = ContactUsSerializer


class FAQList(generics.ListAPIView):
    queryset = FAQ.objects.all()
    serializer_class = FAQSerializer


class NewsletterSubscriptionList(generics.ListAPIView):
    queryset = NewsletterSubscription.objects.all()
    serializer_class = NewsletterSubscriptionSerializer


class SocialMediaList(generics.ListAPIView):
    queryset = SocialMedia.objects.all()
    serializer_class = SocialMediaSerializer


class EventList(generics.ListAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer


class AnalyticsList(generics.ListAPIView):
    queryset = Analytics.objects.all()
    serializer_class = AnalyticsSerializer

@contextmanager
def use_language(language):
    current_language = get_language()
    try:
        activate(language)
        yield
    finally:
        activate(current_language)

