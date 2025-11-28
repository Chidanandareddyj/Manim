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
        
        # === MOTION TRACKER (bottom left) ===
        tracker_bg = RoundedRectangle(
            width=2.2, height=1.4, corner_radius=0.1,
            fill_opacity=0.15, fill_color=WHITE,
            stroke_width=1, stroke_color="#4a5568"
        )
        tracker_bg.to_corner(DL, buff=0.3)
        
        tracker_title = Text("MOTION", font_size=10, color="#9ca3af", weight=BOLD)
        tracker_title.next_to(tracker_bg.get_top(), DOWN, buff=0.1)
        
        tracker_status = Text("STILL", font_size=14, color="#22c55e", weight=BOLD)
        tracker_status.move_to(tracker_bg.get_center())
        
        tracker_group = VGroup(tracker_bg, tracker_title, tracker_status)
        
        # === LIVE GRAPHS (5-second rolling window) ===
        graph_y_positions = [1.6, 0, -1.6]
        graph_colors = ["#ef4444", "#22c55e", "#3b82f6"]
        graph_names = ["X", "Y", "Z"]
        
        # We'll use ValueTrackers for live data
        time_tracker = ValueTracker(0)
        
        # Data storage (will be updated)
        self.x_data = []
        self.y_data = []
        self.z_data = []
        self.time_data = []
        
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
        self.add_fixed_in_frame_mobjects(title, tracker_group)
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
        
        self.play(
            *[FadeIn(g) for g in graph_groups],
            FadeIn(tracker_group),
            run_time=1
        )
        
        # Draw static signal (Z at -1g, X/Y at 0)
        np.random.seed(42)
        static_samples = 150
        t_static = np.linspace(0, 5, static_samples)
        x_static = 0.02 * np.random.randn(static_samples)
        y_static = 0.02 * np.random.randn(static_samples)
        z_static = -1.0 + 0.02 * np.random.randn(static_samples)
        
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
        
        # Update status
        new_status = Text("TILTING", font_size=14, color="#f59e0b", weight=BOLD)
        new_status.move_to(tracker_status.get_center())
        self.add_fixed_in_frame_mobjects(new_status)
        
        tilt_text = Text("Posture Change: Tilting", font_size=20, color="#f59e0b")
        tilt_text.next_to(title, DOWN, buff=0.15)
        self.add_fixed_in_frame_mobjects(tilt_text)
        
        self.play(
            FadeOut(intro_text),
            FadeIn(tilt_text),
            ReplacementTransform(tracker_status, new_status),
            run_time=0.5
        )
        tracker_status = new_status
        
        # Clear old lines
        self.play(*[FadeOut(line) for line in static_lines], run_time=0.3)
        
        # Tilt the device
        tilt_group = VGroup(cube, axes_group)
        
        # Generate tilt data
        tilt_samples = 150
        t_tilt = np.linspace(0, 5, tilt_samples)
        # During tilt: Z decreases (gravity component shifts), X increases slightly
        z_tilt = -1.0 + 0.35 * np.sin(np.linspace(0, np.pi, tilt_samples)) + 0.015 * np.random.randn(tilt_samples)
        x_tilt = 0.25 * np.sin(np.linspace(0, np.pi, tilt_samples)) + 0.015 * np.random.randn(tilt_samples)
        y_tilt = 0.02 * np.random.randn(tilt_samples)
        
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
            Rotate(tilt_group, angle=-PI/10, axis=RIGHT, about_point=accel_center),
            run_time=1
        )
        
        self.wait(0.3)
        
        # ============================================================
        # SCENE 3: WALKING - X/Y OSCILLATIONS (12-18s)
        # ============================================================
        
        # Update status
        walk_status = Text("WALKING", font_size=14, color="#22c55e", weight=BOLD)
        walk_status.move_to(tracker_status.get_center())
        self.add_fixed_in_frame_mobjects(walk_status)
        
        walk_text = Text("Walking: X/Y Oscillate", font_size=20, color="#22c55e")
        walk_text.next_to(title, DOWN, buff=0.15)
        self.add_fixed_in_frame_mobjects(walk_text)
        
        self.play(
            FadeOut(tilt_text),
            FadeIn(walk_text),
            ReplacementTransform(tracker_status, walk_status),
            *[FadeOut(line) for line in tilt_lines],
            run_time=0.5
        )
        tracker_status = walk_status
        
        # Walking data
        walk_samples = 150
        t_walk = np.linspace(0, 5, walk_samples)
        x_walk = 0.5 * np.sin(2 * np.pi * 1.8 * t_walk) + 0.02 * np.random.randn(walk_samples)
        y_walk = 0.35 * np.cos(2 * np.pi * 1.8 * t_walk) + 0.02 * np.random.randn(walk_samples)
        z_walk = -0.65 + 0.15 * np.sin(2 * np.pi * 3.6 * t_walk) + 0.02 * np.random.randn(walk_samples)
        
        walk_lines = []
        for i, (data, axes, color) in enumerate(zip([x_walk, y_walk, z_walk], graph_axes_list, graph_colors)):
            points = [axes.c2p(t_walk[j], data[j]) for j in range(walk_samples)]
            line = VMobject(color=color, stroke_width=2)
            line.set_points_smoothly(points[::2])
            walk_lines.append(line)
            self.add_fixed_in_frame_mobjects(line)
        
        # Bob the device
        original_pos = tilt_group.get_center()
        
        def walk_bob(mob, dt):
            t = self.renderer.time
            offset = np.array([
                0.08 * np.sin(2 * np.pi * 1.8 * t),
                0.05 * np.cos(2 * np.pi * 1.8 * t),
                0.03 * np.sin(2 * np.pi * 3.6 * t)
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
        
        # Update status
        rotate_status = Text("ROTATING", font_size=14, color="#a855f7", weight=BOLD)
        rotate_status.move_to(tracker_status.get_center())
        self.add_fixed_in_frame_mobjects(rotate_status)
        
        rotate_text = Text("Rotation: All Axes Wobble", font_size=20, color="#a855f7")
        rotate_text.next_to(title, DOWN, buff=0.15)
        self.add_fixed_in_frame_mobjects(rotate_text)
        
        self.play(
            FadeOut(walk_text),
            FadeIn(rotate_text),
            ReplacementTransform(tracker_status, rotate_status),
            *[FadeOut(line) for line in walk_lines],
            run_time=0.5
        )
        tracker_status = rotate_status
        
        # Rotation data - all axes change
        rot_samples = 150
        t_rot = np.linspace(0, 5, rot_samples)
        x_rot = 0.4 * np.sin(2 * np.pi * 0.8 * t_rot) + 0.3 * np.sin(2 * np.pi * 1.5 * t_rot) + 0.02 * np.random.randn(rot_samples)
        y_rot = 0.35 * np.cos(2 * np.pi * 0.6 * t_rot) + 0.25 * np.cos(2 * np.pi * 1.2 * t_rot) + 0.02 * np.random.randn(rot_samples)
        z_rot = -0.5 + 0.4 * np.sin(2 * np.pi * 0.5 * t_rot + PI/3) + 0.02 * np.random.randn(rot_samples)
        
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
        
        # Update status
        still_status = Text("STILL", font_size=14, color="#22c55e", weight=BOLD)
        still_status.move_to(tracker_status.get_center())
        self.add_fixed_in_frame_mobjects(still_status)
        
        rest_text = Text("Returning to Rest", font_size=20, color="#9ca3af")
        rest_text.next_to(title, DOWN, buff=0.15)
        self.add_fixed_in_frame_mobjects(rest_text)
        
        self.play(
            FadeOut(rotate_text),
            FadeIn(rest_text),
            ReplacementTransform(tracker_status, still_status),
            run_time=0.5
        )
        tracker_status = still_status
        
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
        x_final = 0.015 * np.random.randn(final_samples)
        y_final = 0.015 * np.random.randn(final_samples)
        z_final = -1.0 + 0.015 * np.random.randn(final_samples)
        
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
