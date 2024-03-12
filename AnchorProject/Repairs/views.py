from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import UserRegisterForm
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from .models import UserProfile, MechanicProfile, Post
from django.http import JsonResponse
import json

# Create your views here.
def home(request):
    if request.user.is_authenticated:
        profile, number = profile_from_user(request.user)
        if number == 2:
            return redirect("mecanic")
        elif number == 1:
            return redirect("owner")
    return render(request, 'home.html', {})

def profile_from_user(user):
    '''
    Recibe un usuario, y regresar el perfil asociado
    - Regresa tupla con primer elemento: perfil,
        segundo elemento: 1 si es usuario, 2 si es mecánico
        Regresa None, None, si no encuentra al perfil
    '''
    consultaPerfilUsuario = UserProfile.objects.filter(user_django_profile=user)
    if consultaPerfilUsuario.exists():
        return (consultaPerfilUsuario.first(), 1)
    consultaPerfilMecanico = MechanicProfile.objects.filter(mec_django_profile=user)
    if consultaPerfilMecanico.exists():
        return (consultaPerfilMecanico.first(), 2)
    return (None, None)

def view_mec(request):
    if request.user.is_authenticated:
        profile, number = profile_from_user(request.user)
        if number == 2:
            posts = Post.objects.filter(mecanic_post=profile)
                # Serialize each post to JSON
                # wth the curve brackets i make it a dictionary intead of a list
            posts_json = {"posts" : [post.to_json() for post in posts]}
            # convert a python dict to a string
            dictionaty_to_jason = json.dumps(posts_json)
            return render(request, 'home_mec.html', {"type_of_user": 2, "posts": dictionaty_to_jason})

        elif number == 1:
            messages.success(request, "There has been a problem!")
            return redirect("owner")


def view_owner(request):
    if request.user.is_authenticated:
        profile, number = profile_from_user(request.user)
        if number == 2:
            messages.success(request, "There has been a problem!")
            return redirect("mecanic")
        elif number == 1:
            posts = Post.objects.filter(user_post=profile).order_by('-date')

            return render(request, 'home_owner.html', {"type_of_user": 1, "posts": posts})
    return render(request, 'home_owner.html', {"type_of_user": 1})

def register_user(request):
    form = UserRegisterForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            user = request.POST['username']
            password = request.POST['password']
            phone = request.POST['phone']
            type_of_user = request.POST['type_of_user']
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']

            # Create user
            user = User.objects.create_user(username=user, password=make_password(password), first_name=first_name, last_name=last_name)
            user.set_password(password)
            user.save()
            # Create profile
            if type_of_user == '1':
                profile = UserProfile(user_django_profile=user, phone=phone)
                profile.save()
                messages.success(request, "You have been registered as a Boat Owner!")
                login(request, user)
                return redirect("owner")
            if type_of_user == '2':
                profile = MechanicProfile(mec_django_profile=user, phone=phone)
                profile.save()
                messages.success(request, "You have been registered as a Mechanic!")
                login(request, user)
                return redirect("mecanic")
    return render(request, 'register.html', {"form": form})

def login_user(request):
    if request.method == 'POST':
        username = request.POST['user_name_login']
        password = request.POST['password_login']
        # authenticate the user
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You have been logged In!")
            # profile and number come from profile_from_user
            profile, number = profile_from_user(user)
            if number == 1:
                return redirect("owner")
            if number == 2:
                return redirect("mecanic")
        else:
            messages.error(request, "There was a problem, try again")
            return render(request, 'login.html', {})
    else:
        if request.user.is_authenticated:
            profile, number = profile_from_user(request.user)
            if number == 1:
                return redirect("owner")
            if number == 2:
                return redirect("mecanic")
        return render(request, 'login.html', {})



def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out")
    return render(request, 'home.html', {})


#view_owner_boat_user

def post(request):
    showmap = True
    if request.user.is_authenticated:
        profile, number = profile_from_user(request.user)
        if number == 2:
            return redirect("mecanic")
        elif number == 1:
            if request.method == 'POST':
                comment = request.POST['comment']
                photo = request.FILES['photo_post']
                latitud = request.POST['latitude']
                longitud = request.POST['longitude']
                date = request.POST['repairtime']

                user = request.user
                # create post
                post = Post(comment=comment, photo=photo, user_post=profile, post_latitud=latitud, post_longitud=longitud, date=date)
                post.save()
                messages.success(request, "Your post has been created")
                return redirect('owner')
            return render(request, 'post_user.html', {'showmap': showmap, "type_of_user": number})
    return redirect('home')



def post_detail(request, id):
    if request.user.is_authenticated:
        profile, number = profile_from_user(request.user)
        if number == 2:
            messages.success(request, "There has been a problem!")
            return redirect("mecanic")
        elif number == 1:
            postdetail = Post.objects.get(id=id)  # Corrected line
            return render(request, 'each_post.html', {'post': postdetail, "type_of_user": number})
    return redirect('home')

def mec_see_open_request_posts(request):
    if request.user.is_authenticated:
        profile, number = profile_from_user(request.user)
        if number == 2:
            posts = Post.objects.filter(status = 0).order_by('-date')
            return render(request, 'open_request_mec.html', {"type_of_user": 2, "posts": posts})
        elif number == 1:
            return redirect("owner")
    return redirect("home")

def mec_accept_post(request, id):
    if request.user.is_authenticated:
        profile, number = profile_from_user(request.user)
        if number == 2:
            post = Post.objects.get(id=id)
            post.mecanic_post = profile
            post.status = 1
            post.save()
            return redirect("mecanic")
        elif number == 1:
            return redirect("owner")
    return redirect("home")
