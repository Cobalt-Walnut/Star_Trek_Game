#DO NOT CHANGE UNLESS YOU KNOW WHAT YOU'RE DOING.
#IF YOU DO, THE GAME MAY NOT WORK.
#DO NOT CHANGE UNLESS YOU KNOW WHAT YOU'RE DOING.
#IF YOU DO, THE GAME MAY NOT WORK.
#DO NOT CHANGE UNLESS YOU KNOW WHAT YOU'RE DOING.
#IF YOU DO, THE GAME MAY NOT WORK.
#DO NOT CHANGE UNLESS YOU KNOW WHAT YOU'RE DOING.
#IF YOU DO, THE GAME MAY NOT WORK.
#DO NOT CHANGE UNLESS YOU KNOW WHAT YOU'RE DOING.
#IF YOU DO, THE GAME MAY NOT WORK.

import pygame
import random
import math
import time
import asyncio

WIDTH, HEIGHT = 1400, 800

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
ORANGE = (255, 165, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
LIGHT_BLUE = (173, 216, 230)


# Loads all images needed
def load_images():
    images = {
        "constitution": pygame.image.load("assets/constitution_class.png").convert_alpha(),
        "galaxy": pygame.image.load("assets/galaxy_class1.png").convert_alpha(),
        "invincible": pygame.image.load("assets/invincible_class.png").convert_alpha(),
        "intrepid": pygame.image.load("assets/intrepid_class1.png").convert_alpha(),
        "discovery": pygame.image.load("assets/discovery_class.png").convert_alpha(),
        "klingon": pygame.image.load("assets/klingon_ship1.png").convert_alpha(),
        "romulan": pygame.image.load("assets/romulan_ship.png").convert_alpha(),
        "background": pygame.image.load("assets/space_background.png").convert(),
        "warp_drive": pygame.image.load("assets/warp_drive.png").convert_alpha(),
    }

    # Resize images
    images["constitution"] = pygame.transform.scale(images["constitution"], (80, 155))
    images["galaxy"] = pygame.transform.scale(images["galaxy"], (110, 150))
    images["invincible"] = pygame.transform.scale(images["invincible"], (100, 190))
    images["intrepid"] = pygame.transform.scale(images["intrepid"], (87, 153))
    images["discovery"] = pygame.transform.scale(images["discovery"], (95, 205))
    images["klingon"] = pygame.transform.scale(images["klingon"], (76, 90))
    images["romulan"] = pygame.transform.scale(images["romulan"], (60, 75))
    images["warp_drive"] = pygame.transform.scale(images["warp_drive"], (WIDTH, HEIGHT))
    images["background"] = pygame.transform.scale(images["background"], (WIDTH, HEIGHT))

    # Explosion images
    images["explosion"] = [pygame.image.load(f"assets/explosion_{i}.png").convert_alpha() for i in range(6)]
    images["explosion"] = [pygame.transform.scale(img, (65, 65)) for img in images["explosion"]]

    images["small_explosion"] = [pygame.image.load(f"assets/explosion_{i}.png").convert_alpha() for i in range(6)]
    images["small_explosion"] = [pygame.transform.scale(img, (30, 30)) for img in images["small_explosion"]]

    images["big_explosion"] = [pygame.image.load(f"assets/explosion_{i}.png").convert_alpha() for i in range(6)]
    images["big_explosion"] = [pygame.transform.scale(img, (120, 120)) for img in images["small_explosion"]]

    return images


class Explosion(pygame.sprite.Sprite):
    def __init__(self, center):
        super().__init__()
        self.images = images["explosion"]
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect(center=center)
        self.frame_rate = 50
        self.last_update = pygame.time.get_ticks()

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.index += 1
            if self.index >= len(self.images):
                self.kill()
            else:
                center = self.rect.center
                self.image = self.images[self.index]
                self.rect = self.image.get_rect(center=center)

class Big_Explosion(pygame.sprite.Sprite):
    def __init__(self, center):
        super().__init__()
        self.images = images["big_explosion"]
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect(center=center)
        self.frame_rate = 50
        self.last_update = pygame.time.get_ticks()

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.index += 1
            if self.index >= len(self.images):
                self.kill()
            else:
                center = self.rect.center
                self.image = self.images[self.index]
                self.rect = self.image.get_rect(center=center)

class Small_Explosion(pygame.sprite.Sprite):
    def __init__(self, center):
        super().__init__()
        self.images = images["small_explosion"]
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect(center=center)
        self.frame_rate = 50
        self.last_update = pygame.time.get_ticks()

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.index += 1
            if self.index >= len(self.images):
                self.kill()
            else:
                center = self.rect.center
                self.image = self.images[self.index]
                self.rect = self.image.get_rect(center=center)

class Starship(pygame.sprite.Sprite):
    def __init__(self, ship_class, level_multiplier):
        super().__init__()
        self.ship_class = ship_class
        if ship_class == "Constitution":
            self.image = images["constitution"]
            self.health = 100
            self.energy = 100
            self.torpedoes = 144
            self.speed = 9
            self.torpedo_power = 25
            self.phaser_power = 15
            self.shield_strength = 100
            self.travel_method = "Warp Drive"
            self.travel_image = images["warp_drive"]
            self.special_weapon = "Photonic Shockwave"
            self.special_weapon_ammo = 100
            self.homing_torpedo_ammo = 25
            self.max_health = self.health
            self.max_phasers = self.energy
            self.max_torpedos = self.torpedoes
            self.max_shields = self.shield_strength
            self.max_homing_torpedoes = self.homing_torpedo_ammo
            self.acceleration = 0.1
            self.deceleration = 0.05

        elif ship_class == "Galaxy":
            self.image = images["galaxy"]
            self.health = 150
            self.energy = 150
            self.torpedoes = 250
            self.speed = 8
            self.torpedo_power = 30 #Test Value
            self.phaser_power = 20
            self.shield_strength = 130
            self.travel_method = "Warp Drive"
            self.travel_image = images["warp_drive"]
            self.special_weapon = "Quantum Torpedoes"
            self.special_weapon_ammo = 100
            self.homing_torpedo_ammo = 40
            self.max_health = self.health
            self.max_phasers = self.energy
            self.max_torpedos = self.torpedoes
            self.max_shields = self.shield_strength
            self.max_homing_torpedoes = self.homing_torpedo_ammo
            self.acceleration = 0.07
            self.deceleration = 0.03

        elif ship_class == "Invincible":
            self.image = images["invincible"]
            self.health = 300
            self.energy = 400
            self.torpedoes = 200
            self.speed = 3
            self.torpedo_power = 39
            self.phaser_power = 29
            self.shield_strength = 500
            self.travel_method = "Warp Drive"#"Quantum Slipstream"
            self.travel_image = images["warp_drive"]#quantum_slipstream_img
            self.special_weapon = "Pulse Phaser Cannon"
            self.special_weapon_ammo = 150
            self.homing_torpedo_ammo = 100
            self.max_health = self.health
            self.max_phasers = self.energy
            self.max_torpedos = self.torpedoes
            self.max_shields = self.shield_strength
            self.max_homing_torpedoes = self.homing_torpedo_ammo
            self.acceleration = 0.02
            self.deceleration = 0.01

        elif ship_class == "Intrepid":
            self.image = images["intrepid"]
            self.health = 120
            self.energy = 130
            self.torpedoes = 96
            self.speed = 10
            self.torpedo_power = 25
            self.phaser_power = 15
            self.shield_strength = 100
            self.travel_method = "Warp Drive"#"Pathway Drive"
            self.travel_image = images["warp_drive"]#pathway_drive_img
            self.special_weapon = "Transphasic Torpedoes"
            self.special_weapon_ammo = 100
            self.homing_torpedo_ammo = 30
            self.max_health = self.health
            self.max_phasers = self.energy
            self.max_torpedos = self.torpedoes
            self.max_shields = self.shield_strength
            self.max_homing_torpedoes = self.homing_torpedo_ammo
            self.acceleration = 0.12
            self.deceleration = 0.6

        elif ship_class == "Sovereign":
            self.image = images["discovery"]
            self.health = 250
            self.energy = 300
            self.torpedoes = 150
            self.speed = 5
            self.torpedo_power = 38
            self.phaser_power = 25
            self.shield_strength = 150
            self.travel_method = "Warp Drive"#"Spore Drive"
            self.travel_image = images["warp_drive"]#spore_drive_img
            self.special_weapon = "Dark Matter Torpedoes"
            self.special_weapon_ammo = 200
            self.homing_torpedo_ammo = 50
            self.max_health = self.health
            self.max_phasers = self.energy
            self.max_torpedos = self.torpedoes
            self.max_shields = self.shield_strength
            self.max_homing_torpedoes = self.homing_torpedo_ammo
            self.acceleration = 0.08
            self.deceleration = 0.04

        self.rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT - 90))
        self.travel_cooldown = 0
        self.special_weapon_cooldown = 0

        # Acceleration Testing
        #self.velocity = pygame.Vector2(0, 0)  # Current velocity (x, y)
        #self.max_speed = self.speed	
        self.max_health = self.health
        self.max_phasers = self.energy
        self.max_torpedos = self.torpedoes
        self.max_shields = self.shield_strength
        self.max_homing_torpedoes = self.homing_torpedo_ammo

        self.homing_torpedo_cooldown = 0
          # Start with 5 homing torpedoes


        self.rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT - 50))
        self.warp_drive = 1

        # Add this dictionary to map special weapon names to classes
        self.special_weapon_classes = {
            "Photonic Shockwave": PhotonicShockwave,
            "Quantum Torpedoes": QuantumTorpedo,
            "Pulse Phaser Cannon": PulsePhaserCannon,
            "Transphasic Torpedoes": TransphasicTorpedo,
            "Dark Matter Torpedoes": DarkMatterTorpedo
        }

    def move(self, dx, dy, screen):
        self.rect.x += dx * self.speed
        self.rect.y += dy * self.speed
        self.rect.clamp_ip(screen.get_rect())

    def explode(self):
        return Big_Explosion(self.rect.center)

    def fire_phaser(self, phaser_sound):

        if self.energy >= 10:
            self.energy -= 10
            pygame.mixer.Sound.play(phaser_sound)
            return Phaser(self.rect.centerx, self.rect.top, self.phaser_power)
        return None

    def fire_torpedo(self, torpedo_sound):

        if self.torpedoes > 0:
            self.torpedoes -= 1
            pygame.mixer.Sound.play(torpedo_sound)
            return Torpedo(self.rect.centerx, self.rect.top, self.torpedo_power)
        return None

    def fire_homing_torpedo(self, target_group, all_sprites, torpedo_sound):

        if self.homing_torpedo_ammo > 0 and self.homing_torpedo_cooldown <= 0:
            self.homing_torpedo_ammo -= 1
            if self.ship_class == "Invincible":
                self.homing_torpedo_cooldown = 15  # 0.25 second cooldown (assuming 60 FPS)
                pygame.mixer.Sound.play(torpedo_sound)
            else:
                self.homing_torpedo_cooldown = 30  # 0.5 second cooldown (assuming 60 FPS)
                pygame.mixer.Sound.play(torpedo_sound)
            return HomingTorpedo(self.rect.centerx, self.rect.top, target_group, all_sprites, self.torpedo_power)
        return None

    def update(self):
        '''
        # Movement based on keyboard input
        keys = pygame.key.get_pressed()

        # Accelerate the ship based on key presses
        if keys[pygame.K_LEFT]:
            self.velocity.x -= self.acceleration
        if keys[pygame.K_RIGHT]:
            self.velocity.x += self.acceleration
        if keys[pygame.K_UP]:
            self.velocity.y -= self.acceleration
        if keys[pygame.K_DOWN]:
            self.velocity.y += self.acceleration

        # Apply deceleration when no key is pressed
        if not keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT]:
            if self.velocity.x > 0:
                self.velocity.x -= self.deceleration
            elif self.velocity.x < 0:
                self.velocity.x += self.deceleration

        if not keys[pygame.K_UP] and not keys[pygame.K_DOWN]:
            if self.velocity.y > 0:
                self.velocity.y -= self.deceleration
            elif self.velocity.y < 0:
                self.velocity.y += self.deceleration

        # Cap the ship's velocity to the max speed for smooth movement
        self.velocity.x = max(min(self.velocity.x, self.max_speed), -self.max_speed)
        self.velocity.y = max(min(self.velocity.y, self.max_speed), -self.max_speed)

        # Apply velocity to position
        self.rect.x += self.velocity.x
        self.rect.y += self.velocity.y

        # Keep player on the screen
        self.rect.left = max(self.rect.left, 0)
        self.rect.right = min(self.rect.right, WIDTH)
        self.rect.top = max(self.rect.top, 0)
        self.rect.bottom = min(self.rect.bottom, HEIGHT)

        # Update cooldowns
        if self.special_weapon_cooldown > 0:
            self.special_weapon_cooldown -= 1
        if self.homing_torpedo_cooldown > 0:
            self.homing_torpedo_cooldown -= 1
        '''

        # Movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed

        # Keep player on the screen
        self.rect.left = max(self.rect.left, 0)
        self.rect.right = min(self.rect.right, WIDTH)
        self.rect.top = max(self.rect.top, 0)
        self.rect.bottom = min(self.rect.bottom, HEIGHT)

        # Update cooldowns
        if self.special_weapon_cooldown > 0:
            self.special_weapon_cooldown -= 1
        if self.homing_torpedo_cooldown > 0:
            self.homing_torpedo_cooldown -= 1

    def fire_special_weapon(self, special_sound):

        if self.special_weapon_ammo > 0 and self.special_weapon_cooldown <= 0:
            self.special_weapon_ammo -= 1
            self.special_weapon_cooldown = 180  # 3 seconds cooldown

            weapon_class = self.special_weapon_classes.get(self.special_weapon)
            if weapon_class is None:
                print(f"Unknown special weapon: {self.special_weapon}")
                return None
           
            pygame.mixer.Sound.play(special_sound)

            if self.ship_class in ["Constitution"]:
                return weapon_class(self.rect.centerx, self.rect.top)
            elif self.ship_class in ["Invincible"]:
                projectiles = []
                angles = [-90, -75, -60, -45, -30, -15, 0, 15, 30, 45, 60, 75, 90]  # Angles for the fan shape
                for angle in angles:
                    projectile = weapon_class(self.rect.centerx, self.rect.top, angle)
                    projectiles.append(projectile)
                return projectiles
            else:
                projectiles = []
                angles = [-30, -15, 0, 15, 30]  # Angles for the fan shape
                for angle in angles:
                    projectile = weapon_class(self.rect.centerx, self.rect.top, angle)
                    projectiles.append(projectile)
                return projectiles

        return None

    def special_travel(self):
        if self.travel_cooldown <= 0:
            if self.travel_method == "Warp Drive":
                self.travel_cooldown = 300
                return self.travel_image, "Engaging Warp Drive!", 50
            elif self.travel_method == "Quantum Slipstream":
                self.travel_cooldown = 240
                return self.travel_image, "Entering Quantum Slipstream!", 75
            elif self.travel_method == "Pathway Drive":
                self.travel_cooldown = 180
                return self.travel_image, "Activating Pathway Drive!", 100
            elif self.travel_method == "Spore Drive":
                self.travel_cooldown = 120
                return self.travel_image, "Initiating Spore Drive Jump!", 150
        return None, 0

