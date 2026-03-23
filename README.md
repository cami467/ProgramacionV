# Sistema de Registro y Login — Django

# Datos
- Alumna: Camila Noel Benitez Aguilera
- Materia: Programación 5
- Fecha de revisión: [26-03-2026]

---

# Descripción
Sistema web desarrollado en Django 5.2 que implementa registro y login de usuarios.
Incluye el modelo Ciudad relacionado mediante ForeignKey al modelo Usuario.
Las contraseñas se almacenan encriptadas usando PBKDF2 con SHA256 a través de `set_password()`.

---

# Tecnologías
- Python 3.13.7 
- Django 5.2
- PostgreSQL 
- Bootstrap 5.3

---

# Estructura del Proyecto

```

```
PROGRAMACIONV/ Nombre del proyecto
|
├── Programacion5TN/          # Carpeta de configuración del proyecto
│   ├──__init__.py
│   ├── settings.py          # Configuración global del proyecto(BD, templates, static)
│   ├── urls.py              # URLs padre — incluye las rutas de accounts
│   ├── wsgi.py              # Configuración para servidores web
│   └── asgi.py              # Configuración para servidores async
|   
|   
|
├── accounts/                 # App principal
|   ├── models.py             # Modelos Ciudad y Usuario
|   ├── views.py              # Vistas register, login, logout, home
|   ├── forms.py              # Formularios RegisterForm y LoginForm
|   ├── urls.py               # URLs hijas de la app
|   ├── admin.py              # Registro de modelos en el panel admin
|   ├── migrations/           # Migraciones generadas automáticamente
|   └── templates/
|       └── accounts/
|           ├── base.html
|           ├── delete_cuidad.html
|           ├── register.html
|           ├── login.html
|           └── home.html
|
├── static/                   # Archivos estáticos (CSS, JS, imágenes)
├── venv/                     # Entorno virtual
├── db.sqlite3   
├── Documentacion_django.docx    
├── Documentacion_django.pdf          
├── manage.py
└── README.md
```

---

## Modelos

### Ciudad
| Campo   | Tipo        | Detalle                        |
|---------|-------------|--------------------------------|
| nombre  | CharField   | max_length=100, unique=True    |

### Usuario
| Campo      | Tipo           | Detalle                                      |
|------------|----------------|----------------------------------------------|
| nombre     | CharField      | max_length=100                               |
| apellido   | CharField      | max_length=100                               |
| edad       | IntegerField   | null=True, blank=True                        |
| telefono   | CharField      | max_length=20, null=True, blank=True         |
| correo     | EmailField     | unique=True — campo de login (USERNAME_FIELD)|
| ciudad     | ForeignKey     | → Ciudad, on_delete=SET_NULL                 |
| is_active  | BooleanField   | default=True                                 |
| is_staff   | BooleanField   | default=False                                |
| created_at | DateTimeField  | auto_now_add=True                            |

**Nota de seguridad:** La contraseña es manejada internamente por `AbstractBaseUser`.
No se define como campo manual. Se encripta con `set_password()` en `UsuarioManager`.

---

## Clases de Autenticación

### UsuarioManager (hereda de BaseUserManager)
Maneja la lógica de creación de usuarios.
- `create_user()` — encripta la contraseña con `set_password()` antes de guardar
- `create_superuser()` — crea un administrador con `is_staff=True`

### Usuario (hereda de AbstractBaseUser + PermissionsMixin)
- `AbstractBaseUser` — da soporte para autenticación (login, logout, sesiones)
- `PermissionsMixin` — agrega `is_superuser` y manejo de grupos
- `USERNAME_FIELD = 'correo'` — el login se hace con correo en lugar de username
- `objects = UsuarioManager()` — usa el manager personalizado

---

## Vistas

| Vista         | Método | Descripción                                              |
|---------------|--------|----------------------------------------------------------|
| `home`        | GET    | Página principal, protegida con `@login_required`        |
| `register`    | GET    | Muestra el formulario de registro vacío                  |
| `register`    | POST   | Valida datos, crea usuario y devuelve `JsonResponse`     |
| `login_view`  | GET    | Muestra el formulario de login vacío                     |
| `login_view`  | POST   | Autentica usuario y devuelve `JsonResponse`              |
| `logout_view` | GET    | Elimina la sesión y redirige al login                    |

### Salida tipo diccionario (JsonResponse)
El profesor pide que las vistas devuelvan un diccionario al completarse con éxito:

```python
# Registro exitoso
return JsonResponse({
    'mensaje': 'Usuario registrado correctamente',
    'usuario': usuario.correo,
})

# Login exitoso
return JsonResponse({
    'mensaje': 'Login exitoso',
    'usuario': usuario.correo,
})
```

---

## URLs

| URL                    | Vista         | Nombre     |
|------------------------|---------------|------------|
| /accounts/             | home          | home       |
| /accounts/register/    | register      | register   |
| /accounts/login/       | login_view    | login      |
| /accounts/logout/      | logout_view   | logout     |

---

## Configuración destacada en settings.py

```python
AUTH_USER_MODEL = 'accounts.Usuario'   # modelo de usuario personalizado
LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/accounts/'
```

---



---

## Progreso

### [fecha]
- [18/03/2026] Entorno virtual creado y activado — se ve `(venv)` en CMD
- [18/03/2026] Django 5.2 instalado (`pip show django`)
- [18/03/2026] Proyecto `config` y app `accounts` creados
- [18/03/2026] `settings.py` configurado (BD, templates, static, AUTH_USER_MODEL)
- [18/03/2026] `config/urls.py` con `include('accounts.urls')`
- [18/03/2026] Modelos `Ciudad` y `Usuario` creados en `models.py`
- [19/03/2026] `UsuarioManager` con `set_password()` implementado
- [19/03/2026] Migración ejecutada sin errores
- [20/03/2026] Tablas `accounts_ciudad` y `accounts_usuario` verificadas en el gestor
- [20/03/2026] Superusuario creado con `createsuperuser`
- [21/03/2026] `forms.py` con `RegisterForm` y `LoginForm`
- [21/03/2026] Vistas `register`, `login_view`, `logout_view` y `home` funcionando
- [21/03/2026] `JsonResponse` implementado en register y login
- [21/03/2026] Templates con Bootstrap: `base.html`, `register.html`, `login.html`, `home.html`, `delete_ciudad.html`
- [21/03/2026] `@login_required` protegiendo la vista `home`

