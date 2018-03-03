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
name = 'bill-nye-the-battle-snake'

#this function finds our key in the snake dict
def find_us(data):
    for i in range(len(data['snakes']['data'])):
        #print data['snakes']['data'][i]['name']
        if data['snakes']['data'][i]['name'] == name:
            return i
    return -1

#this function finds our head position, also finds a list of the foods
def find_positions(data):

    food_position = []
    snakehead_position = (data['snakes']['data'][snakekey]['body']['data'][0]['x'],data['snakes']['data'][snakekey]['body']['data'][0]['y'])
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

def goto(snake, food, danger, snakehealth):
    max_pos = max(danger)
    index = 0
    for i in range(len(danger)):
        if danger[i] == max_pos:
            index = i

    directions = ['left',  'right', 'up', 'down']
    if snakehealth < (board_height + board_width + 5):
        if(snake[0]-food[0] > 0 and danger[0] > 1):
            return "left"
        elif(snake[0]-food[0] < 0 and danger[1] > 1):
            return "right"
        elif(snake[1]-food[1] > 0 and danger[2] > 1):
            return "up"
        elif(snake[1]-food[1] < 0 and danger[3] > 1):
            return "down"
        else:
            return directions[index]
    else:
        return directions[index]

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
    #print 'our sneks key: ', snakekey
    oursnake_head, food_pos = find_positions(data)
    #print 'Danger List: ', danger(data, oursnake_head)
    danger_list = danger(data, oursnake_head)
    moves = dangerdistance(oursnake_head, danger_list)    
    snakehealth = data['snakes']['data'][snakekey]['health']
    closest_food = shortest_path(oursnake_head, food_pos)
    ourlength = data.get('snakes').get('data')[snakekey].get('length')
    directions = ['left',  'right', 'up', 'down']
    direction = goto(oursnake_head,closest_food[0][0],moves, snakehealth)

    return {
        'move': direction,
        'taunt': 'Bill! Bill! Bill! Bill!'
    }

def dangerdistance(oursnake_head, danger_list):
    moves = [0] * 4
    headx = oursnake_head[0]
    heady = oursnake_head[1]
    leftdist = []
    rightdist = []
    updist = []
    downdist = []
    for i in range(len(danger_list)):
        
        if headx == danger_list[i][0]:
            #print 'headx ', headx
            #print 'danger_list[i][1] ', danger_list[i][1]
            if heady > danger_list[i][1]:
                updist.append(heady - danger_list[i][1])
            else:
                downdist.append(danger_list[i][1] - heady)
        if heady == danger_list[i][1]:
            #print 'heady ', heady
            #print 'danger_list[i][0] ', danger_list[i][0]
            if headx > danger_list[i][0]:
                leftdist.append(headx -danger_list[i][0])
            else:
                rightdist.append(danger_list[i][0] - headx)
    #print 'leftdist ',leftdist
    #print 'rightdist ', rightdist
    #print 'updist ', updist
    #print 'downdist ', downdist
    moves[0] = min(leftdist)
    moves[1] = min(rightdist)
    moves[2] = min(updist)
    moves[3] = min(downdist)
    #print moves
    return moves


#This function returns a list of every snake body item as co-ordinates
def danger(data, oursnake_head):
    danger_list = []
    for i in range(len(data['snakes']['data'])):
            for k in range(data['snakes']['data'][i]['length']):
                if (oursnake_head != (data['snakes']['data'][i]['body']['data'][(k)]['x'],data['snakes']['data'][i]['body']['data'][(k)]['y'])):
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
