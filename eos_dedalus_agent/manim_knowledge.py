# manim_knowledge.py

# This file stores all the hard-won knowledge about the Manim API.
# Both the Generator and Fixer tools will use this.
# Enhanced with comprehensive API documentation and best practices.

MANIM_API_KNOWLEDGE = """
# ============================================================================
# MANIM 0.18.1 COMMUNITY EDITION - COMPREHENSIVE API REFERENCE
# ============================================================================

## CRITICAL RULES FOR VOICEOVER SCENES
**CAMERA ANIMATION IN VoiceoverScene IS COMPLETELY BANNED.**
* The camera API is non-standard and causes crashes in voiceover contexts.
* NEVER use camera.animate, move_camera, or set_camera_orientation
* Instead of zooming camera: Scale the mobjects with obj.animate.scale()
* Instead of panning camera: Use FadeOut on other objects or Indicate for focus

**ALLOWED FOCUS TECHNIQUES:**
✅ self.play(obj.animate.scale(2))          # Zoom in on object
✅ self.play(obj.animate.scale(0.5))        # Zoom out
✅ self.play(Indicate(obj, color=YELLOW))   # Point at object
✅ self.play(Circumscribe(obj, color=RED))  # Circle object
✅ self.play(FadeOut(other_obj))           # Focus by removing distractions
✅ self.play(obj.animate.move_to(ORIGIN))  # Center object

<FORBIDDEN_API>
    <!-- ABSOLUTELY BANNED - WILL CAUSE CRASHES -->
    <COMMAND>interpolate_color</COMMAND>
    <COMMAND>ManimColor.interpolate</COMMAND>
    <COMMAND>self.camera.animate</COMMAND>
    <COMMAND>self.camera.frame.animate</COMMAND>
    <COMMAND>self.camera.frame_center.animate</COMMAND>
    <COMMAND>self.move_camera</COMMAND>
    <COMMAND>self.set_camera_orientation</COMMAND>
    <COMMAND>...animate.stretch</COMMAND>
    <COMMAND>...animate.set_stretch</COMMAND>
    <COMMAND>stroke_dasharray</COMMAND>
    <COMMAND>...animate.restore()</COMMAND>
    <!-- Any .animate method not in ALLOWED list below -->
</FORBIDDEN_API>

<ALLOWED_API>
    <!-- ========================================================== -->
    <!-- 1. SCENE OPERATIONS (PRIMARY COMMANDS) -->
    <!-- ========================================================== -->
    <SECTION NAME="Scene Operations">
        <COMMAND>self.play(animation_1, animation_2, ...)</COMMAND>
        <COMMAND>self.add(mobject_1, mobject_2, ...)</COMMAND>
        <COMMAND>self.remove(mobject_1, mobject_2, ...)</COMMAND>
        <COMMAND>self.wait(duration)</COMMAND>
        <COMMAND>self.voiceover(text="...") as tracker:</COMMAND>
    </SECTION>

    <!-- ========================================================== -->
    <!-- 2. ANIMATION CLASSES (for use inside `self.play()`) -->
    <!-- ========================================================== -->
    <SECTION NAME="Animation Classes">
        <COMMAND>Create(mobject)</COMMAND>
        <COMMAND>Uncreate(mobject)</COMMAND>
        <COMMAND>Write(mobject)</COMMAND>
        <COMMAND>FadeIn(mobject, shift=...)</COMMAND>
        <COMMAND>FadeOut(mobject, shift=...)</COMMAND>
        <COMMAND>DrawBorderThenFill(mobject)</COMMAND>
        <COMMAND>Transform(mobject_a, mobject_b)</COMMAND>
        <COMMAND>ReplacementTransform(mobject_a, mobject_b)</COMMAND>
        <COMMAND>MoveAlongPath(mobject, path)</COMMAND>
        <COMMAND>Rotate(mobject, angle=...)</COMMAND>
        <COMMAND>Indicate(mobject, color=...)</COMMAND>
        <COMMAND>Circumscribe(mobject, color=...)</COMMAND>
        <COMMAND>Flash(point, color=...)</COMMAND>
        <COMMAND>AnimationGroup(anim_1, anim_2, lag_ratio=...)</COMMAND>
        <COMMAND>Succession(anim_1, anim_2, ...)</COMMAND>
    </SECTION>

    <!-- ========================================================== -->
    <!-- 3. `.animate` PROPERTIES (The *ONLY* allowed methods) -->
    <!-- ========================================================== -->
    <SECTION NAME="Allowed .animate Methods">
        <COMMAND>mobject.animate.scale(value)</COMMAND>
        <COMMAND>mobject.animate.shift(DIRECTION)</COMMAND>
        <COMMAND>mobject.animate.move_to(point_or_mobject)</COMMAND>
        <COMMAND>mobject.animate.set_color(COLOR)</COMMAND>
        <COMMAND>mobject.animate.set_opacity(value)</COMMAND>
        <COMMAND>mobject.animate.set_fill(color=..., opacity=...)</COMMAND>
        <COMMAND>mobject.animate.set_stroke(color=..., width=...)</COMMAND>
        <COMMAND>mobject.animate.rotate(angle)</COMMAND>
        <COMMAND>mobject.animate.align_to(mobject, DIRECTION)</COMMAND>
        <COMMAND>mobject.animate.next_to(mobject, DIRECTION)</COMMAND>
    </SECTION>

    <!-- ========================================================== -->
    <!-- 4. MOBJECT CREATION (The most common mobjects) -->
    <!-- ========================================================== -->
    <SECTION NAME="Mobject Creation">
        <COMMAND>Circle(radius=...)</COMMAND>
        <COMMAND>Square(side_length=...)</COMMAND>
        <COMMAND>Rectangle(width=..., height=...)</COMMAND>
        <COMMAND>Polygon(p1, p2, p3, ...)</COMMAND>
        <COMMAND>Dot(point=...)</COMMAND>
        <COMMAND>Line(start, end)</COMMAND>
        <COMMAND>Arrow(start, end, buff=...)</COMMAND>
        <COMMAND>DashedLine(start, end, dash_length=...)</COMMAND>
        <COMMAND>DashedRectangle(width=..., height=..., dash_length=...)</COMMAND>
        <COMMAND>Cross(mobject)</COMMAND>
        <COMMAND>Text(str(text))</COMMAND>
        <COMMAND>MathTex(r"latex_string")</COMMAND>
        <COMMAND>Group(mobject_1, mobject_2, ...)</COMMAND>
        <COMMAND>VGroup(vmobject_1, vmobject_2, ...)</COMMAND>
        <COMMAND>Axes(x_range=..., y_range=..., ...)</COMMAND>
        <COMMAND>axes.plot(lambda_func, x_range=...)</COMMAND>
        <COMMAND>SurroundingRectangle(mobject, buff=...)</COMMAND>
        <COMMAND>Brace(mobject, direction=...)</COMMAND>
        <COMMAND>SVGMobject("path/to/file.svg")</COMMAND>
        <COMMAND>VMobject()</COMMAND>
    </SECTION>

    <!-- ========================================================== -->
    <!-- 5. COMMON MOBJECT METHODS (For setup, not animation) -->
    <!-- ========================================================== -->
    <SECTION NAME="Common Mobject Utility Methods">
        <COMMAND>mobject.move_to(point_or_mobject)</COMMAND>
        <COMMAND>mobject.shift(DIRECTION)</COMMAND>
        <COMMAND>mobject.scale(value)</COMMAND>
        <COMMAND>mobject.next_to(mobject, DIRECTION, buff=...)</COMMAND>
        <COMMAND>mobject.set_color(COLOR)</COMMAND>
        <COMMAND>mobject.set_fill(color=..., opacity=...)</COMMAND>
        <COMMAND>mobject.set_stroke(color=..., width=..., opacity=...)</COMMAND>
        <COMMAND>mobject.save_state()</COMMAND>
        <COMMAND>vgroup.arrange(DIRECTION, buff=...)</COMMAND>
        <COMMAND>mobject.get_center()</COMMAND>
        <COMMAND>vmobject.set_points_as_corners([...])</COMMAND>
    </SECTION>
    
    <!-- ========================================================== -->
    <!-- 6. OTHER -->
    <!-- ========================================================== -->
    <SECTION NAME="Colors and Constants">
        **Colors are STRINGS (not objects):**
        PRIMARY_COLORS = {
            "BLUE": "#58C4DD",
            "GREEN": "#8BE17D",
            "RED": "#FF6188",
            "YELLOW": "#FFD866",
            "PURPLE": "#AB9DF2",
            "ORANGE": "#FF9472",
            "PINK": "#FF6AB3",
            "TEAL": "#78DCE8",
            "GRAY": "#727072",
            "WHITE": "#FCFCFA",
            "BLACK": "#000000"
        }

        **Directional Constants:**
        ✅ ORIGIN (0,0,0) - Use this instead of CENTER
        ✅ UP, DOWN, LEFT, RIGHT (unit vectors)
        ✅ UL, UR, DL, DR (diagonal corners)
        ✅ PI, TAU (mathematical constants)
        ❌ CENTER - Does not exist, use ORIGIN

        **Module Usage:**
        ✅ numpy as np - ALL math operations (np.sin, np.cos, np.array, etc.)
        ✅ from manim import * - Already includes everything needed
        ❌ import math - Use numpy instead (np.sin not math.sin)
        ❌ import random - Use np.random instead
        ❌ import scipy - Not available in rendering environment
        ❌ from scipy.special import betainc - Will crash
    </SECTION>

    <SECTION NAME="Best Practices for 3Blue1Brown Style">
        **Pacing and Timing:**
        - Each voiceover segment: 5-15 seconds maximum
        - Use self.wait(0.5) for brief pauses between related animations
        - Use self.wait(1) for topic transitions
        - Match animation duration to narration with tracker.get_remaining_duration()

        **Visual Hierarchy:**
        - Start with simple shapes, build complexity gradually
        - Use color to direct attention (highlight key elements)
        - Remove or fade old content before adding new (avoid clutter)
        - Keep 3-5 mobjects on screen at once maximum

        **Animation Flow:**
        - Introduce concept → Show transformation → Reveal insight
        - Use Create() for drawing new objects from nothing
        - Use FadeIn() with shift for objects appearing from direction
        - Use ReplacementTransform() to show one thing becoming another
        - Use AnimationGroup with lag_ratio for staggered group animations

        **Common Patterns:**
        # Pattern 1: Build equation step by step
        eq1 = MathTex("E")
        eq2 = MathTex("E = mc")
        eq3 = MathTex("E = mc^2")
        self.play(Write(eq1))
        self.play(ReplacementTransform(eq1, eq2))
        self.play(ReplacementTransform(eq2, eq3))

        # Pattern 2: Focus on specific part
        equation = MathTex("x^2", "+", "y^2", "=", "r^2")
        self.play(Write(equation))
        self.play(Indicate(equation[0], color=YELLOW))  # Highlight x^2

        # Pattern 3: Transform shape to show concept
        square = Square()
        circle = Circle()
        self.play(Create(square))
        self.wait(0.5)
        self.play(Transform(square, circle))  # Square morphs into circle
    </SECTION>

    <SECTION NAME="Type Safety Reminders">
        **Text/MathTex Input Must Be str:**
        ✅ Text("Hello")
        ✅ Text(str(variable))
        ✅ MathTex(r"x^2")
        ❌ Text(np.random.choice([...])) - numpy.str_ will crash
        ❌ Text(5) - int will crash
        SOLUTION: Always wrap in str() if uncertain: Text(str(value))

        **VGroup vs Group:**
        ✅ VGroup(circle, square, line) - All VMobjects
        ✅ Group(*self.mobjects) - Any mobjects including Groups
        ❌ VGroup(*self.mobjects) - Will crash if contains Group
        ❌ VGroup(Group(...)) - Will crash, Groups aren't VMobjects

        **SVGMobject vs VMobject:**
        ✅ SVGMobject("file.svg") - Load external SVG file
        ✅ VMobject().set_points_as_corners([...]) - Custom vector path
        ❌ SVGMobject().set_points_as_corners([...]) - Crashes, needs file
    </SECTION>
</ALLOWED_API>

## ============================================================================
## ADVANCED TECHNIQUES
## ============================================================================

**Multi-Step Transformations:**
When showing evolution of an idea, use ReplacementTransform in sequence:
```python
v1 = MathTex("\\text{Idea 1}")
v2 = MathTex("\\text{Idea 2}")
v3 = MathTex("\\text{Final Form}")
self.play(Write(v1))
self.wait()
self.play(ReplacementTransform(v1, v2))
self.wait()
self.play(ReplacementTransform(v2, v3))
```

**Cleanup Between Scenes:**
Always clean up before new major sections:
```python
# End of previous section
self.play(*[FadeOut(mob) for mob in self.mobjects])
self.wait(0.5)
# Start fresh with new section
```

**Layered Animations:**
Create depth by animating multiple objects together:
```python
self.play(
    Create(background_shape),
    Write(foreground_text),
    FadeIn(annotation, shift=UP),
    run_time=2,
    lag_ratio=0.3  # Stagger the starts
)
```

**Color Transitions:**
Smoothly change colors to show state changes:
```python
node = Circle(fill_color=BLUE, fill_opacity=0.5)
self.play(Create(node))
self.wait()
# Change state
self.play(node.animate.set_fill(RED, opacity=0.8))
```
"""

