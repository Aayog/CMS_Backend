from django.urls import path
from . import views

urlpatterns = [
    path("navbar/", views.NavbarItemList.as_view(), name="navbar-list"),
    path("footer/", views.FooterList.as_view(), name="footer-list"),
    path("about-us/", views.AboutUsList.as_view(), name="about-us-list"),
    path("blog/", views.BlogList.as_view(), name="blog-list"),
    path("blog/<slug:slug>/", views.BlogDetail.as_view(), name="blog-detail"),
    path("testimonials/", views.TestimonialList.as_view(), name="testimonial-list"),
    path("gallery/", views.GalleryList.as_view(), name="gallery-list"),
    path("contact-us/", views.ContactUsList.as_view(), name="contact-us-list"),
    path("faq/", views.FAQList.as_view(), name="faq-list"),
    path(
        "newsletter/",
        views.NewsletterSubscriptionList.as_view(),
        name="newsletter-list",
    ),
    path("social-media/", views.SocialMediaList.as_view(), name="social-media-list"),
    path("event/", views.EventList.as_view(), name="event-list"),
    path("analytics/", views.AnalyticsList.as_view(), name="analytics-list"),
]

