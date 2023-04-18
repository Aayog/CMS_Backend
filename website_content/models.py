from django.db import models
from django.utils.translation import gettext_lazy as _
from autoslug import AutoSlugField

class NavbarItem(models.Model):
    title = models.CharField(max_length=200)
    link = models.CharField(max_length=200)
    def __str__(self):
        return self.title


class Footer(models.Model):
    content = models.TextField()

    def __str__(self):
        return f"Footer {self.pk}"


class AboutUs(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name_plural = "AboutUs"

class Blog(models.Model):
    title = models.CharField(max_length=200)
    slug = AutoSlugField(populate_from="headline")
    content = models.TextField()
    # author = models.ForeignKey(, on_delete=models.CASCADE)
    author = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.slug


class Testimonial(models.Model):
    name = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    content = models.TextField()

    def __str__(self):
        return f"{self.name} - {self.title}"


class Gallery(models.Model):
    title = models.CharField(max_length=200)
    image_desc = models.CharField(max_length=200)
    image = models.ImageField(upload_to="gallery/")
    created_at = models.DateTimeField(auto_now_add=True)
    # maybe add tags

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name_plural = "Galleries"

class ContactUs(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "ContactUs"

class FAQ(models.Model):
    question = models.CharField(max_length=300)
    category = models.CharField(max_length=100)
    answer = models.TextField()
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.question
    
    class Meta:
        verbose_name_plural = "FAQs"

class NewsletterSubscription(models.Model):
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.email


class SocialMedia(models.Model):
    platform = models.CharField(max_length=100)
    link = models.CharField(max_length=200)

    def __str__(self):
        return self.platform


class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=200)
    image = models.ImageField(upload_to="event_images/")
    organizer = models.CharField(max_length=200)
    registration_link = models.URLField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    def __str__(self):
        return self.title


class Analytics(models.Model):
    page = models.CharField(max_length=200)
    views = models.PositiveIntegerField()
    unique_visitors = models.PositiveIntegerField()
    date = models.DateField()
    time = models.TimeField()
    source = models.CharField(max_length=200)
    bounce_rate = models.FloatField()
    time_on_page = models.DurationField()
    # site = models.ForeignKey(Site, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.page} ({self.date} {self.time})"

    class Meta:
        verbose_name_plural = "Analytics"