from django.db import models

# Create your models here.
class Map(models.Model):
	x = models.IntegerField()
	y = models.IntegerField()
	image = models.ImageField(upload_to='map_images/', default='pic_folder/no-img.jpg')
