# Mini Game 2 - Visual Upgrade (Space Shooter)

## Build / Run Instructions
1. Ensure you have Python installed.
2. Install the required dependencies using pip:
   ```bash
   pip install -r requirements.txt
   ```
   (Requirements include `pygame` and `PyOpenGL`).
3. Run the main script to start the game:
   ```bash
   python main.py
   ```

## Controls
*   **Mouse**: Move the spaceship (X/Y axes).
*   **Spacebar**: Shoot your current weapon.
*   **1, 2, 3**: Toggle the current weapon color (Red, Green, Blue). Matching colors destroy asteroids of the same color!
*   **E**: Activate Skill (Fires 5 homing missiles). Has a cooldown.
*   **F**: Toggle the Headlight (Only visible/active during the Night cycle).

## Feature Checklist (Grading Rubric)

- [x] **Lighting & Shading (Fixed Pipeline)**: Enabled OpenGL lighting, with a primary light source (Sun) that moves. Smooth shading is used, and visible specular highlights are present on the spaceship hull and glass.
- [x] **Material System (3+ Materials)**: Applied distinct materials using `glMaterialfv`. 
  - *Opaque Matte*: The asteroids use a matte material with 0 shininess.
  - *Opaque Glossy/Metallic*: The main ship hull is highly reflective chrome.
  - *Transparent/Glass*: The ship's canopy is clear glass.
- [x] **Correct Transparency**: The ship's canopy is transparent. Blending is enabled correctly (`GL_SRC_ALPHA`, `GL_ONE_MINUS_SRC_ALPHA`), and depth writing is temporarily disabled (`glDepthMask(GL_FALSE)`) while drawing it to prevent artifacts.
- [x] **Day/Night Cycle**: A smooth sine-wave based time parameter controls the sun's position. This dynamically alters:
  1. The background clearing color (`glClearColor`).
  2. The main light (`GL_LIGHT0`) intensity and color.
  3. The ambient and specular levels of the scene.
- [x] **HUD / Overlay Text**: A 2D Orthographic overlay displays 4 live values: `Score`, `Lives`, `FPS`, and `Time of Day` (Sun intensity factor).
- [x] **Gameplay + One New Interaction**: The game remains a fully playable 3D shooter. A new toggleable **Headlight (`F` key)** has been added. It is linked to the rendering upgrades, as it uses a spotlight (`GL_LIGHT1`) that automatically powers up fully only during the darkest part of the night cycle. 
