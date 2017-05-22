# Create your views here.
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from displayer.models import Profile, SeasonRecord, TotalRecord, DailyRecord, Smelt, Stat,\
    Pitprofile, PitdailyRecord, PitseasonRecord, PittotalRecord, Pitsmelt, Pitstat

def start(request):
    profile_list = Profile.objects.all().order_by('-no')[:30]
    context = {'profile_list': profile_list}
    return render(request, 'start.html', context)

def search(request):
    profile_list = Profile.objects.all().order_by('-no')[:30]
    context = {'profile_list': profile_list}
    return render(request, 'search.html', context)

def index(request):
    profile_list = Profile.objects.all().order_by('-no')[:30]
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

def pindex(request):
    profile_list = Pitprofile.objects.all().order_by('-no')[:20]
    context = {'profile_list': profile_list}
    return render(request, 'displaycher/pindex.html', context)

def pdata(request, pitprofile_id):
    profile = get_object_or_404(Pitprofile, pk=pitprofile_id)
    season = get_object_or_404(PitseasonRecord, pk=pitprofile_id)
    total = get_object_or_404(PittotalRecord, pk=pitprofile_id)
    daily = get_object_or_404(PitdailyRecord, pk=pitprofile_id)
    smelt = get_object_or_404(Pitsmelt, pk=pitprofile_id)
    stat = get_object_or_404(Pitstat, pk=pitprofile_id)

    context = {'profile': profile, 'season':season, 'total':total, 'daily':daily, 'smelt':smelt, 'stat':stat}

    return render(request, 'displaycher/pdata.html', context)