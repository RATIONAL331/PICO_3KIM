from django.shortcuts import render, redirect, reverse
from django.contrib.auth.models import User
from django.shortcuts import Http404
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Profile, ProfilePicoInfoLog
from photo.models import Photo
from .forms import ChargeForm

from django.db import transaction

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

    @transaction.atomic
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
            request.user.save()
            return redirect('profile', request.user.username)
            
class MyPicoLog(LoginRequiredMixin, TemplateView):
    template_name = 'mypicolog.html'

    def get(self, request, username):
        user = None
        try:
            user = User.objects.get(username=username)
        except:
            raise Http404()
        
        if(request.user.username != username):
            return self.handle_no_permission()

        profile = user.profile
        logging = ProfilePicoInfoLog.objects.filter(profile=profile,)

        return render(request, 'mypicolog.html', {'object_list': logging})

@login_required
def follow(request, username):
    if username == request.user.username:
        return redirect('profile', username)

    user = None
    try:
        user = User.objects.get(username=username)
    except:
        raise Http404()

    profile = user.profile
    
    if request.user in profile.followers.all():
        profile.followers.remove(request.user)
        request.user.profile.following.remove(user)
    else:
        profile.followers.add(request.user)
        request.user.profile.following.add(user)

    return redirect('profile', username)
    
class FollowersView(TemplateView):
    template_name = 'profile_followers.html'

    def get(self, request, username):
        user = None
        try:
            user = User.objects.get(username=username)
        except:
            raise Http404()

        followers = user.profile.followers.all()

        return render(request, 'profile_followers.html', {'user':user, 'followers_list': followers})

class FollowingView(TemplateView):
    template_name = 'profile_following.html'

    def get(self, request, username):
        user = None
        try:
            user = User.objects.get(username=username)
        except:
            raise Http404()

        following = user.profile.following.all()

        return render(request, 'profile_following.html', {'user':user, 'following_list': following})