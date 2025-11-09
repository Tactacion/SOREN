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

class Video1Scene2(VoiceoverScene):
    """
    Scene: Introducing Schrödinger Bridge
    Narration: The Schrödinger Bridge gives us a principled way to think about this. It asks: what's the most natural, entropy-respecting way to transform one probability distribution into another? Think of it like finding how a cloud of particles would naturally flow from one configuration to another.
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
        
        def construct(self):
            # Define zones for layout
            ZONES = {
                "title": np.array([0, 3.2, 0]),
                "left": np.array([-3.5, 0, 0]),
                "center": np.array([0, 0, 0]),
                "right": np.array([3.5, 0, 0]),
                "bottom": np.array([0, -2.5, 0])
            }

            # CLEANUP: Fade existing objects to background
            if len(self.mobjects) > 0:
                old_objects = VGroup(*[obj for obj in self.mobjects])
                self.play(
                    old_objects.animate.scale(0.4).set_opacity(0.15).to_edge(UR),
                    run_time=0.8
                )

            with self.voiceover(text="The Schrödinger Bridge gives us a principled way to think about this. It asks: what's the most natural, entropy-respecting way to transform one probability distribution into another? Think of it like finding how a cloud of particles would naturally flow from one configuration to another.") as tracker:

                # Title appears with emphasis
                title = Text("Schrödinger Bridge", font_size=44, weight=BOLD, color=YELLOW)
                title.move_to(ZONES["title"])
                self.play(
                    Write(title),
                    Flash(title, color=YELLOW, flash_radius=0.5),
                    run_time=1
                )

                # Create source distribution (blue Gaussian)
                source_axes = Axes(
                    x_range=[-2, 2, 1],
                    y_range=[-2, 2, 1],
                    x_length=2.5,
                    y_length=2.5,
                    tips=False
                ).shift(ZONES["left"] + DOWN*0.3).scale(0.8)

                def gaussian_2d(u, v):
                    return 1.2 * np.exp(-(u**2 + v**2) / 0.5)

                source_surface = Surface(
                    lambda u, v: source_axes.c2p(u, v, gaussian_2d(u, v)),
                    u_range=[-1.5, 1.5],
                    v_range=[-1.5, 1.5],
                    resolution=(20, 20),
                    fill_color=BLUE,
                    fill_opacity=0.7,
                    stroke_color=BLUE_D,
                    stroke_width=0.5
                )

                source_label = Text("Source", font_size=24, color=BLUE).next_to(source_axes, UP, buff=0.2)

                # Create target distribution (green crescent)
                target_axes = source_axes.copy().shift(ZONES["right"] - ZONES["left"])

                def crescent_2d(u, v):
                    r = np.sqrt(u**2 + v**2)
                    angle = np.arctan2(v, u)
                    return 1.5 * np.exp(-((r - 1)**2) / 0.3) * (1 + 0.5 * np.cos(angle)) * (u > -0.3)

                target_surface = Surface(
                    lambda u, v: target_axes.c2p(u, v, crescent_2d(u, v)),
                    u_range=[-1.5, 1.5],
                    v_range=[-1.5, 1.5],
                    resolution=(20, 20),
                    fill_color=GREEN,
                    fill_opacity=0.7,
                    stroke_color=GREEN_D,
                    stroke_width=0.5
                )

                target_label = Text("Target", font_size=24, color=GREEN).next_to(target_axes, UP, buff=0.2)

                # Animate distributions appearing
                self.play(
                    LaggedStart(
                        Create(source_axes),
                        Create(source_surface),
                        Write(source_label),
                        lag_ratio=0.3
                    ),
                    run_time=1.5
                )

                self.play(
                    LaggedStart(
                        Create(target_axes),
                        Create(target_surface),
                        Write(target_label),
                        lag_ratio=0.3
                    ),
                    run_time=1.5
                )

                # Generate particles from source distribution
                np.random.seed(42)
                num_particles = 200
                particles_start = []
                particles_end = []

                for _ in range(num_particles):
                    # Sample from 2D Gaussian
                    x = np.random.normal(0, 0.5)
                    y = np.random.normal(0, 0.5)
                    if abs(x) < 1.5 and abs(y) < 1.5:
                        start_pos = source_axes.c2p(x, y, 0)
                        particles_start.append(start_pos)

                        # Sample from crescent for end position
                        angle = np.random.uniform(-np.pi, np.pi)
                        r = 1 + np.random.normal(0, 0.3)
                        if np.cos(angle) > -0.3:
                            x_end = r * np.cos(angle)
                            y_end = r * np.sin(angle)
                            end_pos = target_axes.c2p(x_end, y_end, 0)
                            particles_end.append(end_pos)

                # Create particle dots
                particles = VGroup(*[
                    Dot(point=pos, radius=0.02, color=WHITE, fill_opacity=0.8)
                    for pos in particles_start[:len(particles_end)]
                ])

                self.play(
                    LaggedStart(*[FadeIn(p, scale=0.5) for p in particles], lag_ratio=0.005),
                    run_time=1.5
                )

                # Create three transport scenarios
                # 1. Direct Transport (red straight lines)
                direct_paths = VGroup(*[
                    Line(start, end, color=RED, stroke_width=0.5, stroke_opacity=0.3)
                    for start, end in zip(particles_start[:len(particles_end)], particles_end)
                ])
                direct_label = Text("Direct Transport", font_size=20, color=RED).move_to(ZONES["bottom"] + LEFT*3.5)

                # 2. Random Walk (gray chaotic)
                random_paths = VGroup()
                for start, end in zip(particles_start[:len(particles_end)][:50], particles_end[:50]):
                    path_points = [start]
                    for i in range(5):
                        intermediate = start + (end - start) * (i + 1) / 6 + np.random.randn(3) * 0.3
                        path_points.append(intermediate)
                    path_points.append(end)
                    random_paths.add(
                        VMobject(stroke_color=GRAY, stroke_width=0.5, stroke_opacity=0.2).set_points_as_corners(path_points)
                    )
                random_label = Text("Random Walk", font_size=20, color=GRAY).move_to(ZONES["bottom"])

                # 3. Schrödinger Bridge (golden smooth curves)
                bridge_paths = VGroup()
                for start, end in zip(particles_start[:len(particles_end)], particles_end):
                    # Create smooth curved path
                    control1 = start + (end - start) * 0.3 + UP * 0.3
                    control2 = start + (end - start) * 0.7 + DOWN * 0.2
                    bridge_paths.add(
                        CubicBezier(start, control1, control2, end, color=GOLD, stroke_width=1, stroke_opacity=0.4)
                    )
                bridge_label = Text("Schrödinger Bridge", font_size=20, color=GOLD).move_to(ZONES["bottom"] + RIGHT*3.5)

                # Show all three scenarios semi-transparently
                self.play(
                    LaggedStart(
                        AnimationGroup(Create(direct_paths, run_time=1), FadeIn(direct_label)),
                        AnimationGroup(Create(random_paths, run_time=1), FadeIn(random_label)),
                        AnimationGroup(Create(bridge_paths, run_time=1), FadeIn(bridge_label)),
                        lag_ratio=0.4
                    ),
                    run_time=3
                )

                self.wait(0.5)

                # Highlight Schrödinger Bridge by fading others
                self.play(
                    direct_paths.animate.set_opacity(0.1),
                    random_paths.animate.set_opacity(0.1),
                    direct_label.animate.set_opacity(0.3),
                    random_label.animate.set_opacity(0.3),
                    bridge_paths.animate.set_stroke(width=2, opacity=0.8),
                    bridge_label.animate.scale(1.2).set_color(YELLOW),
                    Flash(bridge_label, color=YELLOW, flash_radius=0.3),
                    run_time=1.5
                )

                # Animate particles flowing along golden paths
                particle_animations = []
                for particle, path in zip(particles, bridge_paths):
                    particle_animations.append(
                        MoveAlongPath(particle, path, rate_func=smooth, run_time=2.5)
                    )

                self.play(
                    LaggedStart(*particle_animations, lag_ratio=0.01),
                    run_time=3
                )

                # Final emphasis: particles glow at target
                self.play(
                    *[p.animate.set_color(GREEN).scale(1.5).set_opacity(1) for p in particles],
                    run_time=0.8
                )

                self.wait(1)
