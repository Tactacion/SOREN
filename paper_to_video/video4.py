from manim import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.elevenlabs import ElevenLabsService
import numpy as np
import os

ZONES = {
    'title': np.array([0, 3.2, 0]),
    'top_left': np.array([-4, 2, 0]),
    'top_right': np.array([4, 2, 0]),
    'left': np.array([-4, 0, 0]),
    'center': np.array([0, 0, 0]),
    'right': np.array([4, 0, 0]),
    'bottom': np.array([0, -2.5, 0])
}

BLUE = "#58C4DD"
GREEN = "#8BE17D"
ORANGE = "#FFB74D"
RED = "#FF6188"
YELLOW = "#FFD700"
GOLD = "#FFD700"
PURPLE = "#C678DD"
GRAY = "#888888"
WHITE = "#FFFFFF"

class Video4(VoiceoverScene):
    """
    Impact
    """
    
    def construct(self):
        self.set_speech_service(
            ElevenLabsService(
                api_key=os.getenv("ELEVENLABS_API_KEY"),
                voice_id="21m00Tcm4TUPJeGCAgmA"
            )
        )
        
        self.camera.background_color = "#000000"

        # ============================================================
        # SCENE 1: The Regret-Information Connection
        # ============================================================
        # Scene 1: The Regret-Information Connection
        
        if self.mobjects:
            self.play(*[FadeOut(obj) for obj in self.mobjects], run_time=0.5)
        
        with self.voiceover(text="""Here's the beautiful insight that makes Bayesian optimization work: there's a mathematical bridge connecting how much regret you accumulate and how much information you gain. Learn faster about the function, and you'll make better decisions with lower regret.""") as tracker:
            
            # Step 1: Title
            title = Text("The Regret-Information Connection", font_size=42, color=GOLD)
            title.move_to(ZONES['title'])
            self.play(Write(title), run_time=1)
            
            # Step 2: Create left pillar (RED rectangle for REGRET)
            self.left_pillar = Rectangle(width=1.5, height=3, color=RED, fill_opacity=0.3)
            self.left_pillar.move_to([-4, -1, 0])
            left_label = Text("REGRET", font_size=28, color=RED, weight=BOLD)
            left_label.next_to(self.left_pillar, DOWN, buff=0.3)
            
            self.play(
                FadeIn(self.left_pillar, scale=0.5),
                Write(left_label),
                run_time=1.2
            )
            
            # Step 3: Create right pillar (BLUE rectangle for INFORMATION GAIN)
            self.right_pillar = Rectangle(width=1.5, height=3, color=BLUE, fill_opacity=0.3)
            self.right_pillar.move_to([4, -1, 0])
            right_label = Text("INFORMATION\nGAIN", font_size=24, color=BLUE, weight=BOLD)
            right_label.next_to(self.right_pillar, DOWN, buff=0.3)
            
            self.play(
                FadeIn(self.right_pillar, scale=0.5),
                Write(right_label),
                run_time=1.2
            )
            
            # Step 4: Create ground base for pillars
            ground_base = Line(start=[-5.5, -2.5, 0], end=[5.5, -2.5, 0], color=GRAY, stroke_width=4)
            self.play(Create(ground_base), run_time=0.8)
            
            # Step 5: Create bridge arch (curved path connecting pillars)
            left_top = self.left_pillar.get_top()
            right_top = self.right_pillar.get_top()
            mid_point = [(left_top[0] + right_top[0])/2, left_top[1] + 1.5, 0]
            
            self.bridge_arch = VMobject(color=GOLD, stroke_width=6)
            self.bridge_arch.set_points_smoothly([
                left_top,
                [left_top[0] + 1, left_top[1] + 0.8, 0],
                mid_point,
                [right_top[0] - 1, right_top[1] + 0.8, 0],
                right_top
            ])
            
            self.play(Create(self.bridge_arch), run_time=2)
            
            # Step 6: Add equation on bridge
            self.equation_text = MathTex(r"\text{Regret} \leq \sqrt{T \times \gamma_T}", font_size=32, color=WHITE)
            self.equation_text.move_to(mid_point)
            self.equation_text.shift(UP*0.3)
            
            self.play(Write(self.equation_text), run_time=1.5)
            
            # Step 7: Create particle system (flowing dots from right to left)
            particles = VGroup(*[
                Dot(point=[4 + 0.3, 0.5 + i*0.4, 0], radius=0.06, color=BLUE)
                for i in range(6)
            ])
            
            self.play(
                LaggedStart(*[FadeIn(p, scale=0.3) for p in particles], lag_ratio=0.15),
                run_time=1.5
            )
            
            # Step 8: Animate particles flowing along bridge
            particle_targets = VGroup(*[
                Dot(point=[-4 - 0.3, 0.5 + i*0.4, 0], radius=0.06, color=RED)
                for i in range(6)
            ])
            
            self.play(
                *[Transform(particles[i], particle_targets[i]) for i in range(6)],
                run_time=2.5
            )
            
            # Step 9: Flash effects at connection points
            self.play(
                Flash(left_top, color=RED, flash_radius=0.5),
                Flash(right_top, color=BLUE, flash_radius=0.5),
                run_time=0.8
            )
            
            # Step 10: Add arrows showing information flow
            flow_arrow1 = Arrow(
                start=[3, 0, 0],
                end=[0, 1, 0],
                color=PURPLE,
                buff=0.1,
                stroke_width=4
            )
            flow_arrow2 = Arrow(
                start=[0, 1, 0],
                end=[-3, 0, 0],
                color=PURPLE,
                buff=0.1,
                stroke_width=4
            )
            
            self.play(
                Create(flow_arrow1),
                Create(flow_arrow2),
                run_time=1.5
            )
            
            # Step 11: Highlight the equation with a glow effect
            equation_box = Rectangle(
                width=self.equation_text.width + 0.5,
                height=self.equation_text.height + 0.3,
                color=YELLOW,
                stroke_width=3
            )
            equation_box.move_to(self.equation_text.get_center())
            
            self.play(Create(equation_box), run_time=0.8)
            self.play(FadeOut(equation_box), run_time=0.5)
            
            # Step 12: Pulse animation on pillars to emphasize connection
            self.play(
                self.left_pillar.animate.scale(1.1).set_fill(opacity=0.5),
                self.right_pillar.animate.scale(1.1).set_fill(opacity=0.5),
                run_time=0.8
            )
            self.play(
                self.left_pillar.animate.scale(1/1.1).set_fill(opacity=0.3),
                self.right_pillar.animate.scale(1/1.1).set_fill(opacity=0.3),
                run_time=0.8
            )
            
            self.wait(0.5)

        # ============================================================
        # SCENE 2: Dual Perspective Setup
        # ============================================================
        # Scene 2: Dual Perspective Setup
        
        if self.mobjects:
            self.play(*[FadeOut(obj) for obj in self.mobjects], run_time=0.5)
        
        with self.voiceover(text="""Let's watch both quantities evolve together as we run Bayesian optimization. On top, we'll track cumulative regret—the price we pay for not knowing the optimum. Below, we'll track information gain—how much we've learned about the function.""") as tracker:
            
            # Step 1: Title
            title = Text("Dual Perspective Setup", font_size=42, color=GOLD)
            title.move_to(ZONES['title'])
            self.play(Write(title), run_time=1)
            
            # Step 2: Create top axes (cumulative regret)
            self.top_axes = Axes(
                x_range=[0, 50, 10],
                y_range=[0, 100, 20],
                x_length=9,
                y_length=2.5,
                axis_config={"color": WHITE}
            )
            self.top_axes.move_to([0, 1.5, 0])
            
            # Step 3: Create bottom axes (information gain)
            self.bottom_axes = Axes(
                x_range=[0, 50, 10],
                y_range=[0, 20, 5],
                x_length=9,
                y_length=2.5,
                axis_config={"color": WHITE}
            )
            self.bottom_axes.move_to([0, -1.5, 0])
            
            # Step 4: Animate both axes appearing
            self.play(
                Create(self.top_axes),
                Create(self.bottom_axes),
                run_time=2
            )
            
            # Step 5: Create y-axis labels
            top_y_label = Text("Cumulative Regret", font_size=28, color=RED)
            top_y_label.next_to(self.top_axes.y_axis, LEFT, buff=0.3)
            top_y_label.rotate(90 * DEGREES)
            
            bottom_y_label = MathTex(r"\text{Information Gain } \gamma_T", font_size=28, color=BLUE)
            bottom_y_label.next_to(self.bottom_axes.y_axis, LEFT, buff=0.3)
            bottom_y_label.rotate(90 * DEGREES)
            
            # Step 6: Animate y-axis labels
            self.play(
                Write(top_y_label),
                Write(bottom_y_label),
                run_time=1.5
            )
            
            # Step 7: Create x-axis labels
            top_x_label = Text("Iterations", font_size=24, color=WHITE)
            top_x_label.next_to(self.top_axes.x_axis, DOWN, buff=0.2)
            
            bottom_x_label = Text("Iterations", font_size=24, color=WHITE)
            bottom_x_label.next_to(self.bottom_axes.x_axis, DOWN, buff=0.2)
            
            # Step 8: Animate x-axis labels
            self.play(
                FadeIn(top_x_label, shift=UP*0.2),
                FadeIn(bottom_x_label, shift=UP*0.2),
                run_time=1
            )
            
            # Step 9: Create vertical dotted line at x=0
            top_start = self.top_axes.c2p(0, 0)
            bottom_end = self.bottom_axes.c2p(0, 0)
            self.vertical_line = DashedLine(
                start=top_start,
                end=bottom_end,
                color=GRAY,
                dash_length=0.1,
                stroke_width=2
            )
            
            # Step 10: Animate vertical line
            self.play(Create(self.vertical_line), run_time=1)
            
            # Step 11: Create icons - frowning face (regret is bad)
            self.frowning_face = Text("☹", font_size=36, color=RED)
            self.frowning_face.next_to(top_y_label, LEFT, buff=0.3)
            
            # Step 12: Create lightbulb icon (learning is good)
            self.lightbulb = Text("💡", font_size=36, color=YELLOW)
            self.lightbulb.next_to(bottom_y_label, LEFT, buff=0.3)
            
            # Step 13: Animate icons with flash effect
            self.play(
                FadeIn(self.frowning_face, scale=0.5),
                run_time=0.8
            )
            
            # Step 14: Animate lightbulb
            self.play(
                FadeIn(self.lightbulb, scale=0.5),
                run_time=0.8
            )
            
            # Step 15: Add grid lines to both axes for clarity
            top_grid_lines = VGroup()
            for y in [20, 40, 60, 80]:
                line = DashedLine(
                    self.top_axes.c2p(0, y),
                    self.top_axes.c2p(50, y),
                    color=GRAY,
                    dash_length=0.05,
                    stroke_width=1
                )
                top_grid_lines.add(line)
            
            bottom_grid_lines = VGroup()
            for y in [5, 10, 15]:
                line = DashedLine(
                    self.bottom_axes.c2p(0, y),
                    self.bottom_axes.c2p(50, y),
                    color=GRAY,
                    dash_length=0.05,
                    stroke_width=1
                )
                bottom_grid_lines.add(line)
            
            # Step 16: Animate grid lines
            self.play(
                LaggedStart(*[Create(line) for line in top_grid_lines], lag_ratio=0.1),
                LaggedStart(*[Create(line) for line in bottom_grid_lines], lag_ratio=0.1),
                run_time=1.5
            )
            
            self.wait(0.5)

        # ============================================================
        # SCENE 3: First Iterations
        # ============================================================
        # Scene 3: First Iterations
        
        # Continue from previous
        
        with self.voiceover(text="""In early iterations, we're exploring aggressively. Each experiment reveals a lot of new information—notice the steep blue curve—but we're also making suboptimal choices, so regret accumulates quickly in red.""") as tracker:
            
            # Step 1: Title
            title = Text("First Iterations", font_size=42, color=GOLD)
            title.move_to(ZONES['title'])
            self.play(Write(title), run_time=1)
            
            # Step 2: Create 10 points for red curve (regret - top plot)
            # Steep accumulation in early iterations
            red_x_vals = [i for i in range(10)]
            red_y_vals = [0, 0.8, 1.8, 3.0, 4.3, 5.7, 7.2, 8.8, 10.5, 12.3]
            red_curve_points = [self.top_axes.c2p(x, y) for x, y in zip(red_x_vals, red_y_vals)]
            
            # Step 3: Create 10 points for blue curve (information gain - bottom plot)
            # Steep initial learning
            blue_y_vals = [0, 2.5, 4.2, 5.5, 6.5, 7.3, 7.9, 8.4, 8.8, 9.1]
            blue_curve_points = [self.bottom_axes.c2p(x, y) for x, y in zip(red_x_vals, blue_y_vals)]
            
            # Step 4: Create red dots
            red_dots = VGroup(*[
                Dot(point, radius=0.06, color=RED)
                for point in red_curve_points
            ])
            
            # Step 5: Create blue dots
            blue_dots = VGroup(*[
                Dot(point, radius=0.06, color=BLUE)
                for point in blue_curve_points
            ])
            
            # Step 6: Animate first few points with flash effects
            for i in range(4):
                # Flash circles at new points
                flash_red = Circle(radius=0.15, color=RED).move_to(red_curve_points[i])
                flash_blue = Circle(radius=0.15, color=BLUE).move_to(blue_curve_points[i])
                
                # Vertical dotted line connecting points
                vertical_line = DashedLine(
                    red_curve_points[i], 
                    blue_curve_points[i], 
                    color=GRAY, 
                    dash_length=0.1
                )
                
                self.play(
                    Flash(red_curve_points[i], color=RED, flash_radius=0.3),
                    Flash(blue_curve_points[i], color=BLUE, flash_radius=0.3),
                    FadeIn(red_dots[i], scale=0.5),
                    FadeIn(blue_dots[i], scale=0.5),
                    Create(vertical_line),
                    run_time=0.6
                )
                
                # Draw line segment if not first point
                if i > 0:
                    red_segment = Line(
                        red_curve_points[i-1], 
                        red_curve_points[i], 
                        color=RED, 
                        stroke_width=3
                    )
                    blue_segment = Line(
                        blue_curve_points[i-1], 
                        blue_curve_points[i], 
                        color=BLUE, 
                        stroke_width=3
                    )
                    self.play(
                        Create(red_segment),
                        Create(blue_segment),
                        run_time=0.4
                    )
            
            # Step 7: Speed up for remaining points
            remaining_red_dots = VGroup(*[red_dots[i] for i in range(4, 10)])
            remaining_blue_dots = VGroup(*[blue_dots[i] for i in range(4, 10)])
            
            self.play(
                LaggedStart(*[FadeIn(d, scale=0.5) for d in remaining_red_dots], lag_ratio=0.1),
                LaggedStart(*[FadeIn(d, scale=0.5) for d in remaining_blue_dots], lag_ratio=0.1),
                run_time=1.5
            )
            
            # Step 8: Draw remaining line segments
            red_line_segments = VGroup()
            blue_line_segments = VGroup()
            
            for i in range(4, 10):
                red_segment = Line(
                    red_curve_points[i-1], 
                    red_curve_points[i], 
                    color=RED, 
                    stroke_width=3
                )
                blue_segment = Line(
                    blue_curve_points[i-1], 
                    blue_curve_points[i], 
                    color=BLUE, 
                    stroke_width=3
                )
                red_line_segments.add(red_segment)
                blue_line_segments.add(blue_segment)
            
            self.play(
                LaggedStart(*[Create(seg) for seg in red_line_segments], lag_ratio=0.08),
                LaggedStart(*[Create(seg) for seg in blue_line_segments], lag_ratio=0.08),
                run_time=1.5
            )
            
            # Step 9: Create smooth curves through points
            red_curve = VMobject(color=RED, stroke_width=4)
            red_curve.set_points_smoothly(red_curve_points)
            
            blue_curve = VMobject(color=BLUE, stroke_width=4)
            blue_curve.set_points_smoothly(blue_curve_points)
            
            # Step 10: Highlight the steep blue curve
            blue_highlight = blue_curve.copy().set_stroke(color=YELLOW, width=6)
            self.play(
                Create(blue_highlight),
                run_time=1
            )
            self.play(FadeOut(blue_highlight), run_time=0.5)
            
            # Step 11: Highlight accumulating red regret
            red_highlight = red_curve.copy().set_stroke(color=ORANGE, width=6)
            self.play(
                Create(red_highlight),
                run_time=1
            )
            self.play(FadeOut(red_highlight), run_time=0.5)
            
            # Step 12: Create vertical connectors for storage
            vertical_connectors = VGroup(*[
                DashedLine(
                    red_curve_points[i], 
                    blue_curve_points[i], 
                    color=GRAY, 
                    dash_length=0.08
                )
                for i in range(0, 10, 2)
            ])
            
            self.play(
                LaggedStart(*[Create(line) for line in vertical_connectors], lag_ratio=0.1),
                run_time=1
            )
            
            # STORE for next scene
            self.red_curve = red_curve
            self.blue_curve = blue_curve
            self.red_dots = red_dots
            self.blue_dots = blue_dots
            self.vertical_connectors = vertical_connectors
            
            self.wait(0.5)

        # ============================================================
        # SCENE 4: Exploitation Phase
        # ============================================================
        # Scene 4: Exploitation Phase
        
        # Continue from previous
        
        with self.voiceover(text="""As we learn more, the information gain curve flattens—there's less new to discover. But here's the payoff: our regret curve also grows more slowly because we're now exploiting our knowledge to make better choices.""") as tracker:
            
            # Step 1: Title
            title = Text("Exploitation Phase", font_size=42, color=GOLD)
            title.move_to(ZONES['title'])
            self.play(Write(title), run_time=1)
            
            # Step 2: Create extension curves from iteration 10 to 30
            # Red curve (regret) - logarithmic growth slowing down
            red_extension_points = []
            for i in range(10, 31):
                x = self.bottom_axes.c2p(i, 0)[0]
                # Logarithmic curve that flattens: y = 2.5 + 0.8*log(i-8)
                y_val = 2.5 + 0.8 * (i - 8) ** 0.4
                y = self.bottom_axes.c2p(0, y_val)[1]
                red_extension_points.append([x, y, 0])
            
            red_curve_extension = VMobject(color=RED, stroke_width=4)
            red_curve_extension.set_points_smoothly(red_extension_points)
            
            # Blue curve (information gain) - flattening more dramatically
            blue_extension_points = []
            for i in range(10, 31):
                x = self.top_axes.c2p(i, 0)[0]
                # Flattening curve: y = 3.0 + 0.5*log(i-8)
                y_val = 3.0 + 0.5 * (i - 8) ** 0.35
                y = self.top_axes.c2p(0, y_val)[1]
                blue_extension_points.append([x, y, 0])
            
            blue_curve_extension = VMobject(color=BLUE, stroke_width=4)
            blue_curve_extension.set_points_smoothly(blue_extension_points)
            
            # Step 3: Animate curve extensions
            self.play(
                Create(red_curve_extension),
                Create(blue_curve_extension),
                run_time=2.5
            )
            
            # Step 4: Create dots on extensions
            red_dots_extension = VGroup(*[
                Dot(red_extension_points[i], radius=0.06, color=RED)
                for i in range(0, len(red_extension_points), 1)
            ])
            
            blue_dots_extension = VGroup(*[
                Dot(blue_extension_points[i], radius=0.06, color=BLUE)
                for i in range(0, len(blue_extension_points), 1)
            ])
            
            # Step 5: Animate dots appearing
            self.play(
                LaggedStart(*[FadeIn(d, scale=0.5) for d in red_dots_extension], lag_ratio=0.05),
                LaggedStart(*[FadeIn(d, scale=0.5) for d in blue_dots_extension], lag_ratio=0.05),
                run_time=2
            )
            
            # Step 6: Create tangent line at iteration 10 on red curve (steeper)
            red_point_10 = red_extension_points[0]
            tangent_length = 1.5
            # Steeper slope (~45 degrees)
            tangent_line_red_10 = Line(
                start=[red_point_10[0] - tangent_length*0.7, red_point_10[1] - tangent_length*0.7, 0],
                end=[red_point_10[0] + tangent_length*0.7, red_point_10[1] + tangent_length*0.7, 0],
                color=ORANGE,
                stroke_width=3
            )
            
            # Step 7: Create tangent line at iteration 30 on red curve (flatter)
            red_point_30 = red_extension_points[-1]
            # Flatter slope (~20 degrees)
            tangent_line_red_30 = Line(
                start=[red_point_30[0] - tangent_length*0.9, red_point_30[1] - tangent_length*0.36, 0],
                end=[red_point_30[0] + tangent_length*0.9, red_point_30[1] + tangent_length*0.36, 0],
                color=ORANGE,
                stroke_width=3
            )
            
            # Step 8: Animate red tangent lines
            self.play(Create(tangent_line_red_10), run_time=0.8)
            self.wait(0.3)
            
            angle_label_red_10 = Text("~45°", font_size=24, color=ORANGE)
            angle_label_red_10.next_to(tangent_line_red_10, RIGHT, buff=0.2)
            self.play(FadeIn(angle_label_red_10, scale=0.8), run_time=0.5)
            
            # Step 9: Show flatter tangent at iteration 30
            self.play(Create(tangent_line_red_30), run_time=0.8)
            self.wait(0.3)
            
            angle_label_red_30 = Text("~20°", font_size=24, color=ORANGE)
            angle_label_red_30.next_to(tangent_line_red_30, RIGHT, buff=0.2)
            self.play(FadeIn(angle_label_red_30, scale=0.8), run_time=0.5)
            
            # Step 10: Create tangent line at iteration 10 on blue curve
            blue_point_10 = blue_extension_points[0]
            tangent_line_blue_10 = Line(
                start=[blue_point_10[0] - tangent_length*0.8, blue_point_10[1] - tangent_length*0.56, 0],
                end=[blue_point_10[0] + tangent_length*0.8, blue_point_10[1] + tangent_length*0.56, 0],
                color=YELLOW,
                stroke_width=3
            )
            
            # Step 11: Create tangent line at iteration 30 on blue curve (very flat)
            blue_point_30 = blue_extension_points[-1]
            tangent_line_blue_30 = Line(
                start=[blue_point_30[0] - tangent_length*0.98, blue_point_30[1] - tangent_length*0.17, 0],
                end=[blue_point_30[0] + tangent_length*0.98, blue_point_30[1] + tangent_length*0.17, 0],
                color=YELLOW,
                stroke_width=3
            )
            
            # Step 12: Animate blue tangent lines
            self.play(Create(tangent_line_blue_10), run_time=0.8)
            self.wait(0.3)
            
            angle_label_blue_10 = Text("~35°", font_size=24, color=YELLOW)
            angle_label_blue_10.next_to(tangent_line_blue_10, RIGHT, buff=0.2)
            self.play(FadeIn(angle_label_blue_10, scale=0.8), run_time=0.5)
            
            # Step 13: Show very flat tangent at iteration 30
            self.play(Create(tangent_line_blue_30), run_time=0.8)
            self.wait(0.3)
            
            angle_label_blue_30 = Text("~10°", font_size=24, color=YELLOW)
            angle_label_blue_30.next_to(tangent_line_blue_30, RIGHT, buff=0.2)
            self.play(FadeIn(angle_label_blue_30, scale=0.8), run_time=0.5)
            
            # Step 14: Highlight the flattening with flash effects
            self.play(
                Flash(red_point_30, color=RED, flash_radius=0.5),
                Flash(blue_point_30, color=BLUE, flash_radius=0.5),
                run_time=0.8
            )
            
            # Step 15: Update stored objects
            # Combine original curves with extensions
            self.red_curve = VGroup(self.red_curve, red_curve_extension)
            self.blue_curve = VGroup(self.blue_curve, blue_curve_extension)
            self.red_dots = VGroup(self.red_dots, red_dots_extension)
            self.blue_dots = VGroup(self.blue_dots, blue_dots_extension)
            
            # Store tangent lines
            self.tangent_red_10 = tangent_line_red_10
            self.tangent_red_30 = tangent_line_red_30
            self.tangent_blue_10 = tangent_line_blue_10
            self.tangent_blue_30 = tangent_line_blue_30
            
            # Store angle labels
            self.angle_labels = VGroup(
                angle_label_red_10,
                angle_label_red_30,
                angle_label_blue_10,
                angle_label_blue_30
            )
            
            self.wait(0.5)

        # ============================================================
        # SCENE 5: The Square Root Relationship
        # ============================================================
        # Scene 5: The Square Root Relationship
        
        # Continue from previous
        
        with self.voiceover(text="""The theoretical bound tells us regret grows like the square root of time multiplied by information gain. This sublinear growth is crucial—it means our average regret per iteration actually decreases over time.""") as tracker:
            
            # Step 1: Title
            title = Text("The Square Root Relationship", font_size=42, color=GOLD)
            title.move_to(ZONES['title'])
            self.play(Write(title), run_time=1)
            
            # Step 2: Extend red curve from iteration 30 to 50
            red_extension_points = [self.top_axes.c2p(t, 30 + 0.7 * (t - 30)) for t in range(31, 51)]
            self.extended_red_curve = VMobject(color=RED, stroke_width=3)
            self.extended_red_curve.set_points_smoothly([self.top_axes.c2p(30, 30)] + red_extension_points)
            self.play(Create(self.extended_red_curve), run_time=1.5)
            
            # Step 3: Extend blue curve from iteration 30 to 50
            blue_extension_points = [self.bottom_axes.c2p(t, 10 + 0.1 * (t - 30)) for t in range(31, 51)]
            self.extended_blue_curve = VMobject(color=BLUE, stroke_width=3)
            self.extended_blue_curve.set_points_smoothly([self.bottom_axes.c2p(30, 10)] + blue_extension_points)
            self.play(Create(self.extended_blue_curve), run_time=1.5)
            
            # Step 4: Add dots at key points on extended curves
            extended_red_dots = VGroup(*[
                Dot(self.top_axes.c2p(t, 30 + 0.7 * (t - 30)), radius=0.06, color=RED)
                for t in [35, 40, 45, 50]
            ])
            extended_blue_dots = VGroup(*[
                Dot(self.bottom_axes.c2p(t, 10 + 0.1 * (t - 30)), radius=0.06, color=BLUE)
                for t in [35, 40, 45, 50]
            ])
            self.play(
                LaggedStart(*[FadeIn(d, scale=0.5) for d in extended_red_dots], lag_ratio=0.1),
                LaggedStart(*[FadeIn(d, scale=0.5) for d in extended_blue_dots], lag_ratio=0.1),
                run_time=1.5
            )
            
            # Step 5: Create theoretical bound curve (yellow, semi-transparent)
            bound_points = [self.top_axes.c2p(t, 5 * (t ** 0.5)) for t in range(1, 51)]
            self.yellow_bound_curve = VMobject(color=YELLOW, stroke_width=4, stroke_opacity=0.6)
            self.yellow_bound_curve.set_points_smoothly(bound_points)
            self.play(Create(self.yellow_bound_curve), run_time=2)
            
            # Step 6: Add formula for theoretical bound
            bound_formula = MathTex(r"\sqrt{T \times \gamma_T}", font_size=32, color=YELLOW)
            bound_formula.next_to(self.top_axes.c2p(50, 5 * (50 ** 0.5)), RIGHT, buff=0.3)
            self.play(Write(bound_formula), run_time=1)
            
            # Step 7: Create gap annotation showing distance between actual regret and bound
            gap_start = self.top_axes.c2p(40, 30 + 0.7 * 10)
            gap_end = self.top_axes.c2p(40, 5 * (40 ** 0.5))
            self.gap_annotation = Arrow(gap_start, gap_end, color=ORANGE, buff=0.1, stroke_width=3)
            gap_label = Text("Gap to bound", font_size=24, color=ORANGE)
            gap_label.next_to(self.gap_annotation, RIGHT, buff=0.2)
            self.play(Create(self.gap_annotation), FadeIn(gap_label, shift=LEFT*0.3), run_time=1.5)
            
            # Step 8: Create inset axes in bottom-right corner
            self.inset_axes = Axes(
                x_range=[0, 50, 10],
                y_range=[0, 2, 0.5],
                x_length=3,
                y_length=2,
                axis_config={"color": WHITE, "stroke_width": 2}
            )
            self.inset_axes.move_to([4.5, -2.5, 0])
            inset_title = Text("Average Regret", font_size=20, color=WHITE)
            inset_title.next_to(self.inset_axes, UP, buff=0.1)
            self.play(Create(self.inset_axes), Write(inset_title), run_time=1)
            
            # Step 9: Add average regret curve (decreasing)
            avg_regret_points = [self.inset_axes.c2p(t, 10 / (t ** 0.5)) for t in range(1, 51)]
            self.average_regret_curve = VMobject(color=GREEN, stroke_width=3)
            self.average_regret_curve.set_points_smoothly(avg_regret_points)
            self.play(Create(self.average_regret_curve), run_time=2)
            
            # Step 10: Add dashed reference line showing 1/√T decay rate
            ref_points = [self.inset_axes.c2p(t, 5 / (t ** 0.5)) for t in range(1, 51)]
            self.dashed_reference = DashedLine(
                self.inset_axes.c2p(1, 5),
                self.inset_axes.c2p(50, 5 / (50 ** 0.5)),
                color=GRAY,
                dash_length=0.1
            )
            ref_label = MathTex(r"1/\sqrt{T}", font_size=20, color=GRAY)
            ref_label.next_to(self.inset_axes.c2p(50, 5 / (50 ** 0.5)), RIGHT, buff=0.1)
            self.play(Create(self.dashed_reference), Write(ref_label), run_time=1.5)
            
            # Step 11: Highlight the decreasing nature with arrows
            highlight_dots = VGroup(*[
                Dot(self.inset_axes.c2p(t, 10 / (t ** 0.5)), radius=0.05, color=GREEN)
                for t in [5, 15, 30, 50]
            ])
            self.play(
                LaggedStart(*[Flash(d.get_center(), color=GREEN, flash_radius=0.3) for d in highlight_dots], lag_ratio=0.2),
                run_time=2
            )
            
            # Step 12: Final emphasis - pulse the yellow bound curve
            self.play(
                self.yellow_bound_curve.animate.set_stroke(width=6, opacity=0.9),
                run_time=0.5
            )
            self.play(
                self.yellow_bound_curve.animate.set_stroke(width=4, opacity=0.6),
                run_time=0.5
            )
            
            self.wait(0.5)

        # ============================================================
        # SCENE 6: Kernel Impact Comparison
        # ============================================================
        # Scene 6: Kernel Impact Comparison
        
        if self.mobjects:
            self.play(*[FadeOut(obj) for obj in self.mobjects], run_time=0.5)
        
        with self.voiceover(text="""Different kernels lead to dramatically different information gain rates. A smooth RBF kernel has bounded information gain—you learn efficiently. A linear kernel's information gain grows without bound—you need more samples to learn the same amount.""") as tracker:
            
            # Step 1: Title
            title = Text("Kernel Impact Comparison", font_size=42, color=GOLD)
            title.move_to(ZONES['title'])
            self.play(Write(title), run_time=1)
            
            # Step 2: Create vertical divider line
            self.divider = Line(start=[0, 3, 0], end=[0, -3, 0], color=WHITE, stroke_width=2)
            self.play(Create(self.divider), run_time=0.8)
            
            # Step 3: Left and right titles
            left_title = Text("RBF Kernel (Smooth)", font_size=32, color=BLUE)
            left_title.move_to([-3.5, 2.5, 0])
            right_title = Text("Linear Kernel (Rough)", font_size=32, color=RED)
            right_title.move_to([3.5, 2.5, 0])
            self.play(
                Write(left_title),
                Write(right_title),
                run_time=1.2
            )
            
            # Step 4: Create left axes for RBF
            self.left_axes = Axes(
                x_range=[0, 10, 2],
                y_range=[0, 5, 1],
                x_length=4.5,
                y_length=3.5,
                axis_config={"color": GRAY}
            )
            self.left_axes.move_to([-3.5, 0, 0])
            left_x_label = Text("Iterations", font_size=18, color=WHITE)
            left_x_label.next_to(self.left_axes, DOWN, buff=0.2)
            left_y_label = Text("Value", font_size=18, color=WHITE)
            left_y_label.next_to(self.left_axes, LEFT, buff=0.2)
            
            self.play(Create(self.left_axes), run_time=1)
            self.play(FadeIn(left_x_label), FadeIn(left_y_label), run_time=0.5)
            
            # Step 5: Create right axes for Linear
            self.right_axes = Axes(
                x_range=[0, 10, 2],
                y_range=[0, 5, 1],
                x_length=4.5,
                y_length=3.5,
                axis_config={"color": GRAY}
            )
            self.right_axes.move_to([3.5, 0, 0])
            right_x_label = Text("Iterations", font_size=18, color=WHITE)
            right_x_label.next_to(self.right_axes, DOWN, buff=0.2)
            right_y_label = Text("Value", font_size=18, color=WHITE)
            right_y_label.next_to(self.right_axes, LEFT, buff=0.2)
            
            self.play(Create(self.right_axes), run_time=1)
            self.play(FadeIn(right_x_label), FadeIn(right_y_label), run_time=0.5)
            
            # Step 6: Left information gain curve (bounded, logarithmic)
            self.left_ig_curve = self.left_axes.plot(
                lambda x: 3 * (1 - 0.85**x),
                x_range=[0, 10],
                color=BLUE,
                stroke_width=4
            )
            left_ig_label = Text("Info Gain", font_size=16, color=BLUE)
            left_ig_label.next_to(self.left_ig_curve, RIGHT, buff=0.1)
            self.play(Create(self.left_ig_curve), run_time=2)
            self.play(FadeIn(left_ig_label, shift=LEFT*0.2), run_time=0.5)
            
            # Step 7: Left regret curve (decreasing)
            self.left_regret_curve = self.left_axes.plot(
                lambda x: 4 * (0.7**x),
                x_range=[0, 10],
                color=ORANGE,
                stroke_width=4
            )
            left_regret_label = Text("Regret", font_size=16, color=ORANGE)
            left_regret_label.next_to(self.left_axes, UP, buff=0.1).shift(LEFT*1.5)
            self.play(Create(self.left_regret_curve), run_time=2)
            self.play(FadeIn(left_regret_label, shift=DOWN*0.2), run_time=0.5)
            
            # Step 8: Right information gain curve (unbounded, linear growth)
            self.right_ig_curve = self.right_axes.plot(
                lambda x: 0.45 * x,
                x_range=[0, 10],
                color=BLUE,
                stroke_width=4
            )
            right_ig_label = Text("Info Gain", font_size=16, color=BLUE)
            right_ig_label.next_to(self.right_ig_curve, RIGHT, buff=0.1)
            self.play(Create(self.right_ig_curve), run_time=2)
            self.play(FadeIn(right_ig_label, shift=LEFT*0.2), run_time=0.5)
            
            # Step 9: Right regret curve (slower decrease)
            self.right_regret_curve = self.right_axes.plot(
                lambda x: 4.5 / (x + 1),
                x_range=[0, 10],
                color=ORANGE,
                stroke_width=4
            )
            right_regret_label = Text("Regret", font_size=16, color=ORANGE)
            right_regret_label.next_to(self.right_axes, UP, buff=0.1).shift(RIGHT*1.5)
            self.play(Create(self.right_regret_curve), run_time=2)
            self.play(FadeIn(right_regret_label, shift=DOWN*0.2), run_time=0.5)
            
            # Step 10: Left RBF kernel inset (Gaussian bump)
            self.rbf_inset = Axes(
                x_range=[-2, 2, 1],
                y_range=[0, 1.2, 0.5],
                x_length=2,
                y_length=1.2,
                axis_config={"color": GRAY, "stroke_width": 1}
            )
            self.rbf_inset.move_to([-3.5, -2.2, 0])
            rbf_curve = self.rbf_inset.plot(
                lambda x: 1.0 * (2.718**(-x**2)),
                x_range=[-2, 2],
                color=GREEN,
                stroke_width=3
            )
            rbf_label = Text("RBF", font_size=14, color=GREEN)
            rbf_label.next_to(self.rbf_inset, DOWN, buff=0.1)
            self.play(Create(self.rbf_inset), run_time=0.8)
            self.play(Create(rbf_curve), FadeIn(rbf_label), run_time=1)
            
            # Step 11: Right linear kernel inset (straight line)
            self.linear_inset = Axes(
                x_range=[-2, 2, 1],
                y_range=[0, 1.2, 0.5],
                x_length=2,
                y_length=1.2,
                axis_config={"color": GRAY, "stroke_width": 1}
            )
            self.linear_inset.move_to([3.5, -2.2, 0])
            linear_curve = self.linear_inset.plot(
                lambda x: 0.5 * x + 0.6,
                x_range=[-1.5, 1.5],
                color=PURPLE,
                stroke_width=3
            )
            linear_label = Text("Linear", font_size=14, color=PURPLE)
            linear_label.next_to(self.linear_inset, DOWN, buff=0.1)
            self.play(Create(self.linear_inset), run_time=0.8)
            self.play(Create(linear_curve), FadeIn(linear_label), run_time=1)
            
            # Step 12: Add comparison arrows
            bounded_arrow = Arrow(start=[-5.5, 1, 0], end=[-5.5, 2.5, 0], color=YELLOW, buff=0.1)
            bounded_text = Text("Bounded", font_size=16, color=YELLOW)
            bounded_text.next_to(bounded_arrow, LEFT, buff=0.1)
            
            unbounded_arrow = Arrow(start=[5.5, 1, 0], end=[5.5, 3.5, 0], color=RED, buff=0.1)
            unbounded_text = Text("Unbounded", font_size=16, color=RED)
            unbounded_text.next_to(unbounded_arrow, RIGHT, buff=0.1)
            
            self.play(
                Create(bounded_arrow),
                FadeIn(bounded_text),
                run_time=1
            )
            
            # Step 13: Final comparison highlight
            self.play(
                Create(unbounded_arrow),
                FadeIn(unbounded_text),
                run_time=1
            )
            
            self.wait(0.5)

        # ============================================================
        # SCENE 7: Real-World Efficiency
        # ============================================================
        # Scene 7: Real-World Efficiency
        
        if self.mobjects:
            self.play(*[FadeOut(obj) for obj in self.mobjects], run_time=0.5)
        
        with self.voiceover(text="""This isn't just theory—it's why Bayesian optimization dominates expensive optimization problems. With an RBF kernel on a smooth function, you might need only 50 evaluations to find near-optimal solutions that random search would need thousands of attempts to discover.""") as tracker:
            
            # Step 1: Title
            title = Text("Real-World Efficiency", font_size=42, color=GOLD, weight=BOLD)
            title.move_to(ZONES['title'])
            self.play(Write(title), run_time=1)
            
            # Step 2: Create bar chart axes
            bar_chart_axes = Axes(
                x_range=[0, 4, 1],
                y_range=[0, 3000, 500],
                x_length=8,
                y_length=4,
                axis_config={"color": WHITE},
                tips=False
            )
            bar_chart_axes.move_to(ZONES['center']).shift(DOWN*0.3)
            
            # Y-axis labels
            y_labels = VGroup(*[
                Text(str(int(val)), font_size=20, color=WHITE).next_to(
                    bar_chart_axes.c2p(0, val), LEFT, buff=0.2
                )
                for val in [0, 500, 1000, 1500, 2000, 2500, 3000]
            ])
            
            self.play(Create(bar_chart_axes), Write(y_labels), run_time=1.5)
            
            # Step 3: Create three bars with different heights
            bar_width = 0.6
            bar_data = [
                ("Random", 2500, RED, 1),
                ("Grid", 1800, ORANGE, 2),
                ("Bayesian", 50, GREEN, 3)
            ]
            
            three_bars = VGroup()
            bar_labels = VGroup()
            value_labels = VGroup()
            
            for method, value, color, x_pos in bar_data:
                # Create bar as rectangle
                bar_height = (value / 3000) * 4  # Scale to axes height
                bar = Rectangle(
                    width=bar_width,
                    height=bar_height,
                    color=color,
                    fill_opacity=0.7,
                    stroke_width=2
                )
                bar_bottom = bar_chart_axes.c2p(x_pos, 0)
                bar.move_to(bar_bottom).shift(UP * bar_height / 2)
                three_bars.add(bar)
                
                # Method label below
                label = Text(method, font_size=24, color=WHITE)
                label.next_to(bar, DOWN, buff=0.3)
                bar_labels.add(label)
                
                # Value label above
                val_label = Text(str(value), font_size=22, color=color, weight=BOLD)
                val_label.next_to(bar, UP, buff=0.2)
                value_labels.add(val_label)
            
            # Step 4: Animate bars appearing
            self.play(
                LaggedStart(*[FadeIn(bar, shift=UP) for bar in three_bars], lag_ratio=0.3),
                run_time=2
            )
            
            # Step 5: Add labels
            self.play(
                Write(bar_labels),
                run_time=1.5
            )
            
            # Step 6: Add value labels
            self.play(
                LaggedStart(*[FadeIn(label, scale=0.5) for label in value_labels], lag_ratio=0.2),
                run_time=1.5
            )
            
            # Step 7: Create mini-animations above bars (icons)
            # Random: scattered dots
            random_dots = VGroup(*[
                Dot(point=three_bars[0].get_top() + UP*0.5 + RIGHT*(i*0.15-0.3) + UP*(0.1 if i%2 else 0),
                    radius=0.04, color=RED)
                for i in range(5)
            ])
            
            # Grid: grid pattern
            grid_dots = VGroup(*[
                Dot(point=three_bars[1].get_top() + UP*0.5 + RIGHT*(i%3*0.15-0.15) + UP*(i//3*0.15),
                    radius=0.04, color=ORANGE)
                for i in range(6)
            ])
            
            # Bayesian: smooth path
            bayesian_path = VMobject(color=GREEN, stroke_width=3)
            start_point = three_bars[2].get_top() + UP*0.5 + LEFT*0.3
            bayesian_path.set_points_smoothly([
                start_point,
                start_point + RIGHT*0.2 + UP*0.1,
                start_point + RIGHT*0.4 + UP*0.05,
                start_point + RIGHT*0.6
            ])
            
            mini_animations = VGroup(random_dots, grid_dots, bayesian_path)
            
            # Step 8: Show mini animations
            self.play(
                LaggedStart(*[FadeIn(d, scale=0.3) for d in random_dots], lag_ratio=0.1),
                run_time=1
            )
            self.play(
                LaggedStart(*[FadeIn(d, scale=0.3) for d in grid_dots], lag_ratio=0.08),
                run_time=1
            )
            self.play(Create(bayesian_path), run_time=1)
            
            # Step 9: Budget constraint line (dashed horizontal)
            budget_y = 100
            budget_constraint_line = DashedLine(
                start=bar_chart_axes.c2p(0.5, budget_y),
                end=bar_chart_axes.c2p(3.5, budget_y),
                color=YELLOW,
                dash_length=0.1,
                stroke_width=3
            )
            
            budget_label = Text("Budget: 100 evals", font_size=22, color=YELLOW)
            budget_label.next_to(budget_constraint_line, RIGHT, buff=0.2)
            
            # Step 10: Show budget line
            self.play(
                Create(budget_constraint_line),
                Write(budget_label),
                run_time=1.5
            )
            
            # Step 11: Highlight Bayesian bar (flash effect)
            self.play(
                three_bars[2].animate.set_fill(opacity=1).scale(1.1),
                run_time=0.8
            )
            self.play(
                Flash(three_bars[2].get_center(), color=GREEN, flash_radius=0.8),
                run_time=0.5
            )
            
            # Step 12: Add emphasis text
            emphasis = Text("50× more efficient!", font_size=32, color=GREEN, weight=BOLD)
            emphasis.next_to(three_bars[2], RIGHT, buff=0.8)
            self.play(FadeIn(emphasis, shift=LEFT*0.3), run_time=1)
            
            # STORE for next scene
            self.bar_chart = VGroup(bar_chart_axes, y_labels, three_bars, bar_labels, value_labels, mini_animations)
            self.bayesian_bar = three_bars[2]
            self.budget_line = VGroup(budget_constraint_line, budget_label)
            
            self.wait(0.5)

        # ============================================================
        # SCENE 8: Foundation for Modern ML
        # ============================================================
        # Scene 8: Foundation for Modern ML
        
        if self.mobjects:
            self.play(*[FadeOut(obj) for obj in self.mobjects], run_time=0.5)
        
        with self.voiceover(text="""This regret-information framework has become foundational across machine learning: hyperparameter tuning, neural architecture search, robotics control, drug discovery—anywhere experiments are expensive but finding optimal solutions is critical. It's the principled science behind turning costly trial-and-error into efficient optimization.""") as tracker:
            
            # Step 1: Title
            title = Text("Foundation for Modern ML", font_size=42, color=GOLD, weight=BOLD)
            title.move_to(ZONES['title'])
            self.play(Write(title), run_time=1)
            
            # Step 2: Create center circle with Bayesian Optimization
            center_circle = Circle(radius=1.2, color=BLUE, fill_opacity=0.2, stroke_width=4)
            center_circle.move_to(ZONES['center'])
            
            center_title = Text("Bayesian\nOptimization", font_size=24, color=WHITE, weight=BOLD)
            center_title.move_to(center_circle.get_center())
            
            regret_eq = MathTex(r"R_T = O(\sqrt{T})", font_size=28, color=YELLOW)
            regret_eq.next_to(center_title, DOWN, buff=0.15)
            
            self.center_node = VGroup(center_circle, center_title, regret_eq)
            self.play(FadeIn(center_circle, scale=0.5), run_time=0.8)
            self.play(Write(center_title), run_time=0.8)
            self.play(Write(regret_eq), run_time=0.8)
            
            # Step 3: Create 6 outer nodes in hexagon layout
            applications = [
                ("Hyperparameter\nTuning", ORANGE),
                ("Neural\nArchitecture", RED),
                ("Robotics\nControl", GREEN),
                ("Drug\nDiscovery", PURPLE),
                ("Materials\nScience", BLUE),
                ("AutoML\nPipelines", GOLD)
            ]
            
            radius = 3.5
            angles = [i * 60 * DEGREES for i in range(6)]
            
            outer_circles = []
            outer_labels = []
            
            for i, (label_text, color) in enumerate(applications):
                angle = angles[i]
                x = radius * np.cos(angle)
                y = radius * np.sin(angle)
                
                circle = Circle(radius=0.6, color=color, fill_opacity=0.15, stroke_width=3)
                circle.move_to([x, y, 0])
                
                label = Text(label_text, font_size=18, color=color, weight=BOLD)
                label.move_to(circle.get_center())
                
                outer_circles.append(circle)
                outer_labels.append(label)
            
            self.outer_nodes = VGroup(*[VGroup(c, l) for c, l in zip(outer_circles, outer_labels)])
            
            # Step 4: Create connecting arrows
            self.arrows = VGroup()
            for i in range(6):
                arrow = Arrow(
                    center_circle.get_center(),
                    outer_circles[i].get_center(),
                    color=GRAY,
                    buff=1.3,
                    stroke_width=2
                )
                self.arrows.add(arrow)
            
            # Step 5: Animate arrows appearing
            self.play(
                LaggedStart(*[Create(arrow) for arrow in self.arrows], lag_ratio=0.1),
                run_time=2
            )
            
            # Step 6: Animate outer nodes appearing
            self.play(
                LaggedStart(*[FadeIn(node, scale=0.5) for node in self.outer_nodes], lag_ratio=0.15),
                run_time=2.5
            )
            
            # Step 7: Add icons/symbols to outer nodes
            icons = []
            for i, circle in enumerate(outer_circles):
                if i == 0:  # Hyperparameter - grid symbol
                    icon = VGroup(*[
                        Line([circle.get_x()-0.15, circle.get_y()+0.3, 0], 
                             [circle.get_x()-0.15, circle.get_y()-0.3, 0], stroke_width=1, color=WHITE),
                        Line([circle.get_x()+0.15, circle.get_y()+0.3, 0], 
                             [circle.get_x()+0.15, circle.get_y()-0.3, 0], stroke_width=1, color=WHITE)
                    ])
                elif i == 1:  # Neural Architecture - network nodes
                    icon = VGroup(*[
                        Dot([circle.get_x()-0.15, circle.get_y()+0.25, 0], radius=0.04, color=WHITE),
                        Dot([circle.get_x()+0.15, circle.get_y()+0.25, 0], radius=0.04, color=WHITE),
                        Dot([circle.get_x(), circle.get_y()-0.25, 0], radius=0.04, color=WHITE)
                    ])
                elif i == 2:  # Robotics - arrow path
                    icon = Arrow([circle.get_x()-0.2, circle.get_y(), 0],
                                [circle.get_x()+0.2, circle.get_y(), 0],
                                buff=0, stroke_width=2, color=WHITE)
                elif i == 3:  # Drug Discovery - molecule
                    icon = RegularPolygon(n=6, radius=0.15, color=WHITE, stroke_width=2)
                    icon.move_to(circle.get_center())
                elif i == 4:  # Materials - crystal
                    icon = Square(side_length=0.25, color=WHITE, stroke_width=2)
                    icon.move_to(circle.get_center())
                else:  # AutoML - pipeline
                    icon = VGroup(*[
                        Rectangle(width=0.15, height=0.2, color=WHITE, stroke_width=1.5).shift([circle.get_x()-0.15, circle.get_y(), 0]),
                        Rectangle(width=0.15, height=0.2, color=WHITE, stroke_width=1.5).shift([circle.get_x()+0.15, circle.get_y(), 0])
                    ])
                icons.append(icon)
            
            # Step 8: Animate icons appearing
            self.play(
                LaggedStart(*[FadeIn(icon, scale=0.3) for icon in icons], lag_ratio=0.12),
                run_time=2
            )
            
            # Step 9: Pulse effect on center node
            pulse_circle = Circle(radius=1.2, color=BLUE, stroke_width=6)
            pulse_circle.move_to(center_circle.get_center())
            self.play(
                pulse_circle.animate.scale(1.3).set_stroke(opacity=0),
                run_time=1.2
            )
            self.remove(pulse_circle)
            
            # Step 10: Sequential highlight of outer nodes
            for i in range(6):
                highlight = Circle(radius=0.65, color=applications[i][1], stroke_width=5)
                highlight.move_to(outer_circles[i].get_center())
                self.play(
                    FadeIn(highlight, scale=0.9),
                    FadeOut(highlight, scale=1.1),
                    run_time=0.4
                )
            
            # Step 11: Add glow effects to all nodes
            glow_circles = VGroup()
            for circle in outer_circles:
                glow = Circle(radius=0.7, color=YELLOW, stroke_width=2, stroke_opacity=0.5)
                glow.move_to(circle.get_center())
                glow_circles.add(glow)
            
            self.play(
                LaggedStart(*[Create(glow) for glow in glow_circles], lag_ratio=0.08),
                run_time=1.5
            )
            
            # Step 12: Final emphasis - all elements together
            self.full_network = VGroup(
                self.center_node,
                self.arrows,
                self.outer_nodes,
                VGroup(*icons),
                glow_circles
            )
            
            self.play(
                self.full_network.animate.scale(1.05),
                run_time=0.5
            )
            self.play(
                self.full_network.animate.scale(1/1.05),
                run_time=0.5
            )
            
            self.wait(0.5)
