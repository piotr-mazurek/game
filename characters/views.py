from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from characters.models import Character
from characters.forms import CharacterCreationForm


def index(request):
	character_list = Character.objects.order_by('created_at')
	context = {'character_list': character_list}
	# import pdb; pdb.set_trace()
	return render(request, 'characters/index.html', context)

def detail(request, character_id):
	return HttpResponse("You're looking at character %s." % character_id)

def create(request):

	if request.method == 'POST':
		form = CharacterCreationForm(request.POST)
		if form.is_valid():
			# import pdb; pdb.set_trace()
			character = Character(
				character_class_id=form.cleaned_data['character_class'],
				name=form.cleaned_data['name'],
				image=form.cleaned_data['image'],
			)
			character.save()
			return redirect('index')
	else:
		form = CharacterCreationForm()
		return render(request,'characters/create.html', {'form': form})
