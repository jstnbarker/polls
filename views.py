from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.template import loader
from .models import Question

# Create your views here.

def index(request):
    latest_question_list = Question.objects.order_by("-pub_date")[:5]
    template = loader.get_template("polls/index.html")
    context = {"latest_question_list": latest_question_list}
    return HttpResponse(template.render(context, request))

def detail(request, question_id):
    # django offers a function: `get_object_or_404()` because the following 
    # try except sequence is a common idiom
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist")
    template = loader.get_template("polls/detail.html")
    context = {"question": question}
    return HttpResponse(template.render(context, request))

def results(request, question_id):
    response = "You're looking at the results of question %s"

    return HttpResponse(response % question_id)

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "You didn't select a choice.",
            },
        )
    else:
        selected_choice.votes = F("votes") + 1 
        selected_choice.save()
    return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))

