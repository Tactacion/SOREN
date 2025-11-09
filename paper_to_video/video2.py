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

class Video2(VoiceoverScene):
    """
    The Insight
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
        # SCENE 1: The Core Challenge
        # ============================================================
        # Scene 1: The Core Challenge
        
        if self.mobjects:
            self.play(*[FadeOut(obj) for obj in self.mobjects], run_time=0.5)
        
        with self.voiceover(text="""We've seen how Gaussian Processes model uncertainty, but here's the real question: how do we use that uncertainty to make smart decisions? The breakthrough is realizing that minimizing regret—the cost of not knowing the optimum—is fundamentally about maximizing how quickly we learn.""") as tracker:
            
            # Step 1: Title
            title = Text("The Core Challenge", font_size=42, color=GOLD)
            title.move_to(ZONES['title'])
            self.play(Write(title), run_time=1)
            
            # Step 2: Create axes
            self.axes = Axes(
                x_range=[0, 10, 1], 
                y_range=[0, 8, 1], 
                x_length=9, 
                y_length=5,
                axis_config={"color": WHITE}
            )
            self.axes.move_to(ZONES['center']).shift(DOWN*0.3)
            self.play(Create(self.axes), run_time=1.5)
            
            # Step 3: Create true function curve (dashed GRAY with multiple peaks)
            def true_function(x):
                return 3 + 2*np.sin(x*0.8) + 1.5*np.sin(x*1.5 + 1) + 0.5*np.sin(x*3)
            
            self.true_curve = self.axes.plot(
                true_function, 
                x_range=[0, 10], 
                color=GRAY, 
                stroke_width=3
            )
            self.true_curve.set_stroke(dash_length=0.1)
            self.play(Create(self.true_curve), run_time=2)
            
            # Step 4: Mark the highest peak with gold aura
            peak_x = 7.5  # Approximate location of highest peak
            peak_y = true_function(peak_x)
            peak_point = self.axes.c2p(peak_x, peak_y)
            
            gold_aura = Circle(radius=0.4, color=GOLD, fill_opacity=0.3, stroke_width=3)
            gold_aura.move_to(peak_point)
            self.play(FadeIn(gold_aura, scale=0.5), Flash(peak_point, color=GOLD, flash_radius=0.5), run_time=1)
            
            # Step 5: Create regret counter (top-right corner)
            self.regret_counter = Text("Regret: 0", font_size=28, color=RED)
            self.regret_counter.to_edge(UP, buff=0.3).to_edge(RIGHT, buff=0.5)
            self.play(FadeIn(self.regret_counter, shift=DOWN*0.2), run_time=0.8)
            
            # Step 6: Create three sample points with error bars
            sample_x_vals = [2, 5, 8.5]
            sample_y_vals = [true_function(x) for x in sample_x_vals]
            
            self.sample_points = VGroup()
            error_bars = VGroup()
            
            for x_val, y_val in zip(sample_x_vals, sample_y_vals):
                point = self.axes.c2p(x_val, y_val)
                
                # X mark
                x_mark = VGroup(
                    Line(point + [-0.15, -0.15, 0], point + [0.15, 0.15, 0], color=RED, stroke_width=4),
                    Line(point + [-0.15, 0.15, 0], point + [0.15, -0.15, 0], color=RED, stroke_width=4)
                )
                self.sample_points.add(x_mark)
                
                # Error bars
                error_bar = Line(
                    point + [0, -0.5, 0], 
                    point + [0, 0.5, 0], 
                    color=RED, 
                    stroke_width=2
                )
                error_bars.add(error_bar)
            
            # Step 7: Animate sample points appearing
            self.play(
                LaggedStart(*[FadeIn(sp, scale=0.5) for sp in self.sample_points], lag_ratio=0.3),
                run_time=2
            )
            
            # Step 8: Add error bars
            self.play(
                LaggedStart(*[Create(eb) for eb in error_bars], lag_ratio=0.2),
                run_time=1.5
            )
            
            # Step 9: Create climbing figure (small dot that moves)
            self.figure = Dot(
                self.axes.c2p(sample_x_vals[0], sample_y_vals[0]), 
                radius=0.12, 
                color=BLUE
            )
            self.play(FadeIn(self.figure, scale=0.5), run_time=0.8)
            
            # Step 10: Figure moves to second sample (stumbles at low point)
            stumble_point = self.axes.c2p(3.5, true_function(3.5))
            self.play(
                self.figure.animate.move_to(stumble_point),
                run_time=1.2
            )
            stumble_indicator = Circle(radius=0.2, color=ORANGE, stroke_width=3)
            stumble_indicator.move_to(stumble_point)
            self.play(Flash(stumble_point, color=ORANGE, flash_radius=0.4), FadeIn(stumble_indicator, scale=0.5), run_time=0.6)
            self.play(FadeOut(stumble_indicator), run_time=0.4)
            
            # Step 11: Update regret counter
            new_regret = Text("Regret: 12", font_size=28, color=RED)
            new_regret.move_to(self.regret_counter.get_center())
            self.play(Transform(self.regret_counter, new_regret), run_time=0.8)
            
            # Step 12: Figure continues climbing toward peak
            self.play(
                self.figure.animate.move_to(self.axes.c2p(sample_x_vals[1], sample_y_vals[1])),
                run_time=1.2
            )
            self.play(
                self.figure.animate.move_to(self.axes.c2p(sample_x_vals[2], sample_y_vals[2])),
                run_time=1.5
            )
            
            # Final regret update
            final_regret = Text("Regret: 8", font_size=28, color=YELLOW)
            final_regret.move_to(self.regret_counter.get_center())
            self.play(Transform(self.regret_counter, final_regret), run_time=0.8)
            
            self.wait(0.5)

        # ============================================================
        # SCENE 2: Introducing UCB
        # ============================================================
        # Scene 2: Introducing UCB
        
        if self.mobjects:
            self.play(*[FadeOut(obj) for obj in self.mobjects], run_time=0.5)
        
        with self.voiceover(text="""Enter the Upper Confidence Bound, or UCB. The formula is beautifully simple: take your predicted mean and add beta times the uncertainty. This single number captures both what looks good and what we don't know yet.""") as tracker:
            
            # Step 1: Title
            title = Text("Introducing UCB", font_size=42, color=GOLD)
            title.move_to(ZONES['title'])
            self.play(Write(title), run_time=1)
            
            # Step 2: UCB equation at top center
            self.ucb_equation = MathTex(
                r"\text{UCB}(x) = \mu(x) + \beta \sigma(x)",
                font_size=36,
                color=WHITE
            )
            self.ucb_equation.next_to(title, DOWN, buff=0.4)
            self.play(Write(self.ucb_equation), run_time=1.5)
            
            # Step 3: Create three horizontal axes strips
            strip_height = 1.5
            strip_width = 10
            x_range = [0, 10, 2]
            y_range = [-1, 1, 1]
            
            # Mean axes (top strip)
            self.mean_axes = Axes(
                x_range=x_range,
                y_range=y_range,
                x_length=strip_width,
                y_length=strip_height,
                axis_config={"include_tip": False}
            )
            self.mean_axes.move_to([0, 1, 0])
            
            # Uncertainty axes (middle strip)
            self.uncertainty_axes = Axes(
                x_range=x_range,
                y_range=[0, 1, 0.5],
                x_length=strip_width,
                y_length=strip_height,
                axis_config={"include_tip": False}
            )
            self.uncertainty_axes.move_to([0, -0.5, 0])
            
            # UCB axes (bottom strip)
            self.ucb_axes = Axes(
                x_range=x_range,
                y_range=[-1, 2, 1],
                x_length=strip_width,
                y_length=strip_height,
                axis_config={"include_tip": False}
            )
            self.ucb_axes.move_to([0, -2, 0])
            
            # Step 4: Animate axes creation
            self.play(
                LaggedStart(
                    Create(self.mean_axes),
                    Create(self.uncertainty_axes),
                    Create(self.ucb_axes),
                    lag_ratio=0.3
                ),
                run_time=2
            )
            
            # Step 5: Add labels for each strip
            mean_label = Text("Mean μ(x)", font_size=24, color=BLUE)
            mean_label.next_to(self.mean_axes, LEFT, buff=0.3)
            
            uncertainty_label = Text("Uncertainty σ(x)", font_size=24, color=YELLOW)
            uncertainty_label.next_to(self.uncertainty_axes, LEFT, buff=0.3)
            
            ucb_label = Text("UCB", font_size=24, color=PURPLE)
            ucb_label.next_to(self.ucb_axes, LEFT, buff=0.3)
            
            self.play(
                LaggedStart(
                    Write(mean_label),
                    Write(uncertainty_label),
                    Write(ucb_label),
                    lag_ratio=0.2
                ),
                run_time=1.5
            )
            
            # Step 6: Create beta tracker and display
            self.beta_tracker = ValueTracker(1.0)
            beta_display = MathTex(r"\beta = ", font_size=28, color=WHITE)
            beta_value = DecimalNumber(
                self.beta_tracker.get_value(),
                num_decimal_places=1,
                font_size=28,
                color=ORANGE
            )
            beta_value.add_updater(lambda m: m.set_value(self.beta_tracker.get_value()))
            beta_group = VGroup(beta_display, beta_value).arrange(RIGHT, buff=0.1)
            beta_group.to_edge(RIGHT, buff=0.5).shift(UP*2)
            
            self.play(FadeIn(beta_group, shift=LEFT*0.3), run_time=0.8)
            
            # Step 7: Draw mean curve (blue GP mean)
            def mean_func(x):
                return 0.3 * np.sin(x * 0.8) - 0.2
            
            self.mean_curve = self.mean_axes.plot(
                mean_func,
                color=BLUE,
                stroke_width=4
            )
            self.play(Create(self.mean_curve), run_time=2)
            
            # Step 8: Draw uncertainty region (yellow filled area)
            def uncertainty_func(x):
                return 0.5 * np.exp(-0.3 * (x - 5)**2) + 0.2
            
            uncertainty_curve = self.uncertainty_axes.plot(
                uncertainty_func,
                color=YELLOW,
                stroke_width=3
            )
            
            # Create filled region
            self.uncertainty_region = self.uncertainty_axes.get_area(
                uncertainty_curve,
                x_range=[0, 10],
                color=YELLOW,
                opacity=0.4
            )
            
            self.play(
                Create(uncertainty_curve),
                FadeIn(self.uncertainty_region),
                run_time=2
            )
            
            # Step 9: Draw UCB curve (purple)
            def ucb_func(x):
                beta = self.beta_tracker.get_value()
                return mean_func(x) + beta * uncertainty_func(x)
            
            self.ucb_curve = always_redraw(
                lambda: self.ucb_axes.plot(
                    lambda x: mean_func(x) + self.beta_tracker.get_value() * uncertainty_func(x),
                    color=PURPLE,
                    stroke_width=4
                )
            )
            
            self.play(Create(self.ucb_curve), run_time=2)
            
            # Step 10: Add vertical dashed reference lines
            reference_x_values = [2, 5, 8]
            reference_lines = VGroup()
            
            for x_val in reference_x_values:
                line_top = self.mean_axes.c2p(x_val, 1)
                line_bottom = self.ucb_axes.c2p(x_val, -1)
                dashed_line = DashedLine(
                    line_top,
                    line_bottom,
                    color=GRAY,
                    dash_length=0.1,
                    stroke_width=2
                )
                reference_lines.add(dashed_line)
            
            self.play(
                LaggedStart(*[Create(line) for line in reference_lines], lag_ratio=0.2),
                run_time=1.5
            )
            
            # Step 11: Animate beta changing to show effect
            self.play(
                self.beta_tracker.animate.set_value(2.0),
                run_time=2
            )
            
            # Step 12: Return beta to original value
            self.play(
                self.beta_tracker.animate.set_value(1.0),
                run_time=1.5
            )
            
            self.wait(0.5)

        # ============================================================
        # SCENE 3: UCB Visualization
        # ============================================================
        # Scene 3: UCB Visualization
        
        if self.mobjects:
            self.play(*[FadeOut(obj) for obj in self.mobjects], run_time=0.5)
        
        with self.voiceover(text="""Let's see this in action. The dashed line is our unknown function, the solid blue is our current belief, and the purple surface is the UCB. Notice how UCB is elevated both at peaks we've found AND in unexplored regions with high uncertainty.""") as tracker:
            
            # Step 1: Title
            title = Text("UCB Visualization", font_size=42, color=GOLD)
            title.move_to(ZONES['title'])
            self.play(Write(title), run_time=1)
            
            # Step 2: Create axes
            self.axes = Axes(
                x_range=[0, 10, 1], 
                y_range=[-1, 3, 1], 
                x_length=9, 
                y_length=5
            )
            self.axes.move_to(ZONES['center']).shift(DOWN*0.3)
            self.play(Create(self.axes), run_time=1.5)
            
            # Step 3: Create true function (dashed gray curve with peaks at x=2.5 and x=7)
            self.true_function = self.axes.plot(
                lambda x: 1.5 * np.exp(-0.5*((x-2.5)/1.2)**2) + 2 * np.exp(-0.5*((x-7)/1.5)**2),
                color=GRAY,
                stroke_width=3
            )
            self.true_function.set_stroke(dash_length=0.1)
            self.play(Create(self.true_function), run_time=2)
            
            # Step 4: Add legend for true function
            true_label = Text("Unknown Function", font_size=20, color=GRAY)
            true_label.next_to(self.axes, UP, buff=0.2).shift(LEFT*3)
            self.play(FadeIn(true_label, shift=DOWN*0.2), run_time=0.6)
            
            # Step 5: Create initial GP mean (flat at y=0)
            self.gp_mean = self.axes.plot(
                lambda x: 0,
                color=BLUE,
                stroke_width=4
            )
            self.play(Create(self.gp_mean), run_time=1.5)
            
            # Step 6: Create uncertainty band (±2σ around mean)
            uncertainty_upper = self.axes.plot(lambda x: 1.5, color=BLUE, stroke_width=0)
            uncertainty_lower = self.axes.plot(lambda x: -1.5, color=BLUE, stroke_width=0)
            self.uncertainty_band = Polygon(
                *[self.axes.c2p(x, 1.5) for x in np.linspace(0, 10, 50)],
                *[self.axes.c2p(x, -1.5) for x in np.linspace(10, 0, 50)],
                color=BLUE,
                fill_opacity=0.2,
                stroke_width=0
            )
            self.play(FadeIn(self.uncertainty_band), run_time=1)
            
            # Step 7: Create initial UCB curve (mean + 2σ)
            self.ucb_curve = self.axes.plot(
                lambda x: 1.5,
                color=PURPLE,
                stroke_width=5
            )
            self.play(Create(self.ucb_curve), run_time=1.5)
            
            # Step 8: Add observed points
            self.observed_points = VGroup(
                Dot(self.axes.c2p(1, 0.3), radius=0.1, color=RED),
                Dot(self.axes.c2p(9, 0.5), radius=0.1, color=RED)
            )
            self.play(
                LaggedStart(*[FadeIn(d, scale=0.5) for d in self.observed_points], lag_ratio=0.3),
                run_time=1.2
            )
            
            # Step 9: Update GP mean to fit through observed points
            updated_gp_mean = self.axes.plot(
                lambda x: 0.3*np.exp(-0.5*((x-1)/2)**2) + 0.5*np.exp(-0.5*((x-9)/2)**2),
                color=BLUE,
                stroke_width=4
            )
            self.play(Transform(self.gp_mean, updated_gp_mean), run_time=2)
            
            # Step 10: Update uncertainty band (narrow near observations, wide in middle)
            def upper_uncertainty(x):
                base = 0.3*np.exp(-0.5*((x-1)/2)**2) + 0.5*np.exp(-0.5*((x-9)/2)**2)
                sigma = 0.3 + 1.2*np.exp(-0.5*((x-1)/1.5)**2) + 1.2*np.exp(-0.5*((x-9)/1.5)**2)
                return base + 2*sigma
            
            def lower_uncertainty(x):
                base = 0.3*np.exp(-0.5*((x-1)/2)**2) + 0.5*np.exp(-0.5*((x-9)/2)**2)
                sigma = 0.3 + 1.2*np.exp(-0.5*((x-1)/1.5)**2) + 1.2*np.exp(-0.5*((x-9)/1.5)**2)
                return base - 2*sigma
            
            updated_uncertainty_band = Polygon(
                *[self.axes.c2p(x, upper_uncertainty(x)) for x in np.linspace(0, 10, 80)],
                *[self.axes.c2p(x, lower_uncertainty(x)) for x in np.linspace(10, 0, 80)],
                color=BLUE,
                fill_opacity=0.2,
                stroke_width=0
            )
            self.play(Transform(self.uncertainty_band, updated_uncertainty_band), run_time=2)
            
            # Step 11: Update UCB curve (high near observations AND in unexplored middle)
            updated_ucb_curve = self.axes.plot(
                upper_uncertainty,
                color=PURPLE,
                stroke_width=5
            )
            self.play(Transform(self.ucb_curve, updated_ucb_curve), run_time=2)
            
            # Step 12: Add legend labels
            mean_label = Text("GP Mean", font_size=20, color=BLUE)
            mean_label.next_to(true_label, DOWN, buff=0.2, aligned_edge=LEFT)
            ucb_label = Text("UCB (Mean + 2σ)", font_size=20, color=PURPLE)
            ucb_label.next_to(mean_label, DOWN, buff=0.2, aligned_edge=LEFT)
            
            self.play(
                LaggedStart(
                    FadeIn(mean_label, shift=DOWN*0.2),
                    FadeIn(ucb_label, shift=DOWN*0.2),
                    lag_ratio=0.3
                ),
                run_time=1.5
            )
            
            self.wait(0.5)

        # ============================================================
        # SCENE 4: UCB Selects Next Point
        # ============================================================
        # Scene 4: UCB Selects Next Point
        
        # Continue from previous
        
        with self.voiceover(text="""The algorithm simply picks wherever UCB is highest. Watch how it naturally balances exploitation—sampling near good values—with exploration—investigating uncertain regions. This isn't a heuristic; it's optimal in a precise mathematical sense.""") as tracker:
            
            # Step 1: Title
            title = Text("UCB Selects Next Point", font_size=42, color=GOLD)
            title.move_to(ZONES['title'])
            self.play(Write(title), run_time=1)
            
            # Step 2: Create scanning line with glow effect
            x_min = self.axes.x_range[0]
            x_max = self.axes.x_range[1]
            y_min = self.axes.y_range[0]
            y_max = self.axes.y_range[1]
            
            scanning_line = Line(
                start=self.axes.c2p(x_min, y_min),
                end=self.axes.c2p(x_min, y_max),
                color=YELLOW,
                stroke_width=3
            )
            scan_glow = Line(
                start=self.axes.c2p(x_min, y_min),
                end=self.axes.c2p(x_min, y_max),
                color=YELLOW,
                stroke_width=8,
                stroke_opacity=0.3
            )
            
            # Step 3: Create tracking dot on UCB curve
            ucb_highlight_dot = Dot(
                point=self.axes.c2p(x_min, 0),
                radius=0.1,
                color=YELLOW
            )
            
            self.play(
                Create(scanning_line),
                Create(scan_glow),
                FadeIn(ucb_highlight_dot, scale=0.5),
                run_time=1
            )
            
            # Step 4: Scan across to find maximum UCB
            # Find max UCB point (around x=3.5 based on typical UCB behavior)
            max_x = 3.5
            max_y_ucb = 2.8  # UCB value at max
            max_y_true = 0.3 * max_x**2 - 1.5  # True function value
            
            self.play(
                scanning_line.animate.move_to(self.axes.c2p(max_x, (y_min + y_max) / 2)),
                scan_glow.animate.move_to(self.axes.c2p(max_x, (y_min + y_max) / 2)),
                ucb_highlight_dot.animate.move_to(self.axes.c2p(max_x, max_y_ucb)),
                run_time=3
            )
            
            # Step 5: Flash and highlight the maximum point
            self.play(
                Flash(ucb_highlight_dot.get_center(), color=GOLD, flash_radius=0.5),
                ucb_highlight_dot.animate.scale(1.5).set_color(GOLD),
                run_time=0.8
            )
            
            # Step 6: Create gold star at maximum UCB point
            max_ucb_star = RegularPolygon(n=5, color=GOLD, fill_opacity=0.8)
            max_ucb_star.scale(0.3)
            max_ucb_star.move_to(self.axes.c2p(max_x, max_y_ucb))
            
            self.play(
                Transform(ucb_highlight_dot, max_ucb_star),
                FadeOut(scanning_line),
                FadeOut(scan_glow),
                run_time=1
            )
            
            # Step 7: Draw vertical dashed line to x-axis
            vertical_dashed_line = DashedLine(
                start=self.axes.c2p(max_x, max_y_ucb),
                end=self.axes.c2p(max_x, y_min),
                color=GRAY,
                dash_length=0.1
            )
            
            self.play(Create(vertical_dashed_line), run_time=1)
            
            # Step 8: Create new observation dot on true function
            new_observation_dot = Dot(
                point=self.axes.c2p(max_x, max_y_true),
                radius=0.12,
                color=RED
            )
            
            self.play(
                FadeIn(new_observation_dot, scale=0.5),
                Flash(new_observation_dot.get_center(), color=RED, flash_radius=0.4),
                run_time=1
            )
            
            # Step 9: Update GP mean curve (shrinks uncertainty around new point)
            updated_gp_mean = self.axes.plot(
                lambda x: 0.3 * x**2 - 1.5 if abs(x - max_x) < 1.5 else 0.25 * x**2 - 1.3,
                color=BLUE,
                stroke_width=4
            )
            
            self.play(
                Transform(self.gp_mean, updated_gp_mean),
                run_time=1.5
            )
            
            # Step 10: Update uncertainty band (shrink around new observation)
            upper_bound_updated = self.axes.plot(
                lambda x: (0.3 * x**2 - 1.5 + 0.3) if abs(x - max_x) > 1.0 else (0.3 * x**2 - 1.5 + 0.1),
                color=BLUE,
                stroke_width=0
            )
            lower_bound_updated = self.axes.plot(
                lambda x: (0.3 * x**2 - 1.5 - 0.3) if abs(x - max_x) > 1.0 else (0.3 * x**2 - 1.5 - 0.1),
                color=BLUE,
                stroke_width=0
            )
            
            updated_uncertainty_band = self.axes.get_area(
                upper_bound_updated,
                bounded_graph=lower_bound_updated,
                color=BLUE,
                opacity=0.2
            )
            
            self.play(
                Transform(self.uncertainty_band, updated_uncertainty_band),
                run_time=1.5
            )
            
            # Step 11: Highlight balance between exploitation and exploration
            exploit_label = Text("Exploitation", font_size=24, color=GREEN)
            exploit_label.next_to(self.axes.c2p(-2, -1), DOWN, buff=0.2)
            
            explore_label = Text("Exploration", font_size=24, color=ORANGE)
            explore_label.next_to(self.axes.c2p(3.5, 2), UP, buff=0.2)
            
            self.play(
                FadeIn(exploit_label, shift=UP*0.2),
                FadeIn(explore_label, shift=DOWN*0.2),
                run_time=1
            )
            
            # Step 12: Fade out labels and store state
            self.play(
                FadeOut(exploit_label),
                FadeOut(explore_label),
                FadeOut(title),
                run_time=0.8
            )
            
            # STORE for next scene
            self.observed_points.add(new_observation_dot)
            self.max_ucb_point = self.axes.c2p(max_x, max_y_true)
            self.vertical_dashed_line = vertical_dashed_line
            self.gp_mean = updated_gp_mean
            self.uncertainty_band = updated_uncertainty_band
            
            self.wait(0.5)

        # ============================================================
        # SCENE 5: Information Gain Concept
        # ============================================================
        # Scene 5: Information Gain Concept
        
        if self.mobjects:
            self.play(*[FadeOut(obj) for obj in self.mobjects], run_time=0.5)
        
        with self.voiceover(text="""But why does this work? The key is information gain—how much we learn about the entire function from each sample. The regret we accumulate is directly bounded by how quickly we can reduce our uncertainty.""") as tracker:
            
            # Step 1: Title
            title = Text("Information Gain Concept", font_size=42, color=GOLD)
            title.move_to(ZONES['title'])
            self.play(Write(title), run_time=1)
            
            # Step 2: Create domain border (10x5 domain)
            self.domain_border = Rectangle(width=8, height=4, color=WHITE, stroke_width=3)
            self.domain_border.move_to(ZONES['center'])
            self.play(Create(self.domain_border), run_time=1)
            
            # Step 3: Create heatmap_rectangle (initially uniform bright yellow)
            self.heatmap = Rectangle(width=7.9, height=3.9, color=YELLOW, fill_opacity=0.7)
            self.heatmap.move_to(ZONES['center'])
            self.play(FadeIn(self.heatmap), run_time=1)
            
            # Step 4: Add axes labels
            x_label = Text("x: 0-10", font_size=24, color=WHITE)
            x_label.next_to(self.domain_border, DOWN, buff=0.2)
            y_label = Text("y: 0-5", font_size=24, color=WHITE)
            y_label.next_to(self.domain_border, LEFT, buff=0.2)
            self.play(Write(x_label), Write(y_label), run_time=0.8)
            
            # Step 5: Create uncertainty counter
            self.uncertainty_counter = Text("Total Uncertainty: 100%", font_size=32, color=WHITE)
            self.uncertainty_counter.next_to(title, DOWN, buff=0.3)
            self.play(Write(self.uncertainty_counter), run_time=0.8)
            
            # Step 6: Create legend
            legend_title = Text("Uncertainty", font_size=24, color=WHITE)
            legend_title.to_edge(RIGHT, buff=0.5).shift(UP*1.5)
            high_box = Rectangle(width=0.4, height=0.3, color=YELLOW, fill_opacity=0.7)
            high_box.next_to(legend_title, DOWN, buff=0.2)
            high_label = Text("High", font_size=20, color=WHITE)
            high_label.next_to(high_box, RIGHT, buff=0.1)
            low_box = Rectangle(width=0.4, height=0.3, color=BLUE, fill_opacity=0.7)
            low_box.next_to(high_box, DOWN, buff=0.1)
            low_label = Text("Low", font_size=20, color=WHITE)
            low_label.next_to(low_box, RIGHT, buff=0.1)
            legend = VGroup(legend_title, high_box, high_label, low_box, low_label)
            self.play(FadeIn(legend, shift=LEFT*0.3), run_time=1)
            
            # Step 7: Create sample dots (3 RED dots at sampling locations)
            sample_positions = [
                self.domain_border.get_center() + LEFT*2 + UP*0.5,
                self.domain_border.get_center() + RIGHT*1.5 + DOWN*0.8,
                self.domain_border.get_center() + LEFT*0.5 + DOWN*1.2
            ]
            self.sample_dots = VGroup(*[
                Dot(point=pos, radius=0.12, color=RED)
                for pos in sample_positions
            ])
            self.play(
                LaggedStart(*[FadeIn(d, scale=0.5) for d in self.sample_dots], lag_ratio=0.3),
                run_time=1.5
            )
            
            # Step 8: Flash effect at each sample
            self.play(
                LaggedStart(*[Flash(d.get_center(), color=RED, flash_radius=0.5) for d in self.sample_dots], lag_ratio=0.2),
                run_time=1.5
            )
            
            # Step 9: Create uncertainty gradients (circular dark blue waves expanding from each sample)
            uncertainty_circles = VGroup()
            for pos in sample_positions:
                circle1 = Circle(radius=0.8, color=BLUE, stroke_width=3, fill_opacity=0.3)
                circle1.move_to(pos)
                circle2 = Circle(radius=1.3, color=BLUE, stroke_width=2, fill_opacity=0.2)
                circle2.move_to(pos)
                uncertainty_circles.add(circle1, circle2)
            
            self.play(
                LaggedStart(*[Create(c) for c in uncertainty_circles], lag_ratio=0.1),
                run_time=2
            )
            
            # Step 10: Update heatmap to show reduced uncertainty around samples
            heatmap_updated = VGroup()
            # Create blue circles around samples
            for pos in sample_positions:
                blue_region = Circle(radius=1.2, color=BLUE, fill_opacity=0.6)
                blue_region.move_to(pos)
                heatmap_updated.add(blue_region)
            
            self.play(FadeIn(heatmap_updated), run_time=1.5)
            
            # Step 11: Update uncertainty counter
            new_counter = Text("Total Uncertainty: 45%", font_size=32, color=GREEN)
            new_counter.move_to(self.uncertainty_counter.get_center())
            self.play(Transform(self.uncertainty_counter, new_counter), run_time=1)
            
            # Step 12: Add arrows showing information spread
            info_arrows = VGroup()
            for pos in sample_positions:
                for angle in [0, PI/2, PI, 3*PI/2]:
                    arrow_end = pos + [0.9*np.cos(angle), 0.9*np.sin(angle), 0]
                    arrow = Arrow(pos, arrow_end, color=PURPLE, buff=0.15, stroke_width=2)
                    info_arrows.add(arrow)
            
            self.play(
                LaggedStart(*[Create(a) for a in info_arrows], lag_ratio=0.02),
                run_time=2
            )
            
            # Step 13: Highlight the reduction in uncertainty
            self.play(
                self.heatmap.animate.set_fill(YELLOW, opacity=0.3),
                run_time=1.5
            )
            
            # Step 14: Pulse effect on sample dots
            self.play(
                *[d.animate.scale(1.5).set_color(ORANGE) for d in self.sample_dots],
                run_time=0.8
            )
            self.play(
                *[d.animate.scale(1/1.5).set_color(RED) for d in self.sample_dots],
                run_time=0.8
            )
            
            # Step 15: Final emphasis
            emphasis_text = Text("Less Uncertainty = Better Decisions", font_size=28, color=GREEN)
            emphasis_text.next_to(self.domain_border, DOWN, buff=0.8)
            self.play(Write(emphasis_text), run_time=1.5)
            
            self.wait(0.5)

        # ============================================================
        # SCENE 6: Random vs Intelligent Sampling
        # ============================================================
        # Scene 6: Random vs Intelligent Sampling
        
        if self.mobjects:
            self.play(*[FadeOut(obj) for obj in self.mobjects], run_time=0.5)
        
        with self.voiceover(text="""Compare two strategies side by side. Random sampling learns slowly, wasting samples in uninformative regions. GP-UCB focuses samples where they maximize information gain, learning the function's structure much faster.""") as tracker:
            
            # Step 1: Title
            title = Text("Random vs Intelligent Sampling", font_size=42, color=GOLD)
            title.move_to(ZONES['title'])
            self.play(Write(title), run_time=1)
            
            # Step 2: Split screen divider line
            self.divider_line = Line(start=[0, 3, 0], end=[0, -3, 0], color=WHITE, stroke_width=3)
            self.play(Create(self.divider_line), run_time=0.8)
            
            # Step 3: Left and right titles
            left_title = Text("Random Sampling", font_size=32, color=RED)
            left_title.move_to([-3.5, 2.5, 0])
            right_title = Text("GP-UCB", font_size=32, color=GREEN)
            right_title.move_to([3.5, 2.5, 0])
            self.play(Write(left_title), Write(right_title), run_time=1)
            
            # Step 4: Create two identical uncertainty heatmaps (simplified as grids with colored squares)
            # Left heatmap
            left_squares = VGroup()
            for i in range(-2, 3):
                for j in range(-1, 2):
                    opacity = 0.3 + 0.15 * (abs(i) + abs(j))
                    sq = Rectangle(width=0.6, height=0.6, color=YELLOW, fill_opacity=opacity, stroke_width=1)
                    sq.move_to([-3.5 + i*0.6, 0.8 + j*0.6, 0])
                    left_squares.add(sq)
            
            # Right heatmap
            right_squares = VGroup()
            for i in range(-2, 3):
                for j in range(-1, 2):
                    opacity = 0.3 + 0.15 * (abs(i) + abs(j))
                    sq = Rectangle(width=0.6, height=0.6, color=YELLOW, fill_opacity=opacity, stroke_width=1)
                    sq.move_to([3.5 + i*0.6, 0.8 + j*0.6, 0])
                    right_squares.add(sq)
            
            self.left_heatmap = left_squares
            self.right_heatmap = right_squares
            
            self.play(
                LaggedStart(*[FadeIn(sq) for sq in left_squares], lag_ratio=0.02),
                LaggedStart(*[FadeIn(sq) for sq in right_squares], lag_ratio=0.02),
                run_time=2
            )
            
            # Step 5: Create bar graphs below heatmaps
            left_bar_label = Text("Total Information Gained", font_size=18, color=WHITE)
            left_bar_label.move_to([-3.5, -1.8, 0])
            right_bar_label = Text("Total Information Gained", font_size=18, color=WHITE)
            right_bar_label.move_to([3.5, -1.8, 0])
            
            self.play(Write(left_bar_label), Write(right_bar_label), run_time=0.8)
            
            # Bar graph backgrounds
            left_bar_bg = Rectangle(width=2, height=0.3, color=GRAY, fill_opacity=0.3, stroke_width=2)
            left_bar_bg.move_to([-3.5, -2.3, 0])
            right_bar_bg = Rectangle(width=2, height=0.3, color=GRAY, fill_opacity=0.3, stroke_width=2)
            right_bar_bg.move_to([3.5, -2.3, 0])
            
            self.play(Create(left_bar_bg), Create(right_bar_bg), run_time=0.5)
            
            # Initial bars (will grow)
            left_bar = Rectangle(width=0.1, height=0.3, color=RED, fill_opacity=0.8, stroke_width=0)
            left_bar.move_to([-4.5, -2.3, 0])
            right_bar = Rectangle(width=0.1, height=0.3, color=GREEN, fill_opacity=0.8, stroke_width=0)
            right_bar.move_to([2.5, -2.3, 0])
            
            self.left_bar_graph = left_bar
            self.right_bar_graph = right_bar
            
            self.play(FadeIn(left_bar), FadeIn(right_bar), run_time=0.5)
            
            # Step 6-12: Animate 8 rounds of sampling
            left_sample_positions = [
                [-4.1, 1.4, 0], [-2.5, 0.2, 0], [-4.7, 0.8, 0], [-2.9, 1.4, 0],
                [-3.8, 0.5, 0], [-2.2, 1.1, 0], [-4.4, 0.2, 0], [-3.2, 0.8, 0]
            ]
            
            right_sample_positions = [
                [4.1, 1.4, 0], [2.9, 1.4, 0], [4.7, 0.8, 0], [3.5, 0.2, 0],
                [2.3, 0.8, 0], [4.4, 0.2, 0], [3.2, 1.1, 0], [2.6, 0.5, 0]
            ]
            
            for round_idx in range(8):
                # Add sampling dots
                left_dot = Dot(point=left_sample_positions[round_idx], radius=0.08, color=RED)
                right_dot = Dot(point=right_sample_positions[round_idx], radius=0.08, color=GREEN)
                
                self.play(
                    Flash(left_sample_positions[round_idx], color=RED, flash_radius=0.3),
                    Flash(right_sample_positions[round_idx], color=GREEN, flash_radius=0.3),
                    FadeIn(left_dot, scale=0.5),
                    FadeIn(right_dot, scale=0.5),
                    run_time=0.6
                )
                
                # Show uncertainty reduction (small circles for left, larger for right)
                left_reduction = Circle(radius=0.25, color=RED, fill_opacity=0.2, stroke_width=2)
                left_reduction.move_to(left_sample_positions[round_idx])
                right_reduction = Circle(radius=0.45, color=GREEN, fill_opacity=0.2, stroke_width=2)
                right_reduction.move_to(right_sample_positions[round_idx])
                
                self.play(
                    Create(left_reduction),
                    Create(right_reduction),
                    run_time=0.5
                )
                
                # Grow bars (left grows slowly, right grows faster)
                left_new_width = 0.1 + (round_idx + 1) * 0.2
                right_new_width = 0.1 + (round_idx + 1) * 0.35
                
                left_bar_new = Rectangle(width=left_new_width, height=0.3, color=RED, fill_opacity=0.8, stroke_width=0)
                left_bar_new.move_to([-4.5 + left_new_width/2 - 0.05, -2.3, 0])
                
                right_bar_new = Rectangle(width=right_new_width, height=0.3, color=GREEN, fill_opacity=0.8, stroke_width=0)
                right_bar_new.move_to([2.5 + right_new_width/2 - 0.05, -2.3, 0])
                
                self.play(
                    Transform(self.left_bar_graph, left_bar_new),
                    Transform(self.right_bar_graph, right_bar_new),
                    run_time=0.5
                )
                
                # Fade out reduction circles
                self.play(FadeOut(left_reduction), FadeOut(right_reduction), run_time=0.3)
            
            self.wait(0.5)

        # ============================================================
        # SCENE 7: The Regret Bound
        # ============================================================
        # Scene 7: The Regret Bound
        
        if self.mobjects:
            self.play(*[FadeOut(obj) for obj in self.mobjects], run_time=0.5)
        
        with self.voiceover(text="""Here's the beautiful theorem: your cumulative regret grows at most as the square root of the information gain times the number of samples. This means that strategies maximizing information gain automatically minimize regret.""") as tracker:
            
            # Step 1: Title
            title = Text("The Regret Bound", font_size=42, color=GOLD)
            title.move_to(ZONES['title'])
            self.play(Write(title), run_time=1)
            
            # Step 2: Create regret inequality formula
            self.regret_formula = MathTex(
                r"R_T \leq \sqrt{\beta_T \cdot I_T \cdot T}",
                font_size=40,
                color=WHITE
            )
            self.regret_formula.move_to([0, 2.5, 0])
            self.play(Write(self.regret_formula), run_time=1.5)
            
            # Step 3: Highlight the sqrt symbol
            sqrt_highlight = Circle(radius=0.4, color=YELLOW, stroke_width=4)
            sqrt_highlight.move_to(self.regret_formula[0][3].get_center())
            self.play(Create(sqrt_highlight), run_time=0.8)
            self.play(FadeOut(sqrt_highlight), run_time=0.5)
            
            # Step 4: Create top axes for information gain
            self.top_axes = Axes(
                x_range=[0, 10, 2],
                y_range=[0, 5, 1],
                x_length=6,
                y_length=2.5,
                axis_config={"color": GRAY}
            )
            self.top_axes.move_to([0, 0.8, 0])
            
            top_label = Text("Information Gain", font_size=24, color=GREEN)
            top_label.next_to(self.top_axes, UP, buff=0.2)
            
            self.play(Create(self.top_axes), Write(top_label), run_time=1.2)
            
            # Step 5: Create information gain curve (logarithmic growth)
            self.info_gain_curve = self.top_axes.plot(
                lambda x: 2 * (x**0.5),
                x_range=[0.1, 10],
                color=GREEN,
                stroke_width=4
            )
            self.play(Create(self.info_gain_curve), run_time=2)
            
            # Step 6: Create bottom axes for cumulative regret
            self.bottom_axes = Axes(
                x_range=[0, 10, 2],
                y_range=[0, 5, 1],
                x_length=6,
                y_length=2.5,
                axis_config={"color": GRAY}
            )
            self.bottom_axes.move_to([0, -1.8, 0])
            
            bottom_label = Text("Cumulative Regret", font_size=24, color=RED)
            bottom_label.next_to(self.bottom_axes, UP, buff=0.2)
            
            self.play(Create(self.bottom_axes), Write(bottom_label), run_time=1.2)
            
            # Step 7: Create cumulative regret curve (sqrt growth)
            self.regret_curve = self.bottom_axes.plot(
                lambda x: 1.5 * (x**0.5),
                x_range=[0.1, 10],
                color=RED,
                stroke_width=4
            )
            self.play(Create(self.regret_curve), run_time=2)
            
            # Step 8: Create dashed bound curve (theoretical upper bound)
            bound_curve = self.bottom_axes.plot(
                lambda x: 2.2 * (x**0.5),
                x_range=[0.1, 10],
                color=YELLOW,
                stroke_width=3
            )
            bound_curve.set_stroke(dash_length=0.1)
            
            bound_label = Text("Bound", font_size=20, color=YELLOW)
            bound_label.next_to(bound_curve, RIGHT, buff=0.1)
            
            self.play(Create(bound_curve), Write(bound_label), run_time=1.5)
            
            # Step 9: Add sample points on information gain curve
            sample_dots_top = VGroup(*[
                Dot(self.top_axes.c2p(i, 2 * (i**0.5)), radius=0.06, color=GREEN)
                for i in range(1, 11)
            ])
            self.play(
                LaggedStart(*[FadeIn(d, scale=0.5) for d in sample_dots_top], lag_ratio=0.08),
                run_time=1.5
            )
            
            # Step 10: Add sample points on regret curve
            sample_dots_bottom = VGroup(*[
                Dot(self.bottom_axes.c2p(i, 1.5 * (i**0.5)), radius=0.06, color=RED)
                for i in range(1, 11)
            ])
            self.play(
                LaggedStart(*[FadeIn(d, scale=0.5) for d in sample_dots_bottom], lag_ratio=0.08),
                run_time=1.5
            )
            
            # Step 11: Add connecting arrows between corresponding points
            connecting_arrows = VGroup(*[
                Arrow(
                    sample_dots_top[i].get_center(),
                    sample_dots_bottom[i].get_center(),
                    color=PURPLE,
                    buff=0.1,
                    stroke_width=2
                )
                for i in range(0, 10, 3)  # Every 3rd point
            ])
            self.play(
                LaggedStart(*[Create(a) for a in connecting_arrows], lag_ratio=0.15),
                run_time=1.5
            )
            
            # Step 12: Flash effect on the formula to emphasize the relationship
            self.play(
                Flash(self.regret_formula.get_center(), color=YELLOW, flash_radius=1.0),
                self.regret_formula.animate.scale(1.1),
                run_time=0.8
            )
            self.play(self.regret_formula.animate.scale(1/1.1), run_time=0.5)
            
            self.wait(0.5)

        # ============================================================
        # SCENE 8: The Complete Picture
        # ============================================================
        # Scene 8: The Complete Picture
        
        if self.mobjects:
            self.play(*[FadeOut(obj) for obj in self.mobjects], run_time=0.5)
        
        with self.voiceover(text="""So here's the insight: UCB isn't just a clever heuristic—it's a principled strategy that maximizes information gain, which provably minimizes regret. By being optimistic about uncertainty, we learn efficiently and find the optimum quickly.""") as tracker:
            
            # Step 1: Title
            title = Text("The Complete Picture", font_size=42, color=GOLD, weight=BOLD)
            title.move_to(ZONES['title'])
            self.play(Write(title), run_time=1)
            
            # Step 2: Create axes with labels
            self.axes = Axes(
                x_range=[0, 10, 1], 
                y_range=[-2, 3, 1], 
                x_length=9, 
                y_length=4.5,
                axis_config={"include_numbers": True, "font_size": 24}
            )
            self.axes.move_to(ZONES['center']).shift(DOWN*0.3)
            x_label = Text("x", font_size=28, color=WHITE).next_to(self.axes.x_axis, RIGHT, buff=0.2)
            y_label = Text("f(x)", font_size=28, color=WHITE).next_to(self.axes.y_axis, UP, buff=0.2)
            self.play(Create(self.axes), Write(x_label), Write(y_label), run_time=1.5)
            
            # Step 3: True function (gray dashed)
            self.true_function = self.axes.plot(
                lambda x: 2*np.sin(x*0.8) + 0.3*x - 1, 
                color=GRAY, 
                stroke_width=3
            )
            self.true_function.set_stroke(dash_length=0.1)
            true_label = Text("True Function", font_size=24, color=GRAY)
            true_label.next_to(self.axes, UP, buff=0.1).shift(LEFT*3)
            self.play(Create(self.true_function), FadeIn(true_label), run_time=1.5)
            
            # Step 4: Uncertainty heatmap (simplified as shaded regions)
            uncertainty_regions = VGroup()
            for i in range(0, 10):
                x_val = i + 0.5
                y_mean = 2*np.sin(x_val*0.8) + 0.3*x_val - 1
                uncertainty = 1.5 * (1 - i/10)  # Decreasing uncertainty
                rect = Rectangle(
                    width=0.8, 
                    height=uncertainty*2, 
                    color=PURPLE, 
                    fill_opacity=0.15,
                    stroke_width=0
                )
                rect.move_to(self.axes.c2p(x_val, y_mean))
                uncertainty_regions.add(rect)
            self.play(
                LaggedStart(*[FadeIn(r, scale=0.8) for r in uncertainty_regions], lag_ratio=0.08),
                run_time=2
            )
            
            # Step 5: GP mean curve (blue)
            self.gp_mean_curve = self.axes.plot(
                lambda x: 2*np.sin(x*0.8) + 0.3*x - 1 + 0.2*np.sin(x*2), 
                color=BLUE, 
                stroke_width=4
            )
            gp_label = Text("GP Mean", font_size=24, color=BLUE)
            gp_label.next_to(true_label, RIGHT, buff=0.8)
            self.play(Create(self.gp_mean_curve), FadeIn(gp_label), run_time=1.5)
            
            # Step 6: UCB curve (purple)
            ucb_curve = self.axes.plot(
                lambda x: 2*np.sin(x*0.8) + 0.3*x - 1 + 1.5*(1 - x/10), 
                color=PURPLE, 
                stroke_width=4
            )
            ucb_label = Text("UCB", font_size=24, color=PURPLE)
            ucb_label.next_to(gp_label, RIGHT, buff=0.8)
            self.play(Create(ucb_curve), FadeIn(ucb_label), run_time=1.5)
            
            # Step 7: Sample dots (red)
            sample_positions = [1.5, 3.2, 5.8, 7.1, 8.5]
            self.sample_dots = VGroup(*[
                Dot(
                    self.axes.c2p(x, 2*np.sin(x*0.8) + 0.3*x - 1), 
                    radius=0.1, 
                    color=RED
                )
                for x in sample_positions
            ])
            self.play(
                LaggedStart(*[FadeIn(d, scale=0.5) for d in self.sample_dots], lag_ratio=0.15),
                run_time=2
            )
            
            # Step 8: Flash effects on samples
            self.play(
                LaggedStart(*[Flash(d.get_center(), color=YELLOW, flash_radius=0.3) for d in self.sample_dots], lag_ratio=0.1),
                run_time=1.5
            )
            
            # Step 9: Gold star at UCB maximum
            ucb_max_x = 2.5
            ucb_max_y = 2*np.sin(ucb_max_x*0.8) + 0.3*ucb_max_x - 1 + 1.5*(1 - ucb_max_x/10)
            gold_star = RegularPolygon(n=5, color=GOLD, fill_opacity=0.8)
            gold_star.scale(0.3).move_to(self.axes.c2p(ucb_max_x, ucb_max_y))
            self.play(FadeIn(gold_star, scale=0.3), Flash(gold_star.get_center(), color=GOLD), run_time=1)
            
            # Step 10: Info gained counter (green box)
            info_box = Rectangle(width=2.5, height=0.8, color=GREEN, stroke_width=2)
            info_box.to_edge(UP, buff=0.5).shift(LEFT*4)
            self.info_counter = Text("Info Gain: 87%", font_size=24, color=GREEN)
            self.info_counter.move_to(info_box.get_center())
            self.play(Create(info_box), Write(self.info_counter), run_time=1)
            
            # Step 11: Regret counter (red box)
            regret_box = Rectangle(width=2.5, height=0.8, color=RED, stroke_width=2)
            regret_box.next_to(info_box, RIGHT, buff=0.5)
            self.regret_counter = Text("Regret: 0.13", font_size=24, color=RED)
            self.regret_counter.move_to(regret_box.get_center())
            self.play(Create(regret_box), Write(self.regret_counter), run_time=1)
            
            # Step 12: Corner display box with key insight
            corner_box = Rectangle(width=3.5, height=1.2, color=GOLD, stroke_width=3, fill_opacity=0.1)
            corner_box.to_edge(RIGHT, buff=0.3).shift(DOWN*2)
            insight_text = Text("Optimism Under\nUncertainty", font_size=22, color=GOLD)
            insight_text.move_to(corner_box.get_center())
            self.play(Create(corner_box), Write(insight_text), run_time=1.5)
            
            # Step 13: Arrows showing information flow
            info_arrows = VGroup(*[
                Arrow(
                    self.sample_dots[i].get_center(),
                    info_box.get_bottom(),
                    color=GREEN,
                    buff=0.1,
                    stroke_width=2
                )
                for i in range(len(self.sample_dots))
            ])
            self.play(
                LaggedStart(*[Create(a) for a in info_arrows], lag_ratio=0.1),
                run_time=2
            )
            
            # Step 14: Highlight the connection
            self.play(
                gold_star.animate.scale(1.3),
                Flash(gold_star.get_center(), color=GOLD, flash_radius=0.5),
                run_time=0.8
            )
            self.play(gold_star.animate.scale(1/1.3), run_time=0.5)
            
            # Step 15: Pulse uncertainty regions
            self.play(
                uncertainty_regions.animate.set_fill(opacity=0.3),
                run_time=0.8
            )
            self.play(
                uncertainty_regions.animate.set_fill(opacity=0.15),
                run_time=0.8
            )
            
            # Step 16: Emphasize counters
            self.play(
                self.info_counter.animate.scale(1.2),
                self.regret_counter.animate.scale(1.2),
                run_time=0.6
            )
            self.play(
                self.info_counter.animate.scale(1/1.2),
                self.regret_counter.animate.scale(1/1.2),
                run_time=0.6
            )
            
            # Step 17: Final emphasis on complete picture
            self.play(
                title.animate.set_color(GOLD).scale(1.1),
                run_time=0.8
            )
            
            self.wait(0.5)
