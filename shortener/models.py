from django.db import models

# Create your models here.
class KirrURL(models.Model):
    url = models.CharField(max_length=200, )
    shortcode = models.CharField(max_length=20,default='cfe')

    def __str__(self):
        return str(self.url)

