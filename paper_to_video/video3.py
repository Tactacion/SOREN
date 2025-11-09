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

class Video3(VoiceoverScene):
    """
    How It Works
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
        # SCENE 1: The Regret Concept
        # ============================================================
        # Scene 1: The Regret Concept
        
        if self.mobjects:
            self.play(*[FadeOut(obj) for obj in self.mobjects], run_time=0.5)
        
        with self.voiceover(text="""Let's understand what we mean by 'regret' in optimization. Every time you pick a point to sample, there's a gap between the reward you got and the best possible reward you could have gotten. That gap is your instantaneous regret.""") as tracker:
            
            # Step 1: Title
            title = Text("The Regret Concept", font_size=42, color=GOLD)
            title.move_to(ZONES['title'])
            self.play(Write(title), run_time=1)
            
            # Step 2: Create 2D coordinate axes
            self.axes = Axes(
                x_range=[0, 10, 1], 
                y_range=[0, 10, 1], 
                x_length=8, 
                y_length=5,
                axis_config={"color": WHITE}
            )
            self.axes.move_to(ZONES['center'])
            
            # Add axis labels
            x_label = Text("Time t", font_size=28, color=WHITE)
            x_label.next_to(self.axes.x_axis, DOWN, buff=0.3)
            y_label = Text("Reward", font_size=28, color=WHITE)
            y_label.next_to(self.axes.y_axis, LEFT, buff=0.3)
            
            self.play(Create(self.axes), run_time=1.5)
            self.play(FadeIn(x_label), FadeIn(y_label), run_time=0.8)
            
            # Step 3: Create horizontal dashed gold line at y=8
            best_start = self.axes.c2p(0, 8)
            best_end = self.axes.c2p(10, 8)
            self.best_line = DashedLine(best_start, best_end, color=GOLD, dash_length=0.15, stroke_width=4)
            self.play(Create(self.best_line), run_time=1.5)
            
            # Step 4: Add label for best possible reward
            best_label = Text("Best Possible Reward", font_size=24, color=GOLD)
            best_label.next_to(self.best_line, UP, buff=0.2)
            self.play(Write(best_label), run_time=1)
            
            # Step 5: Create 10 blue dots at random heights (y=3 to 7)
            dot_y_values = [5, 4, 6, 3.5, 5.5, 4.5, 6.5, 4, 5, 3]
            self.blue_dots = VGroup(*[
                Dot(self.axes.c2p(i + 0.5, dot_y_values[i]), radius=0.12, color=BLUE)
                for i in range(10)
            ])
            
            # Step 6: Animate dots appearing one by one
            self.play(
                LaggedStart(*[FadeIn(d, scale=0.5) for d in self.blue_dots], lag_ratio=0.15),
                run_time=2.5
            )
            
            # Step 7: Create vertical red line segments (regret segments)
            self.regret_segments = VGroup(*[
                Line(
                    self.blue_dots[i].get_center(),
                    self.axes.c2p(i + 0.5, 8),
                    color=RED,
                    stroke_width=3
                )
                for i in range(10)
            ])
            
            # Step 8: Animate regret segments appearing
            self.play(
                LaggedStart(*[Create(seg) for seg in self.regret_segments], lag_ratio=0.12),
                run_time=2.5
            )
            
            # Step 9: Add label for instantaneous regret with arrow
            regret_label = Text("Instantaneous\nRegret", font_size=22, color=RED)
            regret_label.move_to(self.axes.c2p(7, 5))
            
            arrow_to_segment = Arrow(
                regret_label.get_left() + [0.2, 0, 0],
                self.regret_segments[4].get_center(),
                color=RED,
                buff=0.1,
                stroke_width=3
            )
            
            self.play(Write(regret_label), run_time=1)
            
            # Step 10: Animate arrow pointing to regret segment
            self.play(Create(arrow_to_segment), run_time=1)
            
            # Emphasize the labeled segment with flash
            self.play(
                Flash(self.regret_segments[4].get_center(), color=RED, flash_radius=0.4),
                run_time=0.8
            )
            
            self.wait(0.5)

        # ============================================================
        # SCENE 2: Cumulative Regret Visualization
        # ============================================================
        # Scene 2: Cumulative Regret Visualization
        
        # Continue from previous scene with self.axes, self.best_line, self.blue_dots, self.regret_segments
        
        with self.voiceover(text="""Cumulative regret is just the sum of all these gaps over time. We can visualize this as the area between what we got and what was optimal. The bigger this area grows, the worse our algorithm is performing.""") as tracker:
            
            # Step 1: Title
            title = Text("Cumulative Regret Visualization", font_size=42, color=GOLD)
            title.move_to(ZONES['title'])
            self.play(Write(title), run_time=1)
            
            # Step 2: Create red fill area (polygon between gold line and blue points)
            # Get points for the polygon - trace from left to right along best line, then back along blue dots
            x_vals = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
            
            # Top edge: points along the gold best line (y=8)
            top_points = [self.axes.c2p(x, 8) for x in x_vals]
            
            # Bottom edge: points along blue dots (rewards: 6,5,7,6,8,7,8,7,8,8)
            rewards = [6, 5, 7, 6, 8, 7, 8, 7, 8, 8]
            bottom_points = [self.axes.c2p(x_vals[i], rewards[i]) for i in range(len(x_vals))]
            
            # Create polygon by going along top, then back along bottom (reversed)
            fill_points = top_points + bottom_points[::-1]
            
            self.red_fill_area = Polygon(*fill_points, color=RED, fill_opacity=0.3, stroke_width=0)
            
            # Step 3: Animate the fill area appearing
            self.play(FadeIn(self.red_fill_area, scale=1.0), run_time=2)
            
            # Step 4: Highlight the fill area with a brief flash effect
            self.play(
                self.red_fill_area.animate.set_fill(opacity=0.5),
                run_time=0.5
            )
            self.play(
                self.red_fill_area.animate.set_fill(opacity=0.3),
                run_time=0.5
            )
            
            # Step 5: Create secondary axes below main plot for cumulative regret
            self.secondary_axes = Axes(
                x_range=[0, 10, 1],
                y_range=[0, 30, 10],
                x_length=8,
                y_length=3,
                axis_config={"color": GRAY}
            )
            self.secondary_axes.move_to(ZONES['bottom'])
            self.secondary_axes.shift(UP * 0.5)
            
            self.play(Create(self.secondary_axes), run_time=1.5)
            
            # Step 6: Add y-axis label for cumulative regret
            y_label = Text("Cumulative Regret", font_size=28, color=PURPLE)
            y_label.next_to(self.secondary_axes, LEFT, buff=0.3)
            y_label.rotate(90 * DEGREES)
            self.play(Write(y_label), run_time=1)
            
            # Step 7: Calculate cumulative regret values
            # Regret at each step = 8 - reward
            regrets = [8 - r for r in rewards]
            cumulative_regrets = []
            total = 0
            for r in regrets:
                total += r
                cumulative_regrets.append(total)
            
            # Step 8: Create points for the cumulative regret curve
            cumulative_points = [
                self.secondary_axes.c2p(x_vals[i], cumulative_regrets[i])
                for i in range(len(x_vals))
            ]
            
            # Step 9: Create purple cumulative curve using smooth path
            self.purple_curve = VMobject(color=PURPLE, stroke_width=4)
            self.purple_curve.set_points_smoothly([self.secondary_axes.c2p(0, 0)] + cumulative_points)
            
            self.play(Create(self.purple_curve), run_time=3)
            
            # Step 10: Add dots at each cumulative regret point
            cumulative_dots = VGroup(*[
                Dot(cumulative_points[i], radius=0.08, color=PURPLE)
                for i in range(len(cumulative_points))
            ])
            
            self.play(
                LaggedStart(*[FadeIn(d, scale=0.5) for d in cumulative_dots], lag_ratio=0.1),
                run_time=2
            )
            
            # Step 11: Add annotation showing final cumulative regret value
            final_value = cumulative_regrets[-1]
            final_label = MathTex(f"\\text{{Total: }}{int(final_value)}", font_size=32, color=PURPLE)
            final_label.next_to(cumulative_dots[-1], RIGHT, buff=0.3)
            self.play(Write(final_label), run_time=1)
            
            # Step 12: Create vertical sweep line to show connection between plots
            sweep_line = DashedLine(
                self.axes.c2p(5, 0),
                self.secondary_axes.c2p(5, 30),
                color=YELLOW,
                dash_length=0.1,
                stroke_width=2
            )
            
            self.play(Create(sweep_line), run_time=1)
            self.play(FadeOut(sweep_line), run_time=0.5)
            
            # STORE for next scene
            self.title = title
            
            self.wait(0.5)

        # ============================================================
        # SCENE 3: Linear vs Sublinear Growth
        # ============================================================
        # Scene 3: Linear vs Sublinear Growth
        
        if self.mobjects:
            self.play(*[FadeOut(obj) for obj in self.mobjects], run_time=0.5)
        
        with self.voiceover(text="""Here's the key insight: if cumulative regret grows linearly with time, you're not learning anything. But if it grows sublinearly—like square root of T or log of T—then your average regret per round approaches zero. You're getting smarter!""") as tracker:
            
            # Step 1: Title
            title = Text("Linear vs Sublinear Growth", font_size=42, color=GOLD)
            title.move_to(ZONES['title'])
            self.play(Write(title), run_time=1)
            
            # Step 2: Create axes
            self.axes = Axes(
                x_range=[0, 100, 20],
                y_range=[0, 100, 20],
                x_length=8,
                y_length=5,
                axis_config={"color": WHITE}
            )
            self.axes.move_to(ZONES['center']).shift(DOWN*0.3)
            
            x_label = Text("Time T", font_size=24, color=WHITE)
            x_label.next_to(self.axes.x_axis, DOWN, buff=0.3)
            
            y_label = Text("Cumulative Regret", font_size=24, color=WHITE)
            y_label.next_to(self.axes.y_axis, LEFT, buff=0.3)
            
            self.play(Create(self.axes), Write(x_label), Write(y_label), run_time=1.5)
            
            # Step 3: Create red linear line O(T)
            self.red_line = self.axes.plot(lambda x: x, x_range=[0, 100], color=RED, stroke_width=4)
            red_label = Text("Linear: O(T) - BAD", font_size=28, color=RED, weight=BOLD)
            red_label.next_to(self.axes.c2p(70, 70), UP+RIGHT, buff=0.2)
            
            self.play(Create(self.red_line), run_time=2)
            self.play(FadeIn(red_label, shift=DOWN*0.2), run_time=0.8)
            
            # Step 4: Create blue sqrt curve O(√T)
            self.blue_curve = self.axes.plot(lambda x: 3 * (x ** 0.5), x_range=[0, 100], color=BLUE, stroke_width=4)
            blue_label = Text("Sublinear: O(√T) - GOOD", font_size=28, color=BLUE, weight=BOLD)
            blue_label.next_to(self.axes.c2p(70, 30), UP, buff=0.2)
            
            self.play(Create(self.blue_curve), run_time=2)
            self.play(FadeIn(blue_label, shift=DOWN*0.2), run_time=0.8)
            
            # Step 5: Create green log curve O(log T)
            self.green_curve = self.axes.plot(lambda x: 3.25 * (x ** 0.01) if x > 0 else 0, x_range=[1, 100], color=GREEN, stroke_width=4)
            green_label = Text("Sublinear: O(log T) - BETTER", font_size=28, color=GREEN, weight=BOLD)
            green_label.next_to(self.axes.c2p(70, 15), UP, buff=0.2)
            
            self.play(Create(self.green_curve), run_time=2)
            self.play(FadeIn(green_label, shift=DOWN*0.2), run_time=0.8)
            
            # Step 6: Highlight the divergence with dots
            time_points = [20, 40, 60, 80, 100]
            red_dots = VGroup(*[
                Dot(self.axes.c2p(t, t), radius=0.08, color=RED)
                for t in time_points
            ])
            blue_dots = VGroup(*[
                Dot(self.axes.c2p(t, 3 * (t ** 0.5)), radius=0.08, color=BLUE)
                for t in time_points
            ])
            green_dots = VGroup(*[
                Dot(self.axes.c2p(t, 3.25 * (t ** 0.01)), radius=0.08, color=GREEN)
                for t in time_points
            ])
            
            self.play(
                LaggedStart(*[FadeIn(d, scale=0.5) for d in red_dots], lag_ratio=0.1),
                LaggedStart(*[FadeIn(d, scale=0.5) for d in blue_dots], lag_ratio=0.1),
                LaggedStart(*[FadeIn(d, scale=0.5) for d in green_dots], lag_ratio=0.1),
                run_time=2
            )
            
            # Step 7: Add dashed line showing average regret approaching zero
            dashed_line = DashedLine(
                start=self.axes.c2p(70, 1),
                end=self.axes.c2p(100, 1),
                color=YELLOW,
                dash_length=0.1,
                stroke_width=3
            )
            
            average_label = Text("Average regret → 0", font_size=24, color=YELLOW)
            average_label.next_to(dashed_line, RIGHT, buff=0.2)
            
            self.play(Create(dashed_line), Write(average_label), run_time=1.5)
            
            # Step 8: Flash the good curves
            self.play(
                Flash(self.axes.c2p(50, 3 * (50 ** 0.5)), color=BLUE, flash_radius=0.5),
                Flash(self.axes.c2p(50, 3.25 * (50 ** 0.01)), color=GREEN, flash_radius=0.5),
                run_time=1
            )
            
            self.wait(0.5)

        # ============================================================
        # SCENE 4: Why Sublinear Matters
        # ============================================================
        # Scene 4: Why Sublinear Matters
        
        if self.mobjects:
            self.play(*[FadeOut(obj) for obj in self.mobjects], run_time=0.5)
        
        with self.voiceover(text="""Think about what this means practically. With sublinear regret, even though you're accumulating some regret, if you divide by the number of rounds, you're approaching optimal performance. The algorithm is converging to always picking the best option.""") as tracker:
            
            # Step 1: Title
            title = Text("Why Sublinear Matters", font_size=42, color=GOLD, weight=BOLD)
            title.move_to(ZONES['title'])
            self.play(Write(title), run_time=1)
            
            # Step 2: Create left panel axes (cumulative regret)
            self.left_axes = Axes(
                x_range=[0, 100, 20],
                y_range=[0, 20, 5],
                x_length=5,
                y_length=4,
                axis_config={"color": WHITE}
            )
            self.left_axes.move_to(ZONES['left'])
            
            left_title = Text("Cumulative Regret", font_size=24, color=BLUE)
            left_title.next_to(self.left_axes, UP, buff=0.3)
            
            self.play(Create(self.left_axes), Write(left_title), run_time=1.5)
            
            # Step 3: Create right panel axes (average regret)
            self.right_axes = Axes(
                x_range=[0, 100, 20],
                y_range=[0, 2, 0.5],
                x_length=5,
                y_length=4,
                axis_config={"color": WHITE}
            )
            self.right_axes.move_to(ZONES['right'])
            
            right_title = Text("Average Regret", font_size=24, color=GREEN)
            right_title.next_to(self.right_axes, UP, buff=0.3)
            
            self.play(Create(self.right_axes), Write(right_title), run_time=1.5)
            
            # Step 4: Draw left curve (sqrt(T) function)
            self.left_curve = self.left_axes.plot(
                lambda x: 2 * (x ** 0.5) if x > 0 else 0,
                x_range=[0.1, 100],
                color=BLUE,
                stroke_width=4
            )
            self.play(Create(self.left_curve), run_time=2)
            
            # Step 5: Add label for left curve
            left_label = MathTex(r"\sqrt{T}", font_size=32, color=BLUE)
            left_label.next_to(self.left_curve.get_end(), RIGHT, buff=0.2)
            self.play(FadeIn(left_label, shift=LEFT*0.3), run_time=0.8)
            
            # Step 6: Draw right curve (1/sqrt(T) function)
            self.right_curve = self.right_axes.plot(
                lambda x: 20 / (x ** 0.5) if x > 0 else 2,
                x_range=[1, 100],
                color=GREEN,
                stroke_width=4
            )
            self.play(Create(self.right_curve), run_time=2)
            
            # Step 7: Add label for right curve
            right_label = MathTex(r"\frac{1}{\sqrt{T}}", font_size=32, color=GREEN)
            right_label.next_to(self.right_curve.get_end(), RIGHT, buff=0.2)
            self.play(FadeIn(right_label, shift=LEFT*0.3), run_time=0.8)
            
            # Step 8: Draw gold horizontal line at y=0 on right panel
            self.optimal_line = Line(
                start=self.right_axes.c2p(0, 0),
                end=self.right_axes.c2p(100, 0),
                color=GOLD,
                stroke_width=5
            )
            self.play(Create(self.optimal_line), run_time=1.5)
            
            # Step 9: Add optimal performance label
            optimal_label = Text("Optimal Performance", font_size=20, color=GOLD)
            optimal_label.next_to(self.optimal_line, DOWN, buff=0.2)
            self.play(FadeIn(optimal_label, shift=UP*0.2), run_time=0.8)
            
            # Step 10: Create division arrows connecting panels
            arrow1 = Arrow(
                start=self.left_axes.c2p(25, 10),
                end=self.right_axes.c2p(25, 0.8),
                color=ORANGE,
                buff=0.2,
                stroke_width=3
            )
            arrow2 = Arrow(
                start=self.left_axes.c2p(50, 14),
                end=self.right_axes.c2p(50, 0.56),
                color=ORANGE,
                buff=0.2,
                stroke_width=3
            )
            arrow3 = Arrow(
                start=self.left_axes.c2p(75, 17.3),
                end=self.right_axes.c2p(75, 0.46),
                color=ORANGE,
                buff=0.2,
                stroke_width=3
            )
            
            division_arrows = VGroup(arrow1, arrow2, arrow3)
            
            self.play(
                LaggedStart(*[Create(a) for a in division_arrows], lag_ratio=0.3),
                run_time=2
            )
            
            # Step 11: Add division symbol labels
            div_label1 = MathTex(r"\div T", font_size=24, color=ORANGE)
            div_label1.move_to((arrow1.get_start() + arrow1.get_end()) / 2 + UP*0.3)
            
            div_label2 = MathTex(r"\div T", font_size=24, color=ORANGE)
            div_label2.move_to((arrow2.get_start() + arrow2.get_end()) / 2 + UP*0.3)
            
            div_label3 = MathTex(r"\div T", font_size=24, color=ORANGE)
            div_label3.move_to((arrow3.get_start() + arrow3.get_end()) / 2 + UP*0.3)
            
            div_labels = VGroup(div_label1, div_label2, div_label3)
            
            self.play(
                LaggedStart(*[FadeIn(l, scale=0.5) for l in div_labels], lag_ratio=0.2),
                run_time=1.5
            )
            
            # Step 12: Highlight convergence with dots on right curve
            convergence_dots = VGroup(*[
                Dot(self.right_axes.c2p(t, 20 / (t ** 0.5)), radius=0.06, color=YELLOW)
                for t in [10, 25, 50, 75, 100]
            ])
            
            self.play(
                LaggedStart(*[Flash(d.get_center(), color=YELLOW, flash_radius=0.3) for d in convergence_dots], lag_ratio=0.15),
                LaggedStart(*[FadeIn(d, scale=0.5) for d in convergence_dots], lag_ratio=0.15),
                run_time=2
            )
            
            self.wait(0.5)

        # ============================================================
        # SCENE 5: Kernel Smoothness Introduction
        # ============================================================
        # Scene 5: Kernel Smoothness Introduction
        
        if self.mobjects:
            self.play(*[FadeOut(obj) for obj in self.mobjects], run_time=0.5)
        
        with self.voiceover(text="""Now, why do some algorithms achieve better regret bounds than others? It comes down to smoothness assumptions. Different kernels in Gaussian Processes encode different beliefs about how smooth the function is, and smoother functions are fundamentally easier to optimize.""") as tracker:
            
            # Step 1: Title
            title = Text("Kernel Smoothness Introduction", font_size=42, color=GOLD)
            title.move_to(ZONES['title'])
            self.play(Write(title), run_time=1)
            
            # Step 2: Create three panel titles
            linear_title = Text("Linear Kernel", font_size=28, color=GRAY)
            matern_title = Text("Matérn Kernel", font_size=28, color=BLUE)
            rbf_title = Text("RBF/Squared Exp", font_size=28, color=GREEN)
            
            linear_title.move_to([-4, 2.2, 0])
            matern_title.move_to([0, 2.2, 0])
            rbf_title.move_to([4, 2.2, 0])
            
            self.play(
                LaggedStart(*[Write(t) for t in [linear_title, matern_title, rbf_title]], 
                            lag_ratio=0.3),
                run_time=1.5
            )
            
            # Step 3: Create three sets of axes
            linear_axes = Axes(x_range=[0, 10, 2], y_range=[0, 5, 1], 
                               x_length=3.5, y_length=2.5, 
                               axis_config={"include_tip": False})
            matern_axes = Axes(x_range=[0, 10, 2], y_range=[0, 5, 1], 
                               x_length=3.5, y_length=2.5,
                               axis_config={"include_tip": False})
            rbf_axes = Axes(x_range=[0, 10, 2], y_range=[0, 5, 1], 
                            x_length=3.5, y_length=2.5,
                            axis_config={"include_tip": False})
            
            linear_axes.move_to([-4, 0.5, 0])
            matern_axes.move_to([0, 0.5, 0])
            rbf_axes.move_to([4, 0.5, 0])
            
            self.play(
                LaggedStart(*[Create(a) for a in [linear_axes, matern_axes, rbf_axes]], 
                            lag_ratio=0.2),
                run_time=2
            )
            
            # Step 4: Create background rectangles for panels
            linear_bg = Rectangle(width=4, height=4.5, color=GRAY, stroke_width=2, fill_opacity=0.05)
            matern_bg = Rectangle(width=4, height=4.5, color=BLUE, stroke_width=2, fill_opacity=0.05)
            rbf_bg = Rectangle(width=4, height=4.5, color=GREEN, stroke_width=2, fill_opacity=0.05)
            
            linear_bg.move_to([-4, 0.3, 0])
            matern_bg.move_to([0, 0.3, 0])
            rbf_bg.move_to([4, 0.3, 0])
            
            self.play(
                LaggedStart(*[Create(bg) for bg in [linear_bg, matern_bg, rbf_bg]], 
                            lag_ratio=0.15),
                run_time=1.5
            )
            
            # Step 5: Create linear kernel function (jagged piecewise linear)
            linear_points = [
                linear_axes.c2p(0, 1),
                linear_axes.c2p(1.5, 3),
                linear_axes.c2p(2.5, 1.5),
                linear_axes.c2p(4, 3.5),
                linear_axes.c2p(5, 2),
                linear_axes.c2p(6.5, 4),
                linear_axes.c2p(7.5, 2.5),
                linear_axes.c2p(9, 3.8),
                linear_axes.c2p(10, 2.5)
            ]
            
            linear_path = VMobject(color=GRAY, stroke_width=4)
            linear_path.set_points_as_corners(linear_points)
            
            self.play(Create(linear_path), run_time=2)
            
            # Step 6: Create Matérn kernel function (moderately smooth)
            matern_points = [
                matern_axes.c2p(0, 1),
                matern_axes.c2p(1, 2),
                matern_axes.c2p(2.5, 3),
                matern_axes.c2p(4, 2.5),
                matern_axes.c2p(6, 3.5),
                matern_axes.c2p(8, 2.8),
                matern_axes.c2p(10, 3.2)
            ]
            
            matern_path = VMobject(color=BLUE, stroke_width=4)
            matern_path.set_points_smoothly(matern_points)
            
            self.play(Create(matern_path), run_time=2)
            
            # Step 7: Create RBF kernel function (perfectly smooth)
            rbf_curve = rbf_axes.plot(
                lambda x: 2.5 + 1.2 * np.sin(0.6 * x) + 0.3 * np.cos(1.2 * x),
                x_range=[0, 10],
                color=GREEN,
                stroke_width=4
            )
            
            self.play(Create(rbf_curve), run_time=2)
            
            # Step 8: Add dots to emphasize corners on linear function
            linear_dots = VGroup(*[
                Dot(point, radius=0.06, color=GRAY)
                for point in linear_points
            ])
            
            self.play(
                LaggedStart(*[FadeIn(d, scale=0.5) for d in linear_dots], lag_ratio=0.08),
                run_time=1.5
            )
            
            # Step 9: Create regret bound labels
            linear_regret = MathTex(r"O(T^{2/3})", font_size=32, color=GRAY)
            matern_regret = MathTex(r"O(\sqrt{T} \log T)", font_size=32, color=BLUE)
            rbf_regret = MathTex(r"O(\sqrt{T})", font_size=32, color=GREEN)
            
            linear_regret.next_to(linear_axes, DOWN, buff=0.4)
            matern_regret.next_to(matern_axes, DOWN, buff=0.4)
            rbf_regret.next_to(rbf_axes, DOWN, buff=0.4)
            
            self.play(
                LaggedStart(*[Write(r) for r in [linear_regret, matern_regret, rbf_regret]], 
                            lag_ratio=0.25),
                run_time=2
            )
            
            # Step 10: Add "Regret Bound:" labels above the regret formulas
            linear_label = Text("Regret Bound:", font_size=20, color=GRAY)
            matern_label = Text("Regret Bound:", font_size=20, color=BLUE)
            rbf_label = Text("Regret Bound:", font_size=20, color=GREEN)
            
            linear_label.next_to(linear_regret, UP, buff=0.15)
            matern_label.next_to(matern_regret, UP, buff=0.15)
            rbf_label.next_to(rbf_regret, UP, buff=0.15)
            
            self.play(
                LaggedStart(*[FadeIn(l, shift=DOWN*0.2) for l in [linear_label, matern_label, rbf_label]], 
                            lag_ratio=0.2),
                run_time=1.5
            )
            
            # Step 11: Create VGroups for each panel
            self.linear_panel = VGroup(linear_bg, linear_title, linear_axes, linear_path, linear_dots, linear_label, linear_regret)
            self.matern_panel = VGroup(matern_bg, matern_title, matern_axes, matern_path, matern_label, matern_regret)
            self.rbf_panel = VGroup(rbf_bg, rbf_title, rbf_axes, rbf_curve, rbf_label, rbf_regret)
            
            # Step 12: Create overall group and highlight with subtle animation
            self.all_panels_group = VGroup(self.linear_panel, self.matern_panel, self.rbf_panel)
            
            # Subtle pulse effect to emphasize the comparison
            self.play(
                self.all_panels_group.animate.scale(1.05),
                run_time=0.4
            )
            self.play(
                self.all_panels_group.animate.scale(1/1.05),
                run_time=0.4
            )
            
            self.wait(0.5)

        # ============================================================
        # SCENE 6: Correlation Decay
        # ============================================================
        # Scene 6: Correlation Decay
        
        if self.mobjects:
            self.play(*[FadeOut(obj) for obj in self.mobjects], run_time=0.5)
        
        with self.voiceover(text="""Here's the intuition: kernels define how correlated nearby points are. With a smooth kernel, knowing the value at one point tells you a lot about nearby points. With a rough kernel, each point is more independent, so you need more samples to learn the function.""") as tracker:
            
            # Step 1: Title
            title = Text("Correlation Decay", font_size=42, color=GOLD)
            title.move_to(ZONES['title'])
            self.play(Write(title), run_time=1)
            
            # Step 2: Create heatmap grid (10x10)
            grid_size = 10
            cell_size = 0.5
            heatmap_grid = VGroup()
            
            # Center point will be at (5, 5) in grid coordinates
            center_i, center_j = 5, 5
            
            # Create grid of squares with correlation values
            for i in range(grid_size):
                for j in range(grid_size):
                    # Calculate distance from center
                    dist = ((i - center_i)**2 + (j - center_j)**2)**0.5
                    # RBF kernel correlation (smooth decay)
                    correlation = 0.9 ** (dist * 0.8)
                    
                    # Map correlation to color (high=YELLOW, low=BLUE)
                    if correlation > 0.7:
                        color = YELLOW
                    elif correlation > 0.4:
                        color = ORANGE
                    elif correlation > 0.2:
                        color = RED
                    else:
                        color = BLUE
                    
                    square = Square(side_length=cell_size, color=color, fill_opacity=correlation)
                    square.move_to([
                        (i - grid_size/2) * cell_size,
                        (j - grid_size/2) * cell_size,
                        0
                    ])
                    heatmap_grid.add(square)
            
            heatmap_grid.move_to(ZONES['center'])
            
            # Step 3: Animate grid creation
            self.play(
                LaggedStart(*[FadeIn(sq, scale=0.5) for sq in heatmap_grid], lag_ratio=0.01),
                run_time=2
            )
            
            # Step 4: Add center dot
            center_dot = Dot(point=heatmap_grid[center_i * grid_size + center_j].get_center(), 
                             radius=0.15, color=WHITE)
            self.play(FadeIn(center_dot, scale=2), Flash(center_dot.get_center(), color=WHITE), run_time=0.8)
            
            # Step 5: Add axis labels
            x_label = Text("Distance →", font_size=24, color=WHITE)
            x_label.next_to(heatmap_grid, DOWN, buff=0.3)
            y_label = Text("Correlation", font_size=24, color=WHITE)
            y_label.next_to(heatmap_grid, LEFT, buff=0.3)
            axis_labels = VGroup(x_label, y_label)
            self.play(Write(axis_labels), run_time=1)
            
            # Step 6: Add colorbar legend
            colorbar = VGroup()
            bar_height = 2
            bar_width = 0.3
            colors_list = [YELLOW, ORANGE, RED, BLUE]
            labels_list = ["1.0", "0.7", "0.4", "0.0"]
            
            for i, (col, lbl) in enumerate(zip(colors_list, labels_list)):
                rect = Rectangle(width=bar_width, height=bar_height/4, color=col, fill_opacity=0.8)
                rect.move_to([4, 1.5 - i * bar_height/4, 0])
                label = Text(lbl, font_size=18, color=WHITE)
                label.next_to(rect, RIGHT, buff=0.1)
                colorbar.add(rect, label)
            
            self.play(FadeIn(colorbar, shift=LEFT*0.5), run_time=1)
            
            # Step 7: Highlight correlation pattern with arrows
            arrows = VGroup()
            for direction in [RIGHT, LEFT, UP, DOWN]:
                arrow = Arrow(
                    center_dot.get_center(),
                    center_dot.get_center() + direction * 1.5,
                    color=WHITE,
                    buff=0.2,
                    stroke_width=3
                )
                arrows.add(arrow)
            
            self.play(
                LaggedStart(*[Create(a) for a in arrows], lag_ratio=0.1),
                run_time=1.5
            )
            
            # Step 8: Fade arrows and show smooth kernel label
            self.play(FadeOut(arrows), run_time=0.5)
            
            smooth_label = Text("Smooth Kernel (RBF)", font_size=28, color=YELLOW)
            smooth_label.next_to(heatmap_grid, UP, buff=0.3)
            self.play(Write(smooth_label), run_time=1)
            
            self.wait(1)
            
            # Step 9: Transform to rough kernel (Matérn with low smoothness)
            rough_grid = VGroup()
            for i in range(grid_size):
                for j in range(grid_size):
                    dist = ((i - center_i)**2 + (j - center_j)**2)**0.5
                    # Matérn kernel with rapid decay
                    correlation = 0.5 ** (dist * 1.5) if dist < 3 else 0.1
                    
                    if correlation > 0.7:
                        color = YELLOW
                    elif correlation > 0.4:
                        color = ORANGE
                    elif correlation > 0.2:
                        color = RED
                    else:
                        color = BLUE
                    
                    square = Square(side_length=cell_size, color=color, fill_opacity=max(correlation, 0.3))
                    square.move_to([
                        (i - grid_size/2) * cell_size,
                        (j - grid_size/2) * cell_size,
                        0
                    ])
                    rough_grid.add(square)
            
            rough_grid.move_to(ZONES['center'])
            
            rough_label = Text("Rough Kernel (Matérn)", font_size=28, color=RED)
            rough_label.next_to(rough_grid, UP, buff=0.3)
            
            # Step 10: Transform to rough kernel
            self.play(
                Transform(heatmap_grid, rough_grid),
                Transform(smooth_label, rough_label),
                run_time=2
            )
            
            self.wait(1)
            
            # Step 11: Add annotation about independence
            annotation = Text("More independent points\n→ Need more samples", 
                             font_size=24, color=WHITE)
            annotation.move_to(ZONES['bottom'])
            self.play(FadeIn(annotation, shift=UP*0.3), run_time=1)
            
            self.wait(1)
            
            # Step 12: Final emphasis with flash
            self.play(
                Flash(center_dot.get_center(), color=RED, flash_radius=1),
                center_dot.animate.scale(1.3),
                run_time=0.8
            )
            
            # STORE for next scene
            self.heatmap_grid = heatmap_grid
            self.center_dot = center_dot
            self.colorbar = colorbar
            self.axis_labels = axis_labels
            
            self.wait(0.5)

        # ============================================================
        # SCENE 7: Sampling Efficiency
        # ============================================================
        # Scene 7: Sampling Efficiency
        
        if self.mobjects:
            self.play(*[FadeOut(obj) for obj in self.mobjects], run_time=0.5)
        
        with self.voiceover(text="""Watch what happens when we sample these functions. With the smooth RBF kernel, each sample gives us information about a wider region, so we converge faster. With the linear kernel, each sample is more localized, requiring more exploration.""") as tracker:
            
            # Step 1: Title
            title = Text("Sampling Efficiency", font_size=42, color=GOLD)
            title.move_to(ZONES['title'])
            self.play(Write(title), run_time=1)
            
            # Step 2: Create three panel axes (vertically stacked)
            panel_height = 1.8
            panel_width = 10
            
            axes_rbf = Axes(x_range=[0, 10, 2], y_range=[-2, 2, 1], 
                            x_length=panel_width, y_length=panel_height,
                            axis_config={"include_tip": False})
            axes_matern = Axes(x_range=[0, 10, 2], y_range=[-2, 2, 1], 
                               x_length=panel_width, y_length=panel_height,
                               axis_config={"include_tip": False})
            axes_linear = Axes(x_range=[0, 10, 2], y_range=[-2, 2, 1], 
                               x_length=panel_width, y_length=panel_height,
                               axis_config={"include_tip": False})
            
            axes_rbf.move_to([0, 1.5, 0])
            axes_matern.move_to([0, -0.5, 0])
            axes_linear.move_to([0, -2.5, 0])
            
            self.panel_axes = VGroup(axes_rbf, axes_matern, axes_linear)
            
            # Step 3: Create panel labels
            label_rbf = Text("RBF Kernel", font_size=24, color=BLUE)
            label_rbf.next_to(axes_rbf, LEFT, buff=0.3)
            
            label_matern = Text("Matérn Kernel", font_size=24, color=GREEN)
            label_matern.next_to(axes_matern, LEFT, buff=0.3)
            
            label_linear = Text("Linear Kernel", font_size=24, color=ORANGE)
            label_linear.next_to(axes_linear, LEFT, buff=0.3)
            
            panel_labels = VGroup(label_rbf, label_matern, label_linear)
            
            self.play(
                LaggedStart(*[Create(ax) for ax in self.panel_axes], lag_ratio=0.2),
                LaggedStart(*[Write(lbl) for lbl in panel_labels], lag_ratio=0.2),
                run_time=2
            )
            
            # Step 4: Create true functions (thin black curves)
            true_func_rbf = axes_rbf.plot(lambda x: 0.8 * (x - 5)**2 / 12 - 0.5, 
                                           color=GRAY, stroke_width=2)
            true_func_matern = axes_matern.plot(lambda x: 0.6 * (x - 5)**2 / 12 - 0.3, 
                                                color=GRAY, stroke_width=2)
            true_func_linear = axes_linear.plot(lambda x: 0.4 * (x - 5)**2 / 12 - 0.2, 
                                                color=GRAY, stroke_width=2)
            
            self.true_functions = VGroup(true_func_rbf, true_func_matern, true_func_linear)
            
            self.play(
                LaggedStart(*[Create(f) for f in self.true_functions], lag_ratio=0.15),
                run_time=2
            )
            
            # Step 5: Create initial GP mean curves (flat at y=0)
            gp_mean_rbf = axes_rbf.plot(lambda x: 0, color=BLUE, stroke_width=4)
            gp_mean_matern = axes_matern.plot(lambda x: 0, color=GREEN, stroke_width=4)
            gp_mean_linear = axes_linear.plot(lambda x: 0, color=ORANGE, stroke_width=4)
            
            self.gp_means = VGroup(gp_mean_rbf, gp_mean_matern, gp_mean_linear)
            
            self.play(
                LaggedStart(*[Create(m) for m in self.gp_means], lag_ratio=0.15),
                run_time=1.5
            )
            
            # Step 6: Create initial confidence bands (wide)
            def create_confidence_band(axes, y_offset=0, width=1.5, color=BLUE):
                points_upper = [axes.c2p(x, y_offset + width) for x in range(0, 11)]
                points_lower = [axes.c2p(x, y_offset - width) for x in range(10, -1, -1)]
                return Polygon(*points_upper, *points_lower, 
                              color=color, fill_opacity=0.2, stroke_width=0)
            
            band_rbf = create_confidence_band(axes_rbf, 0, 1.5, BLUE)
            band_matern = create_confidence_band(axes_matern, 0, 1.5, GREEN)
            band_linear = create_confidence_band(axes_linear, 0, 1.5, ORANGE)
            
            self.confidence_bands = VGroup(band_rbf, band_matern, band_linear)
            
            self.play(
                LaggedStart(*[FadeIn(b) for b in self.confidence_bands], lag_ratio=0.15),
                run_time=1.5
            )
            
            # Step 7: Create sample points (8 points at x=1,3,4,5,6,7,8,9)
            sample_x = [1, 3, 4, 5, 6, 7, 8, 9]
            
            dots_rbf = VGroup(*[
                Dot(axes_rbf.c2p(x, 0.8 * (x - 5)**2 / 12 - 0.5), 
                    radius=0.08, color=RED)
                for x in sample_x
            ])
            dots_matern = VGroup(*[
                Dot(axes_matern.c2p(x, 0.6 * (x - 5)**2 / 12 - 0.3), 
                    radius=0.08, color=RED)
                for x in sample_x
            ])
            dots_linear = VGroup(*[
                Dot(axes_linear.c2p(x, 0.4 * (x - 5)**2 / 12 - 0.2), 
                    radius=0.08, color=RED)
                for x in sample_x
            ])
            
            self.sample_points = VGroup(dots_rbf, dots_matern, dots_linear)
            
            # Step 8-11: Add samples one by one with GP updates
            # First sample
            self.play(
                FadeIn(dots_rbf[0], scale=0.5),
                FadeIn(dots_matern[0], scale=0.5),
                FadeIn(dots_linear[0], scale=0.5),
                run_time=0.6
            )
            
            # Step 9: Second and third samples
            self.play(
                LaggedStart(
                    FadeIn(dots_rbf[1], scale=0.5),
                    FadeIn(dots_matern[1], scale=0.5),
                    FadeIn(dots_linear[1], scale=0.5),
                    lag_ratio=0.1
                ),
                run_time=0.8
            )
            
            self.play(
                LaggedStart(
                    FadeIn(dots_rbf[2], scale=0.5),
                    FadeIn(dots_matern[2], scale=0.5),
                    FadeIn(dots_linear[2], scale=0.5),
                    lag_ratio=0.1
                ),
                run_time=0.8
            )
            
            # Step 10: Update GP means to start converging (RBF fastest)
            new_gp_rbf = axes_rbf.plot(lambda x: 0.7 * (x - 5)**2 / 12 - 0.5, 
                                       color=BLUE, stroke_width=4)
            new_gp_matern = axes_matern.plot(lambda x: 0.4 * (x - 5)**2 / 12 - 0.2, 
                                             color=GREEN, stroke_width=4)
            new_gp_linear = axes_linear.plot(lambda x: 0.1 * (x - 5)**2 / 12, 
                                             color=ORANGE, stroke_width=4)
            
            new_band_rbf = create_confidence_band(axes_rbf, -0.3, 0.8, BLUE)
            new_band_matern = create_confidence_band(axes_matern, -0.1, 1.0, GREEN)
            new_band_linear = create_confidence_band(axes_linear, 0, 1.3, ORANGE)
            
            self.play(
                Transform(gp_mean_rbf, new_gp_rbf),
                Transform(gp_mean_matern, new_gp_matern),
                Transform(gp_mean_linear, new_gp_linear),
                Transform(band_rbf, new_band_rbf),
                Transform(band_matern, new_band_matern),
                Transform(band_linear, new_band_linear),
                run_time=2
            )
            
            # Step 11: Add remaining samples
            self.play(
                LaggedStart(*[FadeIn(dots_rbf[i], scale=0.5) for i in range(3, 8)], lag_ratio=0.08),
                LaggedStart(*[FadeIn(dots_matern[i], scale=0.5) for i in range(3, 8)], lag_ratio=0.08),
                LaggedStart(*[FadeIn(dots_linear[i], scale=0.5) for i in range(3, 8)], lag_ratio=0.08),
                run_time=2
            )
            
            # Step 12: Final convergence (RBF converges best)
            final_gp_rbf = axes_rbf.plot(lambda x: 0.8 * (x - 5)**2 / 12 - 0.5, 
                                         color=BLUE, stroke_width=4)
            final_gp_matern = axes_matern.plot(lambda x: 0.6 * (x - 5)**2 / 12 - 0.3, 
                                               color=GREEN, stroke_width=4)
            final_gp_linear = axes_linear.plot(lambda x: 0.35 * (x - 5)**2 / 12 - 0.15, 
                                               color=ORANGE, stroke_width=4)
            
            final_band_rbf = create_confidence_band(axes_rbf, -0.5, 0.3, BLUE)
            final_band_matern = create_confidence_band(axes_matern, -0.3, 0.5, GREEN)
            final_band_linear = create_confidence_band(axes_linear, -0.15, 0.8, ORANGE)
            
            self.play(
                Transform(gp_mean_rbf, final_gp_rbf),
                Transform(gp_mean_matern, final_gp_matern),
                Transform(gp_mean_linear, final_gp_linear),
                Transform(band_rbf, final_band_rbf),
                Transform(band_matern, final_band_matern),
                Transform(band_linear, final_band_linear),
                run_time=2.5
            )
            
            # Step 13: Highlight RBF efficiency with flash
            self.play(
                Flash(label_rbf.get_center(), color=BLUE, flash_radius=0.8),
                label_rbf.animate.scale(1.2),
                run_time=1
            )
            
            # Step 14: Final emphasis
            self.play(
                label_rbf.animate.scale(1/1.2),
                run_time=0.5
            )
            
            self.wait(0.5)

        # ============================================================
        # SCENE 8: Regret Bounds Summary
        # ============================================================
        # Scene 8: Regret Bounds Summary
        
        if self.mobjects:
            self.play(*[FadeOut(obj) for obj in self.mobjects], run_time=0.5)
        
        with self.voiceover(text="""So here's the bottom line: smoother kernels give better regret bounds because they let you learn faster from fewer samples. The RBF kernel's O(√T) bound is near-optimal, while less smooth kernels pay a price in either the exponent or logarithmic factors. Choose your kernel based on what you know about your function!""") as tracker:
            
            # Step 1: Title
            title = Text("Regret Bounds Summary", font_size=42, color=GOLD, weight=BOLD)
            title.move_to(ZONES['title'])
            self.play(Write(title), run_time=1)
            
            # Step 2: Create table structure
            # Column headers
            col_headers = VGroup(
                Text("Kernel", font_size=28, color=WHITE, weight=BOLD),
                Text("Smoothness", font_size=28, color=WHITE, weight=BOLD),
                Text("Regret Bound", font_size=28, color=WHITE, weight=BOLD),
                Text("Visual", font_size=28, color=WHITE, weight=BOLD)
            )
            col_headers.arrange(RIGHT, buff=1.2)
            col_headers.move_to(ZONES['center']).shift(UP*1.5)
            
            self.play(
                LaggedStart(*[FadeIn(h, shift=DOWN*0.3) for h in col_headers], lag_ratio=0.15),
                run_time=1.5
            )
            
            # Step 3: Create horizontal line under headers
            header_line = Line(
                start=col_headers.get_left() + LEFT*0.3 + DOWN*0.3,
                end=col_headers.get_right() + RIGHT*0.3 + DOWN*0.3,
                color=WHITE,
                stroke_width=2
            )
            self.play(Create(header_line), run_time=0.8)
            
            # Step 4: Row 1 - Linear kernel (jagged curve)
            linear_kernel = Text("Linear", font_size=24, color=WHITE)
            linear_smooth = MathTex(r"\nu = 1", font_size=24, color=WHITE)
            linear_regret = MathTex(r"O(T^{2/3})", font_size=24, color=ORANGE)
            
            # Create jagged curve for linear
            jagged_points = [
                [-0.4, 0, 0], [-0.2, 0.15, 0], [0, -0.1, 0], 
                [0.2, 0.2, 0], [0.4, 0, 0]
            ]
            linear_visual = VMobject(color=GRAY, stroke_width=3)
            linear_visual.set_points_smoothly(jagged_points)
            
            row1 = VGroup(linear_kernel, linear_smooth, linear_regret, linear_visual)
            row1.arrange(RIGHT, buff=1.2)
            row1.move_to(col_headers.get_center()).shift(DOWN*1.0)
            
            self.play(
                LaggedStart(*[FadeIn(obj, scale=0.8) for obj in row1], lag_ratio=0.1),
                run_time=1.5
            )
            
            # Step 5: Row 2 - Matérn kernel (wavy curve)
            matern_kernel = Text("Matérn", font_size=24, color=WHITE)
            matern_smooth = MathTex(r"\nu > 1", font_size=24, color=WHITE)
            matern_regret = MathTex(r"O(T^{\frac{\nu+1}{2\nu+1}})", font_size=22, color=BLUE)
            
            # Create wavy curve for Matérn
            wavy_points = [
                [-0.4, 0, 0], [-0.2, 0.1, 0], [0, -0.05, 0], 
                [0.2, 0.08, 0], [0.4, 0, 0]
            ]
            matern_visual = VMobject(color=BLUE, stroke_width=3)
            matern_visual.set_points_smoothly(wavy_points)
            
            row2 = VGroup(matern_kernel, matern_smooth, matern_regret, matern_visual)
            row2.arrange(RIGHT, buff=1.2)
            row2.move_to(col_headers.get_center()).shift(DOWN*2.0)
            
            self.play(
                LaggedStart(*[FadeIn(obj, scale=0.8) for obj in row2], lag_ratio=0.1),
                run_time=1.5
            )
            
            # Step 6: Row 3 - RBF/SE kernel (smooth curve)
            rbf_kernel = Text("RBF/SE", font_size=24, color=WHITE)
            rbf_smooth = MathTex(r"\nu = \infty", font_size=24, color=WHITE)
            rbf_regret = MathTex(r"O(\sqrt{T})", font_size=24, color=GREEN)
            
            # Create smooth curve for RBF
            smooth_points = [
                [-0.4, 0, 0], [-0.2, 0.05, 0], [0, 0.08, 0], 
                [0.2, 0.05, 0], [0.4, 0, 0]
            ]
            rbf_visual = VMobject(color=GREEN, stroke_width=3)
            rbf_visual.set_points_smoothly(smooth_points)
            
            row3 = VGroup(rbf_kernel, rbf_smooth, rbf_regret, rbf_visual)
            row3.arrange(RIGHT, buff=1.2)
            row3.move_to(col_headers.get_center()).shift(DOWN*3.0)
            
            self.play(
                LaggedStart(*[FadeIn(obj, scale=0.8) for obj in row3], lag_ratio=0.1),
                run_time=1.5
            )
            
            # Step 7: Highlight RBF row with gold border
            gold_border = Rectangle(
                width=row3.get_width() + 0.5,
                height=row3.get_height() + 0.3,
                color=GOLD,
                stroke_width=4
            )
            gold_border.move_to(row3.get_center())
            
            self.play(Create(gold_border), run_time=1)
            
            # Step 8: Add star next to RBF
            star = Text("★", font_size=36, color=GOLD)
            star.next_to(gold_border, LEFT, buff=0.2)
            self.play(FadeIn(star, scale=2), Flash(star.get_center(), color=GOLD, flash_radius=0.5), run_time=0.8)
            
            # Step 9: Add footnote
            footnote = Text("*assuming bounded RKHS norm", font_size=20, color=GRAY)
            footnote.to_edge(DOWN, buff=0.3)
            self.play(FadeIn(footnote, shift=UP*0.2), run_time=0.8)
            
            # Step 10: Pulse the regret bounds to emphasize
            self.play(
                linear_regret.animate.scale(1.2).set_color(YELLOW),
                matern_regret.animate.scale(1.2).set_color(YELLOW),
                rbf_regret.animate.scale(1.3).set_color(YELLOW),
                run_time=0.8
            )
            self.play(
                linear_regret.animate.scale(1/1.2).set_color(ORANGE),
                matern_regret.animate.scale(1/1.2).set_color(BLUE),
                rbf_regret.animate.scale(1/1.3).set_color(GREEN),
                run_time=0.8
            )
            
            # Store for next scene
            self.table = VGroup(col_headers, header_line, row1, row2, row3, gold_border, star)
            self.footnote = footnote
            
            self.wait(0.5)
