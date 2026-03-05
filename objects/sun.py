import math
from OpenGL.GL import *
from OpenGL.GLU import *

class Sun:
    def __init__(self):
        self.id = GL_LIGHT0
        # We will update this dynamically now
        self.position = [0.0, 0.0, 0.0, 0.0] 
        self.ambient = [0.2, 0.2, 0.2, 1.0]
        self.specular = [1.0, 1.0, 1.0, 1.0] 
        
        self.time_factor = 0.78 
        self.cycle_speed = 0.005
        
        # Variables for the visual sphere
        self.vis_x = 0.0
        self.vis_y = 0.0
        self.vis_z = -60.0 # Deep in the background so the camera can see it!

    def setup(self):
        glEnable(GL_LIGHTING)
        glEnable(self.id)
        glShadeModel(GL_SMOOTH)
        glEnable(GL_NORMALIZE) 
        glLightModelf(GL_LIGHT_MODEL_LOCAL_VIEWER, GL_TRUE)
        glLightModelf(GL_LIGHT_MODEL_TWO_SIDE, GL_TRUE) 
        glDisable(GL_COLOR_MATERIAL)

    def update(self):
        self.time_factor += self.cycle_speed
        
        # 1. VISUAL POSITION (The glowing ball in the sky)
        # Wide orbit so it sweeps across the background
        self.vis_x = 30.0 * math.cos(self.time_factor)  
        self.vis_y = 20.0 * math.sin(self.time_factor) 
        
        # 2. LIGHT POSITION (The physics)
        # We use the same X and Y, but put Z way behind the camera (50.0). 
        # w=0.0 makes it a Directional Light (parallel rays).
        # This makes the light hit the FRONT of the ship, matching the sun's visual angle!
        self.position = [self.vis_x, self.vis_y, 50.0, 0.0] 
        
        if self.vis_y > -10.0:
            self.intensity = max(0.0, min(1.0, (self.vis_y + 10.0) / 20.0))
            self.diffuse = [self.intensity, self.intensity, self.intensity, 1.0]
            self.specular = [self.intensity, self.intensity, self.intensity, 1.0]
        else:
            self.intensity = 0.05
            self.diffuse = [0.0, 0.0, 0.0, 1.0]
            self.specular = [0.0, 0.0, 0.0, 1.0]
        
        ambient_level = max(0.2, self.intensity * 0.3) 
        self.ambient = [ambient_level, ambient_level, ambient_level, 1.0]
        
        sky_r = 0.4 * self.intensity
        sky_g = 0.6 * self.intensity
        sky_b = 0.2 + (0.8 * self.intensity) 
        glClearColor(sky_r, sky_g, sky_b, 1.0)

    def draw(self):
        # Update OpenGL Light Physics
        glLightfv(self.id, GL_POSITION, (GLfloat * 4)(*self.position))
        glLightfv(self.id, GL_AMBIENT, (GLfloat * 4)(*self.ambient))
        glLightfv(self.id, GL_DIFFUSE, (GLfloat * 4)(*self.diffuse))
        glLightfv(self.id, GL_SPECULAR, (GLfloat * 4)(*self.specular))
        
        glPushMatrix()
        
        # Move to the VISUAL position to draw the actual sphere
        glTranslatef(self.vis_x, self.vis_y, self.vis_z)
        
        glDisable(GL_LIGHTING)
        
        # Only draw the sun if it has some intensity (i.e., not completely night)
        if self.intensity > 0.05:
            glEnable(GL_BLEND)
            glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
            glDepthMask(GL_FALSE) # Don't write to depth buffer for the sun so it blends well
            
            # The sun's color intensity goes up to 1.0, but we also use it for alpha to fade it out
            # As self.intensity drops from 1.0 down to 0.05, the sun sphere becomes transparent
            color_intensity = max(0.2, self.intensity)
            
            # Use intensity for alpha to fade out
            glColor4f(1.0, 0.9 * color_intensity, 0.5 * color_intensity, self.intensity)
            
            quadric = gluNewQuadric()
            # Scale up the sphere so it looks good from far away
            gluSphere(quadric, 3.0, 16, 16) 
            gluDeleteQuadric(quadric)
            
            glDepthMask(GL_TRUE)
            glDisable(GL_BLEND)
        
        glEnable(GL_LIGHTING)
        glPopMatrix()