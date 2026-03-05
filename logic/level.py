import random
from objects.spaceship import SpaceShip
from objects.scenery import Star
from objects.asteroid import Asteroid
from objects.bullet import Bullet
from objects.powerup import PowerUp
from objects.missiles import Missile
from objects.sun import Sun # <--- NEW IMPORT
from objects.moon import Moon # <--- NEW IMPORT
from objects.headlight import Headlight

class Level:
    def __init__(self):
        self.ship = SpaceShip()
        self.bullets = []
        self.asteroids = []
        self.stars = []
        self.powerups = []
        self.missiles = []
        
        # --- NEW: Initialize and setup the Sun and Moon ---
        self.sun = Sun()
        self.sun.setup()
        self.moon = Moon(self.sun)
        self.moon.setup()
        self.headlight = Headlight()
        self.headlight.setup()
        # -----------------------------------------
        
        self.spawn_objects()

    def spawn_objects(self):
        # 1. Asteroids
        for i in range(5):
            start_pos = -50.0 - (i * 60.0)
            self.asteroids.append(Asteroid(start_z=start_pos))
        # 2. Stars
        for i in range(50):
            self.stars.append(Star())
        # 3. PowerUps
        self.powerups.append(PowerUp())

    def spawn_bullet(self):
        color = self.ship.get_current_color()
        self.bullets.append(Bullet(self.ship.x, self.ship.y - 0.5, -2.3, color))

    def activate_skill(self):
        if self.ship.skill_timer > 0: return 
        self.ship.skill_timer = self.ship.skill_cooldown_max
        colors = [(1,0,0,1), (0,1,0,1), (0,0,1,1), (1,1,0,1), (0,1,1,1)]
        targets = []
        for a in self.asteroids:
            dist = (a.x - self.ship.x)**2 + (a.y - self.ship.y)**2 + (a.z - self.ship.z)**2
            targets.append((dist, a))
        targets.sort(key=lambda x: x[0])
        sorted_asteroids = [t[1] for t in targets]
        for i in range(5):
            target = None
            if len(sorted_asteroids) > 0: target = sorted_asteroids[i % len(sorted_asteroids)]
            self.missiles.append(Missile(self.ship.x, self.ship.y, self.ship.z, target, colors[i]))

    def update(self, mouse_dx, mouse_dy):
        # --- NEW: Update the Day/Night cycle ---
        self.sun.update()
        self.moon.update()
        # ---------------------------------------
        
        self.ship.update(mouse_dx, mouse_dy)
        
        for a in self.asteroids: a.update()
        for s in self.stars: s.update()
        for p in self.powerups: p.update()
        for m in self.missiles: m.update()
        self.missiles = [m for m in self.missiles if m.alive]
        
        # --- BULLET LOGIC ---
        for b in self.bullets:
            b.update()
            if not b.alive: continue

            # 2. Check Collision with ASTEROIDS
            for a in self.asteroids:
                hit = ((b.x - a.x)**2 + (b.y - a.y)**2 + (b.z - a.z)**2)**0.5 < (b.radius + 2.0)
                
                if hit:
                    b.alive = False 
                    is_rainbow = (len(b.color) > 3 and b.color[3] == 1)
                    if is_rainbow or b.color[:3] == a.color[:3]:
                        a.reset() 
                    else:
                        print("WRONG COLOR")
                    break

        self.bullets = [b for b in self.bullets if b.alive]

    def draw(self):
        # --- NEW: Apply the lighting to the scene first! ---
        self.sun.draw()
        self.moon.draw()
        self.headlight.draw(self.ship.x, self.ship.y, self.ship.z, self.sun.intensity)
        # ---------------------------------------------------
        
        for s in self.stars: s.draw()
        for a in self.asteroids: a.draw(is_invincible=False)
        for p in self.powerups: p.draw()
        for m in self.missiles: m.draw()
        for b in self.bullets: b.draw()
        self.ship.draw()