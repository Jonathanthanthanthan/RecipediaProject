from django.apps import AppConfig

class RecipediaPostCongig(AppConfig):
    name = 'RecipediaPost'

    def ready(self):
        import RecipediaPost.signals


