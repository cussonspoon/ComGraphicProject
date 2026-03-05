import math
from OpenGL.GL import *
from logic.obj_loader import OBJ

class Moon:
    def __init__(self, sun):
        self.sun = sun
        # Use an icosahedron for the moon (very low poly sphere)
        self.model = OBJ("assets/moon.obj", flat_normals=True)
        self.vis_x = 0.0
        self.vis_y = 0.0
        self.vis_z = -60.0
        self.intensity = 0.0
        # Light 1 for the moon
        self.id = GL_LIGHT1
        self.position = [0.0, 0.0, 0.0, 0.0]

    def setup(self):
        glEnable(GL_LIGHTING)
        glEnable(self.id)
        
    def update(self):
        # Moon orbits opposite to the sun
        moon_time = self.sun.time_factor + math.pi
        
        self.vis_x = 30.0 * math.cos(moon_time)
        self.vis_y = 20.0 * math.sin(moon_time)
        
        self.position = [self.vis_x, self.vis_y, 50.0, 0.0]
        
        if self.vis_y > -10.0:
            # When moon is up, light intensity scales
            self.intensity = max(0.0, min(1.0, (self.vis_y + 10.0) / 20.0))
            moon_light = self.intensity * 0.05 # Very dim
            self.ambient = [moon_light * 0.2, moon_light * 0.3, moon_light * 0.5, 1.0]
            # No diffuse or specular light during the night, so asteroid colors stay hidden
            self.diffuse = [0.0, 0.0, 0.0, 1.0]
            self.specular = [0.0, 0.0, 0.0, 1.0]
        else:
            self.intensity = 0.0
            self.ambient = [0.0, 0.0, 0.0, 1.0]
            self.diffuse = [0.0, 0.0, 0.0, 1.0]
            self.specular = [0.0, 0.0, 0.0, 1.0]
            
    def draw(self):
        # Light setup
        glLightfv(self.id, GL_POSITION, (GLfloat * 4)(*self.position))
        glLightfv(self.id, GL_AMBIENT, (GLfloat * 4)(*self.ambient))
        glLightfv(self.id, GL_DIFFUSE, (GLfloat * 4)(*self.diffuse))
        glLightfv(self.id, GL_SPECULAR, (GLfloat * 4)(*self.specular))

        if self.intensity > 0.05:
            glPushMatrix()
            glTranslatef(self.vis_x, self.vis_y, self.vis_z)
            glScalef(2.0, 2.0, 2.0)
            
            # Rotate it dynamically slightly, or keep the D shape facing nice
            glRotatef(self.sun.time_factor * 20.0, 0, 0, 1)
            glRotatef(-30, 0, 1, 0)
            
            # Simple gray moon texture without lighting so it glows softly
            glDisable(GL_LIGHTING)
            glEnable(GL_BLEND)
            glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
            
            # Fade moon in based on intensity
            # It should be light gray/blue
            glColor4f(0.8, 0.8, 0.9, self.intensity)
            
            self.model.draw()
            
            glDisable(GL_BLEND)
            glEnable(GL_LIGHTING)
            glPopMatrix()
