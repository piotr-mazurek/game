from django.shortcuts import render, redirect
import datetime
from village.classes import CharacterVillage
from village.forms import VillageNameChangeForm
from village.models import (
    Village, 
    BuildingsInVillage, 
    ResourcesInVillage, 
    Buildings, 
    Costs,
    Gainings,
    Resources,
    )


def overview(request):
    """Rendering village overview."""
    c = CharacterVillage(request.session.get('selected_character_id'))
    village = Village.objects.get(
        character_id=request.session.get('selected_character_id')
    )
    request.session["village_id"]=village.id
    buildings = BuildingsInVillage.objects.filter(
        village_id=village.id
    )
    all_resources = Resources.objects.all()
    res_names = {};
    for r in all_resources:
        res_names[r.id] = r.resource_type
    for building in buildings:
        if building.level < building.building_id.max_level:
            building.building_id.cost = c.building_cost_per_level(
                building.building_id.id, building.level+1
            ).get_resources()
            for k, v in building.building_id.cost.items():
                building.building_id.cost[res_names[k]] = v
                del building.building_id.cost[k] 
    resources = c.get_current_resources().get_resources()
    grow = c.get_current_resource_grow().get_resources()
    result_res = {}
    for k, v in resources.items():
        res = {
            'grow': grow[k],
            'name': res_names[k],
            'amount': resources[k],
        }
        result_res[k] = res
    context = {
        'village': village,
        'buildings': buildings,
        'resources': result_res,
    }
    return render(request, 'village/overview.html', context)

def upgrade(request, building_id):
    """Building level upgrade."""

    building = BuildingsInVillage.objects.get(
        building_id=building_id,
        village_id=request.session.get('village_id')
    )
    c = CharacterVillage(request.session.get('selected_character_id'))
    c.upgrade_building(building_id)

    return redirect('overview')

def downgrade(request, building_id):
    """Building level downgrade."""
    building = BuildingsInVillage.objects.get(
        building_id=building_id,
        village_id=request.session.get('village_id')
    )
    c = CharacterVillage(request.session.get('selected_character_id'))
    c.downgrade_building(building_id)

    return redirect('overview')

def building_detail(request, id):
    """ Rendering detail view for building."""
    c = CharacterVillage(request.session.get('selected_character_id'))
    building = BuildingsInVillage.objects.get(id=id)
    all_resources = Resources.objects.all()
    res_names = {};
    for r in all_resources:
        res_names[r.id] = r.resource_type
    building_cost = c.building_cost(building.building_id)
    for k, v in building_cost.items():
        building_cost[res_names[k]] = v
        del building_cost[k]
    building_gains = c.resource_grow(building.building_id)
    for k, v in building_gains.items():
        building_gains[res_names[k]] = v
        del building_gains[k]
    context = {
        'building': building,
        'building_gains': building_gains,
        'building_cost': building_cost,
    }

    return render(request, 'village/building_detail.html', context)

def village_name_change(request, village_id):
    """Rendering village name change view."""
    village = Village.objects.get(id=village_id)
    if request.method == 'POST':
        form = VillageNameChangeForm(request.POST)
        if form.is_valid():
            village.name = form.cleaned_data['name']
            village.save()

            return redirect('overview')

    form = VillageNameChangeForm()
    context = {
        'form': form,
        'village': village
    }

    return render(request, 'village/village_name_change.html', context)
