### Mini Game 2 - Visual Upgrade (Space Shooter)

## Build / Run Instructions
Ensure you have Python installed.

Install dependencies:
```bash
pip install pygame PyOpenGL
```
Run the game:
```bash
python main.py
```

## Controls
Mouse: Move the spaceship (X/Y axes).

Spacebar: Shoot current weapon.

1, 2, 3: Toggle weapon colors. Matching the weapon color to the asteroid color is required for destruction:

  - **Red:** (1.0, 0.0, 0.0) — Press 1.
  - **Green:** (0.0, 1.0, 0.0) — Press 2.
  - **Blue:** (0.0, 0.0, 1.0) — Press 3.
  - **Magenta:** (1.0, 0.0, 1.0) — Press 1 + 3.
  - **Yellow:** (1.0, 1.0, 0.0) — Press 1 + 2.
  - **Cyan:** (0.0, 1.0, 1.0) — Press 2 + 3.
  - **White:** (1.0, 1.0, 1.0) — Press 1 + 2 + 3 (or no keys).

E: Activate Skill (Fires 5 homing missiles).

## Feature Checklist (Grading Rubric)

[x] **A. Lighting & Shading (Fixed Pipeline):** Enabled OpenGL lighting using smooth shading (`GL_SMOOTH`). The scene features visible specular highlights on the metallic hull and glass.

[x] **B. Material System (3+ Materials):** Applied distinct material parameters per-object:

  - **Opaque Matte:** The Moon and Asteroids use low specular and zero shininess.
  - **Opaque Metallic:** The main ship hull is high-gloss chrome with 75.0 shininess and maximum specular.
  - **Transparent Glass:** The ship's canopy uses alpha blending.

[x] **C. Correct Transparency:** The canopy uses `SRC_ALPHA` blending. Depth writing is disabled during the glass pass (`glDepthMask(GL_FALSE)`) to prevent artifacts and restored afterward.

[x] **D. Day/Night Cycle:** A smooth sine-wave cycle transitions between Sun (`GL_LIGHT0`) and Moon (`GL_LIGHT1`). This cycle affects:

  - **Sky Color:** `glClearColor` transitions from space-blue to pitch black.
  - **Light Source:** The Sun orbits and fades, while the Moon rises to provide dim ambient light.
  - **Scene Brightness:** Global ambient and material diffuse scaling adjust based on time-of-day.

[x] **E. HUD / Overlay Text:** A 2D orthographic overlay displays four live values: Score, Lives, FPS, and Sun Intensity (Time of Day). The overlay is designed not to break 3D lighting or depth states.

[x] **F. Gameplay + New Interaction:** The game includes an Automatic Razor-Beam Headlight.

  - **Logic:** This is a specialized spotlight (`GL_LIGHT2`) that automatically activates when the Sun intensity drops below 0.2.
  - **Visuals:** It produces a super-narrow, high-intensity 2-degree beam aligned with the crosshair to illuminate targets in total darkness.
