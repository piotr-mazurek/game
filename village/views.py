from django.shortcuts import render, redirect
from village.models import (
    Village,
    BuildingsInVillage,
    ResourcesInVillage,
    Buildings,
    Costs,
    Gainings,
    )


def cost_per_level(level, building_id):

    costs = Costs.objects.filter(building_id=building_id)
    structure = Buildings.objects.get(id=building_id)
    building_costs = {}
    total_cost = {}
    for cost in costs:
        building_costs[str(cost.resource_id.resource_type)] = {}
        current_cost = cost.starting_cost
        for i in range(1, structure.max_level+1):
            building_costs[
                str(cost.resource_id.resource_type)
                ][i] = int(current_cost)
            current_cost *= cost.multiplier
    for resource in building_costs:
        total_cost[resource] = building_costs[resource][level]
    return total_cost


def gain_per_level(level, building_id):

    gains = Gainings.objects.filter(building_id=building_id)
    structure = Buildings.objects.get(id=building_id)
    building_gain = {}
    total_gain = {}
    for gain in gains:
        building_gain[str(gain.resource_id.resource_type)] = {}
        current_gain = gain.first_gain
        for i in range(1, structure.max_level+1):
            building_gain[
                str(gain.resource_id.resource_type)
                ][i] = int(current_gain)
            current_gain *= gain.multiplier
    for resource in building_gain:
        total_gain[resource] = building_gain[resource][level]
    return total_gain


def overview(request):

    village = Village.objects.get(pk=1)
    request.session["village_id"] = village.id
    all_buildings = Buildings.objects.all()
    buildings = BuildingsInVillage.objects.filter(
        village_id=request.session.get('village_id')
        )
    resources = ResourcesInVillage.objects.filter(
        village_id=request.session.get('village_id')
        )
    name = village.name
    cost_next_level = {}
    for building in buildings:
        cost_next_level[building.building_id] = cost_per_level(
            building.level+1,
            building.building_id.id
            )
    context = {
        'name': name,
        'buildings': buildings,
        'resources': resources,
        'all_buildings': all_buildings,
        'cost_next_level': cost_next_level
    }
    return render(request, 'village/overview.html', context)


def upgrade(request, building_id):

    building = BuildingsInVillage.objects.get(
        building_id=building_id, village_id=request.session.get('village_id')
        )
    building.level += 1
    total_cost = cost_per_level(building.level, building_id)
    resources = ResourcesInVillage.objects.filter(
        village_id=request.session.get('village_id')
        )
    for resource in resources:
        try:
            resource.amount -= total_cost[
                str(resource.resource_id.resource_type)
                ]
            if resource.amount < 0:
                return redirect('overview')
            resource.save()
        except:
            pass
    building.save()
    return redirect('overview')


def downgrade(request, building_id):

    building = BuildingsInVillage.objects.get(
        building_id=building_id, village_id=request.session.get('village_id')
        )
    total_cost = cost_per_level(building.level, building_id)
    resources = ResourcesInVillage.objects.filter(
        village_id=request.session.get('village_id')
        )
    building.level -= 1
    for resource in resources:
        try:
            resource.amount += total_cost[
                str(resource.resource_id.resource_type)
                ]
            if resource.amount > resource.capacity:
                resource.amount = resource.capacity
            resource.save()
        except:
            pass
    building.save()
    return redirect('overview')
