# Error
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.shortcuts import render

from django.urls import reverse

from django.http import HttpResponseRedirect
# return type 1~3
from django.http import HttpResponse
# from django.template import loader

from django.utils import timezone

from django.views import generic

from .models import Question, Choice

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        # Return the last five published questions (not including those set to be published in the future).
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]

        # View Test Before
        # return Question.objects.order_by('-pub_date')[:5]

def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    
    # return type 1~3
    # template = loader.get_template('polls/index.html')

    context = {
        'latest_question_list' : latest_question_list
    }
    # return type 4
    return render(request, 'polls/index.html', context)

    # return type 3
    # return HttpResponse(template.render(context, request))
    
    # return type 2
    # output = ','.join([q.question_text for q in latest_question_list])
    # return HttpResponse(output)
    
    # return type 1
    # return HttpResponse("Hello, world. You're at the polls index.")

class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"

    def get_queryset(self):
        # Excludes any questions that aren't published yet.
        return Question.objects.filter(pub_date__lte=timezone.now())

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})
    # return type 1~3
    # return HttpResponse("You're looking at question %s." % question_id)
    
    # type 3
    # try:
    #     question = Question.objects.get(pk = question_id)
    # except Question.DoesNotExist:
    #     raise Http404("Question does not exit")
    # return render(request, 'polls/detail.html', {'question': question})


class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"


def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})


    # type 1
    # response = "You're looking at the results of question %s."
    # return HttpResponse(response % question_id)

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, "polls/detail.html",{
                            'question' : question,
                            'error_message':'You didn`t select a choice.'
                        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(
                                    reverse('polls:results', 
                                            args=(question_id,)
                                            )
                                    )
    # Type 1
    # return HttpResponse("You're voting on question %s." % question_id)