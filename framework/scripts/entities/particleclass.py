#### Imports ####
import pygame, random


#### Class(es) ####
class ParticleManager:
    def __init__(self):
        self.particle_list = []

    def show_particles(self, surf, scroll):
        particle_list = self.particle_list.copy()
        for particle in particle_list:
            particle.display_self(surf, scroll)

    def add_particle(self, particle):
        self.particle_list.append(particle)

    def remove_particle(self, particle):
        self.particle_list.remove(particle)

    def remove_all_particles(self):
        self.particle_list = []


class Particle:
    def __init__(self, pos, size):
        self.pos = pos
        self.size = size
        self.color = [255, 50, 0]

    def display_self(self, surf, scroll):
        color = self.color
        pygame.draw.circle(surf, color, (self.pos[0] - scroll[0], self.pos[1] - scroll[1]), self.size)
        self.pos[1] -= random.randint(-1, 1)
        self.pos[0] -= random.randint(-1, 1)
        self.size -= 0.2
        if self.color[1] < 255 - 3:
        	self.color[1] += 5