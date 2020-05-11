from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

from taggit.managers import TaggableManager
# Create your models here.

class Photo(models.Model):
    title = models.CharField('TITLE', max_length=30)
    description = models.TextField('Photo Description', blank=True)
    tags = TaggableManager(blank=True)
    PICOIN = models.PositiveIntegerField(default=0, verbose_name='PICOIN')
    # image = ThumbnailImageField(upload_to='photo/%Y/%m')
    image = models.ImageField('IMAGE', upload_to='SorlPhoto/%Y')
    upload_dt = models.DateTimeField('Upload Date', auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='OWNER', blank=True, null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('photo:photo_detail', args=(self.id,))