from django.apps import AppConfig


class AccountsConfig(AppConfig):
    name = 'accounts'
        # add this
    def ready(self):
        import accounts.signals  # noqa
