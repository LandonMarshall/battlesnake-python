import bottle
import os
import random

global count
global ourlength
global name
global snakekey
ourlength = 0
board_height = 0
board_width = 0
count = 0
snakekey = 0
name = 'snekyyy'

def find_us(data):
    for i in range(len(data['snakes']['data'])):
        print data['snakes']['data'][i]['name']
        if data['snakes']['data'][i]['name'] == name:
            return i
    return -1

def find_positions(data):

    food_position = []
    snake_position = (data['snakes']['data'][snakekey]['body']['data'][(ourlength-1)]['x'],data['snakes']['data'][snakekey]['body']['data'][(ourlength-1)]['y'])
    for i in range(len(data['food']['data'])):
        food_position.append((data['food']['data'][i]['x'], data['food']['data'][i]['y']))
    return (snake_position, food_position)

def shortest_path(snake, food):
    distance = []
    for i in range(len(food)):
        #Creates touple of (food coordinates, total blocks away)
        distance.append((food[i],abs(food[i][0]-snake[0])+abs(food[i][1]-snake[1])))
    return sorted(distance, key=lambda distance: distance[1])

'''
co-ords:
    print data['snakes']['data'][0]['body']['data'][0]['x']
    print data['snakes']['data'][0]['body']['data'][0]['y']
    food list x and y: data.get('food').get('data')[i].get('x'), i = food items
    snake coords x and y: data.get('snakes').get('data')[i].get('body').get('data')[j].get('x') i = snakes, j = length of each snake'''

@bottle.route('/')
def static():
    return "the server is running ahah"


@bottle.route('/static/<path:path>')
def static(path):
    return bottle.static_file(path, root='static/')


@bottle.post('/start')
def start():
    global board_width
    global board_height
    data = bottle.request.json
    game_id = data.get('game_id')
    board_width = data.get('width')
    board_height = data.get('height')
    head_url = 'https://i.imgur.com/pRNYWzI.png'

    # TODO: Do things with data

    return {
        'color': '#00FF00',
        'taunt': '{} ({}x{})'.format(game_id, board_width, board_height),
        'head_url': head_url
    }


@bottle.post('/move')
def move():
    global ourlength
    global count
    global snakekey

    data = bottle.request.json
    snakekey = find_us(data)
    print snakekey
    snake_pos, food_pos = find_positions(data)
    #print shortest_path(snake_pos, food_pos)
    print data
    ourlength = data.get('snakes').get('data')[0].get('length')

   # print data['snakes']['data'][0]['body']['data'][0]['x']
   # print data['snakes']['data'][0]['body']['data'][0]['y']
    # TODO: Do things with data

    directions = ['up',  'left', 'down', 'right']
    direction = directions[count]
    if count == 3:
        count = 0
    else:
        count = count + 1

    return {
        'move': direction,
        'taunt': 'Bill! Bill! Bill! Bill!'
    }


'''
Wall direction: 
    left = 1
    right = 2 
    top = 3
    bottom = 4
    none = 0 
'''
def wallHit(snake_position):
    array = [0,0,0,0]
    #left wall
    if snake_position[0] == 1:
        array[0] = 1

    #right wall
    if snake_position[0] == board_width:
        array[1] = 1

    #top wall
    if snake_position[1] == 1:
        array[2] = 1

    #bottom wall
    if snake_position[1] == board_width:
        array[3] = 1

    return array

def danger(snake_position):

    return
    


# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()

if __name__ == '__main__':
    bottle.run(
        application,
        host=os.getenv('IP', '0.0.0.0'),
        port=os.getenv('PORT', '8080'),
        debug = True)
