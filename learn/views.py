# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from learn.models import *
from django.template import Context, loader
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.template import RequestContext

import django.contrib.auth
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

import json

def index(request):
    users = User.objects.all()
    songs = Song.objects.all()
    template = loader.get_template('learn/index.html')
    context = Context({
        'users': users,
	'songs': songs,
    })
    return HttpResponse(template.render(RequestContext(request)))

@login_required
def home(request):
	userId = request.user.id
	u = User.objects.get(pk=userId)

	Learned = None
	PlanToLearn = None
	Learning = None
	Dropped = None

	#Create lists for this user if you haven't done so before.
	lists = List.objects.filter(user_id=userId)
	if not lists:
		Learned = List(name="Learned", user_id=userId)
		PlanToLearn = List(name="Plan to Learn", user_id=userId)
		Learning = List(name="Learning", user_id=userId)
		Dropped = List(name="Dropped", user_id=userId)
		Learned.save()
		PlanToLearn.save()
		Learning.save()
		Dropped.save()

	#Otherwise, get the lists that already exist.
	else:
		for l in lists:
			if l.name == "Learned":     
				Learned = l
			elif l.name == "Plan to Learn":
				PlanToLearn = l
			elif l.name == "Learning":
				Learning = l
			elif l.name == "Dropped":
				Dropped = l

	listOfLists = [Learning, PlanToLearn, Learned, Dropped]

	context = Context({
	'u': u,
	'listOfLists': listOfLists,
	'LearnedID' : Learned.id,
	'PlanToLearnID' : PlanToLearn.id,
	'LearningID' : Learning.id,
	'DroppedID' : Dropped.id
	})
	return render(request, 'learn/home.html', context)

@login_required
def viewSongDetails(request, userId, songId):
    song = get_object_or_404(Song, pk=songId)
    u = get_object_or_404(User, pk=userId)
    return render(request, 'learn/view.html', {'song': song, 'u': u})

@login_required
def add(request):
	userId = request.user.id
	u = User.objects.get(pk=userId)
	
	if request.method == 'GET':
		Learned = None
		PlanToLearn = None
		Learning = None
		Dropped = None


		lists = List.objects.filter(user_id=userId)

		for l in lists:
			if l.name == "Learned":     
				Learned = l
			elif l.name == "Plan to Learn":
				PlanToLearn = l
			elif l.name == "Learning":
				Learning = l
			elif l.name == "Dropped":
				Dropped = l

		listOfLists = [Learning, PlanToLearn, Learned, Dropped]

		context = Context({
		'u': u,
		'LearnedID' : Learned.id,
		'PlanToLearnID' : PlanToLearn.id,
		'LearningID' : Learning.id,
		'DroppedID' : Dropped.id
		})
		return render(request, 'learn/add.html', context)

	if request.method =='POST':
		#Save the song
		s = Song(title=request.POST['title'], 
			album=request.POST['album'],
			artist=request.POST['artist'],
			musicVideoLink=request.POST['musicVideoLink'],
			theList_id=request.POST['dropDownList'])
		s.save()

		#Add lyrics if applicable
		lyrics = request.POST['lyrics']
		if lyrics != "":
			l = Lyric(song_id=s.id, text=lyrics)
			l.save()

		#Add vocaloid if applicable
		featuring = request.POST['featuring']
		if featuring != "":
			v = Vocaloid(song_id=s.id, name=featuring)
			v.save()			

		return HttpResponseRedirect(reverse('learn.views.home'))

