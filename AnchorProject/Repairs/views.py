from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import UserRegisterForm
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from .models import  UserProfile, MechanicProfile


# Create your views here.
def home(request):
    return render(request, 'home.html', {})

def register_user(request):
    if request.method == 'GET':
        form = UserRegisterForm()
        return render(request, 'register.html', {'form': form})

    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            # se guarda el usuario con el nombre y la contrasena porque el toggle no es parte de usuraio de django
            # user = form.save(commit=False)
            # us cliente o mecanico?
            user = User.objects.create(
                    username= request.POST['username'],
                    password = make_password(request.POST['password'])
                )
            if request.POST['type_of_user'] == 1:
                # quiero guardar el usuario con todo y perfil y todo viene de request.POST
                user_complementado = UserProfile.objects.create(
                    phone = request.POST['phone_number'],
                    # linkear_el_user_django
                    user_django_profile = user
                )







def loging_user(request):
    pass

def logout_ser(request):
    pass
