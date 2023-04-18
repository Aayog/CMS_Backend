from django.apps import AppConfig, apps


def init_app():
    # Import the models here
    from .models import MyModel

    # Use the models here
    MyModel.objects.all()


# Call the init_app func


class UsersConfig(AppConfig):
    name = "users"