@login_required
def editSongDetails(request, userId, songId):
	s = Song.objects.get(pk=songId)
	u = User.objects.get(pk=userId)

	if request.method == 'GET':
		return render_to_response('learn/edit.html', { 's':s, 'u':u},
                                  context_instance=RequestContext(request))
	
	if request.method =='POST':
		#update title, album, artist, and music video link
		s.title = request.POST['title']
		s.album = request.POST['album']
		s.artist = request.POST['artist']
		s.musicVideoLink = request.POST['musicVideoLink']
		s.save()

		#update vocaloids
		counter = 1
		for v in s.vocaloid_set.all():
			checkboxName = 'id_delete_featuring' + str(counter)			
			if checkboxName in request.POST:
				v.delete()
				counter += 1
			else:
				v.name = request.POST['featuring' + str(counter)]
				v.save()
				counter += 1
		
		#update lyrics
		counter = 1
		for l in s.lyric_set.all():
			checkboxName = 'id_delete_lyrics' + str(counter)			
			if checkboxName in request.POST:
				l.delete()
				counter += 1
			else:
				l.text = request.POST['lyrics' + str(counter)]
				l.save()
				counter += 1
		
		#add new lyrics to database, if applicable
		newlyrics = request.POST['lyrics']
		if newlyrics != "":
			ly = Lyric(song_id=songId, text=newlyrics)
			ly.save()
		
		#add new vocaloid to database, if applicable
		newvocaloid = request.POST['featuring']
		if newvocaloid != "":
			nv = Vocaloid(song_id=songId, name=newvocaloid)
			nv.save()	

        	return HttpResponseRedirect(reverse('learn.views.home'))

@login_required
def move(request, userId, songId, fromlist, tolist):
	u = User.objects.get(pk=userId)

	#retrieve song
	s = Song.objects.get(pk=songId)
	#retrieve fromlist
	l1 = List.objects.get(pk=fromlist)
	#retrive tolist
	l2 = List.objects.get(pk=tolist)
	#delete from fromlist
	s.delete()
	#add to tolist
	l2.song_set.add(s)
    

	#with those changes made, regenerate the HTML for all the lists:
	Learned = None
	PlanToLearn = None
	Learning = None
	Dropped = None


	lists = List.objects.filter(user_id=userId)

	for l in lists:
		if l.name == "Learning":
			Learning = l
		elif l.name == "Plan to Learn":
			PlanToLearn = l
		elif l.name == "Learned":     
			Learned = l
		elif l.name == "Dropped":
			Dropped = l

	listOfLists = [Learning, PlanToLearn, Learned, Dropped]

	context = Context({
	'u': u,
	'listOfLists': listOfLists,
	'LearnedID' : Learned.id,
	'PlanToLearnID' : PlanToLearn.id,
	'LearningID' : Learning.id,
	'DroppedID' : Dropped.id
	})
	return render(request, 'learn/Lists.html', context)

def login(request):
    if request.method == 'GET':
        form = LoginForm()
        next = request.GET['next']
        return render_to_response('auth/login.html', {'form':form,
                                                      'next':next},
                                  context_instance=RequestContext(request))

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if not form.is_valid():
            return render_to_response('auth/login.html', {'form':form},
                                  context_instance=RequestContext(request))

        user = authenticate(username=request.POST['username'],
                            password=request.POST['password'])
        if user is None:
            return render_to_response('auth/login.html',
                                      {'form':form,
                                       'error': 'Invalid username or password'},
                                      context_instance=RequestContext(request))
        django.contrib.auth.login(request,user)
        return HttpResponseRedirect(request.POST['next'])

def logout(request):
    django.contrib.auth.logout(request)
    return HttpResponseRedirect(reverse('learn.views.index'))

def create(request):
    if request.method == 'GET':
        form = UserForm()
        return render_to_response('auth/create.html', {'form':form},
                                  context_instance=RequestContext(request))

    if request.method == 'POST':
        form = UserForm(request.POST)
        if not form.is_valid():
            return render_to_response('auth/create.html', {'form':form},
                                  context_instance=RequestContext(request))

        try:
            u = User.objects.get(username=request.POST['username'])
            return render_to_response('auth/create.html',
                                      {'form':form,
                                       'error':'Username already taken'},
                                  context_instance=RequestContext(request))
        except User.DoesNotExist:
            pass

        if request.POST['password'] != request.POST['confirm']:
            return render_to_response('auth/create.html',
                                      {'form':form,
                                       'error':'Passwords must match'},
                                  context_instance=RequestContext(request))

        user = User.objects.create_user(username=request.POST['username'],
                                        password=request.POST['password'])
        user.save()
        return HttpResponseRedirect(reverse('learn.views.home'))

