from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from photo.models import Photo

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    followers = models.ManyToManyField(User, related_name='user_followers')
    PICOIN = models.PositiveIntegerField(default=0, verbose_name='PICOIN')

    def __str__(self):
        return self.user.email
        
@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class ProfilePicoInfoLog(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name='PROFILE')
    donator = models.ForeignKey(User, on_delete=models.DO_NOTHING, verbose_name='DONATOR', null=True)
    PICOIN = models.IntegerField(default=0, verbose_name='PICOIN')
    where = models.ForeignKey(Photo, on_delete=models.PROTECT, verbose_name='WHERE', null=True)
    donate_dt = models.DateTimeField('Donation Datetime', auto_now_add=True, null=True)

    class Meta:
        ordering = ('-donate_dt', )

    def __str__(self):
        return '%s %d' %(self.donator.username, self.PICOIN)

class PhotoicoInfoLog(models.Model):
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE, verbose_name='PHOTO')
    donator = models.ForeignKey(User, on_delete=models.DO_NOTHING, verbose_name='DONATOR', null=True)
    PICOIN = models.PositiveIntegerField(default=0, verbose_name='PICOIN')
    donate_dt = models.DateTimeField('Donation Datetime', auto_now_add=True, null=True)

    class Meta:
        ordering = ('-donate_dt', )
    
    def __str__(self):
        return '%s %d' %(self.donator.username, self.PICOIN)