# -*- coding: utf-8 -*-
from __future__ import unicode_literals


import datetime

from django.db import models
from django.utils.encoding import python_2_unicode_compatible

from django.utils import timezone
# Create your models here.

#each database table has a model which is nothing but a class
@python_2_unicode_compatible  # only if you need to support Python 2
class Question(models.Model):

	question_text = models.CharField(max_length = 100)
	pub_date = models.DateTimeField('date published')

	def was_published_recently(self):
		return timezone.now() - datetime.timedelta(days=1) <= self.pub_date <= timezone.now()

	def __str__(self):
		return self.question_text

@python_2_unicode_compatible  
class Choices(models.Model):

	question_number  = models.ForeignKey(Question, on_delete = models.CASCADE)
	choice_text = models.CharField(max_length = 100)
	votes = models.IntegerField(default  = 0)

	def __str__(self):
		return self.choice_text


