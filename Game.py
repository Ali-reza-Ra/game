# import libray to use
from curses import initscr, noecho, cbreak, error
from random import random, randint
from time import sleep

# game settings and variables
StdScreen = initscr()
noecho()
cbreak()
StdScreen.keypad(True)
StdScreen.nodelay(True)
maxlines, maxcols = StdScreen.getmaxyx()
maxlines -= 1
maxcols -= 1
world = []
food = []
enemy = []
score = 0
player_l = player_c = randint(0, maxlines - 1)


# init the game
def init():
    global player_l, player_c
    for i in range(0, maxlines + 1):
        world.append([])
        for j in range(0, maxcols + 1):
            world[i].append(' ' if random() > 0.03 else '.')
    for i in range(10):
        foodline, foodcols = random_place()
        foodage = randint(500, 1000)
        food.append((foodline, foodcols, foodage))
    for i in range(5):
        enemyline, enemycols = random_place()
        enemy.append((enemyline, enemycols))
    player_l, player_c = random_place()


# draw the objects
def draw():
    for i in range(maxlines):
        for j in range(maxcols):
            StdScreen.addch(i, j, world[i][j])
    StdScreen.addstr(1, 1, f'score: {score}')
    for f in food:
        foodline, foodcols, foodage = f
        StdScreen.addch(foodline, foodcols, '$')
    for i in enemy:
        enemyline, enemycols = i
        StdScreen.addch(enemyline, enemycols, 'E')
    StdScreen.addch(player_l, player_c, 'P')
    StdScreen.refresh()


# make a random place for objects
def random_place():
    a = randint(0, maxlines - 1)
    b = randint(0, maxcols - 1)
    while world[a][b] != ' ':
        a = randint(0, maxlines - 1)
        b = randint(0, maxcols - 1)
    return a, b


# make sure the objects in the screen range
def in_range(num, minimum, maximum):
    if num < minimum:
        return minimum
    if num > maximum:
        return maximum
    return num


# control the foods
def check_food():
    global score
    for i in range(len(food)):
        foodline, foodcols, foodage = food[i]
        if player_l == foodline and player_c == foodcols:
            score += 10
            foodline, foodcols = random_place()
            foodage = randint(100, 200)
        if foodage <= 0:
            foodline, foodcols = random_place()
            foodage = randint(100, 200)
        food[i] = (foodline, foodcols, foodage)


# control the player moves
def move(control):
    global player_l, player_c
    if control == 'w' and world[player_l - 1][player_c] != '.':
        player_l -= 1
    elif control == 's' and world[player_l + 1][player_c] != '.':
        player_l += 1
    elif control == 'd' and world[player_l][player_c + 1] != '.':
        player_c += 1
    elif control == 'a' and world[player_l][player_c - 1] != '.':
        player_c -= 1

    player_l = in_range(player_l, 0, maxlines - 1)
    player_c = in_range(player_c, 0, maxcols - 1)


# control the enemies
def enemy_check():
    global playing
    for i in range(len(enemy)):
        el, ec = enemy[i]
        if random() > 0.9:
            if el > player_l:
                el -= 1
            if ec > player_c:
                ec -= 1
            if el < player_l:
                el += 1
            if ec < player_c:
                ec += 1
            el = in_range(el, 0, maxlines - 1)
            ec = in_range(ec, 0, maxcols - 1)
            enemy[i] = (el, ec)
        if el == player_l and ec == player_c:
            StdScreen.addstr(maxlines // 2, maxcols // 2 - 3, 'you dead!')
            StdScreen.refresh()
            sleep(3)
            playing = False


# main game loop
init()
playing = True
while playing:
    try:
        c = StdScreen.getkey()
    except error:
        c = ''
    if c in 'wasd':
        move(c)
    elif c == 'q':
        playing = False
        StdScreen.addstr(maxlines // 2, maxcols // 2 - 8, 'thanks for playing')
        StdScreen.refresh()
        sleep(2)
    draw()
    check_food()
    enemy_check()
    sleep(0.03)
