from django.shortcuts import render
from models import MapModel
from collections import defaultdict
# Create your views here.


def map_view(request):
    """ """
    char_x = 3
    char_y = 3
    map_size = 2

    map_object = MapModel.objects.all()

    dbtemp = map_object.filter(
        x__gte=char_x - map_size,
        x__lte=char_x + map_size,
        y__gte=char_y - map_size,
        y__lte=char_y + map_size,
    )

    map_boundary = (map_size * 2) + 1
    result = {x: {y: {}
                  for y in range(1, map_boundary)
                  } for x in range(1, map_boundary)}
    for obj in dbtemp:
        result[obj.x][obj.y] = obj

    return render(request, 'visual.html', {'result': result})


def init_db_map(request):
    """ """
    for x in range(1, 5):
        for y in range(1, 5):
            MapModel(x=x, y=y).save()


def visual(request):
    """ """
