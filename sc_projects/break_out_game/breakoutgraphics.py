"""
stanCode Breakout Project
Adapted from Eric Roberts's Breakout by
Sonja Johnson-Yu, Kylie Jue, Nick Bowman, 
and Jerry Liao
"""
from campy.graphics.gwindow import GWindow
from campy.graphics.gobjects import GOval, GRect, GLabel
from campy.graphics.gimage import GImage
from campy.gui.events.mouse import onmouseclicked, onmousemoved
import random


BRICK_SPACING = 5      # Space between bricks (in pixels). This space is used for horizontal and vertical spacing.
BRICK_WIDTH = 40       # Height of a brick (in pixels).
BRICK_HEIGHT = 15      # Height of a brick (in pixels).
BRICK_ROWS = 10        # Number of rows of bricks.
BRICK_COLS = 10        # Number of columns of bricks.
BRICK_OFFSET = 50      # Vertical offset of the topmost brick from the window top (in pixels).
BALL_RADIUS = 10       # Radius of the ball (in pixels).
PADDLE_WIDTH = 75      # Width of the paddle (in pixels).
PADDLE_HEIGHT = 15     # Height of the paddle (in pixels).
PADDLE_OFFSET = 50     # Vertical offset of the paddle from the window bottom (in pixels).

INITIAL_Y_SPEED = 7.0  # Initial vertical speed for the ball.
MAX_X_SPEED = 5        # Maximum initial horizontal speed for the ball.


