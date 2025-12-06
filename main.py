from manim import *
import numpy as np

config.quality = "high_quality"  # 720p30 - faster rendering
config.frame_rate = 60  # Reduced from 60 for faster rendering
# For even faster testing, use: config.quality = "low_quality"  # 480p15
# To render: manim -pql main.py AccelerometerFull
# -p = preview (opens video when done)
# -ql = low quality (fastest)
# -qm = medium quality (balanced)
# -qh = high quality (slowest, best quality)


class AccelerometerFull(ThreeDScene):
    """
    Educational Accelerometer visualization (~30s).
    Clear cause-and-effect: one axis moves at a time, corresponding graph responds.
    
    Scenes:
    - [0-5s]   Introduction: Static device, Z at -1g (gravity)
    - [5-11s]  X-Axis Demo: Slide LEFT/RIGHT, only X graph spikes
    - [11-17s] Y-Axis Demo: Slide UP/DOWN, only Y graph spikes
    - [17-23s] Z-Axis Demo: Tilt device, Z changes (gravity redistribution)
    - [23-30s] Combined + Summary
    """
    
    def construct(self):
        # === CAMERA & BACKGROUND ===
        self.set_camera_orientation(phi=65 * DEGREES, theta=-45 * DEGREES)
        self.camera.background_color = BLACK
        
        # ============================================================
        # SECTION 1: CREATE ALL PERSISTENT ELEMENTS
        # ============================================================
        
        # === COLOR PALETTE (color-blind friendly) ===
        palette = {
            "x": "#4477AA",  # deep blue
            "y": "#CCBB44",  # golden yellow
            "z": "#66CCEE",  # sky blue
        }
        
        # === TITLE ===
        title = Text("Accelerometer", font_size=36, weight=BOLD, color=WHITE)
        title.to_edge(UP, buff=0.25)
        
        # === 3D CUBE ===
        cube = Cube(side_length=1.5, fill_opacity=0.12, stroke_width=2.5)
        cube.set_fill(BLUE_E, opacity=0.12)
        cube.set_stroke(WHITE, width=2.5)
        
        # === 3D AXES (THICKER ARROWS) ===
        axis_length = 1.4
        axis_thickness = 0.045
        
        x_axis = Arrow3D(ORIGIN, RIGHT * axis_length, color=palette["x"], thickness=axis_thickness, height=0.24, base_radius=0.08)
        y_axis = Arrow3D(ORIGIN, UP * axis_length, color=palette["y"], thickness=axis_thickness, height=0.24, base_radius=0.08)
        z_axis = Arrow3D(ORIGIN, OUT * axis_length, color=palette["z"], thickness=axis_thickness, height=0.24, base_radius=0.08)
        
        x_label = Text("X", font_size=20, color=palette["x"], weight=BOLD)
        x_label.rotate(PI/2, axis=RIGHT)
        x_label.next_to(x_axis.get_end(), RIGHT, buff=0.08)
        
        y_label = Text("Y", font_size=20, color=palette["y"], weight=BOLD)
        y_label.rotate(PI/2, axis=RIGHT)
        y_label.next_to(y_axis.get_end(), UP, buff=0.08)
        
        z_label = Text("Z", font_size=20, color=palette["z"], weight=BOLD)
        z_label.rotate(PI/2, axis=RIGHT)
        z_label.next_to(z_axis.get_end(), OUT, buff=0.08)
        
        axes_group = VGroup(x_axis, y_axis, z_axis, x_label, y_label, z_label)
        
        # === GROUP ACCELEROMETER ===
        accel_group = VGroup(cube, axes_group)
        accel_center = LEFT * 3.8
        accel_group.move_to(accel_center)
        
        # === LIVE GRAPHS ===
        graph_y_positions = [1.6, 0, -1.6]
        graph_colors = [palette["x"], palette["y"], palette["z"]]
        graph_names = ["X", "Y", "Z"]
        
        graph_axes_list = []
        graph_groups = []
        
        for i, (y_pos, color, name) in enumerate(zip(graph_y_positions, graph_colors, graph_names)):
            axes = Axes(
                x_range=[0, 5, 1],
                y_range=[-2.5, 1.5, 1],
                x_length=4.5,
                y_length=1.2,
                axis_config={
                    "stroke_width": 1.2,
                    "stroke_color": "#4a5568",
                    "include_numbers": False,
                    "include_tip": False,
                },
            )
            axes.shift(RIGHT * 3.6 + UP * y_pos)
            
            # Grid lines
            grid = VGroup()
            for yv in [-2, -1, 0, 1]:
                gl = Line(axes.c2p(0, yv), axes.c2p(5, yv), color="#2d3748", stroke_width=0.5, stroke_opacity=0.4)
                grid.add(gl)
            
            # Y labels
            y_labels = VGroup(
                Text("-2g", font_size=9, color="#718096"),
                Text("-1g", font_size=9, color="#718096"),
                Text("0", font_size=9, color="#718096"),
                Text("+1g", font_size=9, color="#718096"),
            )
            y_labels[0].next_to(axes.c2p(0, -2), LEFT, buff=0.05)
            y_labels[1].next_to(axes.c2p(0, -1), LEFT, buff=0.05)
            y_labels[2].next_to(axes.c2p(0, 0), LEFT, buff=0.05)
            y_labels[3].next_to(axes.c2p(0, 1), LEFT, buff=0.05)
            
            # Axis indicator
            axis_dot = Dot(radius=0.05, color=color)
            axis_name = Text(name, font_size=14, color=color, weight=BOLD)
            axis_indicator = VGroup(axis_dot, axis_name).arrange(RIGHT, buff=0.06)
            axis_indicator.next_to(axes, LEFT, buff=0.3)
            
            graph_group = VGroup(axes, grid, y_labels, axis_indicator)
            graph_axes_list.append(axes)
            graph_groups.append(graph_group)
        
        # ============================================================
        # SECTION 2: FIX 2D ELEMENTS TO FRAME
        # ============================================================
        self.add_fixed_in_frame_mobjects(title)
        for g in graph_groups:
            self.add_fixed_in_frame_mobjects(g)
        
        # ============================================================
        # HELPER: Create graph line for given data
        # ============================================================
        def create_graph_line(data, axes, color):
            samples = len(data)
            t_vals = np.linspace(0, 5, samples)
            points = [axes.c2p(t_vals[j], data[j]) for j in range(samples)]
            line = VMobject(color=color, stroke_width=2.5)
            line.set_points_smoothly(points[::2])
            self.add_fixed_in_frame_mobjects(line)
            return line
        
        def create_animated_graph_line(data, axes, color, progress_tracker):
            """Create a line that draws based on progress_tracker value (0 to 1)"""
            samples_count = len(data)
            t_vals = np.linspace(0, 5, samples_count)
            all_points = [axes.c2p(t_vals[j], data[j]) for j in range(samples_count)]
            
            line = VMobject(color=color, stroke_width=2.5)
            self.add_fixed_in_frame_mobjects(line)
            
            def update_line(mob):
                progress = progress_tracker.get_value()
                num_points = max(2, int(progress * len(all_points)))
                points_to_draw = all_points[:num_points]
                if len(points_to_draw) >= 2:
                    mob.set_points_smoothly(points_to_draw[::2] if len(points_to_draw) > 4 else points_to_draw)
            
            line.add_updater(update_line)
            return line
        
        # ============================================================
        # SCENE 1: INTRODUCTION - STATIC DEVICE (0-5s)
        # ============================================================
        
        intro_text = Text("Device at Rest (Gravity on Z)", font_size=20, color="#9ca3af")
        intro_text.next_to(title, DOWN, buff=0.15)
        self.add_fixed_in_frame_mobjects(intro_text)
        
        # Fade in
        self.play(
            FadeIn(cube, scale=0.9),
            FadeIn(title),
            FadeIn(intro_text),
            run_time=1.2
        )
        self.play(Create(axes_group), run_time=0.8)
        self.play(*[FadeIn(g) for g in graph_groups], run_time=0.8)
        
        # Static signal: Z at -1g, X/Y flat
        samples = 100  # Reduced from 100 for faster rendering
        x_static = np.zeros(samples)
        y_static = np.zeros(samples)
        z_static = -1.0 * np.ones(samples)
        
        static_lines = [
            create_graph_line(x_static, graph_axes_list[0], palette["x"]),
            create_graph_line(y_static, graph_axes_list[1], palette["y"]),
            create_graph_line(z_static, graph_axes_list[2], palette["z"]),
        ]
        
        self.play(*[Create(line, run_time=1.2) for line in static_lines], rate_func=linear)
        self.wait(0.8)
        
        # ============================================================
        # SCENE 2: X-AXIS DEMO - SLIDE LEFT/RIGHT (5-11s)
        # ============================================================
        
        self.play(*[FadeOut(line) for line in static_lines], FadeOut(intro_text), run_time=0.3)
        
        x_demo_text = Text("X-Axis: Slide Left ← → Right", font_size=20, color=palette["x"])
        x_demo_text.next_to(title, DOWN, buff=0.15)
        self.add_fixed_in_frame_mobjects(x_demo_text)
        self.play(FadeIn(x_demo_text), run_time=0.4)
        
        # Highlight X-axis
        self.play(x_axis.animate.set_color(WHITE), run_time=0.15)
        self.play(x_axis.animate.set_color(palette["x"]), run_time=0.15)
        
        # Save state for clean restoration
        accel_group.save_state()
        
        # X movement data - SIMPLE SINUSOIDAL MOVEMENT
        t_x = np.linspace(0, 5, samples)
        # Simple sinusoidal acceleration pattern
        frequency = 0.8  # cycles per 5 seconds
        amplitude = 1.2
        x_data = amplitude * np.sin(2 * PI * frequency * t_x)
        
        y_data = np.zeros(samples)
        z_data = -1.0 * np.ones(samples)
        
        # Create progress tracker for synchronized graph drawing
        x_progress = ValueTracker(0)
        
        x_line = create_animated_graph_line(x_data, graph_axes_list[0], palette["x"], x_progress)
        y_line = create_animated_graph_line(y_data, graph_axes_list[1], palette["y"], x_progress)
        z_line = create_animated_graph_line(z_data, graph_axes_list[2], palette["z"], x_progress)
        
        # Animate cube sliding with graph - synchronized sinusoidal movement
        slide_distance = 1.5
        
        # Remove the static cube and axes from scene (they were added separately)
        self.remove(cube, axes_group)
        
        # Create a function that returns cube at correct position
        def get_moving_cube():
            progress = x_progress.get_value()
            t = progress * 5
            position = slide_distance * np.sin(2 * PI * frequency * t)
            target_pos = accel_center + RIGHT * position
            return accel_group.copy().move_to(target_pos)
        
        # Use always_redraw to create cube that updates every frame
        moving_cube = always_redraw(get_moving_cube)
        self.add(moving_cube)
        
        # Animate progress - cube will update automatically via always_redraw
        self.play(
            x_progress.animate.set_value(1.0),
            run_time=5.0,
            rate_func=linear
        )
        
        # Clean up - restore original cube
        self.remove(moving_cube)
        accel_group.move_to(accel_center)
        self.add(cube, axes_group)
        
        # Remove updaters and finalize lines
        x_line.clear_updaters()
        y_line.clear_updaters()
        z_line.clear_updaters()
        
        accel_group.restore()
        accel_group.move_to(accel_center)
        self.wait(0.4)
        
        # ============================================================
        # SCENE 3: Y-AXIS DEMO - SLIDE UP/DOWN (11-17s)
        # ============================================================
        
        self.play(
            *[FadeOut(line) for line in [x_line, y_line, z_line]],
            FadeOut(x_demo_text),
            run_time=0.3
        )
        
        y_demo_text = Text("Y-Axis: Slide Up ↑ ↓ Down", font_size=20, color=palette["y"])
        y_demo_text.next_to(title, DOWN, buff=0.15)
        self.add_fixed_in_frame_mobjects(y_demo_text)
        self.play(FadeIn(y_demo_text), run_time=0.4)
        
        # Highlight Y-axis
        self.play(y_axis.animate.set_color(WHITE), run_time=0.15)
        self.play(y_axis.animate.set_color(palette["y"]), run_time=0.15)
        
        accel_group.save_state()
        
        # Y movement data - SIMPLE SINUSOIDAL MOVEMENT
        t_y = np.linspace(0, 5, samples)
        # Simple sinusoidal acceleration pattern
        frequency = 0.8  # cycles per 5 seconds
        amplitude = 1.2
        x_data_y = np.zeros(samples)
        y_data_y = amplitude * np.sin(2 * PI * frequency * t_y)
        
        z_data_y = -1.0 * np.ones(samples)
        
        # Create progress tracker for synchronized graph drawing
        y_progress = ValueTracker(0)
        
        x_line2 = create_animated_graph_line(x_data_y, graph_axes_list[0], palette["x"], y_progress)
        y_line2 = create_animated_graph_line(y_data_y, graph_axes_list[1], palette["y"], y_progress)
        z_line2 = create_animated_graph_line(z_data_y, graph_axes_list[2], palette["z"], y_progress)
        
        # Animate cube sliding with graph - synchronized sinusoidal movement
        slide_distance = 1.5
        
        # Remove the static cube and axes from scene (they were added separately)
        self.remove(cube, axes_group)
        
        # Create a function that returns cube at correct position
        def get_moving_cube_y():
            progress = y_progress.get_value()
            t = progress * 5
            position = slide_distance * np.sin(2 * PI * frequency * t)
            target_pos = accel_center + UP * position
            return accel_group.copy().move_to(target_pos)
        
        # Use always_redraw to create cube that updates every frame
        moving_cube = always_redraw(get_moving_cube_y)
        self.add(moving_cube)
        
        # Animate progress - cube will update automatically via always_redraw
        self.play(
            y_progress.animate.set_value(1.0),
            run_time=5.0,
            rate_func=linear
        )
        
        # Clean up - restore original cube
        self.remove(moving_cube)
        accel_group.move_to(accel_center)
        self.add(cube, axes_group)
        
        # Remove updaters
        x_line2.clear_updaters()
        y_line2.clear_updaters()
        z_line2.clear_updaters()
        
        accel_group.restore()
        accel_group.move_to(accel_center)
        self.wait(0.4)
        
        # ============================================================
        # SCENE 4: Z-AXIS DEMO - TILT (Gravity Redistribution) (17-23s)
        # ============================================================
        
        self.play(
            *[FadeOut(line) for line in [x_line2, y_line2, z_line2]],
            FadeOut(y_demo_text),
            run_time=0.3
        )
        
        z_demo_text = Text("Z-Axis: Move Up ↑ ↓ Down", font_size=20, color=palette["z"])
        z_demo_text.next_to(title, DOWN, buff=0.15)
        self.add_fixed_in_frame_mobjects(z_demo_text)
        self.play(FadeIn(z_demo_text), run_time=0.4)
        
        # Highlight Z-axis
        self.play(z_axis.animate.set_color(WHITE), run_time=0.15)
        self.play(z_axis.animate.set_color(palette["z"]), run_time=0.15)
        
        accel_group.save_state()
        
        # Z movement data - SIMPLE SINUSOIDAL MOVEMENT
        # Gravity always contributes -1g baseline on Z
        t_z = np.linspace(0, 5, samples)
        frequency = 0.8  # cycles per 5 seconds
        amplitude = 1.0
        x_data_z = np.zeros(samples)
        y_data_z = np.zeros(samples)
        # Simple sinusoidal variation on top of gravity baseline
        z_data_z = -1.0 + amplitude * np.sin(2 * PI * frequency * t_z)
        
        # Create progress tracker for synchronized graph drawing
        z_progress = ValueTracker(0)
        
        x_line3 = create_animated_graph_line(x_data_z, graph_axes_list[0], palette["x"], z_progress)
        y_line3 = create_animated_graph_line(y_data_z, graph_axes_list[1], palette["y"], z_progress)
        z_line3 = create_animated_graph_line(z_data_z, graph_axes_list[2], palette["z"], z_progress)
        
        # Animate cube sliding with graph - synchronized sinusoidal movement
        slide_distance = 1.5
        
        # Remove the static cube and axes from scene (they were added separately)
        self.remove(cube, axes_group)
        
        # Create a function that returns cube at correct position
        def get_moving_cube_z():
            progress = z_progress.get_value()
            t = progress * 5
            position = slide_distance * np.sin(2 * PI * frequency * t)
            target_pos = accel_center + OUT * position
            return accel_group.copy().move_to(target_pos)
        
        # Use always_redraw to create cube that updates every frame
        moving_cube = always_redraw(get_moving_cube_z)
        self.add(moving_cube)
        
        # Animate progress - cube will update automatically via always_redraw
        self.play(
            z_progress.animate.set_value(1.0),
            run_time=5.0,
            rate_func=linear
        )
        
        # Clean up - restore original cube
        self.remove(moving_cube)
        accel_group.move_to(accel_center)
        self.add(cube, axes_group)
        
        # Remove updaters
        x_line3.clear_updaters()
        y_line3.clear_updaters()
        z_line3.clear_updaters()
        
        accel_group.restore()
        accel_group.move_to(accel_center)
        self.wait(0.4)
        
        # ============================================================
        # SCENE 5: COMBINED MOTION + SUMMARY (23-30s)
        # ============================================================
        
        self.play(
            *[FadeOut(line) for line in [x_line3, y_line3, z_line3]],
            FadeOut(z_demo_text),
            run_time=0.3
        )
        
        combined_text = Text("Combined Motion: All Axes Respond", font_size=20, color="#a855f7")
        combined_text.next_to(title, DOWN, buff=0.15)
        self.add_fixed_in_frame_mobjects(combined_text)
        self.play(FadeIn(combined_text), run_time=0.4)
        
        # Combined movement data - realistic acceleration spikes
        # Simulate quick movements in different directions
        x_comb = np.zeros(samples)
        y_comb = np.zeros(samples)
        z_comb = -1.0 * np.ones(samples)
        
        # X quick shake (accel/decel pairs)
        x_comb[5:10] = -0.8 * np.sin(np.linspace(0, PI, 5))
        x_comb[10:15] = 0.8 * np.sin(np.linspace(0, PI, 5))
        x_comb[20:25] = 0.8 * np.sin(np.linspace(0, PI, 5))
        x_comb[25:30] = -0.8 * np.sin(np.linspace(0, PI, 5))
        
        # Y quick movements
        y_comb[35:40] = -0.6 * np.sin(np.linspace(0, PI, 5))
        y_comb[40:45] = 0.6 * np.sin(np.linspace(0, PI, 5))
        
        # Z quick movements (on top of gravity)
        z_comb[55:60] = -1.0 - 0.5 * np.sin(np.linspace(0, PI, 5))
        z_comb[60:65] = -1.0 + 0.5 * np.sin(np.linspace(0, PI, 5))
        z_comb[70:75] = -1.0 + 0.5 * np.sin(np.linspace(0, PI, 5))
        z_comb[75:80] = -1.0 - 0.5 * np.sin(np.linspace(0, PI, 5))
        
        # Create progress tracker for synchronized graph drawing
        comb_progress = ValueTracker(0)
        
        x_line4 = create_animated_graph_line(x_comb, graph_axes_list[0], palette["x"], comb_progress)
        y_line4 = create_animated_graph_line(y_comb, graph_axes_list[1], palette["y"], comb_progress)
        z_line4 = create_animated_graph_line(z_comb, graph_axes_list[2], palette["z"], comb_progress)
        
        # Quick combined motion - synchronized with graph
        accel_group.save_state()
        
        # X movements (samples 5-30)
        self.play(
            accel_group.animate.shift(RIGHT * 0.3),
            comb_progress.animate.set_value(0.15),
            rate_func=rate_functions.ease_out_quad,
            run_time=0.5
        )
        self.play(
            accel_group.animate.shift(LEFT * 0.6),
            comb_progress.animate.set_value(0.30),
            rate_func=there_and_back,
            run_time=0.6
        )
        
        # Y movements (samples 35-45)
        self.play(
            accel_group.animate.shift(UP * 0.25),
            comb_progress.animate.set_value(0.45),
            rate_func=rate_functions.ease_out_quad,
            run_time=0.5
        )
        self.play(
            accel_group.animate.shift(DOWN * 0.25),
            comb_progress.animate.set_value(0.55),
            rate_func=rate_functions.ease_in_quad,
            run_time=0.4
        )
        
        # Z movements (samples 55-80)
        self.play(
            accel_group.animate.shift(OUT * 0.2),
            comb_progress.animate.set_value(0.65),
            rate_func=rate_functions.ease_out_quad,
            run_time=0.4
        )
        self.play(
            accel_group.animate.shift(IN * 0.4),
            comb_progress.animate.set_value(0.80),
            rate_func=there_and_back,
            run_time=0.5
        )
        
        # Complete graph
        self.play(
            accel_group.animate.move_to(accel_center),
            comb_progress.animate.set_value(1.0),
            run_time=0.4
        )
        
        # Remove updaters
        x_line4.clear_updaters()
        y_line4.clear_updaters()
        z_line4.clear_updaters()
        
        accel_group.restore()
        accel_group.move_to(accel_center)
        
        # Summary
        self.play(FadeOut(combined_text), run_time=0.3)
        
        summary_text = Text(
            "Acceleration = Gravity + Motion",
            font_size=24,
            color="#fbbf24",
            weight=BOLD
        )
        summary_text.to_edge(DOWN, buff=0.5)
        self.add_fixed_in_frame_mobjects(summary_text)
        
        self.play(FadeIn(summary_text, shift=UP * 0.2), run_time=0.8)
        
        # Final pulse
        self.play(cube.animate.set_stroke(color="#fbbf24", width=4), run_time=0.25)
        self.play(cube.animate.set_stroke(color=WHITE, width=2.5), run_time=0.25)
        self.play(cube.animate.set_stroke(color="#fbbf24", width=4), run_time=0.25)
        self.play(cube.animate.set_stroke(color=WHITE, width=2.5), run_time=0.25)
        
        self.move_camera(phi=55 * DEGREES, theta=-55 * DEGREES, run_time=1.2)
        self.wait(0.5)
