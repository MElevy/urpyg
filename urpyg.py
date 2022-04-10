import pyglet, random
from pyglet import clock

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

keys = {
    'up arrow' : pyglet.window.key.UP,
    'down arrow' : pyglet.window.key.DOWN,
    'right arrow' : pyglet.window.key.RIGHT,
    'left arrow' : pyglet.window.key.LEFT,
    'enter' : pyglet.window.key.ENTER,
    'space' : pyglet.window.key.SPACE,
    'backspace' : pyglet.window.key.BACKSPACE,
    'left control' : pyglet.window.key.LCTRL,
    'right control' : pyglet.window.key.RCTRL,
}

modifiers = {
    'shift' : pyglet.window.key.MOD_SHIFT,
    'control' : pyglet.window.key.MOD_CTRL 
}

buttons = {
    'left' : pyglet.window.mouse.LEFT,
    'middle' : pyglet.window.mouse.MIDDLE,
    'right' : pyglet.window.mouse.RIGHT
}

held_alphabet = { name : 0 for name in 'qwertyuiopasdfghjklzxcvbnm'}
held_numbers = { str(name) : 0 for name in '1234567890' }

held_keys = dict(**held_alphabet, **held_numbers, shift = 0, space = 0, backspace = 0, enter = 0, escape = False)
held_keys['up arrow'] = 0
held_keys['down arrow'] = 0
held_keys['right arrow'] = 0
held_keys['left arrow'] = 0
held_keys['left mouse'] = 0
held_keys['right mouse'] = 0
held_keys['middle mouse'] = 0
held_keys['+'] = 0
held_keys['-'] = 0
held_keys['='] = 0

held_modifiers = {
    'shift' : 0,
    'control' : 0
}

del held_alphabet
del held_numbers

class Mouse:
    x = 0
    y = 0
    dx = 0
    dy = 0
    clicked = 0
    dragged = 0
    def __init__(self):
        pass

mouse = Mouse()

class Window:
    def __init__(self, title = '', fullscreen = False, resizable = False, interval = 1 / 60, mouse_enabled = True):
        self._window = pyglet.window.Window(caption = title, fullscreen = fullscreen, resizable = resizable)
        self._title = title
        self._resizable = resizable
        self._mouse_enabled = mouse_enabled
        self.key_press_actions = []
        self.mouse_press_actions = []

        self._window.set_exclusive_mouse(not mouse_enabled)

        self.init()

        clock.schedule_interval(self.update, interval)

    def init(self):
        pass

    def update(self, dt: float):
        pass

    def input(self, key):
        pass

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        self._title = value
        self._window.set_caption(value)

    @property
    def resizable(self) -> bool:
        return self._resizable
    
    @resizable.setter
    def resizable(self, value: bool):
        self._resizable = value
        self._window,resizable = value

    @property
    def width(self) -> int:
        return self._window.width

    @width.setter
    def width(self, value: int):
        self._window.width = value
	
    @property
    def height(self) -> int:
        return self._window.height

    @height.setter
    def height(self, value: int):
        self._window.height = value

    @property
    def mouse_enabled(self) -> bool:
        return self._mouse_enabled

    @mouse_enabled.setter
    def mouse_enabled(self, value: bool):
        self._mouse_enabled = value
        self._window.set_exclusive_mouse(not values)

    def render(self):
        pass

    def run(self):
        window = self._window

        @window.event
        def on_draw():
            window.clear()
            self.render()

        @window.event
        def on_key_press(symbol, mods):
            keys_rev = {keyCode: keyName for keyName, keyCode in keys.items()}
            if symbol not in keys.values():
                held_keys[chr(symbol)] = 1
                self.input(chr(symbol) + ' down')
            else:
                held_keys[keys_rev[symbol]] = 1
                self.input(keys_rev[symbol] + ' down')

            if mods & modifiers['shift']:
                held_modifiers['shift'] = 1

            if mods & modifiers['control']:
                held_modifiers['control'] = 1

        @window.event
        def on_key_release(symbol, mods):
            keys_rev = {keyCode: keyName for keyName, keyCode in keys.items()}
            if symbol not in keys.values():
                held_keys[chr(symbol)] = 0
                self.input(chr(symbol) + ' up')
            else:
                held_keys[keys_rev[symbol]] = 0
                self.input(keys_rev[symbol] + ' up')

            if not mods & modifiers['shift']:
                held_modifiers['shift'] = 0

            if not mods & modifiers['control']:
                held_modifiers['control'] = 0

        @window.event
        def on_mouse_motion(x, y, dx, dy):
            mouse.x = x
            mouse.y = y
            mouse.dx = dx
            mouse.dy = dy

        @window.event
        def on_mouse_press(x, y, button, mods):
            mouse.x = x
            mouse.y = y
            mouse.clicked = 1

            if button == buttons['left']:
                held_keys['left mouse'] = 1
                self.input('left mouse down')
            elif button == buttons['right']: 
                held_keys['right mouse'] = 1
                self.input('right mouse down')
            else: 
                held_keys['middle mouse'] = 1
                self.input('middle mouse down')

            if mods & modifiers['shift']:
                held_modifiers['shift'] = 1

            if mods & modifiers['control']:
                held_modifiers['control'] = 1

        @window.event
        def on_mouse_release(x, y, button, mods):
            mouse.x = x
            mouse.y = y
            mouse.clicked = 0
            mouse.dragged = 0

            if button == buttons['left']:
                held_keys['left mouse'] = 0
                self.input('left mouse up')
            elif button == buttons['right']:
                held_keys['right mouse'] = 0
                self.input('right mouse up')
            else: 
                held_keys['middle mouse'] = 0
                self.input('middle mouse up')

            if not mods & modifiers['shift']:
                held_modifiers['shift'] = 0

            if not mods & modifiers['control']:
                held_modifiers['control'] = 0

        @window.event
        def on_mouse_drag(x, y, dx, dy, button, mods):
            mouse.x = x
            mouse.y = y
            mouse.dx = dx
            mouse.dy = dy

            mouse.dragged = 1

            for mouse_press_action in self.mouse_press_actions:
                mouse_press_action(x, y, button, mods)

            if button == buttons['left']: held_keys['left mouse'] = 1
            elif button == buttons['right']: held_keys['right mouse'] = 1
            else: held_keys['middle mouse'] = 1

            if mods & modifiers['shift']:
                held_modifiers['shift'] = 1

            if mods & modifiers['control']:
                held_modifiers['control'] = 1

        pyglet.app.run()

