# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone
#from django.template import loader

from sample_app.models import Question, Choices


class HomePageView(generic.ListView):

	#without using generic views --- input is a request
	"""question_list = Question.objects.all()
	context = {
		'question_list':question_list,
	}
	return render(request,'sample_app/home_page.html',context)"""
	#using generic views

	template_name = "sample_app/home_page.html"
	context_object_name = "question_list"

	def get_queryset(self):
		return Question.objects.filter(
				pub_date__lte = timezone.now()
			).all()

class DetailsView(generic.DetailView):

	"""
	try:
		question = Question.objects.get(pk = question_id)
	except Question.DoesNotExist:
		raise Http404("Question does not exist")

	return render(request,'sample_app/details.html',{'question':question})
	"""
	model = Question
	template_name = 'sample_app/details.html'

	def get_queryset(self):
		return Question.objects.filter(pub_date__lte = timezone.now())

class ResultsView(generic.DetailView):
	

	"""
	question = get_object_or_404(Question, pk = question_id)
	return render(request, 'sample_app/results.html', {'question':question})
	"""

	model = Question
	template_name = 'sample_app/results.html'

def votes(request, question_id):
	question = get_object_or_404(Question, pk = question_id)
	try:
		selected_choice = question.choices_set.get(pk = request.POST['choice'])
	except (KeyError, Choices.DoesNotExist):
		return render(request, 'sample_app/details.html', {
			'question': question,
			'error_message': "you didn't select a choice."
			})
	else:
		selected_choice.votes += 1
		selected_choice.save()
		return HttpResponseRedirect(reverse('sample_app:results', args = (question_id)))