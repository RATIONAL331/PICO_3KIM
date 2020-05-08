from django.views.generic import TemplateView

from django.views.generic import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy, reverse

from django.contrib.auth.mixins import AccessMixin

from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import RegisterForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage

from django.contrib.auth.decorators import login_required

from django.db.models import Q
from itertools import chain
from photo.models import Photo

class HomeView(TemplateView):
    template_name = 'home.html'

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your blog account.'
            message = render_to_string('registration/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
            email.send()
            return render(request, 'registration/register_validate.html')
    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {'form': form})
  
    
def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        # return redirect('home')
        return render(request, 'registration/registration_done.html')
    else:
        return Http404('Activation link is invalid!')

class OwnerOnlyMixin(AccessMixin):
    raise_exception = True
    permission_denied_message = "Owner only can update/delete the object"

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if request.user != obj.owner:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

class OtherOnlyMixin(AccessMixin):
    raise_exception = True
    permission_denied_message = "Others only can donate the object"

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if request.user == obj.owner:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)
    
    @classmethod
    def as_view(cls, **kwargs):
        view = super(OtherOnlyMixin, cls).as_view(**kwargs)
        return login_required(view)

def post_search(request):
    template_name = "search.html"
    search_word = request.GET.get('search_word', '')
    

    if search_word:
        search_words = search_word.split()
        for allWord in search_word:
            allWord.strip()
            for char in allWord:
                if char in "?.!/;:":
                    allWord.replace(char, '')
                elif char in ",":
                    allWord.replace(char, ' ')

        search_words.sort()
        # 찾는 검색어가 하나일 때 # 으로 시작하면 태그검색, @로 시작하면 유저 검색 그마저도 아니면 사진검색
        if len(search_words) == 1:
            if(search_words[0][0] == '#'):
                tag = search_words[0][1:]
                return redirect('photo:tagged_object_list', tag)
            elif(search_words[0][0] == '@'):
                # @를 입력하고 아무것도 입력안하면
                if(len(search_words[0]) == 1):
                    finduser = User.objects.none()
                    return render(request, template_name, {'search': finduser, 'search_word':search_words[0]})
                user = search_words[0][1:]
                finduser = User.objects.filter(Q(username__icontains=user))
                return render(request, template_name, {'search': finduser, 'search_word':search_words[0]})
            else:
                br = Photo.objects.filter(Q(title__icontains=search_word) | Q(description__icontains=search_word) | Q(owner__username__icontains=search_word)).distinct()
                return render(request, template_name, {'search' : br, 'search_word':search_words[0]})
        # 찾는 검색어가 여러개일 때 공통적으로 사진검색이며 #으로 시작하는 태그와 @로 시작하는 유저인 것을 모두 확인해야함
        else:
            br = Photo.objects.all()
            for word in search_words:
                if word[0] == '#':
                    if len(word) == 1:
                        continue
                    br = br.objects.filter(Q(tags__name__icontains=word[1:]))
                elif word[0] == '@':
                    if len(word) == 1:
                        continue
                    br = br.objects.filter(Q(owner__username__icontains=word[1:]))
                else:
                    br = br.objects.filter(Q(title__icontains=word) | Q(description__icontains=word) | Q(owner__username__icontains=word))

                return render(request, template_name, {'search' : br})