"""
stanCode Breakout Project
Adapted from Eric Roberts's Breakout by
Sonja Johnson-Yu, Kylie Jue, Nick Bowman,
and Jerry Liao
"""

from campy.gui.events.timer import pause
from breakoutgraphics import BreakoutGraphics


FRAME_RATE = 1000 / 60  # 60 frames per second.
NUM_LIVES = 3


def main():
    """
    This program plays a Breakout game. A ball will be bouncing in the window,
    players use the paddle to make ball bounce to collide bricks and remove them.
    If the ball moves out of the bottom of the window, the game will restart a new round.
    After NUM_LIVES rounds or all bricks are removes, the game will be finished.
    """
    graphics = BreakoutGraphics()
    dx = graphics.get_dx()
    dy = graphics.get_dy()
    left_cnt = NUM_LIVES

    while True:
        # if lost all lives or remove all bricks then stopping the loop
        if left_cnt == 0 or graphics.brick_cnt == 0:
            graphics.game_over()
            break
        else:
            if graphics.start == 1:
                graphics.ball.move(dx, dy)
                # if ball moves over the bottom of window, restart a round
                if graphics.ball.y > graphics.window.height - graphics.ball.height:
                    # reset the ball at the start point
                    graphics.set_ball()
                    left_cnt -= 1
                    # turn the start switch from 1 to 0 to prepare the next start
                    graphics.start = 0
                # change the moving direction when the ball collides to window
                if graphics.ball.x < 0 or graphics.ball.x > graphics.window.width - graphics.ball.width:
                    dx = -dx
                if graphics.ball.y < 0:
                    dy = -dy
                # change the moving direction when the ball collides to paddle
                if graphics.collide_paddle() and dy > 0:
                    dy = -dy
                # change the moving direction when the ball collides to brick
                if graphics.ball.y + graphics.ball.height < graphics.paddle.y:
                    # change dy when the ball collides brick by top or bottom
                    if graphics.collide_brick_top_bottom():
                        dy = -dy
                    # change dx when the ball collides brick by left or right side
                    if graphics.collide_brick_left_right():
                        dx = -dx
                    # change both dx and dy when the ball collides brick by one point
                    if graphics.collide_brick_one_point():
                        dy = -dy
                        dx = -dx
            pause(FRAME_RATE)


if __name__ == '__main__':
    main()
