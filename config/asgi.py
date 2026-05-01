import os
from django.core.wsgi import get_wsgi_application


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

application = get_wsgi_application()


try:
    from django.contrib.auth import get_user_model
    User = get_user_model()
    if not User.objects.filter(username="admin").exists():
        User.objects.create_superuser("admin", "admin@admin.com", "TuPassword123")
        print("✅ Superusuario 'admin' creado exitosamente")
except Exception as e:
    print(f"ℹ️ Nota sobre el admin: {e}")