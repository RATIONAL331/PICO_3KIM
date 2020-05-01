from django.views.generic import ListView, DetailView, TemplateView
from .models import Photo
from django.db import transaction
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render, Http404
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, DeleteView
from django.db.models import Q

from PICO_PROJECT.views import OwnerOnlyMixin, OtherOnlyMixin

from core.forms import DonateForm
from core.models import PhotoicoInfoLog, ProfilePicoInfoLog


# Create your views here.

class PhotoLV(ListView):
    model = Photo

class PhotoDV(DetailView):
    model = Photo

class PhotoCV(LoginRequiredMixin, CreateView):
    model = Photo
    fields = ('title', 'image', 'description', 'tags')
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

    def get_context_data(self, **kwargs):
        context = super(PhotoDonateDetailView, self).get_context_data(**kwargs)
        context['form'] = DonateForm()
        return context

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        form = DonateForm(request.POST)
        if form.is_valid():
            if(request.user.profile.PICOIN < form.cleaned_data['PICOIN']):
                return redirect(reverse('charge'))

            self.object = self.get_object()
            donating = PhotoicoInfoLog()
            donating.donator = request.user
            donating.PICOIN = form.cleaned_data['PICOIN']
            donating.photo = self.object
            donating.save()

            request.user.profile.PICOIN -= form.cleaned_data['PICOIN']
            request.user.save()

            # 후원받는 사람 PICOIN늘리기
            self.object.owner.profile.PICOIN += form.cleaned_data['PICOIN']
            self.object.owner.save()

            # 후원 받은 사람 LOGGING
            charging = ProfilePicoInfoLog()
            charging.profile = self.object.owner.profile
            charging.donator = request.user
            charging.PICOIN = form.cleaned_data['PICOIN']
            charging.where = self.object
            charging.save()

            # 후원 한 사람 LOGGING
            charging = ProfilePicoInfoLog()
            charging.profile = request.user.profile
            charging.donator = self.object.owner
            charging.PICOIN = -form.cleaned_data['PICOIN']
            charging.where = self.object
            charging.save()

            # 사진 PICOIN늘리기
            self.object.PICOIN += form.cleaned_data['PICOIN']
            self.object.save()

            return redirect('photo:photo_detail', self.object.id)
        else:
            self.object = self.get_object()
            context = super(PhotoDonateDetailView, self).get_context_data(**kwargs)
            context['form'] = form
            return self.render_to_response(context=context)

class PhotoPicoLog(TemplateView):
    template_name = 'photo_donate_list.html'

    def get(self, request, pk):
        photo = None
        try:
            photo = Photo.objects.get(pk=pk)
        except:
            raise Http404()
        
        logging = PhotoicoInfoLog.objects.filter(photo=photo)

        return render(request, 'photo/photo_donate_list.html', {'object_list': logging, 'photo':photo})


def post_search(request):
    template_name = "photo/photo_search.html"
    search_word = request.GET.get('search_word', '')
    if search_word:
        br = Photo.objects.filter(Q(title__icontains=search_word) | Q(description__icontains=search_word) | Q(owner__username__icontains=search_word)).distinct()
    return render(request, template_name, {'photo_search' : br, 'search_word':search_word})
