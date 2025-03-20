import os  # 添加这一行以导入os模块

# 定义BASE_DIR
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.staticfiles',
    'django.contrib.messages',
    # 添加我们的应用
    'users.apps.UsersConfig',
    'books.apps.BooksConfig',
    'user_messages.apps.MessagesConfig',  # 确保只添加一次
    'orders.apps.OrdersConfig',  # 添加这一行
    'crispy_forms',
    'crispy_bootstrap4',
]

# 设置自定义用户模型
AUTH_USER_MODEL = 'users.User'

# 媒体文件设置
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# 静态文件设置
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

# 数据库设置
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'bookmarket',
        'USER': 'root',  # 根据实际情况修改
        'PASSWORD': 'wzz20041019',  # 根据实际情况修改
        'HOST': 'localhost',
        'PORT': '3306',
    }
}

# 中间件设置
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# 语言设置
LANGUAGE_CODE = 'zh-hans'
TIME_ZONE = 'Asia/Shanghai'

DEBUG = True

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],  # 添加这个路径
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'user_messages.context_processors.unread_messages_count',  # 添加这行
            ],
        },
    },
]

# 添加以下配置
ROOT_URLCONF = 'bookmarket.urls'

# 登录相关配置
LOGIN_URL = '/users/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/users/login/'

# 认证相关配置
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]

# Session配置
SESSION_COOKIE_AGE = 1209600  # 两周
SESSION_EXPIRE_AT_BROWSER_CLOSE = False

CRISPY_TEMPLATE_PACK = 'bootstrap4'

# 确保移除重复的 messages 应用

SECRET_KEY = 'djaofjo123fa'