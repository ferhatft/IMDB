from django.db import models
from django.template.defaultfilters import slugify
from django_comments_xtd.models import XtdComment
from star_ratings.models import Rating
# Create the Movie model

    
class Actor(models.Model):
    name = models.CharField(max_length=70, blank=True)
    image = models.ImageField(max_length=100, upload_to='actor/')

    def __str__(self):
        return '%s %s' % (self.name, self.id)

    class Meta:
        ordering = ['name']
        verbose_name = 'Actor'
        verbose_name_plural = 'Actors'


class Movie(models.Model):
    title = models.CharField(max_length=255)
    slug  = models.SlugField(blank=True, null=True)
    image = models.ImageField(null=True)
    release_year = models.IntegerField()
    director = models.CharField(max_length=255)
    actors = models.ManyToManyField(Actor, related_name='movies', blank=True)
    plot = models.TextField()
    # subject = 
    time = models.CharField(max_length=50, null=True)
    
    comments = models.ManyToManyField(XtdComment, blank=True)
    ratings = models.OneToOneField(Rating, on_delete=models.CASCADE, null=True, blank=True)


    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):

        title =  slugify(self.title)
        self.slug = title
        
        if not self.ratings:
            self.ratings = Rating.objects.create()
        super(Movie, self).save(*args, **kwargs)

        return super(Movie, self).save(*args, **kwargs)
    
    
        
    def get_absolute_url(self):
        if self.slug:
            return "/movies/{str}".format(str=self.slug)

    class Meta:
        ordering = ['id']
        verbose_name = 'Movie'
        verbose_name_plural = 'Movies'
    
    

# Create the TVShow model
class TVShow(models.Model):
    title = models.CharField(max_length=255)
    slug  = models.SlugField(blank=True, null=True)
    image = models.ImageField(null=True)
    release_year = models.IntegerField()
    director = models.CharField(max_length=255)
    actors = models.ManyToManyField(Actor, related_name='tvshows', blank=True)
    plot = models.TextField()
    # subject = 
    time = models.CharField(max_length=50, null=True)
    
    comments = models.ManyToManyField(XtdComment, blank=True)
    ratings = models.OneToOneField(Rating, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.title

    
    def save(self, *args, **kwargs):

        title =  slugify(self.title)
        self.slug = title
        
        if not self.ratings:
            self.ratings = Rating.objects.create()
            
        return super(TVShow, self).save(*args, **kwargs)
        
    def get_absolute_url(self):
        if self.slug:
            return "/tvshows/{str}".format(str=self.slug)

    class Meta:
        ordering = ['id']
        verbose_name = 'TVShow'
        verbose_name_plural = 'TVShows'
    
    