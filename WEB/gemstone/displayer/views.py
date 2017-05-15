from django.shortcuts import render

# Create your views here.
from django.shortcuts import get_object_or_404, render
from displayer.models import Profile, DailyRecord

def index(request):
    profile_list = Profile.objects.all().order_by('-no')[:5]
    context = {'profile_list': profile_list}
    return render(request, 'displayer/index.html', context)

def data(request, profile_id):
    profile = get_object_or_404(Profile, pk=profile_id)
    daily = DailyRecord.objects.all().order_by('-no')[:5]
    return render(request, 'displayer/data.html', {'profile': profile, 'daily':daily})
