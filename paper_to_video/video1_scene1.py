from manim import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.elevenlabs import ElevenLabsService
import numpy as np
import os

# Zone definitions
ZONES = {
    'title': np.array([0, 3.2, 0]),
    'top_left': np.array([-4, 2, 0]),
    'top_right': np.array([4, 2, 0]),
    'left': np.array([-4, 0, 0]),
    'center': np.array([0, 0, 0]),
    'right': np.array([4, 0, 0]),
    'bottom': np.array([0, -2.5, 0])
}

# 3B1B Color palette
BLUE = "#58C4DD"
GREEN = "#8BE17D"
ORANGE = "#FFB74D"
RED = "#FF6188"
YELLOW = "#FFD700"

class Video1Scene1(VoiceoverScene):
    """
    Scene: The Multi-Distribution Challenge
    Narration: Imagine you're training a model that needs to juggle multiple probability distributions at once—matching images to captions, aligning generated outputs with human preferences, and satisfying safety constraints simultaneously. Current methods handle these relationships one pair at a time, but what if we could see the whole picture?
    """
    
    def construct(self):
        # ElevenLabs voice
        self.set_speech_service(
            ElevenLabsService(
                api_key=os.getenv("ELEVENLABS_API_KEY"),
                voice_id="21m00Tcm4TUPJeGCAgmA"
            )
        )
        
        self.camera.background_color = "#000000"
        
        # Define zones for layout
        ZONES = {
            "title": np.array([0, 3.2, 0]),
            "left": np.array([-4, 0, 0]),
            "center": np.array([0, 0, 0]),
            "right": np.array([4, 0, 0]),
            "bottom": np.array([0, -2.5, 0])
        }

        with self.voiceover(text="Imagine you're training a model that needs to juggle multiple probability distributions at once—matching images to captions, aligning generated outputs with human preferences, and satisfying safety constraints simultaneously. Current methods handle these relationships one pair at a time, but what if we could see the whole picture?") as tracker:

            # Set up 3D camera
            self.set_camera_orientation(phi=70 * DEGREES, theta=-45 * DEGREES)

            # Define distribution colors and labels
            dist_info = [
                (RED, "Images", 0),
                (BLUE, "Text", 72 * DEGREES),
                (GREEN, "Preferences", 144 * DEGREES),
                (YELLOW, "Constraints", 216 * DEGREES),
                (PURPLE, "Outputs", 288 * DEGREES)
            ]

            # Create 3D Gaussian surfaces arranged in pentagon
            distributions = VGroup()
            labels = VGroup()
            radius = 3

            for color, label_text, angle in dist_info:
                # Position in pentagon formation
                x = radius * np.cos(angle)
                y = radius * np.sin(angle)

                # Create 3D Gaussian surface
                surface = Surface(
                    lambda u, v: np.array([
                        u, v, 1.5 * np.exp(-(u**2 + v**2) / 0.5)
                    ]),
                    u_range=[-1, 1],
                    v_range=[-1, 1],
                    resolution=(20, 20),
                    fill_opacity=0.6,
                    stroke_width=0.5,
                    stroke_color=color,
                    fill_color=color
                )
                surface.shift(np.array([x, y, 0]))
                distributions.add(surface)

                # Create label
                label = Text(label_text, font_size=24, color=color)
                label.rotate(90 * DEGREES, axis=RIGHT)
                label.next_to(surface, OUT, buff=0.3)
                labels.add(label)

            # Animate distributions appearing with stagger
            self.play(
                LaggedStart(*[
                    FadeIn(dist, shift=OUT*0.5, scale=0.8)
                    for dist in distributions
                ], lag_ratio=0.15),
                LaggedStart(*[
                    Write(label)
                    for label in labels
                ], lag_ratio=0.15),
                run_time=tracker.duration * 0.3
            )

            # Create pairwise connection lines (complete graph)
            connection_lines = VGroup()
            num_dists = len(distributions)

            for i in range(num_dists):
                for j in range(i + 1, num_dists):
                    # Get centers of distributions
                    start = distributions[i].get_center()
                    end = distributions[j].get_center()

                    # Create dashed line
                    line = DashedLine(
                        start + OUT * 0.5,
                        end + OUT * 0.5,
                        color=WHITE,
                        stroke_width=2,
                        stroke_opacity=0.4,
                        dash_length=0.1
                    )
                    connection_lines.add(line)

            # Animate pairwise connections pulsing
            self.play(
                LaggedStart(*[
                    Succession(
                        Create(line),
                        line.animate.set_stroke(opacity=0.7, width=3),
                        line.animate.set_stroke(opacity=0.4, width=2)
                    )
                    for line in connection_lines
                ], lag_ratio=0.08),
                run_time=tracker.duration * 0.35
            )

            self.wait(0.3)

            # Create central golden sphere representing unified solution
            center_sphere = Sphere(
                radius=0.6,
                resolution=(30, 30),
                fill_color=GOLD,
                fill_opacity=0.9,
                stroke_width=1,
                stroke_color=GOLD_E
            )
            center_sphere.move_to(ORIGIN + OUT * 1.5)

            # Add glow effect to sphere
            glow = Sphere(
                radius=0.8,
                resolution=(20, 20),
                fill_color=GOLD,
                fill_opacity=0.2,
                stroke_width=0
            )
            glow.move_to(center_sphere.get_center())

            # Create light rays from distributions to center
            light_rays = VGroup()
            for dist in distributions:
                start = dist.get_center() + OUT * 1.5
                end = center_sphere.get_center()

                ray = Line(
                    start, end,
                    color=GOLD,
                    stroke_width=3,
                    stroke_opacity=0
                )
                light_rays.add(ray)

            # Animate unified solution appearing
            self.play(
                FadeIn(glow, scale=0.5),
                GrowFromCenter(center_sphere),
                connection_lines.animate.set_stroke(opacity=0.15),
                run_time=0.8
            )

            # Animate light rays converging
            self.play(
                LaggedStart(*[
                    Succession(
                        ray.animate.set_stroke(opacity=0.8),
                        ray.animate.set_stroke(opacity=0.3)
                    )
                    for ray in light_rays
                ], lag_ratio=0.12),
                glow.animate.set_opacity(0.4).scale(1.2),
                run_time=tracker.duration * 0.25
            )

            # Orbit camera around the structure
            self.play(
                Rotate(
                    VGroup(distributions, labels, connection_lines, center_sphere, glow, light_rays),
                    angle=PI/2,
                    axis=OUT,
                    about_point=ORIGIN + OUT * 1
                ),
                run_time=tracker.duration * 0.1
            )

            # Final emphasis: pulse the center sphere
            self.play(
                center_sphere.animate.scale(1.15).set_fill(opacity=1),
                glow.animate.scale(1.3).set_opacity(0.5),
                run_time=0.4
            )
            self.play(
                center_sphere.animate.scale(1/1.15).set_fill(opacity=0.9),
                glow.animate.scale(1/1.3).set_opacity(0.3),
                run_time=0.4
            )

            self.wait(1)
