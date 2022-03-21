from django.db import models


# Create your models here.

class PlayerModel(models.Model):
    name = models.CharField(max_length=200)
    hand_name = models.CharField(max_length=100)
    hand = models.CharField(max_length=200)
    stack = models.IntegerField()
    phase = models.CharField(max_length=200)
    # Done because Django community won't expose this by default
    objects = models.Manager()
