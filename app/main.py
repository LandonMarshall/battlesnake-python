import bottle
import os
import random

global count
global ourlength
global name
global snakekey
global direction
direction = 'up'
ourlength = 0
board_height = 0
board_width = 0
count = 0
snakekey = 0
name = 'snekyyy'

#this function finds our key in the snake dict
def find_us(data):
    for i in range(len(data['snakes']['data'])):
        print data['snakes']['data'][i]['name']
        if data['snakes']['data'][i]['name'] == name:
            return i
    return -1

#this function finds our head position, also finds a list of the foods
def find_positions(data):

    food_position = []
    snakehead_position = (data['snakes']['data'][snakekey]['body']['data'][0]['x'],data['snakes']['data'][snakekey]['body']['data'][0]['y'])
    print "our head: ", snakehead_position
    for i in range(len(data['food']['data'])):
        food_position.append((data['food']['data'][i]['x'], data['food']['data'][i]['y']))
    return (snakehead_position, food_position)

#this function finds the shortest path to food
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
    return "the server is running"


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
        'color': '#FF0000',
        "secondary_color": "#00FF00",
        'taunt': '{} ({}x{})'.format(game_id, board_width, board_height),
        'head_url': head_url
    }


@bottle.post('/move')
def move():
    data = bottle.request.json
    global ourlength
    global direction
    global count
    global snakekey
    snakekey = find_us(data)
    print 'our sneks key: ', snakekey
    oursnake_head, food_pos = find_positions(data)
    print 'Danger List: ', danger(data)
    danger_list = danger(data)
    moves = safemoves(oursnake_head,danger_list)
    print moves
    #print shortest_path(snake_pos, food_pos)
    ourlength = data.get('snakes').get('data')[snakekey].get('length')
   # print data['snakes']['data'][0]['body']['data'][0]['x']
   # print data['snakes']['data'][0]['body']['data'][0]['y']
    directions = ['left',  'right', 'up', 'down']
    safe_moves = []
    for i in range(len(moves)):
        if moves[i] == 0:
            safe_moves.append(i)
    print safe_moves
    print random.choice(safe_moves)
    direction = directions[random.choice(safe_moves)]


    
    return {
        'move': direction,
        'taunt': 'Bill! Bill! Bill! Bill!'
    }

def safemoves(oursnake_head, danger_list):
    #left,right,up,down
    moves = [0] * 4
    left = (oursnake_head[0]-1,oursnake_head[1])
    right = (oursnake_head[0]+1,oursnake_head[1])
    up = (oursnake_head[0],oursnake_head[1]-1)
    down = (oursnake_head[0],oursnake_head[1]+1)
    if left in danger_list:
        moves[0] = 1
    if right in danger_list:
        moves[1] = 1
    if up in danger_list:
        moves[2] = 1
    if down in danger_list:
        moves[3] = 1
    return moves



#This function returns a list of every snake body item as co-ordinates
def danger(data):
    danger_list = []   
    for i in range(len(data['snakes']['data'])):
            for k in range(data['snakes']['data'][i]['length']):
                danger_list.append((data['snakes']['data'][i]['body']['data'][(k)]['x'],data['snakes']['data'][i]['body']['data'][(k)]['y']))
    for i in range(board_height):
        danger_list.append((-1,i))
        danger_list.append((board_width,i))
    for i in range(board_width):
        danger_list.append((i,-1))
        danger_list.append((i,board_height))
        #left wall = -1,y
        # top wall = x,-1
        #right wall = board_width, y
        #bottom wall = x, board_height
    return danger_list
    


# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()

if __name__ == '__main__':
    bottle.run(
        application,
        host=os.getenv('IP', '0.0.0.0'),
        port=os.getenv('PORT', '8080'),
        debug = True)
