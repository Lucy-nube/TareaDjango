"""
WSGI config for TareaDjango project.
"""

import os
from django.core.wsgi import get_wsgi_application

# Cambiamos 'config.settings' por 'TareaDjango.settings'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TareaDjango.settings')

application = get_wsgi_application()

# --- BLOQUE PARA CREAR EL ADMIN AUTOMÁTICAMENTE ---
try:
    from django.contrib.auth import get_user_model
    User = get_user_model()

    # Define aquí tus credenciales
    username = "admin"
    email = "admin@ejemplo.com"
    password = "TuPasswordSegura123" 

    if not User.objects.filter(username=username).exists():
        User.objects.create_superuser(username, email, password)
        print(f"✅ Superusuario '{username}' creado exitosamente")
    else:
        # Si ya existe pero no recuerdas la clave, puedes cambiar el 'username' arriba a 'admin2'
        print(f"ℹ️ El superusuario '{username}' ya existe")
except Exception as e:
    print(f"❌ Error al intentar crear el superusuario: {e}")