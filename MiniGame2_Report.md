# Mini Game 2: Visual Upgrades Report

## 1. Material System Description
The material system was implemented by managing OpenGL's built-in fixed-function pipeline properties (`GL_AMBIENT`, `GL_DIFFUSE`, `GL_SPECULAR`, and `GL_SHININESS`) per object. `glMaterialfv` and `glMaterialf` were used before drawing each respective 3D model component to give them unique physical properties reacting to the light.

*   **Opaque Matte (Asteroids):** The asteroids use a very simple matte material. Their specular lighting was explicitly set to 0.0, and shininess to 0.0. This makes them look like dull, unpolished rocks that absorb light rather than reflecting it, contrasting greatly with the spaceship.
*   **Opaque Glossy/Metallic (Ship Hull):** The main body of the spaceship was given a chrome-like appearance. This was achieved by setting high ambient and diffuse values, but specifically maxing out the specular highlight to `[1.0, 1.0, 1.0, 1.0]` and setting the shininess exponent extremely high (`128.0`). This creates sharp, intense highlights typical of polished metal.
*   **Transparent Glass (Ship Canopy):** The glass uses a material with an alpha value of `0.25` in its ambient/diffuse channels, combined with a high specular highlight. This ensures it catches the light (looking physically present) while remaining see-through. 

## 2. Transparency Approach
Transparency was handled by strictly managing the OpenGL state machine around the drawing of the glass canopy object to prevent depth sorting artifacts. 
1.  **Blending Setup:** `glEnable(GL_BLEND)` was called, using the standard formula `glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)`.
2.  **Depth Masking:** Crucially, `glDepthMask(GL_FALSE)` was called before drawing the glass. This allows the glass to be drawn and depth-tested against *existing* objects, but prevents the glass from writing its own depth into the buffer. This ensures that objects drawn behind or inside the glass after the glass is drawn aren't incorrectly occluded.
3.  **State Restoration:** After drawing the glass, `glDepthMask(GL_TRUE)` and `glDisable(GL_BLEND)` are called immediately to restore the state for the rest of the opaque objects in the scene.

## 3. Day / Night Model
The Day/Night cycle was modeled by treating `GL_LIGHT0` as the sun. A global `time_factor` increments continuously, acting as the input to sine and cosine functions to calculate the sun's orbital position around the X/Y axes (a directional light, `w=0.0`).

When the sun's Y position is positive (North arc), it represents daytime. The intensity follows the sine curve, peaking at the top and fading at the horizon. When the Y position is negative (South arc), the light is "turned off" by setting its diffuse and specular components to zero, simulating nighttime. The `time_factor` also directly dynamically drives the `glClearColor` to transition from a light blue sky to a dark, deep void, and modulates the global ambient light to ensure the scene doesn't turn entirely pitch black.

## 4. Key Design Decisions & Gameplay Integration
A significant design decision was the integration of the **Headlight**. Rather than just adding a visual flair that was always on, the headlight was explicitly tied to the Day/Night cycle to enhance gameplay.

The headlight (`GL_LIGHT1`) is configured as a Spot Light (`GL_SPOT_CUTOFF` and `GL_SPOT_DIRECTION`). It points forward from the ship. Its intensity is inversely proportional to the sun's intensity. During the day, it is structurally disabled (intensity = 0). As the world plunges into darkness, the player can press `F` to toggle the headlight, providing a vital cone of illumination to see incoming asteroids in the pitch black. This ties the rendering requirement (multiple lights, spot lighting) directly to a meaningful gameplay interaction (surviving the visual impairment of night).
