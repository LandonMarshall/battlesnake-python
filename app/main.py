import bottle
import os
import random

global count
count = 0

def find_positions:
    for n in
    snake_position = (data['snake']['data'][0]['body']['data']['x'],data['snake']['data'][0]['body']['data']['x'])
    food_position = (data)
    return (snake_position, food_position)

def shortest_path():



'''co-ords:
    food list x and y: data.get('food').get('data')[i].get('x'), i = food items
    snake coords x and y: data.get('snakes').get('data')[i].get('body').get('data')[j].get('x') i = snakes, j = length of each snake
'''

@bottle.route('/')
def static():
    return "the server is running ahah"


@bottle.route('/static/<path:path>')
def static(path):
    return bottle.static_file(path, root='static/')


@bottle.post('/start')
def start():
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
    print data
    print data.get('food').get('data')[0].get('x')
    print data.get('food').get('data')[0].get('y')
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


# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()

if __name__ == '__main__':
    bottle.run(
        application,
        host=os.getenv('IP', '0.0.0.0'),
        port=os.getenv('PORT', '8080'),
        debug = True)
