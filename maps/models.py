from django.db import models

# Create your models here.
class MapModel(models.Model):
	x = models.IntegerField()
	y = models.IntegerField()
	image = models.ImageField(upload_to='map_images/', default='pic_folder/no-img.jpg')

	def __str__(self):
		return '%s %s' % (self.x, self.y)