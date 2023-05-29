from django.db import models
from django.template.defaultfilters import slugify

# Create the Movie model
class Movie(models.Model):
    title = models.CharField(max_length=255)
    slug  = models.SlugField(blank=True, null=True)
    image = models.ImageField(null=True)
    release_year = models.IntegerField()
    director = models.CharField(max_length=255)
    actors = models.CharField(max_length=255)
    plot = models.TextField()
    time = models.CharField(max_length=50, null=True)

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):

        title =  slugify(self.title)
        self.slug = title

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
    actors = models.CharField(max_length=255,null=True,verbose_name="cast")
    plot = models.TextField()
    time = models.CharField(max_length=50, null=True)
    

    def __str__(self):
        return self.title

    
    def save(self, *args, **kwargs):

        title =  slugify(self.title)
        self.slug = title

        return super(TVShow, self).save(*args, **kwargs)
        
    def get_absolute_url(self):
        if self.slug:
            return "/tvshows/{str}".format(str=self.slug)

    class Meta:
        ordering = ['id']
        verbose_name = 'TVShow'
        verbose_name_plural = 'TVShows'
    