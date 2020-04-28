from django.views.generic import ListView, DetailView
from .models import Photo

from django.db import transaction
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView
from PICO_PROJECT.views import OwnerOnlyMixin, OtherOnlyMixin

from core.forms import DonateForm
from core.models import PhotoicoInfoLog
# Create your views here.

class PhotoLV(ListView):
    model = Photo

class PhotoDV(DetailView):
    model = Photo

class PhotoCV(LoginRequiredMixin, CreateView):
    model = Photo
    fields = ('title', 'image', 'description')
    success_url = reverse_lazy('photo:index')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

class PhotoChangeLV(LoginRequiredMixin, ListView):
    model = Photo
    template_name = 'photo/photo_change_list.html'

    def get_queryset(self):
        return Photo.objects.filter(owner=self.request.user)

class PhotoUV(OwnerOnlyMixin, UpdateView):
    model = Photo
    fields = ('title', 'image', 'description')
    success_url = reverse_lazy('photo:index')

class PhotoDelV(OwnerOnlyMixin, DeleteView):
    model = Photo
    success_url = reverse_lazy('photo:index')

class PhotoDonateDetailView(OtherOnlyMixin, DetailView):
    model = Photo
    template_name = 'photo/photo_donate.html'

    def get(self, request, *args, **kwargs):
        form = DonateForm()
        return render(request, 'charge.html', {'form':form, 'user':request.user})

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        form = DonateForm(request.POST)
        if form.is_valid():
            donating = PhotoicoInfoLog()
            # donating.profile = 
            donating.donator = request.user
            donating.PICOIN = form.cleaned_data['PICOIN']
            # donating.where = 
            donating.save()

            request.user.profile.PICOIN -= form.cleaned_data['PICOIN']
            request.user.save()

            # 후원받는 사람 PICOIN늘리기

            # 사진 PICOIN늘리기

            return redirect('profile', request.user.username)
    