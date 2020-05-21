# Import neccessary functions
import pygame, sys
from pygame.locals import *
from random import randint
from copy import deepcopy

# Needed vars
line_length = 150
lvl = 0
players = []
players_copy = []

# Color constants
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (128, 128, 128)
RED = (255, 0, 0)
GARNET = (112, 0, 0)
ORANGE = (255, 106, 0)
DARKORANGE = (252, 119, 3)
GREEN = (0, 255, 0)
DARKGREEN = (0, 163, 3)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
PURPLE = (212, 0, 255)

# Custom classes
class Player:
    def __init__(self, name):
        self.box_size = 50
        self.points = 0
        self.name = name
        self.index = len(players)
        self.level = 1
        self.hits = 0
        self.misses = 0
        self.ptsFromLevel = 5
        self.time = lvl.time[0]

    def hit(self):
        self.points += 1
        self.hit_last = True
        self.timeout_last = False
        self.hits += 1
        self.update()

    def miss(self):
        self.points -= lvl.minus
        self.hit_last = False
        self.timeout_last = False
        self.misses += 1
        self.update()

    def timeout(self):
        self.miss()
        self.timeout_last = True

    def out(self):
        del players[self.index]

    def update(self):
        if self.points < 5:
            self.box_size = 50
            self.level = 1
        elif self.points < 10:
            self.box_size = 35
            self.level = 2
        else:
            self.box_size = 25
            self.level = 3
        self.ptsFromLevel = (self.level+1)*5-5-self.points
        self.time = lvl.time[self.level-1]
        players_copy[self.index] = deepcopy(self)

    def update_next(self):
        self.index = players.index(self)
        self.next = players[self.index+1 if self.index+1 < len(players) else 0]
        print(f'{self.name}:{self.next.name}')

class Level:
    def __init__(self, lvl):
        self.lvl = lvl
        if lvl == 0:
            self.name = 'Easy'
            self.time = [4, 6, 9]
            self.lines = 75
            self.lose_at = -10
            self.minus = 2
            self.instruction = 'Shouldn\'t be that bad. Good luck!'
        elif lvl == 1:
            self.name = 'Medium'
            self.time = [4, 6, 9]
            self.lines = 50
            self.lose_at = -10
            self.minus = 2
            self.instruction = 'It\'ll get difficult towards level 3. Hang in there!'
        elif lvl == 2:
            self.name = 'Hard'
            self.time = [2, 4, 6]
            self.lines = 45
            self.lose_at = -4
            self.minus = 2
            self.instruction = 'You\'re in for a treat. Good luck!'
        else:
            self.name = 'Insane'
            self.time = [2, 3, 5]
            self.lines = 40
            self.lose_at = -4
            self.minus = 2
            self.instruction = 'There\'s no way you\'re beating this. Have fun!'

class Text:
    def __init__(self, text, x, y, color=WHITE, font=None, size=24, center=True):
        self._font = pygame.font.SysFont(font, size)
        self._size = size
        self.actualFont = font
        self.actualText = text
        self._color = color
        self.x, self.y = x, y
        self.recenter = True
        self.center = center
        self.render()

    def draw(self):
        if hasattr(self, 'input'):
            if self.recenter:
                self.textRect.center = (self.x, self.y)
            else:
                self.textRect.w = self.input.w-10
                self.textRect.center = self.input.center
        else:
            if self.center:
                self.textRect.center = (self.x, self.y)
            else:
                self.textRect.topleft = (self.x, self.y)
        screen.blit(self._text, self.textRect)

    def render(self):
        self._text = self._font.render(self.actualText, True, self._color)
        self.textRect = self._text.get_rect()

    @property
    def text(self):
        return self.actualText

    @text.setter
    def text(self, val):
        self.actualText = val
        self.render()

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, val):
        self._color = val
        self.render()

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, val):
        self._size = val
        self._font = pygame.font.SysFont(self.actualFont, self._size)

    @property
    def font(self):
        return self.actualFont

    @font.setter
    def font(self, val):
        self.actualFont = val
        self._font = pygame.font.SysFont(self.actualFont, self._size)

