import numpy as np
import pygame
import time

WIDTH, HEIGHT = 1600, 1200
INFECTION_DURATION = 10

cols = {
    "susceptible": (200, 200, 200),
    "infected": (255, 0, 0),
    "recovered": (0, 255, 0),
    "dead": (0, 0, 0),
}


class Ball:
    def __init__(self):
        self.x = np.random.randint(0, WIDTH)
        self.y = np.random.randint(0, HEIGHT)
        self.dx = np.random.randn()
        self.dy = np.random.randn()
        # self.diameter = 10
        self.radius = 10
        self.state = "susceptible"
        self.infection_start = None

    def draw(self, screen):
        pygame.draw.circle(
            screen, cols[self.state], (int(self.x), int(self.y)), self.radius
        )

    def move(self):
        self.x = self.x + self.dx
        self.y = self.y + self.dy

        # collision detection against edge of window
        if self.x - self.radius < 0:
            self.x = 0 + self.radius
            self.dx = -self.dx
        elif self.x + self.radius > WIDTH:
            self.x = WIDTH - self.radius
            self.dx = -self.dx

        if self.y - self.radius < 0:
            self.y = 0 + self.radius
            self.dy = -self.dy
        elif self.y + self.radius > HEIGHT:
            self.y = HEIGHT - self.radius
            self.dy = -self.dy

    def intersects(self, other):
        """Do I intersect with another ball?"""
        return np.hypot(self.x - other.x, self.y - other.y) < self.radius * 2

    def infect(self):
        self.state = "infected"
        self.infection_start = time.time()

    def die(self):
        """I died"""
        self.state = "dead"
        self.dx, self.dy = 0, 0

    def disease_progression(self):
        if self.state is "infected":
            # maybe die
            if np.random.random() < 0.0001:
                self.die()

            # recover after disease has run its course
            infection_time = time.time() - self.infection_start
            if infection_time > INFECTION_DURATION:
                self.state = "recovered"


class Population:
    """Make a collection of balls"""

    def __init__(self, N):
        self.N = N
        self.balls = [Ball() for _ in range(self.N)]
        # infect patient zero
        self.balls[0].infect()

    def update(self):
        # move
        for ball in self.balls:
            ball.move()

        # check for interaction
        for i in range(self.N):
            for j in range(i + 1, self.N):
                if self.balls[i].intersects(self.balls[j]):
                    self.interaction(i, j)

        # progress disease
        for ball in self.balls:
            ball.disease_progression()

    def draw(self, screen):
        for ball in self.balls:
            ball.draw(screen)

    def interaction(self, i, j):
        if (self.balls[i].state is "infected") & (self.balls[j].state is "susceptible"):
            self.balls[j].infect()
        elif (self.balls[i].state is "susceptible") & (
            self.balls[j].state is "infected"
        ):
            self.balls[i].infect()
