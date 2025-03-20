import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bookmarket.settings')
django.setup()

from users.models import User

def create_admin_user():
    username = 'admin'
    email = 'admin@example.com'
    password = 'admin123'
    
    if not User.objects.filter(username=username).exists():
        admin = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            role='admin',
            student_id='ADMIN001'
        )
        print(f'管理员用户 {username} 创建成功!')
    else:
        print(f'用户 {username} 已存在!')

if __name__ == '__main__':
    create_admin_user() 