from rest_framework import generics
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

class NavbarItemList(generics.ListAPIView):
    queryset = NavbarItem.objects.all()
    serializer_class = NavbarItemSerializer


class FooterList(generics.ListAPIView):
    queryset = Footer.objects.all()
    serializer_class = FooterSerializer


class AboutUsList(generics.ListAPIView):
    queryset = AboutUs.objects.all()
    serializer_class = AboutUsSerializer


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
