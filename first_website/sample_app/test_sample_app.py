import datetime
from django.test import TestCase
from django.utils import timezone

from .models import Question, Choices

class QuestionMethodTests(TestCase):

	def test_was_published_recently_for_future_question(self):
		future_pub_date = timezone.now() + datetime.timedelta(days = 5)
		test_object = Question(pub_date = future_pub_date)
		self.assertIs(test_object.was_published_recently(),False)

	def test_was_published_recently_with_old_question(self):
		old_date = timezone.now() - datetime.timedelta(days = 5)
		test_object = Question(pub_date = old_date)
		self.assertIs(test_object.was_published_recently(),False)

	def test_was_published_recently_with_recent_question(self):
		recent_date = timezone.now() - datetime.timedelta(hours = 3)
		test_object = Question(pub_date = recent_date)
		self.assertIs(test_object.was_published_recently(),True)
