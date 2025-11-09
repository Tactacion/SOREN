# manim_knowledge.py
# ============================================================================
# COMPREHENSIVE MANIM 0.18.1 API KNOWLEDGE BASE
# ============================================================================
# This module contains all the knowledge needed to generate perfect Manim code

MANIM_API = """
═══════════════════════════════════════════════════════════════════════════
MANIM 0.18.1 API REFERENCE - VOICEOVER SCENE
═══════════════════════════════════════════════════════════════════════════

**CRITICAL RULES:**
1. Colors are HEX STRINGS: BLUE = "#58C4DD" (not ManimColor objects)
2. NO CAMERA ANIMATION - Use mobject.animate.scale() instead
3. Every voiceover block MUST have run_time=tracker.duration
4. ALWAYS convert colors before comparison: obj.get_fill_color().to_hex() == BLUE

═══════════════════════════════════════════════════════════════════════════
SCENE STRUCTURE
═══════════════════════════════════════════════════════════════════════════

```python
# Clear previous objects
if self.mobjects:
    self.play(*[FadeOut(obj) for obj in self.mobjects], run_time=0.5)

# Each beat gets its own voiceover block
with self.voiceover(text="Your narration here") as tracker:
    # Create objects
    obj = Circle(radius=1, color=BLUE)

    # Animate with tracker
    self.play(FadeIn(obj, shift=DOWN*0.3), run_time=tracker.duration)

self.wait(2)
```

═══════════════════════════════════════════════════════════════════════════
COLORS (ALL ARE STRINGS)
═══════════════════════════════════════════════════════════════════════════

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

**COLOR COMPARISON (CRITICAL):**
❌ WRONG: if obj.get_fill_color() == BLUE
✅ RIGHT: if obj.get_fill_color().to_hex() == BLUE

═══════════════════════════════════════════════════════════════════════════
FORBIDDEN API (DO NOT USE - WILL CRASH)
═══════════════════════════════════════════════════════════════════════════

❌ self.camera.animate
❌ self.camera.frame.animate
❌ self.camera.frame_center.animate
❌ self.move_camera()
❌ self.set_camera_orientation()
❌ interpolate_color()
❌ ManimColor.interpolate()
❌ obj.animate.stretch()
❌ CENTER (use ORIGIN instead)
❌ random.X (use np.random.X)
❌ math.X (use np.X)

═══════════════════════════════════════════════════════════════════════════
ALLOWED MOBJECT CREATION
═══════════════════════════════════════════════════════════════════════════

**Shapes:**
Circle(radius=1.0, color=BLUE, fill_opacity=0.5, stroke_width=2)
Square(side_length=2.0, color=RED, fill_opacity=0.5)
Rectangle(width=4.0, height=2.0, color=GREEN, fill_opacity=0.5)
Triangle(color=YELLOW)
Polygon(p1, p2, p3, ..., color=ORANGE, fill_opacity=0.5)
Arc(radius=1.0, start_angle=0, angle=PI, color=BLUE)
Dot(point=ORIGIN, radius=0.08, color=RED)
Ellipse(width=2.0, height=1.0, color=PURPLE)

**Lines:**
Line(start=LEFT, end=RIGHT, color=WHITE, stroke_width=2)
DashedLine(start=UP, end=DOWN, color=BLUE)
Arrow(start=LEFT, end=RIGHT, buff=0, color=YELLOW, stroke_width=3)
DoubleArrow(start=LEFT, end=RIGHT, color=GREEN)
Vector(direction=RIGHT, color=RED)

**Text:**
Text("Hello", font_size=48, color=WHITE)
Text("Bold text", font_size=48, color=WHITE, weight=BOLD)
MathTex(r"E = mc^2", font_size=36, color=BLUE)
MathTex(r"\int_0^1 f(x)dx", font_size=36)

**IMPORTANT - Text Styling:**
❌ WRONG: Text("text", slant="italic")  # No slant parameter!
✅ RIGHT: Text("text", font_size=48, color=WHITE)
✅ RIGHT: Text("text", weight=BOLD)  # For bold text

**Graphs:**
Axes(
    x_range=[-3, 3, 1],
    y_range=[-2, 2, 1],
    x_length=6,
    y_length=4,
    tips=False
)
NumberLine(x_range=[-5, 5, 1], length=10, include_numbers=True)
axes.plot(lambda x: x**2, x_range=[-2, 2], color=BLUE)
BarChart(values=[1, 2, 3, 4], bar_colors=[BLUE, GREEN, RED, YELLOW])

**Groups:**
VGroup(obj1, obj2, obj3)  # Vector group
Group(obj1, obj2, obj3)   # Generic group

**Utility:**
SurroundingRectangle(mobject, color=YELLOW, buff=0.1)
Brace(mobject, direction=DOWN, color=WHITE)

═══════════════════════════════════════════════════════════════════════════
ALLOWED ANIMATIONS
═══════════════════════════════════════════════════════════════════════════

**Creation:**
Create(mobject)
Uncreate(mobject)
Write(mobject, lag_ratio=0.1)
DrawBorderThenFill(mobject)
FadeIn(mobject, shift=DOWN*0.3, scale=0.8)
FadeOut(mobject, shift=UP*0.3, scale=1.2)
GrowFromCenter(mobject)
GrowFromEdge(mobject, edge=LEFT)

**Transformation:**
Transform(mobject1, mobject2, run_time=1)
ReplacementTransform(mobject1, mobject2)
TransformMatchingShapes(mobject1, mobject2)

**Movement:**
mobject.animate.shift(UP*2)
mobject.animate.move_to(point)
mobject.animate.next_to(other, DOWN, buff=0.5)
mobject.animate.to_edge(LEFT, buff=0.5)
mobject.animate.to_corner(UL, buff=0.5)

**Styling:**
mobject.animate.set_color(BLUE)
mobject.animate.set_opacity(0.5)
mobject.animate.set_fill(color=RED, opacity=0.8)
mobject.animate.set_stroke(color=WHITE, width=3)
mobject.animate.scale(2.0)
mobject.animate.rotate(PI/4)

**Emphasis:**
Indicate(mobject, color=YELLOW, scale_factor=1.2)
Circumscribe(mobject, color=RED, fade_out=True)
Flash(point, color=YELLOW, line_length=0.3)
FocusOn(mobject)
Wiggle(mobject)

**Sequencing:**
AnimationGroup(anim1, anim2, lag_ratio=0.5)
LaggedStart(anim1, anim2, anim3, lag_ratio=0.2)
Succession(anim1, anim2, anim3)

═══════════════════════════════════════════════════════════════════════════
MOBJECT METHODS
═══════════════════════════════════════════════════════════════════════════

**Arrangement:**
vgroup.arrange(RIGHT, buff=0.5)
vgroup.arrange_in_grid(rows=3, cols=4, buff=0.2)

**Positioning (use these, NOT during animation):**
obj.move_to(ORIGIN)
obj.shift(UP*2)
obj.next_to(other, DOWN, buff=0.5)
obj.to_edge(LEFT, buff=0.5)
obj.to_corner(UR, buff=0.5)
obj.align_to(other, UP)

**Styling (use these BEFORE animation):**
obj.set_color(BLUE)
obj.set_opacity(0.5)
obj.set_fill(color=RED, opacity=0.8)
obj.set_stroke(color=WHITE, width=3, opacity=1.0)

**Getters:**
obj.get_center()
obj.get_width()
obj.get_height()
obj.get_top()
obj.get_bottom()
obj.get_left()
obj.get_right()
obj.get_corner(UL)
obj.get_edge_center(LEFT)
obj.get_fill_color().to_hex()  # Returns hex string like "#58C4DD"

═══════════════════════════════════════════════════════════════════════════
CONSTANTS
═══════════════════════════════════════════════════════════════════════════

**Directions:**
UP, DOWN, LEFT, RIGHT, IN, OUT
UL, UR, DL, DR (corners)
ORIGIN = np.array([0, 0, 0])

**Math:**
PI = 3.14159...
TAU = 2*PI
DEGREES = PI/180

═══════════════════════════════════════════════════════════════════════════
COMMON PATTERNS
═══════════════════════════════════════════════════════════════════════════

**Creating multiple objects:**
```python
dots = VGroup(*[
    Dot(point=np.array([i*0.5, 0, 0]), color=BLUE, radius=0.05)
    for i in range(10)
])
```

**Random positioning:**
```python
particles = VGroup(*[
    Dot(
        point=ORIGIN + np.array([np.random.uniform(-3, 3), np.random.uniform(-2, 2), 0]),
        radius=0.03,
        color=BLUE
    )
    for _ in range(100)
])
```

**Grid arrangement:**
```python
grid = VGroup(*[Circle(radius=0.2, color=BLUE) for _ in range(20)])
grid.arrange_in_grid(rows=4, cols=5, buff=0.3)
```

**Conditional colors:**
```python
coins = VGroup(*[
    Circle(
        radius=0.1,
        color=BLUE if np.random.random() > 0.5 else RED,
        fill_opacity=0.8
    )
    for _ in range(10)
])
```

**Counting with color comparison:**
```python
# WRONG: count = sum([1 if coin.get_fill_color() == BLUE else 0 for coin in coins])
# RIGHT:
count = sum([1 if coin.get_fill_color().to_hex() == BLUE else 0 for coin in coins])
```

═══════════════════════════════════════════════════════════════════════════
POLISH TECHNIQUES (3BLUE1BROWN STYLE)
═══════════════════════════════════════════════════════════════════════════

1. **Secondary Motion:**
   ❌ FadeIn(obj)
   ✅ FadeIn(obj, shift=DOWN*0.3, scale=0.8)

2. **Lag Ratios:**
   ❌ Write(text)
   ✅ Write(text, lag_ratio=0.1)

3. **Rate Functions:**
   ❌ Transform(a, b)
   ✅ Transform(a, b, rate_func=smooth, run_time=1.5)

4. **Layered Animations:**
   ```python
   self.play(
       FadeIn(title, shift=DOWN*0.5),
       Create(underline),
       run_time=tracker.duration
   )
   ```

5. **Emphasis After Creation:**
   ```python
   self.play(Create(circle), run_time=tracker.duration)
   self.play(Indicate(circle, color=YELLOW), run_time=0.5)
   ```

6. **Staggered Appearances:**
   ```python
   self.play(
       LaggedStart(*[GrowFromCenter(obj) for obj in objects], lag_ratio=0.1),
       run_time=tracker.duration
   )
   ```
"""

