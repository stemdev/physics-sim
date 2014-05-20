import math
import pygame

class Gfield:
    """ Origin drawn at the top center of pygame window,
        with the positive y-axis directed upward.
    """
    def __init__(self, screen):
        self.g = 9.8
        self.screen=screen

    def force(self, xy=(0,0), m=1):
        return 0, -1*mass*self.g
    
    def _trans(self, xy):
        """ Transformation into pygame coordinates
        """
        x,y = xy
        return (x+self.screen.get_width()/2, -1*y+self.screen.get_height()/10)

class Pendulum(Gfield):
    def __init__(self, screen, fps, radius=1, theta=math.pi*3/2, th_d1=0, mass=1):
        """ Accept initial conditions for a `Pendulum` object.
            `theta` is in radians, and `th_d1` represents angular velocity.
            
            The pendulum is attached to the origin, and swings in the
            third and fourth quadrants.
        """
        Gfield.__init__(self, screen)
        self.r=radius*100
        self.th=theta
        self.th_d1=th_d1
        self.th_d2=0
        self.mass=mass
        self.dt=(1.0/fps)*10

    def _potential(self):
        """ Return potential energy of self
        """
        return self.mass*self.g*(self.r*math.sin(self.th)+self.r)
    
    def _kinetic(self):
        """ Return the potential energy of self
        """
        return (0.5)*self.mass*(self.r*self.th_d1)**2

    def _get_pos(self):
        """ Return an integer representation of position
        """
        x, y = self._get_coords()
        return int(x), int(y)

    def _get_coords(self, mode='cartesian'):
        """ Return coordinates in cartesian or polar coordinates
        """
        return {
            'cartesian': ( self.r*math.cos(self.th), self.r*math.sin(self.th) ),
            'polar': (self.r, self.th)
        }[mode]

    def _draw(self, delete=False):
        """ Draw to the screen
        """
        if delete:
            color = (0,0,0)
        else:
            color = (100,0,50)

        ball_position = self._trans(self._get_pos())
        pygame.draw.circle(
            self.screen,
            color,
            ball_position,
            10
        )

        pygame.draw.line(
            self.screen,
            color,
            self._trans((0,0)),
            ball_position,
            2
        )
        
        scrwidth = self.screen.get_width()
        scrheight = self.screen.get_height()

        pygame.draw.line(
            self.screen,
            color,
            self._trans((-0.9*scrwidth/2, -scrheight*.8)),
            self._trans((-0.9*scrwidth/2, -scrheight*.8 + self._potential()*.2)),
            5
        )
        
        pygame.draw.line(
            self.screen,
            color,
            self._trans((-0.8*scrwidth/2, -scrheight*.8)),
            self._trans((-0.8*scrwidth/2, -scrheight*.8 + self._kinetic()*.2)),
            5
        )
    
    def render(self):
        self._draw(delete=True)
        
        th = self.th
        self.th_d2 = -1*self.g*math.cos(th)/self.r # from the lagrangian
        self.th_d1 = self.th_d1 + self.th_d2*self.dt
        self.th = self.th + self.th_d1*self.dt
        
        self._draw()


width, height = 1280, 900
screen = pygame.display.set_mode((width, height))
mainClock=pygame.time.Clock()

fps = 10
pend = Pendulum(screen, fps, theta=math.pi+.5, radius=5)

while True:
    pend.render()
    pygame.display.flip()
    mainClock.tick(fps)


