from manim import *
import numpy as np

config.quality = "high_quality"  # 1080p60
config.frame_rate = 60


class AccelerometerFull(ThreeDScene):
    """
    Full 30-second Accelerometer visualization video.
    Scenes:
    - [0-6s] Introduction: Static device with gravity
    - [6-12s] Tilt/Posture: Z-axis changes
    - [12-18s] Walking: X/Y oscillations
    - [18-24s] Rotation: All axes wobble
    - [24-30s] Return to rest + Summary
    """
    
    def construct(self):
        # === CAMERA & BACKGROUND ===
        self.set_camera_orientation(phi=65 * DEGREES, theta=-45 * DEGREES)
        self.camera.background_color = BLACK
        
        # ============================================================
        # SECTION 1: CREATE ALL PERSISTENT ELEMENTS
        # ============================================================
        
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
        
        x_axis = Arrow3D(ORIGIN, RIGHT * axis_length, color="#ef4444", thickness=axis_thickness, height=0.24, base_radius=0.08)
        y_axis = Arrow3D(ORIGIN, UP * axis_length, color="#22c55e", thickness=axis_thickness, height=0.24, base_radius=0.08)
        z_axis = Arrow3D(ORIGIN, OUT * axis_length, color="#3b82f6", thickness=axis_thickness, height=0.24, base_radius=0.08)
        
        x_label = Text("X", font_size=20, color="#ef4444", weight=BOLD)
        x_label.rotate(PI/2, axis=RIGHT)
        x_label.next_to(x_axis.get_end(), RIGHT, buff=0.08)
        
        y_label = Text("Y", font_size=20, color="#22c55e", weight=BOLD)
        y_label.rotate(PI/2, axis=RIGHT)
        y_label.next_to(y_axis.get_end(), UP, buff=0.08)
        
        z_label = Text("Z", font_size=20, color="#3b82f6", weight=BOLD)
        z_label.rotate(PI/2, axis=RIGHT)
        z_label.next_to(z_axis.get_end(), OUT, buff=0.08)
        
        axes_group = VGroup(x_axis, y_axis, z_axis, x_label, y_label, z_label)
        
        # === GROUP ACCELEROMETER ===
        accel_static = VGroup(cube, axes_group)
        accel_center = LEFT * 3.8
        accel_static.move_to(accel_center)
        
        # === LIVE GRAPHS (5-second rolling window) ===
        graph_y_positions = [1.6, 0, -1.6]
        graph_colors = ["#ef4444", "#22c55e", "#3b82f6"]
        graph_names = ["X", "Y", "Z"]
        
        # Create graph axes
        graph_axes_list = []
        graph_groups = []
        
        for i, (y_pos, color, name) in enumerate(zip(graph_y_positions, graph_colors, graph_names)):
            axes = Axes(
                x_range=[0, 5, 1],
                y_range=[-2, 2, 1],
                x_length=4.5,
                y_length=1.0,
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
            for yv in [-1, 0, 1]:
                gl = Line(axes.c2p(0, yv), axes.c2p(5, yv), color="#2d3748", stroke_width=0.5, stroke_opacity=0.4)
                grid.add(gl)
            
            # Y labels
            y_labels = VGroup(
                Text("-1g", font_size=9, color="#718096"),
                Text("0", font_size=9, color="#718096"),
                Text("+1g", font_size=9, color="#718096"),
            )
            y_labels[0].next_to(axes.c2p(0, -1), LEFT, buff=0.05)
            y_labels[1].next_to(axes.c2p(0, 0), LEFT, buff=0.05)
            y_labels[2].next_to(axes.c2p(0, 1), LEFT, buff=0.05)
            
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
        # SCENE 1: INTRODUCTION - STATIC DEVICE (0-6s)
        # ============================================================
        
        # Intro text
        intro_text = Text("Device at Rest", font_size=20, color="#9ca3af")
        intro_text.next_to(title, DOWN, buff=0.15)
        self.add_fixed_in_frame_mobjects(intro_text)
        
        # Fade in device
        self.play(
            FadeIn(cube, scale=0.9),
            FadeIn(title),
            FadeIn(intro_text),
            run_time=1.5
        )
        
        # Show axes
        self.play(Create(axes_group), run_time=1)
        
        # Show graphs and tracker AFTER axes
        for g in graph_groups:
            self.add_fixed_in_frame_mobjects(g)
        
        self.play(*[FadeIn(g) for g in graph_groups], run_time=1)
        
        # Draw static signal (Z at -1g, X/Y at 0)
        static_samples = 150
        t_static = np.linspace(0, 5, static_samples)
        x_static = 0.04 * np.sin(2 * np.pi * 0.25 * t_static)
        y_static = 0.04 * np.sin(2 * np.pi * 0.18 * t_static + PI / 4)
        z_static = -1.0 + 0.03 * np.cos(2 * np.pi * 0.15 * t_static)
        
        static_lines = []
        for i, (data, axes, color) in enumerate(zip([x_static, y_static, z_static], graph_axes_list, graph_colors)):
            points = [axes.c2p(t_static[j], data[j]) for j in range(static_samples)]
            line = VMobject(color=color, stroke_width=2)
            line.set_points_smoothly(points[::2])
            static_lines.append(line)
            self.add_fixed_in_frame_mobjects(line)
        
        self.play(
            *[Create(line, run_time=1.5) for line in static_lines],
            rate_func=linear
        )
        
        self.wait(0.5)
        
        # ============================================================
        # SCENE 2: TILT / POSTURE CHANGE (6-12s)
        # ============================================================
        
        tilt_text = Text("Posture Change: Tilting", font_size=20, color="#f59e0b")
        tilt_text.next_to(title, DOWN, buff=0.15)
        self.add_fixed_in_frame_mobjects(tilt_text)
        
        self.play(
            FadeOut(intro_text),
            FadeIn(tilt_text),
            run_time=0.5
        )
        
        # Clear old lines
        self.play(*[FadeOut(line) for line in static_lines], run_time=0.3)
        
        # Tilt the device
        tilt_group = VGroup(cube, axes_group)
        
        # Generate tilt data
        tilt_samples = 150
        t_tilt = np.linspace(0, 5, tilt_samples)
        tilt_angle = PI / 5
        theta_profile = tilt_angle * np.sin(np.linspace(0, np.pi, tilt_samples))
        z_tilt = -np.cos(theta_profile)
        x_tilt = 0.8 * np.sin(theta_profile)
        y_tilt = 0.05 * np.sin(2 * np.pi * 0.5 * t_tilt)
        
        tilt_lines = []
        for i, (data, axes, color) in enumerate(zip([x_tilt, y_tilt, z_tilt], graph_axes_list, graph_colors)):
            points = [axes.c2p(t_tilt[j], data[j]) for j in range(tilt_samples)]
            line = VMobject(color=color, stroke_width=2)
            line.set_points_smoothly(points[::2])
            tilt_lines.append(line)
            self.add_fixed_in_frame_mobjects(line)
        
        # Animate tilt with graph
        self.play(
            Rotate(tilt_group, angle=PI/5, axis=RIGHT, about_point=accel_center),
            *[Create(line, run_time=3) for line in tilt_lines],
            rate_func=linear,
            run_time=3
        )
        
        # Pulse Z-axis to highlight
        self.play(
            z_axis.animate.set_color(WHITE), run_time=0.2
        )
        self.play(
            z_axis.animate.set_color("#3b82f6"), run_time=0.2
        )
        
        # Tilt back slightly
        self.play(
            Rotate(tilt_group, angle=-PI/5, axis=RIGHT, about_point=accel_center),
            run_time=1.2
        )
        
        self.wait(0.3)
        
        # ============================================================
        # SCENE 3: WALKING - X/Y OSCILLATIONS (12-18s)
        # ============================================================
        
        walk_text = Text("Walking: X/Y Oscillate", font_size=20, color="#22c55e")
        walk_text.next_to(title, DOWN, buff=0.15)
        self.add_fixed_in_frame_mobjects(walk_text)
        
        self.play(
            FadeOut(tilt_text),
            FadeIn(walk_text),
            *[FadeOut(line) for line in tilt_lines],
            run_time=0.5
        )
        
        # Walking data
        walk_samples = 150
        t_walk = np.linspace(0, 5, walk_samples)
        walk_frequency = 1.8
        x_walk = 0.55 * np.sin(2 * np.pi * walk_frequency * t_walk)
        y_walk = 0.4 * np.cos(2 * np.pi * walk_frequency * t_walk)
        z_walk = -0.65 + 0.18 * np.sin(2 * np.pi * 2 * walk_frequency * t_walk + PI / 4)
        
        walk_lines = []
        for i, (data, axes, color) in enumerate(zip([x_walk, y_walk, z_walk], graph_axes_list, graph_colors)):
            points = [axes.c2p(t_walk[j], data[j]) for j in range(walk_samples)]
            line = VMobject(color=color, stroke_width=2)
            line.set_points_smoothly(points[::2])
            walk_lines.append(line)
            self.add_fixed_in_frame_mobjects(line)
        
        # Bob the device
        original_pos = tilt_group.get_center()
        
        walk_phase = ValueTracker(0)
        
        def walk_bob(mob, dt):
            walk_phase.increment_value(dt)
            t = walk_phase.get_value()
            offset = np.array([
                0.08 * np.sin(2 * np.pi * walk_frequency * t),
                0.05 * np.cos(2 * np.pi * walk_frequency * t),
                0.03 * np.sin(2 * np.pi * 2 * walk_frequency * t)
            ])
            mob.move_to(original_pos + offset)
        
        tilt_group.add_updater(walk_bob)
        
        self.play(
            *[Create(line, run_time=4) for line in walk_lines],
            rate_func=linear,
            run_time=4
        )
        
        # Pulse X and Y
        self.play(
            x_axis.animate.set_color(WHITE),
            y_axis.animate.set_color(WHITE),
            run_time=0.2
        )
        self.play(
            x_axis.animate.set_color("#ef4444"),
            y_axis.animate.set_color("#22c55e"),
            run_time=0.2
        )
        
        tilt_group.clear_updaters()
        tilt_group.move_to(original_pos)
        
        self.wait(0.3)
        
        # ============================================================
        # SCENE 4: ROTATION - ALL AXES WOBBLE (18-24s)
        # ============================================================
        
        rotate_text = Text("Rotation: All Axes Wobble", font_size=20, color="#a855f7")
        rotate_text.next_to(title, DOWN, buff=0.15)
        self.add_fixed_in_frame_mobjects(rotate_text)
        
        self.play(
            FadeOut(walk_text),
            FadeIn(rotate_text),
            *[FadeOut(line) for line in walk_lines],
            run_time=0.5
        )
        
        # Rotation data - all axes change
        rot_samples = 150
        t_rot = np.linspace(0, 5, rot_samples)
        x_rot = 0.4 * np.sin(2 * np.pi * 0.8 * t_rot) + 0.25 * np.sin(2 * np.pi * 1.2 * t_rot)
        y_rot = 0.35 * np.cos(2 * np.pi * 0.6 * t_rot) + 0.2 * np.cos(2 * np.pi * 1.1 * t_rot)
        z_rot = -0.5 + 0.4 * np.sin(2 * np.pi * 0.5 * t_rot + PI / 3)
        
        rot_lines = []
        for i, (data, axes, color) in enumerate(zip([x_rot, y_rot, z_rot], graph_axes_list, graph_colors)):
            points = [axes.c2p(t_rot[j], data[j]) for j in range(rot_samples)]
            line = VMobject(color=color, stroke_width=2)
            line.set_points_smoothly(points[::2])
            rot_lines.append(line)
            self.add_fixed_in_frame_mobjects(line)
        
        # Complex rotation
        self.play(
            Rotate(tilt_group, angle=PI/4, axis=UP, about_point=accel_center, run_time=2),
            Rotate(tilt_group, angle=PI/6, axis=RIGHT, about_point=accel_center, run_time=2),
            *[Create(line, run_time=4) for line in rot_lines],
            rate_func=linear,
            run_time=4
        )
        
        # Pulse all axes
        self.play(
            x_axis.animate.set_color(WHITE),
            y_axis.animate.set_color(WHITE),
            z_axis.animate.set_color(WHITE),
            run_time=0.2
        )
        self.play(
            x_axis.animate.set_color("#ef4444"),
            y_axis.animate.set_color("#22c55e"),
            z_axis.animate.set_color("#3b82f6"),
            run_time=0.2
        )
        
        self.wait(0.3)
        
        # ============================================================
        # SCENE 5: RETURN TO REST + SUMMARY (24-30s)
        # ============================================================
        
        rest_text = Text("Returning to Rest", font_size=20, color="#9ca3af")
        rest_text.next_to(title, DOWN, buff=0.15)
        self.add_fixed_in_frame_mobjects(rest_text)
        
        self.play(
            FadeOut(rotate_text),
            FadeIn(rest_text),
            run_time=0.5
        )
        
        # Rotate back to original orientation
        self.play(
            tilt_group.animate.move_to(accel_center),
            Rotate(tilt_group, angle=-PI/4, axis=UP, about_point=accel_center),
            Rotate(tilt_group, angle=-PI/6 + PI/10, axis=RIGHT, about_point=accel_center),
            *[FadeOut(line) for line in rot_lines],
            run_time=1.5
        )
        
        # Final static data
        final_samples = 100
        t_final = np.linspace(0, 5, final_samples)
        x_final = 0.03 * np.sin(2 * np.pi * 0.3 * t_final + PI / 5)
        y_final = 0.03 * np.sin(2 * np.pi * 0.25 * t_final)
        z_final = -1.0 + 0.02 * np.cos(2 * np.pi * 0.2 * t_final)
        
        final_lines = []
        for i, (data, axes, color) in enumerate(zip([x_final, y_final, z_final], graph_axes_list, graph_colors)):
            points = [axes.c2p(t_final[j], data[j]) for j in range(final_samples)]
            line = VMobject(color=color, stroke_width=2)
            line.set_points_smoothly(points[::2])
            final_lines.append(line)
            self.add_fixed_in_frame_mobjects(line)
        
        self.play(
            *[Create(line, run_time=1) for line in final_lines],
            rate_func=linear
        )
        
        # Summary text
        self.play(FadeOut(rest_text), run_time=0.3)
        
        summary_text = Text(
            "Raw Acceleration = Gravity + Motion",
            font_size=24,
            color="#fbbf24",
            weight=BOLD
        )
        summary_text.to_edge(DOWN, buff=0.5)
        self.add_fixed_in_frame_mobjects(summary_text)
        
        self.play(FadeIn(summary_text, shift=UP * 0.2), run_time=1)
        
        # Final pulse on device (tease data flow)
        self.play(
            cube.animate.set_stroke(color="#fbbf24", width=4),
            run_time=0.3
        )
        self.play(
            cube.animate.set_stroke(color=WHITE, width=2.5),
            run_time=0.3
        )
        self.play(
            cube.animate.set_stroke(color="#fbbf24", width=4),
            run_time=0.3
        )
        self.play(
            cube.animate.set_stroke(color=WHITE, width=2.5),
            run_time=0.3
        )
        
        # Camera slowly pulls back
        self.move_camera(phi=55 * DEGREES, theta=-55 * DEGREES, run_time=1.5)
        
        self.wait(0.5)