class Button:
    def __init__(self, x, y, width, height, command, color=BLACK, btn_width=0, text=None, text_color=WHITE, font=None, text_size=24, disabled=False):
        self.button = pygame.Rect(0, 0, width, height)
        self.button.center = (x, y)
        self._color = color
        self.fadeColor = [i+40 if i < 215 else 255 for i in self._color]
        self.fade = False
        self.disabled = disabled
        self.command = command
        self.btn_width = btn_width
        if text:
            self.text = Text(text, x, y, text_color, font, text_size)

    def update(self):
        if not self.disabled:
            if self.button.collidepoint(pygame.mouse.get_pos()):
                self.fade = True
            else:
                self.fade = False

    def handle(self, event):
        if not self.disabled:
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                if self.button.collidepoint(event.pos):
                    self.command()

    def enable(self):
        self.disabled = False

    def disable(self):
        self.disabled = True

    def draw(self):
        self.update()
        if not self.disabled:
            color = self.fadeColor if self.fade else self._color
        else:
            color = self.fadeColor
        pygame.draw.rect(screen, color, self.button, 1 if self.disabled else self.btn_width)
        if hasattr(self, 'text'):
            self.text.draw()

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, val):
        self._color = val
        self.fadeColor = [i+40 if i < 215 else 255 for i in self._color]

class Input:
    def __init__(self, x, y, width, height, filler='', text_color=WHITE, font=None, text_size=24, recenter=True, blacklist=[]):
        self.input = pygame.Rect(0, 0, width, height)
        self.input.center = (x, y)
        self.textSurface = Text('', x, y, text_color, font, text_size)
        self.textSurface.recenter = recenter
        self.textSurface.input = self.input
        self.text_color = text_color
        self.blacklist = blacklist
        self.active = False
        self.filler = filler
        self.text = ''
        self.width = width
        self.recenter = recenter
        self.x, self.y = x, y

    def handle(self, event):
        if event.type == MOUSEBUTTONDOWN and event.button == 1:
            if self.input.collidepoint(event.pos):
                self.active = True
            else:
                self.active = False
        elif event.type == KEYDOWN and self.active:
            if event.key == K_BACKSPACE and len(self.text) > 0:
                self.text = self.text[:-1]
            elif (event.unicode.isalnum() or event.unicode == ' ') and event.unicode not in self.blacklist:
                self.text += event.unicode
            self.textSurface.text = self.text

    def update(self):
        if self.text == '':
            self.textSurface.color = [i-70 if i > 70 else 0 for i in self.text_color]
            self.textSurface.text = self.filler
            self.textSurface.recenter = True
        else:
            self.textSurface.color = self.text_color
            self.textSurface.recenter = self.recenter
        width = max(self.width, self.textSurface._text.get_width()+10)
        self.input.w = width
        if self.recenter:
            self.input.center = (self.x, self.y)

    def draw(self):
        self.update()
        pygame.draw.rect(screen, WHITE if self.active else BLACK, self.input, 2)
        self.textSurface.draw()

# Game control functions
def stop_game():
    pygame.quit()
    sys.exit()

def screen_reset(color):
    screen.fill(color)

def screen_resize(w, h):
    global width, height, screen
    # Set global vars first, then the actual screen
    width, height = w, h
    screen = pygame.display.set_mode((width, height))

def screen_init(w, h, color=None, title=None):
    global screen
    # Resize the screen
    screen_resize(w, h)
    # Start pygame
    pygame.init()
    # Set optional values: the title of the window, and the screen color
    if title: pygame.display.set_caption(title)
    if color: screen_reset(color)

def screen_update():
    pygame.display.flip()

def new_frame(box, color=BLACK):
    '''Parameters:
    box - the box (pygame Rect object) to use for each frame
    color - the color to draw the box with'''
    screen_reset(BLACK)
    # Draw the number of lines specified in the Level object (assigned to lvl) in random locations
    for i in range(lvl.lines):
        x = randint(-line_length, width)
        y = randint(0, height)
        pygame.draw.line(screen, RED if lvl.lvl == 3 else WHITE, (x, y), (x+line_length, y))
    pygame.draw.rect(screen, color, box)
    screen_update()

def create_box():
    '''Create and return a pygame Rect object in a random location'''
    box_size = current.box_size
    x = randint(0, width-box_size)
    y = randint(0, height-box_size)
    return pygame.Rect(x, y, box_size, box_size)

