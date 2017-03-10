import json

from django.shortcuts import render

from settings.models import VotingSystem
from votes.models import Vote, Status
from jay.utils import get_user_details


# Create your views here.
def home(request):
    ctx = {}
    votes = Vote.objects.filter(status__stage=Status.OPEN)
    results = Vote.objects.filter(status__stage=Status.PUBLIC)
    systems = VotingSystem.objects.all()

    if request.user.is_authenticated():
        details = get_user_details(request.user)

        votes_shown = [v for v in votes if v.filter.matches(details)]

        ctx["vote_list_title"] = "Your votes"

        if len(votes) != len(votes_shown):
            ctx["eligible_alert"] = True
    else:
        votes_shown = votes

    ctx["systems"] = systems
    ctx["votes"] = votes_shown
    ctx["results"] = results

    return render(request, "home.html", ctx)
