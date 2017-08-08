import datetime
from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .models import Question, Choices

def create_question(question_text,days):
	time = timezone.now() + datetime.timedelta(days = days)
	return Question.objects.create(question_text = question_text, pub_date = time)

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

	def test_index_view_with_no_questions(self):
		response = self.client.get(reverse('sample_app:home_page'))
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, "No polls are available.")
		self.assertQuerysetEqual(response.context['question_list'], [])

	def test_index_view_with_a_past_question(self):
		create_question(question_text="Past question.", days=-30)
		response = self.client.get(reverse('sample_app:home_page'))
		self.assertQuerysetEqual(
		response.context['question_list'],
		['<Question: Past question.>']
		)
	def test_index_view_with_a_future_question(self):

		create_question(question_text="Future question.", days=30)
		response = self.client.get(reverse('sample_app:home_page'))
		self.assertContains(response, "No polls are available.")
		self.assertQuerysetEqual(response.context['question_list'], [])

	def test_index_view_with_future_question_and_past_question(self):

		create_question(question_text="Past question.", days=-30)
		create_question(question_text="Future question.", days=30)
		response = self.client.get(reverse('sample_app:home_page'))
		self.assertQuerysetEqual(
		response.context['question_list'],
		['<Question: Past question.>']
		)
"""
	def test_index_view_with_two_past_questions(self):
		create_question(question_text="Past question 1.", days=-30)
		create_question(question_text="Past question 2.", days=-5)
		response = self.client.get(reverse('sample_app:home_page'))
		self.assertQuerysetEqual(
		response.context['question_list'],
		['<Question: Past question 2.>', '<Question: Past question 1.>'])
"""
class QuestionIndexDetailTests(TestCase):
	def test_detail_view_with_a_future_question(self):
		"""
		The detail view of a question with a pub_date in the future should
		return a 404 not found.
		"""
		future_question = create_question(question_text='Future question.', days=5)
		url = reverse('sample_app:details', args=(future_question.id,))
		response = self.client.get(url)
		self.assertEqual(response.status_code, 404)

	def test_detail_view_with_a_past_question(self):
		"""
		The detail view of a question with a pub_date in the past should
		display the question's text.
		"""
		past_question = create_question(question_text='Past Question.', days=-5)
		url = reverse('sample_app:details', args=(past_question.id,))
		response = self.client.get(url)
		self.assertContains(response, past_question.question_text)