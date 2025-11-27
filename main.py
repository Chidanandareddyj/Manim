from manim import *
import numpy as np

config.quality = "high_quality"  # 1080p60
config.frame_rate = 60


class IMUIntro(ThreeDScene):
    """
    Clip 1: IMU/Accelerometer Basics - Static Introduction (0-10s)
    Shows 3D device with gravity baseline and real-time graphs.
    """
    
    def construct(self):
        # === CAMERA SETUP ===
        self.set_camera_orientation(phi=65 * DEGREES, theta=-50 * DEGREES)
        
        # Subtle background
        self.camera.background_color = "#0a0a0a"
        
        # === 3D IMU DEVICE (CUBE) ===
        device = Cube(side_length=2, fill_opacity=0.2, stroke_width=2)
        device.set_fill(BLUE_D, opacity=0.2)
        device.set_stroke(WHITE, width=2)
        
        device_label = Text("IMU Device", font_size=32, weight=BOLD, color=YELLOW)
        device_label.to_edge(UP).shift(DOWN * 0.5)
        
        # === 3D AXES FROM CENTER ===
        axis_length = 2.0
        
        # X-axis (Red) - pointing right
        x_axis = Arrow3D(
            start=ORIGIN,
            end=RIGHT * axis_length,
            color=RED,
            thickness=0.02,
            height=0.3,
            base_radius=0.06
        )
        x_label = Text("X", font_size=28, color=RED, weight=BOLD)
        x_label.next_to(x_axis.get_end(), RIGHT, buff=0.2)
        x_label.rotate(PI/2, axis=RIGHT)
        
        # Y-axis (Green) - pointing up
        y_axis = Arrow3D(
            start=ORIGIN,
            end=UP * axis_length,
            color=GREEN,
            thickness=0.02,
            height=0.3,
            base_radius=0.06
        )
        y_label = Text("Y", font_size=28, color=GREEN, weight=BOLD)
        y_label.next_to(y_axis.get_end(), UP, buff=0.2)
        y_label.rotate(PI/2, axis=RIGHT)
        
        # Z-axis (Blue) - pointing out
        z_axis = Arrow3D(
            start=ORIGIN,
            end=OUT * axis_length,
            color=BLUE,
            thickness=0.02,
            height=0.3,
            base_radius=0.06
        )
        z_label = Text("Z", font_size=28, color=BLUE, weight=BOLD)
        z_label.next_to(z_axis.get_end(), OUT, buff=0.2)
        z_label.rotate(PI/2, axis=RIGHT)
        
        axes_group = VGroup(x_axis, y_axis, z_axis, x_label, y_label, z_label)
        
        # === GRAVITY VECTOR ===
        weight = Sphere(radius=0.15, color=YELLOW)
        weight.set_sheen(-0.4, DR)
        
        gravity_arrow = Arrow3D(
            start=UP * 1.2,
            end=DOWN * 1.2,
            color=BLUE,
            thickness=0.04,
            height=0.4,
            base_radius=0.08
        )
        
        gravity_label = Text("Gravity\n(1g)", font_size=24, color=BLUE)
        gravity_label.next_to(ORIGIN, LEFT, buff=2)
        
        # Group device elements
        device_group = VGroup(device, axes_group, weight, gravity_arrow)
        device_group.shift(LEFT * 3 + UP * 0.5)
        
        # === ACCELERATION GRAPHS (FIXED TO CAMERA) ===
        graph_y_positions = [1.8, 0, -1.8]
        graph_colors = [RED, GREEN, BLUE]
        graph_names = ["X", "Y", "Z"]
        
        # Synthetic data
        num_samples = 500
        time_range = np.linspace(0, 5, num_samples)
        
        # At rest: Z = -1g, X/Y ≈ 0
        z_data = np.full(num_samples, -1.0) + 0.03 * np.random.randn(num_samples)
        x_data = 0.02 * np.random.randn(num_samples)
        y_data = 0.02 * np.random.randn(num_samples)
        
        data_sets = [x_data, y_data, z_data]
        
        # Create graph panels
        graph_axes = []
        graph_lines = []
        graph_groups = []
        
        for i, (y_pos, color, name, data) in enumerate(zip(graph_y_positions, graph_colors, graph_names, data_sets)):
            # Create axes
            axes = Axes(
                x_range=[0, 5, 1],
                y_range=[-2, 2, 1],
                x_length=4.5,
                y_length=1.2,
                axis_config={
                    "stroke_width": 2,
                    "stroke_color": GREY,
                    "include_numbers": False,
                    "include_tip": False,
                },
            )
            axes.shift(RIGHT * 3.5 + UP * y_pos)
            
            # Y-axis labels
            y_labels = VGroup(
                Text("-2g", font_size=12, color=GREY_B),
                Text("0g", font_size=12, color=GREY_B),
                Text("+2g", font_size=12, color=GREY_B),
            )
            y_labels[0].next_to(axes.c2p(0, -2), LEFT, buff=0.1)
            y_labels[1].next_to(axes.c2p(0, 0), LEFT, buff=0.1)
            y_labels[2].next_to(axes.c2p(0, 2), LEFT, buff=0.1)
            
            # Title
            title = Text(f"{name}-axis", font_size=20, color=color, weight=BOLD)
            title.next_to(axes, UP, buff=0.2)
            
            # Zero reference line
            zero_line = DashedLine(
                axes.c2p(0, 0), axes.c2p(5, 0),
                color=GREY, stroke_width=1, stroke_opacity=0.4
            )
            
            # Create data line
            display_samples = 300
            points = [axes.c2p(time_range[j], data[j]) for j in range(display_samples)]
            line = VMobject(color=color, stroke_width=2.5)
            line.set_points_as_corners(points)
            
            # Group everything
            graph_group = VGroup(axes, y_labels, title, zero_line)
            line_mob = line  # Store reference
            
            graph_axes.append(axes)
            graph_lines.append(line)
            graph_groups.append(graph_group)
        
        # === ANIMATION SEQUENCE ===
        
        # Fix labels to frame
        self.add_fixed_in_frame_mobjects(device_label, gravity_label)
        for g in graph_groups:
            self.add_fixed_in_frame_mobjects(g)
        for line in graph_lines:
            self.add_fixed_in_frame_mobjects(line)
        
        # [0-2s] Introduce device
        self.play(
            FadeIn(device, scale=0.9),
            FadeIn(device_label),
            run_time=2
        )
        
        # [2-3.5s] Show axes
        self.play(
            Create(axes_group),
            run_time=1.5
        )
        
        # [3.5-5.5s] Show gravity
        self.play(
            Create(gravity_arrow),
            FadeIn(weight, scale=0.5),
            FadeIn(gravity_label),
            run_time=2
        )
        
        # [5.5-7s] Bring in graphs
        self.play(
            *[FadeIn(g) for g in graph_groups],
            run_time=1.5
        )
        
        # [7-10s] Animate signal lines
        self.play(
            *[Create(line, run_time=3) for line in graph_lines],
            rate_func=linear
        )
        
        # [10-11.5s] Narration
        narration = Text(
            "At rest: Gravity dominates Z-axis",
            font_size=28,
            color=YELLOW,
            weight=BOLD
        )
        narration.to_edge(DOWN).shift(UP * 0.3)
        self.add_fixed_in_frame_mobjects(narration)
        
        self.play(FadeIn(narration, shift=UP * 0.3), run_time=1.5)
        self.wait(1)
        
        # Store for next scene
        self.device_group = device_group
        self.device = device
        self.graph_axes = graph_axes
        self.graph_groups = graph_groups
        self.narration = narration


