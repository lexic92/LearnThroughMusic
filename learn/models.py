from django.db import models
from django import forms

# Create your models here.
class User(models.Model):
	username = models.CharField(max_length=20)
	password = models.CharField(max_length=20)
	def __unicode__(self):
		return self.username

class List(models.Model):
	user = models.ForeignKey(User)
	name = models.CharField(max_length=50)
	def __unicode__(self):
		return self.name

class Song(models.Model):
	theList = models.ForeignKey(List)
	title = models.CharField(max_length=50)
	artist = models.CharField(max_length=50)
	album = models.CharField(max_length=50)
	musicVideoLink = models.CharField(max_length=400)
	def __unicode__(self):
		return self.title

class Lyric(models.Model):
	song = models.ForeignKey(Song)
	text = models.TextField()
	def __unicode__(self):
		return self.text

class Vocaloid(models.Model):
	song = models.ForeignKey(Song)
	name = models.CharField(max_length=50)
	def __unicode__(self):
		return self.name

class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput(render_value=False),
                               max_length=100)

class UserForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput(render_value=False),
                               max_length=100)
    confirm = forms.CharField(widget=forms.PasswordInput(render_value=False),
                               max_length=100)
