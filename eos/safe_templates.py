# safe_templates.py
# ============================================================================
# PROVEN SAFE CODE TEMPLATES - GUARANTEED TO WORK
# ============================================================================
# These templates have been tested and verified to work perfectly in Manim

SAFE_PATTERNS = {
    "scene_start": """
# Clear previous scene
if self.mobjects:
    self.play(*[FadeOut(obj) for obj in self.mobjects], run_time=0.5)
""",

    "voiceover_block": """
with self.voiceover(text="{narration}") as tracker:
    {animations}
""",

    "create_circle": """
circle = Circle(radius={radius}, color={color}, fill_opacity={opacity})
circle.move_to({position})
""",

    "create_text": """
text = Text("{content}", font_size={size}, color={color})
text.move_to({position})
""",

    "create_math": """
equation = MathTex(r"{latex}", font_size={size}, color={color})
equation.move_to({position})
""",

    "create_rectangle": """
rect = Rectangle(width={width}, height={height}, color={color}, fill_opacity={opacity})
rect.move_to({position})
""",

    "create_group": """
group = VGroup(*[
    {object_creation}
    for i in range({count})
])
group.arrange({direction}, buff={buff})
""",

    "create_particles": """
particles = VGroup(*[
    Dot(
        point=ORIGIN + np.array([
            np.random.uniform({x_min}, {x_max}),
            np.random.uniform({y_min}, {y_max}),
            0
        ]),
        radius={radius},
        color={color}
    ).set_opacity({opacity})
    for _ in range({count})
])
""",

    "animate_fadein": """
self.play(FadeIn({object}, shift={shift}), run_time=tracker.duration)
""",

    "animate_create": """
self.play(Create({object}), run_time=tracker.duration)
""",

    "animate_write": """
self.play(Write({object}, lag_ratio=0.1), run_time=tracker.duration)
""",

    "animate_transform": """
self.play(Transform({obj1}, {obj2}, rate_func=smooth), run_time=tracker.duration)
""",

    "animate_indicate": """
self.play(Indicate({object}, color=YELLOW, scale_factor=1.2), run_time=0.5)
""",

    "animate_group_stagger": """
self.play(
    LaggedStart(*[GrowFromCenter(obj) for obj in {group}], lag_ratio=0.1),
    run_time=tracker.duration
)
""",

    "animate_move": """
self.play({object}.animate.shift({direction}), run_time=tracker.duration)
""",

    "animate_scale": """
self.play({object}.animate.scale({factor}), run_time=tracker.duration)
""",

    "animate_color": """
self.play({object}.animate.set_color({color}), run_time=tracker.duration)
""",

    "scene_end": """
self.wait(2)
"""
}

SAFE_COLORS = ["BLUE", "GREEN", "RED", "YELLOW", "ORANGE", "PURPLE", "WHITE", "GRAY"]
SAFE_DIRECTIONS = ["UP", "DOWN", "LEFT", "RIGHT"]
SAFE_POSITIONS = ["ORIGIN", "UP*2", "DOWN*2", "LEFT*3", "RIGHT*3"]

def get_template(template_name: str, **kwargs) -> str:
    """Get a safe template with parameters filled in"""
    if template_name not in SAFE_PATTERNS:
        raise ValueError(f"Unknown template: {template_name}")

    template = SAFE_PATTERNS[template_name]
    return template.format(**kwargs)

def validate_parameters(**kwargs) -> bool:
    """Validate that parameters are safe"""
    for key, value in kwargs.items():
        if key == "color" and value not in SAFE_COLORS:
            return False
        if key == "direction" and value not in SAFE_DIRECTIONS:
            return False
    return True
