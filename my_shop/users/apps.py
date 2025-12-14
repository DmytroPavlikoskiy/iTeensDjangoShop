from django.apps import AppConfig


class UsersConfig(AppConfig):
    name = "users"
    def ready(self):
        # from signals import user_signal_profile
        return super().ready()