class SpecialWeapon(pygame.sprite.Sprite):
    def __init__(self, x, y, angle=0):
        super().__init__()
        self.angle = angle
        self.speed = 10
        self.damage = 30
        self.position = pygame.math.Vector2(x, y)
        self.image = self.create_image()
        self.rect = self.image.get_rect(center=(x, y))

    def create_image(self):
        # This method should be overridden by subclasses
        surface = pygame.Surface((10, 10))
        surface.fill((255, 255, 255))  # Default white square
        return surface

    def update(self):
        dx = self.speed * math.sin(math.radians(self.angle))
        dy = -self.speed * math.cos(math.radians(self.angle))
        self.position += pygame.math.Vector2(dx, dy)
        self.rect.center = round(self.position.x), round(self.position.y)
        if self.rect.bottom < 0 or self.rect.top > HEIGHT or self.rect.left > WIDTH or self.rect.right < 0:
            self.kill()

class PhotonicShockwave(SpecialWeapon):
    def create_image(self):
        surface = pygame.Surface((140, 25))
        surface.fill(BLUE)
        return pygame.transform.rotate(surface, -self.angle)

class PulsePhaserCannon(SpecialWeapon):
    def create_image(self):
        surface = pygame.Surface((15, 25))
        surface.fill(RED)
        return pygame.transform.rotate(surface, -self.angle)

