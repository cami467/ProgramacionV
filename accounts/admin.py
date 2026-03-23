from django.contrib import admin

from .models import Ciudad, Usuario


#──────────────────────────────────────────────────────────────────────────────────────────
# Registramos el modelo Ciudad en el panel de administración
# Esto permite crear, editar y eliminar ciudades desde la interfaz gráfica de Django.
#──────────────────────────────────────────────────────────────────────────────────────────
admin.site.register(Ciudad)

#──────────────────────────────────────────────────────────────────────────────────────────
# Registramos el modelo Usuario en el panel de administración
# Asi podemos gestionar usuarios fácilmente sin usar la consola ni consultas manuales
#──────────────────────────────────────────────────────────────────────────────────────────
admin.site.register(Usuario)
