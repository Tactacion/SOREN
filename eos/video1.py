from manim import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.elevenlabs import ElevenLabsService
import numpy as np
import os

# 3Blue1Brown colors (STRINGS)
BLUE = "#58C4DD"
GREEN = "#8BE17D"
ORANGE = "#FFB74D"
RED = "#FF6188"
YELLOW = "#FFD700"
GOLD = "#FFD700"
PURPLE = "#C678DD"
GRAY = "#888888"
WHITE = "#FFFFFF"
BLACK = "#000000"
TEAL = "#4DD0E1"

# Fix for ManimColor interpolation
from manim.utils.color import ManimColor

# Constants
CENTER = ORIGIN
MIDDLE = ORIGIN

class Video1(VoiceoverScene):
    def construct(self):
        # Set up speech service *once*
        self.set_speech_service(
            ElevenLabsService(
                api_key=os.getenv("ELEVENLABS_API_KEY"),
                voice_id="21m00Tcm4TlUPJeGCAgmA",
                model="eleven_turbo_v2_5"
            )
        )
        # Set background color *once*
        self.camera.background_color = "#000000"

        # ==========================================================
        # SCENE 1: The Cookie Jar Paradox
        # ==========================================================
        # Clear any existing mobjects
        if self.mobjects:
            self.play(*[FadeOut(obj) for obj in self.mobjects], run_time=0.5)
        # Narration: "You're standing in front of a cookie jar with three cookies inside."
        # Visual: Draw a glass jar at CENTER with three cookies: one small (1), one medium (5), one large (10). Label each with its value.
        with self.voiceover(text="You're standing in front of a cookie jar with three cookies inside.") as tracker:
            # Create jar (glass cylinder effect)
            jar_body = Rectangle(width=3, height=4, color=BLUE, stroke_width=3).set_fill(opacity=0.1)
            jar_top = Ellipse(width=3, height=0.6, color=BLUE, stroke_width=3).set_fill(BLUE, opacity=0.1)
            jar_top.move_to(jar_body.get_top())
            jar = VGroup(jar_body, jar_top).move_to(ORIGIN)
            # Create cookies with labels
            cookie1 = Circle(radius=0.25, color=ORANGE, fill_opacity=0.8).shift(LEFT * 0.8 + DOWN * 0.5)
            label1 = MathTex("1", color=WHITE).scale(0.6).move_to(cookie1)
            cookie5 = Circle(radius=0.35, color=ORANGE, fill_opacity=0.8).shift(RIGHT * 0.8 + DOWN * 0.5)
            label5 = MathTex("5", color=WHITE).scale(0.7).move_to(cookie5)
            cookie10 = Circle(radius=0.5, color=ORANGE, fill_opacity=0.8).shift(UP * 0.3)
            label10 = MathTex("10", color=WHITE).scale(0.8).move_to(cookie10)
            cookies_group = VGroup(cookie1, label1, cookie5, label5, cookie10, label10)
            # Animate jar appearing
            self.play(
                DrawBorderThenFill(jar),
                run_time=tracker.duration * 0.4
            )
            # Animate cookies dropping in with lag
            self.play(
                LaggedStart(
                    FadeIn(VGroup(cookie1, label1), shift=DOWN * 0.5),
                    FadeIn(VGroup(cookie5, label5), shift=DOWN * 0.5),
                    FadeIn(VGroup(cookie10, label10), shift=DOWN * 0.5),
                    lag_ratio=0.3
                ),
                run_time=tracker.duration * 0.6
            )
        # Narration: "The rule is simple: always take the biggest cookie you can see."
        # Visual: Animate a hand reaching in and grabbing the cookie labeled 10. Show +10 points appearing.
        with self.voiceover(text="The rule is simple: always take the biggest cookie you can see.") as tracker:
            # Create hand (simplified as arrow pointing down)
            hand = Arrow(start=UP * 3 + LEFT * 0.5, end=UP * 1.5, color=YELLOW, buff=0, stroke_width=8)
            # Animate hand reaching
            self.play(
                GrowFromEdge(hand, edge=UP),
                run_time=tracker.duration * 0.4
            )
            # Emphasize the biggest cookie
            self.play(
                Indicate(VGroup(cookie10, label10), color=YELLOW, scale_factor=1.3),
                run_time=tracker.duration * 0.3
            )
            # Grab animation
            self.play(
                hand.animate.shift(DOWN * 1.2),
                VGroup(cookie10, label10).animate.shift(UP * 0.5).scale(0.8),
                run_time=tracker.duration * 0.3
            )
        # Narration: "Seems smart, right? You got ten points."
        # Visual: Display running total: 'Score: 10' in top right corner with a checkmark.
        with self.voiceover(text="Seems smart, right? You got ten points.") as tracker:
            # Show +10 points
            plus_ten = MathTex("+10", color=GREEN).scale(1.2).next_to(cookie10, UP)
            self.play(
                FadeIn(plus_ten, shift=UP * 0.3),
                run_time=tracker.duration * 0.4
            )
            # Move cookie and hand away
            self.play(
                FadeOut(VGroup(cookie10, label10, hand), shift=UP * 2),
                run_time=tracker.duration * 0.3
            )
            # Create score display
            score_box = Rectangle(width=2, height=0.8, color=GREEN, stroke_width=2).to_corner(UR, buff=0.5)
            score_text = Text("Score: 10", color=GREEN).scale(0.6).move_to(score_box)
            checkmark = MathTex(r"\checkmark", color=GREEN).scale(0.8).next_to(score_box, LEFT, buff=0.2)
            self.play(
                LaggedStart(
                    ReplacementTransform(plus_ten, score_text),
                    DrawBorderThenFill(score_box),
                    Write(checkmark),
                    lag_ratio=0.2
                ),
                run_time=tracker.duration * 0.3
            )
        # Narration: "But now the jar magically refills with two new cookies."
        # Visual: Animate two new cookies appearing: both labeled 15. The jar now has cookies: 1, 5, 15, 15.
        with self.voiceover(text="But now the jar magically refills with two new cookies.") as tracker:
            # Create sparkle effect
            sparkles = VGroup(*[
                Dot(jar.get_center() + np.array([np.random.uniform(-1, 1), np.random.uniform(-1, 1), 0]),
                    radius=0.05, color=YELLOW)
                for _ in range(20)
            ])
            self.play(
                FadeIn(sparkles, lag_ratio=0.05),
                run_time=tracker.duration * 0.3
            )
            # Create two new cookies labeled 15
            cookie15_a = Circle(radius=0.45, color=ORANGE, fill_opacity=0.8).shift(LEFT * 0.5 + UP * 0.8)
            label15_a = MathTex("15", color=WHITE).scale(0.75).move_to(cookie15_a)
            cookie15_b = Circle(radius=0.45, color=ORANGE, fill_opacity=0.8).shift(RIGHT * 0.5 + UP * 0.8)
            label15_b = MathTex("15", color=WHITE).scale(0.75).move_to(cookie15_b)
            self.play(
                FadeOut(sparkles),
                LaggedStart(
                    FadeIn(VGroup(cookie15_a, label15_a), shift=DOWN * 0.5, scale=0.5),
                    FadeIn(VGroup(cookie15_b, label15_b), shift=DOWN * 0.5, scale=0.5),
                    lag_ratio=0.3
                ),
                run_time=tracker.duration * 0.7
            )
        # Narration: "Here's the twist: you can only take one more cookie total."
        # Visual: Show 'Moves Left: 1' counter appearing. Dim the hand to show limitation.
        with self.voiceover(text="Here's the twist: you can only take one more cookie total.") as tracker:
            # Create moves counter
            moves_box = Rectangle(width=2.2, height=0.8, color=RED, stroke_width=2).to_corner(UL, buff=0.5)
            moves_text = Text("Moves Left: 1", color=RED).scale(0.5).move_to(moves_box)
            self.play(
                DrawBorderThenFill(moves_box),
                Write(moves_text, lag_ratio=0.1),
                run_time=tracker.duration * 0.5
            )
            # Dim all cookies to show limitation
            self.play(
                VGroup(cookie1, label1, cookie5, label5, cookie15_a, label15_a, cookie15_b, label15_b).animate.set_opacity(0.5),
                run_time=tracker.duration * 0.5
            )
        # Narration: "Your greedy choice locked you out of thirty points."
        # Visual: Show the two 15-cookies glowing unreachable. Display 'Possible: 10' vs 'Optimal: 30' in red.
        with self.voiceover(text="Your greedy choice locked you out of thirty points.") as tracker:
            # Restore opacity and make 15-cookies glow
            self.play(
                VGroup(cookie1, label1, cookie5, label5, cookie15_a, label15_a, cookie15_b, label15_b).animate.set_opacity(1),
                run_time=tracker.duration * 0.2
            )
            self.play(
                Indicate(VGroup(cookie15_a, label15_a), color=YELLOW, scale_factor=1.2),
                Indicate(VGroup(cookie15_b, label15_b), color=YELLOW, scale_factor=1.2),
                run_time=tracker.duration * 0.3
            )
            # Show comparison
            comparison = VGroup(
                Text("Possible: 10", color=RED).scale(0.6),
                Text("vs", color=WHITE).scale(0.5),
                Text("Optimal: 30", color=GREEN).scale(0.6)
            ).arrange(RIGHT, buff=0.3).next_to(jar, DOWN, buff=0.8)
            self.play(
                Write(comparison, lag_ratio=0.1),
                run_time=tracker.duration * 0.5
            )
        # Narration: "What if you had waited? Taken the small cookie first?"
        # Visual: Rewind animation. Show hand taking cookie 1 instead. Display +1 points.
        with self.voiceover(text="What if you had waited? Taken the small cookie first?") as tracker:
            # Fade out current scene elements except jar
            self.play(
                FadeOut(VGroup(cookie1, label1, cookie5, label5, cookie15_a, label15_a, cookie15_b, label15_b)),
                FadeOut(comparison),
                FadeOut(score_box),
                FadeOut(score_text),
                FadeOut(checkmark),
                FadeOut(moves_box),
                FadeOut(moves_text),
                run_time=tracker.duration * 0.2
            )
            # Reset: show original three cookies again
            cookie1_new = Circle(radius=0.25, color=ORANGE, fill_opacity=0.8).shift(LEFT * 0.8 + DOWN * 0.5)
            label1_new = MathTex("1", color=WHITE).scale(0.6).move_to(cookie1_new)
            cookie5_new = Circle(radius=0.35, color=ORANGE, fill_opacity=0.8).shift(RIGHT * 0.8 + DOWN * 0.5)
            label5_new = MathTex("5", color=WHITE).scale(0.7).move_to(cookie5_new)
            cookie10_new = Circle(radius=0.5, color=ORANGE, fill_opacity=0.8).shift(UP * 0.3)
            label10_new = MathTex("10", color=WHITE).scale(0.8).move_to(cookie10_new)
            self.play(
                LaggedStart(
                    FadeIn(VGroup(cookie1_new, label1_new), shift=DOWN * 0.3),
                    FadeIn(VGroup(cookie5_new, label5_new), shift=DOWN * 0.3),
                    FadeIn(VGroup(cookie10_new, label10_new), shift=DOWN * 0.3),
                    lag_ratio=0.2
                ),
                run_time=tracker.duration * 0.3
            )
            # Create new hand
            hand2 = Arrow(start=UP * 3 + LEFT * 1.5, end=UP * 1.5 + LEFT * 0.8, color=BLUE, buff=0, stroke_width=8)
            # Emphasize small cookie
            self.play(
                Circumscribe(VGroup(cookie1_new, label1_new), color=BLUE),
                run_time=tracker.duration * 0.2
            )
            # Grab small cookie
            self.play(
                GrowFromEdge(hand2, edge=UP),
                run_time=tracker.duration * 0.15
            )
            self.play(
                hand2.animate.move_to(cookie1_new.get_center() + UP * 0.5),
                VGroup(cookie1_new, label1_new).animate.shift(UP * 0.3).scale(0.8),
                run_time=tracker.duration * 0.15
            )
        # Narration: "The jar refills the same way, but now you can grab both fifteens."
        # Visual: Animate hand taking both 15-cookies in sequence. Show +15, +15 appearing. Final score: 31.
        with self.voiceover(text="The jar refills the same way, but now you can grab both fifteens.") as tracker:
            # Show +1
            plus_one = MathTex("+1", color=GREEN).scale(0.8).next_to(cookie1_new, UP)
            self.play(
                FadeIn(plus_one, shift=UP * 0.2),
                run_time=tracker.duration * 0.1
            )
            # Remove cookie and hand
            self.play(
                FadeOut(VGroup(cookie1_new, label1_new, hand2, plus_one), shift=UP),
                run_time=tracker.duration * 0.1
            )
            # Refill with sparkles
            sparkles2 = VGroup(*[
                Dot(jar.get_center() + np.array([np.random.uniform(-1, 1), np.random.uniform(-1, 1), 0]),
                    radius=0.05, color=YELLOW)
                for _ in range(15)
            ])
            self.play(
                FadeIn(sparkles2, lag_ratio=0.05),
                run_time=tracker.duration * 0.1
            )
            # Create two 15-cookies
            cookie15_c = Circle(radius=0.45, color=ORANGE, fill_opacity=0.8).shift(LEFT * 0.5 + UP * 0.5)
            label15_c = MathTex("15", color=WHITE).scale(0.75).move_to(cookie15_c)
            cookie15_d = Circle(radius=0.45, color=ORANGE, fill_opacity=0.8).shift(RIGHT * 0.5 + UP * 0.5)
            label15_d = MathTex("15", color=WHITE).scale(0.75).move_to(cookie15_d)
            self.play(
                FadeOut(sparkles2),
                FadeIn(VGroup(cookie15_c, label15_c, cookie15_d, label15_d), shift=DOWN * 0.4),
                run_time=tracker.duration * 0.15
            )
            # Grab first 15
            hand3 = Arrow(start=UP * 3 + LEFT * 0.8, end=UP * 1.5, color=BLUE, buff=0, stroke_width=8)
            self.play(
                GrowFromEdge(hand3, edge=UP),
                run_time=tracker.duration * 0.1
            )
            self.play(
                hand3.animate.move_to(cookie15_c.get_center() + UP * 0.5),
                VGroup(cookie15_c, label15_c).animate.shift(UP * 0.3),
                run_time=tracker.duration * 0.1
            )
            plus_fifteen_a = MathTex("+15", color=GREEN).scale(1).next_to(cookie15_c, RIGHT)
            self.play(
                FadeIn(plus_fifteen_a, shift=UP * 0.2),
                run_time=tracker.duration * 0.08
            )
            self.play(
                FadeOut(VGroup(cookie15_c, label15_c, hand3), shift=UP),
                run_time=tracker.duration * 0.08
            )
            # Grab second 15
            hand4 = Arrow(start=UP * 3 + RIGHT * 0.8, end=UP * 1.5, color=BLUE, buff=0, stroke_width=8)
            self.play(
                GrowFromEdge(hand4, edge=UP),
                run_time=tracker.duration * 0.1
            )
            self.play(
                hand4.animate.move_to(cookie15_d.get_center() + UP * 0.5),
                VGroup(cookie15_d, label15_d).animate.shift(UP * 0.3),
                run_time=tracker.duration * 0.1
            )
            plus_fifteen_b = MathTex("+15", color=GREEN).scale(1).next_to(cookie15_d, LEFT)
            self.play(
                FadeIn(plus_fifteen_b, shift=UP * 0.2),
                run_time=tracker.duration * 0.08
            )
            self.play(
                FadeOut(VGroup(cookie15_d, label15_d, hand4), shift=UP),
                run_time=tracker.duration * 0.05
            )
        # Narration: "Being greedy gave you ten. Being strategic gave you thirty-one."
        # Visual: Split screen: left shows 'Greedy: 10' with sad face, right shows 'Strategic: 31' with trophy.
        with self.voiceover(text="Being greedy gave you ten. Being strategic gave you thirty-one.") as tracker:
            # Clear jar and remaining elements
            self.play(
                FadeOut(jar),
                FadeOut(cookie5_new),
                FadeOut(label5_new),
                FadeOut(cookie10_new),
                FadeOut(label10_new),
                FadeOut(plus_fifteen_a),
                FadeOut(plus_fifteen_b),
                run_time=tracker.duration * 0.2
            )
            # Create split screen
            divider = Line(UP * 3, DOWN * 3, color=WHITE, stroke_width=2)
            # Left side: Greedy
            greedy_title = Text("Greedy: 10", color=RED).scale(0.8).shift(LEFT * 3 + UP * 1.5)
            sad_face = Text(":(", color=RED).scale(2).shift(LEFT * 3 + DOWN * 0.5)
            # Right side: Strategic
            strategic_title = Text("Strategic: 31", color=GREEN).scale(0.8).shift(RIGHT * 3 + UP * 1.5)
            trophy = MathTex(r"\bigstar", color=GOLD).scale(3).shift(RIGHT * 3 + DOWN * 0.5)
            self.play(
                Create(divider),
                run_time=tracker.duration * 0.2
            )
            self.play(
                LaggedStart(
                    Write(greedy_title, lag_ratio=0.1),
                    FadeIn(sad_face, shift=DOWN * 0.3),
                    lag_ratio=0.3
                ),
                run_time=tracker.duration * 0.4
            )
            self.play(
                LaggedStart(
                    Write(strategic_title, lag_ratio=0.1),
                    FadeIn(trophy, shift=DOWN * 0.3, scale=0.5),
                    lag_ratio=0.3
                ),
                run_time=tracker.duration * 0.4
            )
        # Narration: "So why does our intuition fail us here?"
        # Visual: Zoom out to show both paths as branching trees. Highlight the question mark at the root.
        with self.voiceover(text="So why does our intuition fail us here?") as tracker:
            # Fade out split screen
            self.play(
                FadeOut(VGroup(divider, greedy_title, sad_face, strategic_title, trophy)),
                run_time=tracker.duration * 0.2
            )
            # Create branching tree
            root = Dot(ORIGIN + UP * 2, radius=0.15, color=YELLOW)
            question = MathTex("?", color=YELLOW).scale(1.2).next_to(root, UP, buff=0.2)
            # Left branch (greedy)
            left_line = Line(root.get_center(), LEFT * 2.5 + DOWN * 0.5, color=RED, stroke_width=3)
            left_node = Circle(radius=0.4, color=RED, fill_opacity=0.8).move_to(LEFT * 2.5 + DOWN * 0.5)
            left_label = MathTex("10", color=WHITE).move_to(left_node)
            # Right branch (strategic)
            right_line = Line(root.get_center(), RIGHT * 2.5 + DOWN * 0.5, color=GREEN, stroke_width=3)
            right_node = Circle(radius=0.4, color=GREEN, fill_opacity=0.8).move_to(RIGHT * 2.5 + DOWN * 0.5)
            right_label = MathTex("1", color=WHITE).scale(0.8).move_to(right_node)
            # Right branch continuation
            right_line2 = Line(right_node.get_center(), RIGHT * 2.5 + DOWN * 2.5, color=GREEN, stroke_width=3)
            right_node2 = Circle(radius=0.5, color=GREEN, fill_opacity=0.8).move_to(RIGHT * 2.5 + DOWN * 2.5)
            right_label2 = MathTex("31", color=WHITE).scale(0.9).move_to(right_node2)
            self.play(
                GrowFromCenter(root),
                Write(question),
                run_time=tracker.duration * 0.2
            )
            self.play(
                LaggedStart(
                    Create(left_line),
                    GrowFromCenter(left_node),
                    Write(left_label),
                    lag_ratio=0.3
                ),
                run_time=tracker.duration * 0.3
            )
            self.play(
                LaggedStart(
                    Create(right_line),
                    GrowFromCenter(right_node),
                    Write(right_label),
                    Create(right_line2),
                    GrowFromCenter(right_node2),
                    Write(right_label2),
                    lag_ratio=0.2
                ),
                run_time=tracker.duration * 0.4
            )
            # Emphasize the question
            self.play(
                Indicate(question, color=YELLOW, scale_factor=1.5),
                run_time=tracker.duration * 0.1
            )
        self.wait(2)


        # ==========================================================
        # SCENE 2: The Consulting Job Trap
        # ==========================================================
        # Clear any existing mobjects
        if self.mobjects:
            self.play(*[FadeOut(obj) for obj in self.mobjects], run_time=0.5)
        # Narration: "Let's make this concrete with a job scheduling problem."
        # Visual: Draw a timeline labeled 'Weeks' from 1 to 8 horizontally across the screen.
        with self.voiceover(text="Let's make this concrete with a job scheduling problem.") as tracker:
            timeline = Line(LEFT * 5.5, RIGHT * 5.5, color=WHITE).shift(DOWN * 1.5)
            week_labels = VGroup(*[
                Text(str(i), font_size=24).next_to(timeline.point_from_proportion(i / 8), DOWN, buff=0.3)
                for i in range(1, 9)
            ])
            weeks_title = Text("Weeks", font_size=28, color=YELLOW).next_to(timeline, LEFT, buff=0.5)
            self.play(
                Create(timeline),
                Write(weeks_title, lag_ratio=0.1),
                LaggedStart(*[FadeIn(label, shift=DOWN*0.2) for label in week_labels], lag_ratio=0.1),
                run_time=tracker.duration
            )
        # Narration: "You're a consultant with three types of jobs available each week."
        # Visual: Create three job cards above the timeline: 'No Work: $0', 'Low Stress: $10', 'High Stress: $50'.
        with self.voiceover(text="You're a consultant with three types of jobs available each week.") as tracker:
            card_width = 2.2
            card_height = 1.2
            no_work_card = VGroup(
                Rectangle(width=card_width, height=card_height, color=GRAY, fill_opacity=0.2),
                Text("No Work", font_size=22, color=GRAY),
                Text("$0", font_size=28, color=GRAY, weight=BOLD).shift(DOWN * 0.3)
            ).arrange(DOWN, buff=0.15).shift(LEFT * 3.5 + UP * 1.5)
            low_stress_card = VGroup(
                Rectangle(width=card_width, height=card_height, color=BLUE, fill_opacity=0.2),
                Text("Low Stress", font_size=22, color=BLUE),
                Text("$10", font_size=28, color=BLUE, weight=BOLD).shift(DOWN * 0.3)
            ).arrange(DOWN, buff=0.15).shift(UP * 1.5)
            high_stress_card = VGroup(
                Rectangle(width=card_width, height=card_height, color=RED, fill_opacity=0.2),
                Text("High Stress", font_size=22, color=RED),
                Text("$50", font_size=28, color=RED, weight=BOLD).shift(DOWN * 0.3)
            ).arrange(DOWN, buff=0.15).shift(RIGHT * 3.5 + UP * 1.5)
            self.play(
                LaggedStart(
                    FadeIn(no_work_card, shift=DOWN*0.4),
                    FadeIn(low_stress_card, shift=DOWN*0.4),
                    FadeIn(high_stress_card, shift=DOWN*0.4),
                    lag_ratio=0.3
                ),
                run_time=tracker.duration
            )
        # Narration: "Low stress jobs are easy. You can do them anytime."
        # Visual: Animate the Low Stress card with a calm blue color and gentle pulse.
        with self.voiceover(text="Low stress jobs are easy. You can do them anytime.") as tracker:
            self.play(
                Indicate(low_stress_card, color=BLUE, scale_factor=1.15),
                low_stress_card[0].animate.set_fill(BLUE, opacity=0.4),
                run_time=tracker.duration
            )
            self.play(low_stress_card.animate.scale(1.05).scale(1/1.05), rate_func=smooth, run_time=0.6)
        # Narration: "High stress jobs pay great, but there's a catch."
        # Visual: Animate the High Stress card with intense red color and aggressive pulse.
        with self.voiceover(text="High stress jobs pay great, but there's a catch.") as tracker:
            self.play(
                Indicate(high_stress_card, color=RED, scale_factor=1.2),
                high_stress_card[0].animate.set_fill(RED, opacity=0.5),
                Flash(high_stress_card.get_center(), color=RED, flash_radius=0.8),
                run_time=tracker.duration
            )
            self.play(
                high_stress_card.animate.scale(1.1).scale(1/1.1),
                rate_func=there_and_back,
                run_time=0.5
            )
        # Narration: "You can only take a high stress job if you rested the previous week."
        # Visual: Show a lock icon appearing on the High Stress card with text: 'Requires: Rest Last Week'.
        with self.voiceover(text="You can only take a high stress job if you rested the previous week.") as tracker:
            lock_body = Rectangle(width=0.25, height=0.3, color=YELLOW, fill_opacity=1)
            lock_shackle = Arc(radius=0.15, start_angle=0, angle=PI, color=YELLOW, stroke_width=6)
            lock_shackle.next_to(lock_body, UP, buff=0)
            lock_icon = VGroup(lock_shackle, lock_body).scale(0.8).next_to(high_stress_card, RIGHT, buff=0.3)
            requirement_text = Text("Requires: Rest Last Week", font_size=18, color=YELLOW).next_to(lock_icon, DOWN, buff=0.2)
            self.play(
                GrowFromCenter(lock_icon),
                Write(requirement_text, lag_ratio=0.05),
                run_time=tracker.duration
            )
            self.play(Circumscribe(VGroup(lock_icon, requirement_text), color=YELLOW, run_time=1.0))
        # Narration: "The greedy approach says: always take the highest paying job available."
        # Visual: Highlight the High Stress card with a glowing border and text: 'Greedy Choice: $50'.
        with self.voiceover(text="The greedy approach says: always take the highest paying job available.") as tracker:
            glow_rect = SurroundingRectangle(high_stress_card, color=GOLD, buff=0.15, stroke_width=6)
            greedy_text = Text("Greedy Choice: $50", font_size=24, color=GOLD, weight=BOLD).next_to(high_stress_card, UP, buff=0.3)
            self.play(
                Create(glow_rect),
                Write(greedy_text, lag_ratio=0.08),
                run_time=tracker.duration
            )
            self.play(Flash(high_stress_card.get_center(), color=GOLD, flash_radius=1.2), run_time=0.8)
        # Store job blocks for the timeline
        job_blocks = []
        total_money = 0
        # Narration: "Week one: you rest, because you have to start somewhere."
        # Visual: Place a gray 'Rest' block on week 1. Show 'Total: $0'.
        with self.voiceover(text="Week one: you rest, because you have to start somewhere.") as tracker:
            week1_pos = timeline.point_from_proportion(0.5 / 8) + UP * 0.5
            rest_block = VGroup(
                Rectangle(width=0.8, height=0.6, color=GRAY, fill_opacity=0.6),
                Text("Rest", font_size=16, color=WHITE)
            ).arrange(DOWN, buff=0.05).move_to(week1_pos)
            total_display = Text(f"Total: ${total_money}", font_size=28, color=GREEN).to_edge(UP).shift(DOWN * 0.3)
            self.play(
                FadeIn(rest_block, shift=DOWN*0.3),
                Write(total_display, lag_ratio=0.1),
                run_time=tracker.duration
            )
            job_blocks.append(rest_block)
        # Narration: "Week two: now you can take the high stress job. Fifty dollars!"
        # Visual: Place a red 'High Stress' block on week 2. Animate +$50. Show 'Total: $50'.
        with self.voiceover(text="Week two: now you can take the high stress job. Fifty dollars!") as tracker:
            week2_pos = timeline.point_from_proportion(1.5 / 8) + UP * 0.5
            high_block = VGroup(
                Rectangle(width=0.8, height=0.6, color=RED, fill_opacity=0.7),
                Text("High", font_size=16, color=WHITE, weight=BOLD)
            ).arrange(DOWN, buff=0.05).move_to(week2_pos)
            plus_50 = Text("+$50", font_size=32, color=GREEN, weight=BOLD).next_to(high_block, UP, buff=0.3)
            total_money += 50
            new_total = Text(f"Total: ${total_money}", font_size=28, color=GREEN).to_edge(UP).shift(DOWN * 0.3)
            self.play(
                FadeIn(high_block, shift=DOWN*0.3),
                FadeIn(plus_50, shift=UP*0.2),
                run_time=tracker.duration * 0.6
            )
            self.play(
                Transform(total_display, new_total),
                FadeOut(plus_50, shift=UP*0.3),
                run_time=tracker.duration * 0.4
            )
            self.play(Flash(high_block.get_center(), color=RED), run_time=0.5)
            job_blocks.append(high_block)
        # Narration: "Week three: you're exhausted. High stress is locked. Take low stress."
        # Visual: Show lock icon on High Stress. Place blue 'Low Stress' block on week 3. Show +$10. 'Total: $60'.
        with self.voiceover(text="Week three: you're exhausted. High stress is locked. Take low stress.") as tracker:
            # Show lock briefly
            temp_lock = lock_icon.copy().scale(1.5).move_to(high_stress_card.get_center())
            self.play(FadeIn(temp_lock, scale=0.5), run_time=tracker.duration * 0.25)
            week3_pos = timeline.point_from_proportion(2.5 / 8) + UP * 0.5
            low_block = VGroup(
                Rectangle(width=0.8, height=0.6, color=BLUE, fill_opacity=0.7),
                Text("Low", font_size=16, color=WHITE)
            ).arrange(DOWN, buff=0.05).move_to(week3_pos)
            plus_10 = Text("+$10", font_size=28, color=GREEN).next_to(low_block, UP, buff=0.3)
            total_money += 10
            new_total = Text(f"Total: ${total_money}", font_size=28, color=GREEN).to_edge(UP).shift(DOWN * 0.3)
            self.play(
                FadeOut(temp_lock),
                FadeIn(low_block, shift=DOWN*0.3),
                FadeIn(plus_10, shift=UP*0.2),
                run_time=tracker.duration * 0.5
            )
            self.play(
                Transform(total_display, new_total),
                FadeOut(plus_10, shift=UP*0.3),
                run_time=tracker.duration * 0.25
            )
            job_blocks.append(low_block)
        # Narration: "This pattern continues: you're trapped alternating between low stress and exhaustion."
        # Visual: Fast-forward animation showing weeks 4-8 filling with alternating Low Stress and High Stress. Final total: $180.
        with self.voiceover(text="This pattern continues: you're trapped alternating between low stress and exhaustion.") as tracker:
            remaining_blocks = []
            money_animations = []
            # Week 4: High Stress
            week4_pos = timeline.point_from_proportion(3.5 / 8) + UP * 0.5
            high_block4 = VGroup(
                Rectangle(width=0.8, height=0.6, color=RED, fill_opacity=0.7),
                Text("High", font_size=16, color=WHITE, weight=BOLD)
            ).arrange(DOWN, buff=0.05).move_to(week4_pos)
            remaining_blocks.append(high_block4)
            total_money += 50
            # Week 5: Low Stress
            week5_pos = timeline.point_from_proportion(4.5 / 8) + UP * 0.5
            low_block5 = VGroup(
                Rectangle(width=0.8, height=0.6, color=BLUE, fill_opacity=0.7),
                Text("Low", font_size=16, color=WHITE)
            ).arrange(DOWN, buff=0.05).move_to(week5_pos)
            remaining_blocks.append(low_block5)
            total_money += 10
            # Week 6: High Stress
            week6_pos = timeline.point_from_proportion(5.5 / 8) + UP * 0.5
            high_block6 = VGroup(
                Rectangle(width=0.8, height=0.6, color=RED, fill_opacity=0.7),
                Text("High", font_size=16, color=WHITE, weight=BOLD)
            ).arrange(DOWN, buff=0.05).move_to(week6_pos)
            remaining_blocks.append(high_block6)
            total_money += 50
            # Week 7: Low Stress
            week7_pos = timeline.point_from_proportion(6.5 / 8) + UP * 0.5
            low_block7 = VGroup(
                Rectangle(width=0.8, height=0.6, color=BLUE, fill_opacity=0.7),
                Text("Low", font_size=16, color=WHITE)
            ).arrange(DOWN, buff=0.05).move_to(week7_pos)
            remaining_blocks.append(low_block7)
            total_money += 10
            # Week 8: High Stress
            week8_pos = timeline.point_from_proportion(7.5 / 8) + UP * 0.5
            high_block8 = VGroup(
                Rectangle(width=0.8, height=0.6, color=RED, fill_opacity=0.7),
                Text("High", font_size=16, color=WHITE, weight=BOLD)
            ).arrange(DOWN, buff=0.05).move_to(week8_pos)
            remaining_blocks.append(high_block8)
            total_money += 50
            final_total = Text(f"Total: ${total_money}", font_size=28, color=GREEN).to_edge(UP).shift(DOWN * 0.3)
            self.play(
                LaggedStart(*[FadeIn(block, shift=DOWN*0.3) for block in remaining_blocks], lag_ratio=0.15),
                run_time=tracker.duration * 0.7
            )
            self.play(
                Transform(total_display, final_total),
                run_time=tracker.duration * 0.3
            )
            # Emphasize the trap pattern
            all_job_blocks = VGroup(*job_blocks, *remaining_blocks)
            self.play(Circumscribe(all_job_blocks, color=YELLOW, stroke_width=4, run_time=1.5))
        self.wait(2)


        # ==========================================================
        # SCENE 3: The Hidden Pattern
        # ==========================================================
        # Clear the scene
        if self.mobjects:
            self.play(*[FadeOut(obj) for obj in self.mobjects], run_time=0.5)
        # Create timeline structure (reusable)
        def create_timeline():
            timeline = VGroup()
            for i in range(8):
                box = Square(side_length=0.6, color=WHITE, stroke_width=2)
                box.set_fill(color=BLACK, opacity=0.3)
                week_label = Text(f"W{i+1}", font_size=16).move_to(box.get_center())
                week_group = VGroup(box, week_label)
                timeline.add(week_group)
            timeline.arrange(RIGHT, buff=0.15)
            return timeline
        # Narration: "But what if we tried a different pattern?"
        # Visual: Clear the timeline. Show a question mark hovering above it.
        with self.voiceover(text="But what if we tried a different pattern?") as tracker:
            timeline = create_timeline()
            timeline.move_to(ORIGIN)
            question_mark = MathTex(r"?", font_size=80, color=YELLOW)
            question_mark.next_to(timeline, UP, buff=0.5)
            self.play(
                FadeIn(timeline, shift=DOWN*0.3, lag_ratio=0.05),
                run_time=tracker.duration * 0.6
            )
            self.play(
                Write(question_mark, lag_ratio=0.1),
                run_time=tracker.duration * 0.4
            )
        # Narration: "What if we strategically rest every other week?"
        # Visual: Place alternating Rest and High Stress blocks: Rest, High, Rest, High, Rest, High, Rest, High.
        with self.voiceover(text="What if we strategically rest every other week?") as tracker:
            self.play(FadeOut(question_mark, shift=UP*0.3), run_time=0.3)
            pattern_blocks = VGroup()
            for i in range(8):
                box = timeline[i][0]
                if i % 2 == 0:  # Rest
                    block = Rectangle(width=0.5, height=0.5, color=GRAY, stroke_width=2)
                    block.set_fill(color=GRAY, opacity=0.5)
                    label = Text("R", font_size=20, color=WHITE)
                else:  # High Stress
                    block = Rectangle(width=0.5, height=0.5, color=RED, stroke_width=2)
                    block.set_fill(color=RED, opacity=0.7)
                    label = Text("H", font_size=20, color=WHITE)
                label.move_to(block.get_center())
                block_group = VGroup(block, label)
                block_group.move_to(box.get_center())
                pattern_blocks.add(block_group)
            self.play(
                LaggedStart(*[FadeIn(block, shift=DOWN*0.2) for block in pattern_blocks], lag_ratio=0.1),
                run_time=tracker.duration
            )
        # Narration: "Week one: rest. Week two: high stress. Week three: rest again."
        # Visual: Animate placing first three blocks with running total: $0, $50, $50.
        with self.voiceover(text="Week one: rest. Week two: high stress. Week three: rest again.") as tracker:
            total_label = Text("Total: $0", font_size=28, color=GREEN).to_edge(UP)
            self.play(FadeIn(total_label, shift=DOWN*0.2), run_time=0.3)
            # Week 1: Rest
            self.play(Indicate(pattern_blocks[0], color=YELLOW, scale_factor=1.3), run_time=tracker.duration * 0.25)
            # Week 2: High Stress
            new_total_1 = Text("Total: $50", font_size=28, color=GREEN).move_to(total_label.get_center())
            self.play(
                Indicate(pattern_blocks[1], color=YELLOW, scale_factor=1.3),
                Transform(total_label, new_total_1),
                run_time=tracker.duration * 0.35
            )
            # Week 3: Rest
            new_total_2 = Text("Total: $50", font_size=28, color=GREEN).move_to(total_label.get_center())
            self.play(
                Indicate(pattern_blocks[2], color=YELLOW, scale_factor=1.3),
                Transform(total_label, new_total_2),
                run_time=tracker.duration * 0.4
            )
        # Narration: "This pattern gives us four high stress jobs over eight weeks."
        # Visual: Highlight all four High Stress blocks glowing red. Show calculation: 4 × $50 = $200.
        with self.voiceover(text="This pattern gives us four high stress jobs over eight weeks.") as tracker:
            high_stress_blocks = VGroup(pattern_blocks[1], pattern_blocks[3], pattern_blocks[5], pattern_blocks[7])
            self.play(
                LaggedStart(*[Indicate(block, color=RED, scale_factor=1.4) for block in high_stress_blocks], lag_ratio=0.15),
                run_time=tracker.duration * 0.6
            )
            calculation = MathTex(r"4 \times \$50 = \$200", font_size=36, color=YELLOW)
            calculation.next_to(timeline, DOWN, buff=0.6)
            self.play(Write(calculation, lag_ratio=0.1), run_time=tracker.duration * 0.4)
        # Narration: "Two hundred dollars beats the greedy approach by twenty dollars."
        # Visual: Show comparison: 'Greedy: $180' vs 'Strategic: $200'. Animate the strategic side winning.
        with self.voiceover(text="Two hundred dollars beats the greedy approach by twenty dollars.") as tracker:
            greedy_text = Text("Greedy: $180", font_size=32, color=RED).shift(LEFT*2.5 + DOWN*2)
            strategic_text = Text("Strategic: $200", font_size=32, color=GREEN).shift(RIGHT*2.5 + DOWN*2)
            self.play(
                FadeIn(greedy_text, shift=RIGHT*0.3),
                FadeIn(strategic_text, shift=LEFT*0.3),
                run_time=tracker.duration * 0.5
            )
            winner_arrow = Arrow(strategic_text.get_top(), strategic_text.get_top() + UP*0.5, color=GOLD, buff=0.1)
            winner_star = Text("★", font_size=48, color=GOLD).next_to(winner_arrow, UP, buff=0.1)
            self.play(
                GrowFromCenter(winner_arrow),
                FadeIn(winner_star, shift=DOWN*0.2, scale=1.5),
                strategic_text.animate.set_color(GOLD),
                run_time=tracker.duration * 0.5
            )
        # Narration: "But wait, there's an even better pattern hiding here."
        # Visual: Clear timeline again. Show multiple question marks appearing.
        with self.voiceover(text="But wait, there's an even better pattern hiding here.") as tracker:
            self.play(
                *[FadeOut(obj, shift=DOWN*0.3) for obj in [pattern_blocks, calculation, greedy_text, strategic_text, winner_arrow, winner_star, total_label]],
                run_time=0.5
            )
            question_marks = VGroup(*[
                MathTex(r"?", font_size=50, color=YELLOW).move_to(
                    ORIGIN + np.array([np.cos(i * TAU / 5) * 1.5, np.sin(i * TAU / 5) * 1.5, 0])
                ) for i in range(5)
            ])
            self.play(
                LaggedStart(*[FadeIn(qm, shift=DOWN*0.2, scale=1.5) for qm in question_marks], lag_ratio=0.15),
                run_time=tracker.duration
            )
        # Narration: "What if we rest, then do two low stress jobs, then rest again?"
        # Visual: Place pattern: Rest, Low, Low, Rest, Low, Low, Rest, Low. Show blocks appearing.
        with self.voiceover(text="What if we rest, then do two low stress jobs, then rest again?") as tracker:
            self.play(FadeOut(question_marks, shift=UP*0.3), run_time=0.3)
            new_pattern_blocks = VGroup()
            pattern_sequence = ["R", "L", "L", "R", "L", "L", "R", "L"]
            for i in range(8):
                box = timeline[i][0]
                if pattern_sequence[i] == "R":  # Rest
                    block = Rectangle(width=0.5, height=0.5, color=GRAY, stroke_width=2)
                    block.set_fill(color=GRAY, opacity=0.5)
                    label = Text("R", font_size=20, color=WHITE)
                else:  # Low Stress
                    block = Rectangle(width=0.5, height=0.5, color=BLUE, stroke_width=2)
                    block.set_fill(color=BLUE, opacity=0.7)
                    label = Text("L", font_size=20, color=WHITE)
                label.move_to(block.get_center())
                block_group = VGroup(block, label)
                block_group.move_to(box.get_center())
                new_pattern_blocks.add(block_group)
            self.play(
                LaggedStart(*[FadeIn(block, shift=DOWN*0.2) for block in new_pattern_blocks], lag_ratio=0.12),
                run_time=tracker.duration
            )
        # Narration: "That's five low stress jobs: fifty dollars total."
        # Visual: Count the blue blocks: 1, 2, 3, 4, 5. Show calculation: 5 × $10 = $50.
        with self.voiceover(text="That's five low stress jobs: fifty dollars total.") as tracker:
            low_stress_indices = [1, 2, 4, 5, 7]
            counter_labels = VGroup()
            for idx, i in enumerate(low_stress_indices):
                counter = Text(str(idx + 1), font_size=24, color=YELLOW)
                counter.next_to(new_pattern_blocks[i], UP, buff=0.2)
                counter_labels.add(counter)
                self.play(
                    FadeIn(counter, shift=DOWN*0.2, scale=1.5),
                    Indicate(new_pattern_blocks[i], color=YELLOW, scale_factor=1.3),
                    run_time=tracker.duration * 0.15
                )
            calculation_2 = MathTex(r"5 \times \$10 = \$50", font_size=36, color=BLUE)
            calculation_2.next_to(timeline, DOWN, buff=0.6)
            self.play(Write(calculation_2, lag_ratio=0.1), run_time=tracker.duration * 0.25)
        # Narration: "Okay, that's worse. So the rest-high pattern is optimal?"
        # Visual: Show three strategies side by side: Greedy ($180), Rest-High ($200), Rest-Low-Low ($50).
        with self.voiceover(text="Okay, that's worse. So the rest-high pattern is optimal?") as tracker:
            self.play(
                *[FadeOut(obj, shift=DOWN*0.3) for obj in [timeline, new_pattern_blocks, counter_labels, calculation_2]],
                run_time=0.4
            )
            strategy_1 = VGroup(
                Text("Greedy", font_size=24, color=WHITE),
                Text("$180", font_size=32, color=RED)
            ).arrange(DOWN, buff=0.2).shift(LEFT*3.5)
            strategy_2 = VGroup(
                Text("Rest-High", font_size=24, color=WHITE),
                Text("$200", font_size=32, color=GREEN)
            ).arrange(DOWN, buff=0.2).shift(ORIGIN)
            strategy_3 = VGroup(
                Text("Rest-Low-Low", font_size=24, color=WHITE),
                Text("$50", font_size=32, color=BLUE)
            ).arrange(DOWN, buff=0.2).shift(RIGHT*3.5)
            self.play(
                LaggedStart(
                    FadeIn(strategy_1, shift=RIGHT*0.3),
                    FadeIn(strategy_2, shift=UP*0.3),
                    FadeIn(strategy_3, shift=LEFT*0.3),
                    lag_ratio=0.2
                ),
                run_time=tracker.duration * 0.7
            )
            question_mark_2 = MathTex(r"?", font_size=60, color=YELLOW).next_to(strategy_2, UP, buff=0.3)
            self.play(Write(question_mark_2, lag_ratio=0.1), run_time=tracker.duration * 0.3)
        # Narration: "Actually, the true optimal mixes patterns in a way that's not obvious at all."
        # Visual: Show a complex optimal pattern appearing: Rest, High, Low, Low, Rest, High, Low, Low. Total: $220.
        with self.voiceover(text="Actually, the true optimal mixes patterns in a way that's not obvious at all.") as tracker:
            self.play(
                *[FadeOut(obj, shift=DOWN*0.3) for obj in [strategy_1, strategy_2, strategy_3, question_mark_2]],
                run_time=0.4
            )
            optimal_timeline = create_timeline()
            optimal_timeline.move_to(ORIGIN + UP*0.5)
            self.play(FadeIn(optimal_timeline, shift=DOWN*0.3, lag_ratio=0.05), run_time=0.4)
            optimal_pattern_blocks = VGroup()
            optimal_sequence = ["R", "H", "L", "L", "R", "H", "L", "L"]
            for i in range(8):
                box = optimal_timeline[i][0]
                if optimal_sequence[i] == "R":  # Rest
                    block = Rectangle(width=0.5, height=0.5, color=GRAY, stroke_width=2)
                    block.set_fill(color=GRAY, opacity=0.5)
                    label = Text("R", font_size=20, color=WHITE)
                elif optimal_sequence[i] == "H":  # High Stress
                    block = Rectangle(width=0.5, height=0.5, color=RED, stroke_width=2)
                    block.set_fill(color=RED, opacity=0.7)
                    label = Text("H", font_size=20, color=WHITE)
                else:  # Low Stress
                    block = Rectangle(width=0.5, height=0.5, color=BLUE, stroke_width=2)
                    block.set_fill(color=BLUE, opacity=0.7)
                    label = Text("L", font_size=20, color=WHITE)
                label.move_to(block.get_center())
                block_group = VGroup(block, label)
                block_group.move_to(box.get_center())
                optimal_pattern_blocks.add(block_group)
            self.play(
                LaggedStart(*[FadeIn(block, shift=DOWN*0.2, scale=1.2) for block in optimal_pattern_blocks], lag_ratio=0.1),
                run_time=tracker.duration * 0.5
            )
            optimal_label = Text("OPTIMAL PATTERN", font_size=28, color=GOLD, weight=BOLD)
            optimal_label.next_to(optimal_timeline, UP, buff=0.5)
            optimal_total = MathTex(r"\$50 + \$20 + \$20 + \$50 + \$20 + \$20 = \$220", font_size=32, color=GOLD)
            optimal_total.next_to(optimal_timeline, DOWN, buff=0.6)
            self.play(
                Write(optimal_label, lag_ratio=0.1),
                run_time=tracker.duration * 0.25
            )
            self.play(
                Write(optimal_total, lag_ratio=0.05),
                run_time=tracker.duration * 0.25
            )
            # Final emphasis
            winner_box = SurroundingRectangle(VGroup(optimal_timeline, optimal_pattern_blocks, optimal_total), color=GOLD, buff=0.3, stroke_width=4)
            self.play(Create(winner_box, rate_func=smooth), run_time=0.8)
        self.wait(2)


        # ==========================================================
        # SCENE 4: The Explosion of Possibilities
        # ==========================================================
        # Clear the scene
        if self.mobjects:
            self.play(*[FadeOut(obj) for obj in self.mobjects], run_time=0.5)
        # Create timeline at the bottom
        timeline = NumberLine(
            x_range=[0, 8],
            length=10,
            include_numbers=True,
            label_direction=DOWN,
            font_size=24
        ).to_edge(DOWN, buff=1.5)
        timeline_label = Text("Week", font_size=28).next_to(timeline, LEFT, buff=0.3)
        # Narration: "How do we find this optimal pattern without checking every possibility?"
        # Visual: Show the timeline with a branching tree growing above it, one branch per week.
        with self.voiceover(text="How do we find this optimal pattern without checking every possibility?") as tracker:
            self.play(
                Create(timeline),
                Write(timeline_label),
                run_time=tracker.duration * 0.6
            )
            # Create initial tree structure hint
            tree_root = Dot(timeline.number_to_point(0) + UP * 0.5, color=YELLOW, radius=0.08)
            self.play(
                GrowFromCenter(tree_root),
                run_time=tracker.duration * 0.4
            )
        # Narration: "Each week, we have three choices: rest, low stress, or high stress."
        # Visual: Animate the tree branching into three paths at week 1. Label them N, L, H.
        with self.voiceover(text="Each week, we have three choices: rest, low stress, or high stress.") as tracker:
            week1_pos = timeline.number_to_point(1)
            # Create three branches from root
            branch_n = Line(tree_root.get_center(), week1_pos + UP * 1.5, color=GRAY, stroke_width=3)
            branch_l = Line(tree_root.get_center(), week1_pos + UP * 2.5, color=BLUE, stroke_width=3)
            branch_h = Line(tree_root.get_center(), week1_pos + UP * 3.5, color=RED, stroke_width=3)
            node_n = Dot(week1_pos + UP * 1.5, color=GRAY, radius=0.07)
            node_l = Dot(week1_pos + UP * 2.5, color=BLUE, radius=0.07)
            node_h = Dot(week1_pos + UP * 3.5, color=RED, radius=0.07)
            label_n = Text("N", font_size=24, color=GRAY).next_to(node_n, RIGHT, buff=0.15)
            label_l = Text("L", font_size=24, color=BLUE).next_to(node_l, RIGHT, buff=0.15)
            label_h = Text("H", font_size=24, color=RED).next_to(node_h, RIGHT, buff=0.15)
            self.play(
                LaggedStart(
                    Create(branch_n),
                    Create(branch_l),
                    Create(branch_h),
                    lag_ratio=0.3
                ),
                run_time=tracker.duration * 0.5
            )
            self.play(
                LaggedStart(
                    GrowFromCenter(node_n),
                    GrowFromCenter(node_l),
                    GrowFromCenter(node_h),
                    FadeIn(label_n, shift=RIGHT * 0.2),
                    FadeIn(label_l, shift=RIGHT * 0.2),
                    FadeIn(label_h, shift=RIGHT * 0.2),
                    lag_ratio=0.2
                ),
                run_time=tracker.duration * 0.5
            )
        # Store first level nodes for next step
        first_level = VGroup(node_n, node_l, node_h)
        all_branches = VGroup(branch_n, branch_l, branch_h)
        all_labels = VGroup(label_n, label_l, label_h)
        # Narration: "Well, not quite. High stress is only available if we rested last week."
        # Visual: Show some branches marked with X (invalid). Only branches after Rest can have High.
        with self.voiceover(text="Well, not quite. High stress is only available if we rested last week.") as tracker:
            week2_pos = timeline.number_to_point(2)
            # From node_l (blue), create branches to week 2 - but mark H as invalid
            branch_l_to_n = Line(node_l.get_center(), week2_pos + UP * 2.0, color=GRAY, stroke_width=2)
            branch_l_to_l = Line(node_l.get_center(), week2_pos + UP * 2.5, color=BLUE, stroke_width=2)
            branch_l_to_h = Line(node_l.get_center(), week2_pos + UP * 3.0, color=RED, stroke_width=2, stroke_opacity=0.3)
            node_l_n = Dot(week2_pos + UP * 2.0, color=GRAY, radius=0.06)
            node_l_l = Dot(week2_pos + UP * 2.5, color=BLUE, radius=0.06)
            # X mark for invalid high stress after low stress
            x_mark = VGroup(
                Line(ORIGIN + UP * 0.1 + LEFT * 0.1, ORIGIN + DOWN * 0.1 + RIGHT * 0.1, color=RED, stroke_width=4),
                Line(ORIGIN + UP * 0.1 + RIGHT * 0.1, ORIGIN + DOWN * 0.1 + LEFT * 0.1, color=RED, stroke_width=4)
            ).move_to(week2_pos + UP * 3.0)
            self.play(
                Create(branch_l_to_n),
                Create(branch_l_to_l),
                Create(branch_l_to_h),
                run_time=tracker.duration * 0.4
            )
            self.play(
                GrowFromCenter(node_l_n),
                GrowFromCenter(node_l_l),
                Create(x_mark),
                run_time=tracker.duration * 0.3
            )
            # Show valid H branch from N (rest)
            branch_n_to_h = Line(node_n.get_center(), week2_pos + UP * 1.8, color=RED, stroke_width=2)
            node_n_h = Dot(week2_pos + UP * 1.8, color=RED, radius=0.06)
            checkmark = Text("✓", font_size=20, color=GREEN).move_to(week2_pos + UP * 1.8 + RIGHT * 0.3)
            self.play(
                Create(branch_n_to_h),
                GrowFromCenter(node_n_h),
                FadeIn(checkmark, scale=1.5),
                run_time=tracker.duration * 0.3
            )
        all_branches.add(branch_l_to_n, branch_l_to_l, branch_l_to_h, branch_n_to_h)
        second_level = VGroup(node_l_n, node_l_l, node_n_h)
        # Narration: "But even with constraints, the tree explodes exponentially."
        # Visual: Animate the tree growing to week 8. Show it filling the screen with hundreds of branches.
        with self.voiceover(text="But even with constraints, the tree explodes exponentially.") as tracker:
            # Create explosion of branches from week 2 to week 8
            explosion_branches = VGroup()
            explosion_nodes = VGroup()
            # Generate many branches spreading out
            for week in range(3, 9):
                week_pos = timeline.number_to_point(week)
                num_branches = min(30, 3 ** (week - 1))
                for i in range(num_branches):
                    # Random vertical spread
                    y_offset = UP * np.random.uniform(0.5, 5.5)
                    start_y = UP * np.random.uniform(0.5, 5.0)
                    if week == 3:
                        start_point = timeline.number_to_point(2) + start_y
                    else:
                        start_point = timeline.number_to_point(week - 1) + start_y
                    end_point = week_pos + y_offset
                    branch_color = np.random.choice([GRAY, BLUE, RED])
                    branch = Line(
                        start_point,
                        end_point,
                        color=branch_color,
                        stroke_width=max(0.5, 3 - week * 0.3),
                        stroke_opacity=max(0.2, 1 - week * 0.1)
                    )
                    explosion_branches.add(branch)
                    if i % 3 == 0:  # Add some nodes
                        node = Dot(end_point, radius=max(0.02, 0.07 - week * 0.008), color=branch_color)
                        explosion_nodes.add(node)
            self.play(
                LaggedStart(
                    *[Create(branch) for branch in explosion_branches],
                    lag_ratio=0.001
                ),
                run_time=tracker.duration * 0.7
            )
            self.play(
                LaggedStart(
                    *[GrowFromCenter(node) for node in explosion_nodes],
                    lag_ratio=0.001
                ),
                run_time=tracker.duration * 0.3
            )
        # Narration: "For eight weeks, we're looking at hundreds of possible schedules."
        # Visual: Display counter rapidly increasing: '3... 9... 27... 81... 243... 729... 2,187 paths'.
        with self.voiceover(text="For eight weeks, we're looking at hundreds of possible schedules.") as tracker:
            counter_values = [3, 9, 27, 81, 243, 729, 2187]
            counter = Text("3", font_size=60, color=YELLOW, weight="BOLD").to_edge(UP, buff=0.5)
            counter_label = Text("possible paths", font_size=32, color=WHITE).next_to(counter, DOWN, buff=0.3)
            self.play(
                FadeIn(counter, shift=DOWN * 0.3),
                FadeIn(counter_label, shift=DOWN * 0.3),
                run_time=tracker.duration * 0.2
            )
            time_per_number = tracker.duration * 0.8 / len(counter_values)
            for value in counter_values[1:]:
                new_counter = Text(str(value), font_size=60, color=YELLOW, weight="BOLD").move_to(counter.get_center())
                self.play(
                    Transform(counter, new_counter),
                    run_time=time_per_number
                )
            self.play(Indicate(counter, color=RED, scale_factor=1.3))
        # Narration: "For fifty weeks? That's more paths than atoms in the universe."
        # Visual: Show the number: '7.2 × 10²³ paths'. Animate the tree exploding off screen.
        with self.voiceover(text="For fifty weeks? That's more paths than atoms in the universe.") as tracker:
            huge_number = MathTex(r"7.2 \times 10^{23}", font_size=72, color=RED).move_to(counter.get_center())
            huge_label = Text("paths", font_size=36, color=RED).next_to(huge_number, DOWN, buff=0.3)
            self.play(
                ReplacementTransform(counter, huge_number),
                ReplacementTransform(counter_label, huge_label),
                run_time=tracker.duration * 0.4
            )
            # Explosion effect
            self.play(
                explosion_branches.animate.scale(2).set_opacity(0.1),
                explosion_nodes.animate.scale(2).set_opacity(0.1),
                all_branches.animate.scale(1.5).set_opacity(0.2),
                Flash(huge_number.get_center(), color=RED, flash_radius=2.0),
                run_time=tracker.duration * 0.6
            )
        # Narration: "We need a smarter approach. One that doesn't check every path."
        # Visual: Fade out the massive tree. Show a single glowing question mark in the center.
        with self.voiceover(text="We need a smarter approach. One that doesn't check every path.") as tracker:
            self.play(
                FadeOut(explosion_branches),
                FadeOut(explosion_nodes),
                FadeOut(all_branches),
                FadeOut(first_level),
                FadeOut(second_level),
                FadeOut(all_labels),
                FadeOut(tree_root),
                FadeOut(x_mark),
                FadeOut(checkmark),
                FadeOut(huge_number),
                FadeOut(huge_label),
                run_time=tracker.duration * 0.5
            )
            question_mark = Text("?", font_size=120, color=YELLOW, weight="BOLD").move_to(ORIGIN + UP * 0.5)
            self.play(
                GrowFromCenter(question_mark),
                run_time=tracker.duration * 0.3
            )
            self.play(
                Indicate(question_mark, color=YELLOW, scale_factor=1.2),
                run_time=tracker.duration * 0.2
            )
        # Narration: "The key insight is this: we don't need to remember the entire past."
        # Visual: Show a timeline with a glowing window highlighting just the current week and previous week.
        with self.voiceover(text="The key insight is this: we don't need to remember the entire past.") as tracker:
            self.play(
                FadeOut(question_mark),
                run_time=tracker.duration * 0.2
            )
            # Create new clean timeline
            new_timeline = NumberLine(
                x_range=[0, 8],
                length=10,
                include_numbers=True,
                label_direction=DOWN,
                font_size=24
            ).move_to(ORIGIN)
            self.play(
                Create(new_timeline),
                run_time=tracker.duration * 0.3
            )
            # Highlight window showing only current and previous week
            window_rect = Rectangle(
                width=2.8,
                height=1.2,
                color=YELLOW,
                stroke_width=4
            ).move_to(new_timeline.number_to_point(4))
            week_labels = VGroup(
                Text("week 3", font_size=20, color=GRAY).move_to(new_timeline.number_to_point(3) + UP * 0.8),
                Text("week 4", font_size=20, color=YELLOW).move_to(new_timeline.number_to_point(4) + UP * 0.8)
            )
            self.play(
                Create(window_rect),
                FadeIn(week_labels, shift=DOWN * 0.2),
                run_time=tracker.duration * 0.3
            )
            self.play(
                Indicate(window_rect, color=YELLOW),
                run_time=tracker.duration * 0.2
            )
        # Narration: "We only need to remember what state we're in right now."
        # Visual: Animate three colored auras appearing: gray (rested), blue (did low stress), red (did high stress).
        with self.voiceover(text="We only need to remember what state we're in right now.") as tracker:
            self.play(
                FadeOut(new_timeline),
                FadeOut(timeline),
                FadeOut(timeline_label),
                FadeOut(window_rect),
                FadeOut(week_labels),
                run_time=tracker.duration * 0.2
            )
            # Create three state auras
            state_rested = Circle(radius=0.8, color=GRAY, fill_opacity=0.3, stroke_width=4).shift(LEFT * 3.5)
            state_low = Circle(radius=0.8, color=BLUE, fill_opacity=0.3, stroke_width=4).shift(ORIGIN)
            state_high = Circle(radius=0.8, color=RED, fill_opacity=0.3, stroke_width=4).shift(RIGHT * 3.5)
            label_rested = Text("Rested", font_size=28, color=GRAY).next_to(state_rested, DOWN, buff=0.3)
            label_low = Text("Did Low", font_size=28, color=BLUE).next_to(state_low, DOWN, buff=0.3)
            label_high = Text("Did High", font_size=28, color=RED).next_to(state_high, DOWN, buff=0.3)
            states = VGroup(state_rested, state_low, state_high)
            labels = VGroup(label_rested, label_low, label_high)
            self.play(
                LaggedStart(
                    AnimationGroup(GrowFromCenter(state_rested), FadeIn(label_rested, shift=UP * 0.2)),
                    AnimationGroup(GrowFromCenter(state_low), FadeIn(label_low, shift=UP * 0.2)),
                    AnimationGroup(GrowFromCenter(state_high), FadeIn(label_high, shift=UP * 0.2)),
                    lag_ratio=0.3
                ),
                run_time=tracker.duration * 0.7
            )
            self.play(
                LaggedStart(
                    Indicate(state_rested, color=GRAY),
                    Indicate(state_low, color=BLUE),
                    Indicate(state_high, color=RED),
                    lag_ratio=0.2
                ),
                run_time=tracker.duration * 0.3
            )
        # Narration: "Because your current state determines what you can do next."
        # Visual: Show arrows from each aura to valid next states. Gray→all three, Blue→N/L, Red→N/L.
        with self.voiceover(text="Because your current state determines what you can do next.") as tracker:
            # From Rested (gray) - can go to all three
            arrow_r_to_r = Arrow(state_rested.get_top(), state_rested.get_top() + UP * 1.2 + LEFT * 0.5, color=GRAY, buff=0.1, stroke_width=3)
            arrow_r_to_l = Arrow(state_rested.get_right(), state_low.get_left(), color=BLUE, buff=0.1, stroke_width=3)
            arrow_r_to_h = Arrow(state_rested.get_top(), state_high.get_top() + UP * 0.3, color=RED, buff=0.1, stroke_width=3)
            # From Low (blue) - can only go to N or L
            arrow_l_to_r = Arrow(state_low.get_left(), state_rested.get_right(), color=GRAY, buff=0.1, stroke_width=3)
            arrow_l_to_l = Arrow(state_low.get_top(), state_low.get_top() + UP * 1.2, color=BLUE, buff=0.1, stroke_width=3)
            # From High (red) - can only go to N or L
            arrow_h_to_r = Arrow(state_high.get_top(), state_rested.get_top() + UP * 0.3, color=GRAY, buff=0.1, stroke_width=3)
            arrow_h_to_l = Arrow(state_high.get_left(), state_low.get_right(), color=BLUE, buff=0.1, stroke_width=3)
            # Show arrows from rested state
            self.play(
                LaggedStart(
                    Create(arrow_r_to_r),
                    Create(arrow_r_to_l),
                    Create(arrow_r_to_h),
                    lag_ratio=0.2
                ),
                run_time=tracker.duration * 0.35
            )
            # Show arrows from low stress state
            self.play(
                LaggedStart(
                    Create(arrow_l_to_r),
                    Create(arrow_l_to_l),
                    lag_ratio=0.2
                ),
                run_time=tracker.duration * 0.25
            )
            # Show arrows from high stress state
            self.play(
                LaggedStart(
                    Create(arrow_h_to_r),
                    Create(arrow_h_to_l),
                    lag_ratio=0.2
                ),
                run_time=tracker.duration * 0.25
            )
            # Emphasize the valid transitions
            self.play(
                Indicate(state_rested, color=YELLOW),
                run_time=tracker.duration * 0.15
            )
        self.wait(2)


        # ==========================================================
        # SCENE 5: States: Your Identity in Time
        # ==========================================================
        # Clear the scene
        if self.mobjects:
            self.play(*[FadeOut(obj) for obj in self.mobjects], run_time=0.5)
        # Narration: "Think of a state as your identity at a moment in time."
        # Visual: Draw a character at week 4 with a glowing blue aura labeled 'State: Did Low Stress'.
        with self.voiceover(text="Think of a state as your identity at a moment in time.") as tracker:
            # Create character (simple circle representation)
            character = Circle(radius=0.4, color=WHITE, fill_opacity=1.0)
            character.set_stroke(width=3)
            character.move_to(ORIGIN)
            # Create glowing blue aura
            aura = Circle(radius=0.7, color=BLUE, fill_opacity=0.3)
            aura.set_stroke(color=BLUE, width=4, opacity=0.8)
            aura.move_to(character.get_center())
            # Create state label
            state_label = Text("State: Did Low Stress", font_size=28, color=BLUE)
            state_label.next_to(character, DOWN, buff=0.8)
            # Create week indicator
            week_indicator = Text("Week 4", font_size=24, color=WHITE)
            week_indicator.next_to(character, UP, buff=0.8)
            # Animate everything in with polish
            self.play(
                FadeIn(aura, scale=0.5),
                FadeIn(character, shift=DOWN*0.3),
                run_time=tracker.duration * 0.6
            )
            self.play(
                Write(state_label, lag_ratio=0.1),
                FadeIn(week_indicator, shift=DOWN*0.2),
                run_time=tracker.duration * 0.4
            )
        # Narration: "This identity isn't about what you earned. It's about what you can do."
        # Visual: Show three doors ahead of the character: 'Rest', 'Low Stress', 'High Stress (LOCKED)'.
        with self.voiceover(text="This identity isn't about what you earned. It's about what you can do.") as tracker:
            # Create three doors as rectangles
            door_rest = Rectangle(width=1.2, height=2.0, color=GRAY, fill_opacity=0.2)
            door_low = Rectangle(width=1.2, height=2.0, color=GRAY, fill_opacity=0.2)
            door_high = Rectangle(width=1.2, height=2.0, color=GRAY, fill_opacity=0.2)
            # Position doors to the right of character
            doors = VGroup(door_rest, door_low, door_high)
            doors.arrange(RIGHT, buff=0.5)
            doors.shift(RIGHT * 3.5)
            # Create door labels
            label_rest = Text("Rest", font_size=20, color=WHITE)
            label_rest.next_to(door_rest, DOWN, buff=0.2)
            label_low = Text("Low Stress", font_size=20, color=WHITE)
            label_low.next_to(door_low, DOWN, buff=0.2)
            label_high = Text("High Stress", font_size=20, color=WHITE)
            label_high.next_to(door_high, DOWN, buff=0.2)
            door_labels = VGroup(label_rest, label_low, label_high)
            # Animate doors appearing
            self.play(
                LaggedStart(
                    *[FadeIn(door, shift=RIGHT*0.3) for door in doors],
                    lag_ratio=0.2
                ),
                run_time=tracker.duration * 0.6
            )
            self.play(
                LaggedStart(
                    *[Write(label, lag_ratio=0.1) for label in door_labels],
                    lag_ratio=0.15
                ),
                run_time=tracker.duration * 0.4
            )
        # Narration: "If your state is 'rested', all doors are open."
        # Visual: Change aura to gray. Animate all three doors unlocking and glowing green.
        with self.voiceover(text="If your state is 'rested', all doors are open.") as tracker:
            # Create new gray aura
            gray_aura = Circle(radius=0.7, color=GRAY, fill_opacity=0.3)
            gray_aura.set_stroke(color=GRAY, width=4, opacity=0.8)
            gray_aura.move_to(character.get_center())
            # Create new state label
            new_state_label = Text("State: Rested", font_size=28, color=GRAY)
            new_state_label.next_to(character, DOWN, buff=0.8)
            # Transform aura and label
            self.play(
                Transform(aura, gray_aura, rate_func=smooth),
                Transform(state_label, new_state_label, rate_func=smooth),
                run_time=tracker.duration * 0.4
            )
            # Create green glows for doors
            glow_rest = door_rest.copy().set_stroke(color=GREEN, width=8, opacity=1.0).set_fill(color=GREEN, opacity=0.4)
            glow_low = door_low.copy().set_stroke(color=GREEN, width=8, opacity=1.0).set_fill(color=GREEN, opacity=0.4)
            glow_high = door_high.copy().set_stroke(color=GREEN, width=8, opacity=1.0).set_fill(color=GREEN, opacity=0.4)
            # Animate doors unlocking
            self.play(
                Transform(door_rest, glow_rest, rate_func=smooth),
                Transform(door_low, glow_low, rate_func=smooth),
                Transform(door_high, glow_high, rate_func=smooth),
                run_time=tracker.duration * 0.5
            )
            # Add emphasis
            self.play(
                Flash(door_rest.get_center(), color=GREEN, flash_radius=0.5),
                Flash(door_low.get_center(), color=GREEN, flash_radius=0.5),
                Flash(door_high.get_center(), color=GREEN, flash_radius=0.5),
                run_time=0.3
            )
        # Narration: "If your state is 'did high stress', you're exhausted. Only two doors open."
        # Visual: Change aura to red. Animate the High Stress door locking with a red X.
        with self.voiceover(text="If your state is 'did high stress', you're exhausted. Only two doors open.") as tracker:
            # Create red aura
            red_aura = Circle(radius=0.7, color=RED, fill_opacity=0.3)
            red_aura.set_stroke(color=RED, width=4, opacity=0.8)
            red_aura.move_to(character.get_center())
            # Create exhausted state label
            exhausted_label = Text("State: Exhausted", font_size=28, color=RED)
            exhausted_label.next_to(character, DOWN, buff=0.8)
            # Transform to exhausted state
            self.play(
                Transform(aura, red_aura, rate_func=smooth),
                Transform(state_label, exhausted_label, rate_func=smooth),
                run_time=tracker.duration * 0.3
            )
            # Lock the high stress door
            locked_door = door_high.copy().set_stroke(color=RED, width=6, opacity=1.0).set_fill(color=RED, opacity=0.3)
            # Create red X
            x_line1 = Line(
                locked_door.get_corner(UP + LEFT) + DOWN*0.2 + RIGHT*0.1,
                locked_door.get_corner(DOWN + RIGHT) + UP*0.2 + LEFT*0.1,
                color=RED,
                stroke_width=8
            )
            x_line2 = Line(
                locked_door.get_corner(UP + RIGHT) + DOWN*0.2 + LEFT*0.1,
                locked_door.get_corner(DOWN + LEFT) + UP*0.2 + RIGHT*0.1,
                color=RED,
                stroke_width=8
            )
            red_x = VGroup(x_line1, x_line2)
            # Animate locking
            self.play(
                Transform(door_high, locked_door, rate_func=smooth),
                run_time=tracker.duration * 0.4
            )
            self.play(
                Create(x_line1),
                Create(x_line2),
                run_time=tracker.duration * 0.3
            )
        # Narration: "The beautiful thing? We don't need to remember how you got exhausted."
        # Visual: Show multiple paths leading to the red state: different histories, same aura.
        with self.voiceover(text="The beautiful thing? We don't need to remember how you got exhausted.") as tracker:
            # Create multiple history paths coming from the left
            path1_points = [LEFT * 5 + UP * 1.5, LEFT * 3 + UP * 1, character.get_center()]
            path2_points = [LEFT * 5 + UP * 0.5, LEFT * 3.5 + UP * 0.2, character.get_center()]
            path3_points = [LEFT * 5 + DOWN * 0.5, LEFT * 3 + DOWN * 0.3, character.get_center()]
            path4_points = [LEFT * 5 + DOWN * 1.5, LEFT * 3.5 + DOWN * 1, character.get_center()]
            # Create curved paths
            path1 = VMobject()
            path1.set_points_as_corners(path1_points)
            path1.set_stroke(color=YELLOW, width=3, opacity=0.6)
            path2 = VMobject()
            path2.set_points_as_corners(path2_points)
            path2.set_stroke(color=ORANGE, width=3, opacity=0.6)
            path3 = VMobject()
            path3.set_points_as_corners(path3_points)
            path3.set_stroke(color=PURPLE, width=3, opacity=0.6)
            path4 = VMobject()
            path4.set_points_as_corners(path4_points)
            path4.set_stroke(color=BLUE, width=3, opacity=0.6)
            paths = VGroup(path1, path2, path3, path4)
            # Create history labels
            hist1 = Text("Week 1: High Stress", font_size=16, color=YELLOW)
            hist1.next_to(path1.get_start(), LEFT, buff=0.2)
            hist2 = Text("Week 2: Low → High", font_size=16, color=ORANGE)
            hist2.next_to(path2.get_start(), LEFT, buff=0.2)
            hist3 = Text("Week 3: Rest → High", font_size=16, color=PURPLE)
            hist3.next_to(path3.get_start(), LEFT, buff=0.2)
            hist4 = Text("Different History", font_size=16, color=BLUE)
            hist4.next_to(path4.get_start(), LEFT, buff=0.2)
            histories = VGroup(hist1, hist2, hist3, hist4)
            # Animate paths appearing
            self.play(
                LaggedStart(
                    *[Create(path) for path in paths],
                    lag_ratio=0.15
                ),
                run_time=tracker.duration * 0.6
            )
            self.play(
                LaggedStart(
                    *[FadeIn(hist, shift=RIGHT*0.2) for hist in histories],
                    lag_ratio=0.15
                ),
                run_time=tracker.duration * 0.4
            )
        # Narration: "Whether you did high stress last week or two weeks ago doesn't matter."
        # Visual: Fade out the history paths. Only the current state remains glowing.
        with self.voiceover(text="Whether you did high stress last week or two weeks ago doesn't matter.") as tracker:
            # Fade out all paths and history labels
            self.play(
                *[FadeOut(path, shift=LEFT*0.5) for path in paths],
                *[FadeOut(hist, shift=LEFT*0.5) for hist in histories],
                run_time=tracker.duration * 0.7
            )
            # Emphasize the current state
            self.play(
                Indicate(aura, color=RED, scale_factor=1.3),
                Indicate(character, color=RED, scale_factor=1.2),
                run_time=tracker.duration * 0.3
            )
        # Narration: "All that matters is: what state are you in, and what week is it?"
        # Visual: Display two variables glowing: 'Week: 4' and 'State: Exhausted'.
        with self.voiceover(text="All that matters is: what state are you in, and what week is it?") as tracker:
            # Create variable boxes
            week_box = Rectangle(width=2.5, height=1.0, color=YELLOW, fill_opacity=0.2)
            week_box.set_stroke(color=YELLOW, width=3)
            week_box.move_to(LEFT * 3 + UP * 2)
            week_text = Text("Week: 4", font_size=28, color=YELLOW)
            week_text.move_to(week_box.get_center())
            state_box = Rectangle(width=3.5, height=1.0, color=RED, fill_opacity=0.2)
            state_box.set_stroke(color=RED, width=3)
            state_box.move_to(LEFT * 3 + DOWN * 0)
            state_text = Text("State: Exhausted", font_size=28, color=RED)
            state_text.move_to(state_box.get_center())
            # Animate boxes appearing with glow
            self.play(
                DrawBorderThenFill(week_box),
                FadeIn(week_text, shift=DOWN*0.2),
                run_time=tracker.duration * 0.4
            )
            self.play(
                Flash(week_box.get_center(), color=YELLOW, flash_radius=0.8),
                run_time=0.3
            )
            self.play(
                DrawBorderThenFill(state_box),
                FadeIn(state_text, shift=DOWN*0.2),
                run_time=tracker.duration * 0.4
            )
            self.play(
                Flash(state_box.get_center(), color=RED, flash_radius=0.8),
                run_time=0.3
            )
        # Narration: "This compression is the secret. History becomes a single label."
        # Visual: Show a long timeline compressing into a single point labeled with week and state.
        with self.voiceover(text="This compression is the secret. History becomes a single label.") as tracker:
            # Create long timeline
            timeline = Line(LEFT * 6, RIGHT * 1, color=WHITE, stroke_width=4)
            timeline.move_to(DOWN * 2)
            # Create week markers on timeline
            week_markers = VGroup()
            week_labels = VGroup()
            for i in range(5):
                marker = Line(UP * 0.15, DOWN * 0.15, color=WHITE, stroke_width=3)
                marker.move_to(timeline.point_from_proportion(i / 4))
                week_markers.add(marker)
                label = Text(f"W{i}", font_size=18, color=WHITE)
                label.next_to(marker, DOWN, buff=0.2)
                week_labels.add(label)
            # Create history events on timeline
            event1 = Dot(timeline.point_from_proportion(0.25), color=BLUE, radius=0.08)
            event2 = Dot(timeline.point_from_proportion(0.5), color=GREEN, radius=0.08)
            event3 = Dot(timeline.point_from_proportion(0.75), color=YELLOW, radius=0.08)
            event4 = Dot(timeline.point_from_proportion(1.0), color=RED, radius=0.08)
            events = VGroup(event1, event2, event3, event4)
            # Show timeline
            self.play(
                Create(timeline),
                LaggedStart(*[GrowFromCenter(marker) for marker in week_markers], lag_ratio=0.1),
                LaggedStart(*[FadeIn(label, shift=UP*0.1) for label in week_labels], lag_ratio=0.1),
                run_time=tracker.duration * 0.4
            )
            # Show events
            self.play(
                LaggedStart(*[GrowFromCenter(event) for event in events], lag_ratio=0.15),
                run_time=tracker.duration * 0.3
            )
            # Compress timeline into single point
            compressed_point = Dot(ORIGIN + DOWN * 2, color=RED, radius=0.15)
            compressed_label = VGroup(
                Text("Week: 4", font_size=20, color=YELLOW),
                Text("State: Exhausted", font_size=20, color=RED)
            ).arrange(DOWN, buff=0.1)
            compressed_label.next_to(compressed_point, UP, buff=0.3)
            self.play(
                timeline.animate.scale(0.01).move_to(compressed_point.get_center()),
                *[marker.animate.scale(0.01).move_to(compressed_point.get_center()) for marker in week_markers],
                *[label.animate.scale(0.01).move_to(compressed_point.get_center()) for label in week_labels],
                *[event.animate.move_to(compressed_point.get_center()) for event in events],
                run_time=tracker.duration * 0.3
            )
            # Show compressed result
            self.play(
                FadeOut(timeline),
                FadeOut(week_markers),
                FadeOut(week_labels),
                FadeOut(events),
                GrowFromCenter(compressed_point),
                FadeIn(compressed_label, shift=DOWN*0.2),
                run_time=0.3
            )
        # Narration: "And that label tells us everything we need to make the optimal choice."
        # Visual: From the labeled point, show three arrows pointing forward to next week's possible states.
        with self.voiceover(text="And that label tells us everything we need to make the optimal choice.") as tracker:
            # Create three arrows pointing to future states
            arrow1 = Arrow(
                compressed_point.get_center() + RIGHT * 0.3,
                compressed_point.get_center() + RIGHT * 3 + UP * 1.5,
                color=GRAY,
                buff=0.1,
                stroke_width=4
            )
            arrow2 = Arrow(
                compressed_point.get_center() + RIGHT * 0.3,
                compressed_point.get_center() + RIGHT * 3,
                color=BLUE,
                buff=0.1,
                stroke_width=4
            )
            arrow3 = Arrow(
                compressed_point.get_center() + RIGHT * 0.3,
                compressed_point.get_center() + RIGHT * 3 + DOWN * 1.5,
                color=RED,
                buff=0.1,
                stroke_width=4
            )
            arrows = VGroup(arrow1, arrow2, arrow3)
            # Create future state labels
            future1 = VGroup(
                Text("Week 5", font_size=18, color=WHITE),
                Text("Rested", font_size=20, color=GRAY)
            ).arrange(DOWN, buff=0.05)
            future1.next_to(arrow1.get_end(), RIGHT, buff=0.2)
            future2 = VGroup(
                Text("Week 5", font_size=18, color=WHITE),
                Text("Did Low", font_size=20, color=BLUE)
            ).arrange(DOWN, buff=0.05)
            future2.next_to(arrow2.get_end(), RIGHT, buff=0.2)
            future3 = VGroup(
                Text("Week 5", font_size=18, color=WHITE),
                Text("BLOCKED", font_size=20, color=RED)
            ).arrange(DOWN, buff=0.05)
            future3.next_to(arrow3.get_end(), RIGHT, buff=0.2)
            futures = VGroup(future1, future2, future3)
            # Animate arrows growing
            self.play(
                LaggedStart(
                    *[GrowArrow(arrow) for arrow in arrows],
                    lag_ratio=0.2
                ),
                run_time=tracker.duration * 0.6
            )
            # Animate future states appearing
            self.play(
                LaggedStart(
                    *[FadeIn(future, shift=LEFT*0.3) for future in futures],
                    lag_ratio=0.2
                ),
                run_time=tracker.duration * 0.4
            )
            # Emphasize the optimal choice (arrow2 - Did Low)
            self.play(
                Indicate(arrow2, color=BLUE, scale_factor=1.2),
                Circumscribe(future2, color=BLUE, buff=0.1),
                run_time=1.0
            )
        self.wait(2)


        # ==========================================================
        # SCENE 6: The Table of Futures
        # ==========================================================
        # Clear previous scene
        if self.mobjects:
            self.play(*[FadeOut(obj) for obj in self.mobjects], run_time=0.5)
        # Narration: "Now imagine a table. Rows are states, columns are weeks."
        # Visual: Draw a grid: 3 rows (Rest, Low, High) × 8 columns (weeks 1-8). All cells empty.
        with self.voiceover(text="Now imagine a table. Rows are states, columns are weeks.") as tracker:
            # Create row labels
            row_labels = VGroup(
                Text("Rested", font_size=28),
                Text("Low Stress", font_size=28),
                Text("Exhausted", font_size=28)
            ).arrange(DOWN, buff=0.8).shift(LEFT * 4.5)
            # Create column labels (weeks 1-8)
            col_labels = VGroup(*[
                Text(f"W{i}", font_size=24) for i in range(1, 9)
            ]).arrange(RIGHT, buff=0.6).shift(UP * 2.5 + RIGHT * 0.5)
            # Create grid cells (3 rows × 8 columns)
            grid_cells = VGroup()
            for row in range(3):
                row_group = VGroup()
                for col in range(8):
                    cell = Rectangle(width=0.55, height=0.7, color=WHITE, stroke_width=2)
                    cell.move_to(col_labels[col].get_center() + DOWN * (1.3 + row * 0.8))
                    row_group.add(cell)
                grid_cells.add(row_group)
            # Animate creation with polish
            self.play(
                LaggedStart(
                    Write(row_labels, lag_ratio=0.2),
                    Write(col_labels, lag_ratio=0.1),
                    lag_ratio=0.3
                ),
                run_time=tracker.duration * 0.7
            )
            self.play(
                Create(grid_cells, lag_ratio=0.02),
                run_time=tracker.duration * 0.3
            )
        # Narration: "Each cell will answer: from this state at this week, what's the best I can do?"
        # Visual: Highlight cell (Rest, Week 4) and show text: 'Best profit from here to end?'
        with self.voiceover(text="Each cell will answer: from this state at this week, what's the best I can do?") as tracker:
            example_cell = grid_cells[0][3]  # Rest, Week 4
            highlight_rect = SurroundingRectangle(example_cell, color=YELLOW, buff=0.05, stroke_width=4)
            question_text = Text("Best profit\nfrom here to end?", font_size=22, color=YELLOW)
            question_text.next_to(example_cell, UP, buff=0.3)
            self.play(
                Create(highlight_rect),
                FadeIn(question_text, shift=DOWN * 0.2),
                run_time=tracker.duration * 0.6
            )
            self.play(Indicate(question_text, color=YELLOW, scale_factor=1.15), run_time=tracker.duration * 0.4)
        # Narration: "Let's start at the end. Week eight, any state: you're done."
        # Visual: Highlight the rightmost column (week 8). All three cells fill with '$0'.
        with self.voiceover(text="Let's start at the end. Week eight, any state: you're done.") as tracker:
            self.play(FadeOut(highlight_rect), FadeOut(question_text), run_time=0.3)
            week8_cells = VGroup(*[grid_cells[row][7] for row in range(3)])
            week8_highlight = SurroundingRectangle(week8_cells, color=BLUE, buff=0.1, stroke_width=3)
            zero_values = VGroup(*[
                Text("$0", font_size=24, color=BLUE).move_to(grid_cells[row][7].get_center())
                for row in range(3)
            ])
            self.play(Create(week8_highlight), run_time=tracker.duration * 0.4)
            self.play(
                LaggedStart(*[FadeIn(val, shift=DOWN * 0.2) for val in zero_values], lag_ratio=0.2),
                run_time=tracker.duration * 0.6
            )
        # Narration: "These are our base cases. The future is empty, so the value is zero."
        # Visual: Animate the three cells in week 8 glowing gold, labeled 'Base Case'.
        with self.voiceover(text="These are our base cases. The future is empty, so the value is zero.") as tracker:
            base_case_label = Text("Base Cases", font_size=26, color=GOLD).next_to(week8_cells, RIGHT, buff=0.4)
            self.play(
                week8_highlight.animate.set_color(GOLD),
                zero_values.animate.set_color(GOLD),
                run_time=tracker.duration * 0.5
            )
            self.play(
                Write(base_case_label, lag_ratio=0.1),
                Flash(week8_cells.get_center(), color=GOLD, flash_radius=0.5),
                run_time=tracker.duration * 0.5
            )
        # Narration: "Now step back to week seven. If you're rested, what are your options?"
        # Visual: Highlight cell (Rest, Week 7). Show three arrows pointing to week 8: Rest→$0, Low→$10, High→$50.
        with self.voiceover(text="Now step back to week seven. If you're rested, what are your options?") as tracker:
            self.play(FadeOut(week8_highlight), FadeOut(base_case_label), run_time=0.3)
            rest_week7_cell = grid_cells[0][6]
            rest_highlight = SurroundingRectangle(rest_week7_cell, color=GREEN, buff=0.05, stroke_width=4)
            # Create three arrows showing options
            arrow_rest = Arrow(
                rest_week7_cell.get_right() + RIGHT * 0.1,
                grid_cells[0][7].get_left() + LEFT * 0.1,
                buff=0.05, color=GRAY, stroke_width=2, max_tip_length_to_length_ratio=0.15
            )
            arrow_low = Arrow(
                rest_week7_cell.get_right() + RIGHT * 0.1,
                grid_cells[1][7].get_left() + LEFT * 0.1,
                buff=0.05, color=GRAY, stroke_width=2, max_tip_length_to_length_ratio=0.15
            )
            arrow_high = Arrow(
                rest_week7_cell.get_right() + RIGHT * 0.1,
                grid_cells[2][7].get_left() + LEFT * 0.1,
                buff=0.05, color=GRAY, stroke_width=2, max_tip_length_to_length_ratio=0.15
            )
            self.play(Create(rest_highlight), run_time=tracker.duration * 0.3)
            self.play(
                LaggedStart(
                    Create(arrow_rest),
                    Create(arrow_low),
                    Create(arrow_high),
                    lag_ratio=0.3
                ),
                run_time=tracker.duration * 0.7
            )
        # Narration: "You can rest for zero, low stress for ten, or high stress for fifty."
        # Visual: Display the three options as cards: 'Rest: $0+$0', 'Low: $10+$0', 'High: $50+$0'.
        with self.voiceover(text="You can rest for zero, low stress for ten, or high stress for fifty.") as tracker:
            option_cards = VGroup()
            card_rest = VGroup(
                Rectangle(width=1.2, height=0.5, color=GRAY, fill_opacity=0.2),
                Text("Rest: $0+$0", font_size=18)
            )
            card_rest[1].move_to(card_rest[0].get_center())
            card_low = VGroup(
                Rectangle(width=1.2, height=0.5, color=BLUE, fill_opacity=0.2),
                Text("Low: $10+$0", font_size=18)
            )
            card_low[1].move_to(card_low[0].get_center())
            card_high = VGroup(
                Rectangle(width=1.2, height=0.5, color=RED, fill_opacity=0.2),
                Text("High: $50+$0", font_size=18)
            )
            card_high[1].move_to(card_high[0].get_center())
            option_cards.add(card_rest, card_low, card_high)
            option_cards.arrange(DOWN, buff=0.2).next_to(rest_week7_cell, LEFT, buff=1.2)
            self.play(
                LaggedStart(
                    FadeIn(card_rest, shift=RIGHT * 0.3),
                    FadeIn(card_low, shift=RIGHT * 0.3),
                    FadeIn(card_high, shift=RIGHT * 0.3),
                    lag_ratio=0.3
                ),
                run_time=tracker.duration
            )
        # Narration: "Obviously, take the high stress job. Fifty dollars is best."
        # Visual: Highlight the High card glowing. Fill cell (Rest, Week 7) with '$50'.
        with self.voiceover(text="Obviously, take the high stress job. Fifty dollars is best.") as tracker:
            high_glow = SurroundingRectangle(card_high, color=GOLD, buff=0.05, stroke_width=4)
            value_50 = Text("$50", font_size=24, color=GREEN).move_to(rest_week7_cell.get_center())
            self.play(
                Create(high_glow),
                card_high.animate.scale(1.15),
                run_time=tracker.duration * 0.5
            )
            self.play(
                FadeIn(value_50, shift=DOWN * 0.2),
                Flash(rest_week7_cell.get_center(), color=GREEN),
                run_time=tracker.duration * 0.5
            )
        # Narration: "If you're exhausted at week seven, high stress is locked."
        # Visual: Highlight cell (High, Week 7). Show only two arrows: Rest→$0, Low→$10.
        with self.voiceover(text="If you're exhausted at week seven, high stress is locked.") as tracker:
            self.play(
                FadeOut(option_cards),
                FadeOut(high_glow),
                FadeOut(arrow_rest),
                FadeOut(arrow_low),
                FadeOut(arrow_high),
                FadeOut(rest_highlight),
                run_time=0.4
            )
            exhausted_week7_cell = grid_cells[2][6]
            exhausted_highlight = SurroundingRectangle(exhausted_week7_cell, color=RED, buff=0.05, stroke_width=4)
            # Only two arrows (no high stress option)
            arrow_rest_ex = Arrow(
                exhausted_week7_cell.get_right() + RIGHT * 0.1,
                grid_cells[0][7].get_left() + LEFT * 0.1,
                buff=0.05, color=GRAY, stroke_width=2, max_tip_length_to_length_ratio=0.15
            )
            arrow_low_ex = Arrow(
                exhausted_week7_cell.get_right() + RIGHT * 0.1,
                grid_cells[1][7].get_left() + LEFT * 0.1,
                buff=0.05, color=BLUE, stroke_width=3, max_tip_length_to_length_ratio=0.15
            )
            # X mark on high stress option
            x_mark = VGroup(
                Line(UP * 0.15 + LEFT * 0.15, DOWN * 0.15 + RIGHT * 0.15, color=RED, stroke_width=3),
                Line(UP * 0.15 + RIGHT * 0.15, DOWN * 0.15 + LEFT * 0.15, color=RED, stroke_width=3)
            ).move_to(exhausted_week7_cell.get_center() + RIGHT * 0.8)
            self.play(Create(exhausted_highlight), run_time=tracker.duration * 0.3)
            self.play(
                LaggedStart(
                    Create(arrow_rest_ex),
                    Create(arrow_low_ex),
                    Create(x_mark),
                    lag_ratio=0.3
                ),
                run_time=tracker.duration * 0.7
            )
        # Narration: "Best you can do is low stress for ten dollars."
        # Visual: Fill cell (High, Week 7) with '$10'. Animate it glowing.
        with self.voiceover(text="Best you can do is low stress for ten dollars.") as tracker:
            value_10 = Text("$10", font_size=24, color=BLUE).move_to(exhausted_week7_cell.get_center())
            self.play(
                arrow_low_ex.animate.set_color(GOLD).set_stroke(width=5),
                run_time=tracker.duration * 0.4
            )
            self.play(
                FadeIn(value_10, shift=DOWN * 0.2),
                Flash(exhausted_week7_cell.get_center(), color=BLUE),
                Indicate(value_10, color=GOLD, scale_factor=1.2),
                run_time=tracker.duration * 0.6
            )
        # Narration: "We fill the table right to left, each cell looking one week ahead."
        # Visual: Animate filling week 6, then 5, then 4. Show cells lighting up in sequence like a wave.
        with self.voiceover(text="We fill the table right to left, each cell looking one week ahead.") as tracker:
            self.play(
                FadeOut(exhausted_highlight),
                FadeOut(arrow_rest_ex),
                FadeOut(arrow_low_ex),
                FadeOut(x_mark),
                run_time=0.3
            )
            # Create sample values for weeks 6, 5, 4
            week6_values = VGroup(
                Text("$50", font_size=22, color=GREEN).move_to(grid_cells[0][5].get_center()),
                Text("$40", font_size=22, color=GREEN).move_to(grid_cells[1][5].get_center()),
                Text("$10", font_size=22, color=BLUE).move_to(grid_cells[2][5].get_center())
            )
            week5_values = VGroup(
                Text("$90", font_size=22, color=GREEN).move_to(grid_cells[0][4].get_center()),
                Text("$60", font_size=22, color=GREEN).move_to(grid_cells[1][4].get_center()),
                Text("$50", font_size=22, color=GREEN).move_to(grid_cells[2][4].get_center())
            )
            week4_values = VGroup(
                Text("$140", font_size=20, color=GREEN).move_to(grid_cells[0][3].get_center()),
                Text("$100", font_size=20, color=GREEN).move_to(grid_cells[1][3].get_center()),
                Text("$70", font_size=22, color=GREEN).move_to(grid_cells[2][3].get_center())
            )
            # Animate wave effect
            self.play(
                LaggedStart(
                    *[FadeIn(val, shift=LEFT * 0.3) for val in week6_values],
                    lag_ratio=0.15
                ),
                run_time=tracker.duration * 0.3
            )
            self.play(
                LaggedStart(
                    *[FadeIn(val, shift=LEFT * 0.3) for val in week5_values],
                    lag_ratio=0.15
                ),
                run_time=tracker.duration * 0.3
            )
            self.play(
                LaggedStart(
                    *[FadeIn(val, shift=LEFT * 0.3) for val in week4_values],
                    lag_ratio=0.15
                ),
                run_time=tracker.duration * 0.3
            )
            # Final emphasis: show the wave pattern
            all_filled = VGroup(zero_values, value_50, value_10, week6_values, week5_values, week4_values)
            self.play(Indicate(all_filled, color=GOLD, scale_factor=1.05), run_time=tracker.duration * 0.1)
        self.wait(2)


        # ==========================================================
        # SCENE 7: The Bellman Revelation
        # ==========================================================
        # Clear the scene
        if self.mobjects:
            self.play(*[FadeOut(obj) for obj in self.mobjects], run_time=0.5)
        # Narration: "Here's the equation that makes everything work."
        # Visual: Display in center: 'Value(state, week) = reward + Value(next_state, week+1)'.
        with self.voiceover(text="Here's the equation that makes everything work.") as tracker:
            equation = MathTex(
                r"\text{Value}(\text{state}, \text{week})", 
                r"=", 
                r"\text{reward}", 
                r"+", 
                r"\text{Value}(\text{next\_state}, \text{week}+1)"
            ).scale(0.8)
            equation.move_to(ORIGIN)
            self.play(Write(equation, lag_ratio=0.1), run_time=tracker.duration)
        self.wait(0.5)
        # Narration: "The value of being in a state is the immediate reward you get..."
        # Visual: Highlight 'reward' in the equation. Show a coin labeled '$10' appearing.
        with self.voiceover(text="The value of being in a state is the immediate reward you get...") as tracker:
            reward_part = equation[2]
            self.play(Indicate(reward_part, color=YELLOW, scale_factor=1.3), run_time=tracker.duration * 0.5)
            coin = Circle(radius=0.4, color=GOLD, fill_opacity=0.8).set_stroke(color=YELLOW, width=3)
            coin_label = Text("$10", font_size=24, color=BLACK).move_to(coin.get_center())
            coin_group = VGroup(coin, coin_label).next_to(reward_part, DOWN, buff=0.5)
            self.play(
                FadeIn(coin_group, shift=UP*0.3, scale=0.5),
                run_time=tracker.duration * 0.5
            )
        self.wait(0.5)
        # Narration: "...plus the best value you can get from wherever you land next."
        # Visual: Highlight 'Value(next_state, week+1)'. Show an arrow pointing to a future cell.
        with self.voiceover(text="plus the best value you can get from wherever you land next.") as tracker:
            future_part = equation[4]
            self.play(Indicate(future_part, color=BLUE, scale_factor=1.3), run_time=tracker.duration * 0.5)
            arrow = Arrow(
                future_part.get_right() + RIGHT*0.2,
                future_part.get_right() + RIGHT*1.5,
                buff=0.1,
                color=BLUE,
                stroke_width=4
            )
            future_box = Rectangle(width=1.2, height=0.8, color=BLUE, fill_opacity=0.3)
            future_box.next_to(arrow, RIGHT, buff=0.1)
            future_label = Text("Future", font_size=20, color=BLUE).move_to(future_box.get_center())
            self.play(
                GrowFromEdge(arrow, edge=LEFT),
                FadeIn(future_box, shift=LEFT*0.3),
                Write(future_label),
                run_time=tracker.duration * 0.5
            )
        self.wait(0.5)
        # Clear for the table
        self.play(
            FadeOut(equation, shift=UP*0.5),
            FadeOut(coin_group, shift=DOWN*0.3),
            FadeOut(arrow),
            FadeOut(future_box),
            FadeOut(future_label),
            run_time=0.8
        )
        # Narration: "Let's see this in action. Week five, rested state."
        # Visual: Highlight cell (Rest, Week 5). Show it empty, waiting to be filled.
        with self.voiceover(text="Let's see this in action. Week five, rested state.") as tracker:
            # Create a simplified table
            table_title = Text("Dynamic Programming Table", font_size=28, color=WHITE).to_edge(UP, buff=0.5)
            # Column headers
            week5_header = Text("Week 5", font_size=24, color=BLUE).move_to(UP*2 + RIGHT*2)
            week6_header = Text("Week 6", font_size=24, color=BLUE).move_to(UP*2 + RIGHT*4.5)
            # Row labels
            rest_label = Text("Rest", font_size=22, color=GREEN).move_to(UP*1 + LEFT*1.5)
            low_label = Text("Low", font_size=22, color=ORANGE).move_to(ORIGIN + LEFT*1.5)
            high_label = Text("High", font_size=22, color=RED).move_to(DOWN*1 + LEFT*1.5)
            # Create cells
            rest_week5_cell = Rectangle(width=1.5, height=0.8, color=GREEN, stroke_width=3)
            rest_week5_cell.move_to(UP*1 + RIGHT*2)
            rest_week5_value = Text("?", font_size=28, color=WHITE).move_to(rest_week5_cell.get_center())
            rest_week6_cell = Rectangle(width=1.5, height=0.8, color=GREEN, stroke_width=2, fill_opacity=0.1)
            rest_week6_cell.move_to(UP*1 + RIGHT*4.5)
            rest_week6_value = Text("$130", font_size=24, color=WHITE).move_to(rest_week6_cell.get_center())
            low_week6_cell = Rectangle(width=1.5, height=0.8, color=ORANGE, stroke_width=2, fill_opacity=0.1)
            low_week6_cell.move_to(ORIGIN + RIGHT*4.5)
            low_week6_value = Text("$110", font_size=24, color=WHITE).move_to(low_week6_cell.get_center())
            high_week6_cell = Rectangle(width=1.5, height=0.8, color=RED, stroke_width=2, fill_opacity=0.1)
            high_week6_cell.move_to(DOWN*1 + RIGHT*4.5)
            high_week6_value = Text("$70", font_size=24, color=WHITE).move_to(high_week6_cell.get_center())
            table_elements = VGroup(
                table_title, week5_header, week6_header,
                rest_label, low_label, high_label,
                rest_week5_cell, rest_week6_cell, low_week6_cell, high_week6_cell,
                rest_week6_value, low_week6_value, high_week6_value
            )
            self.play(
                LaggedStart(
                    FadeIn(table_title, shift=DOWN*0.2),
                    FadeIn(week5_header, shift=DOWN*0.2),
                    FadeIn(week6_header, shift=DOWN*0.2),
                    FadeIn(rest_label, shift=RIGHT*0.2),
                    FadeIn(low_label, shift=RIGHT*0.2),
                    FadeIn(high_label, shift=RIGHT*0.2),
                    lag_ratio=0.1
                ),
                run_time=tracker.duration * 0.5
            )
            self.play(
                Create(rest_week5_cell),
                Create(rest_week6_cell),
                Create(low_week6_cell),
                Create(high_week6_cell),
                run_time=tracker.duration * 0.3
            )
            self.play(
                Write(rest_week5_value),
                Write(rest_week6_value),
                Write(low_week6_value),
                Write(high_week6_value),
                run_time=tracker.duration * 0.2
            )
            self.play(Circumscribe(VGroup(rest_week5_cell, rest_week5_value), color=YELLOW, buff=0.1))
        self.wait(0.5)
        # Narration: "Option one: rest this week. Zero dollars now, but what about the future?"
        # Visual: Show arrow to cell (Rest, Week 6). Display: '$0 now + $130 future = $130 total'.
        with self.voiceover(text="Option one: rest this week. Zero dollars now, but what about the future?") as tracker:
            option1_label = Text("Option 1: Rest", font_size=20, color=GREEN).to_edge(LEFT, buff=0.5).shift(DOWN*2)
            arrow1 = Arrow(
                rest_week5_cell.get_right(),
                rest_week6_cell.get_left(),
                buff=0.1,
                color=GREEN,
                stroke_width=4
            )
            calc1 = MathTex(r"\$0", r"+", r"\$130", r"=", r"\$130").scale(0.7)
            calc1.next_to(option1_label, RIGHT, buff=0.5)
            calc1[0].set_color(GRAY)
            calc1[2].set_color(GREEN)
            calc1[4].set_color(GREEN)
            self.play(
                Write(option1_label),
                GrowFromEdge(arrow1, edge=LEFT),
                run_time=tracker.duration * 0.4
            )
            self.play(Flash(rest_week6_cell.get_center(), color=GREEN, flash_radius=0.5))
            self.play(
                Write(calc1, lag_ratio=0.15),
                run_time=tracker.duration * 0.6
            )
        self.wait(0.5)
        # Narration: "Option two: low stress. Ten dollars now, plus the future from that state."
        # Visual: Show arrow to cell (Low, Week 6). Display: '$10 now + $110 future = $120 total'.
        with self.voiceover(text="Option two: low stress. Ten dollars now, plus the future from that state.") as tracker:
            option2_label = Text("Option 2: Low", font_size=20, color=ORANGE).next_to(option1_label, DOWN, buff=0.3, aligned_edge=LEFT)
            arrow2 = Arrow(
                rest_week5_cell.get_bottom() + DOWN*0.2,
                low_week6_cell.get_left(),
                buff=0.1,
                color=ORANGE,
                stroke_width=4
            )
            calc2 = MathTex(r"\$10", r"+", r"\$110", r"=", r"\$120").scale(0.7)
            calc2.next_to(option2_label, RIGHT, buff=0.5)
            calc2[0].set_color(ORANGE)
            calc2[2].set_color(ORANGE)
            calc2[4].set_color(ORANGE)
            self.play(
                Write(option2_label),
                GrowFromEdge(arrow2, edge=LEFT),
                run_time=tracker.duration * 0.4
            )
            self.play(Flash(low_week6_cell.get_center(), color=ORANGE, flash_radius=0.5))
            self.play(
                Write(calc2, lag_ratio=0.15),
                run_time=tracker.duration * 0.6
            )
        self.wait(0.5)
        # Narration: "Option three: high stress. Fifty now, but you'll be exhausted."
        # Visual: Show arrow to cell (High, Week 6). Display: '$50 now + $70 future = $120 total'.
        with self.voiceover(text="Option three: high stress. Fifty now, but you'll be exhausted.") as tracker:
            option3_label = Text("Option 3: High", font_size=20, color=RED).next_to(option2_label, DOWN, buff=0.3, aligned_edge=LEFT)
            arrow3 = Arrow(
                rest_week5_cell.get_bottom() + DOWN*0.5,
                high_week6_cell.get_left(),
                buff=0.1,
                color=RED,
                stroke_width=4
            )
            calc3 = MathTex(r"\$50", r"+", r"\$70", r"=", r"\$120").scale(0.7)
            calc3.next_to(option3_label, RIGHT, buff=0.5)
            calc3[0].set_color(RED)
            calc3[2].set_color(RED)
            calc3[4].set_color(RED)
            self.play(
                Write(option3_label),
                GrowFromEdge(arrow3, edge=LEFT),
                run_time=tracker.duration * 0.4
            )
            self.play(Flash(high_week6_cell.get_center(), color=RED, flash_radius=0.5))
            self.play(
                Write(calc3, lag_ratio=0.15),
                run_time=tracker.duration * 0.6
            )
        self.wait(0.5)
        # Narration: "The best option is resting. Counter-intuitive, but the math is clear."
        # Visual: Highlight the Rest option glowing gold. Fill cell (Rest, Week 5) with '$130'.
        with self.voiceover(text="The best option is resting. Counter-intuitive, but the math is clear.") as tracker:
            self.play(
                Indicate(calc1, color=GOLD, scale_factor=1.2),
                Indicate(option1_label, color=GOLD, scale_factor=1.2),
                run_time=tracker.duration * 0.4
            )
            rest_week5_cell.generate_target()
            rest_week5_cell.target.set_fill(color=GOLD, opacity=0.3)
            rest_week5_cell.target.set_stroke(color=GOLD, width=5)
            new_value = Text("$130", font_size=28, color=GOLD, weight="BOLD").move_to(rest_week5_cell.get_center())
            self.play(
                MoveToTarget(rest_week5_cell),
                Transform(rest_week5_value, new_value),
                run_time=tracker.duration * 0.4
            )
            self.play(Flash(rest_week5_cell.get_center(), color=GOLD, flash_radius=0.8, line_length=0.3))
        self.wait(0.5)
        # Narration: "This is why greedy fails. It only sees the fifty dollars now."
        # Visual: Show greedy choice (High: $50) vs optimal choice (Rest: $130). Animate the difference.
        with self.voiceover(text="This is why greedy fails. It only sees the fifty dollars now.") as tracker:
            # Fade out arrows and some elements
            self.play(
                FadeOut(arrow1),
                FadeOut(arrow2),
                FadeOut(arrow3),
                FadeOut(rest_week6_cell),
                FadeOut(low_week6_cell),
                FadeOut(high_week6_cell),
                FadeOut(rest_week6_value),
                FadeOut(low_week6_value),
                FadeOut(high_week6_value),
                FadeOut(week6_header),
                run_time=0.5
            )
            # Create comparison
            comparison_title = Text("Greedy vs Optimal", font_size=32, color=WHITE).move_to(UP*2.5)
            greedy_box = Rectangle(width=3, height=2, color=RED, stroke_width=4).shift(LEFT*3 + DOWN*0.5)
            greedy_title = Text("Greedy", font_size=24, color=RED).next_to(greedy_box, UP, buff=0.2)
            greedy_choice = Text("Choose High", font_size=20, color=RED).move_to(greedy_box.get_center() + UP*0.4)
            greedy_value = Text("$50 now", font_size=28, color=RED, weight="BOLD").move_to(greedy_box.get_center() + DOWN*0.3)
            optimal_box = Rectangle(width=3, height=2, color=GOLD, stroke_width=4).shift(RIGHT*3 + DOWN*0.5)
            optimal_title = Text("Optimal", font_size=24, color=GOLD).next_to(optimal_box, UP, buff=0.2)
            optimal_choice = Text("Choose Rest", font_size=20, color=GOLD).move_to(optimal_box.get_center() + UP*0.4)
            optimal_value = Text("$130 total", font_size=28, color=GOLD, weight="BOLD").move_to(optimal_box.get_center() + DOWN*0.3)
            self.play(
                FadeOut(option1_label),
                FadeOut(option2_label),
                FadeOut(option3_label),
                FadeOut(calc1),
                FadeOut(calc2),
                FadeOut(calc3),
                FadeOut(table_title),
                FadeOut(week5_header),
                FadeOut(rest_label),
                FadeOut(low_label),
                FadeOut(high_label),
                FadeOut(rest_week5_cell),
                FadeOut(rest_week5_value),
                run_time=0.5
            )
            self.play(
                Write(comparison_title),
                run_time=tracker.duration * 0.2
            )
            self.play(
                LaggedStart(
                    AnimationGroup(
                        Create(greedy_box),
                        Write(greedy_title),
                        Write(greedy_choice),
                        Write(greedy_value)
                    ),
                    AnimationGroup(
                        Create(optimal_box),
                        Write(optimal_title),
                        Write(optimal_choice),
                        Write(optimal_value)
                    ),
                    lag_ratio=0.3
                ),
                run_time=tracker.duration * 0.6
            )
            self.play(Indicate(greedy_value, color=RED, scale_factor=1.3), run_time=tracker.duration * 0.2)
        self.wait(0.5)
        # Narration: "The Bellman equation sees the whole future compressed into one number."
        # Visual: Show the equation again, with the future value glowing. Text: 'The future, summarized'.
        with self.voiceover(text="The Bellman equation sees the whole future compressed into one number.") as tracker:
            self.play(
                FadeOut(greedy_box),
                FadeOut(greedy_title),
                FadeOut(greedy_choice),
                FadeOut(greedy_value),
                FadeOut(optimal_box),
                FadeOut(optimal_title),
                FadeOut(optimal_choice),
                FadeOut(optimal_value),
                FadeOut(comparison_title),
                run_time=0.5
            )
            final_equation = MathTex(
                r"\text{Value}(\text{state}, \text{week})", 
                r"=", 
                r"\text{reward}", 
                r"+", 
                r"\text{Value}(\text{next\_state}, \text{week}+1)"
            ).scale(0.9)
            final_equation.move_to(ORIGIN + UP*0.5)
            self.play(Write(final_equation, lag_ratio=0.1), run_time=tracker.duration * 0.3)
            future_highlight = SurroundingRectangle(
                final_equation[4],
                color=BLUE,
                buff=0.15,
                corner_radius=0.1
            )
            future_highlight.set_fill(color=BLUE, opacity=0.2)
            summary_text = Text("The future, summarized", font_size=28, color=BLUE, slant="ITALIC")
            summary_text.next_to(final_equation, DOWN, buff=0.8)
            self.play(
                Create(future_highlight),
                run_time=tracker.duration * 0.3
            )
            self.play(
                final_equation[4].animate.set_color(BLUE),
                Write(summary_text, lag_ratio=0.1),
                run_time=tracker.duration * 0.4
            )
            self.play(
                Flash(final_equation[4].get_center(), color=BLUE, flash_radius=0.8),
                Indicate(summary_text, color=BLUE, scale_factor=1.2)
            )
        self.wait(2)


        # ==========================================================
        # SCENE 8: Why This Actually Works
        # ==========================================================
        # Clear previous scene
        if self.mobjects:
            self.play(*[FadeOut(obj) for obj in self.mobjects], run_time=0.5)
        # Narration: "But why does this give us the truly optimal answer?"
        # Visual: Show a question mark with the DP table in the background.
        with self.voiceover(text="But why does this give us the truly optimal answer?") as tracker:
            # Create DP table in background
            table = VGroup()
            for i in range(5):
                row = VGroup()
                for j in range(9):
                    cell = Square(side_length=0.5, color=BLUE, fill_opacity=0.1, stroke_width=1)
                    value = MathTex(str(np.random.randint(10, 50)), font_size=20)
                    cell_group = VGroup(cell, value)
                    row.add(cell_group)
                row.arrange(RIGHT, buff=0.05)
                table.add(row)
            table.arrange(DOWN, buff=0.05)
            table.scale(0.8).set_opacity(0.3)
            # Create large question mark
            question_mark = MathTex("?", font_size=120, color=YELLOW)
            question_mark.move_to(ORIGIN)
            self.play(
                FadeIn(table, shift=DOWN*0.3),
                run_time=tracker.duration * 0.5
            )
            self.play(
                Write(question_mark, lag_ratio=0.1),
                run_time=tracker.duration * 0.5
            )
        # Narration: "The key is a property called optimal substructure."
        # Visual: Display text: 'Optimal Substructure' with a glowing border.
        with self.voiceover(text="The key is a property called optimal substructure.") as tracker:
            self.play(FadeOut(question_mark, shift=UP*0.5), run_time=0.4)
            title = Text("Optimal Substructure", font_size=48, color=GOLD, weight="BOLD")
            title.move_to(ORIGIN)
            border = SurroundingRectangle(title, color=GOLD, buff=0.3, stroke_width=4)
            border.set_fill(GOLD, opacity=0.1)
            self.play(
                Write(title, lag_ratio=0.05),
                Create(border),
                run_time=tracker.duration * 0.7
            )
            self.play(
                Flash(title.get_center(), color=GOLD, flash_radius=1.5),
                run_time=tracker.duration * 0.3
            )
        # Narration: "If your overall plan is optimal, then every piece of it must be optimal too."
        # Visual: Show a path through the table. Highlight one segment glowing gold.
        with self.voiceover(text="If your overall plan is optimal, then every piece of it must be optimal too.") as tracker:
            self.play(
                FadeOut(title, shift=UP*0.3),
                FadeOut(border, shift=UP*0.3),
                table.animate.set_opacity(1.0).scale(1.25),
                run_time=0.6
            )
            # Create a path through the table
            path_cells = [
                table[0][0], table[0][1], table[1][1], table[1][2], 
                table[2][2], table[2][3], table[3][3], table[4][3]
            ]
            # Highlight entire path
            self.play(
                LaggedStart(*[cell[0].animate.set_fill(GOLD, opacity=0.5).set_stroke(GOLD, width=3) 
                              for cell in path_cells],
                            lag_ratio=0.15),
                run_time=tracker.duration * 0.6
            )
            # Emphasize one segment
            segment = VGroup(path_cells[2][0], path_cells[3][0], path_cells[4][0])
            self.play(
                segment.animate.set_fill(YELLOW, opacity=0.8),
                Flash(path_cells[3].get_center(), color=YELLOW),
                run_time=tracker.duration * 0.4
            )
        # Narration: "Imagine your plan from week three onward is the best possible."
        # Visual: Highlight cells from week 3 to 8 as a connected path.
        with self.voiceover(text="Imagine your plan from week three onward is the best possible.") as tracker:
            # Reset previous highlights
            for cell in path_cells:
                cell[0].set_fill(BLUE, opacity=0.1).set_stroke(BLUE, width=1)
            # Create path from week 3 onward (columns 2-8)
            week3_path = [
                table[0][2], table[1][3], table[2][4], table[3][5], table[4][6]
            ]
            # Add connecting arrows
            arrows = VGroup()
            for i in range(len(week3_path) - 1):
                arrow = Arrow(
                    week3_path[i].get_center(),
                    week3_path[i+1].get_center(),
                    buff=0.15,
                    color=GOLD,
                    stroke_width=3,
                    max_tip_length_to_length_ratio=0.15
                )
                arrows.add(arrow)
            self.play(
                LaggedStart(*[cell[0].animate.set_fill(GOLD, opacity=0.6).set_stroke(GOLD, width=3) 
                              for cell in week3_path],
                            lag_ratio=0.2),
                run_time=tracker.duration * 0.6
            )
            self.play(
                LaggedStart(*[Create(arrow) for arrow in arrows], lag_ratio=0.2),
                run_time=tracker.duration * 0.4
            )
        # Narration: "But your plan from week five onward is suboptimal."
        # Visual: Show a different, better path from week 5 to 8 appearing in green.
        with self.voiceover(text="But your plan from week five onward is suboptimal.") as tracker:
            # Alternative better path from week 5
            better_path = [
                table[2][4], table[1][5], table[0][6], table[0][7]
            ]
            better_arrows = VGroup()
            for i in range(len(better_path) - 1):
                arrow = Arrow(
                    better_path[i].get_center(),
                    better_path[i+1].get_center(),
                    buff=0.15,
                    color=GREEN,
                    stroke_width=4,
                    max_tip_length_to_length_ratio=0.15
                )
                better_arrows.add(arrow)
            self.play(
                LaggedStart(*[cell[0].animate.set_fill(GREEN, opacity=0.7).set_stroke(GREEN, width=4) 
                              for cell in better_path],
                            lag_ratio=0.2),
                run_time=tracker.duration * 0.6
            )
            self.play(
                LaggedStart(*[Create(arrow) for arrow in better_arrows], lag_ratio=0.2),
                run_time=tracker.duration * 0.4
            )
        # Narration: "Then you could swap in the better path and improve your overall plan."
        # Visual: Animate replacing the old path with the green path. Show total value increasing.
        with self.voiceover(text="Then you could swap in the better path and improve your overall plan.") as tracker:
            # Fade out old path segments from week 5 onward
            old_segments = [week3_path[2], week3_path[3], week3_path[4]]
            old_arrows_subset = VGroup(arrows[2], arrows[3])
            # Show value labels
            old_value = MathTex("75", font_size=40, color=GOLD).to_edge(UP).shift(LEFT*2)
            old_label = Text("Old:", font_size=30, color=GOLD).next_to(old_value, LEFT)
            new_value = MathTex("92", font_size=40, color=GREEN).to_edge(UP).shift(RIGHT*2)
            new_label = Text("New:", font_size=30, color=GREEN).next_to(new_value, LEFT)
            self.play(
                FadeIn(old_label, shift=DOWN*0.2),
                FadeIn(old_value, shift=DOWN*0.2),
                run_time=tracker.duration * 0.3
            )
            self.play(
                LaggedStart(*[cell[0].animate.set_fill(RED, opacity=0.3).set_stroke(RED, width=2) 
                              for cell in old_segments],
                            lag_ratio=0.1),
                old_arrows_subset.animate.set_color(RED).set_opacity(0.3),
                run_time=tracker.duration * 0.3
            )
            self.play(
                FadeIn(new_label, shift=DOWN*0.2),
                FadeIn(new_value, shift=DOWN*0.2),
                better_arrows.animate.set_stroke(width=5),
                run_time=tracker.duration * 0.4
            )
        # Narration: "This contradicts the assumption that your original plan was optimal."
        # Visual: Show a red X over the original path. Display: 'Contradiction!'.
        with self.voiceover(text="This contradicts the assumption that your original plan was optimal.") as tracker:
            # Create big red X
            x_line1 = Line(table.get_corner(UL) + DOWN*0.5, table.get_corner(DR) + UP*0.5, 
                           color=RED, stroke_width=8)
            x_line2 = Line(table.get_corner(UR) + DOWN*0.5, table.get_corner(DL) + UP*0.5, 
                           color=RED, stroke_width=8)
            red_x = VGroup(x_line1, x_line2)
            contradiction_text = Text("Contradiction!", font_size=56, color=RED, weight="BOLD")
            contradiction_text.next_to(table, DOWN, buff=0.5)
            self.play(
                Create(x_line1),
                Create(x_line2),
                run_time=tracker.duration * 0.5
            )
            self.play(
                Write(contradiction_text, lag_ratio=0.05),
                Flash(contradiction_text.get_center(), color=RED, flash_radius=2.0),
                run_time=tracker.duration * 0.5
            )
        # Narration: "So if the whole is optimal, every part must be optimal."
        # Visual: Show the golden path again, with every segment glowing. Text: 'All pieces optimal'.
        with self.voiceover(text="So if the whole is optimal, every part must be optimal.") as tracker:
            # Clear contradiction
            self.play(
                FadeOut(red_x, shift=DOWN*0.3),
                FadeOut(contradiction_text, shift=DOWN*0.3),
                FadeOut(old_label), FadeOut(old_value),
                FadeOut(new_label), FadeOut(new_value),
                FadeOut(arrows), FadeOut(better_arrows),
                run_time=0.5
            )
            # Create complete optimal path
            optimal_path = [
                table[0][0], table[0][1], table[1][2], table[2][3], 
                table[3][4], table[3][5], table[4][6], table[4][7]
            ]
            # Reset all cells
            for row in table:
                for cell in row:
                    cell[0].set_fill(BLUE, opacity=0.1).set_stroke(BLUE, width=1)
            # Highlight optimal path with glow effect
            self.play(
                LaggedStart(*[cell[0].animate.set_fill(GOLD, opacity=0.7).set_stroke(GOLD, width=4) 
                              for cell in optimal_path],
                            lag_ratio=0.1),
                run_time=tracker.duration * 0.5
            )
            # Add glow pulses
            self.play(
                LaggedStart(*[Flash(cell.get_center(), color=YELLOW, flash_radius=0.4) 
                              for cell in optimal_path],
                            lag_ratio=0.08),
                run_time=tracker.duration * 0.3
            )
            all_optimal_text = Text("All pieces optimal", font_size=44, color=GOLD, weight="BOLD")
            all_optimal_text.to_edge(DOWN, buff=0.8)
            self.play(
                FadeIn(all_optimal_text, shift=UP*0.3),
                run_time=tracker.duration * 0.2
            )
        # Narration: "This means we can build the optimal solution from optimal pieces."
        # Visual: Animate building the path segment by segment, each piece clicking into place.
        with self.voiceover(text="This means we can build the optimal solution from optimal pieces.") as tracker:
            self.play(FadeOut(all_optimal_text, shift=DOWN*0.3), run_time=0.3)
            # Reset path
            for cell in optimal_path:
                cell[0].set_fill(BLUE, opacity=0.1).set_stroke(BLUE, width=1)
            # Build piece by piece with connecting arrows
            build_arrows = VGroup()
            for i in range(len(optimal_path)):
                cell = optimal_path[i]
                # Highlight cell
                self.play(
                    cell[0].animate.set_fill(GOLD, opacity=0.7).set_stroke(GOLD, width=4),
                    cell.animate.scale(1.2),
                    run_time=tracker.duration / len(optimal_path) * 0.6
                )
                self.play(
                    cell.animate.scale(1/1.2),
                    run_time=tracker.duration / len(optimal_path) * 0.2
                )
                # Add arrow to next cell
                if i < len(optimal_path) - 1:
                    arrow = Arrow(
                        cell.get_center(),
                        optimal_path[i+1].get_center(),
                        buff=0.15,
                        color=GOLD,
                        stroke_width=3,
                        max_tip_length_to_length_ratio=0.15
                    )
                    build_arrows.add(arrow)
                    self.play(
                        Create(arrow),
                        run_time=tracker.duration / len(optimal_path) * 0.2
                    )
        # Narration: "And that's exactly what our table does, one cell at a time."
        # Visual: Show the table filling animation again, each cell building on previous ones.
        with self.voiceover(text="And that's exactly what our table does, one cell at a time.") as tracker:
            # Clear current visualization
            self.play(
                FadeOut(build_arrows),
                run_time=0.3
            )
            # Reset all cells
            for row in table:
                for cell in row:
                    cell[0].set_fill(BLUE, opacity=0.1).set_stroke(BLUE, width=1)
            # Animate filling table row by row, left to right
            all_cells = []
            for row in table:
                for cell in row:
                    all_cells.append(cell)
            # Fill animation with building effect
            fill_animations = []
            for i, cell in enumerate(all_cells):
                fill_animations.append(
                    AnimationGroup(
                        cell[0].animate.set_fill(BLUE, opacity=0.5).set_stroke(BLUE, width=2),
                        Flash(cell.get_center(), color=BLUE, flash_radius=0.3, line_length=0.2)
                    )
                )
            self.play(
                LaggedStart(*fill_animations, lag_ratio=0.03),
                run_time=tracker.duration
            )
            # Final emphasis
            self.play(
                table.animate.set_fill(GOLD, opacity=0.6).set_stroke(GOLD, width=3),
                run_time=0.5
            )
        self.wait(2)


        # ==========================================================
        # SCENE 9: The Moving Cost Problem
        # ==========================================================
        # Clear any existing mobjects
        if self.mobjects:
            self.play(*[FadeOut(obj) for obj in self.mobjects], run_time=0.5)
        # Narration: "Let's level up with a harder problem. You're running a business in two cities."
        # Visual: Draw two city skylines: New York (left) and San Francisco (right).
        with self.voiceover(text="Let's level up with a harder problem. You're running a business in two cities.") as tracker:
            # Create New York skyline (left)
            ny_buildings = VGroup(
                Rectangle(width=0.6, height=2.0, color=BLUE).set_fill(BLUE, opacity=0.7),
                Rectangle(width=0.5, height=1.5, color=BLUE).set_fill(BLUE, opacity=0.7),
                Rectangle(width=0.7, height=2.5, color=BLUE).set_fill(BLUE, opacity=0.7),
                Rectangle(width=0.4, height=1.2, color=BLUE).set_fill(BLUE, opacity=0.7)
            ).arrange(RIGHT, buff=0.1).shift(LEFT * 4 + DOWN * 0.5)
            ny_label = Text("New York", font_size=28, color=BLUE).next_to(ny_buildings, UP, buff=0.3)
            ny_group = VGroup(ny_buildings, ny_label)
            # Create San Francisco skyline (right)
            sf_buildings = VGroup(
                Rectangle(width=0.5, height=1.8, color=ORANGE).set_fill(ORANGE, opacity=0.7),
                Rectangle(width=0.6, height=2.2, color=ORANGE).set_fill(ORANGE, opacity=0.7),
                Rectangle(width=0.4, height=1.4, color=ORANGE).set_fill(ORANGE, opacity=0.7),
                Rectangle(width=0.7, height=1.9, color=ORANGE).set_fill(ORANGE, opacity=0.7)
            ).arrange(RIGHT, buff=0.1).shift(RIGHT * 4 + DOWN * 0.5)
            sf_label = Text("San Francisco", font_size=28, color=ORANGE).next_to(sf_buildings, UP, buff=0.3)
            sf_group = VGroup(sf_buildings, sf_label)
            # POLISH: Stagger the appearance with LaggedStart
            self.play(
                LaggedStart(
                    FadeIn(ny_group, shift=DOWN * 0.5),
                    FadeIn(sf_group, shift=DOWN * 0.5),
                    lag_ratio=0.3
                ),
                run_time=tracker.duration
            )
        # Narration: "Each month, operating costs are different in each city."
        # Visual: Show a timeline below with costs: NY: $5, $3, $8, $2... SF: $4, $7, $2, $6...
        with self.voiceover(text="Each month, operating costs are different in each city.") as tracker:
            # Create cost labels for NY
            ny_costs = [5, 3, 8, 2]
            ny_cost_labels = VGroup(*[
                Text(f"${cost}", font_size=20, color=BLUE)
                for cost in ny_costs
            ]).arrange(RIGHT, buff=0.4).next_to(ny_buildings, DOWN, buff=0.5)
            # Create cost labels for SF
            sf_costs = [4, 7, 2, 6]
            sf_cost_labels = VGroup(*[
                Text(f"${cost}", font_size=20, color=ORANGE)
                for cost in sf_costs
            ]).arrange(RIGHT, buff=0.4).next_to(sf_buildings, DOWN, buff=0.5)
            # POLISH: Write with lag_ratio for sequential appearance
            self.play(
                Write(ny_cost_labels, lag_ratio=0.2),
                Write(sf_cost_labels, lag_ratio=0.2),
                run_time=tracker.duration
            )
        # Narration: "You can move between cities, but moving costs money."
        # Visual: Draw a bridge between the cities labeled 'Moving Cost: $10'.
        with self.voiceover(text="You can move between cities, but moving costs money.") as tracker:
            # Create curved arrow between cities
            bridge = Arc(
                radius=4.5,
                start_angle=PI * 0.2,
                angle=PI * 0.6,
                color=RED
            ).shift(DOWN * 0.3)
            arrow_tip_1 = Arrow(
                start=bridge.point_from_proportion(0.95),
                end=bridge.point_from_proportion(1.0),
                color=RED,
                buff=0,
                stroke_width=4,
                max_tip_length_to_length_ratio=0.5
            )
            arrow_tip_2 = Arrow(
                start=bridge.point_from_proportion(0.05),
                end=bridge.point_from_proportion(0.0),
                color=RED,
                buff=0,
                stroke_width=4,
                max_tip_length_to_length_ratio=0.5
            )
            moving_cost_label = Text("Moving Cost: $10", font_size=24, color=RED).move_to(UP * 1.2)
            # POLISH: Create with smooth rate function and add emphasis
            self.play(
                Create(bridge, rate_func=smooth),
                run_time=tracker.duration * 0.6
            )
            self.play(
                FadeIn(arrow_tip_1, shift=LEFT * 0.2),
                FadeIn(arrow_tip_2, shift=RIGHT * 0.2),
                FadeIn(moving_cost_label, shift=DOWN * 0.2),
                run_time=tracker.duration * 0.4
            )
        # Clear the stage for the table
        with self.voiceover(text="Now your state isn't just time. It's time and location.") as tracker:
            all_elements = VGroup(ny_group, sf_group, ny_cost_labels, sf_cost_labels, bridge, arrow_tip_1, arrow_tip_2, moving_cost_label)
            self.play(
                FadeOut(all_elements, shift=UP * 0.5),
                run_time=tracker.duration * 0.5
            )
            # Create 2D table: rows are NY/SF, columns are months 1-12
            # Create row labels
            row_label_ny = Text("NY", font_size=24, color=BLUE).shift(LEFT * 5.5 + UP * 1.0)
            row_label_sf = Text("SF", font_size=24, color=ORANGE).shift(LEFT * 5.5 + DOWN * 1.0)
            # Create column labels (months 1-12, but show only 1-6 for space)
            month_labels = VGroup(*[
                Text(str(i), font_size=18, color=WHITE)
                for i in range(1, 7)
            ]).arrange(RIGHT, buff=0.6).shift(UP * 2.5 + RIGHT * 0.5)
            # Create grid cells (6 months shown)
            cells_ny = VGroup(*[
                Rectangle(width=0.8, height=0.8, color=BLUE, stroke_width=2)
                for _ in range(6)
            ]).arrange(RIGHT, buff=0.1).shift(UP * 1.0 + RIGHT * 0.5)
            cells_sf = VGroup(*[
                Rectangle(width=0.8, height=0.8, color=ORANGE, stroke_width=2)
                for _ in range(6)
            ]).arrange(RIGHT, buff=0.1).shift(DOWN * 1.0 + RIGHT * 0.5)
            table_group = VGroup(row_label_ny, row_label_sf, month_labels, cells_ny, cells_sf)
            # POLISH: Build table with staggered animations
            self.play(
                LaggedStart(
                    FadeIn(row_label_ny, shift=RIGHT * 0.3),
                    FadeIn(row_label_sf, shift=RIGHT * 0.3),
                    Write(month_labels, lag_ratio=0.1),
                    Create(cells_ny, lag_ratio=0.05),
                    Create(cells_sf, lag_ratio=0.05),
                    lag_ratio=0.2
                ),
                run_time=tracker.duration * 0.5
            )
        # Narration: "Each cell asks: if I'm in this city this month, what's my minimum total cost?"
        # Visual: Highlight cell (NY, Month 5). Show text: 'Min cost from here to end?'.
        with self.voiceover(text="Each cell asks: if I'm in this city this month, what's my minimum total cost?") as tracker:
            # Highlight cell (NY, Month 5) - index 4
            highlight_cell = cells_ny[4].copy().set_stroke(YELLOW, width=6)
            question_text = Text("Min cost from\nhere to end?", font_size=20, color=YELLOW).next_to(cells_ny[4], DOWN, buff=0.5)
            # POLISH: Use Circumscribe for emphasis
            self.play(
                Create(highlight_cell),
                run_time=tracker.duration * 0.4
            )
            self.play(
                FadeIn(question_text, shift=UP * 0.2),
                run_time=tracker.duration * 0.4
            )
            self.play(
                Indicate(highlight_cell, color=YELLOW, scale_factor=1.2),
                run_time=tracker.duration * 0.2
            )
        # Narration: "At month twelve, you're done. Cost is zero regardless of location."
        # Visual: Fill the rightmost column (month 12) with '$0' for both NY and SF.
        with self.voiceover(text="At month twelve, you're done. Cost is zero regardless of location.") as tracker:
            # Remove previous highlight
            self.play(
                FadeOut(highlight_cell),
                FadeOut(question_text),
                run_time=0.3
            )
            # Add month 12 label and cells
            month_12_label = Text("12", font_size=18, color=WHITE).next_to(month_labels, RIGHT, buff=1.2)
            cell_ny_12 = Rectangle(width=0.8, height=0.8, color=BLUE, stroke_width=2).next_to(cells_ny, RIGHT, buff=0.6)
            cell_sf_12 = Rectangle(width=0.8, height=0.8, color=ORANGE, stroke_width=2).next_to(cells_sf, RIGHT, buff=0.6)
            zero_ny = Text("$0", font_size=20, color=GREEN).move_to(cell_ny_12.get_center())
            zero_sf = Text("$0", font_size=20, color=GREEN).move_to(cell_sf_12.get_center())
            # POLISH: Emphasize the final column
            self.play(
                FadeIn(month_12_label, shift=DOWN * 0.2),
                Create(cell_ny_12),
                Create(cell_sf_12),
                run_time=tracker.duration * 0.5
            )
            self.play(
                Write(zero_ny),
                Write(zero_sf),
                run_time=tracker.duration * 0.3
            )
            self.play(
                Flash(zero_ny.get_center(), color=GREEN, flash_radius=0.3),
                Flash(zero_sf.get_center(), color=GREEN, flash_radius=0.3),
                run_time=tracker.duration * 0.2
            )
        # Narration: "Month eleven in New York. You can stay or move to SF."
        # Visual: Highlight cell (NY, Month 11). Show two arrows: stay (NY) or move (SF).
        with self.voiceover(text="Month eleven in New York. You can stay or move to SF.") as tracker:
            # Highlight cell (NY, Month 11) - the cell before month 12
            cell_ny_11 = Rectangle(width=0.8, height=0.8, color=BLUE, stroke_width=2).next_to(cells_ny, RIGHT, buff=0.1).shift(LEFT * 0.5)
            highlight_11 = cell_ny_11.copy().set_stroke(YELLOW, width=6)
            # Create arrows: stay (horizontal) and move (diagonal down)
            stay_arrow = Arrow(
                start=cell_ny_11.get_right(),
                end=cell_ny_12.get_left(),
                color=GREEN,
                buff=0.1,
                stroke_width=4
            )
            stay_label = Text("Stay", font_size=16, color=GREEN).next_to(stay_arrow, UP, buff=0.1)
            move_arrow = Arrow(
                start=cell_ny_11.get_right() + DOWN * 0.2,
                end=cell_sf_12.get_left() + UP * 0.2,
                color=RED,
                buff=0.1,
                stroke_width=4
            )
            move_label = Text("Move", font_size=16, color=RED).next_to(move_arrow, DOWN, buff=0.1)
            # POLISH: Sequential reveal with emphasis
            self.play(
                Create(highlight_11),
                run_time=tracker.duration * 0.3
            )
            self.play(
                GrowFromEdge(stay_arrow, LEFT),
                FadeIn(stay_label, shift=RIGHT * 0.2),
                run_time=tracker.duration * 0.35
            )
            self.play(
                GrowFromEdge(move_arrow, LEFT),
                FadeIn(move_label, shift=RIGHT * 0.2),
                run_time=tracker.duration * 0.35
            )
        # Narration: "Staying costs five dollars this month, plus zero future. Total: five."
        # Visual: Show: 'Stay: $5 operating + $0 future = $5'.
        with self.voiceover(text="Staying costs five dollars this month, plus zero future. Total: five.") as tracker:
            stay_calc = MathTex(
                r"\text{Stay: } \$5", r" + ", r"\$0", r" = ", r"\$5",
                font_size=28,
                color=GREEN
            ).next_to(stay_arrow, UP, buff=0.8)
            # POLISH: Reveal calculation step by step
            self.play(
                Write(stay_calc[0:3], lag_ratio=0.2),
                run_time=tracker.duration * 0.5
            )
            self.play(
                Write(stay_calc[3:5]),
                run_time=tracker.duration * 0.3
            )
            self.play(
                Circumscribe(stay_calc[4], color=GREEN, buff=0.1),
                run_time=tracker.duration * 0.2
            )
        # Narration: "Moving costs ten for the move, plus four for SF operations. Total: fourteen."
        # Visual: Show: 'Move: $10 moving + $4 operating + $0 future = $14'.
        with self.voiceover(text="Moving costs ten for the move, plus four for SF operations. Total: fourteen.") as tracker:
            move_calc = MathTex(
                r"\text{Move: } \$10", r" + ", r"\$4", r" + ", r"\$0", r" = ", r"\$14",
                font_size=28,
                color=RED
            ).next_to(move_arrow, DOWN, buff=0.8)
            # POLISH: Reveal calculation step by step
            self.play(
                Write(move_calc[0:5], lag_ratio=0.15),
                run_time=tracker.duration * 0.6
            )
            self.play(
                Write(move_calc[5:7]),
                run_time=tracker.duration * 0.3
            )
            self.play(
                Circumscribe(move_calc[6], color=RED, buff=0.1),
                run_time=tracker.duration * 0.1
            )
        # Narration: "Staying is cheaper. The moving cost makes switching expensive."
        # Visual: Fill cell (NY, Month 11) with '$5'. Highlight it as the better choice.
        with self.voiceover(text="Staying is cheaper. The moving cost makes switching expensive.") as tracker:
            # Create the $5 value in the cell
            value_11 = Text("$5", font_size=20, color=GREEN).move_to(cell_ny_11.get_center())
            # Dim the move option
            self.play(
                move_arrow.animate.set_opacity(0.3),
                move_label.animate.set_opacity(0.3),
                move_calc.animate.set_opacity(0.3),
                run_time=tracker.duration * 0.3
            )
            # POLISH: Emphasize the winning choice
            self.play(
                stay_arrow.animate.set_stroke(width=6),
                stay_calc.animate.scale(1.2),
                run_time=tracker.duration * 0.3
            )
            self.play(
                FadeIn(value_11, scale=1.5),
                run_time=tracker.duration * 0.2
            )
            self.play(
                Flash(value_11.get_center(), color=GREEN, flash_radius=0.4),
                Indicate(highlight_11, color=GREEN, scale_factor=1.15),
                run_time=tracker.duration * 0.2
            )
        self.wait(2)


        # ==========================================================
        # SCENE 10: When Your Opponent Thinks
        # ==========================================================
        # Clear any existing mobjects
        if self.mobjects:
            self.play(*[FadeOut(obj) for obj in self.mobjects], run_time=0.5)
        # Narration: "What if the future isn't just uncertain, but actively against you?"
        # Visual: Show two characters: Alice (blue) and Bob (red) facing each other.
        with self.voiceover(text="What if the future isn't just uncertain, but actively against you?") as tracker:
            # Create Alice (blue character on left)
            alice_circle = Circle(radius=0.6, color=BLUE, fill_opacity=0.8)
            alice_label = Text("Alice", font_size=28, color=WHITE).move_to(alice_circle.get_center())
            alice = VGroup(alice_circle, alice_label).shift(LEFT * 3.5)
            # Create Bob (red character on right)
            bob_circle = Circle(radius=0.6, color=RED, fill_opacity=0.8)
            bob_label = Text("Bob", font_size=28, color=WHITE).move_to(bob_circle.get_center())
            bob = VGroup(bob_circle, bob_label).shift(RIGHT * 3.5)
            # Animate both characters appearing with polish
            self.play(
                FadeIn(alice, shift=RIGHT*0.5),
                FadeIn(bob, shift=LEFT*0.5),
                run_time=tracker.duration
            )
        # Narration: "There's a row of coins. Alice and Bob take turns picking from the ends."
        # Visual: Draw a row of coins: [3, 1, 5, 2, 4]. Alice on left, Bob on right.
        with self.voiceover(text="There's a row of coins. Alice and Bob take turns picking from the ends.") as tracker:
            # Create coin values
            coin_values = [3, 1, 5, 2, 4]
            coins = VGroup()
            for val in coin_values:
                coin_circle = Circle(radius=0.4, color=GOLD, fill_opacity=0.9)
                coin_circle.set_stroke(color=YELLOW, width=3)
                coin_text = Text(str(val), font_size=32, color=BLACK, weight="BOLD")
                coin = VGroup(coin_circle, coin_text)
                coins.add(coin)
            coins.arrange(RIGHT, buff=0.3).move_to(ORIGIN).shift(UP * 0.5)
            # Animate coins appearing with lag
            self.play(
                LaggedStart(*[FadeIn(coin, shift=DOWN*0.3) for coin in coins], lag_ratio=0.15),
                run_time=tracker.duration
            )
        # Narration: "Alice wants to maximize her total. Bob wants to minimize it."
        # Visual: Show Alice with an up arrow (maximize), Bob with a down arrow (minimize).
        with self.voiceover(text="Alice wants to maximize her total. Bob wants to minimize it.") as tracker:
            # Create up arrow for Alice (maximize)
            alice_arrow = Arrow(start=ORIGIN, end=UP*0.8, color=BLUE, buff=0, stroke_width=6)
            alice_arrow.next_to(alice, DOWN, buff=0.3)
            alice_max_label = Text("MAX", font_size=20, color=BLUE, weight="BOLD")
            alice_max_label.next_to(alice_arrow, DOWN, buff=0.1)
            alice_goal = VGroup(alice_arrow, alice_max_label)
            # Create down arrow for Bob (minimize)
            bob_arrow = Arrow(start=ORIGIN, end=DOWN*0.8, color=RED, buff=0, stroke_width=6)
            bob_arrow.next_to(bob, DOWN, buff=0.3)
            bob_min_label = Text("MIN", font_size=20, color=RED, weight="BOLD")
            bob_min_label.next_to(bob_arrow, DOWN, buff=0.1)
            bob_goal = VGroup(bob_arrow, bob_min_label)
            self.play(
                GrowFromEdge(alice_arrow, edge=DOWN),
                GrowFromEdge(bob_arrow, edge=UP),
                run_time=tracker.duration * 0.6
            )
            self.play(
                Write(alice_max_label),
                Write(bob_min_label),
                run_time=tracker.duration * 0.4
            )
        # Narration: "Alice goes first. She can take the three or the four."
        # Visual: Highlight the two end coins (3 and 4) glowing.
        with self.voiceover(text="Alice goes first. She can take the three or the four.") as tracker:
            # Highlight first and last coins
            first_coin = coins[0]
            last_coin = coins[4]
            self.play(
                Indicate(first_coin, color=BLUE, scale_factor=1.3),
                Indicate(last_coin, color=BLUE, scale_factor=1.3),
                run_time=tracker.duration * 0.7
            )
            self.play(
                Circumscribe(first_coin, color=BLUE, buff=0.1),
                Circumscribe(last_coin, color=BLUE, buff=0.1),
                run_time=tracker.duration * 0.3
            )
        # Narration: "If she takes the three, Bob will respond optimally to hurt her."
        # Visual: Show a tree: Alice takes 3, then Bob's two choices (1 or 4) branching.
        with self.voiceover(text="If she takes the three, Bob will respond optimally to hurt her.") as tracker:
            # Move coins up to make room for tree
            self.play(
                coins.animate.shift(UP * 1.5),
                alice.animate.shift(UP * 1.5),
                bob.animate.shift(UP * 1.5),
                alice_goal.animate.shift(UP * 1.5),
                bob_goal.animate.shift(UP * 1.5),
                run_time=0.8
            )
            # Create tree structure
            root = Circle(radius=0.3, color=BLUE, fill_opacity=0.8).shift(DOWN * 0.5)
            root_text = Text("A:3", font_size=20, color=WHITE).move_to(root.get_center())
            root_node = VGroup(root, root_text)
            # Bob's two choices
            left_choice = Circle(radius=0.3, color=RED, fill_opacity=0.8).shift(DOWN * 1.8 + LEFT * 1.5)
            left_text = Text("B:1", font_size=20, color=WHITE).move_to(left_choice.get_center())
            left_node = VGroup(left_choice, left_text)
            right_choice = Circle(radius=0.3, color=RED, fill_opacity=0.8).shift(DOWN * 1.8 + RIGHT * 1.5)
            right_text = Text("B:4", font_size=20, color=WHITE).move_to(right_choice.get_center())
            right_node = VGroup(right_choice, right_text)
            # Connecting lines
            line_left = Line(root.get_bottom(), left_choice.get_top(), color=WHITE, stroke_width=2)
            line_right = Line(root.get_bottom(), right_choice.get_top(), color=WHITE, stroke_width=2)
            self.play(
                FadeIn(root_node, shift=DOWN*0.2),
                run_time=tracker.duration * 0.3
            )
            self.play(
                Create(line_left),
                Create(line_right),
                run_time=tracker.duration * 0.3
            )
            self.play(
                FadeIn(left_node, shift=DOWN*0.2),
                FadeIn(right_node, shift=DOWN*0.2),
                run_time=tracker.duration * 0.4
            )
        # Narration: "Bob will take the four, leaving Alice with worse options."
        # Visual: Animate Bob taking 4. Remaining coins: [1, 5, 2]. Show Bob's choice glowing red.
        with self.voiceover(text="Bob will take the four, leaving Alice with worse options.") as tracker:
            # Highlight Bob's choice of 4
            self.play(
                Indicate(right_node, color=RED, scale_factor=1.4),
                Flash(right_node.get_center(), color=RED, flash_radius=0.5),
                run_time=tracker.duration * 0.5
            )
            # Show remaining coins [1, 5, 2]
            remaining_text = Text("Remaining: [1, 5, 2]", font_size=28, color=ORANGE)
            remaining_text.next_to(right_node, DOWN, buff=0.5)
            self.play(
                Write(remaining_text, lag_ratio=0.1),
                run_time=tracker.duration * 0.5
            )
        # Clear the tree for next section
        self.play(
            *[FadeOut(obj) for obj in [root_node, left_node, right_node, line_left, line_right, remaining_text]],
            run_time=0.5
        )
        # Narration: "The DP table now alternates: Alice's turns maximize, Bob's turns minimize."
        # Visual: Show a table with rows colored: blue rows (Alice's turn), red rows (Bob's turn).
        with self.voiceover(text="The DP table now alternates: Alice's turns maximize, Bob's turns minimize.") as tracker:
            # Move everything to top
            self.play(
                coins.animate.scale(0.7).to_edge(UP, buff=0.5),
                FadeOut(alice),
                FadeOut(bob),
                FadeOut(alice_goal),
                FadeOut(bob_goal),
                run_time=0.8
            )
            # Create DP table
            table_rows = 5
            table_cols = 5
            cell_size = 0.6
            dp_table = VGroup()
            for i in range(table_rows):
                row = VGroup()
                # Alternate colors: even rows = Alice (blue), odd rows = Bob (red)
                row_color = BLUE if i % 2 == 0 else RED
                for j in range(table_cols):
                    cell = Square(side_length=cell_size, color=row_color, fill_opacity=0.3)
                    cell.set_stroke(color=WHITE, width=2)
                    row.add(cell)
                row.arrange(RIGHT, buff=0.05)
                dp_table.add(row)
            dp_table.arrange(DOWN, buff=0.05).move_to(ORIGIN).shift(DOWN * 0.3)
            # Add row labels
            alice_label_1 = Text("Alice", font_size=20, color=BLUE).next_to(dp_table[0], LEFT, buff=0.3)
            bob_label_1 = Text("Bob", font_size=20, color=RED).next_to(dp_table[1], LEFT, buff=0.3)
            alice_label_2 = Text("Alice", font_size=20, color=BLUE).next_to(dp_table[2], LEFT, buff=0.3)
            bob_label_2 = Text("Bob", font_size=20, color=RED).next_to(dp_table[3], LEFT, buff=0.3)
            alice_label_3 = Text("Alice", font_size=20, color=BLUE).next_to(dp_table[4], LEFT, buff=0.3)
            labels = VGroup(alice_label_1, bob_label_1, alice_label_2, bob_label_2, alice_label_3)
            self.play(
                LaggedStart(*[FadeIn(row, shift=DOWN*0.2) for row in dp_table], lag_ratio=0.1),
                run_time=tracker.duration * 0.7
            )
            self.play(
                LaggedStart(*[FadeIn(label, shift=RIGHT*0.2) for label in labels], lag_ratio=0.1),
                run_time=tracker.duration * 0.3
            )
        # Narration: "On Alice's turn, we take the max of her options."
        # Visual: Highlight a blue cell. Show: 'max(option1, option2)' with up arrow.
        with self.voiceover(text="On Alice's turn, we take the max of her options.") as tracker:
            # Highlight a blue cell (Alice's row)
            target_cell = dp_table[0][2]
            self.play(
                Indicate(target_cell, color=BLUE, scale_factor=1.3),
                run_time=tracker.duration * 0.3
            )
            # Show max formula
            max_formula = MathTex(r"\max(", r"\text{opt}_1", r",", r"\text{opt}_2", r")", font_size=36, color=BLUE)
            max_formula.next_to(target_cell, UP, buff=0.5)
            up_arrow = Arrow(start=ORIGIN, end=UP*0.5, color=BLUE, buff=0, stroke_width=5)
            up_arrow.next_to(max_formula, RIGHT, buff=0.2)
            self.play(
                Write(max_formula, lag_ratio=0.1),
                GrowFromEdge(up_arrow, edge=DOWN),
                run_time=tracker.duration * 0.7
            )
        # Narration: "On Bob's turn, we take the min, because he's minimizing Alice's gain."
        # Visual: Highlight a red cell. Show: 'min(option1, option2)' with down arrow.
        with self.voiceover(text="On Bob's turn, we take the min, because he's minimizing Alice's gain.") as tracker:
            # Highlight a red cell (Bob's row)
            target_cell_bob = dp_table[1][2]
            self.play(
                Indicate(target_cell_bob, color=RED, scale_factor=1.3),
                run_time=tracker.duration * 0.3
            )
            # Show min formula
            min_formula = MathTex(r"\min(", r"\text{opt}_1", r",", r"\text{opt}_2", r")", font_size=36, color=RED)
            min_formula.next_to(target_cell_bob, DOWN, buff=0.5)
            down_arrow = Arrow(start=ORIGIN, end=DOWN*0.5, color=RED, buff=0, stroke_width=5)
            down_arrow.next_to(min_formula, RIGHT, buff=0.2)
            self.play(
                Write(min_formula, lag_ratio=0.1),
                GrowFromEdge(down_arrow, edge=UP),
                run_time=tracker.duration * 0.7
            )
        # Narration: "The root of the tree gives Alice's guaranteed value under optimal play."
        # Visual: Show the tree collapsing upward, values propagating. Root shows: 'Alice gets: 9'.
        with self.voiceover(text="The root of the tree gives Alice's guaranteed value under optimal play.") as tracker:
            # Fade out formulas
            self.play(
                FadeOut(max_formula),
                FadeOut(up_arrow),
                FadeOut(min_formula),
                FadeOut(down_arrow),
                FadeOut(labels),
                run_time=0.5
            )
            # Create a new tree showing value propagation
            tree_root = Circle(radius=0.4, color=BLUE, fill_opacity=0.9).shift(UP * 1.5)
            tree_root.set_stroke(color=YELLOW, width=4)
            # Animate table cells "flowing" upward into root
            self.play(
                dp_table.animate.scale(0.8).set_opacity(0.3),
                run_time=tracker.duration * 0.3
            )
            # Create value particles flowing up
            particles = VGroup(*[
                Dot(dp_table[i][j].get_center(), radius=0.05, color=BLUE if i % 2 == 0 else RED)
                for i in range(table_rows) for j in range(table_cols)
            ])
            self.play(
                FadeIn(tree_root, scale=0.5),
                *[MoveAlongPath(particle, Line(particle.get_center(), tree_root.get_center())) 
                  for particle in particles],
                run_time=tracker.duration * 0.4
            )
            # Show final result
            result_text = Text("Alice gets: 9", font_size=40, color=YELLOW, weight="BOLD")
            result_text.move_to(tree_root.get_center())
            self.play(
                FadeOut(particles),
                Write(result_text, lag_ratio=0.1),
                Flash(tree_root.get_center(), color=YELLOW, flash_radius=0.8),
                run_time=tracker.duration * 0.3
            )
            # Final emphasis
            self.play(
                Indicate(result_text, color=YELLOW, scale_factor=1.2),
                run_time=1.0
            )
        self.wait(2)


        # ==========================================================
        # SCENE 11: The Inventory Dimension
        # ==========================================================
        # Clear previous scene
        if self.mobjects:
            self.play(*[FadeOut(obj) for obj in self.mobjects], run_time=0.5)
        # Narration: "One more twist. What if your decisions create physical constraints?"
        # Visual: Show a warehouse with empty shelves.
        with self.voiceover(text="One more twist. What if your decisions create physical constraints?") as tracker:
            # Create warehouse structure
            warehouse_floor = Rectangle(width=8, height=0.2, color=GRAY).set_fill(GRAY, opacity=0.8)
            warehouse_floor.to_edge(DOWN, buff=1)
            # Create empty shelves
            shelves = VGroup()
            for i in range(3):
                shelf = Rectangle(width=6, height=0.15, color=GRAY).set_fill(GRAY, opacity=0.6)
                shelf.next_to(warehouse_floor, UP, buff=0.8 + i * 1.2)
                shelves.add(shelf)
            warehouse = VGroup(warehouse_floor, shelves)
            title = Text("Inventory Management Problem", font_size=40, color=BLUE)
            title.to_edge(UP, buff=0.5)
            self.play(
                FadeIn(warehouse, shift=UP*0.3, lag_ratio=0.1),
                Write(title, lag_ratio=0.1),
                run_time=tracker.duration
            )
        # Narration: "You're managing truck inventory. Each month, you sell some trucks."
        # Visual: Animate trucks driving out of the warehouse. Show: 'Demand: 5 trucks/month'.
        with self.voiceover(text="You're managing truck inventory. Each month, you sell some trucks.") as tracker:
            # Create small truck icons on shelves
            trucks = VGroup()
            for i in range(3):
                for j in range(4):
                    truck = Rectangle(width=0.4, height=0.25, color=RED).set_fill(RED, opacity=0.8)
                    truck.move_to(shelves[i].get_center() + LEFT * (1.5 - j * 1.0))
                    # Add wheels
                    wheel1 = Dot(radius=0.06, color=BLACK).next_to(truck, DOWN, buff=0.02).shift(LEFT*0.1)
                    wheel2 = Dot(radius=0.06, color=BLACK).next_to(truck, DOWN, buff=0.02).shift(RIGHT*0.1)
                    truck_group = VGroup(truck, wheel1, wheel2)
                    trucks.add(truck_group)
            self.play(LaggedStart(*[FadeIn(t, shift=DOWN*0.2) for t in trucks], lag_ratio=0.05), run_time=tracker.duration * 0.5)
            # Show demand label
            demand_label = Text("Demand: 5 trucks/month", font_size=28, color=YELLOW)
            demand_label.next_to(warehouse_floor, DOWN, buff=0.5)
            self.play(Write(demand_label, lag_ratio=0.1), run_time=tracker.duration * 0.3)
            # Animate some trucks driving out
            trucks_leaving = trucks[:5]
            self.play(
                LaggedStart(*[t.animate.shift(RIGHT*10) for t in trucks_leaving], lag_ratio=0.1),
                run_time=tracker.duration * 0.2
            )
        # Narration: "You can order more trucks, but ordering costs money."
        # Visual: Show trucks arriving. Display: 'Order Cost: $100 + $20/truck'.
        with self.voiceover(text="You can order more trucks, but ordering costs money.") as tracker:
            # Create new trucks arriving from left
            new_trucks = VGroup()
            for i in range(4):
                truck = Rectangle(width=0.4, height=0.25, color=BLUE).set_fill(BLUE, opacity=0.8)
                wheel1 = Dot(radius=0.06, color=BLACK)
                wheel2 = Dot(radius=0.06, color=BLACK)
                truck_group = VGroup(truck, wheel1, wheel2).arrange(DOWN, buff=0.02)
                truck_group.move_to(LEFT * 8 + UP * (i * 0.5))
                new_trucks.add(truck_group)
            order_cost_label = MathTex(r"\text{Order Cost: } \$100 + \$20/\text{truck}", font_size=32, color=GREEN)
            order_cost_label.next_to(demand_label, DOWN, buff=0.3)
            self.play(
                LaggedStart(*[t.animate.shift(RIGHT*10) for t in new_trucks], lag_ratio=0.15),
                Write(order_cost_label, lag_ratio=0.1),
                run_time=tracker.duration
            )
            self.play(Indicate(order_cost_label, color=YELLOW), run_time=0.8)
        # Narration: "Storing trucks also costs money. Five dollars per truck per month."
        # Visual: Show shelves with trucks. Display: 'Storage: $5/truck/month'.
        with self.voiceover(text="Storing trucks also costs money. Five dollars per truck per month.") as tracker:
            storage_cost_label = MathTex(r"\text{Storage: } \$5/\text{truck}/\text{month}", font_size=32, color=ORANGE)
            storage_cost_label.next_to(order_cost_label, DOWN, buff=0.3)
            # Highlight remaining trucks on shelves
            remaining_trucks = trucks[5:]
            self.play(
                Write(storage_cost_label, lag_ratio=0.1),
                LaggedStart(*[Indicate(t, color=ORANGE) for t in remaining_trucks], lag_ratio=0.05),
                run_time=tracker.duration
            )
            self.play(Circumscribe(storage_cost_label, color=ORANGE), run_time=0.8)
        # Narration: "Now your state is two-dimensional: what month, and how many trucks you have."
        # Visual: Draw a 2D grid: x-axis is months (1-12), y-axis is inventory (0-20 trucks).
        with self.voiceover(text="Now your state is two-dimensional: what month, and how many trucks you have.") as tracker:
            # Fade out warehouse scene
            warehouse_group = Group(*self.mobjects)
            self.play(FadeOut(warehouse_group, shift=DOWN*0.5), run_time=tracker.duration * 0.2)
            # Create 2D grid
            axes = Axes(
                x_range=[0, 12, 1],
                y_range=[0, 20, 5],
                x_length=9,
                y_length=6,
                axis_config={"color": BLUE, "include_numbers": True, "font_size": 24},
                tips=False
            )
            x_label = Text("Month", font_size=28, color=BLUE).next_to(axes.x_axis, DOWN, buff=0.3)
            y_label = Text("Inventory (trucks)", font_size=28, color=BLUE).next_to(axes.y_axis, LEFT, buff=0.3)
            # Create grid lines
            grid_lines = VGroup()
            for x in range(1, 12):
                line = DashedLine(
                    axes.c2p(x, 0),
                    axes.c2p(x, 20),
                    color=GRAY
                ).set_opacity(0.3)
                grid_lines.add(line)
            for y in range(5, 20, 5):
                line = DashedLine(
                    axes.c2p(0, y),
                    axes.c2p(12, y),
                    color=GRAY
                ).set_opacity(0.3)
                grid_lines.add(line)
            self.play(
                Create(axes, lag_ratio=0.1),
                Write(x_label),
                Write(y_label),
                run_time=tracker.duration * 0.6
            )
            self.play(Create(grid_lines, lag_ratio=0.01), run_time=tracker.duration * 0.4)
        # Narration: "Each cell represents a configuration: month three with ten trucks in stock."
        # Visual: Highlight cell (Month 3, 10 trucks). Show a mini warehouse with 10 trucks.
        with self.voiceover(text="Each cell represents a configuration: month three with ten trucks in stock.") as tracker:
            # Highlight specific cell
            cell_point = axes.c2p(3, 10)
            cell_highlight = Rectangle(width=0.75, height=1.5, color=YELLOW).set_fill(YELLOW, opacity=0.3)
            cell_highlight.move_to(cell_point)
            self.play(
                FadeIn(cell_highlight, scale=1.5),
                Flash(cell_point, color=YELLOW, flash_radius=0.5),
                run_time=tracker.duration * 0.4
            )
            # Show mini warehouse with 10 trucks
            mini_trucks = VGroup()
            for i in range(10):
                mini_truck = Rectangle(width=0.15, height=0.1, color=RED).set_fill(RED, opacity=0.8)
                mini_truck.move_to(cell_point + UP*0.4 + LEFT*0.3 + RIGHT*(i%5)*0.12 + DOWN*(i//5)*0.15)
                mini_trucks.add(mini_truck)
            state_label = MathTex(r"\text{State: } (3, 10)", font_size=28, color=YELLOW)
            state_label.next_to(cell_highlight, RIGHT, buff=0.5)
            self.play(
                LaggedStart(*[GrowFromCenter(t) for t in mini_trucks], lag_ratio=0.08),
                Write(state_label),
                run_time=tracker.duration * 0.6
            )
        # Narration: "From here, you decide: order more trucks, or use what you have?"
        # Visual: Show two arrows from the cell: one going right (next month, same inventory), one going up-right (next month, more inventory).
        with self.voiceover(text="From here, you decide: order more trucks, or use what you have?") as tracker:
            # Arrow 1: Use existing inventory (move right, possibly down due to sales)
            arrow1_end = axes.c2p(4, 5)  # Next month, reduced inventory
            arrow1 = Arrow(cell_point, arrow1_end, color=GREEN, buff=0.2, stroke_width=6)
            arrow1_label = Text("Use stock", font_size=20, color=GREEN).next_to(arrow1, DOWN, buff=0.1)
            # Arrow 2: Order more trucks (move right and up)
            arrow2_end = axes.c2p(4, 15)  # Next month, increased inventory
            arrow2 = Arrow(cell_point, arrow2_end, color=BLUE, buff=0.2, stroke_width=6)
            arrow2_label = Text("Order more", font_size=20, color=BLUE).next_to(arrow2, UP, buff=0.1)
            self.play(
                GrowArrow(arrow1),
                Write(arrow1_label, lag_ratio=0.1),
                run_time=tracker.duration * 0.5
            )
            self.play(
                GrowArrow(arrow2),
                Write(arrow2_label, lag_ratio=0.1),
                run_time=tracker.duration * 0.5
            )
        # Narration: "The DP table is now a grid, not a line."
        # Visual: Animate filling the grid from right to left, bottom to top. Cells light up in waves.
        with self.voiceover(text="The DP table is now a grid, not a line.") as tracker:
            # Clear previous highlights
            self.play(
                FadeOut(cell_highlight),
                FadeOut(mini_trucks),
                FadeOut(state_label),
                FadeOut(arrow1),
                FadeOut(arrow1_label),
                FadeOut(arrow2),
                FadeOut(arrow2_label),
                run_time=0.5
            )
            # Create cells for the DP table
            dp_cells = VGroup()
            for month in range(12, 0, -1):  # Right to left
                for inv in range(0, 21, 2):  # Bottom to top
                    cell = Rectangle(width=0.7, height=0.6, color=PURPLE).set_fill(PURPLE, opacity=0.5)
                    cell.move_to(axes.c2p(month, inv))
                    dp_cells.add(cell)
            # Animate filling in waves
            self.play(
                LaggedStart(*[FadeIn(cell, scale=0.8) for cell in dp_cells], lag_ratio=0.003),
                run_time=tracker.duration
            )
        # Narration: "But the principle is the same: current state plus best future."
        # Visual: Show the Bellman equation again: 'Value(month, inventory) = cost + Value(next_month, next_inventory)'.
        with self.voiceover(text="But the principle is the same: current state plus best future.") as tracker:
            # Fade cells to background
            self.play(dp_cells.animate.set_opacity(0.2), run_time=0.5)
            # Show Bellman equation
            bellman_eq = MathTex(
                r"V(m, i) = \min \Big\{ \text{cost} + V(m+1, i') \Big\}",
                font_size=36,
                color=YELLOW
            )
            bellman_eq.to_edge(UP, buff=0.8)
            explanation = VGroup(
                MathTex(r"m = \text{month}", font_size=28, color=WHITE),
                MathTex(r"i = \text{inventory}", font_size=28, color=WHITE),
                MathTex(r"i' = \text{next inventory}", font_size=28, color=WHITE)
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
            explanation.next_to(bellman_eq, DOWN, buff=0.5)
            self.play(
                Write(bellman_eq, lag_ratio=0.1),
                run_time=tracker.duration * 0.6
            )
            self.play(
                FadeIn(explanation, shift=DOWN*0.3, lag_ratio=0.2),
                run_time=tracker.duration * 0.4
            )
            self.play(Indicate(bellman_eq, color=YELLOW, scale_factor=1.1), run_time=1.0)
        # Narration: "State can have as many dimensions as your problem needs."
        # Visual: Show the 2D grid transforming into a 3D cube, then a 4D hypercube (projected). Text: 'State space grows with complexity'.
        with self.voiceover(text="State can have as many dimensions as your problem needs.") as tracker:
            # Fade out equation
            self.play(
                FadeOut(bellman_eq),
                FadeOut(explanation),
                run_time=0.4
            )
            # Highlight 2D grid
            dim_2d_label = Text("2D: (month, inventory)", font_size=32, color=BLUE)
            dim_2d_label.to_edge(UP, buff=0.5)
            self.play(
                dp_cells.animate.set_opacity(0.6),
                Write(dim_2d_label),
                run_time=tracker.duration * 0.2
            )
            # Transform to 3D representation
            self.play(FadeOut(dp_cells), run_time=0.3)
            # Create 3D cube representation (isometric projection)
            cube_3d = VGroup()
            for x in range(5):
                for y in range(5):
                    for z in range(5):
                        if x == 0 or y == 0 or z == 0 or x == 4 or y == 4 or z == 4:
                            # Isometric projection
                            iso_x = (x - z) * 0.3
                            iso_y = (x + z) * 0.15 + y * 0.3
                            dot = Dot(point=np.array([iso_x, iso_y, 0]), radius=0.03, color=GREEN)
                            dot.set_opacity(0.6)
                            cube_3d.add(dot)
            cube_3d.move_to(ORIGIN)
            dim_3d_label = Text("3D: (month, inventory, location)", font_size=32, color=GREEN)
            dim_3d_label.to_edge(UP, buff=0.5)
            self.play(
                ReplacementTransform(dim_2d_label, dim_3d_label),
                LaggedStart(*[GrowFromCenter(d) for d in cube_3d], lag_ratio=0.005),
                run_time=tracker.duration * 0.3
            )
            # Transform to 4D hypercube (projected)
            hypercube_4d = VGroup()
            for i in range(80):
                angle = i * TAU / 80
                radius = 2 + 0.5 * np.sin(4 * angle)
                x = radius * np.cos(angle)
                y = radius * np.sin(angle)
                dot = Dot(point=np.array([x, y, 0]), radius=0.025, color=PURPLE)
                dot.set_opacity(0.7)
                hypercube_4d.add(dot)
            dim_4d_label = Text("4D+: State space grows...", font_size=32, color=PURPLE)
            dim_4d_label.to_edge(UP, buff=0.5)
            self.play(
                ReplacementTransform(dim_3d_label, dim_4d_label),
                ReplacementTransform(cube_3d, hypercube_4d),
                run_time=tracker.duration * 0.3
            )
            # Final message
            complexity_text = Text("State space grows with complexity", font_size=36, color=RED)
            complexity_text.next_to(hypercube_4d, DOWN, buff=0.8)
            self.play(
                Write(complexity_text, lag_ratio=0.1),
                hypercube_4d.animate.scale(1.2).set_opacity(0.9),
                run_time=tracker.duration * 0.2
            )
            self.play(Indicate(complexity_text, color=YELLOW, scale_factor=1.15), run_time=1.0)
        self.wait(2)


        # ==========================================================
        # SCENE 12: The Art of Abstraction
        # ==========================================================
        # Clear the stage
        if self.mobjects:
            self.play(*[FadeOut(obj) for obj in self.mobjects], run_time=0.5)
        # Narration: "So what's the real lesson here?"
        # Visual: Fade out all previous visuals. Show a blank screen with a single question mark.
        with self.voiceover(text="So what's the real lesson here?") as tracker:
            question_mark = MathTex(r"?", font_size=120, color=WHITE)
            self.play(
                FadeIn(question_mark, shift=DOWN*0.3, scale=1.5),
                run_time=tracker.duration
            )
            self.play(Indicate(question_mark, color=YELLOW, scale_factor=1.2), run_time=0.8)
        # Narration: "Dynamic programming isn't really about algorithms. It's about abstraction."
        # Visual: Display the word 'Abstraction' materializing from particles.
        with self.voiceover(text="Dynamic programming isn't really about algorithms. It's about abstraction.") as tracker:
            self.play(FadeOut(question_mark, shift=UP*0.3), run_time=0.4)
            # Create particle effect
            particles = VGroup(*[
                Dot(
                    ORIGIN + np.array([np.random.normal(0, 2.5), np.random.normal(0, 1.5), 0]),
                    radius=0.03,
                    color=BLUE
                ).set_opacity(0.8)
                for _ in range(150)
            ])
            abstraction_text = Text("Abstraction", font_size=72, color=BLUE, weight=BOLD)
            self.play(FadeIn(particles, lag_ratio=0.005), run_time=0.8)
            self.play(
                Transform(particles, abstraction_text),
                run_time=tracker.duration - 0.8,
                rate_func=smooth
            )
            self.play(Flash(abstraction_text.get_center(), color=BLUE, flash_radius=1.5), run_time=0.5)
        # Narration: "The art is choosing what to remember and what to forget."
        # Visual: Show a timeline with a glowing window. Text: 'Remember: current state. Forget: how you got here'.
        with self.voiceover(text="The art is choosing what to remember and what to forget.") as tracker:
            self.play(FadeOut(particles, shift=UP*0.5), run_time=0.5)
            # Create timeline
            timeline = Line(LEFT*5, RIGHT*5, color=GRAY).shift(UP*0.5)
            time_dots = VGroup(*[Dot(timeline.point_from_proportion(i/10), color=GRAY) for i in range(11)])
            # Glowing window
            window = Rectangle(width=1.5, height=1.2, color=YELLOW, stroke_width=4)
            window.move_to(timeline.point_from_proportion(0.6) + DOWN*0.1)
            window.set_fill(YELLOW, opacity=0.2)
            remember_text = Text("Remember: current state", font_size=28, color=GREEN).next_to(window, DOWN, buff=0.5)
            forget_text = Text("Forget: how you got here", font_size=28, color=RED).next_to(remember_text, DOWN, buff=0.3)
            self.play(
                Create(timeline),
                LaggedStart(*[GrowFromCenter(dot) for dot in time_dots], lag_ratio=0.1),
                run_time=1.2
            )
            self.play(
                DrawBorderThenFill(window),
                run_time=tracker.duration - 2.0
            )
            self.play(
                Write(remember_text, lag_ratio=0.05),
                Write(forget_text, lag_ratio=0.05),
                run_time=0.8
            )
        # Narration: "Too little information, and you can't make decisions."
        # Visual: Show a character at a fork with no context. Text: 'Underspecified: can't decide'.
        with self.voiceover(text="Too little information, and you can't make decisions.") as tracker:
            self.play(
                *[FadeOut(obj, shift=LEFT*0.5) for obj in [timeline, time_dots, window, remember_text, forget_text]],
                run_time=0.5
            )
            # Create fork in the road
            fork_base = Line(DOWN*1.5, ORIGIN, color=WHITE, stroke_width=8)
            fork_left = Line(ORIGIN, UP*1.2 + LEFT*1.5, color=WHITE, stroke_width=8)
            fork_right = Line(ORIGIN, UP*1.2 + RIGHT*1.5, color=WHITE, stroke_width=8)
            fork = VGroup(fork_base, fork_left, fork_right).shift(LEFT*2)
            # Character (simple circle with question mark)
            character = VGroup(
                Circle(radius=0.3, color=BLUE, fill_opacity=0.8),
                MathTex(r"?", font_size=36, color=WHITE)
            ).move_to(fork_base.get_start())
            underspec_text = Text("Underspecified: can't decide", font_size=32, color=RED).to_edge(DOWN, buff=1)
            self.play(
                Create(fork, lag_ratio=0.3),
                FadeIn(character, shift=DOWN*0.3),
                run_time=tracker.duration - 1.0
            )
            self.play(Write(underspec_text, lag_ratio=0.05), run_time=0.8)
            self.play(Indicate(character, color=RED, scale_factor=1.3), run_time=0.5)
        # Narration: "Too much information, and computation explodes."
        # Visual: Show a character drowning in data. Text: 'Overspecified: too slow'.
        with self.voiceover(text="Too much information, and computation explodes.") as tracker:
            self.play(
                *[FadeOut(obj) for obj in [fork, character, underspec_text]],
                run_time=0.4
            )
            # Character drowning
            drowning_char = Circle(radius=0.3, color=BLUE, fill_opacity=0.8)
            # Data flood
            data_items = VGroup(*[
                MathTex(str(np.random.randint(0, 100)), font_size=24, color=RED)
                .move_to(np.array([np.random.uniform(-3, 3), np.random.uniform(1, 4), 0]))
                for _ in range(60)
            ])
            overspec_text = Text("Overspecified: too slow", font_size=32, color=RED).to_edge(DOWN, buff=1)
            self.play(FadeIn(drowning_char, shift=UP*0.3), run_time=0.5)
            self.play(
                LaggedStart(*[FadeIn(item, shift=DOWN*0.5) for item in data_items], lag_ratio=0.01),
                drowning_char.animate.set_opacity(0.3).scale(0.7),
                run_time=tracker.duration - 1.2
            )
            self.play(Write(overspec_text, lag_ratio=0.05), run_time=0.7)
        # Narration: "The perfect state is the minimal information that captures all constraints."
        # Visual: Show a glowing balance scale: 'Information' on one side, 'Efficiency' on the other, perfectly balanced.
        with self.voiceover(text="The perfect state is the minimal information that captures all constraints.") as tracker:
            self.play(
                *[FadeOut(obj) for obj in [drowning_char, data_items, overspec_text]],
                run_time=0.5
            )
            # Balance scale
            fulcrum = Triangle(color=GRAY, fill_opacity=1).scale(0.4).rotate(PI)
            beam = Rectangle(width=5, height=0.15, color=WHITE, fill_opacity=1).next_to(fulcrum, UP, buff=0)
            left_plate = Line(UP*0.3, DOWN*0.3, color=WHITE, stroke_width=3).move_to(beam.get_left() + UP*0.5)
            right_plate = Line(UP*0.3, DOWN*0.3, color=WHITE, stroke_width=3).move_to(beam.get_right() + UP*0.5)
            left_chain = Line(beam.get_left(), left_plate.get_top(), color=WHITE, stroke_width=2)
            right_chain = Line(beam.get_right(), right_plate.get_top(), color=WHITE, stroke_width=2)
            scale = VGroup(fulcrum, beam, left_plate, right_plate, left_chain, right_chain)
            info_text = Text("Information", font_size=28, color=BLUE).next_to(left_plate, DOWN, buff=0.5)
            efficiency_text = Text("Efficiency", font_size=28, color=GREEN).next_to(right_plate, DOWN, buff=0.5)
            self.play(
                DrawBorderThenFill(scale),
                run_time=1.0
            )
            self.play(
                Write(info_text, lag_ratio=0.05),
                Write(efficiency_text, lag_ratio=0.05),
                run_time=tracker.duration - 1.5
            )
            self.play(
                scale.animate.set_color(GOLD),
                Flash(fulcrum.get_top(), color=GOLD, flash_radius=1.0),
                run_time=0.5
            )
        # Narration: "In the job problem, we only needed to know last week's choice."
        # Visual: Show the job timeline with just one week highlighted. Text: 'State: last action'.
        with self.voiceover(text="In the job problem, we only needed to know last week's choice.") as tracker:
            self.play(
                *[FadeOut(obj) for obj in [scale, info_text, efficiency_text]],
                run_time=0.4
            )
            # Job timeline
            weeks = VGroup(*[
                Rectangle(width=0.8, height=0.6, color=GRAY, stroke_width=2)
                for _ in range(6)
            ]).arrange(RIGHT, buff=0.3).shift(UP*0.5)
            week_labels = VGroup(*[
                Text(f"W{i+1}", font_size=20, color=WHITE).move_to(weeks[i])
                for i in range(6)
            ])
            # Highlight last week
            highlight = weeks[4].copy().set_stroke(YELLOW, width=5).set_fill(YELLOW, opacity=0.3)
            state_text = Text("State: last action", font_size=32, color=YELLOW).next_to(weeks, DOWN, buff=0.8)
            self.play(
                LaggedStart(*[Create(week) for week in weeks], lag_ratio=0.1),
                LaggedStart(*[Write(label) for label in week_labels], lag_ratio=0.1),
                run_time=1.2
            )
            self.play(
                Create(highlight),
                run_time=tracker.duration - 1.8
            )
            self.play(Write(state_text, lag_ratio=0.05), run_time=0.6)
        # Narration: "In the location problem, we needed to know where we are."
        # Visual: Show the two cities with one glowing. Text: 'State: current location'.
        with self.voiceover(text="In the location problem, we needed to know where we are.") as tracker:
            self.play(
                *[FadeOut(obj) for obj in [weeks, week_labels, highlight, state_text]],
                run_time=0.4
            )
            # Two cities
            city_a = VGroup(
                Circle(radius=0.5, color=BLUE, fill_opacity=0.5),
                Text("A", font_size=36, color=WHITE)
            ).shift(LEFT*2.5)
            city_b = VGroup(
                Circle(radius=0.5, color=GRAY, fill_opacity=0.3),
                Text("B", font_size=36, color=WHITE)
            ).shift(RIGHT*2.5)
            road = Line(city_a.get_right(), city_b.get_left(), color=GRAY, stroke_width=3)
            location_text = Text("State: current location", font_size=32, color=BLUE).to_edge(DOWN, buff=1)
            self.play(
                FadeIn(city_a, shift=RIGHT*0.3),
                FadeIn(city_b, shift=LEFT*0.3),
                Create(road),
                run_time=1.0
            )
            self.play(
                city_a[0].animate.set_fill(BLUE, opacity=0.8).set_stroke(YELLOW, width=4),
                Flash(city_a.get_center(), color=YELLOW, flash_radius=0.8),
                run_time=tracker.duration - 1.5
            )
            self.play(Write(location_text, lag_ratio=0.05), run_time=0.5)
        # Narration: "In the inventory problem, we needed to know how much we're holding."
        # Visual: Show the warehouse. Text: 'State: current inventory'.
        with self.voiceover(text="In the inventory problem, we needed to know how much we're holding.") as tracker:
            self.play(
                *[FadeOut(obj) for obj in [city_a, city_b, road, location_text]],
                run_time=0.4
            )
            # Warehouse
            warehouse = Rectangle(width=3, height=2, color=GRAY, stroke_width=4).shift(UP*0.3)
            roof = Polygon(
                warehouse.get_corner(UP+LEFT),
                warehouse.get_corner(UP+RIGHT),
                warehouse.get_top() + UP*0.5,
                color=GRAY,
                stroke_width=4,
                fill_opacity=0.3
            )
            # Boxes inside
            boxes = VGroup(*[
                Square(side_length=0.3, color=ORANGE, fill_opacity=0.7, stroke_width=2)
                for _ in range(8)
            ]).arrange_in_grid(rows=2, cols=4, buff=0.15).move_to(warehouse)
            inventory_text = Text("State: current inventory", font_size=32, color=ORANGE).next_to(warehouse, DOWN, buff=0.8)
            self.play(
                Create(warehouse),
                Create(roof),
                run_time=0.8
            )
            self.play(
                LaggedStart(*[FadeIn(box, shift=DOWN*0.2) for box in boxes], lag_ratio=0.08),
                run_time=tracker.duration - 1.3
            )
            self.play(Write(inventory_text, lag_ratio=0.05), run_time=0.5)
        # Narration: "Every hard problem has a state space hiding inside it."
        # Visual: Show three different problems morphing into their state diagrams.
        with self.voiceover(text="Every hard problem has a state space hiding inside it.") as tracker:
            self.play(
                *[FadeOut(obj) for obj in [warehouse, roof, boxes, inventory_text]],
                run_time=0.4
            )
            # Three problem icons
            problem1 = VGroup(
                Square(side_length=0.8, color=BLUE, fill_opacity=0.5),
                Text("Job", font_size=20, color=WHITE)
            ).shift(LEFT*3 + UP*1)
            problem2 = VGroup(
                Circle(radius=0.4, color=GREEN, fill_opacity=0.5),
                Text("Location", font_size=18, color=WHITE)
            ).shift(ORIGIN + UP*1)
            problem3 = VGroup(
                Triangle(color=ORANGE, fill_opacity=0.5).scale(0.6),
                Text("Inventory", font_size=18, color=WHITE).shift(DOWN*0.15)
            ).shift(RIGHT*3 + UP*1)
            # State diagrams (simplified)
            state1 = VGroup(*[
                Dot(LEFT*3 + DOWN*0.5 + RIGHT*i*0.6, color=BLUE, radius=0.1)
                for i in range(4)
            ])
            arrows1 = VGroup(*[
                Arrow(state1[i].get_center(), state1[i+1].get_center(), buff=0.1, color=BLUE, stroke_width=2, max_tip_length_to_length_ratio=0.15)
                for i in range(3)
            ])
            state2 = VGroup(
                Dot(ORIGIN + DOWN*0.8, color=GREEN, radius=0.1),
                Dot(LEFT*0.8 + DOWN*1.5, color=GREEN, radius=0.1),
                Dot(RIGHT*0.8 + DOWN*1.5, color=GREEN, radius=0.1)
            )
            arrows2 = VGroup(
                Arrow(state2[0].get_center(), state2[1].get_center(), buff=0.1, color=GREEN, stroke_width=2, max_tip_length_to_length_ratio=0.2),
                Arrow(state2[0].get_center(), state2[2].get_center(), buff=0.1, color=GREEN, stroke_width=2, max_tip_length_to_length_ratio=0.2)
            )
            state3 = VGroup(*[
                Dot(RIGHT*3 + DOWN*0.5 + UP*i*0.5, color=ORANGE, radius=0.1)
                for i in range(3)
            ])
            arrows3 = VGroup(*[
                Arrow(state3[i].get_center(), state3[i+1].get_center(), buff=0.1, color=ORANGE, stroke_width=2, max_tip_length_to_length_ratio=0.2)
                for i in range(2)
            ])
            self.play(
                LaggedStart(
                    FadeIn(problem1, shift=DOWN*0.3),
                    FadeIn(problem2, shift=DOWN*0.3),
                    FadeIn(problem3, shift=DOWN*0.3),
                    lag_ratio=0.2
                ),
                run_time=1.2
            )
            self.play(
                ReplacementTransform(problem1.copy(), VGroup(state1, arrows1)),
                ReplacementTransform(problem2.copy(), VGroup(state2, arrows2)),
                ReplacementTransform(problem3.copy(), VGroup(state3, arrows3)),
                run_time=tracker.duration - 1.2,
                rate_func=smooth
            )
        # Narration: "Finding it is the creative act. The algorithm is just bookkeeping."
        # Visual: Show a lightbulb (insight) transforming into a table (execution).
        with self.voiceover(text="Finding it is the creative act. The algorithm is just bookkeeping.") as tracker:
            self.play(
                *[FadeOut(obj) for obj in [problem1, problem2, problem3, state1, arrows1, state2, arrows2, state3, arrows3]],
                run_time=0.5
            )
            # Lightbulb (insight)
            bulb_circle = Circle(radius=0.5, color=YELLOW, fill_opacity=0.8).shift(UP*0.3)
            bulb_base = Rectangle(width=0.3, height=0.4, color=GRAY, fill_opacity=0.8).next_to(bulb_circle, DOWN, buff=0)
            lightbulb = VGroup(bulb_circle, bulb_base)
            insight_text = Text("Insight", font_size=28, color=YELLOW).next_to(lightbulb, DOWN, buff=0.5)
            # DP Table
            table = VGroup()
            for i in range(3):
                row = VGroup(*[
                    Square(side_length=0.5, color=WHITE, stroke_width=2, fill_opacity=0.1)
                    for _ in range(4)
                ]).arrange(RIGHT, buff=0.1)
                table.add(row)
            table.arrange(DOWN, buff=0.1)
            execution_text = Text("Execution", font_size=28, color=BLUE).next_to(table, DOWN, buff=0.5)
            self.play(
                GrowFromCenter(lightbulb),
                FadeIn(insight_text, shift=UP*0.2),
                run_time=1.2
            )
            self.play(Flash(bulb_circle.get_center(), color=YELLOW, flash_radius=1.0), run_time=0.5)
            self.play(
                ReplacementTransform(lightbulb, table),
                ReplacementTransform(insight_text, execution_text),
                run_time=tracker.duration - 1.7,
                rate_func=smooth
            )
        # Narration: "So next time you face an optimization problem, ask yourself:"
        # Visual: Display the question: 'What is the minimal state that captures my constraints?'
        with self.voiceover(text="So next time you face an optimization problem, ask yourself:") as tracker:
            self.play(
                FadeOut(table, shift=UP*0.5),
                FadeOut(execution_text, shift=UP*0.5),
                run_time=0.5
            )
            question = Text(
                "What is the minimal state\nthat captures my constraints?",
                font_size=36,
                color=YELLOW,
                line_spacing=1.2
            )
            question_box = SurroundingRectangle(question, color=YELLOW, buff=0.3, stroke_width=3)
            question_group = VGroup(question_box, question)
            self.play(
                Write(question, lag_ratio=0.02),
                run_time=tracker.duration - 0.8
            )
            self.play(Create(question_box), run_time=0.8)
        # Narration: "Answer that, and the solution often builds itself."
        # Visual: Show a DP table materializing and filling automatically. Text: 'The rest is just math'.
        with self.voiceover(text="Answer that, and the solution often builds itself.") as tracker:
            self.play(question_group.animate.scale(0.7).to_edge(UP, buff=0.5), run_time=0.6)
            # DP table that fills automatically
            dp_table = VGroup()
            for i in range(4):
                row = VGroup(*[
                    Square(side_length=0.6, color=BLUE, stroke_width=2, fill_opacity=0)
                    for _ in range(5)
                ]).arrange(RIGHT, buff=0.1)
                dp_table.add(row)
            dp_table.arrange(DOWN, buff=0.1).shift(DOWN*0.3)
            # Values that will fill the table
            values = VGroup()
            for i in range(4):
                for j in range(5):
                    val = MathTex(str(np.random.randint(1, 20)), font_size=24, color=GREEN)
                    val.move_to(dp_table[i][j])
                    values.add(val)
            math_text = Text("The rest is just math", font_size=32, color=GREEN).to_edge(DOWN, buff=0.8)
            self.play(
                LaggedStart(*[Create(cell) for row in dp_table for cell in row], lag_ratio=0.02),
                run_time=1.5
            )
            # Fill table row by row
            fill_anims = []
            for i, val in enumerate(values):
                fill_anims.append(FadeIn(val, scale=0.5))
            self.play(
                LaggedStart(*fill_anims, lag_ratio=0.03),
                run_time=tracker.duration - 2.5
            )
            self.play(Write(math_text, lag_ratio=0.05), run_time=0.8)
        # Narration: "Because the future isn't chaos. It's just today's choice plus tomorrow's best outcome."
        # Visual: Show the Bellman equation one final time, glowing: 'V(s,t) = reward + V(s',t+1)'. Fade to black.
        with self.voiceover(text="Because the future isn't chaos. It's just today's choice plus tomorrow's best outcome.") as tracker:
            self.play(
                *[FadeOut(obj) for obj in [question_group, dp_table, values, math_text]],
                run_time=0.6
            )
            # Bellman equation
            bellman = MathTex(
                r"V(s,t)", r"=", r"\text{reward}", r"+", r"V(s',t+1)",
                font_size=60,
                color=WHITE
            )
            bellman[0].set_color(BLUE)
            bellman[2].set_color(GREEN)
            bellman[4].set_color(PURPLE)
            self.play(
                Write(bellman, lag_ratio=0.1),
                run_time=tracker.duration - 1.5
            )
            self.play(
                bellman.animate.set_color(GOLD),
                Flash(bellman.get_center(), color=GOLD, flash_radius=2.0, line_length=0.3),
                run_time=1.0
            )
            self.play(
                bellman.animate.scale(1.2),
                run_time=0.5
            )
            self.play(
                FadeOut(bellman, scale=1.5),
                run_time=1.0
            )
        self.wait(2)