class QuantumTorpedo(SpecialWeapon):
    def create_image(self):
        surface = pygame.Surface((10, 10))
        surface.fill(GREEN)
        pygame.draw.line(surface, WHITE, (5, 5), (5 + 4*math.sin(math.radians(self.angle)), 5 - 4*math.cos(math.radians(self.angle))), 2)
        return surface

class TransphasicTorpedo(SpecialWeapon):
    def create_image(self):
        surface = pygame.Surface((12, 12))
        surface.fill(PURPLE)
        pygame.draw.line(surface, WHITE, (6, 6), (6 + 5*math.sin(math.radians(self.angle)), 6 - 5*math.cos(math.radians(self.angle))), 2)
        return surface

class DarkMatterTorpedo(SpecialWeapon):
    def create_image(self):
        surface = pygame.Surface((20, 20))
        surface.fill((50, 0, 50))  # Dark purple
        pygame.draw.line(surface, WHITE, (7, 7), (7 + 6*math.sin(math.radians(self.angle)), 7 - 6*math.cos(math.radians(self.angle))), 2)
        return surface

class Starbase(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('assets/starbase.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH - self.rect.width)
        self.rect.y = -self.rect.height
        self.speed = 1

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self.kill()

class Enemy(pygame.sprite.Sprite):
    def __init__(self, enemy_type, player, level_multiplier):
        super().__init__()
        self.enemy_type = enemy_type
        self.player = player  # Store the player reference
        if enemy_type == "Klingon":
            self.image = images["klingon"]
            if player.ship_class == "Invincible":
                self.health = 100
            else:
                self.health = 75
            self.fire_rate = 120  # Fire every 2 seconds (assuming 60 FPS)
        elif enemy_type == "Romulan":
            self.image = images["romulan"]
            if player.ship_class == "Invincible":
                self.health = 90
            else:
                self.health = 60
            self.fire_rate = 180  # Fire every 3 seconds
        else:
            self.image = images["klingon"]
            self.health = 55
            self.fire_rate = 240  # Fire every 4 seconds
        self.health = self.health * level_multiplier
        self.rect = self.image.get_rect(center=(random.randint(0, WIDTH), -100))
        self.speed = random.randint(1, 3)
        self.fire_timer = random.randint(0, self.fire_rate)

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self.kill()

        self.fire_timer -= 1
        if self.fire_timer <= 0:
            self.fire_timer = self.fire_rate
            return self.fire(self.player)
        return None

    def fire(self, player):
        if random.random() < 0.7:  # 70% chance to fire phaser, 30% for torpedo
            return EnemyPhaser(self.rect.centerx, self.rect.bottom)
        else:
            return EnemyTorpedo(self.rect.centerx, self.rect.bottom)

    def explode(self, destroyed_sound):
        pygame.mixer.Sound.play(destroyed_sound)
        return Explosion(self.rect.center)

class EnemyPhaser(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((4, 20))
        self.image.fill(ORANGE)
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 3

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self.kill()

class EnemyTorpedo(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((6, 6))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 3

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self.kill()

class Phaser(pygame.sprite.Sprite):
    def __init__(self, x, y, power):
        super().__init__()
        self.image = pygame.Surface((5, 25))  # Adjust size as needed
        self.image.fill(RED)
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 20
        self.power = power

    def update(self):
        self.rect.y -= self.speed
        if self.rect.bottom < 0:
            self.kill()

    def explode(self, hit_sound):
        pygame.mixer.Sound.play(hit_sound)
        return Small_Explosion(self.rect.center)


class Torpedo(pygame.sprite.Sprite):
    def __init__(self, x, y, power):
        super().__init__()
        self.image = pygame.Surface((7, 7))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 14
        self.power = power

    def update(self):
        self.rect.y -= self.speed
        if self.rect.bottom < 0:
            self.kill()

    def explode(self, hit_sound):
        pygame.mixer.Sound.play(hit_sound)
        return Small_Explosion(self.rect.center)

class HomingTorpedo(pygame.sprite.Sprite):
    def __init__(self, x, y, target_group, all_sprites, damage):
        super().__init__()
        self.image = pygame.Surface((8, 8))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect(center=(x, y))
        self.position = pygame.math.Vector2(x, y)
        self.speed = 7
        self.target_group = target_group
        self.creation_time = time.time()
        self.lifetime = 1  # 1 second lifetime
        self.all_sprites = all_sprites
        self.damage = damage

    def update(self):
        current_time = time.time()
        if current_time - self.creation_time > self.lifetime:
            self.kill()
            return

        target = self.find_closest_target()
        if target:
            direction = pygame.math.Vector2(target.rect.center) - self.position
            if direction.length() > 0:
                direction = direction.normalize()
                self.position += direction * self.speed
        else:
            self.position.y -= self.speed  # Move straight up if no target

        self.rect.center = self.position

    def find_closest_target(self):
        closest_target = None
        min_distance = float('inf')
        for target in self.target_group:
            distance = pygame.math.Vector2(target.rect.center).distance_to(self.position)
            if distance < min_distance:
                min_distance = distance
                closest_target = target
        return closest_target

    def explode(self, hit_sound):
        pygame.mixer.Sound.play(hit_sound)
        return Small_Explosion(self.rect.center)

class SpaceAnomaly(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((45, 45))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect(center=(random.randint(0, WIDTH), -70))
        self.speed = 3

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self.kill()


def show_message(message, screen):
    font = pygame.font.Font(None, 36)
    text = font.render(message, True, WHITE)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))

    # Create a semi-transparent background
    bg_rect = text_rect.inflate(20, 20)
    bg_surface = pygame.Surface(bg_rect.size, pygame.SRCALPHA)
    bg_surface.fill((0, 0, 0, 128))  # Black with 50% opacity

    screen.blit(bg_surface, bg_rect)
    screen.blit(text, text_rect)
    pygame.display.flip()
    pygame.time.wait(2000)

ship_class_info = {
    "Constitution": {
        "Description": "Versatile and well-balanced.",
        "Special weapon": "Photonic Shockwave",
        "Travel method": "Warp Drive"
    },
    "Galaxy": {
        "Description": "Large explorer with top-of-the-line weaponry",
        "Special weapon": "Quantum Torpedoes",
        "Travel method": "Warp Drive"
    },
    "Invincible": {
        "Description": "Heavy battleship with strong defenses.",
        "Alert!": "This ship will be more challenging than the others",
        "Special weapon": "Pulse Phaser Cannon",
        "Travel method": "Warp Drive"#"Quantum Slipstream"
    },
    "Intrepid": {
        "Description": "Long-range science vessel with advanced technology.",
        "Special weapon": "Transphasic Torpedoes",
        "Travel method": "Warp Drive"#"Pathway Drive"
    },
    "Sovereign": {
        "Description": "Advanced explorer with cutting-edge weaponry.",
        "Special weapon": "Dark Matter Torpedo",
        "Travel method": "Warp Drive"#"Spore Drive"
    }
}

def choose_ship_class(screen):
    screen.fill((0, 0, 0))
    font = pygame.font.Font(None, 52)
    info_font = pygame.font.Font(None, 42)
    
    title = font.render("Choose Your Ship Class", True, (255, 255, 255))
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 50))
    
    classes = list(ship_class_info.keys())
    ship_images = {
        "Constitution": pygame.image.load("assets/constitution_class-Copy.png"),
        "Galaxy": pygame.image.load("assets/galaxy_class1-Copy.png"),
        "Invincible": pygame.image.load("assets/invincible_class-Copy.png"),
        "Intrepid": pygame.image.load("assets/intrepid_class1-Copy.png"),
        "Sovereign": pygame.image.load("assets/discovery_class-Copy.png")
    }
    ship_sizes = {
        "Constitution": (155, 80),
        "Galaxy": (150, 110),
        "Invincible": (190, 100),
        "Intrepid": (153, 87),
        "Sovereign": (205, 95)
    }
    buttons = []
    
    for i, ship_class in enumerate(classes):
        button = pygame.Rect(WIDTH // 2 - 150, 200 + i * 120, 320, 70)
        pygame.draw.rect(screen, (255, 255, 255), button, 2)
        text = font.render(ship_class, True, (255, 255, 255))
        screen.blit(text, (button.centerx - text.get_width() // 2, button.centery - text.get_height() // 2))
        
        ship_image = pygame.transform.scale(ship_images[ship_class], ship_sizes[ship_class])
        ship_x = WIDTH // 2 - 400 - ship_sizes[ship_class][0] // 2  # Adjust ship placement to the left of buttons
        ship_y = button.centery - ship_sizes[ship_class][1] // 2  # Center ship vertically with button
        screen.blit(ship_image, (ship_x, ship_y))
        
        buttons.append((button, ship_class))
    
    info_rect = pygame.Rect(50, HEIGHT - 240, WIDTH - 100, 180)
    
    htp_rect = pygame.Rect(WIDTH - 250, HEIGHT - 700, 200, 50)
    htp_text = info_font.render("How to Play", True, (255, 255, 255))
    pygame.draw.rect(screen, (255, 255, 255), htp_rect, 2)
    screen.blit(htp_text, (htp_rect.centerx - htp_text.get_width() // 2, htp_rect.centery - htp_text.get_height() // 2))
    
    pygame.display.flip()
    
    while True:
        mouse_pos = pygame.mouse.get_pos()
        hover_info = None
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for rect, ship_class in buttons:
                    if rect.collidepoint(event.pos):
                        return ship_class
                if htp_rect.collidepoint(event.pos):
                    show_how_to_play(screen)
                    return choose_ship_class(screen)
        
        for rect, ship_class in buttons:
            if rect.collidepoint(mouse_pos):
                hover_info = ship_class_info[ship_class]
                break  
        
        screen.fill((0, 0, 0))
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 50))
        
        for rect, ship_class in buttons:
            pygame.draw.rect(screen, (255, 255, 255), rect, 2)
            text = font.render(ship_class, True, (255, 255, 255))
            screen.blit(text, (rect.centerx - text.get_width() // 2, rect.centery - text.get_height() // 2))
            ship_image = pygame.transform.scale(ship_images[ship_class], ship_sizes[ship_class])
            screen.blit(ship_image, (WIDTH // 2 - 400, rect.top))  # Adjust ship placement
        
        pygame.draw.rect(screen, (255, 255, 255), htp_rect, 2)
        screen.blit(htp_text, (htp_rect.centerx - htp_text.get_width() // 2, htp_rect.centery - htp_text.get_height() // 2))
        
        if hover_info:
            pygame.draw.rect(screen, (0, 0, 0), info_rect)
            pygame.draw.rect(screen, (255, 255, 255), info_rect, 2)
            y_offset = info_rect.top + 10
            for key, value in hover_info.items():
                info_text = info_font.render(f"{key}: {value}", True, (255, 255, 255))
                screen.blit(info_text, (info_rect.left + 10, y_offset))
                y_offset += 40  
        
        pygame.display.flip()


def show_how_to_play(screen):
    screen.fill(BLACK)
    font = pygame.font.Font(None, 36)

    instructions = [
        "How to Play:",
        "1. Use arrow keys to move your ship.",
        "2. Press SPACE to fire phasers.",
        "3. Press T to fire torpedoes.",
        "4. Phasers will use energy and torpedos will use your torpedo ammo",
        "5. Press W for escaping the situation",
        "6. Traveling will get you somewhere else but has a cooldown",
        "7. Press S to fire special weapon. (Fires in a fan-shaped ray)",
        "8. Press D to fire homing torpedo.",
        "9. Press C or ESC to cancel and quit.",
        "10. Press P to reload your weapons and shields. (Will take 50% off your health)",
        "11. Starbases (grey mushroom shape) will take off 50 points but give you weapons and shields",
        "12. Anomalies (green square) will give you weapons, shields, or research points",
        "13. Some ships will be more challenging than others because of it's capabilities",
        "An example is the Invincible Class. Enemies spawn 2x faster and starbases 3x slower",
        "Press (any key) to return to the ship selection screen."
    ]

    for i, line in enumerate(instructions):
        text = font.render(line, True, WHITE)
        screen.blit(text, (50, 50 + i * 40))

    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                waiting = False


def play_again_screen(game_duration, screen):
    screen.fill(BLACK)
    font = pygame.font.Font(None, 42)

    title = font.render("Game Over", True, WHITE)
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 150))

    score_text = font.render(f"Final Score: {score}", True, WHITE)
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 250))

    # Display game duration
    minutes, seconds = divmod(int(game_duration), 60)
    duration_text = font.render(f"Game Duration: {minutes:02d} min: {seconds:02d} sec", True, WHITE)
    screen.blit(duration_text, (WIDTH // 2 - duration_text.get_width() // 2, 350))

    play_again_text = font.render("Play Again", True, WHITE)
    play_again_rect = play_again_text.get_rect(center=((WIDTH // 2) - 50, 550))
    pygame.draw.rect(screen, WHITE, play_again_rect.inflate(20, 10), 2)
    screen.blit(play_again_text, play_again_rect)

    quit_text = font.render("Quit", True, WHITE)
    quit_rect = quit_text.get_rect(center=((WIDTH // 2) + 100, 550))
    pygame.draw.rect(screen, WHITE, quit_rect.inflate(20, 10), 2)
    screen.blit(quit_text, quit_rect)

    play_again_text = font.render("Press SPACE to play again,", True, WHITE)
    screen.blit(play_again_text, (WIDTH // 2 - play_again_text.get_width() // 2, HEIGHT // 2 + 20))

    play_again_text1 = font.render("ESC to quit, or click the buttons", True, WHITE)
    screen.blit(play_again_text1, (WIDTH // 2 - play_again_text1.get_width() // 2, HEIGHT // 2 + 60))

    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return True
                elif event.key == pygame.K_ESCAPE:
                    return False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if play_again_rect.collidepoint(event.pos):
                    return True
                elif quit_rect.collidepoint(event.pos):
                    return False

    return False

def recharge_at_starbase(player):
    heal = ' '
    if player.max_health > player.health:
        health_recharge = min((player.max_health/4), player.max_health - player.health)
        heal = 'health'
        shield_recharge = min((player.max_shields/4), player.max_shields - player.shield_strength)
    else:
        health_recharge = min((player.max_health/4), player.max_health - player.health)
        shield_recharge = min((player.max_shields/4), player.max_shields - player.shield_strength)
        heal = 'shields'

    torpedo_recharge = min((player.max_torpedos/4), player.max_torpedos - player.torpedoes)

    energy_recharge = min((player.max_phasers/3), player.max_phasers - player.energy)

# Previous Debugging
    #print("Health")
    #print(health_recharge)
    #print("----------")
    #print("Shields")
    #print(shield_recharge)

# Makes sure when the player's shields, health, torpedos, and energy levels are all maxed,
# give the player homing torpedoes and torpedoes.

    if shield_recharge < 0 or health_recharge < 0:
        if heal == 'shields':
            shield_recharge = 0
        else:
            health_recharge = 0

    elif torpedo_recharge < 0:
        torpedo_recharge = 0

    elif energy_recharge < 0:
        energy_recharge = 0

    elif (shield_recharge < 0 or health_recharge < 0) and torpedo_recharge < 0:
        if heal == 'shields':
            shield_recharge = 0
        else:
            health_recharge = 0

        torpedo_recharge = 0
    elif (shield_recharge < 0 or health_recharge < 0) and energy_recharge < 0:
        if heal == 'shields':
            shield_recharge = 0
        else:
            health_recharge = 0
        energy_recharge = 0

    elif energy_recharge < 0 and torpedo_recharge < 0:
        energy_recharge = 0
        torpedo_recharge = 0

    elif energy_recharge < 0 and torpedo_recharge < 0 and (shield_recharge < 0 or health_recharge < 0):
        energy_recharge = 0
        torpedo_recharge = 0
        if heal == 'shields':
            shield_recharge = 0
        else:
            health_recharge = 0
    else:
        print("Didn't Work")

    if shield_recharge + torpedo_recharge + energy_recharge <= 0:
        player.special_weapon_ammo += 7
        player.homing_torpedo_ammo += 10
        return f"Added 7 {player.special_weapon} and 10 Homing Torpedoes"
    elif shield_recharge + torpedo_recharge + energy_recharge >= 0:
        if heal == 'health':
            player.health += health_recharge
            player.torpedoes += torpedo_recharge
            player.energy += energy_recharge
            return f"Recharged: Health +{health_recharge}%, Torpedoes +{torpedo_recharge}, Energy +{energy_recharge:.0f}"
        else:
            player.shield_strength += shield_recharge
            player.torpedoes += torpedo_recharge
            player.energy += energy_recharge
            return f"Recharged: Shields +{shield_recharge}%, Torpedoes +{torpedo_recharge}, Energy +{energy_recharge:.0f}"

# Modify the draw_lvl_button function
def draw_lvl_button(text, x, y, width, height, color, hover_color, screen, font):
    # Makes Buttons for the Level selector
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    button_rect = pygame.Rect(x, y, width, height)
    
    # Check if the mouse is hovering over the button
    if button_rect.collidepoint(mouse):
        pygame.draw.rect(screen, hover_color, button_rect)  # Highlight on hover
        if click[0]:  # Left click
            return True  # Return True if the button is clicked
        return 'hover'  # Return 'hover' if it's being hovered over
    else:
        pygame.draw.rect(screen, color, button_rect)  # Normal button state
    text_surf = font.render(text, True, WHITE)
    text_rect = text_surf.get_rect(center=(x + width // 2, y + height // 2))
    screen.blit(text_surf, text_rect)  # Draw text on the button
    return False  # Return False if it's neither hovered nor clicked

level_info = {
    1.0: {
        "Description": "A beginner level to get started with the game.",
        "Difficulty": "Easy",
        "Objective": "Get the highest score and the longest time without exploding. Good luck!"
    },
    1.5: {
        "Description": "A medium level with more realistic physics and more enemies.",
        "Difficulty": "Medium",
        "Objective": "Get the highest score and the longest time without exploding. Good luck!"
    },
    2.0: {
        "Description": "A hard level with realistic physics and even more enemies.",
        "Difficulty": "Hard",
        "Objective": "Get the highest score and the longest time without exploding. Good luck!"
    }
}

# Define the level selection function
def select_level(screen, font):
    info_font = pygame.font.Font(None, 32)
    info_rect = pygame.Rect(50, HEIGHT - 240, WIDTH - 100, 180)  # Info box location
    while True:
        screen.fill(BLACK)  # Fill the screen with a black background
        
        # Draw level buttons
        level_1 = draw_lvl_button("Level 1", (WIDTH // 2) - 100, 200, 200, 60, BLUE, LIGHT_BLUE, screen, font)
        level_2 = draw_lvl_button("Level 2", (WIDTH // 2) - 100, 300, 200, 60, BLUE, LIGHT_BLUE, screen, font)
        level_3 = draw_lvl_button("Level 3", (WIDTH // 2) - 100, 400, 200, 60, BLUE, LIGHT_BLUE, screen, font)
        
        # Show level info when hovering over a level button
        hover_info = None
        if level_1 == 'hover':  # Check for hover
            hover_info = level_info[1.0]
        elif level_2 == 'hover':  # Check for hover
            hover_info = level_info[1.5]
        elif level_3 == 'hover':  # Check for hover
            hover_info = level_info[2.0]

        # Display information if hovering over a level
        if hover_info:
            pygame.draw.rect(screen, (0, 0, 0), info_rect)  # Info box background
            pygame.draw.rect(screen, (255, 255, 255), info_rect, 2)  # Info box border
            y_offset = info_rect.top + 10
            for key, value in hover_info.items():
                info_text = info_font.render(f"{key}: {value}", True, (255, 255, 255))
                screen.blit(info_text, (info_rect.left + 10, y_offset))
                y_offset += 40

        # Update the screen with the current state
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return None
        
        # Check for button clicks (only return if a button is clicked)
        if level_1 == True:
            return 1.0
        if level_2 == True:
            return 1.5
        if level_3 == True:
            return 2.0

async def main():
    
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Star Trek Game")


    phaser_sound = pygame.mixer.Sound("sounds/phaser.wav")
    torpedo_sound = pygame.mixer.Sound("sounds/torpedo.wav")
    destroyed_sound = pygame.mixer.Sound("sounds/destroyed.wav")
    hit_sound = pygame.mixer.Sound("sounds/hit.wav")
    warp_sound = pygame.mixer.Sound("sounds/warp.wav")
    special_sound = pygame.mixer.Sound("sounds/special.wav")
    
    global images  # Make the images accessible globally
    images = load_images()  # Load images into a global dictionary
    
    global score  # Make score a global variable so it can be accessed in play_again_screen

    # Define the font here
    font = pygame.font.Font(None, 42)  # You can adjust the size (36) as needed

    playing = True
    while playing:
        score = 0  # Reset score for each new game
        ship_class = choose_ship_class(screen)
        if ship_class is None:
            return

        level_multiplier = select_level(screen, font)
        if level_multiplier is None:
            return

        clock = pygame.time.Clock()
        player = Starship(ship_class, level_multiplier)
        all_sprites = pygame.sprite.Group(player)
        enemies = pygame.sprite.Group()
        phasers = pygame.sprite.Group()
        torpedoes = pygame.sprite.Group()
        special_weapons = pygame.sprite.Group()
        anomalies = pygame.sprite.Group()
        explosions = pygame.sprite.Group()
        enemy_projectiles = pygame.sprite.Group()
        starbases = pygame.sprite.Group()
        homing_torpedoes = pygame.sprite.Group()

        enemy_spawn_timer = 0
        anomaly_spawn_timer = 0
        research_progress = 0

        travel_effect = None
        travel_effect_timer = 0

        starbase_spawn_timer = 0

        original_health = player.max_health
        original_phaser = player.max_phasers
        original_torpedos = player.max_torpedos
        original_shields = player.shield_strength
        original_h_torpedoes = player.max_homing_torpedoes

        start_time = time.time()

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_d:
                        homing_torpedo = player.fire_homing_torpedo(enemies, all_sprites, torpedo_sound)
                        if homing_torpedo:
                            homing_torpedoes.add(homing_torpedo)
                            all_sprites.add(homing_torpedo)

                    elif event.key == pygame.K_SPACE:
                        starbase_collision = pygame.sprite.spritecollide(player, starbases, False)
                        if starbase_collision:
                            starbase = starbase_collision[0]
                            recharge_result = recharge_at_starbase(player)
                            show_message(recharge_result, screen)
                            starbase.kill()
                        else:
                            # Normal firing logic
                            phaser = player.fire_phaser(phaser_sound)
                            if phaser:
                                phasers.add(phaser)
                                all_sprites.add(phaser)
                    elif event.key == pygame.K_t:
                        torpedo = player.fire_torpedo(torpedo_sound)
                        if torpedo:
                            torpedoes.add(torpedo)
                            all_sprites.add(torpedo)
                    elif event.key == pygame.K_w:
                        travel_image, message, bonus = player.special_travel()
                        if message:
                            show_message(message, screen)
                            score += bonus

                            saved_health = player.health
                            saved_shields = player.health
                            saved_energy = player.health
                            saved_torpedoes = player.health
                            saved_special_weapon_ammo = player.health
                            saved_health = player.health

                            enemies.empty()
                            anomalies.empty()
                            enemy_projectiles.empty()
                            explosions.empty()
                            starbases.empty()
                            phasers.empty()
                            torpedoes.empty()
                            special_weapons.empty()
                            homing_torpedoes.empty()

                            all_sprites.empty()
                            screen.fill(BLACK)
                            pygame.display.update()

                            player.rect.center = (WIDTH // 2, HEIGHT - 100)  # Center-bottom position
                            all_sprites.add(player)

                            enemy_spawn_timer = -240
                            anomaly_spawn_timer = -240
                            starbase_spawn_timer = -240

                            travel_effect = travel_image

                            pygame.mixer.stop()
                            pygame.mixer.Sound.play(warp_sound) # Sound plays for 3 seconds while traveling

                            travel_effect_timer = 180  # Display for 3 seconds (180 frames)

                    elif event.key == pygame.K_s:
                        special_weapon = player.fire_special_weapon(special_sound)
                        if special_weapon:
                            if isinstance(special_weapon, list):
                                for projectile in special_weapon:
                                    special_weapons.add(projectile)
                                    all_sprites.add(projectile)
                            else:
                                special_weapons.add(special_weapon)
                                all_sprites.add(special_weapon)
                    elif event.key == pygame.K_c:
                        running = False
                        pygame.QUIT
                    elif event.key == pygame.K_p:
                        show_message("Reloading!", screen)
                        player.energy += original_phaser
                        player.torpedoes += original_torpedos
                        player.homing_torpedo_ammo += original_h_torpedoes * 2
                        player.health -= original_health / 2
            # Player movement
            keys = pygame.key.get_pressed()
            player.move(
                keys[pygame.K_RIGHT] - keys[pygame.K_LEFT],
                keys[pygame.K_DOWN] - keys[pygame.K_UP], screen
            )

            # Update timers
            starbase_spawn_timer += 1
            enemy_spawn_timer += 1
            anomaly_spawn_timer += 1

            # Adjust spawn based on level

            starbase_interval = int((3600 if player.ship_class == "Invincible" else 600) / level_multiplier)
            enemy_interval = int((30 if player.ship_class == "Invincible" else 60) / level_multiplier)
            
            # Spawn Starbases
            if starbase_spawn_timer >= starbase_interval:
                starbases.add(Starbase())
                all_sprites.add(starbases)
                starbase_spawn_timer = 0
            
            # Spawn Enemies
            if enemy_spawn_timer >= enemy_interval:
                enemy_type = random.choices(["Klingon", "Romulan", "Generic"], weights=[0.5, 0.3, 0.2])[0]
                enemies.add(Enemy(enemy_type, player, level_multiplier))
                all_sprites.add(enemies)
                enemy_spawn_timer = 0

            # Spawn Anomalies
            if anomaly_spawn_timer >= 300:
                anomalies.add(SpaceAnomaly())
                all_sprites.add(anomalies)
                anomaly_spawn_timer = 0

            # Update
            for sprite in all_sprites:
                try:
                    sprite.update()
                except Exception as e:
                    print(f"Error updating sprite of type {type(sprite).__name__}: {str(e)}")
                    # Optionally, remove the problematic sprite
                    # all_sprites.remove(sprite)
            explosions.update()
            homing_torpedoes.update()
            starbases.update()

            # Collision detection
            starbase_collision = pygame.sprite.spritecollide(player, starbases, False)
            if starbase_collision:
                starbase = starbase_collision[0]
                recharge_result = recharge_at_starbase(player)
                show_message(recharge_result, screen)
                score -= (50 * level_multiplier)
                starbase.kill()

            hits = pygame.sprite.spritecollide(player, enemy_projectiles, True)
            for hit in hits:
                if isinstance(hit, EnemyPhaser):
                    pygame.mixer.Sound.play(hit_sound)
                    damage = level_multiplier * 5
                else:  # EnemyTorpedo
                    pygame.mixer.Sound.play(hit_sound)
                    damage = level_multiplier * 10

                if player.shield_strength > 0:
                    player.shield_strength = max(0, player.shield_strength - (level_multiplier * damage))
                else:
                    player.health -= level_multiplier * damage

                explosion = Small_Explosion(hit.rect.center)
                explosions.add(explosion)
                all_sprites.add(explosion)

            for torpedo in homing_torpedoes:
                hits = pygame.sprite.spritecollide(torpedo, enemies, False)
                for enemy in hits:
                    enemy.health -= torpedo.damage
                    explosion = torpedo.explode(hit_sound)
                    explosions.add(explosion)
                    all_sprites.add(explosion)
                    if enemy.health <= 0:
                        explosion = enemy.explode(destroyed_sound)
                        explosions.add(explosion)
                        all_sprites.add(explosion)
                        enemy.kill()
                        if player.ship_class == "Invincible":
                            score += 10 if enemy.enemy_type == "Generic" else 20
                        else:
                            score += 30 if enemy.enemy_type == "Generic" else 60
                    torpedo.kill()
                    break  # Exit the loop after hitting one enemy
            homing_torpedoes.update()

            for enemy in enemies:

                projectile = enemy.update()
                if isinstance(projectile, EnemyTorpedo):
                    projectile = enemy.fire(player)  # Pass the player object
                if projectile:
                    enemy_projectiles.add(projectile)
                    all_sprites.add(projectile)

                phaser_hits = pygame.sprite.spritecollide(enemy, phasers, True)
                for phaser in phaser_hits:
                    enemy.health -= phaser.power
                    if enemy.health <= 0:
                        explosion = enemy.explode(destroyed_sound)
                        explosions.add(explosion)
                        all_sprites.add(explosion)
                        enemy.kill()
                        if player.ship_class == "Invincible":
                            score += 10 if enemy.enemy_type == "Generic" else 15
                        else:
                            score += 30 if enemy.enemy_type == "Generic" else 60
                    explosion = phaser.explode(hit_sound)
                    explosions.add(explosion)
                    all_sprites.add(explosion)

                torpedo_hits = pygame.sprite.spritecollide(enemy, torpedoes, True)
                for torpedo in torpedo_hits:
                    enemy.health -= torpedo.power
                    if enemy.health <= 0:
                        explosion = enemy.explode(destroyed_sound)
                        explosions.add(explosion)
                        all_sprites.add(explosion)
                        enemy.kill()
                        if player.ship_class == "Invincible":
                            score += 5 if enemy.enemy_type == "Generic" else 10
                        else:
                            score += 20 if enemy.enemy_type == "Generic" else 40
                    explosion = torpedo.explode(hit_sound)
                    explosions.add(explosion)
                    all_sprites.add(explosion)

                special_weapon_hits = pygame.sprite.spritecollide(
                    enemy, special_weapons, False
                )
                for weapon in special_weapon_hits:
                    enemy.health -= weapon.damage
                    if enemy.health <= 0:
                        explosion = enemy.explode(destroyed_sound)
                        explosions.add(explosion)
                        all_sprites.add(explosion)
                        enemy.kill()
                        if player.ship_class == "Invincible":
                            score += 5 if enemy.enemy_type == "Generic" else 10
                        else:
                            score += 15 if enemy.enemy_type == "Generic" else 30
                if pygame.sprite.collide_rect(enemy, player):
                    if player.shield_strength > 0:
                        player.shield_strength = max(0, player.shield_strength - (10*level_multiplier))  # Prevents negative shields
                    else:
                        player.health -= level_multiplier * 20
                    explosion = enemy.explode(destroyed_sound)
                    explosions.add(explosion)
                    all_sprites.add(explosion)
                    enemy.kill()
            for anomaly in anomalies:
                if pygame.sprite.collide_rect(anomaly, player):
                    effect = random.choice(
                        ["health", "energy", "research", "torpedoes"]
                    )
                    if effect == "health":
                        if player.health < player.max_health:
                            heal_amount = min(20, player.max_health - player.health)
                            player.health += heal_amount
                            show_message(f"Health Restored: +{heal_amount}!", screen)
                        else:
                            show_message("Recharging Shields!", screen)
                            player.shield_strength += 20
                    elif effect == "energy":
                        energy_gain = 30
                        player.energy = min(
                            player.energy + energy_gain,
                            player.max_phasers,
                        )
                        show_message(f"Energy Recharged: +{energy_gain}!", screen)
                    elif effect == "research":
                        research_progress += 10
                        show_message("Research Data Collected: +10%!", screen)
                    elif effect == "torpedoes":
                        torpedo_gain = random.randint(3, 10)
                        player.homing_torpedo_ammo += torpedo_gain
                        player.torpedoes += torpedo_gain
                        show_message(f"Torpedoes and Homing Torpedoes Acquired: +{torpedo_gain}!",screen)
                    anomaly.kill()
            # Research progress
            if research_progress >= 100:
                research_progress = 0
                upgrade = random.choice(
                    ["shields", "phasers", "travel", "torpedoes", "special_weapon"]
                )
                if upgrade == "shields":
                    player.shield_strength += 25
                    show_message("Shields Upgraded: +25 strength!", screen)
                elif upgrade == "torpedoes":
                    player.torpedo_power += 5
                    show_message("Torpedo Power Upgraded: +5!", screen)
                elif upgrade == "phasers":
                    player.phaser_power += 5
                    show_message("Phasers Upgraded: +5 power!", screen)
                elif upgrade == "travel":
                    player.travel_cooldown = max(0, player.travel_cooldown - 60)
                    show_message(f"{player.travel_method} Efficiency Improved!", screen)
           
            # Cooldowns
            if player.travel_cooldown > 0:
                player.travel_cooldown -= 1
            if player.special_weapon_cooldown > 0:
                player.special_weapon_cooldown -= 1
            # Draw
            screen.blit(images["background"], (0, 0))
            all_sprites.draw(screen)
            explosions.draw(screen)
            homing_torpedoes.draw(screen)
            all_sprites.draw(screen)

            # Display travel effect if active
            if travel_effect and travel_effect_timer > 0:
                effect_rect = travel_effect.get_rect(center=(WIDTH // 2, HEIGHT // 2))
                screen.blit(travel_effect, effect_rect)
                travel_effect_timer -= 1
                if travel_effect_timer <= 0:
                    travel_effect = None

            # HUD (adjusted positions for larger screen)
            health_text = font.render(
                f"Health: {player.health}/{player.max_health}", True, WHITE
            )
            energy_text = font.render(f"Energy: {player.energy:.0f}", True, WHITE)
            torpedoes_text = font.render(f"Torpedoes: {player.torpedoes}", True, WHITE)
            score_text = font.render(f"Score: {score}", True, WHITE)
            shield_text = font.render(f"Shields: {player.shield_strength}", True, WHITE)
            research_text = font.render(f"Research: {research_progress}%", True, WHITE)
            travel_text = font.render(
                f"{player.travel_method}: {'Ready' if player.travel_cooldown <= 0 else 'Cooling'}",
                True,
                YELLOW,
            )
            class_text = font.render(f"Ship: {player.ship_class} Class", True, YELLOW)
            special_weapon_text = font.render(
                f"{player.special_weapon}: {player.special_weapon_ammo}", True, YELLOW
            )
            homing_torpedo_text = font.render(f"Homing Torpedoes: {player.homing_torpedo_ammo}", True, YELLOW)

            screen.blit(homing_torpedo_text, (10, 330))
            screen.blit(health_text, (10, 10))
            screen.blit(energy_text, (10, 50))
            screen.blit(torpedoes_text, (10, 90))
            screen.blit(shield_text, (10, 130))
            screen.blit(research_text, (10, 170))
            screen.blit(travel_text, (10, 210))
            screen.blit(class_text, (10, 250))
            screen.blit(special_weapon_text, (10, 290))
            screen.blit(score_text, (WIDTH - 200, 10))

            pygame.display.flip()
            clock.tick(60)
            await asyncio.sleep(0)

            # Game over condition
            if player.health <= 0:
                explosion = player.explode()
                explosions.add(explosion)
                all_sprites.add(explosion)
                show_message("Game Over!", screen)

                # Wait for explosion animation to finish
                while explosions:
                    explosions.update()
                    screen.blit(images["background"], (0, 0))
                    all_sprites.draw(screen)
                    explosions.draw(screen)
                    pygame.display.flip()
                    await asyncio.sleep(0)
                    clock.tick(30)
                running = False

        end_time = time.time()  # Record the end time of the game
        game_duration = end_time - start_time  # Calculate the game duration

        # After the game ends, show the play again screen with the game duration
        pygame.display.flip()
        playing = play_again_screen(game_duration, screen)
    pygame.quit()


if __name__ == "__main__":
    asyncio.run(main())