MANIM_ERROR_DATABASE = """
# ============================================================================
# COMPREHENSIVE MANIM ERROR DATABASE
# ============================================================================
# This database contains ALL known errors and their precise solutions.
# When fixing code, ALWAYS check this database first.

<ERROR_LIST>
    <!-- ================================================================ -->
    <!-- CATEGORY 1: FORBIDDEN .animate METHODS -->
    <!-- ================================================================ -->
    <ERROR>
        <PATTERN>...animate.INVALID_METHOD(...)</PATTERN>
        <SYMPTOMS>
            - TypeError: ...setter() got an unexpected keyword argument
            - AttributeError: object has no attribute 'INVALID_METHOD'
        </SYMPTOMS>
        <EXAMPLES>
            ❌ obj.animate.stretch(2)
            ❌ obj.animate.set_stretch(2)
            ❌ obj.animate.restore()
            ❌ obj.animate.become(other)
        </EXAMPLES>
        <SOLUTION>
            ONLY these .animate methods exist:
            .scale(), .shift(), .move_to(), .rotate(),
            .set_color(), .set_opacity(), .set_fill(), .set_stroke(),
            .align_to(), .next_to()

            Replace invalid methods with allowed ones:
            - Instead of .stretch(2): Use .scale(2) on one axis or create new object
            - Instead of .restore(): Save original properties and animate back manually
            - Instead of .become(): Use ReplacementTransform(obj, target)
        </SOLUTION>
    </ERROR>

    <!-- ================================================================ -->
    <!-- CATEGORY 2: COLOR OPERATIONS -->
    <!-- ================================================================ -->
    <ERROR>
        <PATTERN>interpolate_color(...) or ManimColor.interpolate(...)</PATTERN>
        <TRACEBACK>AttributeError: 'str' object has no attribute 'interpolate'</TRACEBACK>
        <EXPLANATION>
            Colors in Manim 0.18.1 are strings like "#58C4DD", not color objects.
            The interpolate methods don't exist on strings.
        </EXPLANATION>
        <SOLUTION>
            Use solid colors only. To show color change:
            ✅ obj.animate.set_color(BLUE)
            ✅ obj.animate.set_fill(RED, opacity=0.5)

            For gradient effect across multiple objects:
            colors = [BLUE, PURPLE, RED]
            for i, mob in enumerate(group):
                mob.set_color(colors[i % len(colors)])
        </SOLUTION>
    </ERROR>

    <!-- ================================================================ -->
    <!-- CATEGORY 3: CAMERA OPERATIONS -->
    <!-- ================================================================ -->
    <ERROR>
        <PATTERN>self.camera.*, self.move_camera(...), self.set_camera_orientation(...)</PATTERN>
        <TRACEBACK>
            - AttributeError: VoiceoverScene has no attribute 'move_camera'
            - TypeError: Invalid camera operation
        </TRACEBACK>
        <EXPLANATION>
            Camera animation is incompatible with VoiceoverScene.
            These methods are from MovingCameraScene which conflicts with voiceover timing.
        </EXPLANATION>
        <SOLUTION>
            Replace ALL camera operations with mobject operations:

            ❌ self.camera.frame.animate.scale(0.5)
            ✅ all_objects.animate.scale(2)  # "Zoom in" by scaling objects

            ❌ self.camera.frame.animate.move_to(target)
            ✅ all_objects.animate.shift(-target.get_center())  # "Pan" by shifting objects

            ❌ self.move_camera(...)
            ✅ Use FadeOut on background objects to create focus effect
        </SOLUTION>
    </ERROR>

    <!-- ================================================================ -->
    <!-- CATEGORY 4: GROUP TYPE ERRORS -->
    <!-- ================================================================ -->
    <ERROR>
        <PATTERN>VGroup(*self.mobjects) or VGroup(Group(...))</PATTERN>
        <TRACEBACK>TypeError: All submobjects of VGroup must be of type VMobject. Got Group instead.</TRACEBACK>
        <EXPLANATION>
            VGroup ONLY accepts VMobjects (visual mobjects like Circle, Text, etc.)
            Group objects themselves are not VMobjects
            self.mobjects can contain Groups, making VGroup(*self.mobjects) crash
        </EXPLANATION>
        <SOLUTION>
            ✅ VGroup(circle, square, text) - All VMobjects
            ✅ Group(*self.mobjects) - Accepts any mobjects
            ❌ VGroup(*self.mobjects) - May crash if contains Groups

            If you need VGroup specifically, filter first:
            vobjects = [m for m in self.mobjects if isinstance(m, VMobject)]
            vgroup = VGroup(*vobjects)
        </SOLUTION>
    </ERROR>

    <!-- ================================================================ -->
    <!-- CATEGORY 5: STROKE STYLING -->
    <!-- ================================================================ -->
    <ERROR>
        <PATTERN>obj.set_stroke(stroke_dasharray=[...]) or obj.set_style(stroke_dasharray=[...])</PATTERN>
        <TRACEBACK>TypeError: set_stroke() got an unexpected keyword argument 'stroke_dasharray'</TRACEBACK>
        <EXPLANATION>
            stroke_dasharray parameter doesn't exist in Manim 0.18.1
            Dashed styling must be built into the object at creation
        </EXPLANATION>
        <SOLUTION>
            ❌ line = Line(start, end)
               line.set_stroke(stroke_dasharray=[10, 5])

            ✅ line = DashedLine(start, end, dash_length=0.2)
            ✅ rect = DashedRectangle(width=4, height=2, dash_length=0.1)

            Create dashed versions from the start - cannot add dashing later
        </SOLUTION>
    </ERROR>

    <!-- ================================================================ -->
    <!-- CATEGORY 6: TYPE SAFETY -->
    <!-- ================================================================ -->
    <ERROR>
        <PATTERN>Text(non_string_value) or MathTex(non_string_value)</PATTERN>
        <TRACEBACK>
            TypeError: Argument 'orig_text' has incorrect type (expected str, got numpy.str_)
            TypeError: Argument 'orig_text' has incorrect type (expected str, got int)
        </TRACEBACK>
        <EXPLANATION>
            Text() and MathTex() ONLY accept Python str type
            numpy.str_, int, float will all crash even if they look like strings
        </EXPLANATION>
        <SOLUTION>
            ALWAYS wrap uncertain values in str():

            ❌ Text(5)
            ✅ Text("5") or Text(str(5))

            ❌ Text(np.random.choice(["A", "B"]))
            ✅ Text(str(np.random.choice(["A", "B"])))

            ❌ MathTex(variable_value)
            ✅ MathTex(str(variable_value))
        </SOLUTION>
    </ERROR>

    <!-- ================================================================ -->
    <!-- CATEGORY 7: SVG AND VECTOR OPERATIONS -->
    <!-- ================================================================ -->
    <ERROR>
        <PATTERN>SVGMobject().set_points_as_corners([...])</PATTERN>
        <TRACEBACK>ValueError: Must specify file for SVGMobject</TRACEBACK>
        <EXPLANATION>
            SVGMobject() requires a file path - it's ONLY for loading SVG files
            Custom vector paths need VMobject instead
        </EXPLANATION>
        <SOLUTION>
            ❌ shape = SVGMobject()
               shape.set_points_as_corners([...])

            ✅ shape = VMobject()
               shape.set_points_as_corners([...])

            ✅ icon = SVGMobject("path/to/file.svg")  # For loading files
        </SOLUTION>
    </ERROR>

    <!-- ================================================================ -->
    <!-- CATEGORY 8: INDEX AND BOUNDS ERRORS -->
    <!-- ================================================================ -->
    <ERROR>
        <PATTERN>IndexError accessing nested mobjects</PATTERN>
        <TRACEBACK>IndexError: list index out of range (e.g., obj[0][1][i])</TRACEBACK>
        <EXPLANATION>
            VGroups and mobject collections have unpredictable nesting
            Assuming structure like obj[0][1] often fails
        </EXPLANATION>
        <SOLUTION>
            Always check bounds and avoid deep nesting assumptions:

            ❌ for i in range(10):
                   mob = equation[0][1][i]  # Assumes specific structure

            ✅ for i in range(len(equation)):
                   mob = equation[i]

            ✅ if len(equation) > 2:
                   highlight = equation[2]

            Access VGroup members flatly, use len() to check bounds
        </SOLUTION>
    </ERROR>

    <!-- ================================================================ -->
    <!-- CATEGORY 9: STATE MANAGEMENT -->
    <!-- ================================================================ -->
    <ERROR>
        <PATTERN>obj.animate.restore() or Restore(obj)</PATTERN>
        <TRACEBACK>Exception: No state saved</TRACEBACK>
        <EXPLANATION>
            .save_state() and .restore() are unreliable in animation chains
            State may be lost or not exist
        </EXPLANATION>
        <SOLUTION>
            Don't rely on save/restore. Explicitly animate back:

            ❌ obj.save_state()
               self.play(obj.animate.scale(2).set_opacity(0.3))
               self.play(obj.animate.restore())

            ✅ original_scale = 1.0
               original_opacity = 1.0
               self.play(obj.animate.scale(2).set_opacity(0.3))
               self.play(obj.animate.scale(original_scale).set_opacity(original_opacity))
        </SOLUTION>
    </ERROR>

    <!-- ================================================================ -->
    <!-- CATEGORY 10: IMPORT AND MODULE ERRORS -->
    <!-- ================================================================ -->
    <ERROR>
        <PATTERN>from scipy import *, import math, import random</PATTERN>
        <TRACEBACK>
            ModuleNotFoundError: No module named 'scipy'
            NameError: name 'math' is not defined (when using after importing numpy)
        </TRACEBACK>
        <EXPLANATION>
            The rendering environment only has: manim, numpy, standard library basics
            scipy, pandas, matplotlib are NOT available
            Prefer numpy over math module
        </EXPLANATION>
        <SOLUTION>
            ✅ import numpy as np
               value = np.sin(angle)
               random_val = np.random.random()

            ❌ import math
               import random
               import scipy
               from scipy.special import betainc

            Use numpy for ALL mathematical operations
        </SOLUTION>
    </ERROR>
</ERROR_LIST>

## ============================================================================
## DEBUGGING WORKFLOW
## ============================================================================

When you receive an error traceback:

1. **Extract the exact error line number** from the traceback
2. **Identify the error pattern** (TypeError, AttributeError, ValueError, etc.)
3. **Search this ERROR_DATABASE** for matching pattern
4. **Apply the exact solution** from the matching error entry
5. **Verify the fix** doesn't introduce new forbidden patterns
6. **Return the complete fixed code** with ONLY that one fix applied

**DO NOT:**
- Make multiple changes at once
- Add new features while fixing
- Rewrite working code
- Change the class structure

**DO:**
- Fix only the specific error
- Keep all other code identical
- Preserve the original intent
- Use only allowed API methods
"""