ERROR_DATABASE = """
═══════════════════════════════════════════════════════════════════════════
COMMON MANIM ERRORS AND FIXES
═══════════════════════════════════════════════════════════════════════════

1. **TypeError: Cannot compare ManimColor with str**
   Error: coin.get_fill_color() == BLUE
   Fix: coin.get_fill_color().to_hex() == BLUE

2. **AttributeError: 'str' object has no attribute 'interpolate'**
   Error: interpolate_color(BLUE, RED, alpha)
   Fix: Don't use color interpolation - use one color

3. **AttributeError: 'Camera' object has no attribute 'frame'**
   Error: self.camera.frame.animate.move_to(...)
   Fix: obj.animate.scale(2)  # Scale object instead

4. **AttributeError: 'Camera' object has no attribute 'animate'**
   Error: self.camera.animate.move_to(...)
   Fix: obj.animate.scale(2)  # Scale object instead

5. **NameError: name 'CENTER' is not defined**
   Error: obj.move_to(CENTER)
   Fix: obj.move_to(ORIGIN)

6. **NameError: name 'random' is not defined**
   Error: random.uniform(0, 1)
   Fix: np.random.uniform(0, 1)

7. **NameError: name 'math' is not defined**
   Error: math.cos(x)
   Fix: np.cos(x)

8. **ZeroDivisionError in voiceover**
   Error: with self.voiceover(text="") as tracker:
   Fix: Ensure text is never empty

9. **AttributeError: object has no attribute 'restore'**
   Error: obj.restore() without obj.save_state()
   Fix: Call obj.save_state() before restore()

10. **ValueError: SVGMobject with set_points_as_corners**
    Error: SVGMobject().set_points_as_corners([...])
    Fix: Use VMobject().set_points_as_corners([...])

11. **IndexError: list index out of range**
    Error: obj[0][1][i] without bounds check
    Fix: Check length before indexing

12. **AttributeError: 'ManimColor' object has no attribute 'to_hex'**
    Error: Using old Manim version
    Fix: Update to Manim 0.18.1

13. **Overlapping animations causing lag**
    Error: Multiple self.play() calls without proper sequencing
    Fix: Use proper wait() between plays or AnimationGroup

14. **Text rendering with special characters**
    Error: Text with unescaped LaTeX chars
    Fix: Use raw strings r"..." or escape properly

15. **AttributeError: There is no Style Called italic**
    Error: Text("text", slant="italic")
    Fix: Remove slant parameter - Text("text", font_size=X, color=Y)
"""

