from django.http import HttpResponse
from django.utils import timezone

import datetime
import json
import random
import logging

from minesweep.models import Field, Grid

# Create views

def field(request, field_id):
    try:
        status = 200
        field = Field.objects.get(pk=field_id)

        timestamp = int((timezone.make_naive(field.created_date, timezone.utc) - datetime.datetime.fromtimestamp(0)).total_seconds() * 1000)

        data = {
            'id': field.id,
            'height': field.height,
            'width': field.width,
            'count': field.count,
            'active': field.active,
            'created_date':timestamp,
            'flags': []
        }

        grids = Grid.objects.filter(field_id__exact=field).order_by('x', 'y')
        x = None
        for g in grids:
            if g.x != x:
                x = g.x
                row = []
                data['flags'].append(row)

            row.append({'flagged': g.flagged, 'value': str(g.value) if g.swept else '?'})

    except Field.DoesNotExist:
        status = 404
        data = {'error': 'Field not found'}

    return HttpResponse(json.dumps(data), status=status, content_type='application/json')


def flag(request, field_id, x, y):
    error = None
    try:
        field_id = int(field_id)
    except ValueError:
        error = 'Provided field id is invalid.'

    try:
        x = int(x)
    except ValueError:
        error = 'Unable to parse x-coordinate.'

    try:
        y = int(y)
    except ValueError:
        error = 'Unable to parse y-coordinate.'

    if error == None:
        try:
            field = Field.objects.get(pk=field_id)

            if field.active:

                grids = Grid.objects.filter(field_id__exact=field, x__exact=x, y__exact=y)

                if len(grids) == 0:
                    status = 404
                    error = 'Grid not found'
                elif len(grids) > 1:
                    status = 500
                    error = 'Data Error'

                if error != None:
                    data = {'error': error}
                else:

                    status = 200
                    g = grids[0]

                    #flagging grid
                    if not g.flagged:

                        g.flagged = True

                        data = {'result': 'flagged'}

                    #unflagging grid
                    else:

                        g.flagged = False

                        data = {'result': 'unflagged'}


                    g.save()

            #inactive field
            else:
                status = 401
                data = {'error':'Game is no longer active'}

        #unable to find given field
        except Field.DoesNotExist:
            status = 404
            data = {'error': 'Field not found'}

    #unable to parse input
    else:
        status = 401
        data = {'error': error}

    return HttpResponse(json.dumps(data), status=status, content_type='application/json')


def sweepNeighbours(grids, x, y):
    coords = []
    recurse = []

    for i in range(len(grids)):
        g = grids[i]

        #if the grid not swept and is within the surrounding box
        if (not g.swept) and g.x >= x - 1 and g.x <= x + 1 and g.y >= y - 1 and g.y <= y + 1:
            #but not the center
            if not (g.x == x and g.y == y):
                coords.append({'x': g.x, 'y': g.y, 'value': g.value})

                g.swept = True
                g.save()

                if g.value == 0:
                    recurse.append({'x': g.x, 'y': g.y})

    for r in recurse:
        coords.extend(sweepNeighbours(grids, r['x'], r['y']))

    return coords


