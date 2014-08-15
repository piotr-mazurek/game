from django.db import models


class Buildings(models.Model):

    name = models.CharField(max_length=100, unique=True)
    max_level = models.IntegerField()

    def __str__(self):
        return self.name


class Resources(models.Model):

    resource_type = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.resource_type


class Costs(models.Model):

    starting_cost = models.IntegerField()
    multiplier = models.DecimalField(max_digits=5, decimal_places=2)
    building_id = models.ForeignKey(Buildings)
    resource_id = models.ForeignKey(Resources)

    def __str__(self):
        return "%s, %s, %s, %s" % (
            self.building_id,
            self.resource_id,
            self.starting_cost,
            self.multiplier
            )


class Gainings(models.Model):

    first_gain = models.IntegerField()
    multiplier = models.DecimalField(max_digits=5, decimal_places=2)
    building_id = models.ForeignKey(Buildings)
    resource_id = models.ForeignKey(Resources)

    def __str__(self):
        return "%s, %s, %s, %s" % (
            self.building_id,
            self.resource_id,
            self.first_gain,
            self.multiplier
            )


class Village(models.Model):

    name = models.CharField(max_length=100, unique=True)
    character_id = models.IntegerField(default=0)
    last_change = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class BuildingsInVillage(models.Model):

    village_id = models.ForeignKey(Village)
    building_id = models.ForeignKey(Buildings)
    level = models.IntegerField(default=0)

    def __str__(self):
        return "%s, %s" % (
            self.village_id,
            self.building_id
            )


class ResourcesInVillage(models.Model):

    village_id = models.ForeignKey(Village)
    resource_id = models.ForeignKey(Resources)
    amount = models.DecimalField(decimal_places=4, max_digits=20)
    capacity = models.IntegerField()

    def __str__(self):
        return "%s, %s" % (
            self.village_id,
            self.resource_id
        )
