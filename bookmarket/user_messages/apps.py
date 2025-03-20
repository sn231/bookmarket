from django.apps import AppConfig

class MessagesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'user_messages'  # 确保这里的名称与应用目录名称一致