def sweep(request, field_id, x, y):
    error = None
    try:
        field_id = int(field_id)
    except ValueError:
        error = 'Provided field id is invalid.'

    try:
        x = int(x)
    except ValueError:
        error = 'Unable to parse x-coordinate.'

    try:
        y = int(y)
    except ValueError:
        error = 'Unable to parse y-coordinate.'

    if error == None:
        try:
            field = Field.objects.get(pk=field_id)

            if field.active:
                grids = Grid.objects.filter(field_id__exact=field_id, x__exact=x, y__exact=y)

                if len(grids) == 0:
                    status = 404
                    error = 'Grid not found'
                if len(grids) > 1:
                    status = 500
                    error = 'Data Error'

                if error != None:
                    data = {'error': error}
                else:
                    g = grids[0]

                    status = 200

                    g.swept = True
                    g.save()

                    #if its a bomb
                    if g.value == -1:
                        data = {'result': 'loss'}

                        # mark field as inactive
                        field.active = False
                        field.save()
                    else:

                        #get all non-bombs that are not swept
                        grids = Grid.objects.filter(field_id__exact=field_id, value__gte=0, swept__exact=False)

                        data = {'result': 'unclear', 'coords': [{'x': x, 'y': y, 'value': g.value}]}
                        if g.value == 0:
                            data['coords'].extend(sweepNeighbours(grids, x, y))

                        grids = Grid.objects.filter(field_id__exact=field_id, value__gte=0, swept__exact=False)
                        if not grids.exists():
                            try:
                                # mark field as inactive
                                field.active = False
                                field.save()

                                data['result'] = 'win'
                            except Field.DoesNotExist:
                                status = 404
                                data = {'error': 'Field not found'}
            #inactive field
            else:
                status = 401
                data = {'error':'Game is no longer active'}

        #unable to find field
        except Field.DoesNotExist:
            status = 404
            data = {'error': 'Field not found'}

    #unable to parse input
    else:
        status = 401
        data = {'error': error}

    return HttpResponse(json.dumps(data), status=status, content_type='application/json')

def new(request, height, width, chance):
    MAX_HEIGHT = 100
    HEIGHT_ERROR = 'The requested height of ' + str(height) + ' is not valid. It must be a positive integer from 1 to ' + str(MAX_HEIGHT)
    MAX_WIDTH = 100
    WIDTH_ERROR = 'The requested width of ' + str(width) + ' is not valid. It must be a positive integer from 1 to ' + str(MAX_WIDTH)
    MAX_CHANCE = 100
    CHANCE_ERROR = 'The percent chance of ' + str(chance) + ' is not valid. It must be a percent from 0 to ' + str(MAX_CHANCE)

    logging.getLogger('meansweep.views.new').info('New game: ' + str(height) + ', ' + str(width) + ', ' + str(chance))

    error = None
    try:
        height = int(height)
    except ValueError:
        error = HEIGHT_ERROR

    try:
        width = int(width)
    except ValueError:
        error = WIDTH_ERROR

    try:
        chance = int(chance)
    except ValueError:
        error = CHANCE_ERROR

    if height <= 0 or height > MAX_HEIGHT:
        error = HEIGHT_ERROR
    if width <= 0 or width > MAX_WIDTH:
        error = WIDTH_ERROR
    if chance < 0 or chance > MAX_CHANCE:
        error = CHANCE_ERROR

    if error != None:
        status = 401
        data = {'error': error}
    else:
        status = 201

        #create the base field
        f = Field(height=height, width=width, count=0, created_date=timezone.now())
        f.save()

        #create the grids
        grids = []
        for x in range(width):
            row = []
            grids.append(row)
            for y in range(height):
                row.append(Grid(field_id=f.id, x=x, y=y, value=0))

        #create the bombs
        for x in range(width):
            for y in range(height):
                if random.random() * 100 <= chance:
                    grids[x][y].value = -1 #bomb!
                    f.count += 1

                    #update neighbours
                    for i in [x-1, x, x+1]:
                        for j in [y-1, y, y+1]:
                            if i >= 0 and i < width and j >= 0 and j < height and grids[i][j].value > -1:
                                grids[i][j].value += 1

        for x in range(width):
            for y in range(height):
                grids[x][y].save()

        f.save()

        timestamp = int((timezone.make_naive(f.created_date, timezone.utc) - datetime.datetime.fromtimestamp(0)).total_seconds() * 1000)

        data = {
            'id':f.id,
            'height':f.height,
            'width':f.width,
            'count':f.count,
            'active':f.active,
            'created_date':timestamp
        }

    return HttpResponse(json.dumps(data), status=status, content_type='application/json')
