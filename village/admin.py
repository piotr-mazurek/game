from django.contrib import admin
from village.models import (
	Buildings, 
	Resources, 
	Costs, 
	Gainings, 
	BuildingsInVillage, 
	ResourcesInVillage, 
	Village
	)

admin.site.register(Buildings)
admin.site.register(Resources)
admin.site.register(Costs)
admin.site.register(Gainings)
admin.site.register(BuildingsInVillage)
admin.site.register(ResourcesInVillage)
admin.site.register(Village)
