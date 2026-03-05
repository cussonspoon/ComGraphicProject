from OpenGL.GL import *
from logic.obj_loader import OBJ 

class SpaceShip:
    def __init__(self):
        # Your custom models are back!
        self.hull_model = OBJ("assets/ship.obj", flat_normals=True)
        self.glass_model = OBJ("assets/glass.obj", flat_normals=True)
        self.led_model = OBJ("assets/leds.obj", flat_normals=True) 
        
        self.x = 0.0
        self.y = 0.0
        self.z = -5.0 
        self.bank_angle = 0.0
        self.sensitivity = 0.01
        
        self.red_on = False
        self.green_on = False
        self.blue_on = False

        self.skill_cooldown_max = 600  
        self.skill_timer = 0

    def get_current_color(self):
        r = 1.0 if self.red_on else 0.0
        g = 1.0 if self.green_on else 0.0
        b = 1.0 if self.blue_on else 0.0
        
        if r == 0 and g == 0 and b == 0:
            return (1.0, 1.0, 1.0, 0)
            
        return (r, g, b, 0)

    def update(self, mouse_dx, mouse_dy):
        self.x += mouse_dx * self.sensitivity
        self.y -= mouse_dy * self.sensitivity
        self.x = max(-10.0, min(10.0, self.x))
        self.y = max(-6.0, min(6.0, self.y))
        self.bank_angle = self.x / 4.0 
        if self.skill_timer > 0:
            self.skill_timer -= 1

    def draw(self):
        glPushMatrix()
        
        glTranslatef(self.x, self.y - 1.5, -4.0) 
        glRotatef(-self.bank_angle * 30.0, 0, 0, 1)
        glScalef(0.4, 0.4, 0.4) 

        # Enable Color Material for fail-safe diffuse rendering on the .obj files
        glEnable(GL_COLOR_MATERIAL)
        glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)

        # ==========================================
        # 1. THE HULL (Highly Reflective Chrome)
        # ==========================================
        glColor3f(0.8, 0.8, 0.8) 
        specular_array = (GLfloat * 4)(1.0, 1.0, 1.0, 1.0)
        glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, specular_array) 
        glMaterialf(GL_FRONT_AND_BACK, GL_SHININESS, 64.0) 
        
        self.hull_model.draw()

        # ==========================================
        # 2. THE GLASS (Clear Transparent Glass)
        # ==========================================
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glDepthMask(GL_FALSE)

        glColor4f(0.3, 0.6, 1.0, 0.5)
        glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, specular_array)
        glMaterialf(GL_FRONT_AND_BACK, GL_SHININESS, 100.0) 
        
        self.glass_model.draw()

        glDepthMask(GL_TRUE)
        glDisable(GL_BLEND)
        
        # ==========================================
        # 3. THE LED WEAPON INDICATORS (Glowing)
        # ==========================================
        glDisable(GL_LIGHTING)
    
        color = self.get_current_color()
        glColor3f(color[0], color[1], color[2])
        self.led_model.draw()
        
        glEnable(GL_LIGHTING)
        
        glPopMatrix()