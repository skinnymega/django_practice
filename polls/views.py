from django import template
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.template import loader
from django.views import generic
from .models import Question, Choice
from django.shortcuts import render, get_object_or_404
from django.utils import timezone


#def index(request):-> versão antiga, antes de criar o "front"
 #   latest_question_list = Question.objects.order_by('-pub_date')[6]
  #  output = ', '.join([q.question_text for q in latest_question_list])
   # return HttpResponse(output)

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        return Question.objects.filter(pub_date__lte = timezone.now()).order_by('-pub_date')[:5]

    """  code from when it were def index (request) latest_question_list = Question.objects.order_by('-pub_date')[:6]
    template = loader.get_template('polls/index.html')
    context = {
        'latest_question_list': latest_question_list,
    }
    return HttpResponse(template.render(context, request))"""

# Create your views here.

class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now())
    #question = get_object_or_404(Question, pk=question_id)
    #return render(request, 'polls/detail.html', {'question': question})


class ResultsView(generic.DetailView):
    model = Question 
    template_name = 'polls/results.html'

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {'question': question, 'error_message': "You didn't select a choice",})
    else: 
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))