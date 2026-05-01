import os
from django.core.wsgi import get_wsgi_application

# CORRECCIÓN: Ahora apunta correctamente a la carpeta 'config'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

application = get_wsgi_application()

# --- BLOQUE PARA CREAR EL ADMIN AUTOMÁTICAMENTE ---
try:
    from django.contrib.auth import get_user_model
    User = get_user_model()

    # Credenciales para tu panel
    username = "admin"
    email = "admin@ejemplo.com"
    password = "TuPasswordSegura123" 

    if not User.objects.filter(username=username).exists():
        User.objects.create_superuser(username, email, password)
        print(f"✅ Superusuario '{username}' creado exitosamente")
    else:
        print(f"ℹ️ El superusuario '{username}' ya existe")
except Exception as e:
    # Es normal ver una nota aquí durante el despliegue inicial
    print(f"ℹ️ Nota sobre superusuario: {e}")