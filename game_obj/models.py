from django.db import models


# Create your models here.

class TableModel(models.Model):
    state = models.IntegerField()
    user_name = models.CharField(max_length=200)
    user_hand = models.CharField(max_length=200)
    user_stack = models.CharField(max_length=200)
    player_names = models.CharField(max_length=200)
    player_hands = models.CharField(max_length=200)
    player_stacks = models.CharField(max_length=200)
    phase = models.CharField(max_length=200)
    user_stack_length = models.IntegerField()
    table_log = models.CharField(max_length=400)
    hand_name = models.CharField(max_length=200)

    # Done because Django community won't expose this by default
    objects = models.Manager()