class ElementBase:
    def __init__(self, element, *args, x = 0, y = 0, color = (0, 0, 0), anchored = True, colored = True,  **kwargs):
        self._element = (element(*args, x = x, y = y, anchor_x = 'center', anchor_y = 'center', **kwargs) if anchored 
            else element(*args, x = x, y = y, **kwargs))

        if colored:
            self._element.color = color

    def move_towards(self, x, y, speed):
        if self.x < x:
            self.x += speed
        elif self.x > x:
            self.x -= speed

        if self.y < y:
            self.y += speed
        elif self.y > y:
            self.y -= speed

    def move_x_towards(self, x, speed):
        if self.x < x:
            self.x += speed
        elif self.x > x:
            self.x -= speed

    def move_y_towards(self, y, speed):
        if self.y < y:
            self.y += speed
        elif self.y > y:
            self.y -= speed

    @property
    def x(self) -> int:
        return self._element.x

    @x.setter
    def x(self, value: int):
        self._element.x = value

    @property
    def y(self) -> int:
        return self._element.y

    @y.setter
    def y(self, value: int):
        self._element.y = value

    @property
    def color(self):
        return self._element.color

    @color.setter
    def color(self, value):
        self._element.color = value

    def render(self):
        return self._element.draw()


class Label(ElementBase):
    def __init__(self, text = '', x = 0, y = 0, font = ('sans serif', 18), color = (255, 255, 255, 1000)):
        super().__init__(pyglet.text.Label, text, x = x, y = y, color = color, font_name = font[0], font_size = font[1])

    @property
    def text(self):
        return self._element.text
    
    @text.setter
    def text(self, value):
        self._element.text = value

    @property
    def font(self):
        return self._element.font_name, self._element.font_size

    @font.setter
    def font(self, value):
        self._element.font_name = value[0]
        self._element.font_size = value[1]

class Rectangle(ElementBase):
    def __init__(self, x = 0, y = 0, width = 0, height = 0, color = (200, 10, 10), opacity = 1000):
        super().__init__(pyglet.shapes.Rectangle, x = x, y = y, anchored = False, width = width, height = height, color = color)
        self._element.opacity = opacity

    def distance(self, x, y, width, height):
        dist_x, dist_y = 0, 0
        if x < self.x: 
            dist_x = x - (self.x + self.width)
        elif x > self.x:
            dist_x = (x + width) - self.x

        if y < self.y: 
            dist_y = x - (self.y + self.height)
        elif y > self.y:
            dist_y = (y + height) - self.y

        return dist_x, dist_y

    def is_colliding(self, other, type = 'rectangle'):
        left, right = self.x, self.x + self.width
        bottom, top = self.y, self.y + self.height

        colliding = 1

        if type.lower() in ('rectangle', 'rect', 'sprite', 'img', 'image'):
            other_left, other_right = other.x, other.x + other.width
            other_bottom, other_top = other.y, other.y + other.height

            if top < other_bottom or bottom > other_top or right < other_left or left > other_right:
                colliding = 0

        return colliding

    def is_hovered(self, x, y):
        left, right = self.x, self.x + self.width
        bottom, top = self.y, self.y + self.height

        hovered = 1

        if x > right or x < left or y > top or y < bottom:
            hovered = 0

        return hovered

    @property
    def width(self):
        return self._element.width

    @width.setter
    def width(self, value):
        self._element.width = value

    @property
    def height(self):
        return self._element.height

    @height.setter
    def height(self, value):
        self._element.height = value

    @property
    def opacity(self):
        return self._element.opacity

    @opacity.setter
    def opacity(self, value):
        self._element.opacity = value

