import anthropic
import re
from pathlib import Path
from models import Video, Scene
from typing import List
import settings as cfg
import json  # Make sure this is imported

class ManimGenerator:
    """Claude with complete Manim 0.18.1 knowledge"""
    
    def __init__(self):
        self.client = anthropic.Anthropic(api_key=cfg.ANTHROPIC_KEY)
        self.manim_api = self._build_manim_api()
        self.error_database = self._build_error_database()
        self.examples = self._build_examples()
    
    def _build_manim_api(self) -> str:
        return """
MANIM 0.18.1 API (ManimCE):


**CAMERA ANIMATION IN VoiceoverScene IS BANNED.**
* The API is non-standard and breaks. We will NOT animate the camera.
* Instead of zooming the camera, you will SCALE the mobjects.
* Instead of panning the camera, you will INDICATE or FADE OUT other objects.

**ALLOWED FOCUS TECHNIQUES:**
✅ self.play(obj.animate.scale(2)) (To "zoom in")
✅ self.play(obj.animate.scale(0.5)) (To "zoom out")
✅ self.play(Indicate(obj, color=YELLOW)) (To "point at")
✅ self.play(Circumscribe(obj)) (To "circle")
✅ self.play(FadeOut(other_obj)) (To "focus on" obj)

<FORBIDDEN_API>
    <COMMAND>interpolate_color</COMMAND>
    <COMMAND>ManimColor.interpolate</COMMAND>
    
    <COMMAND>self.camera.animate</COMMAND>
    <COMMAND>self.camera.frame.animate</COMMAND>
    <COMMAND>self.camera.frame_center.animate</COMMAND>
    <COMMAND>self.move_camera</COMMAND>
    <COMMAND>self.set_camera_orientation</COMMAND>
    
    <COMMAND>...animate.stretch</COMMAND>
    <COMMAND>...animate.set_stretch</COMMAND>
</FORBIDDEN_API>

<ALLOWED_API>
    <SECTION NAME="Scene Operations">
        <COMMAND>self.play(animation_1, animation_2, ...)</COMMAND>
        <COMMAND>self.add(mobject_1, mobject_2, ...)</COMMAND>
        <COMMAND>self.remove(mobject_1, mobject_2, ...)</COMMAND>
        <COMMAND>self.wait(duration)</COMMAND>
        <COMMAND>self.voiceover(text="...") as tracker:</COMMAND>
    </SECTION>

    <SECTION NAME="Animation Classes">
        <COMMAND>Create(mobject)</COMMAND>
        <COMMAND>Uncreate(mobject)</COMMAND>
        <COMMAND>Write(mobject)</COMMAND>
        <COMMAND>FadeIn(mobject, shift=...)</COMMAND>
        <COMMAND>FadeOut(mobject, shift=...)</COMMAND>
        <COMMAND>DrawBorderThenFill(mobject)</COMMAND>
        <COMMAND>GrowFromCenter(mobject)</COMMAND>
        <COMMAND>GrowFromEdge(mobject, edge=...)</COMMAND>

        <COMMAND>Transform(mobject_a, mobject_b)</COMMAND>
        <COMMAND>ReplacementTransform(mobject_a, mobject_b)</COMMAND>

        <COMMAND>MoveAlongPath(mobject, path)</COMMAND>
        <COMMAND>Rotate(mobject, angle=...)</COMMAND>
        
        <COMMAND>Indicate(mobject, color=...)</COMMAND>
        <COMMAND>Circumscribe(mobject, color=...)</COMMAND>
        <COMMAND>Flash(point, color=...)</COMMAND>
        <COMMAND>FocusOn(mobject)</COMMAND>
        
        <COMMAND>AnimationGroup(anim_1, anim_2, lag_ratio=...)</COMMAND>
        <COMMAND>LaggedStart(anim_1, anim_2, lag_ratio=...)</COMMAND>
        <COMMAND>Succession(anim_1, anim_2, ...)</COMMAND>
    </SECTION>

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

    <SECTION NAME="Mobject Creation">
        <COMMAND>Circle(radius=...)</COMMAND>
        <COMMAND>Square(side_length=...)</COMMAND>
        <COMMAND>Rectangle(width=..., height=...)</COMMAND>
        <COMMAND>Polygon(p1, p2, p3, ...)</COMMAND>
        <COMMAND>Triangle()</COMMAND>
        <COMMAND>Arc(radius=..., start_angle=..., angle=...)</COMMAND>
        <COMMAND>Dot(point=...)</COMMAND>
        <COMMAND>VGroup(mobject_1, mobject_2, ...)</COMMAND>

        <COMMAND>Line(start, end)</COMMAND>
        <COMMAND>DashedLine(start, end)</COMMAND>
        <COMMAND>Arrow(start, end, buff=...)</COMMAND>
        <COMMAND>DoubleArrow(start, end)</COMMAND>
        <COMMAND>Vector(direction)</COMMAND>
        
        <COMMAND>Text(str(text))</COMMAND> <COMMAND>MathTex(r"latex_string")</COMMAND>
        
        <COMMAND>Axes(x_range=..., y_range=..., ...)</COMMAND>
        <COMMAND>NumberLine(x_range=...)</COMMAND>
        <COMMAND>BarChart(values=..., ...)</COMMAND>
        <COMMAND>axes.plot(lambda_func, x_range=...)</COMMAND>
        <COMMAND>axes.get_graph(lambda_func, x_range=...)</COMMAND>
        
        <COMMAND>SurroundingRectangle(mobject, buff=...)</COMMAND>
        <COMMAND>Brace(mobject, direction=...)</COMMAND>
        <COMMAND>SVGMobject("path/to/file.svg")</COMMAND>
        <COMMAND>VMobject()</COMMAND>
    </SECTION>

    <SECTION NAME="Common Mobject Utility Methods">
        <COMMAND>mobject.move_to(point_or_mobject)</COMMAND>
        <COMMAND>mobject.shift(DIRECTION)</COMMAND>
        <COMMAND>mobject.scale(value)</COMMAND>
        <COMMAND>mobject.next_to(mobject, DIRECTION, buff=...)</COMMAND>
        <COMMAND>mobject.align_to(mobject, DIRECTION)</COMMAND>
        <COMMAND>mobject.to_edge(DIRECTION)</COMMAND>
        <COMMAND>mobject.to_corner(DIRECTION)</COMMAND>

        <COMMAND>mobject.set_color(COLOR)</COMMAND>
        <COMMAND>mobject.set_fill(color=..., opacity=...)</COMMAND>
        <COMMAND>mobject.set_stroke(color=..., width=..., opacity=...)</COMMAND>
        <COMMAND>mobject.set_opacity(value)</COMMAND>
        <COMMAND>mobject.set_stroke(stroke_dasharray=[...])</COMMAND>

        <COMMAND>vgroup.arrange(DIRECTION, buff=...)</COMMAND>
        <COMMAND>vgroup.arrange_in_grid(rows=..., cols=..., buff=...)</COMMAND>

        <COMMAND>mobject.get_center()</COMMAND>
        <COMMAND>mobject.get_width()</COMMAND>
        <COMMAND>mobject.get_height()</COMMAND>
        <COMMAND>mobject.get_corner(DIRECTION)</COMMAND>
        <COMMAND>mobject.get_edge_center(DIRECTION)</COMMAND>
        
        <COMMAND>vmobject.set_points_as_corners([...])</COMMAND>
    </SECTION>
    
    <SECTION NAME="Other">
        **Colors are STRINGS:**
        BLUE = "#58C4DD"
        GREEN = "#8BE17D"
        RED = "#FF6188"
        ... (etc)

        **Constants:**
        ✅ ORIGIN, UP, DOWN, LEFT, RIGHT, PI, TAU
        ❌ CENTER - use ORIGIN

        **Modules:**
        ✅ np.random.X, np.cos, np.sin
        ❌ random.X, math.X, scipy, betainc
    </SECTION>
**BANNED COMMANDS (DO NOT USE - THEY CRASH):**
❌ self.play(self.camera.animate...)
❌ self.play(self.camera.frame.animate...)
❌ self.play(self.camera.frame_center.animate...)
❌ self.move_camera(...)
❌ self.set_camera_orientation(...)

**AESTHETIC POLISH (USE THESE!):**
* Secondary Motion: Don't just FadeIn. Use FadeIn(obj, shift=DOWN*0.3)
* Lagging: Don't just Write(text). Use Write(text, lag_ratio=0.1)
* Pacing: Don't just Transform(a, b). Use Transform(a, b, rate_func=smooth)
* Emphasis: Add extra self.play(Indicate(obj)) calls after creation.

### 🔧 NEW FIX ###
**Vector Shapes (VMobject) vs. SVGs (SVGMobject):**
* To create a custom shape from points (like a thought bubble):
    ✅ `my_shape = VMobject().set_points_as_corners([...])`
    ✅ `my_shape = Polygon(p1, p2, p3, ...)`
* To load an SVG file from disk:
    ✅ `my_icon = SVGMobject("path/to/icon.svg")`
* **CRITICAL:** Do NOT mix them.
    ❌ `SVGMobject().set_points_as_corners(...)` (CRASHES: ValueError)
    **Styling VMobjects:**
    * To set fill and stroke (color, width, opacity):
        ✅ `obj.set_fill(color=BLUE, opacity=0.5)`
        ✅ `obj.set_stroke(color=RED, width=4, opacity=0.8)`
    * To make a line dashed:
        ✅ `obj.set_stroke(stroke_dasharray=[8, 4])`
        ✅ `obj = DashedLine(p1, p2)`
    * CRASHES:
        ❌ `obj.set_style(stroke_dasharray=[...])` (TypeError)


**Colors are STRINGS:**
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

**Constants:**
✅ ORIGIN, UP, DOWN, LEFT, RIGHT, PI, TAU
❌ CENTER - use ORIGIN

**Modules:**
✅ np.random.X, np.cos, np.sin
❌ random.X, math.X, scipy, betainc
"""
    
    def _build_error_database(self) -> str:
        return """
COMMON ERRORS:

1. Empty voiceover → ZeroDivisionError
2. interpolate_color(BLUE, RED) → AttributeError 'str'
3. betainc → NameError
4. CENTER → NameError (use ORIGIN)
5. self.camera.frame.animate → AttributeError: 'Camera' object has no attribute 'frame'
6. self.camera.animate → AttributeError: 'Camera' object has no attribute 'animate'
7. self.move_camera → AttributeError: object has no attribute 'move_camera'
8. self.camera.frame_center.animate → AttributeError: 'numpy.ndarray' object has no attribute 'animate'
9. .get_angle() → AttributeError
10. random.X → NameError (use np.random.X)
11. math.X → NameError (use np.X)
12. IndexError on nested access (e.g., obj[0][1][i]) → Check structure first!
13. .restore() without .save_state() → Exception

---
CRITICAL ERRORS (MUST BE REMOVED):
---
14. class ... (e.g., class MyScene(VoiceoverScene):)
15. def construct(self):
16. import ...
17. from ... import ...

---
QUALITY ERRORS (MUST BE FIXED):
---
18. Animation Sparsity: Code has very few animations for a multi-sentence narration
19. Synchronization Error: Found only one with self.voiceover block for a long scene
20. Missing Tracker: A self.play call inside a voiceover block is missing run_time=tracker.duration
"""
    
    def _build_examples(self) -> str:
        return """
WORKING PATTERNS:

Particles:
`````python
VGroup(*[Dot(ORIGIN + np.array([np.random.normal(0, 0.5), np.random.normal(0, 0.5), 0]),
         radius=0.02, color=BLUE).set_opacity(0.7)
     for _ in range(100)])
`````

Transform:
`````python
circle = Circle(radius=1, color=BLUE)
square = Square(side_length=2, color=RED)
self.play(Transform(circle, square), run_time=2, rate_func=smooth)
`````
"""

    def generate_video_file(self, video: Video, output_path: Path) -> str:
        print(f"\n{'='*60}")
        print(f"  {video.title}")
        print(f"{'='*60}\n")
        
        all_scenes = []
        
        for scene in video.scenes:
            print(f"  Scene {scene.id}/{len(video.scenes)}: {scene.title}")
            print(f"    🎬", end="", flush=True)
            
            code = self._generate_perfect_scene(scene)
            print(" ✅")
            
            all_scenes.append(code)
        
        full_code = self._wrap(video, all_scenes)
        
        filepath = output_path / f"video{video.number}.py"
        filepath.write_text(full_code)
        
        print(f"\n  🚀 COMPLETE: video{video.number}.py\n")
        return str(filepath)

    def _generate_perfect_scene(self, scene: Scene) -> str:
        for iteration in range(6):
            print(".", end="", flush=True)
            
            if iteration == 0:
                code = self._initial_generation(scene)
            else:
                code = self._fix_code(code, issues, scene)
            
            print(".", end="", flush=True)
            issues = self._validate_code(code, scene)
            
            if not issues or "PERFECT" in issues:
                return self._final_cleanup(code)
        
        print("!", end="", flush=True)
        return self._final_cleanup(self._emergency_fix(scene))

    def _final_cleanup(self, code: str) -> str:
        code = re.sub(r'^```(python)?\n', '', code, flags=re.MULTILINE)
        code = re.sub(r'\n```$', '', code, flags=re.MULTILINE)
        
        cleaned_lines = []
        for line in code.split('\n'):
            stripped_line = line.strip()
            if (
                not stripped_line.startswith('class ') and
                not stripped_line.startswith('def construct(self):') and
                not stripped_line.startswith('import ') and
                not stripped_line.startswith('from ')
            ):
                cleaned_lines.append(line)
                
        return '\n'.join(cleaned_lines).strip()

    def _initial_generation(self, scene: Scene) -> str:
        """Generate with 3Blue1Brown philosophy"""
        
        prompt = f"""Generate Manim 0.18.1 scene code.
{self.manim_api}
{self.examples}

<scene>
Title: {scene.title}
Full Narration (for context, DO NOT USE in a single block): {scene.narration}
Visual Beats (Use these as your primary instructions): {scene.visual_instructions}
</scene>

═══════════════════════════════════════════════════════════
🎬 3BLUE1BROWN VISUAL INTUITION ENGINE
═══════════════════════════════════════════════════════════

CRITICAL WORKFLOW: 📜 PARSE, SYNC, AND POLISH 🎬

This is the most important rule. You will be given 'Visual Beats' as a list of "Narration" and "Visual" comments. For EACH "Narration" comment, you MUST:

1. SYNC: Create a NEW with self.voiceover(text="...") block using the narration text from the comment.
2. POLISH & ANIMATE: Use the "Visual" comment as your instruction, but make it better.
3. ADD POLISH: Do not just run the visual_command. Add secondary motion, better rate functions, or emphasis.
   - Instead of FadeIn(obj), use FadeIn(obj, shift=DOWN*0.3).
   - Instead of Write(obj), use Write(obj, lag_ratio=0.1).
   - Instead of Transform(a, b), use Transform(a, b, rate_func=smooth).
   - Add Indicate(obj, color=YELLOW) or Circumscribe(obj) to emphasize.
4. USE TRACKER: Add run_time=tracker.duration to your main self.play() call inside the voiceover block to sync the animation to the audio.
5.U must go all out while imaginations of the animations dont hold back at all do whatever u can or is needed 
6.dont overlap and hallucinate i repeat do not overlap and be very very aptwht animations check twice or thrice use as much tokens as u want but be perfect
SUCCESS EXAMPLE:
7.pLease when using all_elements dont use Vgroup use group 
8.for using the Star never use n<5 please prefer n=5
`````python
if self.mobjects: self.play(*[FadeOut(obj) for obj in self.mobjects], run_time=0.5)

# Narration: "First, we initialize a set of particles..."
# Visual: Create 100 particles
with self.voiceover(text="First, we initialize a set of particles...") as tracker:
    particles = VGroup(*[Dot() for _ in range(100)]).arrange_in_grid(10, 10)
    # POLISH: Added lag_ratio and shift. SYNC: Added tracker.duration.
    self.play(FadeIn(particles, lag_ratio=0.01, shift=UP*0.2), run_time=tracker.duration)
    
# Narration: "...which represent our data points in a high-dimensional space."
# Visual: Color them blue
with self.voiceover(text="which represent our data points in a high-dimensional space.") as tracker:
    # POLISH: Added a secondary 'Indicate' animation.
    self.play(particles.animate.set_color(BLUE), run_time=tracker.duration)
    self.play(Indicate(particles, color=BLUE, scale_factor=1.1), run_time=1.0) 

self.wait(2)
`````

REQUIREMENTS:
- Start: if self.mobjects: self.play(*[FadeOut(obj) for obj in self.mobjects], run_time=0.5)
- Loop the Beats: You must create a separate with self.voiceover(...) block for each "Narration" comment in Visual Beats.
- Use Tracker: Always use run_time=tracker.duration.
- Add Polish: Always add secondary animations.
- End: self.wait(2)

Bad Code: dont use like this all_elements = VGroup(*self.mobjects)

Correct Code: all_elements = Group(*self.mobjects)
ANTI-REQUIREMENTS (DO NOT INCLUDE THESE):
- ❌ DO NOT write import ..., from ..., class ..., or def construct(self):.
- ❌ DO NOT use BANNED CAMERA COMMANDS (self.camera.animate, self.move_camera, etc.)
- ❌ DO NOT wrap the entire scene in one voiceover block using scene.narration.
i repeat do not use all_elements=Vgroup use Group instead imma smack u
Generate ONLY the body of the scene code, following the PARSE, SYNC, AND POLISH workflow.
`````python
"""

        response = self.client.messages.create(
            model=cfg.MODEL,
            max_tokens=12000,
            temperature=0.35,
            messages=[{"role": "user", "content": prompt}]
        )
        
        code = response.content[0].text
        match = re.search(r'```(?:python)?\n(.*?)\n```', code, re.DOTALL)
        if match:
            return match.group(1)
        return code.split('```python')[-1].split('```')[0].strip()
    
    def _validate_code(self, code: str, scene: Scene) -> str:
        """Validate against known patterns"""
        
        # Count sentences/beats
        num_beats = scene.visual_instructions.count("# Narration:")
        if num_beats == 0:
            num_beats = 5  # Fallback
            
        num_voiceover_blocks = code.count("with self.voiceover")
        num_tracker_uses = code.count("run_time=tracker.duration")

        sync_check_str = f"Scene has {num_beats} beats."
        if num_voiceover_blocks < num_beats * 0.8:  # Allow for 20% margin
            sync_check_str += f" -> ERROR: Not enough voiceover blocks. Found {num_voiceover_blocks}."
        elif num_voiceover_blocks == 1 and num_beats > 2:
            sync_check_str += f" -> ERROR: Only one voiceover block found for a multi-beat scene. This is wrong."
        elif num_tracker_uses < num_voiceover_blocks * 0.7:  # Allow for some blocks not having animations
            sync_check_str += f" -> ERROR: Missing run_time=tracker.duration. Found {num_voiceover_blocks} blocks but only {num_tracker_uses} tracker uses."
        else:
            sync_check_str += f" -> OK. Found {num_voiceover_blocks} voiceover blocks and {num_tracker_uses} tracker uses."

        prompt = f"""Validate this Manim code block.
{self.error_database}
{self.manim_api}

**Scene Context:**
{sync_check_str}

<code>
{code}
</code>

**Check for ALL of these errors:**

**CRITICAL ERRORS (Generation-breaking):**
1. class ...
2. def construct(self):
3. import ...
4. from ... import ...

**QUALITY ERRORS (Must be fixed):**
5. Synchronization Error: Check the context above. If it says 'ERROR', then list "Synchronization Error" as an issue.
6. Sparsity: Does the code have very few self.play calls? (e.g., < {num_beats})

**MANIM ERRORS (Syntax-breaking):**
7. Empty voiceover text (e.g., text="")
8. BANNED CAMERA COMMANDS: self.camera.frame.animate, self.camera.animate, self.move_camera
9. CENTER (must use ORIGIN)
10. IndexError risks: obj[0][1][i] without checks
11. .restore() without .save_state()

**Response:**
If NO errors are found (code is clean and passes all checks), respond with ONLY the word "PERFECT".
If ANY errors are found, list ALL of them clearly.
"""

        response = self.client.messages.create(
            model=cfg.MODEL,
            max_tokens=2048,
            temperature=0.0,
            messages=[{"role": "user", "content": prompt}]
        )
        
        return response.content[0].text.strip()
    
    def _fix_code(self, code: str, issues: str, scene: Scene) -> str:
        """Fix issues"""
        
        prompt = f"""Fix ALL issues in the Manim code.
{self.manim_api}
{self.error_database}

<bad_code>
{code}
</bad_code>

<issues>
{issues}
</issues>

<scene_visual_beats>
{scene.visual_instructions}
</scene_visual_beats>

**Instructions:**
1. Fix every issue listed in <issues>.
2. IF 'Synchronization Error' IS AN ISSUE: This is the TOP priority. You MUST rewrite the code to follow the 'PARSE, SYNC, AND POLISH' workflow.
   - Look at <scene_visual_beats>.
   - For EACH # Narration: "..." comment:
     a. Create a NEW with self.voiceover(text="...") block using that narration text.
     b. Put the animation code for that beat inside this new block.
     c. Add run_time=tracker.duration to the main self.play() call.
     d. Add polish (shifts, lag_ratios, etc.) as per the manim_api examples.
3. CRITICAL: REMOVE any class ..., def construct(self):, import ..., or from ... lines.
4. BANNED CAMERA: Do not use self.camera.animate, self.camera.frame.animate, or self.move_camera. Use obj.animate.scale() instead.
5. The result MUST be ONLY the code that goes inside the construct method.
6.Also critically ban interpolate colour do not use any kind of colour interpolation revert back to one colour its fine okay

Generate ONLY the fixed Python code body, following the 'PARSE, SYNC, AND POLISH' workflow.
````python
"""

        response = self.client.messages.create(
            model=cfg.MODEL,
            max_tokens=12000,
            temperature=0.15,
            messages=[{"role": "user", "content": prompt}]
        )
        
        fixed = response.content[0].text
        match = re.search(r'```(?:python)?\n(.*?)\n```', fixed, re.DOTALL)
        if match:
            return match.group(1)
        return fixed.split('```python')[-1].split('```')[0].strip()
    
    def _emergency_fix(self, scene: Scene) -> str:
        prompt = f"""Rewrite scene code from scratch.
{self.examples}
{self.manim_api}

<scene>
Title: {scene.title}
Visual Beats:
{scene.visual_instructions}
</scene>

**Instructions:**
1. CRITICAL: You MUST follow the 'PARSE, SYNC, AND POLISH' workflow.
   - For EACH # Narration: "..." comment:
   - Create a NEW with self.voiceover(text="...") block.
   - Create a polished animation (e.g., FadeIn(..., shift=...)) inside it.
   - Use run_time=tracker.duration on the self.play() call.
2. Use ONLY safe patterns.
3. DO NOT write class, def construct, import, or from.
4. DO NOT use banned camera commands.
5. Generate ONLY the code for the body of the construct method.
```python
"""

        response = self.client.messages.create(
            model=cfg.MODEL,
            max_tokens=12000,
            temperature=0.2,
            messages=[{"role": "user", "content": prompt}]
        )
        
        code = response.content[0].text
        match = re.search(r'```(?:python)?\n(.*?)\n```', code, re.DOTALL)
        if match:
            return match.group(1)
        return code.split('```python')[-1].split('```')[0].strip()
    
    def _wrap(self, video: Video, scenes: List[str]) -> str:
        header = '''from manim import *
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
'''
        
        body = f'''
class Video{video.number}(VoiceoverScene):
    def construct(self):
        # Set up speech service *once*
        self.set_speech_service(
            ElevenLabsService(
                api_key=os.getenv("ELEVENLABS_API_KEY"),
                voice_id="s3TPKV1kjDlVtZbl4Ksh",
                model="eleven_turbo_v2_5"
            )
        )
        # Set background color *once*
        self.camera.background_color = "#000000"
'''
        
        for i, scene_code in enumerate(scenes, 1):
            body += f'\n        # {"="*58}\n'
            body += f'        # SCENE {i}: {video.scenes[i-1].title}\n'
            body += f'        # {"="*58}\n'
            
            for line in scene_code.split('\n'):
                if line.strip():
                    body += f'        {line}\n'
            body += "\n"
        
        return header + body