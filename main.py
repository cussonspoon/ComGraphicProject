import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

# --- IMPORTS ---
from logic.game_manager import GameManager
from logic.input import InputHandler
from logic.level import Level
from ui.interface import Interface

def main():
    # 1. INIT
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    
    pygame.mouse.set_visible(False)
    pygame.event.set_grab(True)
    
    # 2. SETUP MANAGERS
    level = Level()
    game_manager = GameManager()
    input_handler = InputHandler()
    ui = Interface()
    
    clock = pygame.time.Clock()
    running = True

    # 3. GAME LOOP
    while running:
        # --- A. INPUT ---
        running = input_handler.process_input(level, game_manager)

        # --- B. LOGIC ---
        if not game_manager.is_game_over:
            game_manager.update(
                level.ship, 
                level.asteroids, 
                level.bullets, 
                level.powerups, 
                level.missiles
            )

        # --- C. DRAWING ---
        # 1. CLEAR EVERYTHING (Removed the glClearColor here so the Sun can control it!)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        # 2. FORCE 3D PROJECTION
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, (display[0]/display[1]), 0.1, 500.0)
        
        # 3. FORCE 3D MODELVIEW
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        
        # 4. FORCE CORE 3D STATES
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_LIGHTING)
        
        # 5. FPS Camera (Locked to Ship)
        gluLookAt(level.ship.x, level.ship.y, 0.0,  
                  level.ship.x, level.ship.y, -100.0,
                  0, 1, 0)
        
        # 6. Draw 3D World
        level.draw()
            
        # 7. Draw 2D UI
        ui.draw(display, 
                game_manager.score, 
                game_manager.lives, 
                level.ship.skill_timer, 
                level.ship.skill_cooldown_max,
                clock.get_fps(),
                level.sun.intensity)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()