class Sprite(ElementBase):
    def __init__(self, source, x = 0, y = 0, width = 0, height = 0):
        self._image = pyglet.image.load(source)
        self._image.width, self._image.height = width, height

        super().__init__(pyglet.sprite.Sprite, x = x, y = y, colored = False, anchored = False, img = self.image)

    def distance(self, x, y, width, height):
        dist_x, dist_y = 0, 0
        if x < self.x: 
            dist_x = x - (self.x + self.width)
        elif x > self.x:
            dist_x = (x + width) - self.x

        if y < self.y: 
            dist_y = x - (self.y + self.height)
        elif y > self.y:
            dist_y = (y + height) - self.y

        return dist_x, dist_y

    def is_colliding(self, other, type = 'rectangle'):
        left, right = self.x, self.x + self.width
        bottom, top = self.y, self.y + self.height

        colliding = 1

        if type.lower() in ('rectangle', 'rect', 'sprite', 'img', 'image'):
            other_left, other_right = other.x, other.x + other.width
            other_bottom, other_top = other.y, other.y + other.height

            if top < other_bottom or bottom > other_top or right < other_left or left > other_right:
                colliding = 0

        return colliding

    def is_hovered(self, x, y):
        left, right = self.x, self.x + self.width
        bottom, top = self.y, self.y + self.height

        hovered = 1

        if x > right or x < left or y > top or y < bottom:
            hovered = 0

        return hovered

    @property
    def width(self):
        return self._image.width

    @width.setter
    def width(self, value):
        self._image.width = value

    @property
    def height(self):
        return self._image.height

    @height.setter
    def height(self, value):
        self._image.height = value

    @property
    def image(self):
        return self._image

    @image.setter
    def image(self, value):
        self._image = pyglet.image.load(value)
        self.height, self.width = self.height, self.width

class Group:
    def __init__(self, *args):
        self.group = list(args)

    def add(self, *args):
        for arg in args:
            self.group.append(arg)

    def delete(self, index):
        del self.group[index]

    def index(self, value):
        return self.group.index(value)

    def __getitem__(self, index):
        return self.group[index]

    def __setitem__(self, index, value):
        self.group[index] = value

    def __len__(self):
        return len(self.group)

    def render(self):
        for item in self.group:
            item.render()

def schedule(interval_time = 1.0):
    def init_schedule(func):
        def call_schedule(*args, **kwargs):
            return func(*args, **kwargs)

        pyglet.clock.schedule_once(func, interval)
        return call_schedule
    return init_schedule

def interval(interval_time = 1.0):
    def init_interval(func):
        def call_interval(*args, **kwargs):
            return func(*args, **kwargs)

        pyglet.clock.schedule_interval(func, interval_time)
        return call_interval
    return init_interval

if __name__ == '__main__':
    class MyApp(Window):
        def init(self):
            self.score = 0
            self.playerSpeed = 300
            self.player_on_cooldown = False
            self.player = Rectangle(10, self.height // 2, 50, 50, (10, 20, 200))
            self.obstacle = Rectangle(self.width // 2, 10, 60, 60, (200, 10, 10))
            self.obstacle2 = Rectangle(self.width // 2, 10, 60, 60, (200, 10, 10))
            self.score_lbl = Label(str(self.score), self.width - 100, self.height - 50)

        def update(self, dt): 
            # self.player.y += (held_keys['up arrow'] - held_keys['down arrow']) * 200 * dt
            # self.player.x += (held_keys['right arrow'] - held_keys['left arrow']) * 200 * dt

            # self.player.move_towards(mouse.x, mouse.y, self.playerSpeed * dt)

            self.obstacle.move_towards(self.player.x + random.randrange(-50, 50), self.player.y + random.randrange(-50, 50), 125 * dt)
            self.obstacle2.move_towards(mouse.x, mouse.y, 125 * dt)

            # if held_keys['left mouse'] and not self.player_on_cooldown:
            #     self.playerSpeed = 1000
            #     self.player_on_cooldown = random.choice([True, True, False])

            # self.player_on_cooldown = random.choice([False, False, False, False, True, True, True])
            # self.playerSpeed = 300

            if not mouse.clicked:
                self.player.x, self.player.y = mouse.x - self.player.width // 2, mouse.y - self.player.height // 2

            if self.player.is_colliding(self.obstacle) or self.player.is_colliding(self.obstacle2) or held_keys['escape']:
                quit()

        def render(self):
            self.player.render()
            self.obstacle.render()
            self.obstacle2.render()
            self.score_lbl.render()

    myapp = MyApp(title = 'Test', fullscreen = True, mouse_enabled = True)

    @interval(1)
    def survive_time(dt):
        myapp.score += 1
        myapp.score_lbl.text = str(myapp.score)

    myapp.run()