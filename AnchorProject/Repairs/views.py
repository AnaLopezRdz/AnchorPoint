from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import UserRegisterForm
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from .models import  UserProfile, MechanicProfile, Post


# Create your views here.
def home(request):
    return render(request, 'home.html', {})
def profile_from_user(user):
    '''
    Recibe un usuario, y regresar el perfil asociado
    - Regresa tupla con primer elemento: perfil,
        segundo elemento: 1 si es usuario, 2 si es mecánico
        Regresa None, None, si no encuentra al perfil
    '''
    consultaPerfilUsuario = UserProfile.objects.filter(user_django_profile = user)
    if consultaPerfilUsuario.count() > 0:
        return (consultaPerfilUsuario[0], 1)
    consultaPerfilMecanico = MechanicProfile.objects.filter(mec_django_profile = user)
    if consultaPerfilUsuario.count() > 0:
        return (consultaPerfilMecanico[0], 2)
    return (None, None)

def view_mec(request):
    return render(request, 'home_mec.html', {"type_of_user": 2})

def view_owner(request):
    return render(request, 'home_owner.html', {"type_of_user": 1})


def register_user(request):
    form = UserRegisterForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            user = request.POST['username']
            password = request.POST['password']
            phone = request.POST['phone']
            type_of_user = request.POST['type_of_user']
            # Create user
            user = User.objects.create_user(username = user, password = make_password(password))
            user.save()
            # Create profile
            if type_of_user == '1':
                profile = UserProfile(user_django_profile = user, phone = phone)
                profile.save()
                messages.success(request, "You have been registered as a Boat Owner!")
                return redirect ("mecanic")
                # return render(request, 'home_owner.html', {"type_of_user": type_of_user})
            if type_of_user == '2':
                profile = MechanicProfile(mec_django_profile = user, phone = phone)
                profile.save()
                messages.success(request, "You have been registered as a Mechanic!")
                return redirect ("owner")
                # return render(request, 'home_mec.html', {"type_of_user": type_of_user})



    return render(request, 'register.html', {"form":form})




def login_user(request):
    if request.method == 'POST':
        username = request.POST['user_name_login']
        password = request.POST['password_login']
        # authenticate the user
        user = authenticate(request, username = username, password = password)
        if user is not None:
            login(request, user)
            messages.success(request, "You have been logged In!")
            # profile and number come from profile_from_user
            profile, number = profile_from_user(user)
            if number == 1:
                # return render(request, 'home_owner.html', {})
                return redirect ("owner")
            if number == 2:
                # return render(request, 'home_mec.html', {})
                return redirect ("mecanic")
        else:
            messages.success(request, "There was a problem, try again")


            return render(request, 'login.html', {})


    return render(request, 'login.html', {})




def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out")
    return render(request, 'home.html', {})

def post(request):
    showmap = True
    # see the type of user to see the correct nav bar
    if request.user != None:
        profile, number = profile_from_user(request.user)
        if number == 2:
            return redirect ("mecanic")
        elif number == 1:
            if request.method == 'POST':
                # what do i get from post?
                comment = request.POST['comment']
                photo = request.FILES['photo']
                latitud = request.POST['latitud']
                longitud = request.POST['longitud']
                user = request.user
                # create post
                post = Post(comment = comment, photo = photo, user_post = profile, post_latitud = latitud, post_longitud = longitud)
                post.save()
                messages.success(request, "Your post has been created")
                return render(request, 'home_owner.html', {'showmap' : showmap, "type_of_user": number})

            # I pass map and user, user for the nav bar, and map to show the mapas argumen
            return render(request, 'post_user.html', {'showmap' : showmap, "type_of_user": number})
    return redirect ('home')
