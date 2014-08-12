from django.shortcuts import render, redirect
from characters.models import Character
from characters.forms import CharacterCreationForm, CharacterRemovalForm


def index(request):

    character_list = Character.objects.order_by('created_at')
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
        context = {
            'character_list': character_list,
        }
    return render(request, 'characters/index.html', context)


def detail(request, character_id):

    if request.method == 'POST':
        request.session["selected_character_id"] = character_id
        return redirect('index')
    else:
        character = Character.objects.get(pk=character_id)
        context = {
            'character': character,
        }
        return render(request, 'characters/detail.html', context)


def create(request):

    if request.method == 'POST':
        form = CharacterCreationForm(request.POST)
        if form.is_valid():
            character = Character(
                character_class_id=form.cleaned_data['character_class'],
                name=form.cleaned_data['name'],
                image=form.cleaned_data['image'],
            )
            character.save()
            return redirect('index')
    else:
        form = CharacterCreationForm()
        return render(request, 'characters/create.html', {'form': form})


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
        'character': character,
    }
    return render(request, 'characters/delete.html', context)
