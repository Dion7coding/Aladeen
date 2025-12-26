import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aladeen_project.settings')
django.setup()

from django.contrib.auth.models import User

username = 'admin123'
password = 'admin@1#'
email = 'admin@example.com'

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, email=email, password=password)
    print(f'Superuser {username} created.')
else:
    print(f'Superuser {username} already exists.')
