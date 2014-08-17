from datetime import datetime
from village.models import Village


class ResourcesContainer(object):
    """ Container for character resources."""

    def __init__(self):
        self.resources = {}

    def add_resource_object(self, resource):
        self.resources[resource.resource_id.id] = resource.amount

    def add_resource(self, resource_id, amount):
        self.resources[resource_id] = amount

    def get_resources(self):
        return self.resources

    def get_resource_by_id(self, resource_id):
        return self.resources.get(resource_id)

    def get_fancy_reslt(self):
        """Gets result dictionary in following form:
        {
            {
                'id': int
                'name': string,
                'amount' float,
            },
            ...
        }

        """
        pass

    def __repr__(self):
        return str(self.resources)


class CharacterVillage(object):

    def __init__(self, character_id):
        self.village = Village.objects.get(character_id=character_id)
        self.grow_resources()

    def grow_resources(self):
        """Updates resources."""
        time_delta = datetime.now() - self.village.last_change.replace(
            tzinfo=None
        )
        if time_delta.seconds == 0:
            return
        grow = self.get_current_resource_grow()
        for resource in self.village.resourcesinvillage_set.all():
            resource.amount += float(time_delta.seconds) * float(
                grow.get_resource_by_id(resource.resource_id.id)/3600
            )
            resource.save()
        self.village.last_change = datetime.now()
        self.village.save()

    def get_current_resources(self):
        """Returns current resources.

            return: ResourcesContainer instance:
        """
        resource_container = ResourcesContainer()
        for resource in self.village.resourcesinvillage_set.all():
            resource_container.add_resource_object(resource)

        return resource_container

    def get_current_resource_grow(self):
        """Returns resource grow per second.

            return: ResourcesContainer instance:
        """
        result = ResourcesContainer()
        for building in self.village.buildingsinvillage_set.all():
            for gain in building.building_id.gainings_set.all():
                result.add_resource(
                    gain.resource_id.id,
                    self.compute_gain_per_level(
                        building.level,
                        gain.first_gain,
                        gain.multiplier,
                    )
                )
        return result

    def resource_grow(self, building_id):
        """Calculates building gain at all levels."""
        gains = {}
        building = self.village.buildingsinvillage_set.get(
            building_id=building_id
        )
        for grow in building.building_id.gainings_set.all():
            current_grow = grow.first_gain
            gains[grow.resource_id.id] = {}
            for lv in range(1, building.building_id.max_level+1):
                gains[grow.resource_id.id][lv] = current_grow
                current_grow *= grow.multiplier
        return gains

    def compute_gain_per_level(self, level, base, multiplier):
        """Calculates building gain per level."""
        gain_sum = base
        for lv in range(1, level):
            gain_sum *= multiplier
        return gain_sum

    def building_cost(self, building_id):
        """Calculates and retruns cost for given building."""
        result = {}
        building = self.village.buildingsinvillage_set.get(
            building_id=building_id
        )
        for cost in building.building_id.costs_set.all():
            current_cost = cost.starting_cost
            result[cost.resource_id.id] = {}
            for lv in range(1, building.building_id.max_level+1):
                result[cost.resource_id.id][lv] = current_cost
                current_cost *= cost.multiplier
        return result

    def building_cost_per_level(self, building_id, level):
        """ Finds cost of building for given level."""
        result = self.building_cost(building_id)
        final_result = ResourcesContainer()
        for res in result:
            try:
                final_result.add_resource(res, result[res][level])
            except:
                pass
        return final_result

    def upgrade_building(self, building_id):
        """Recalculates resources and upgrade building in db."""
        building = self.village.buildingsinvillage_set.get(
            building_id=building_id
        )
        if building.level == building.building_id.max_level:
            return
        upgrade_cost = self.building_cost_per_level(
            building_id, building.level+1
        ).get_resources()
        resources = self.village.resourcesinvillage_set.all()
        is_ok = True
        for resource in resources:
            if resource.amount - float(
                upgrade_cost[resource.resource_id.id]
            ) < 0:
                is_ok = False
        if is_ok:
            for resource in resources:
                resource.amount -= float(upgrade_cost[resource.resource_id.id])
                resource.save()
            building.level += 1
            building.save()

    def downgrade_building(self, building_id):
        """Recalculates resources and downgrade building in db."""
        building = self.village.buildingsinvillage_set.get(
            building_id=building_id
        )
        if building.level == 0:
            return
        downgrade_return = self.building_cost_per_level(
            building_id, building.level
        ).get_resources()
        resources = self.village.resourcesinvillage_set.all()
        for resource in resources:
            resource.amount += float(downgrade_return[resource.resource_id.id])
            resource.save()
        building.level -= 1
        building.save()
