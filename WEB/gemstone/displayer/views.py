# Create your views here.
from django.shortcuts import get_object_or_404, render
from displayer.models import Profile, SeasonRecord
from django.http import JsonResponse

def index(request):
    profile_list = Profile.objects.all().order_by('-no')[:5]
    context = {'profile_list': profile_list}
    return render(request, 'displayer/index.html', context)

# def data(request, profile_id):
#     profile = get_object_or_404(Profile, pk=profile_id)
#     season = SeasonRecord.objects.all().order_by('-no')[:5]
#
#     response = JsonResponse({'profile': profile, 'season': season})
#     return render(request, 'displayer/data.html', response)


def data(request, profile_id):
    profile = get_object_or_404(Profile, pk=profile_id)
    seasons = get_object_or_404(SeasonRecord, pk=profile_id)
    context = {'profile': profile, 'season':seasons}

    return render(request, 'displayer/data.html', context)

# def data(request, profile_id):
#     profile = get_object_or_404(Profile, pk=profile_id)
#     seasons = SeasonRecord.objects.all().order_by('-no')[:5]
#     context = {'profile': profile, 'season':seasons}
#
#     return render(request, 'displayer/data.html', context)