@login_required
def delete(request, userId, songId):
	u = User.objects.get(pk=userId)

	#retrieve song
	s = Song.objects.get(pk=songId)
	#delete song
	s.delete()

	#with those changes made, regenerate the HTML for all the lists:
	Learned = None
	PlanToLearn = None
	Learning = None
	Dropped = None

	lists = List.objects.filter(user_id=userId)

	for l in lists:
		if l.name == "Learning":
			Learning = l
		elif l.name == "Plan to Learn":
			PlanToLearn = l
		elif l.name == "Learned":     
			Learned = l
		elif l.name == "Dropped":
			Dropped = l

	listOfLists = [Learning, PlanToLearn, Learned, Dropped]

	context = Context({
	'u': u,
	'listOfLists': listOfLists,
	'LearnedID' : Learned.id,
	'PlanToLearnID' : PlanToLearn.id,
	'LearningID' : Learning.id,
	'DroppedID' : Dropped.id
	})
	return render(request, 'learn/Lists.html', context)

@login_required
def api_home(request):
	userId = request.user.id
	u = User.objects.get(pk=userId)

	Learned = ["1"]
	PlanToLearn = None
	Learning = None
	Dropped = None

	#Create lists for this user if you haven't done so before.
	lists = List.objects.filter(user_id=userId)
	if not lists:
		Learned = List(name="Learned", user_id=userId)
		PlanToLearn = List(name="Plan to Learn", user_id=userId)
		Learning = List(name="Learning", user_id=userId)
		Dropped = List(name="Dropped", user_id=userId)
		Learned.save()
		PlanToLearn.save()
		Learning.save()
		Dropped.save()

	#Get the lists that already exist.
	for l in lists:
		if l.name == "Learned":     
			Learned = l
		elif l.name == "Plan to Learn":
			PlanToLearn = l
		elif l.name == "Learning":
			Learning = l
		elif l.name == "Dropped":
			Dropped = l

	_Learned = []
	for s in Learned.song_set.all():
		_Learned.append(convertSongToDict(s))

	_PlanToLearn = []
	for s in PlanToLearn.song_set.all():
		_PlanToLearn.append(convertSongToDict(s))

	_Learning = []
	for s in Learning.song_set.all():
		_Learning.append(convertSongToDict(s))

	_Dropped = []
	for s in Dropped.song_set.all():
		_Dropped.append(convertSongToDict(s)) 


	jsonDict = { 	"Learned" : _Learned,  
			"Plan to Learn" : _PlanToLearn,
			"Learning" : _Learning,
			"Dropped" : _Dropped  }
	jsonString = json.dumps(jsonDict, indent=4, separators=(',', ': '))
	print(jsonString)
	return HttpResponse(jsonString)


def convertSongToDict(song):
	songDict = { "title" : song.title,
			"artist" : song.artist,
			"album" : song.album,
			"musicVideoLink" : song.musicVideoLink }
	lyricList = []
	for l in song.lyric_set.all():
		lyricList.append(l.text)

	vocaloidList = []
	for v in song.vocaloid_set.all():
		vocaloidList.append(v.name)

	songDict.update({"lyric_set": lyricList, "vocaloid_set" : vocaloidList})
	return songDict


def api_login(request, _username, _password):
	if request.method == 'GET':
		user = authenticate(username=_username,
                            password=_password)
        	if user is None:
            		return HttpResponse('Invalid username or password')

		django.contrib.auth.login(request, user)
        	return HttpResponse('Successfully logged in')

def api_logout(request):
	django.contrib.auth.logout(request)
	return HttpResponse('logged out')