CREATIVE_EXAMPLES = """
═══════════════════════════════════════════════════════════════════════════
CREATIVE ANIMATION EXAMPLES (3BLUE1BROWN INSPIRED)
═══════════════════════════════════════════════════════════════════════════

**Example 1: Particle Systems**
```python
# Create cloud of particles representing distribution
particles = VGroup(*[
    Dot(
        point=ORIGIN + np.array([
            np.random.normal(0, 1.5),
            np.random.normal(0, 0.8),
            0
        ]),
        radius=0.02,
        color=BLUE
    ).set_opacity(0.6)
    for _ in range(200)
])
self.play(
    LaggedStart(*[GrowFromCenter(p) for p in particles], lag_ratio=0.005),
    run_time=tracker.duration
)
```

**Example 2: Building Complexity**
```python
# Start simple
simple = Square(side_length=1, color=BLUE, fill_opacity=0.3)
self.play(DrawBorderThenFill(simple), run_time=tracker.duration)

# Add detail progressively
details = VGroup(*[
    Line(
        simple.get_corner(UL) + RIGHT*i*0.25,
        simple.get_corner(DL) + RIGHT*i*0.25,
        color=WHITE,
        stroke_width=1
    )
    for i in range(1, 4)
])
self.play(
    LaggedStart(*[Create(d) for d in details], lag_ratio=0.2),
    run_time=tracker.duration
)
```

**Example 3: Transformation Reveals**
```python
# Morph shape to reveal structure
before = Circle(radius=1, color=BLUE, fill_opacity=0.5)
after = Rectangle(width=3, height=0.5, color=GREEN, fill_opacity=0.5)

self.play(Create(before), run_time=tracker.duration * 0.3)
self.play(
    Transform(before, after, rate_func=smooth),
    run_time=tracker.duration * 0.7
)
```

**Example 4: Highlighting with Rings**
```python
# Draw attention with expanding circles
for _ in range(3):
    ring = Circle(radius=0.5, color=YELLOW, stroke_width=3)
    ring.move_to(obj)
    self.play(
        ring.animate.scale(2).set_opacity(0),
        run_time=0.3
    )
    self.remove(ring)
```

**Example 5: Data Visualization**
```python
# Animated bar chart growth
bars = VGroup(*[
    Rectangle(
        width=0.5,
        height=values[i],
        color=BLUE,
        fill_opacity=0.7
    ).shift(RIGHT*i*0.7 + UP*values[i]/2)
    for i in range(len(values))
])
self.play(
    LaggedStart(*[GrowFromEdge(bar, DOWN) for bar in bars], lag_ratio=0.1),
    run_time=tracker.duration
)
```

**Example 6: Mathematical Build-up**
```python
# Build equation step by step
eq_parts = [
    MathTex("E", color=YELLOW),
    MathTex("=", color=WHITE),
    MathTex("m", color=BLUE),
    MathTex("c^2", color=GREEN)
]
equation = VGroup(*eq_parts).arrange(RIGHT, buff=0.2)

for part in eq_parts:
    self.play(Write(part), run_time=tracker.duration / len(eq_parts))
    self.play(Indicate(part, color=YELLOW), run_time=0.3)
```

**Example 7: Spatial Relationships**
```python
# Show connections between objects
objects = VGroup(*[Circle(radius=0.3, color=BLUE) for _ in range(5)])
objects.arrange_in_grid(rows=1, cols=5, buff=1.0)

connections = VGroup(*[
    Arrow(
        objects[i].get_right(),
        objects[i+1].get_left(),
        buff=0.1,
        color=YELLOW,
        stroke_width=2
    )
    for i in range(4)
])

self.play(FadeIn(objects, lag_ratio=0.1), run_time=tracker.duration * 0.5)
self.play(
    LaggedStart(*[GrowArrow(arr) for arr in connections], lag_ratio=0.2),
    run_time=tracker.duration * 0.5
)
```

**Example 8: Focus Techniques**
```python
# Dim everything except focus object
all_objects = VGroup(*self.mobjects)
focus_obj = all_objects[3]

self.play(
    all_objects.animate.set_opacity(0.2),
    focus_obj.animate.set_opacity(1.0).scale(1.3),
    run_time=tracker.duration
)
```
"""

def get_full_api() -> str:
    """Returns complete API documentation"""
    return MANIM_API

def get_error_database() -> str:
    """Returns error database"""
    return ERROR_DATABASE

def get_creative_examples() -> str:
    """Returns creative examples"""
    return CREATIVE_EXAMPLES
