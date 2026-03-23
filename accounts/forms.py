from django import forms
from .models import Usuario, Ciudad


class RegisterForm(forms.Form):

#---------Formulario para registrar un nuevo usuario------------

    #forms.CharField le dice a django que sera un campo string
    nombre = forms.CharField( # Campo de formulario llamado 'nombre'
        max_length=100, # El texto no puede superar con 100 caracteres
        widget=forms.TextInput( #Usamos cuadro de texto como entrada
            attrs={             # Atributos HTML para personalizar el input
            'class': 'form-control',    # Clase CSS(ej: estilo de Bootstrap)
            'placeholder': 'Ingresa tu nombre', # texto que aparece como guía dentro del campo
        })
    )
    apellido = forms.CharField( #Es un tipo de campo de formulario en Django que se usa para guardar texto corto
        max_length=100,
        widget=forms.TextInput(
            attrs={
            'class': 'form-control',
            'placeholder': 'Ingresa tu apellido',
        })
    )
    correo = forms.CharField(
        widget=forms.EmailInput(
            attrs={
            'class': 'form-control',
            'placeholder': 'correo@ejemplo.com',
        })
    )
    #ModelChoiceField: campo de selección basado en un modelo, cuando quieres que el usuario elija un objeto en la base de datos
    #queryset: Define que objetos van a aparecer como opciones en ese campo
    ciudad = forms.ModelChoiceField(
        queryset=Ciudad.objects.all(), # trae todas las ciudades guardadas en la bd y muestralos en el menu desplegable
        widget=forms.Select(attrs={'class': 'form-control'}),
        empty_label='-- Selecciona tu ciudad --',        
    )
    password1 = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Minimo 8 caracteres',
        })
    )
    password2 = forms.CharField(
        label= 'Confirmar contraseña',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Repite la contraseña'
        })
    )

    def clean(self):
        #Validación: las dos contraseñas deben coincidir
        cleaned = super().clean() #Llama al metodo clean() original de Django y obtiene los datos ya validados
        p1 = cleaned.get('password1') # recupera el valor del campo 'password1' del formulario
        p2 = cleaned.get('password2')

        # Si ambos campos existen y no son iguales, lanza un error de validación
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError('Las contraseñas no coinciden')
        # Devuelve los datos limpios y validados para que django los utilice
        return cleaned
    
#-----------------FORMULARIO DE LOGIN----------------------------

class LoginForm(forms.Form):

    #Formulario para iniciar sesión

    # Campo de formulario para el correo electrónico
    correo = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class':'form-control',
            'placeholder' : 'Tu correo registrado',
        })
    )
    # Campo de formulario para la contraseña
    password = forms.CharField(
        label= 'Contraseña',
        widget=forms.PasswordInput(attrs={  # Usamos un input tipo "password" (oculta los caracteres)
            'class': 'form-control',
            'placeholder': 'Tu contraseña',
        })
    )