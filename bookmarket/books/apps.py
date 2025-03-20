from django.apps import AppConfig

class BooksConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'books'  # 确保这里的名称与应用目录名称一致