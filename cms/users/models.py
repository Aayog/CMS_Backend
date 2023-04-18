from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
    Group,
    Permission,
)
from django.contrib.contenttypes.models import ContentType
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.utils.crypto import get_random_string
from django.urls import reverse
from django.conf import settings
from django.utils.http import urlsafe_base64_encode
from .tokens import account_activation_token
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from .threads import send_email

user_permissions = [
    ("can_like_post", "Can like a post"),
    ("can_view_post", "Can view a post"),
    ("can_report_post", "Can report a post"),
    ("can_add_favorite_reporter", "Can add favorite reporters"),
    ("can_add_favorite_category", "Can add favorite categories"),
]

reporter_permissions = user_permissions + [
    ("can_create_post", "Can create a post"),
    ("can_edit_post", "Can edit a post"),
    ("can_delete_post", "Can delete a post"),
]

admin_permissions = reporter_permissions + [
    ("can_add_user", "Can add a user"),
    ("can_edit_user", "Can edit a user"),
    ("can_delete_user", "Can delete a user"),
]


class UserManager(BaseUserManager):
    def create_user(
        self, email, password=None, first_name=None, last_name=None, **extra_fields
    ):
        if not email:
            raise ValueError("Users must have an email address")
        email = self.normalize_email(email)
        user = self.model(
            email=email, first_name=first_name, last_name=last_name, **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_verified", True)
        return self.create_user(email, password, **extra_fields)

    def get_by_natural_key(self, email):
        return self.get(email=email)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    USER = 1
    REPORTER = 2
    ADMIN = 3
    ROLE_CHOICES = (
        (USER, "User"),
        (REPORTER, "Reporter"),
        (ADMIN, "Admin"),
    )
    first_name = models.CharField(max_length=100, null=True)
    last_name = models.CharField(max_length=100, null=True)
    bio = models.TextField(max_length=255, null=True)
    profile_pic = models.ImageField(upload_to="profile_pictures", blank=True)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)  # Confirmed by email activation
    role = models.PositiveSmallIntegerField(
        choices=ROLE_CHOICES[:-1], blank=True, null=True, default=USER
    )
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    zipcode = models.CharField(max_length=30, blank=True, null=True)
    activation_token = models.CharField(max_length=50)
    is_verified = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"

    objects = UserManager()

    class Meta:
        db_table = "users"

    def __str__(self):
        return self.email

    def get_username(self):
        return self.email

    def email_user(self, subject, message):
        print("sending email .. .")
        send_email(subject, message, [self.email])

    def save(self, *args, **kwargs):
        is_new = not self.pk
        super().save(*args, **kwargs)
        # Only if not set first
        if is_new:
            self.save()
            token = account_activation_token.make_token(self)
            uidb64 = urlsafe_base64_encode(force_bytes(self.pk))
            subject = "Activate Your News Portal Account"
            activation_link = f"{reverse('users:activate', kwargs={'uidb64':str(uidb64), 'token':str(token)})}"
            message = render_to_string(
                "account_activation_email.html",
                {
                    "user": self,
                    "domain": "127.0.0.1",  # current_site.domain,
                    "uid": urlsafe_base64_encode(force_bytes(self.pk)),
                    "activation_link": f"{settings.BASE_URL}{activation_link}",
                },
            )
            print(message)
            self.email_user(subject, message)


class Reporter(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    previous_works = models.TextField(blank=True)
    biography = models.TextField(blank=True)
    verified = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=CustomUser)
def set_user_permissions(sender, instance=None, created=False, **kwargs):
    if created:
        if instance.role == CustomUser.USER:
            group, _ = Group.objects.get_or_create(name="User")
            for codename, desc in user_permissions:
                permission, _ = Permission.objects.get_or_create(
                    content_type=ContentType.objects.get_for_model(CustomUser),
                    codename=codename,
                    defaults={"name": desc},
                )
                group.permissions.add(permission)
            instance.groups.add(group)

        elif instance.role == CustomUser.REPORTER:
            group, _ = Group.objects.get_or_create(name="Reporter")
            for codename, desc in reporter_permissions:
                permission, _ = Permission.objects.get_or_create(
                    content_type=ContentType.objects.get_for_model(CustomUser),
                    codename=codename,
                    defaults={"name": desc},
                )
                group.permissions.add(permission)
            instance.groups.add(group)

        elif instance.role == CustomUser.ADMIN:
            group, _ = Group.objects.get_or_create(name="Admin")
            for codename, desc in admin_permissions:
                permission, _ = Permission.objects.get_or_create(
                    content_type=ContentType.objects.get_for_model(CustomUser),
                    codename=codename,
                    defaults={"name": desc},
                )
                group.permissions.add(permission)
            instance.groups.add(group)


# from django.apps import apps

# CustomUserModel = apps.get_model('users', 'CustomUser')

# permission, created = Permission.objects.get_or_create(
#     content_type=ContentType.objects.get_for_model(CustomUserModel),
#     codename='can_do_something'
# )

# ReporterModel = apps.get_model('users', 'Reporter')

# permission, created = Permission.objects.get_or_create(
#     content_type=ContentType.objects.get_for_model(ReporterModel),
#     codename='can_do_something'
# )

# # create content types
# content_type_user = ContentType.objects.create(app_label='users', model=CustomUserModel)

# content_type_reporter = ContentType.objects.create(model=ReporterModel)


# # create groups
# user_group, created = Group.objects.get_or_create(name='user')

# for codename, desc in user_permissions:
#     permission, created = Permission.objects.get_or_create(
#         content_type=content_type_user,
#         codename=codename,
#         defaults={'name': desc}
#     )
#     user_group.permissions.add(permission)

# reporter_group, created = Group.objects.get_or_create(name='reporter')

# for codename, desc in reporter_permissions:
#     permission, created = Permission.objects.get_or_create(
#         content_type=content_type_reporter,
#         codename=codename,
#         defaults={'name': desc}
#     )
#     reporter_group.permissions.add(permission)

# for codename, desc in user_permissions:
#     permission, created = Permission.objects.get_or_create(
#         content_type=content_type_reporter,
#         codename=codename,
#         defaults={'name': desc}
#     )
#     reporter_group.permissions.add(permission)

# for codename, desc in admin_permissions:
#     permission, created = Permission.objects.get_or_create(
#         content_type=content_type_user,
#         codename=codename,
#         defaults={'name': desc}
#     )
#     user_group.permissions.add(permission)

#     permission, created = Permission.objects.get_or_create(
#         content_type=content_type_reporter,
#         codename=codename,
#         defaults={'name': desc}
#     )
#     reporter_group.permissions.add(permission)
