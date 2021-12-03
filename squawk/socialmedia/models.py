from django.core import validators
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import RegexValidator


alphanumeric = RegexValidator(r'^[a-zA-Z ]*$', 'Only alphabetic characters are allowed.')
# This model is for posts
class Post(models.Model):
    body = models.TextField()
    image = models.ImageField(upload_to='uploads/post_photos', blank=True, null=True)
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, blank=True, related_name='likes')

#This model is for comments
class Comment(models.Model):
    comment = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey('Post', related_name='comments', null=True, on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, blank=True, related_name='comment_likes')

# This model is for user profiles
class UserProfile(models.Model):
    user = models.OneToOneField(User, primary_key=True, verbose_name='user', related_name='profile', on_delete=models.CASCADE)
    name = models.CharField(max_length=30, blank=True, null=True)
    major = models.CharField(max_length = 20, blank=True, null=True, validators=[alphanumeric])
    location = models.CharField(max_length=100, blank=True, null=True)
    bio = models.TextField(max_length=150, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    hobbies = models.CharField(max_length=100, blank=True, null=True)
    picture = models.ImageField(upload_to='uploads/profile_pictures', default='uploads/profile_pictures/pfp_default.png', blank=True)
    followers = models.ManyToManyField(User, blank=True, related_name='followers')

# This model is for blocked users
class Blocked(models.Model):
    user = models.ForeignKey(User, null=True, related_name="blocked_users", on_delete=models.CASCADE)
    users = models.ManyToManyField(User, blank=True, related_name="blocked_by")

# This model is for settings
class Setting(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	name = models.CharField(max_length=200)
	value = models.CharField(max_length=200)

	def __str__(self):
		return self.name

# This function allows the system to automatically create a user profile for user on registration using signals
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
        instance.profile.save()
