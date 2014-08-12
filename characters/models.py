from django.db import models

class FighterClasses(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
    	return self.name

class Character(models.Model):
    user_id = models.IntegerField(default=0)
    character_class_id = models.ForeignKey(FighterClasses)
    name = models.CharField(max_length=100, unique=True)
    image = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
    	return self.name