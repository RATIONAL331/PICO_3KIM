from django.shortcuts import render
from django.contrib.auth.models import User
from django.shortcuts import Http404
from django.views.generic import TemplateView

from .models import Profile
from photo.models import Photo

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
