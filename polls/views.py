from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.shortcuts import render,get_object_or_404
from django.http import Http404
from django.views import generic
from django.urls import reverse
from.models import Question,Choice



def index(request):
    latest_question_list = Question.objects.order_by("-pub_date")[:5]
    data = {"question_list": latest_question_list,}
    return HttpResponse(render(request, 'polls/index.html', data))




def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/results.html", {"question": question})


def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/detail.html", {"question": question})


def choice(request, question_id):
    question = get_object_or_404(Question, pk=question_id)

    if request.method == 'GET':
        return render(request, "polls/choice.html", {"question": question})
    elif request.method == 'POST':
        user_submitted_choice = request.POST["choice"]
        if not user_submitted_choice:
            return render(request, "polls/choice.html", {
                "question": question,
                "error_message": "Please enter a valid choice"
            })

        new_choice = Choice(
            question=question,
            choice_text=user_submitted_choice,
        )
        new_choice.save()
        return HttpResponseRedirect(reverse("polls:detail", args=(question.id,)))


def vote_reset(request, question_id):
    question = get_object_or_404(Question, pk=question_id)

    for choice in question.choice_set.all():
        choice.votes = 0
        choice.save()

    return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))


def add_question(request):
    if request.method == 'GET':
        return render(request, "polls/new_question.html", {})
    elif request.method == 'POST':
        user_submitted_question = request.POST["question"]
        if not user_submitted_question:
            return render(request, "polls/new_question.html", {
                "error_message": "Please enter a valid question"
            })
        
        new_question = Question(
            question_text=user_submitted_question,
            pub_date=timezone.now(),
        )
        new_question.save()
    return HttpResponseRedirect(reverse("polls:index",))



def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "You didn't select a choice.",
            },
        )
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))
    
   