# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models



class ChoiceLimit(models.Model):
    choice = models.IntegerField(default=10)
    #api_key = models.CharField(max_length=100)