from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import Profile, ProfilePicoInfoLog, PhotoicoInfoLog

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'

class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline, )
    list_display = ('username', 'email', 'get_PICOIN')
    list_select_related = ('profile', )

    def get_PICOIN(self, instance):
        return instance.profile.PICOIN
    get_PICOIN.short_description = 'PICOIN'

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)


@admin.register(ProfilePicoInfoLog)
class ProfilePicoInfoLogAdmin(admin.ModelAdmin):
    list_display = ('id',)


@admin.register(PhotoicoInfoLog)
class PhotoicoInfoLogAdmin(admin.ModelAdmin):
    list_display = ('id',)
