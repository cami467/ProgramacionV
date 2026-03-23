from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, permission_required
from django.http import JsonResponse
from .models import Usuario, Ciudad
from .forms import RegisterForm, LoginForm

# ─────────────────────────────────────────────
# VISTA: Pagina principal (requiere login)
# ─────────────────────────────────────────────

@login_required  #decorador para proteger rutas
# Definimos una vista llamada home
def home(request):
    #Pagina principal - solo accesible si el usuario esta logueado
    return render(request, 'accounts/home.html',{
        'usuario': request.user,  #diccionario con info del usuario
    })


# ─────────────────────────────────────────────
# VISTA: Registro de usuario
# recibe, valida y guarda datos 
# ─────────────────────────────────────────────
#FUNCION REGISTER
def register(request):
    #Vista para registrar un nuevo usuario
    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid(): # Valida que las contraseñas coincidan, etc
                try:
                    # Extraer datos del formulario validado
                    nombre = form.cleaned_data['nombre']
                    apellido = form.cleaned_data['apellido']
                    correo = form.cleaned_data['correo']
                    password = form.cleaned_data['password1']
                    ciudad = form.cleaned_data['ciudad']

                    # Crear usuario usando el Manager - encripta la contraseña
                    usuario = Usuario.objects.create_user(
                        correo=correo,
                        password=password,
                        nombre=nombre,
                        apellido=apellido,
                        ciudad=ciudad,
                    )
                    # Aquí se autentica al usuario y se inicia su sesión:
                    # Django genera la cookie de sesión y la asocia al navegador,
                    # permitiendo que el usuario permanezca identificado en el sistema
                    login(request, usuario)

                    # En lugar de redirigir a 'home', se retorna un diccionario en formato JSON
                    # esto permite enviar respuestas estructurada al cliente
                    # indicando tanto el mensaje de éxito como el correo del usuario registrado 
                    return JsonResponse({
                        'mensaje': 'Usuario registrado correctamente',
                        'usuario': usuario.correo,
                    })
                except Exception as e:
                    form.add_error(None, f'Error al registrar: {str(e)}')

        # GET o POST con errores: mostrar el formulario
        return render(request, 'accounts/register.html',{
            'form': form,
            'ciudades': Ciudad.objects.all(),
        })

    # GET: mostrar el formulario vacio
    form = RegisterForm()
    return render(request, 'accounts/register.html',{
        'form': form,
        'ciudades': Ciudad.objects.all(),
    })


# ─────────────────────────────────────────────
# VISTA: Login de usuario punto de entrada 
# para que el usuario pueda ser autenticado
# ─────────────────────────────────────────────

#FUNCION VISTA
def login_view(request):
    # Vista para iniciar sesion
    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            correo = form.cleaned_data['correo']
            password = form.cleaned_data['password']

        # authenticate verifica si correo+password son correctos
        # Si coincide con el usuario en la bd, devuelve ese objeto de usuario
        # en caso contrario retorna none
            usuario = authenticate(request, username=correo, password=password)
        
            if usuario is not None:
                # Usuario valida - crear sesión
                login(request, usuario)
                return JsonResponse({
                    'mensaje': 'Login exitoso',
                    'usuario' : usuario.correo,
                })
            else:
                # El video retorno el form con error visible al usuario
                return render(request, 'accounts/login.html',{
                    'form': form,
                    'error': 'Correo o contraseña incorrectos'
                })
            
        return render(request, 'accounts/login.html', {'form': form})
    
    #GET: mostrar formulario vacio
    form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})

# ─────────────────────────────────────────────
# VISTA: Logout vista para cerrar sesión
# ─────────────────────────────────────────────

def logout_view(request):
    # Cerrar sesión y redirigir al login
    logout(request)  # elimina la sesion (cookie)
    return redirect('login')

# ─────────────────────────────────────────────
# VISTA: Eliminar ciudad
# ─────────────────────────────────────────────

@login_required
@permission_required('accounts.delete_ciudad', raise_exception=True)
def delete_ciudad(request):
    if request.method == 'POST':
        ciudad_id = request.POST.get('ciudad_id')
        try:
            ciudad = Ciudad.objects.get(id=ciudad_id)
            ciudad.delete()
            messages.success(request, f'La ciudad "{ciudad.nombre}" ha sido eliminada correctamente.')
        except Ciudad.DoesNotExist:
            messages.error(request, 'La ciudad que intentas eliminar no existe.')
        except Exception as e:
            messages.error(request, f'Error al eliminar la ciudad: {str(e)}')
        return redirect('delete_ciudad')

    ciudades = Ciudad.objects.all()
    return render(request, 'accounts/delete_ciudad.html', {'ciudades': ciudades})
