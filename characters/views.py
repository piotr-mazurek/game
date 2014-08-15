from django.shortcuts import render, redirect
from django.http import HttpResponse
from characters.models import Character
from characters.forms import CharacterCreationForm, CharacterRemovalForm
from village.models import (
	Buildings,
	Resources,
	BuildingsInVillage,
	ResourcesInVillage,
	Village
	)


def index(request):

	user_id = request.session.get('user_id')
	character_list = Character.objects.filter(user_id=user_id)
	if request.session.get('selected_character_id') is not None:
		selected_character = Character.objects.get(
			pk=request.session.get('selected_character_id')
		)
		context = {
			'character_list': character_list,
			'selected_character': selected_character,
		}
		return render(request, 'characters/index.html', context)
	else:
		context = {'character_list': character_list}
	return render(request, 'characters/index.html', context)

def detail(request, character_id):

	if request.method == 'POST':
		request.session["selected_character_id"] = character_id 
		return redirect('index')
	else:
		character = Character.objects.get(pk=character_id)
		context = {'character': character}
		return render(request, 'characters/detail.html', context)

def create(request):
	if request.method == 'POST':
		form = CharacterCreationForm(request.POST)
		if form.is_valid():
			buildings = Buildings.objects.all()
			resources = Resources.objects.all()
			character = Character(
				user_id=request.session.get('user_id'),
				character_class_id=form.cleaned_data['character_class'],
				name=form.cleaned_data['name'],
				image=form.cleaned_data['image'],
			)
			character.save()
			village = Village(
				name="Default village "+str(character.id),
				character_id=character.id,
			)
			village.save()
			for building in buildings:
				buildings_in_village = BuildingsInVillage(
					village_id=village,
					building_id=building,
					level=0,
				)
				buildings_in_village.save()
			for resource in resources:
				resources_in_village = ResourcesInVillage(
					village_id=village,
					resource_id=resource,
					amount=40000,
					capacity=50000,
				)
				resources_in_village.save()

			return redirect('index')
	elif request.method == 'GET':
		form = CharacterCreationForm()
		return render(request,'characters/create.html', {'form': form})

def delete(request, character_id):
	
	character = Character.objects.get(pk=character_id)
	if request.method == 'POST':
		form = CharacterRemovalForm(request.POST)
		if form.is_valid() and form.cleaned_data['removal_check'] == "Delete":
				character.delete()
				if character_id == request.session.get('selected_character_id'):
					request.session["selected_character_id"] = None
				return redirect('index')
	form = CharacterRemovalForm()
	context = {
		'character_id': character_id,
		'form': form,
		'character': character
	}
	return render(request,'characters/delete.html', context)

