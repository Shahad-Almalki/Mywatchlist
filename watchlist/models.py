from django.db import models


class Status(models.Model):
    name = models.CharField(80)

#Makes Django admin / shell print the name instead of Status object (1).
    def __str__(self):
        return self.name

class Cast(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
#TYPE_CHOICES restricts the type field to either “Movie” or “Series”.
class WatchItem(models.Model):
    TYPE_CHOICES = [
        ('Movie', 'Movie'),
        ('Series', 'Series'),
    ]
    title= models.CharField(max_length=200)
    type= models.CharField(max_length=50, choices=TYPE_CHOICES )
    year= models.IntegerField()
    genre= models.CharField(max_length=100)
    rating= models.FloatField()

# Lets me upload a local poster image to MEDIA_ROOT/posters/.
    poster= models.ImageField(upload_to='posters/', blank=True, null= True)

# Stores a URL for external poster images (TMDB).
    poster_url = models.URLField(blank=True, null=True)

# Links each movie to a Status (one-to-many).
# many movies can have the same Status.
    status= models.ForeignKey(Status, on_delete=models.CASCADE)

# Links each movie to multiple cast members.
#a movie can have many actors, and an actor can appear in many movies.
    cast= models.ManyToManyField(Cast, blank=True)


    def __str__(self):
        return self.title
# print the title when you look at the object.