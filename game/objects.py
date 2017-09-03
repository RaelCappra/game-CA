import pygame
from pygame.sprite import Group, GroupSingle, groupcollide

UP = 0, -1
DOWN = 0, 1

class GameObject(pygame.sprite.Sprite):
    def __init__(self, key, type, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('data/{}/{}.png'.format(type, key)).convert_alpha()
        self.rect = pygame.Rect(position[0], position[1], self.image.get_rect().size[0], self.image.get_rect().size[1])
    
    def setPosition(self, position):
        self.rect.x = position[0]
        self.rect.y = position[1]

    def touchingRightBorder(self):
        if(self.rect.right >= 640):
            return True
        return False

    def touchingLeftBorder(self):    
        if(self.rect.left <= 0):
            return True
        return False

    def getPosition(self):
        return (self.rect.x, self.rect.y)

    def draw(self, surface):
        surface.blit(self.image, (self.rect.x, self.rect.y))

    def move(self):
        GameObject.setPosition(self, (self.rect.x + self.speed[0], self.rect.y + self.speed[1]))

class Shot(GameObject):
    def __init__(self, key, position, direction, speed, damage = 1):
        GameObject.__init__(self, key, 'shots', position)
        self.damage = damage
        self.speed = (speed * direction[0], speed * direction[1])

        if(direction == DOWN):
            self.image = pygame.transform.rotate(self.image, 180)

    def checkUpperBorder(self):
        if(self.rect.bottom < 0):
            self.kill()

    def do(self):
        self.move()
        self.checkUpperBorder()

class Entity(GameObject):
    def __init__(self, key, position, shot_key, shot_speed, life, speed):
        GameObject.__init__(self, key, 'entities', position)
        self.abs_speed = speed
        self.speed = (0, 0)
        self.life = life
        self.shots = Group()

        self.shot_key = shot_key
        self.shot_speed = shot_speed

    def setSpeed(self, direction):
        self.speed = (direction[0] * self.abs_speed, direction[1] * self.abs_speed)
 
    def shoot(self):
        temp_image = pygame.image.load('data/shots/{}.png'.format(self.shot_key)).convert_alpha()
        position = (self.rect.x + self.rect.width/2 - temp_image.get_rect().width/2, self.rect.y)
        shot = Shot(self.shot_key, position, self.shot_direction, self.shot_speed)
        self.shots.add(shot)

    def update(self):
        if self.life == 0:
            self.kill()

        GameObject.update(self)
        for shot in self.shots:
            shot.update()

    def draw(self, surface):
        GameObject.draw(self, surface)
        for shot in self.shots:
            shot.draw(surface)

    def do(self):
        self.move()
        self.speed = (0, 0)

        for shot in self.shots:
            shot.do()

class Player(Entity):
    def __init__(self, key, position, shot_key = '1', shot_speed = 4, life = 10, speed = 4, score = 0):
        Entity.__init__(self, key, position, shot_key, shot_speed, life, speed)
        self.score = score
        self.shot_direction = (0, -1)

class Monster(Entity):
    def __init__(self, key, position, shot_key, shot_speed, life = 10, speed = 2):
        Entity.__init__(self, key, position, shot_key, shot_speed, life, speed)
        self.shot_direction = (0, 1)