# Screens
def start_screen():
    def move_on(val):
        global lvl
        nonlocal done
        done = True
        lvl = val

    done = False
    lvlButtons = []
    # Add the difficulty buttons
    for i, item in enumerate(['Easy', 'Medium', 'Hard', 'Insane']):
        lvlButtons.append(Button(int(width*0.75), height//2+(55*i-83)+50, 200, 50, lambda i=i: move_on(i), text=item, color=(100+(i*40), 0, 0)))
    inputs = []
    # Add the player name Inputs
    for i in range(1, 5):
        inputs.append(Input(300, 100*i+100, 200, 50, filler=f'Player {i}\'s name', recenter=False, blacklist=[' ']))
    # Loop to handle each frame and pygame events
    while not done:
        for event in pygame.event.get():
            # Self-explanatory
            if event.type == QUIT: stop_game()
            for item in lvlButtons: item.handle(event)
            for item in inputs: item.handle(event)
        # If no names have been entered, disable the buttons to move on
        if max([len(inpt.text) for inpt in inputs]) == 0:
            for item in lvlButtons: item.disable()
        else:
            for item in lvlButtons: item.enable()
        # Reset the screen and draw each element
        screen_reset(GREY)
        Text('Welcome!', width//2, height//2-200, size=100).draw()
        for i in range(1, 5): Text(f'Player {i}:', 100, 100*i+100, size=40).draw()
        if lvlButtons[0].disabled:
            Text('There must be at least one player to continue', int(width*0.75), height//2+180, color=BLACK, size=18).draw()
        for item in inputs: item.draw()
        for item in lvlButtons: item.draw()
        screen_update()
    global player_names
    player_names = [inpt.text for inpt in inputs]

def create_players():
    players.clear()
    # Take just the player names and create Player objects with those names
    for name in player_names:
        if name != '':
            players.append(Player(name))
    global current, players_copy
    current = players[0]
    # Update the "next" attribute of each Player object
    for item in players:
        item.update_next()
    # Create a copy of the players; used for the leaderboard during end_screen()
    players_copy = deepcopy(players)

def instructions_screen():
    def move_on():
        nonlocal done
        done = True

    instructions = [
    'Find (and click) the hidden BLACK square',
    'The square gets smaller every 5 points',
    f'You get 1 point if you find it, but you lose {lvl.minus} if you miss...',
    f'If you reach {lvl.lose_at} points, it\'s game over', lvl.instruction]
    readyButton = Button(width//2, height-100, 200, 50, move_on, text=f'Ready {players[0].name}?', color=GARNET if lvl.lvl == 3 else BLACK)
    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == QUIT: stop_game()
            readyButton.handle(event)
        # Reset the screen and draw each elements
        screen_reset(BLACK if lvl.lvl == 3 else GREY)
        Text(f'Instructions - {lvl.name.upper()}', width//2, 50, size=72).draw()
        for i, item in enumerate(instructions):
            Text(f'{i+1}. {item}', 20, 125+(i*30), size=32, center=False).draw()
        Text('This is what it looks like:', width//2, height//2, size=24).draw()
        pygame.draw.rect(screen, BLACK, pygame.Rect(width//2-25, height//2+25, 50, 50))
        Text('HA! You can\'t even see it!' if lvl.lvl == 3 else 'It can\'t be that hard...', width//2, height//2+100, size=24).draw()
        Text('Good luck...You\'ll need it...' if lvl.lvl == 3 else 'right?', width//2, height//2+120, size=20, color=GARNET).draw()
        readyButton.draw()
        screen_update()

def info_screen(title, color, lose=False):
    def move_on():
        nonlocal done
        done = True

    def checkPts(val):
        return 'point' if val == 1 else 'points'
    
    # Create the Text objects with empty strings
    nextText = Text('', width//2, height//2+140, size=18, color=BLACK)
    pointsLeft = Text('', width//2, height//2+20, color=BLACK)
    readyButton = Button(width//2, height//2+100, 200, 50, text=f'Ready {current.next.name}?', command=move_on)
    # Set the text under the "Points:" text
    if lose:
        pointsLeft.text = 'You lost too many points'
    else:
        if current.ptsFromLevel == 5 and current.level != 1:
            pointsLeft.text = 'Your box has gotten smaller...'
        elif current.level == 3:
            pointsLeft.text = f'{current.ptsFromLevel} {checkPts(current.ptsFromLevel)} left until you win!'
        elif current.points >= lvl.lose_at+4:
            pointsLeft.text = f'{current.ptsFromLevel} {checkPts(current.ptsFromLevel)} left until level {current.level+1}'
        else:
            ptsLeft = abs(lvl.lose_at-current.points)
            pointsLeft.text = f'{ptsLeft} {checkPts(ptsLeft)} left before you lose...'

    # Set the text under the "ready" button
    if current.next.ptsFromLevel == 5 and current.next.level != 1:
        readyButton.color = PURPLE
        nextText.text = f'Level {current.next.level}...'
    elif current.next.ptsFromLevel == 1 and current.next.level == 3:
        readyButton.btn_width = 2
        readyButton.text.color = BLACK
        nextText.text = f'Last point to win...!'
        
    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == QUIT: stop_game()
            readyButton.handle(event)
        # Reset the screen and draw each element
        screen_reset(color)
        Text(title, width//2, height//2-50, color=BLACK, size=72).draw()
        if not lose: Text(f'Points: {current.points}', width//2, height//2-5, color=BLACK).draw()
        nextText.draw()
        pointsLeft.draw()
        readyButton.draw()
        screen_update()

def switch_player():
    global current
    current = current.next

def check_game_over():
    # Check if the current player has either won (==15) or lost (<=lvl.lose_at)
    if current.points == 15 or current.points <= lvl.lose_at:
        return True
    else:
        return False

def next_level():
    box = create_box()
    pygame.display.flip()
    done = False
    # Start the timer
    start = pygame.time.get_ticks()
    while not done:
        new_frame(box)
        # Check if the time has passed the time allowed for the current level
        if (pygame.time.get_ticks() - start)//1000 >= current.time:
            current.timeout()
            done = True
        else:
            for event in pygame.event.get():
                if event.type == MOUSEBUTTONDOWN and event.button == 1:
                    # If the box is clicked
                    if box.collidepoint(event.pos):
                        print('CLICKED')
                        current.hit()
                        done = True
                    else:
                        print('MISSED')
                        current.miss()
                        done = True
                elif event.type == QUIT: stop_game()
    # Make the box flash white if found, red if not
    for i in range(200):
        new_frame(box, WHITE if current.hit_last and not current.timeout_last else RED)
        new_frame(box, BLACK)
    # Print the current player's stats (for debugging)
    print('', f'Player {current.index+1}:',
        f'Name: {current.name}',
        f'Hit?: {current.hit_last}',
        f'Points: {current.points}',
        f'Box size: {current.box_size}',
        f'Next: {current.next.name}',
        f'Level: {current.level}',
        f'Pts Left: {current.ptsFromLevel}',
        f'Time Limit: {current.time}', sep='\n')

def end_screen(lose=False):
    def move_on():
        nonlocal done
        done = True

    againButton = Button(width//2, height//2+150, 200, 50, move_on, text='Again?')
    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == QUIT: stop_game()
            againButton.handle(event)
        # Reset the screen and draw each element
        screen_reset(GREY if lose else YELLOW)
        Text('GAME OVER' if lose else f'Congratulations {current.name}!', width//2, height//2-200, color=BLACK, size=72).draw()
        if not lose: Text(f'You won on {lvl.name.upper()} mode!', width//2, height//2-145, color=BLACK, size=32).draw()
        for i, player in enumerate(players_copy):
            Text(f'{player.name}: {player.points} points, {player.hits} hits, {player.misses} misses', width//2, height//2+(i*20)-100, color=BLACK).draw()
        againButton.draw()
        screen_update()

def begin_game():
    global lvl
    # Create the screen, start pygame, etc.
    screen_init(1000, 600, GREY, 'FIND THE SQUARE')
    start_screen()
    # Pass the selected difficulty into the Level object to create game vars for difficulty
    lvl = Level(lvl)
    create_players()
    instructions_screen()
    while True:
        next_level()
        if check_game_over():
            # If the player has lost, remove them from the game
            if current.points <= lvl.lose_at:
                # If there are no players left, it's game over
                if len(players)-1 == 0:
                    end_screen(lose=True)
                    break
                # If there still is, just get rid of that one player
                else:
                    info_screen(f'Goodbye {current.name}...', GREY, lose=True)
                    current.out()
                    for item in players: item.update_next()
            else:
                end_screen(lose=False)
                break
        else:
            # Display appropriate info screens based on how the player just did
            if current.timeout_last:
                info_screen('You ran out of time...', DARKORANGE)
            else:
                if current.hit_last:
                    info_screen('You found it!', GREEN)
                else:
                    info_screen('You missed it...', RED)
        # Switch to next player and start this whole process again
        switch_player()
    begin_game()

# Start the game automatically
begin_game()