class BreakoutGraphics:

    def __init__(self, ball_radius = BALL_RADIUS, paddle_width = PADDLE_WIDTH,
                 paddle_height = PADDLE_HEIGHT, paddle_offset = PADDLE_OFFSET,
                 brick_rows = BRICK_ROWS, brick_cols = BRICK_COLS,
                 brick_width = BRICK_WIDTH, brick_height = BRICK_HEIGHT,
                 brick_offset = BRICK_OFFSET, brick_spacing = BRICK_SPACING,
                 title='Breakout'):

        # Create a graphical window, with some extra space.
        window_width = brick_cols * (brick_width + brick_spacing) - brick_spacing
        window_height = brick_offset + 3 * (brick_rows * (brick_height + brick_spacing) - brick_spacing)
        self.window = GWindow(width=window_width, height=window_height, title=title)

        # Create a paddle.
        self.paddle = GRect(paddle_width, paddle_height)
        self.paddle.filled = True
        self.window.add(self.paddle, x=(window_width-paddle_width)/2, y=window_height-paddle_offset)

        # Center a filled ball in the graphical window.
        self.ball = GOval(ball_radius*2, ball_radius*2)
        self.ball.filled = True
        self.set_ball()

        # Default initial velocity for the ball.
        self.__dy = INITIAL_Y_SPEED
        self.__dx = random.randint(1, MAX_X_SPEED)
        self.set_velocity()

        # Set start switch.
        self.start = 0

        # Initialize our mouse listeners.
        onmousemoved(self.paddle_move)
        onmouseclicked(self.click_start)

        # Draw bricks.
        colors = ['navy', 'darkslateblue', 'steelblue', 'skyblue', 'powderblue']
        for i in range(brick_rows):
            color_i = (i//2) % len(colors)
            for j in range(brick_cols):
                self.brick = GRect(brick_width, brick_height)
                self.brick.filled = True
                self.brick.fill_color = colors[color_i]
                self.brick.color = colors[color_i]
                self.window.add(self.brick, x=(brick_width + brick_spacing) * j,
                                y=brick_offset + (brick_height + brick_spacing) * i)

        # Count the number of bricks.
        self.brick_cnt = brick_rows * brick_cols

        # Set ending picture.
        self.img = GImage('GG.jpg')

    def set_ball(self):
        """
        Sets the ball position to the center of the window.
        """
        self.window.add(self.ball, x=(self.window.width-self.ball.width)/2, y=(self.window.height-self.ball.height)/2)

    def set_velocity(self):
        """
        Sets ball x velocity to a random positive or negative number.
        """
        if random.random() > 0.5:
            self.__dx = -self.__dx

    def paddle_move(self, mouse):
        """
        Makes paddle to move left and right following the mouse. The paddle keeps the same height and in the window.
        :param mouse: mouse move
        """
        if mouse.x > self.window.width - self.paddle.width:
            self.paddle.x = self.window.width - self.paddle.width
        elif mouse.x < 0:
            self.paddle.x = 0
        else:
            self.paddle.x = mouse.x - self.paddle.width/2

    def ball_at_start(self):
        """
        Check the ball position is at the starting point.
        :return: boolean
        """
        return self.ball.x == (self.window.width-self.ball.width)/2 and\
               self.ball.y == (self.window.height-self.ball.height)/2

    def click_start(self, click):
        """
        Check the ball position when mouse is clicked.
        If the ball is at starting point, turn the start switch from 0 to 1 to start the game.
        :param click: mouse click
        """
        if self.ball_at_start():
            self.start = 1

    def obj1(self):
        """
        Check whether there is any object at the upper left point of the ball.
        :return: object
        """
        obj1 = self.window.get_object_at(self.ball.x, self.ball.y)
        if obj1 is not None:
            return obj1

    def obj2(self):
        """
        Check whether there is any object at the upper right point of the ball.
        :return: object
        """
        obj2 = self.window.get_object_at(self.ball.x + self.ball.width, self.ball.y)
        if obj2 is not None:
            return obj2

    def obj3(self):
        """
        Check whether there is any object at the lower left point of the ball.
        :return: object
        """
        obj3 = self.window.get_object_at(self.ball.x, self.ball.y+self.ball.height)
        if obj3 is not None:
            return obj3

    def obj4(self):
        """
        Check whether there is any object at the lower right point of the ball.
        :return: object
        """
        obj4 = self.window.get_object_at(self.ball.x+self.ball.width, self.ball.y+self.ball.height)
        if obj4 is not None:
            return obj4

    def collide_paddle(self):
        """
        Check whether the ball collides the paddle.
        :return: boolean
        """
        # just check the bottom side of the ball
        if self.obj3() == self.paddle or self.obj4() == self.paddle:
            return True

    def collide_brick_top_bottom(self):
        """
        Check whether the ball collides the bricks by top side or bottom side and then remove them.
        :return: boolean
        """
        # Check the top side.
        if self.obj1() is not None and self.obj2() is not None:
            # if the upper two point of the ball collides the same brick, just remove once.
            if self.obj1() == self.obj2():
                self.window.remove(self.obj2())
                self.brick_cnt -= 1
            # if the upper two point of the ball collides different bricks, remove both bricks.
            else:
                self.window.remove(self.obj1())
                self.brick_cnt -= 1
                self.window.remove(self.obj2())
                self.brick_cnt -= 1
            return True
        # Check the bottom side.
        if self.obj3() is not None and self.obj4() is not None:
            if self.obj3() == self.obj4():
                self.window.remove(self.obj4())
                self.brick_cnt -= 1
            else:
                self.window.remove(self.obj3())
                self.brick_cnt -= 1
                self.window.remove(self.obj4())
                self.brick_cnt -= 1
            return True

    def collide_brick_left_right(self):
        """
        Check whether the ball collides the bricks by left side or right side and then remove them.
        :return: boolean
        """
        # Check the left side.
        if self.obj1() is not None and self.obj3() is not None:
            if self.obj1() == self.obj3():
                self.window.remove(self.obj1())
                self.brick_cnt -= 1
            else:
                self.window.remove(self.obj1())
                self.brick_cnt -= 1
                self.window.remove(self.obj3())
                self.brick_cnt -= 1
            return True
        # Check the right side.
        if self.obj2() is not None and self.obj4() is not None:
            if self.obj2() == self.obj4():
                self.window.remove(self.obj2())
                self.brick_cnt -= 1
            else:
                self.window.remove(self.obj2())
                self.brick_cnt -= 1
                self.window.remove(self.obj4())
                self.brick_cnt -= 1
            return True

    def collide_brick_one_point(self):
        """
        Check whether the ball collides the brick by just one point and then remove it.
        :return: boolean
        """
        # Check the upper left point.
        if self.obj1() is not None and self.obj2() is None and self.obj3() is None and self.obj4() is None:
            self.window.remove(self.obj1())
            self.brick_cnt -= 1
            return True
        # Check the upper right point.
        if self.obj2() is not None and self.obj1() is None and self.obj3() is None and self.obj4() is None:
            self.window.remove(self.obj2())
            self.brick_cnt -= 1
            return True
        # Check the lower left point.
        if self.obj3() is not None and self.obj1() is None and self.obj2() is None and self.obj4() is None:
            self.window.remove(self.obj3())
            self.brick_cnt -= 1
            return True
        # Check the lower right point.
        if self.obj4() is not None and self.obj1() is None and self.obj2() is None and self.obj3() is None:
            self.window.remove(self.obj4())
            self.brick_cnt -= 1
            return True

    def game_over(self):
        """
        If the loop of the game is stopped, show the 'game over' image.
        """
        self.window.add(self.img, x=(self.window.width-self.img.width)/2, y=(self.window.height-self.img.height)/2)

    # Getter
    def get_dx(self):
        """
        Get the private variable __dx.
        """
        return self.__dx

    def get_dy(self):
        """
        Get the private variable __dy.
        """
        return self.__dy
