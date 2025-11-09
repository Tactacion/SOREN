# visual_system.py
"""
3Blue1Brown Visual Design System
The secret sauce for quality
"""

from dataclasses import dataclass
from typing import List, Dict, Tuple
import json

@dataclass
class VisualMetaphor:
    """A specific way to visualize a concept"""
    concept_type: str
    visual_description: str
    manim_approach: str
    example_code: str

# The 3B1B Visual Language
VISUAL_METAPHORS = {
    "probability_distribution": VisualMetaphor(
        concept_type="probability_distribution",
        visual_description="Smooth landscape/surface with height representing probability",
        manim_approach="Surface3D with color gradient, particles flowing on surface",
        example_code="""
# Create smooth probability landscape
surface = Surface(
    lambda u, v: np.array([u, v, gaussian_2d(u, v)]),
    u_range=[-3, 3], v_range=[-3, 3],
    fill_opacity=0.7,
    checkerboard_colors=[BLUE_D, BLUE_E]
)
# Add flowing particles
particles = VGroup(*[Dot(radius=0.05, color=WHITE) for _ in range(50)])
"""
    ),
    
    "optimization": VisualMetaphor(
        concept_type="optimization",
        visual_description="Ball rolling down gradient on loss landscape",
        manim_approach="3D surface with animated ball following gradient",
        example_code="""
# Loss landscape
landscape = Surface(...)
# Optimization ball
ball = Sphere(radius=0.1, color=ORANGE)
# Gradient vectors
grad_field = ArrowVectorField(gradient_function, color=YELLOW)
"""
    ),
    
    "transformation": VisualMetaphor(
        concept_type="transformation",
        visual_description="Grid morphing to show function transformation",
        manim_approach="NumberPlane with ApplyPointwiseFunction",
        example_code="""
# Grid that morphs
plane = NumberPlane()
# Apply transformation
self.play(
    plane.animate.apply_function(lambda p: transformation(p)),
    run_time=3
)
"""
    ),
    
    "flow": VisualMetaphor(
        concept_type="flow",
        visual_description="Particle system flowing from A to B",
        manim_approach="VGroup of dots with staggered movement",
        example_code="""
# Particle flow
particles = VGroup(*[
    Dot(start_pos + np.random.randn(3)*0.1, radius=0.03)
    for _ in range(100)
])
# Flow animation
self.play(
    *[particle.animate.move_to(end_pos) for particle in particles],
    rate_func=smooth,
    run_time=3
)
"""
    ),
    
    "neural_network": VisualMetaphor(
        concept_type="neural_network",
        visual_description="Layered nodes with weighted connections, activation waves",
        manim_approach="VGroup layers with animated edges, brightness = activation",
        example_code="""
# Network layers
layers = [VGroup(*[Circle(radius=0.15) for _ in range(n)]) 
          for n in [3, 5, 5, 2]]
# Connections with weights
edges = VGroup(*[Line(n1.get_center(), n2.get_center(), stroke_width=weight) 
                 for n1, n2 in pairs])
# Activation wave
self.play(
    *[node.animate.set_fill(YELLOW, opacity=activation[i]) 
      for i, node in enumerate(all_nodes)],
    lag_ratio=0.1
)
"""
    ),
}

@dataclass
class AnimationChoreography:
    """Sophisticated animation patterns"""
    
    @staticmethod
    def progressive_reveal(objects: List, narration_key_points: List[str]) -> str:
        """Reveal objects in sync with key points"""
        return """
# Progressive reveal synchronized with narration
with self.voiceover(text=full_narration) as tracker:
    # Intro (0-20% of time)
    self.play(Write(title), run_time=tracker.duration * 0.2)
    
    # Key point 1 (20-45%)
    self.play(Create(object1), run_time=tracker.duration * 0.25)
    
    # Key point 2 (45-75%)
    self.play(Transform(object1, object2), run_time=tracker.duration * 0.3)
    
    # Conclusion (75-100%)
    self.play(FadeIn(conclusion), run_time=tracker.duration * 0.25)
"""
    
    @staticmethod
    def morph_transition(old_objects: List, new_concept: str) -> str:
        """Smooth morph between related concepts"""
        return """
# Don't just fade out - MORPH to show relationship
old_representation = VGroup(...)
new_representation = VGroup(...)

# Morphing transformation
self.play(
    ReplacementTransform(old_representation, new_representation),
    run_time=2,
    rate_func=smooth
)
"""
    
    @staticmethod
    def emphasis_pattern() -> str:
        """3B1B-style emphasis"""
        return """
# Emphasis technique: flash + zoom + hold
important_object = ...

self.play(
    important_object.animate.scale(1.2).set_color(YELLOW),
    Flash(important_object, color=YELLOW, line_length=0.5),
    run_time=0.5
)
self.wait(0.8)  # Hold for emphasis
self.play(
    important_object.animate.scale(1/1.2).set_color(original_color),
    run_time=0.3
)
"""

def get_visual_strategy(concept_type: str) -> str:
    """Get the visual approach for a concept type"""
    
    strategies = {
        "probability": "Smooth surfaces, particle flows, gradient colors",
        "optimization": "Landscapes with gradient descent, loss curves",
        "architecture": "Layered boxes, data flow arrows, dimensions labeled",
        "attention": "Spotlights, weighted connections, query-key-value dance",
        "loss_function": "Error surfaces, contour plots, descent paths",
        "sampling": "Random particle generation, distribution matching",
        "generative": "Empty → filled, noise → structure, creative process",
    }
    
    return strategies.get(concept_type, "Abstract geometric visualization")

def prevent_overlap(existing_objects: List[str]) -> str:
    """Generate code to avoid overlaps"""
    
    if not existing_objects:
        return "# Clean slate - position freely"
    
    return f"""
# Existing objects: {', '.join(existing_objects)}
# STRATEGY: Move to background or clear specific zones

# Option 1: Fade to background
old_objects = VGroup(*[obj for obj in self.mobjects if obj not in [camera]])
self.play(
    old_objects.animate.scale(0.5).set_opacity(0.3).to_edge(UP),
    run_time=0.8
)

# Option 2: Clear specific zone
if len(self.mobjects) > 3:  # Too crowded
    self.play(FadeOut(*self.mobjects[:-2]), run_time=0.5)

# Now position new content
"""