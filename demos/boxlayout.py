import sys
sys.path.append('..')
from urpyg import *

class BoxLayoutApp(Window):
    def init(self):
        self.layout = BoxLayout(
            BoxLayout(
                Rectangle(0, 0, 0, 0, GREEN),
                orientation = 'h'
            ),
            BoxLayout(
                Rectangle(0, 0, 0, 0),
                Rectangle(0, 0, 0, 0, MAGENTA),
                orientation = 'h'
            ),
            x = 0, y = 0
        )

        self.labels = Group(
            Label('hi', percent_of(25, self.width), percent_of(75, self.height))
        )

    def input(self, key):
        if key == 'left mouse down':
            if self.layout[1][0].is_hovered(mouse.x, mouse.y):
                self.labels[0].text = 'clicked' if self.labels[0].text == 'hi' else 'hi'

    def resize(self, width, height):
        self.labels[0].x, self.labels[0].y = percent_of(25, width), percent_of(75, height)

    def render(self):
        self.layout.render(self.width, self.height)
        self.labels.render()

if __name__ == '__main__':
    BoxLayoutApp(resizable = True).run()
