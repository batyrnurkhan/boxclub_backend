from django.db import models

# Create your models here.
class News(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    photo = models.ImageField(upload_to='news_photos/', blank=True, null=True)

    def __str__(self):
        return self.title