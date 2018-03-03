import bottle
import os
import random

global count 
board_height = 0
board_width = 0
count = 0




def find_positions(data):

    food_position = []

    snake_position = (data['snakes']['data'][0]['body']['data'][0]['x'],data['snakes']['data'][0]['body']['data'][0]['y'])
    for i in range(len(data['food']['data'])):
        food_position.append((data['food']['data'][i]['x'], data['food']['data'][i]['y']))
    print food_position
    return (snake_position, food_position)

def shortest_path():
    return

'''
co-ords:
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
    data = bottle.request.json
    snake_pos, food_pos = find_positions(data)
    ourlength = data.get('snakes').get('data')[0].get('length')
    print data
    print 'x ', data.get('food').get('data')[0].get('x')
    print 'y ', data.get('food').get('data')[0].get('y')
    print data.get('snakes').get('data')[0].get('body').get('data')[0].get('x')
    print data.get('snakes').get('data')[0].get('body').get('data')[0].get('y')

   # print data['snakes']['data'][0]['body']['data'][0]['x']
   # print data['snakes']['data'][0]['body']['data'][0]['y']
    # TODO: Do things with data
    global count
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
    print 'bw ', board_width
    print  board_width
    print board_height

    #left wall
    if snake_position[0] == 1:
        return 1

    #right wall
    elif snake_position[0] == board_width:
        return 1+1

    #top wall
    elif snake_position[1] == 1:
        return 1+1+1

    #bottom wall
    elif snake_position[1] == board_width:
        return 1+1+1+1

    else: 
        return 0


    return    


# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()

if __name__ == '__main__':
    bottle.run(
        application,
        host=os.getenv('IP', '0.0.0.0'),
        port=os.getenv('PORT', '8080'),
        debug = True)
