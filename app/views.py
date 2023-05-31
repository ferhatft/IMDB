from random import shuffle

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator
from django.db.models import Avg, Q
from django.shortcuts import redirect, render
from django_comments_xtd.forms import XtdCommentForm
from django_comments_xtd.models import XtdComment
from star_ratings.models import Rating

from .forms import SearchForm
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
    
    # Retrieve movie ratings and sort by average ratings
    movie_ratings = Rating.objects.filter(content_type__model='movie').order_by('-average')[:10]
    
    print(movie_ratings)
    
    # Retrieve TV show ratings and sort by average ratings
    tv_show_ratings = Rating.objects.filter(content_type__model='tvshow').order_by('-average')

    # Extract movie objects from ratings
    sorted_movies = [rating.content_object for rating in movie_ratings]

    # Extract TV show objects from ratings
    sorted_tv_shows = [rating.content_object for rating in tv_show_ratings]


    context = {
        'all_objects':all_objects,
        'all_movies': all_movies,
        'all_tv_shows': all_tv_shows,
        'slider_objects':slider_objects,
        'sorted_movies': sorted_movies,
        'sorted_tv_shows': sorted_tv_shows,
    }
    return render(request, 'anasayfa.html', context)

def movie_details(request, slug):
    obj = Movie.objects.get(slug=slug)
    movie_content_type = ContentType.objects.get_for_model(obj) # This is where movie_content_type is defined
    comments = XtdComment.objects.filter(content_type=movie_content_type, object_pk=obj.pk)
    rating = obj.ratings
    print(rating)
    
    # if obj.ratings else None
    

    if request.method == 'POST': 
        comment = request.POST.get('comment')
        new_comment = XtdComment.objects.create(
            content_type= ContentType.objects.get_for_model(obj),
            object_pk=obj.id,
            comment=comment,
            site_id=1,  # Update this value according to your SITE_ID
            user=request.user
        )
    
    form = XtdCommentForm(target_object=obj)

    context = {
        'obj': obj,
        'comments': comments,
        'rating': rating,
        'form': form,
    }
    return render(request, "movie-tvshows-details.html", context)

def tvshows_details(request, slug):
    obj = TVShow.objects.get(slug=slug)
    tvshow_content_type = ContentType.objects.get_for_model(obj) # This is where tvshow_content_type is defined
    comments = XtdComment.objects.filter(content_type=tvshow_content_type, object_pk=obj.pk)
    rating = obj.ratings.rating if obj.ratings else None

    if request.method == 'POST':
        comment = request.POST.get('comment')
        new_comment = XtdComment.objects.create(
            content_type= ContentType.objects.get_for_model(obj),
            object_pk=obj.id,
            comment=comment,
            site_id=1,  # Update this value according to your SITE_ID
            user=request.user
        )
    
    form = XtdCommentForm(target_object=obj)
    context = {
        'obj': obj,
        'comments': comments,
        'rating': rating,
        'form':form,
    }
    return render(request, "movie-tvshows-details.html", context)


def search(request):
    
    
    # Get all movie and TV show objects for the slider
    all_movies = Movie.objects.all()
    all_tv_shows = TVShow.objects.all()

    all_objects = list(all_movies) + list(all_tv_shows)
    shuffle(all_objects)
    

    
    # Retrieve movie ratings and sort by average ratings
    movie_ratings = Rating.objects.filter(content_type__model='movie').order_by('-average')[:10]
    
    print(movie_ratings)
    
    # Retrieve TV show ratings and sort by average ratings
    tv_show_ratings = Rating.objects.filter(content_type__model='tvshow').order_by('-average')

    # Extract movie objects from ratings
    sorted_movies = [rating.content_object for rating in movie_ratings]

    # Extract TV show objects from ratings
    sorted_tv_shows = [rating.content_object for rating in tv_show_ratings]


    
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['query']
            all_movies = Movie.objects.filter(
                Q(title__icontains=query) |
                Q(director__icontains=query) |
                Q(actors__icontains=query)
            )
            all_tv_shows = TVShow.objects.filter(
                Q(title__icontains=query) |
                Q(director__icontains=query) |
                Q(actors__icontains=query)
            )
    
            context = {
                'all_objects':all_objects,
                'all_movies': all_movies,
                'all_tv_shows': all_tv_shows,
                'sorted_movies': sorted_movies,
                'sorted_tv_shows': sorted_tv_shows,
                'SearchForm': form,
                'query': query,
            }
            return render(request, 'searchdetail.html', context)
    else:
        form = SearchForm()
        context = {
            'SearchForm': form,
        }
    
        return render(request, 'search.html', context)



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



