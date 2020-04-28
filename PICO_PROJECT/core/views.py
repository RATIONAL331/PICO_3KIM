from django.shortcuts import render, redirect, reverse
from django.contrib.auth.models import User
from django.shortcuts import Http404
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Profile, ProfilePicoInfoLog
from photo.models import Photo
from .forms import ChargeForm

class ProfileView(TemplateView):
    template_name = 'profile.html'

    def get(self, request, username):
        user = None
        try:
            user = User.objects.get(username=username)
        except:
            raise Http404()
        
        profile = user.profile
        photos = Photo.objects.filter(owner=user)
        return render(request, 'profile.html', {'profile':profile, 'photos':photos})

class ChargeView(LoginRequiredMixin, TemplateView):
    template_name = 'charge.html'
    model = User
    
    def get(self, request, *args, **kwargs):
        form = ChargeForm()
        return render(request, 'charge.html', {'form':form, 'user':request.user})

    def post(self, request, *args, **kwargs):
        form = ChargeForm(request.POST)
        if form.is_valid():
            charging = ProfilePicoInfoLog()
            charging.profile = request.user.profile
            charging.donator = request.user
            charging.PICOIN = form.cleaned_data['PICOIN']
            charging.where = None
            charging.save()
            request.user.profile.PICOIN += form.cleaned_data['PICOIN']
            return redirect('profile', request.user.username)
