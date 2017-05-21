# Create your views here.
from django.shortcuts import get_object_or_404, render
from displayer.models import Profile, SeasonRecord, TotalRecord, DailyRecord, Smelt, Stat
from django.http import JsonResponse

def index(request):
    profile_list = Profile.objects.all().order_by('-no')[:20]
    context = {'profile_list': profile_list}
    return render(request, 'displayer/index.html', context)


def data(request, profile_id):
    profile = get_object_or_404(Profile, pk=profile_id)
    season = get_object_or_404(SeasonRecord, pk=profile_id)
    total = get_object_or_404(TotalRecord, pk=profile_id)
    daily = get_object_or_404(DailyRecord, pk=profile_id)
    smelt = get_object_or_404(Smelt, pk=profile_id)
    stat = get_object_or_404(Stat, pk=profile_id)

    context = {'profile': profile, 'season':season, 'total':total, 'daily':daily, 'smelt':smelt, 'stat':stat}

    return render(request, 'displayer/data.html', context)