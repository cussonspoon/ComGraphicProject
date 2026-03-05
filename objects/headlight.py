from OpenGL.GL import *

class Headlight:
    def __init__(self):
        self.id = GL_LIGHT2 
        
        self.ambient = [0.0, 0.0, 0.0, 1.0]
        # Pump the brightness back up so the tiny dot is intensely bright
        self.diffuse = [2.0, 2.0, 2.0, 1.0] 
        self.specular = [2.0, 2.0, 2.0, 1.0]
        
    def setup(self):
        pass
        
    def draw(self, ship_x, ship_y, ship_z, sun_intensity):
        if sun_intensity < 0.2:
            glEnable(self.id)
            
            # Position exactly at the nose of the ship
            light_pos = [ship_x, ship_y - 1.5, -4.0, 1.0]
            glLightfv(self.id, GL_POSITION, (GLfloat * 4)(*light_pos))
            
            # Pointing straight forward (perfectly aligned with the crosshair)
            spot_direction = [0.0, 0.0, -1.0] 
            glLightfv(self.id, GL_SPOT_DIRECTION, (GLfloat * 3)(*spot_direction))
            
            # 1. THE CONE: A razor-thin 2.0 degrees (super narrow)
            glLightf(self.id, GL_SPOT_CUTOFF, 2.0) 
            
            # 2. THE FOCUS: Absolute maximum center intensity (128.0 is the OpenGL limit)
            glLightf(self.id, GL_SPOT_EXPONENT, 128.0) 
            
            # 3. THE FALLOFF: Lowered the decay slightly so this ultra-thin beam 
            # actually has the range to reach the asteroids in front of you
            glLightf(self.id, GL_CONSTANT_ATTENUATION, 1.0)
            glLightf(self.id, GL_LINEAR_ATTENUATION, 0.01)   
            glLightf(self.id, GL_QUADRATIC_ATTENUATION, 0.0) 
            
            # Apply the colors
            glLightfv(self.id, GL_AMBIENT, (GLfloat * 4)(*self.ambient))
            glLightfv(self.id, GL_DIFFUSE, (GLfloat * 4)(*self.diffuse))
            glLightfv(self.id, GL_SPECULAR, (GLfloat * 4)(*self.specular))
        else:
            glDisable(self.id)