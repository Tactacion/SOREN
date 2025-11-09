from manim import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.elevenlabs import ElevenLabsService
import numpy as np
import os
import math

ZONES = {
    'title': np.array([0, 3.2, 0]),
    'top': np.array([0, 2, 0]),
    'top_left': np.array([-4, 2, 0]),
    'top_center': np.array([0, 2, 0]),
    'top_right': np.array([4, 2, 0]),
    'left': np.array([-4, 0, 0]),
    'center': np.array([0, 0, 0]),
    'right': np.array([4, 0, 0]),
    'bottom': np.array([0, -2.5, 0]),
    'bottom_left': np.array([-4, -2.5, 0]),
    'bottom_center': np.array([0, -2.5, 0]),
    'bottom_right': np.array([4, -2.5, 0])
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
BLACK = "#000000"

class Video1(VoiceoverScene):
    def construct(self):
        self.set_speech_service(
            ElevenLabsService(
                api_key=os.getenv("ELEVENLABS_API_KEY"),
                voice_id="21m00Tcm4TUPJeGCAgmA"
            )
        )
        self.camera.background_color = "#000000"

        # ==========================================================
        # SCENE 1
        # ==========================================================
        # Scene 1: The Limitation of Pairs
        
        if self.mobjects:
            self.play(*[FadeOut(obj) for obj in self.mobjects], run_time=0.5)
        
        with self.voiceover(text="""Imagine you're trying to transform one image into another—perhaps editing a photo based on a text description. Classical Schrödinger bridges handle this beautifully for two distributions, creating an optimal transport plan between them. But here's the problem: modern AI doesn't work with just pairs. When you have an input image, a text instruction, AND a desired output, you're dealing with three probability distributions simultaneously. The traditional two-marginal framework simply breaks down, leaving us unable to model these crucial three-way relationships.""") as tracker:
            
            # Create left distribution cloud (BLUE)
            center_point = ZONES['left']
            cloud_left = VGroup(*[
                Dot(radius=0.04, color=BLUE, fill_opacity=0.7).move_to(
                    center_point + np.array([
                        np.random.normal(0, 1.2/3), 
                        np.random.normal(0, 1.2/3), 
                        0
                    ])
                ) for _ in range(50)
            ])
            self.play(LaggedStart(*[FadeIn(dot, scale=0.5) for dot in cloud_left], lag_ratio=0.02), run_time=2)
            
            # Create right distribution cloud (RED)
            center_point = ZONES['right']
            cloud_right = VGroup(*[
                Dot(radius=0.04, color=RED, fill_opacity=0.7).move_to(
                    center_point + np.array([
                        np.random.normal(0, 1.2/3), 
                        np.random.normal(0, 1.2/3), 
                        0
                    ])
                ) for _ in range(50)
            ])
            self.play(LaggedStart(*[FadeIn(dot, scale=0.5) for dot in cloud_right], lag_ratio=0.02), run_time=2)
            
            # Create flowing particles from left to right (ORANGE)
            start_pos = ZONES['left']
            end_pos = ZONES['right']
            particles = VGroup(*[
                Dot(radius=0.05, color=ORANGE).move_to(
                    start_pos + np.array([np.random.uniform(-0.3, 0.3), np.random.uniform(-0.3, 0.3), 0])
                ) for _ in range(20)
            ])
            self.play(LaggedStart(*[FadeIn(p, scale=0.3) for p in particles], lag_ratio=0.05), run_time=1.5)
            
            # Animate flow to destination
            animations = []
            for particle in particles:
                target = end_pos + np.array([np.random.uniform(-0.3, 0.3), np.random.uniform(-0.3, 0.3), 0])
                animations.append(particle.animate.move_to(target))
            self.play(*animations, run_time=2.5, rate_func=smooth)
            
            # Wait
            self.wait(1.5)
            
            # Create top center distribution cloud (GREEN)
            center_point = ZONES['top_center']
            cloud_top = VGroup(*[
                Dot(radius=0.04, color=GREEN, fill_opacity=0.7).move_to(
                    center_point + np.array([
                        np.random.normal(0, 1.0/3), 
                        np.random.normal(0, 1.0/3), 
                        0
                    ])
                ) for _ in range(50)
            ])
            self.play(LaggedStart(*[FadeIn(dot, scale=0.5) for dot in cloud_top], lag_ratio=0.02), run_time=2)
            
            # Create math equation
            math = MathTex("N \\geq 3\\text{ ?}", font_size=66, color=YELLOW)
            math.move_to(ZONES['center'])
            
            # Indicate the math
            self.play(Indicate(math, color=GOLD, scale_factor=1.3), run_time=1.5)
            
            # Create cross mark
            cross = MathTex("\\times", font_size=88, color=RED)
            cross.move_to(ZONES['center'])
            
            # Fade in the cross
            self.play(FadeIn(cross), run_time=1.0)
            
            self.wait(0.5)

        # ==========================================================
        # SCENE 2
        # ==========================================================
        # Scene 2: The Multimodal Challenge
        
        if self.mobjects:
            self.play(*[FadeOut(obj) for obj in self.mobjects], run_time=0.5)
        
        with self.voiceover(text="""Let's visualize what we're really asking for. In text-guided image generation, we need to simultaneously respect three constraints: the source image distribution, the text instruction distribution, and the target image distribution. These aren't independent—they're deeply interconnected. The challenge is finding a joint probability distribution that matches all three marginals while maintaining some notion of optimality. This is the multi-marginal problem, and it's fundamentally different from just chaining together pairwise bridges.""") as tracker:
            
            # Create network structure
            import math
            num_nodes = 3
            radius = 1.8
            nodes = VGroup(*[
                Circle(radius=0.25, color=PURPLE, fill_opacity=0.6, stroke_width=2).move_to(
                    ZONES['center'] + np.array([
                        radius * math.cos(i * 2 * math.pi / num_nodes),
                        radius * math.sin(i * 2 * math.pi / num_nodes),
                        0
                    ])
                ) for i in range(num_nodes)
            ])
            self.play(LaggedStart(*[FadeIn(node, scale=0.3) for node in nodes], lag_ratio=0.15), run_time=2)
            
            # Connect with edges
            edges = VGroup()
            for i in range(num_nodes):
                for j in range(i + 1, num_nodes):
                    if np.random.random() < 0.4:
                        edge = Line(
                            nodes[i].get_center(), 
                            nodes[j].get_center(), 
                            color=PURPLE, 
                            stroke_width=1.5, 
                            stroke_opacity=0.4
                        )
                        edges.add(edge)
            self.play(LaggedStart(*[Create(edge) for edge in edges], lag_ratio=0.05), run_time=2)
            
            # Create labels
            text_image = Text("Image", font_size=32, color=BLUE)
            text_image.move_to(ZONES['bottom_left'])
            
            text_text = Text("Text", font_size=32, color=GREEN)
            text_text.move_to(ZONES['top_center'])
            
            text_output = Text("Output", font_size=32, color=RED)
            text_output.move_to(ZONES['bottom_right'])
            
            self.wait(1.0)
            
            # Create distribution clouds
            center_point_bl = ZONES['bottom_left']
            cloud_bl = VGroup(*[
                Dot(radius=0.04, color=BLUE, fill_opacity=0.7).move_to(
                    center_point_bl + np.array([
                        np.random.normal(0, 0.8/3), 
                        np.random.normal(0, 0.8/3), 
                        0
                    ])
                ) for _ in range(50)
            ])
            
            center_point_tc = ZONES['top_center']
            cloud_tc = VGroup(*[
                Dot(radius=0.04, color=GREEN, fill_opacity=0.7).move_to(
                    center_point_tc + np.array([
                        np.random.normal(0, 0.8/3), 
                        np.random.normal(0, 0.8/3), 
                        0
                    ])
                ) for _ in range(50)
            ])
            
            center_point_br = ZONES['bottom_right']
            cloud_br = VGroup(*[
                Dot(radius=0.04, color=RED, fill_opacity=0.7).move_to(
                    center_point_br + np.array([
                        np.random.normal(0, 0.8/3), 
                        np.random.normal(0, 0.8/3), 
                        0
                    ])
                ) for _ in range(50)
            ])
            
            clouds = VGroup(cloud_bl, cloud_tc, cloud_br)
            self.play(LaggedStart(*[FadeIn(obj) for obj in clouds], lag_ratio=0.3), run_time=2.0)
            
            # Create joint distribution equation
            math = MathTex(r"\pi^*(x_1, x_2, x_3)", font_size=53, color=GOLD)
            math.move_to(ZONES['center'])
            self.play(Write(math), run_time=1.5)
            
            # Circumscribe the equation
            self.play(Circumscribe(math, color=YELLOW, run_time=1.5))
            
            self.wait(0.5)

        # ==========================================================
        # SCENE 3
        # ==========================================================
        # Scene 3: F-Divergence: The Flexibility Key
        
        if self.mobjects:
            self.play(*[FadeOut(obj) for obj in self.mobjects], run_time=0.5)
        
        with self.voiceover(text="""At the heart of measuring differences between distributions lies f-divergence, parameterized by a convex function f. This isn't just one distance measure—it's an entire family. When f equals x log x, you get KL-divergence with its mode-seeking behavior. Different choices of f emphasize different aspects of distribution mismatch. This flexibility becomes crucial when we extend to multiple marginals, because different applications need different notions of 'closeness.' The beauty is that all these divergences share a common mathematical structure we can exploit.""") as tracker:
            
            # CREATE MathTex at top center
            math = MathTex(r"D_f(P||Q) = \int q(x) f\left(\frac{p(x)}{q(x)}\right)dx", font_size=40, color=WHITE)
            math.move_to(ZONES['top_center'])
            self.play(Write(math), run_time=1.5)
            
            self.wait(1.0)
            
            # 3D_SURFACE wave BLUE
            surface = VGroup()
            for i in range(-4, 5):
                for j in range(-3, 4):
                    # Calculate "height" for wave pattern
                    height_factor = 0.5 + 0.5 * np.sin(i * 0.5) * np.cos(j * 0.5)
                    opacity = 0.2 + 0.5 * height_factor
                    
                    sq = Square(side_length=0.35, color=BLUE, fill_opacity=opacity, stroke_width=0.5)
                    # Add perspective shift
                    sq.move_to(ZONES['center'] + np.array([i * 0.45, j * 0.4 + height_factor * 0.3, 0]))
                    surface.add(sq)
            
            self.play(LaggedStart(*[FadeIn(sq, shift=UP*0.1) for sq in surface], lag_ratio=0.01), run_time=2.5)
            
            # CREATE Text for KL-divergence
            text1 = Text("f(x) = x log x", font_size=31, color=ORANGE)
            text1.move_to(ZONES['bottom_left'])
            self.play(FadeIn(text1), run_time=0.8)
            
            text2 = Text("(KL-divergence)", font_size=26, color=ORANGE)
            text2.move_to(ZONES['bottom_left'] + np.array([0, -0.4, 0]))
            self.play(FadeIn(text2), run_time=0.8)
            
            self.wait(1.5)
            
            # MORPH wave to mountain PURPLE
            surface2 = VGroup()
            for i in range(-4, 5):
                for j in range(-3, 4):
                    # Calculate "height" for mountain pattern
                    import math
                    distance = math.sqrt(i**2 + j**2)
                    height_factor = max(0, 1 - distance / 5)
                    opacity = 0.2 + 0.5 * height_factor
                    
                    sq = Square(side_length=0.35, color=PURPLE, fill_opacity=opacity, stroke_width=0.5)
                    # Add perspective shift
                    sq.move_to(ZONES['center'] + np.array([i * 0.45, j * 0.4 + height_factor * 0.4, 0]))
                    surface2.add(sq)
            
            self.play(Transform(surface, surface2), run_time=2.5, rate_func=smooth)
            
            # CREATE Text for Total Variation
            text3 = Text("f(x) = |x-1|", font_size=31, color=GREEN)
            text3.move_to(ZONES['bottom_right'])
            self.play(FadeIn(text3), run_time=0.8)
            
            text4 = Text("(Total Variation)", font_size=26, color=GREEN)
            text4.move_to(ZONES['bottom_right'] + np.array([0, -0.4, 0]))
            self.play(FadeIn(text4), run_time=0.8)
            
            # ANIMATE Indicate surface
            self.play(Indicate(surface, color=GOLD, scale_factor=1.1), run_time=2.0)
            
            self.wait(0.5)

        # ==========================================================
        # SCENE 4
        # ==========================================================
        # Scene 4: Static vs Dynamic: A Profound Equivalence
        
        if self.mobjects:
            self.play(*[FadeOut(obj) for obj in self.mobjects], run_time=0.5)
        
        with self.voiceover(text="""Here's a stunning theoretical result that changes everything. You might think modeling full stochastic trajectories over time—the dynamic formulation—would give you more power than just modeling endpoint couplings—the static formulation. But they're equivalent! For ANY f-divergence, not just KL, the dynamic bridge can be constructed by sampling endpoints from the static solution and connecting them with Brownian bridges. This means we can work in the computationally simpler static setting without losing expressiveness. It's like discovering that a complex path integral reduces to a simple boundary value problem.""") as tracker:
            
            # Create title texts
            dynamic_text = Text("Dynamic Bridge", font_size=36, color=BLUE)
            dynamic_text.move_to(ZONES['top_left'])
            
            static_text = Text("Static Bridge", font_size=36, color=RED)
            static_text.move_to(ZONES['top_right'])
            
            self.play(FadeIn(dynamic_text), FadeIn(static_text), run_time=0.8)
            
            # Create flowing particles from left to right
            start_pos = ZONES['left']
            end_pos = ZONES['right']
            particles = VGroup(*[
                Dot(radius=0.05, color=BLUE).move_to(
                    start_pos + np.array([np.random.uniform(-0.3, 0.3), np.random.uniform(-0.3, 0.3), 0])
                ) for _ in range(15)
            ])
            self.play(LaggedStart(*[FadeIn(p, scale=0.3) for p in particles], lag_ratio=0.05), run_time=1.5)
            
            # Animate flow to destination
            animations = []
            for particle in particles:
                target = end_pos + np.array([np.random.uniform(-0.3, 0.3), np.random.uniform(-0.3, 0.3), 0])
                animations.append(particle.animate.move_to(target))
            self.play(*animations, run_time=2.5, rate_func=smooth)
            
            # Create left dots (dynamic)
            left_dots = VGroup(*[
                Dot(radius=0.1, color=BLUE).move_to(
                    ZONES['left'] + np.array([
                        np.random.uniform(-0.5, 0.5),
                        np.random.uniform(-0.5, 0.5),
                        0
                    ])
                ) for _ in range(8)
            ])
            
            # Create right dots (static)
            right_dots = VGroup(*[
                Dot(radius=0.1, color=RED).move_to(
                    ZONES['right'] + np.array([
                        np.random.uniform(-0.5, 0.5),
                        np.random.uniform(-0.5, 0.5),
                        0
                    ])
                ) for _ in range(8)
            ])
            
            self.play(FadeIn(left_dots), FadeIn(right_dots), run_time=1.0)
            
            # Transform left dots to right dots
            self.play(Transform(left_dots, right_dots), run_time=3.0)
            
            self.wait(1.0)
            
            # Create equivalence symbol
            equivalence = MathTex(r"\Leftrightarrow", font_size=96, color=GOLD)
            equivalence.move_to(ZONES['center'])
            
            # Animate FadeIn equivalence
            self.play(FadeIn(equivalence), run_time=1.0)
            
            # Build equation progressively
            equation = MathTex(r"\text{DSB} = \text{SSB} + \text{Brownian}", font_size=44, color=PURPLE)
            equation.move_to(ZONES['bottom_center'])
            self.play(Write(equation), run_time=3)
            self.play(Indicate(equation, color=GOLD, scale_factor=1.3), run_time=1)
            
            # Circumscribe the equation
            self.play(Circumscribe(equation, color=YELLOW, run_time=1.5))
            
            self.wait(0.5)

        # ==========================================================
        # SCENE 5
        # ==========================================================
        # Scene 5: The Primal Problem: Multi-Marginal SSB
        
        if self.mobjects:
            self.play(*[FadeOut(obj) for obj in self.mobjects], run_time=0.5)
        
        with self.voiceover(text="""Let's write down what we're actually optimizing. The Multi-marginal Static Schrödinger Bridge seeks a coupling π on the product space of all N distributions that matches every single marginal while minimizing f-divergence to a prior R. That prior R encodes our inductive biases—what we think a 'good' coupling should look like before seeing the marginal constraints. This is a constrained optimization problem: minimize divergence subject to N marginal matching constraints. The challenge is that this lives in a very high-dimensional space—the product of all the individual spaces.""") as tracker:
            
            # EQUATION_BUILD "\min_{\pi \in \Pi(\mu_1,...,\mu_N)} D_f(\pi || R)" top_center WHITE 4
            equation = MathTex(r"\min_{\pi \in \Pi(\mu_1,...,\mu_N)} D_f(\pi || R)", font_size=44, color=WHITE)
            equation.move_to(ZONES['top_center'])
            self.play(Write(equation), run_time=4)
            
            # WAIT 1.5
            self.wait(1.5)
            
            # NETWORK 5 BLUE
            import math
            num_nodes = 5
            radius = 1.8
            nodes = VGroup(*[
                Circle(radius=0.25, color=BLUE, fill_opacity=0.6, stroke_width=2).move_to(
                    ZONES['center'] + np.array([
                        radius * math.cos(i * 2 * math.pi / num_nodes),
                        radius * math.sin(i * 2 * math.pi / num_nodes),
                        0
                    ])
                ) for i in range(num_nodes)
            ])
            self.play(LaggedStart(*[FadeIn(node, scale=0.3) for node in nodes], lag_ratio=0.15), run_time=2)
            
            # Connect with edges
            edges = VGroup()
            for i in range(num_nodes):
                for j in range(i + 1, num_nodes):
                    if np.random.random() < 0.4:
                        edge = Line(
                            nodes[i].get_center(), 
                            nodes[j].get_center(), 
                            color=BLUE, 
                            stroke_width=1.5, 
                            stroke_opacity=0.4
                        )
                        edges.add(edge)
            self.play(LaggedStart(*[Create(edge) for edge in edges], lag_ratio=0.05), run_time=2)
            
            # CREATE Text "μ₁" at=center_left color=BLUE size=0.7
            text_mu1 = Text("μ₁", font_size=28, color=BLUE)
            text_mu1.move_to(nodes[0].get_center() + LEFT * 0.5)
            
            # CREATE Text "μ₂" at=top_center color=BLUE size=0.7
            text_mu2 = Text("μ₂", font_size=28, color=BLUE)
            text_mu2.move_to(nodes[1].get_center() + UP * 0.5)
            
            # CREATE Text "μ₃" at=center_right color=BLUE size=0.7
            text_mu3 = Text("μ₃", font_size=28, color=BLUE)
            text_mu3.move_to(nodes[2].get_center() + RIGHT * 0.5)
            
            # CREATE Text "μ₄" at=bottom_left color=BLUE size=0.7
            text_mu4 = Text("μ₄", font_size=28, color=BLUE)
            text_mu4.move_to(nodes[3].get_center() + DOWN * 0.5 + LEFT * 0.3)
            
            # CREATE Text "μ₅" at=bottom_right color=BLUE size=0.7
            text_mu5 = Text("μ₅", font_size=28, color=BLUE)
            text_mu5.move_to(nodes[4].get_center() + DOWN * 0.5 + RIGHT * 0.3)
            
            self.play(
                FadeIn(text_mu1),
                FadeIn(text_mu2),
                FadeIn(text_mu3),
                FadeIn(text_mu4),
                FadeIn(text_mu5),
                run_time=1
            )
            
            # WAIT 1.0
            self.wait(1.0)
            
            # Fade out network to make room for heatmap
            self.play(
                FadeOut(nodes),
                FadeOut(edges),
                FadeOut(text_mu1),
                FadeOut(text_mu2),
                FadeOut(text_mu3),
                FadeOut(text_mu4),
                FadeOut(text_mu5),
                run_time=0.8
            )
            
            # HEATMAP 8x8 BLUE_TO_RED
            grid_size = 8
            heatmap = VGroup()
            for i in range(grid_size):
                for j in range(grid_size):
                    # Calculate intensity
                    intensity = 0.3 + 0.7 * abs(math.sin((i + j) * 0.4))
                    
                    sq = Square(side_length=0.32, stroke_width=0.5, stroke_opacity=0.5)
                    # Color gradient from BLUE to RED
                    if intensity < 0.5:
                        sq.set_fill(BLUE, opacity=intensity * 1.5)
                    else:
                        sq.set_fill(RED, opacity=(intensity - 0.5) * 1.5)
                    
                    sq.move_to(ZONES['center'] + np.array([
                        (i - grid_size/2 + 0.5) * 0.37,
                        (j - grid_size/2 + 0.5) * 0.37,
                        0
                    ]))
                    heatmap.add(sq)
            
            self.play(LaggedStart(*[FadeIn(sq) for sq in heatmap], lag_ratio=0.01), run_time=2.5)
            
            # CREATE Text "Prior R" at=bottom_center color=GOLD size=0.8
            text_prior = Text("Prior R", font_size=32, color=GOLD)
            text_prior.move_to(ZONES['bottom_center'] + UP * 0.3)
            self.play(FadeIn(text_prior), run_time=0.8)
            
            # ANIMATE Indicate heatmap 2.0
            self.play(Indicate(heatmap, color=GOLD, scale_factor=1.3), run_time=2.0)
            
            self.wait(0.5)

        # ==========================================================
        # SCENE 6
        # ==========================================================
        # Scene 6: The Dual Formulation: Unlocking Tractability
        
        if self.mobjects:
            self.play(*[FadeOut(obj) for obj in self.mobjects], run_time=0.5)
        
        with self.voiceover(text="""Here's where the magic happens. Through convex duality, we transform the constrained primal problem into an unconstrained dual problem over potential functions α₁ through αₙ. Instead of optimizing over the enormous space of couplings, we optimize over N functions—one per marginal. The dual objective involves the convex conjugate ψ of our divergence function f. This is a concave maximization problem, which means we can use gradient ascent. Once we find the optimal potentials, we can recover the coupling using a beautiful formula involving ψ prime and the sum of potentials.""") as tracker:
            
            # Build the main equation at top
            equation = MathTex(r"\max_{\alpha_1,...,\alpha_N} \mathcal{L}(\alpha_1,...,\alpha_N)", font_size=44, color=PURPLE)
            equation.move_to(ZONES['top_center'])
            self.play(Write(equation), run_time=3)
            
            self.wait(1.0)
            
            # Create arrows pointing to center from different directions
            arrow1 = Arrow(ZONES['left'], ZONES['center'], color=BLUE, buff=0.3)
            arrow2 = Arrow(ZONES['top_center'], ZONES['center'], color=BLUE, buff=0.3)
            arrow3 = Arrow(ZONES['right'], ZONES['center'], color=BLUE, buff=0.3)
            
            # Create labels for the alphas
            text1 = Text("α₁", font_size=32, color=BLUE)
            text1.move_to(ZONES['left'])
            
            text2 = Text("α₂", font_size=32, color=BLUE)
            text2.move_to(ZONES['top_center'] + DOWN * 0.8)
            
            text3 = Text("αₙ", font_size=32, color=BLUE)
            text3.move_to(ZONES['right'])
            
            self.play(
                Create(arrow1),
                Create(arrow2),
                Create(arrow3),
                FadeIn(text1),
                FadeIn(text2),
                FadeIn(text3),
                run_time=1.5
            )
            
            self.wait(1.5)
            
            # Create 3D surface effect (mountain/concave shape)
            surface = VGroup()
            for i in range(-5, 6):
                for j in range(-4, 5):
                    # Calculate "height" for concave mountain pattern
                    dist_sq = (i * 0.4)**2 + (j * 0.4)**2
                    height_factor = max(0, 1.0 - dist_sq / 4.0)  # Concave peak at center
                    opacity = 0.15 + 0.6 * height_factor
                    
                    sq = Square(side_length=0.28, color=GOLD, fill_opacity=opacity, stroke_width=0.5, stroke_opacity=0.3)
                    # Add perspective shift based on height
                    sq.move_to(ZONES['center'] + np.array([i * 0.35, j * 0.3 + height_factor * 0.5, 0]))
                    surface.add(sq)
            
            self.play(LaggedStart(*[FadeIn(sq, shift=UP*0.1) for sq in surface], lag_ratio=0.008), run_time=2.5)
            
            # Add "Concave!" label
            concave_text = Text("Concave!", font_size=40, color=GREEN)
            concave_text.move_to(ZONES['bottom_center'] + UP * 0.5)
            self.play(FadeIn(concave_text, scale=1.2), run_time=1.0)
            
            # Indicate the surface
            self.play(Indicate(surface, color=GOLD, scale_factor=1.1), run_time=1.5)
            
            # Create the recovery formula
            formula = MathTex(r"\pi^* \propto \psi'\left(\sum \alpha_i\right)dR", font_size=36, color=ORANGE)
            formula.move_to(ZONES['bottom_center'] + DOWN * 0.8)
            self.play(Write(formula), run_time=1.5)
            
            # Circumscribe the formula
            self.play(Circumscribe(formula, color=YELLOW, run_time=2.0))
            
            self.wait(0.5)

        # ==========================================================
        # SCENE 7
        # ==========================================================
        # Scene 7: Block-Coordinate Ascent: The Algorithm
        
        if self.mobjects:
            self.play(*[FadeOut(obj) for obj in self.mobjects], run_time=0.5)
        
        with self.voiceover(text="""How do we actually solve the dual problem? Block-coordinate optimization gives us an elegant iterative algorithm. We cycle through the potentials, maximizing over each αᵢ while holding the others fixed. For the special case of N equals 2 with KL-divergence, this reduces to the famous Sinkhorn algorithm—alternating projections that converge exponentially fast. For general N and general f, we get convergence guarantees under mild conditions. Each iteration involves solving a one-dimensional optimization that's much more tractable than the full joint problem. It's divide and conquer at its finest.""") as tracker:
            
            # Create network with 4 nodes
            import math
            num_nodes = 4
            radius = 1.8
            nodes = VGroup(*[
                Circle(radius=0.25, color=BLUE, fill_opacity=0.6, stroke_width=2).move_to(
                    ZONES['center'] + np.array([
                        radius * math.cos(i * 2 * math.pi / num_nodes),
                        radius * math.sin(i * 2 * math.pi / num_nodes),
                        0
                    ])
                ) for i in range(num_nodes)
            ])
            self.play(LaggedStart(*[FadeIn(node, scale=0.3) for node in nodes], lag_ratio=0.15), run_time=2)
            
            # Connect with edges
            edges = VGroup()
            for i in range(num_nodes):
                for j in range(i + 1, num_nodes):
                    if np.random.random() < 0.4:
                        edge = Line(
                            nodes[i].get_center(), 
                            nodes[j].get_center(), 
                            color=BLUE, 
                            stroke_width=1.5, 
                            stroke_opacity=0.4
                        )
                        edges.add(edge)
            self.play(LaggedStart(*[Create(edge) for edge in edges], lag_ratio=0.05), run_time=2)
            
            # Create alpha labels
            alpha1 = Text("α₁", font_size=32, color=BLUE)
            alpha1.move_to(ZONES['center'] + np.array([-1.8, 0, 0]))
            
            alpha2 = Text("α₂", font_size=32, color=GRAY)
            alpha2.move_to(ZONES['center'] + np.array([0, 1.8, 0]))
            
            alpha3 = Text("α₃", font_size=32, color=GRAY)
            alpha3.move_to(ZONES['center'] + np.array([1.8, 0, 0]))
            
            alpha4 = Text("α₄", font_size=32, color=GRAY)
            alpha4.move_to(ZONES['center'] + np.array([0, -1.8, 0]))
            
            self.play(
                FadeIn(alpha1),
                FadeIn(alpha2),
                FadeIn(alpha3),
                FadeIn(alpha4),
                run_time=1
            )
            
            # Indicate alpha1
            self.play(Indicate(alpha1, color=GOLD, scale_factor=1.3), run_time=1.0)
            self.wait(0.5)
            
            # Morph alpha1 to alpha2 (change colors)
            self.play(
                alpha1.animate.set_color(GRAY),
                alpha2.animate.set_color(BLUE),
                nodes[0].animate.set_color(GRAY),
                nodes[1].animate.set_color(BLUE),
                run_time=1
            )
            self.wait(0.5)
            
            # Morph alpha2 to alpha3
            self.play(
                alpha2.animate.set_color(GRAY),
                alpha3.animate.set_color(BLUE),
                nodes[1].animate.set_color(GRAY),
                nodes[2].animate.set_color(BLUE),
                run_time=1
            )
            self.wait(0.5)
            
            # Morph alpha3 to alpha4
            self.play(
                alpha3.animate.set_color(GRAY),
                alpha4.animate.set_color(BLUE),
                nodes[2].animate.set_color(GRAY),
                nodes[3].animate.set_color(BLUE),
                run_time=1
            )
            self.wait(0.5)
            
            # Growth animation - create branching tree structure
            trunk = VGroup()
            base = Dot(radius=0.08, color=GREEN).move_to(ZONES['center'] + DOWN * 1.5)
            trunk.add(base)
            
            # Generate branches
            branches = []
            for level in range(3):
                new_branches = []
                if level == 0:
                    sources = [base]
                else:
                    sources = branches
                
                for source in sources:
                    for angle in [-0.5, 0.5]:
                        branch_end = source.get_center() + np.array([
                            0.4 * np.sin(angle),
                            0.6,
                            0
                        ])
                        dot = Dot(radius=0.06, color=GREEN).move_to(branch_end)
                        line = Line(source.get_center(), branch_end, color=GREEN, stroke_width=2)
                        trunk.add(line, dot)
                        new_branches.append(dot)
                branches = new_branches
            
            self.play(LaggedStart(*[Create(obj) for obj in trunk], lag_ratio=0.05), run_time=2.5)
            
            # Create "Converges!" text
            converge = Text("Converges!", font_size=40, color=GREEN)
            converge.move_to(ZONES['center'] + DOWN * 2.5)
            
            self.play(FadeIn(converge), run_time=1.0)
            
            self.wait(0.5)

        # ==========================================================
        # SCENE 8
        # ==========================================================
        # Scene 8: Entropic Optimal Transport: The Gibbs Connection
        
        if self.mobjects:
            self.play(*[FadeOut(obj) for obj in self.mobjects], run_time=0.5)
        
        with self.voiceover(text="""Let's specialize to a particularly elegant case: entropic optimal transport. Here, the prior R takes a Gibbs form—exponential of negative cost divided by a temperature parameter ε. The cost function c measures how 'expensive' different couplings are—perhaps perceptual distance for images or semantic similarity for text. The optimal coupling inherits this Gibbs structure, with the learned potentials appearing in the exponent alongside the cost. The temperature ε controls a fundamental trade-off: small ε enforces the marginal constraints tightly but may lead to overfitting; large ε gives smoother solutions but looser constraint satisfaction.""") as tracker:
            
            # Build main equation at top
            equation = MathTex(r"R(x) \propto \exp\left(-\frac{c(x)}{\epsilon}\right)", font_size=44, color=ORANGE)
            equation.move_to(ZONES['top_center'])
            self.play(Write(equation), run_time=3)
            self.play(Indicate(equation, color=GOLD, scale_factor=1.3), run_time=1)
            
            self.wait(1.5)
            
            # Create heatmap visualization
            import math
            grid_size = 10
            heatmap = VGroup()
            for i in range(grid_size):
                for j in range(grid_size):
                    # Calculate intensity with interesting pattern
                    intensity = 0.3 + 0.7 * abs(math.sin((i + j) * 0.4))
                    
                    sq = Square(side_length=0.32, stroke_width=0.5, stroke_opacity=0.5)
                    # Color gradient from BLUE to RED
                    if intensity < 0.5:
                        sq.set_fill(BLUE, opacity=intensity * 1.5)
                    else:
                        sq.set_fill(RED, opacity=(intensity - 0.5) * 1.5)
                    
                    sq.move_to(ZONES['center'] + np.array([
                        (i - grid_size/2 + 0.5) * 0.37,
                        (j - grid_size/2 + 0.5) * 0.37,
                        0
                    ]))
                    heatmap.add(sq)
            
            self.play(LaggedStart(*[FadeIn(sq) for sq in heatmap], lag_ratio=0.01), run_time=2.5)
            
            # Add cost label
            cost_text = Text("Cost c(x)", font_size=32, color=WHITE)
            cost_text.move_to(ZONES['center'])
            self.play(FadeIn(cost_text), run_time=1.0)
            
            self.wait(1.0)
            
            # Create epsilon labels
            eps_small = Text("ε → 0", font_size=29, color=BLUE)
            eps_small.move_to(ZONES['bottom_left'])
            tight_label = Text("(tight)", font_size=22, color=BLUE)
            tight_label.move_to(ZONES['bottom_left'] + np.array([0, -0.4, 0]))
            
            eps_large = Text("ε → ∞", font_size=29, color=RED)
            eps_large.move_to(ZONES['bottom_right'])
            smooth_label = Text("(smooth)", font_size=22, color=RED)
            smooth_label.move_to(ZONES['bottom_right'] + np.array([0, -0.4, 0]))
            
            self.play(FadeIn(eps_small), FadeIn(tight_label), run_time=1.0)
            self.play(FadeIn(eps_large), FadeIn(smooth_label), run_time=1.0)
            
            # Create vector field overlay
            field = VGroup()
            density = 4
            for i in range(-density, density + 1):
                for j in range(-density, density + 1):
                    if i == 0 and j == 0:
                        continue
                    
                    base_pos = ZONES['center'] + np.array([i * 0.6, j * 0.5, 0])
                    # Vector pointing toward center with slight curl
                    direction = -np.array([i * 0.15 + j * 0.05, j * 0.15 - i * 0.05, 0])
                    
                    arrow = Arrow(
                        base_pos,
                        base_pos + direction,
                        buff=0,
                        color=PURPLE,
                        stroke_width=2,
                        max_tip_length_to_length_ratio=0.25
                    )
                    field.add(arrow)
            
            self.play(LaggedStart(*[Create(arr) for arr in field], lag_ratio=0.02), run_time=3)
            
            # Indicate the field
            self.play(Indicate(field, color=GOLD, scale_factor=1.1), run_time=2.0)
            
            # Final optimal coupling equation
            optimal_eq = MathTex(
                r"\pi^*(x) \propto \exp\left(\sum \alpha_i - c(x)/\epsilon\right)",
                font_size=29,
                color=GOLD
            )
            optimal_eq.move_to(ZONES['bottom_center'])
            self.play(Write(optimal_eq), run_time=2.0)
            
            self.wait(0.5)

        # ==========================================================
        # SCENE 9
        # ==========================================================
        # Scene 9: Application: Text-Guided Image Generation
        
        if self.mobjects:
            self.play(*[FadeOut(obj) for obj in self.mobjects], run_time=0.5)
        
        with self.voiceover(text="""Now let's see this framework in action for text-guided image generation. We have three marginals: source images, text instructions, and target images. The cost function lives in a latent space and combines multiple terms—perceptual similarity to preserve structure, semantic alignment with text via cross-attention, and identity preservation for face editing tasks. The learned coupling π naturally captures the three-way relationship: which source images pair with which instructions to produce which outputs. During inference, we use Langevin dynamics to sample from this learned Gibbs distribution, generating images that simultaneously respect all three constraints.""") as tracker:
            
            # Create distribution clouds for the three marginals
            center_point = ZONES['left']
            source_cloud = VGroup(*[
                Dot(radius=0.04, color=BLUE, fill_opacity=0.7).move_to(
                    center_point + np.array([
                        np.random.normal(0, 1.0/3), 
                        np.random.normal(0, 1.0/3), 
                        0
                    ])
                ) for _ in range(50)
            ])
            self.play(LaggedStart(*[FadeIn(dot, scale=0.5) for dot in source_cloud], lag_ratio=0.02), run_time=2)
            
            center_point = ZONES['top_center']
            text_cloud = VGroup(*[
                Dot(radius=0.04, color=GREEN, fill_opacity=0.7).move_to(
                    center_point + np.array([
                        np.random.normal(0, 0.8/3), 
                        np.random.normal(0, 0.8/3), 
                        0
                    ])
                ) for _ in range(50)
            ])
            self.play(LaggedStart(*[FadeIn(dot, scale=0.5) for dot in text_cloud], lag_ratio=0.02), run_time=2)
            
            center_point = ZONES['right']
            output_cloud = VGroup(*[
                Dot(radius=0.04, color=RED, fill_opacity=0.7).move_to(
                    center_point + np.array([
                        np.random.normal(0, 1.0/3), 
                        np.random.normal(0, 1.0/3), 
                        0
                    ])
                ) for _ in range(50)
            ])
            self.play(LaggedStart(*[FadeIn(dot, scale=0.5) for dot in output_cloud], lag_ratio=0.02), run_time=2)
            
            # Create labels
            source_text = Text("Source", font_size=28, color=BLUE)
            source_text.move_to(ZONES['left'])
            
            text_label = Text("Text", font_size=28, color=GREEN)
            text_label.move_to(ZONES['top_center'])
            
            output_text = Text("Output", font_size=28, color=RED)
            output_text.move_to(ZONES['right'])
            
            self.play(
                FadeIn(source_text),
                FadeIn(text_label),
                FadeIn(output_text),
                run_time=1
            )
            
            self.wait(1.0)
            
            # Create flowing particles from left to right
            start_pos = ZONES['left']
            end_pos = ZONES['right']
            particles = VGroup(*[
                Dot(radius=0.05, color=ORANGE).move_to(
                    start_pos + np.array([np.random.uniform(-0.3, 0.3), np.random.uniform(-0.3, 0.3), 0])
                ) for _ in range(25)
            ])
            self.play(LaggedStart(*[FadeIn(p, scale=0.3) for p in particles], lag_ratio=0.05), run_time=1.5)
            
            # Animate flow to destination
            animations = []
            for particle in particles:
                target = end_pos + np.array([np.random.uniform(-0.3, 0.3), np.random.uniform(-0.3, 0.3), 0])
                animations.append(particle.animate.move_to(target))
            self.play(*animations, run_time=2.5, rate_func=smooth)
            
            # Create network visualization
            import math
            num_nodes = 3
            radius = 1.8
            nodes = VGroup(*[
                Circle(radius=0.25, color=PURPLE, fill_opacity=0.6, stroke_width=2).move_to(
                    ZONES['center'] + np.array([
                        radius * math.cos(i * 2 * math.pi / num_nodes),
                        radius * math.sin(i * 2 * math.pi / num_nodes),
                        0
                    ])
                ) for i in range(num_nodes)
            ])
            self.play(LaggedStart(*[FadeIn(node, scale=0.3) for node in nodes], lag_ratio=0.15), run_time=2)
            
            # Connect with edges
            edges = VGroup()
            for i in range(num_nodes):
                for j in range(i + 1, num_nodes):
                    if np.random.random() < 0.4:
                        edge = Line(
                            nodes[i].get_center(), 
                            nodes[j].get_center(), 
                            color=PURPLE, 
                            stroke_width=1.5, 
                            stroke_opacity=0.4
                        )
                        edges.add(edge)
            self.play(LaggedStart(*[Create(edge) for edge in edges], lag_ratio=0.05), run_time=2)
            
            self.wait(1.5)
            
            # Create cost function equation
            cost = MathTex(r"c = c_{\text{percept}} + c_{\text{text}} + c_{\text{identity}}", font_size=32, color=GOLD)
            cost.move_to(ZONES['bottom_center'])
            self.play(Write(cost), run_time=2)
            
            # Animate circumscribe
            self.play(Circumscribe(cost, color=YELLOW, run_time=1.5))
            
            # Morph source to output (using clouds as proxies)
            # Create simplified shapes for morphing
            shape1 = Circle(radius=0.8, color=ORANGE, fill_opacity=0.5)
            shape1.move_to(ZONES['left'])
            self.play(FadeIn(shape1, scale=0.5), run_time=1)
            
            shape2 = Circle(radius=0.8, color=ORANGE, fill_opacity=0.5)
            shape2.move_to(ZONES['right'])
            
            self.play(Transform(shape1, shape2), run_time=2, rate_func=smooth)
            
            # Create Langevin sampling text
            langevin_text = Text("Langevin Sampling", font_size=36, color=YELLOW)
            langevin_text.move_to(ZONES['bottom_center'])
            self.play(FadeIn(langevin_text, shift=UP*0.2), run_time=1.5)
            
            self.wait(0.5)

        # ==========================================================
        # SCENE 10
        # ==========================================================
        # Scene 10: Application: Knowledge Distillation
        
        if self.mobjects:
            self.play(*[FadeOut(obj) for obj in self.mobjects], run_time=0.5)
        
        with self.voiceover(text="""The framework extends beautifully to knowledge distillation with a surprising theoretical connection. Here the three marginals are training data, teacher logits, and student logits. The MSSB formulation implements a variational relaxation of the Information Bottleneck principle—that fundamental trade-off between compression and information preservation. The dual potentials maximize a variational lower bound on the conditional mutual information between teacher and student given the data. This reveals that optimal transport and information theory are two sides of the same coin, unified by the f-divergence framework.""") as tracker:
            
            # Create network with 3 nodes
            import math
            num_nodes = 3
            radius = 1.8
            nodes = VGroup(*[
                Circle(radius=0.25, color=BLUE, fill_opacity=0.6, stroke_width=2).move_to(
                    ZONES['center'] + np.array([
                        radius * math.cos(i * 2 * math.pi / num_nodes),
                        radius * math.sin(i * 2 * math.pi / num_nodes),
                        0
                    ])
                ) for i in range(num_nodes)
            ])
            self.play(LaggedStart(*[FadeIn(node, scale=0.3) for node in nodes], lag_ratio=0.15), run_time=2)
            
            # Connect with edges
            edges = VGroup()
            for i in range(num_nodes):
                for j in range(i + 1, num_nodes):
                    if np.random.random() < 0.4:
                        edge = Line(
                            nodes[i].get_center(), 
                            nodes[j].get_center(), 
                            color=BLUE, 
                            stroke_width=1.5, 
                            stroke_opacity=0.4
                        )
                        edges.add(edge)
            self.play(LaggedStart(*[Create(edge) for edge in edges], lag_ratio=0.05), run_time=2)
            
            # Create labels for the three components
            data_text = Text("Data X", font_size=32, color=BLUE)
            data_text.move_to(ZONES['left'])
            
            teacher_text = Text("Teacher T", font_size=32, color=ORANGE)
            teacher_text.move_to(ZONES['top_center'])
            
            student_text = Text("Student S", font_size=32, color=GREEN)
            student_text.move_to(ZONES['right'])
            
            self.play(
                FadeIn(data_text),
                FadeIn(teacher_text),
                FadeIn(student_text),
                run_time=1
            )
            
            self.wait(1.0)
            
            # Build the mutual information equation
            mutual_info = MathTex("I(S;T|X)", font_size=44, color=PURPLE)
            mutual_info.move_to(ZONES['center'])
            self.play(Write(mutual_info), run_time=2)
            self.play(Indicate(mutual_info, color=GOLD, scale_factor=1.3), run_time=1.5)
            
            self.wait(1.0)
            
            # Create arrow from teacher to student (compression)
            teacher_arrow = Arrow(ZONES['top_center'], ZONES['right'], color=ORANGE, buff=0.3)
            compress_text = Text("Compress", font_size=28, color=RED)
            compress_text.move_to(ZONES['center'] + RIGHT * 1.5)
            
            self.play(Create(teacher_arrow), FadeIn(compress_text))
            
            # Create arrow from data to student (preservation)
            data_arrow = Arrow(ZONES['left'], ZONES['right'], color=BLUE, buff=0.3)
            preserve_text = Text("Preserve", font_size=28, color=GREEN)
            preserve_text.move_to(ZONES['bottom_center'])
            
            self.play(Create(data_arrow), FadeIn(preserve_text))
            
            # Create heatmap visualization
            grid_size = 8
            heatmap = VGroup()
            for i in range(grid_size):
                for j in range(grid_size):
                    # Calculate intensity
                    intensity = 0.3 + 0.7 * abs(math.sin((i + j) * 0.4))
                    
                    sq = Square(side_length=0.32, stroke_width=0.5, stroke_opacity=0.5)
                    # Color gradient from BLUE to RED
                    if intensity < 0.5:
                        sq.set_fill(BLUE, opacity=intensity * 1.5)
                    else:
                        sq.set_fill(RED, opacity=(intensity - 0.5) * 1.5)
                    
                    sq.move_to(ZONES['center'] + np.array([
                        (i - grid_size/2 + 0.5) * 0.37,
                        (j - grid_size/2 + 0.5) * 0.37,
                        0
                    ]))
                    heatmap.add(sq)
            
            # Fade out previous elements and show heatmap
            self.play(
                FadeOut(nodes),
                FadeOut(edges),
                FadeOut(mutual_info),
                FadeOut(teacher_arrow),
                FadeOut(data_arrow),
                FadeOut(compress_text),
                FadeOut(preserve_text),
                run_time=0.8
            )
            
            self.play(LaggedStart(*[FadeIn(sq) for sq in heatmap], lag_ratio=0.01), run_time=2.5)
            
            # Create bottleneck label
            bottleneck = Text("Information Bottleneck", font_size=36, color=GOLD)
            bottleneck.move_to(ZONES['bottom_center'])
            
            self.play(FadeIn(bottleneck, shift=UP * 0.3), run_time=1)
            self.play(Circumscribe(bottleneck, color=YELLOW, run_time=2.0))
            
            self.wait(0.5)

        # ==========================================================
        # SCENE 11
        # ==========================================================
        # Scene 11: Task-Oriented Priors: Design Freedom
        
        if self.mobjects:
            self.play(*[FadeOut(obj) for obj in self.mobjects], run_time=0.5)
        
        with self.voiceover(text="""One of the most powerful aspects of the static formulation is the flexibility to design task-specific priors through the cost function. For image generation, you might use perceptual losses in feature space. For cross-modal alignment, you could incorporate attention mechanisms. For style transfer, you might penalize deviations in texture statistics. Each application gets its own custom prior that encodes domain knowledge. This design freedom is a key advantage over dynamic formulations, where the prior is typically constrained to be a diffusion process. You're not just solving a generic transport problem—you're sculpting the solution space to match your specific needs.""") as tracker:
            
            # CREATE Text "Cost Design" at=top_center color=GOLD size=1.2
            title = Text("Cost Design", font_size=72, color=GOLD)
            title.move_to(ZONES['top_center'])
            self.play(FadeIn(title, scale=0.8), run_time=1)
            
            # WAIT 1.0
            self.wait(1.0)
            
            # GROWTH_ANIMATION tree BLUE
            # Create branching structure
            trunk = VGroup()
            base = Dot(radius=0.08, color=BLUE).move_to(ZONES['center'] + DOWN * 1.5)
            trunk.add(base)
            
            # Generate branches
            branches = []
            for level in range(3):
                new_branches = []
                if level == 0:
                    sources = [base]
                else:
                    sources = branches
                
                for source in sources:
                    for angle in [-0.5, 0.5]:
                        branch_end = source.get_center() + np.array([
                            0.4 * np.sin(angle),
                            0.6,
                            0
                        ])
                        dot = Dot(radius=0.06, color=BLUE).move_to(branch_end)
                        line = Line(source.get_center(), branch_end, color=BLUE, stroke_width=2)
                        trunk.add(line, dot)
                        new_branches.append(dot)
                branches = new_branches
            
            self.play(LaggedStart(*[Create(obj) for obj in trunk], lag_ratio=0.05), run_time=2.5)
            
            # CREATE Text "Perceptual" at=center_left color=BLUE size=0.7
            perceptual = Text("Perceptual", font_size=42, color=BLUE)
            perceptual.move_to(ZONES['center_left'])
            self.play(FadeIn(perceptual), run_time=0.5)
            
            # CREATE Text "Semantic" at=top_center color=GREEN size=0.7
            semantic = Text("Semantic", font_size=42, color=GREEN)
            semantic.move_to(ZONES['top_center'] + DOWN * 0.8)
            self.play(FadeIn(semantic), run_time=0.5)
            
            # CREATE Text "Identity" at=center_right color=ORANGE size=0.7
            identity = Text("Identity", font_size=42, color=ORANGE)
            identity.move_to(ZONES['center_right'])
            self.play(FadeIn(identity), run_time=0.5)
            
            # CREATE Text "Texture" at=bottom_left color=PURPLE size=0.7
            texture = Text("Texture", font_size=42, color=PURPLE)
            texture.move_to(ZONES['bottom_left'])
            self.play(FadeIn(texture), run_time=0.5)
            
            # CREATE Text "Attention" at=bottom_right color=RED size=0.7
            attention = Text("Attention", font_size=42, color=RED)
            attention.move_to(ZONES['bottom_right'])
            self.play(FadeIn(attention), run_time=0.5)
            
            # WAIT 1.5
            self.wait(1.5)
            
            # Fade out tree and labels
            self.play(
                FadeOut(trunk),
                FadeOut(perceptual),
                FadeOut(semantic),
                FadeOut(identity),
                FadeOut(texture),
                FadeOut(attention),
                run_time=0.8
            )
            
            # 3D_SURFACE wave PURPLE
            # Create layered squares with depth illusion
            surface = VGroup()
            for i in range(-4, 5):
                for j in range(-3, 4):
                    # Calculate "height" for wave pattern
                    import math
                    height_factor = 0.5 + 0.5 * math.sin(i * 0.5) * math.cos(j * 0.5)
                    opacity = 0.2 + 0.5 * height_factor
                    
                    sq = Square(side_length=0.35, color=PURPLE, fill_opacity=opacity, stroke_width=0.5)
                    # Add perspective shift
                    sq.move_to(ZONES['center'] + np.array([i * 0.45, j * 0.4 + height_factor * 0.3, 0]))
                    surface.add(sq)
            
            self.play(LaggedStart(*[FadeIn(sq, shift=UP*0.1) for sq in surface], lag_ratio=0.01), run_time=2.5)
            
            # MORPH wave mountain ORANGE
            # Create target shape (mountain-like)
            mountain = VGroup()
            for i in range(-4, 5):
                for j in range(-3, 4):
                    # Calculate "height" for mountain pattern (peak in center)
                    height_factor = 1.0 - (abs(i) + abs(j)) / 10.0
                    height_factor = max(0.1, height_factor)
                    opacity = 0.2 + 0.6 * height_factor
                    
                    sq = Square(side_length=0.35, color=ORANGE, fill_opacity=opacity, stroke_width=0.5)
                    # Add perspective shift
                    sq.move_to(ZONES['center'] + np.array([i * 0.45, j * 0.4 + height_factor * 0.5, 0]))
                    mountain.add(sq)
            
            # Morph
            self.play(Transform(surface, mountain), run_time=2, rate_func=smooth)
            
            # CREATE Text "Custom Prior R" at=bottom_center color=GOLD size=1.0
            prior = Text("Custom Prior R", font_size=60, color=GOLD)
            prior.move_to(ZONES['bottom_center'])
            self.play(FadeIn(prior, shift=UP*0.3), run_time=1)
            
            # ANIMATE Indicate prior 2.0
            self.play(Indicate(prior, color=GOLD, scale_factor=1.3), run_time=2.0)
            
            self.wait(0.5)

        # ==========================================================
        # SCENE 12
        # ==========================================================
        # Scene 12: The Unified Framework
        
        if self.mobjects:
            self.play(*[FadeOut(obj) for obj in self.mobjects], run_time=0.5)
        
        with self.voiceover(text="""Let's step back and appreciate what we've built. Multi-marginal Static Schrödinger Bridges with general f-divergence provide a unified mathematical framework for multimodal AI problems. The static formulation gives computational efficiency. The f-divergence flexibility lets us choose the right notion of distance for each task. The dual formulation makes optimization tractable through block-coordinate ascent. And the entropic regularization connects to both optimal transport and information theory. From text-guided generation to knowledge distillation, from three marginals to arbitrary N, this framework reveals the deep mathematical structure underlying modern multimodal learning. It's not just a new algorithm—it's a new way of thinking about how multiple probability distributions can optimally interact.""") as tracker:
            
            # Create central network framework
            import math
            num_nodes = 6
            radius = 1.8
            nodes = VGroup(*[
                Circle(radius=0.25, color=GOLD, fill_opacity=0.6, stroke_width=2).move_to(
                    ZONES['center'] + np.array([
                        radius * math.cos(i * 2 * math.pi / num_nodes),
                        radius * math.sin(i * 2 * math.pi / num_nodes),
                        0
                    ])
                ) for i in range(num_nodes)
            ])
            self.play(LaggedStart(*[FadeIn(node, scale=0.3) for node in nodes], lag_ratio=0.15), run_time=2)
            
            # Connect with edges
            edges = VGroup()
            for i in range(num_nodes):
                for j in range(i + 1, num_nodes):
                    if np.random.random() < 0.4:
                        edge = Line(
                            nodes[i].get_center(), 
                            nodes[j].get_center(), 
                            color=GOLD, 
                            stroke_width=1.5, 
                            stroke_opacity=0.4
                        )
                        edges.add(edge)
            self.play(LaggedStart(*[Create(edge) for edge in edges], lag_ratio=0.05), run_time=2)
            
            # Store network for later reference
            network = VGroup(nodes, edges)
            
            # Create distribution clouds at various positions
            # Center left - BLUE cloud
            center_point_1 = ZONES['center_left']
            cloud_1 = VGroup(*[
                Dot(radius=0.04, color=BLUE, fill_opacity=0.7).move_to(
                    center_point_1 + np.array([
                        np.random.normal(0, 0.8/3), 
                        np.random.normal(0, 0.8/3), 
                        0
                    ])
                ) for _ in range(50)
            ])
            
            # Top center - GREEN cloud
            center_point_2 = ZONES['top_center']
            cloud_2 = VGroup(*[
                Dot(radius=0.04, color=GREEN, fill_opacity=0.7).move_to(
                    center_point_2 + np.array([
                        np.random.normal(0, 0.8/3), 
                        np.random.normal(0, 0.8/3), 
                        0
                    ])
                ) for _ in range(50)
            ])
            
            # Center right - RED cloud
            center_point_3 = ZONES['center_right']
            cloud_3 = VGroup(*[
                Dot(radius=0.04, color=RED, fill_opacity=0.7).move_to(
                    center_point_3 + np.array([
                        np.random.normal(0, 0.8/3), 
                        np.random.normal(0, 0.8/3), 
                        0
                    ])
                ) for _ in range(50)
            ])
            
            # Bottom left - ORANGE cloud
            center_point_4 = ZONES['bottom_left']
            cloud_4 = VGroup(*[
                Dot(radius=0.04, color=ORANGE, fill_opacity=0.7).move_to(
                    center_point_4 + np.array([
                        np.random.normal(0, 0.8/3), 
                        np.random.normal(0, 0.8/3), 
                        0
                    ])
                ) for _ in range(50)
            ])
            
            # Bottom center - PURPLE cloud
            center_point_5 = ZONES['bottom_center']
            cloud_5 = VGroup(*[
                Dot(radius=0.04, color=PURPLE, fill_opacity=0.7).move_to(
                    center_point_5 + np.array([
                        np.random.normal(0, 0.8/3), 
                        np.random.normal(0, 0.8/3), 
                        0
                    ])
                ) for _ in range(50)
            ])
            
            # Bottom right - YELLOW cloud
            center_point_6 = ZONES['bottom_right']
            cloud_6 = VGroup(*[
                Dot(radius=0.04, color=YELLOW, fill_opacity=0.7).move_to(
                    center_point_6 + np.array([
                        np.random.normal(0, 0.8/3), 
                        np.random.normal(0, 0.8/3), 
                        0
                    ])
                ) for _ in range(50)
            ])
            
            # Group all clouds
            all_clouds = [cloud_1, cloud_2, cloud_3, cloud_4, cloud_5, cloud_6]
            
            # Animate clouds with lagged start
            self.play(LaggedStart(*[LaggedStart(*[FadeIn(dot, scale=0.5) for dot in cloud], lag_ratio=0.02) for cloud in all_clouds], lag_ratio=0.2), run_time=3.0)
            
            self.wait(1.0)
            
            # Perspective shift on network
            self.play(
                network.animate.shift(RIGHT * 0.3).scale(0.95),
                run_time=2,
                rate_func=there_and_back
            )
            
            # Build central equation
            equation = MathTex(r"\text{MSSB}_{D_f}", font_size=44, color=GOLD)
            equation.move_to(ZONES['center'])
            self.play(Write(equation), run_time=2)
            self.play(Indicate(equation, color=GOLD, scale_factor=1.3), run_time=1)
            
            # Store framework reference (network + equation)
            framework = VGroup(network, equation)
            
            # Circumscribe the framework
            self.play(Circumscribe(framework, color=YELLOW, run_time=2.0))
            
            # Growth animation - create branching tree structure
            trunk = VGroup()
            base = Dot(radius=0.08, color=GOLD).move_to(ZONES['center'] + DOWN * 1.5)
            trunk.add(base)
            
            # Generate branches
            branches = []
            for level in range(3):
                new_branches = []
                if level == 0:
                    sources = [base]
                else:
                    sources = branches
                
                for source in sources:
                    for angle in [-0.5, 0.5]:
                        branch_end = source.get_center() + np.array([
                            0.4 * np.sin(angle),
                            0.6,
                            0
                        ])
                        dot = Dot(radius=0.06, color=GOLD).move_to(branch_end)
                        line = Line(source.get_center(), branch_end, color=GOLD, stroke_width=2)
                        trunk.add(line, dot)
                        new_branches.append(dot)
                branches = new_branches
            
            self.play(LaggedStart(*[Create(obj) for obj in trunk], lag_ratio=0.05), run_time=2.5)
            
            # Create title at bottom
            title = Text("Unified Multimodal Framework", font_size=36, color=GOLD)
            title.move_to(ZONES['bottom_center'])
            self.play(FadeIn(title), run_time=1)
            
            # Indicate title
            self.play(Indicate(title, color=GOLD, scale_factor=1.3), run_time=2.0)
            
            self.wait(0.5)
