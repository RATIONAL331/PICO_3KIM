from django.contrib import admin
from .models import Photo
# Register your models here.

class PhotoInline(admin.StackedInline):
    model = Photo
    extra = 2


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'upload_dt')
