import os
from django.core.wsgi import get_wsgi_application

# CORRECCIÓN: Ahora apunta a tu carpeta real 'config'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

application = get_wsgi_application()

# --- BLOQUE PARA CREAR EL ADMIN AUTOMÁTICAMENTE ---
try:
    from django.contrib.auth import get_user_model
    User = get_user_model()

    username = "admin"
    email = "admin@ejemplo.com"
    password = "TuPasswordSegura123" 

    if not User.objects.filter(username=username).exists():
        User.objects.create_superuser(username, email, password)
        print(f"✅ Superusuario '{username}' creado exitosamente")
    else:
        print(f"ℹ️ El superusuario '{username}' ya existe")
except Exception as e:
    # Nota: Es normal que esto imprima un error durante el 'build', 
    # lo importante es que funcione cuando Gunicorn arranque.
    print(f"ℹ️ Nota sobre superusuario: {e}")