class IMUMotion(ThreeDScene):
    """
    Clip 2: IMU Motion Detection (10-30s)
    Shows tilt and shake/walking motion with dynamic graphs.
    """
    
    def construct(self):
        # === CAMERA SETUP ===
        self.set_camera_orientation(phi=65 * DEGREES, theta=-50 * DEGREES)
        self.camera.background_color = "#0a0a0a"
        
        # === RECREATE STATIC ELEMENTS (from previous scene) ===
        # 3D Cube
        device = Cube(side_length=2, fill_opacity=0.3, stroke_width=2)
        device.set_fill(BLUE_D, opacity=0.3)
        device.set_stroke(WHITE, width=2)
        device.shift(LEFT * 3 + UP * 0.5)
        
        # Axes
        axis_length = 2.0
        x_axis = Arrow3D(ORIGIN, RIGHT * axis_length, color=RED, thickness=0.02)
        y_axis = Arrow3D(ORIGIN, UP * axis_length, color=GREEN, thickness=0.02)
        z_axis = Arrow3D(ORIGIN, OUT * axis_length, color=BLUE, thickness=0.02)
        
        x_label = Text("X", font_size=28, color=RED, weight=BOLD)
        x_label.next_to(x_axis.get_end(), RIGHT)
        x_label.rotate(PI/2, axis=RIGHT)
        
        y_label = Text("Y", font_size=28, color=GREEN, weight=BOLD)
        y_label.next_to(y_axis.get_end(), UP)
        y_label.rotate(PI/2, axis=RIGHT)
        
        z_label = Text("Z", font_size=28, color=BLUE, weight=BOLD)
        z_label.next_to(z_axis.get_end(), OUT)
        z_label.rotate(PI/2, axis=RIGHT)
        
        axes_group = VGroup(x_axis, y_axis, z_axis, x_label, y_label, z_label)
        axes_group.shift(LEFT * 3 + UP * 0.5)
        
        # Gravity arrow
        gravity_arrow = Arrow3D(
            start=UP * 1.2,
            end=DOWN * 1.2,
            color=BLUE,
            thickness=0.04
        )
        gravity_arrow.shift(LEFT * 3 + UP * 0.5)
        
        weight = Sphere(radius=0.15, color=YELLOW)
        weight.shift(LEFT * 3 + UP * 0.5)
        
        device_label = Text("IMU Device - Motion", font_size=32, weight=BOLD, color=YELLOW)
        device_label.to_edge(UP).shift(DOWN * 0.5)
        
        # === GRAPHS (EXPANDED TIME) ===
        graph_y_positions = [1.8, 0, -1.8]
        graph_colors = [RED, GREEN, BLUE]
        graph_names = ["X", "Y", "Z"]
        
        num_samples = 1000
        time_range = np.linspace(0, 10, num_samples)
        
        # TILT DATA (0-5s): Z shifts
        tilt_duration = 500
        z_tilt = np.concatenate([
            -1.0 + 0.5 * np.sin(np.linspace(0, np.pi, tilt_duration)) + 0.03 * np.random.randn(tilt_duration),
            -0.5 + 0.03 * np.random.randn(num_samples - tilt_duration)
        ])
        
        # WALKING DATA (5-10s): X and Y oscillate
        walk_start = 500
        x_walk = np.zeros(num_samples) + 0.02 * np.random.randn(num_samples)
        y_walk = np.zeros(num_samples) + 0.02 * np.random.randn(num_samples)
        
        for i in range(walk_start, num_samples):
            t = time_range[i] - 5.0
            x_walk[i] = 0.4 * np.sin(2 * np.pi * 2 * t) + 0.05 * np.random.randn()
            y_walk[i] = 0.3 * np.cos(2 * np.pi * 2 * t - np.pi/2) + 0.05 * np.random.randn()
        
        data_sets = [x_walk, y_walk, z_tilt]
        
        # Create graphs
        graph_axes = []
        graph_groups = []
        
        for i, (y_pos, color, name) in enumerate(zip(graph_y_positions, graph_colors, graph_names)):
            axes = Axes(
                x_range=[0, 10, 2],
                y_range=[-2, 2, 1],
                x_length=4.5,
                y_length=1.2,
                axis_config={"stroke_width": 2, "stroke_color": GREY, "include_tip": False},
            )
            axes.shift(RIGHT * 3.5 + UP * y_pos)
            
            y_labels = VGroup(
                Text("-2g", font_size=12, color=GREY_B),
                Text("0g", font_size=12, color=GREY_B),
                Text("+2g", font_size=12, color=GREY_B),
            )
            y_labels[0].next_to(axes.c2p(0, -2), LEFT, buff=0.1)
            y_labels[1].next_to(axes.c2p(0, 0), LEFT, buff=0.1)
            y_labels[2].next_to(axes.c2p(0, 2), LEFT, buff=0.1)
            
            title = Text(f"{name}-axis", font_size=20, color=color, weight=BOLD)
            title.next_to(axes, UP, buff=0.2)
            
            zero_line = DashedLine(
                axes.c2p(0, 0), axes.c2p(10, 0),
                color=GREY, stroke_width=1, stroke_opacity=0.4
            )
            
            graph_group = VGroup(axes, y_labels, title, zero_line)
            
            graph_axes.append(axes)
            graph_groups.append(graph_group)
        
        # === ADD INITIAL ELEMENTS ===
        self.add(device, axes_group, gravity_arrow, weight)
        self.add_fixed_in_frame_mobjects(device_label)
        for g in graph_groups:
            self.add_fixed_in_frame_mobjects(g)
        self.add(*graph_groups)
        
        # === TILT ANIMATION (0-5s) ===
        tilt_narration = Text(
            "Tilt to sit up? Z-axis shifts...",
            font_size=26,
            color=ORANGE,
            weight=BOLD
        )
        tilt_narration.to_edge(DOWN).shift(UP * 0.3)
        self.add_fixed_in_frame_mobjects(tilt_narration)
        
        self.play(FadeIn(tilt_narration), run_time=1)
        
        # Tilt device
        self.play(
            Rotate(device, angle=PI/6, axis=RIGHT, run_time=3),
            Rotate(axes_group, angle=PI/6, axis=RIGHT, run_time=3),
            Rotate(gravity_arrow, angle=PI/6, axis=RIGHT, run_time=3),
            Rotate(weight, angle=PI/6, axis=RIGHT, run_time=3),
        )
        
        # Draw Z-axis graph during tilt
        z_points_tilt = [graph_axes[2].c2p(time_range[j], z_tilt[j]) for j in range(tilt_duration)]
        z_line_tilt = VMobject(color=BLUE, stroke_width=2.5)
        z_line_tilt.set_points_as_corners(z_points_tilt)
        self.add_fixed_in_frame_mobjects(z_line_tilt)
        
        self.play(Create(z_line_tilt, run_time=3, rate_func=linear))
        self.wait(1)
        
        self.play(FadeOut(tilt_narration))
        
        # === WALKING ANIMATION (5-10s) ===
        walk_narration = Text(
            "Start walking? X and Y dance!",
            font_size=26,
            color=GREEN,
            weight=BOLD
        )
        walk_narration.to_edge(DOWN).shift(UP * 0.3)
        self.add_fixed_in_frame_mobjects(walk_narration)
        
        self.play(FadeIn(walk_narration), run_time=1)
        
        # Shake/bob device
        original_pos = device.get_center()
        
        def shake_updater(mob, dt):
            t = self.renderer.time
            offset = np.array([
                0.1 * np.sin(2 * np.pi * 2 * t),
                0.08 * np.cos(2 * np.pi * 2 * t),
                0
            ])
            mob.move_to(original_pos + offset)
        
        device.add_updater(shake_updater)
        axes_group.add_updater(shake_updater)
        gravity_arrow.add_updater(shake_updater)
        weight.add_updater(shake_updater)
        
        # Draw X and Y graphs
        x_points_walk = [graph_axes[0].c2p(time_range[j], x_walk[j]) for j in range(walk_start, num_samples)]
        y_points_walk = [graph_axes[1].c2p(time_range[j], y_walk[j]) for j in range(walk_start, num_samples)]
        
        x_line_walk = VMobject(color=RED, stroke_width=2.5)
        x_line_walk.set_points_as_corners(x_points_walk)
        
        y_line_walk = VMobject(color=GREEN, stroke_width=2.5)
        y_line_walk.set_points_as_corners(y_points_walk)
        
        # Complete Z graph
        z_points_rest = [graph_axes[2].c2p(time_range[j], z_tilt[j]) for j in range(tilt_duration, num_samples)]
        z_line_rest = VMobject(color=BLUE, stroke_width=2.5)
        z_line_rest.set_points_as_corners(z_points_rest)
        
        # Fix all lines to frame
        self.add_fixed_in_frame_mobjects(x_line_walk, y_line_walk, z_line_rest)
        
        self.play(
            Create(x_line_walk, run_time=4, rate_func=linear),
            Create(y_line_walk, run_time=4, rate_func=linear),
            Create(z_line_rest, run_time=4, rate_func=linear),
        )
        
        device.clear_updaters()
        axes_group.clear_updaters()
        gravity_arrow.clear_updaters()
        weight.clear_updaters()
        
        self.wait(2)
        
        # Final message
        final_text = Text(
            "Motion adds to gravity's pull!",
            font_size=30,
            color=YELLOW,
            weight=BOLD
        )
        final_text.to_edge(DOWN).shift(UP * 0.3)
        self.add_fixed_in_frame_mobjects(final_text)
        
        self.play(
            FadeOut(walk_narration),
            FadeIn(final_text)
        )
        self.wait(2)
    """
    Extended version with dynamic motion (for future segments 10-30s)
    Placeholder for motion detection animations.
    """
    
    def construct(self):
        text = Text(
            "Next: Dynamic Motion Detection\n(Segments 10-30s)",
            font_size=36,
            color=BLUE
        )
        self.play(Write(text))
        self.wait(2)
