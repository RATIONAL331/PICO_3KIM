from django.views.generic import ListView, DetailView, TemplateView
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from .models import Photo
from django.db import transaction
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render, Http404
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, DeleteView
from django.db.models import Q, Sum
from PICO_PROJECT.views import OwnerOnlyMixin, OtherOnlyMixin

from core.forms import DonateForm
from core.models import PhotoicoInfoLog, ProfilePicoInfoLog

from itertools import chain

# Create your views here.

# 랭크를 도입할때에는 사진에 붙은 로그를 참조해야합니다.
# 사진에 붙은 로그에서 후원된 날짜를 기준으로 하루, 주, 월, 3개월, 년을 체크해야합니다.
# 확인한 후, 포함이 되면 그 금액을 모두 더합니다.
# 더한 금액을 기준으로 하여 정렬을 해야합니다. 만약에 값이 같으면 먼저 업로드된 기준으로 정렬합니다.
# Entry.objects.filter(pub_date__lte='2006-01-01') => 2006년 1월 1일보다 작은 것을 찾는다. gt(e) 는 큰 것을 찾는다.
# Blog.objects.annotate(Count('entry')) annotate를 사용하면 집계가능
# Foo.objects.filter(datefield__date=datetime.date.today())
# Sample.objects.filter(date__range=["2011-01-01", "2011-01-31"])
# from datetime import datetime, timedelta
# Entry.objects.filter(pub_date__gte = datetime.now() - timedelta(days=1)) 

class PhotoLV(ListView):
    model = Photo

    def get_queryset(self):
        return Photo.objects.all().order_by('-upload_dt')

class PhotoLVRankDay(ListView):
    model = Photo
    template_name = 'photo/photo_list_rank.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # 도네이션 된지 하루인 것 가져오기 
        infolog = PhotoicoInfoLog.objects.filter(donate_dt__gte=datetime.now()-relativedelta(days=1))

        # photo로 그룹을 묶어준다. 그 후, PICOIN을 SUM해준다.
        infolog = infolog.values('photo').annotate(total_PICO=Sum('PICOIN')).order_by('photo__id')
        
        photo_list = Photo.objects.filter(id__in=infolog.values_list('photo'))
        photo_list = list(zip(photo_list, infolog))
        
        photo_list = sorted(photo_list, key=lambda x:x[1]['total_PICO'], reverse=True)

        context['photo_list'] = photo_list

        return context

class PhotoLVRankWeek(ListView):
    model = Photo
    template_name = 'photo/photo_list_rank.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        infolog = PhotoicoInfoLog.objects.filter(donate_dt__gte=datetime.now()-relativedelta(weeks=1))
        infolog = infolog.values('photo').annotate(total_PICO=Sum('PICOIN')).order_by('photo__id')
        
        photo_list = Photo.objects.filter(id__in=infolog.values_list('photo'))
        photo_list = list(zip(photo_list, infolog))
        photo_list = sorted(photo_list, key=lambda x:x[1]['total_PICO'], reverse=True)

        context['photo_list'] = photo_list

        return context

class PhotoLVRankMonth(ListView):
    model = Photo
    template_name = 'photo/photo_list_rank.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        infolog = PhotoicoInfoLog.objects.filter(donate_dt__gte=datetime.now()-relativedelta(months=1))
        infolog = infolog.values('photo').annotate(total_PICO=Sum('PICOIN')).order_by('photo__id')
        
        photo_list = Photo.objects.filter(id__in=infolog.values_list('photo'))
        photo_list = list(zip(photo_list, infolog))
        
        photo_list = sorted(photo_list, key=lambda x:x[1]['total_PICO'], reverse=True)

        context['photo_list'] = photo_list

        return context

class PhotoLVRank3Month(ListView):
    model = Photo
    template_name = 'photo/photo_list_rank.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        infolog = PhotoicoInfoLog.objects.filter(donate_dt__gte=datetime.now()-relativedelta(months=3))
        infolog = infolog.values('photo').annotate(total_PICO=Sum('PICOIN')).order_by('photo__id')
        
        photo_list = Photo.objects.filter(id__in=infolog.values_list('photo'))
        photo_list = list(zip(photo_list, infolog))
        
        photo_list = sorted(photo_list, key=lambda x:x[1]['total_PICO'], reverse=True)

        context['photo_list'] = photo_list

        return context

class PhotoLVRankYear(ListView):
    model = Photo
    template_name = 'photo/photo_list_rank.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        infolog = PhotoicoInfoLog.objects.filter(donate_dt__gte=datetime.now()-relativedelta(years=1))
        infolog = infolog.values('photo').annotate(total_PICO=Sum('PICOIN')).order_by('photo__id')
        
        photo_list = Photo.objects.filter(id__in=infolog.values_list('photo'))
        photo_list = list(zip(photo_list, infolog))
        
        photo_list = sorted(photo_list, key=lambda x:x[1]['total_PICO'], reverse=True)

        context['photo_list'] = photo_list

        return context

class PhotoLVRankAll(ListView):
    model = Photo

    def get_queryset(self):
        return Photo.objects.all().order_by('-PICOIN')

class PhotoFollowView(LoginRequiredMixin, ListView):
    model = Photo
    template_name = 'photo_follow_list.html'
    def get_queryset(self):
        following = self.request.user.profile.following.all()
        following = chain(following, [self.request.user])
        return Photo.objects.filter(owner__in=following).order_by('-upload_dt')

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

class TaggedObjectLV(ListView):
    template_name = 'photo/taggit_photo_list.html'
    model = Photo

    def get_queryset(self):
        return Photo.objects.filter(Q(tags__name__icontains=self.kwargs.get('tag')))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tagname'] = self.kwargs['tag']
        return context
