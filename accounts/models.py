from django.db import models

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


# ──────────────────────────────────────────────────────────────────────────────────────────

# - AbstractBaseUser → Es la clase base que te permite crear tu propio modelo 
# de usuario personalizado desde cero.
# - BaseUserManager → Es el administrador que define cómo se crean y gestionan
#  los usuarios (por ejemplo, create_user y create_superuser).
# - PermissionsMixin → Añade soporte para permisos y grupos, permitiendo saber 
# si un usuario tiene ciertos privilegios.
# ──────────────────────────────────────────────────────────────────────────────────────────



# ─────────────────────────────────────────────
# MODELO 1: Ciudad
# ─────────────────────────────────────────────

class Ciudad(models.Model):
 # unique=True impide que haya dos ciudades con el mismo nombre
    nombre = models.CharField(max_length=100, unique=True)
    class Meta:
        verbose_name = 'Ciudad'
        verbose_name_plural = 'Ciudades'
        ordering = ['nombre'] # orden alfabetico en el admin
    def __str__(self):
    # __str__ muestra el nombre en lugar de 'Ciudad object(1)'
        return self.nombre

# ─────────────────────────────────────────────
# MANAGER: maneja la logica de creacion de usuarios
# Esto va en el modelo para que
# los controladores sean mas simples
# ─────────────────────────────────────────────

class UsuarioManager(BaseUserManager):
    def create_user(self, correo, password=None, **extra_fields):
    #Crea y guarda un usuario normal
        if not correo:
         raise ValueError('El correo es obligatorio')
        
        # normalize_email convierte el dominio a minusculas
        correo = self.normalize_email(correo)

        # Crea la instancia del usuario pero NO la guarda aun
        usuario = self.model(correo=correo, **extra_fields)

        # set_password encripta la contrasena automaticamente
        # NUNCA guardes la contrasena en texto plano
        usuario.set_password(password)

        usuario.save(using=self._db)
        return usuario

    def create_superuser(self, correo, password=None, **extra_fields):
        #Crea un superusuario (administrador)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_superuser', True) #le da permiso de administrador a django
        return self.create_user(correo, password, **extra_fields)
    
    # ─────────────────────────────────────────────
# MODELO 2: Usuario
# AbstractBaseUser: da soporte para autenticacion
# PermissionsMixin: agrega is_superuser y grupos
# ─────────────────────────────────────────────

class Usuario(AbstractBaseUser, PermissionsMixin):

    # ── Datos personales ──────────────────────
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    edad     = models.IntegerField(null=True, blank=True)
    telefono = models.CharField(max_length=20, null=True, blank=True)

    # ── Credencial principal (reemplaza al 'username') ──
    correo = models.EmailField(unique=True)  #login con correo
    #La contrasena la maneja AbstractBaseUser internamente
    #NO agregues un campo 'password' manualmente

    # ── Relacion con Ciudad (ForeignKey) ──────
    # on delete=SET NULL: si se elimina la ciudad,
    # el usuario queda con ciudad=None (no se elimina)
    ciudad=models.ForeignKey(
        Ciudad,   # Relacion hacia el modelo ciudad
        on_delete=models.SET_NULL,  # Si se borra la ciudad, este campo queda en NULL en lugar de borrar el usuario 
        null=True,    # Permite que el campo quede vacío en la bd
        blank=True,   #Permite que el campo se deje en blanco en formularios
        related_name='usuarios',    # Nombre para acceder desde Ciudad a todos sus usuarios relacionados
    )

    # ── Control de cuenta ─────────────────────

    # Indica si el registro está activo o no
    #BooleanField almacena valores True/False
    is_active = models.BooleanField(default=True)

    # Indica si el usuario es parte del personal administrativo
    # Debe ser BoolenaField, no BigAutoField
    is_staff  = models.BooleanField(default=False)

    #Guarda automaticamente la fecha y la hora en que se creó el registro
    # auto_now_add=True hace que se asigne el valor al momento de la creación
    created_at = models.DateTimeField(auto_now_add=True)


    # ── Configuracion del Manager ───────────── "Manager: es quien se encarga de crear, buscar y manejar los usuarios en la base de datos"
    objects = UsuarioManager() # usar nuestro manager

    # Normalmente django usa 'username', pero aqui le decimos que el login sea con el correo
    # login con correo (no username), define el campo donde inicia sesión
    USERNAME_FIELD = 'correo'  

    # Campos obligatorios que se deben pedir al crear usuario con el comando createsuperuser
    # Ademas del USERNAME_FIELD (correo), tembién se pedirá nombre y apellido
    REQUIRED_FIELDS = ['nombre', 'apellido']

    # Sirve para darle un nombre más amigable al modelo
    class Meta: 
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
    
    # _str_ sirve para mostrar una representación en texto legible del objeto, ejemplo: "Camila Gómez - camila@gmail.com"
    def __str__(self):
        return f'{self.nombre} {self.apellido} - {self.correo}'


