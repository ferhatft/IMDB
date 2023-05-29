from random import shuffle

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.shortcuts import redirect, render

from .models import Movie, TVShow

# Create your views here.

def home(request):

    # Get all movie and TV show objects for the slider
    all_movies = Movie.objects.all()
    all_tv_shows = TVShow.objects.all()

    all_objects = list(all_movies) + list(all_tv_shows)
    shuffle(all_objects)
    

    
    # Get the first 3 objects for the slider
    slider_objects = all_objects[:3]
    context = {
        'all_objects':all_objects,
        'all_movies': all_movies,
        'all_tv_shows': all_tv_shows,
        'slider_objects':slider_objects,
    }
    return render(request, 'anasayfa.html', context)


def movie_details(request,slug):
    obj = Movie.objects.get(slug=slug)
    context = {
        'obj':obj,
    }
    return render(request, "movie-tvshows-details.html",context)

def tvshows_details(request,slug):
    obj = TVShow.objects.get(slug=slug)
    context = {
        'obj':obj,
    }
    return render(request, "movie-tvshows-details.html",context)




def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password != password2:
            messages.error(request, "Parolalar eşleşmiyor")
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Kullanıcı adı zaten alınmış")
            return redirect('register')

        user = User.objects.create_user(username=username, password=password)
        user.save()
        messages.success(
            request, "Başarıyla kayıt oldunuz. Şimdi giriş yapabilirsiniz.")
        return redirect('login')
    else:
        return render(request, 'register.html')


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username, password)

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            print(username, password)
            return redirect('home') 
        else:
            return render(request, 'login.html', {'error': 'Kullanıcı adı veya parola hatalı.'})
    else:
        return render(request, 'login.html')




def user_logout(request):
    logout(request)
    return redirect('login')



