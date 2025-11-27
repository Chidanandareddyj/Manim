from manim import *
import numpy as np

config.quality = "high_quality"  # 1080p60
config.frame_rate = 60


class IMUIntro(ThreeDScene):
    """
    Clip 1: IMU/Accelerometer Basics - Static Introduction (0-10s)
    Shows 3D cube with X/Y/Z axes and real-time graphs.
    Clean layout: Accelerometer centered on left, Graphs on right.
    """
    
    def construct(self):
        # === CAMERA SETUP ===
        self.set_camera_orientation(phi=65 * DEGREES, theta=-45 * DEGREES)
        
        # True black background
        self.camera.background_color = BLACK
        
        # === TITLE (TOP CENTER) ===
        title = Text("Accelerometer", font_size=38, weight=BOLD, color=WHITE)
        title.to_edge(UP, buff=0.3)
        
        # === 3D CUBE (enhanced accelerometer representation) ===
        cube = Cube(side_length=1.6, fill_opacity=0.12, stroke_width=2.5)
        cube.set_fill(BLUE_E, opacity=0.12)
        cube.set_stroke(WHITE, width=2.5)
        
        # === CHIP LABEL ON TOP ===
        chip_label = Text("ACCEL", font_size=12, color="#94a3b8", weight=BOLD)
        chip_label.rotate(PI/2, axis=RIGHT)
        chip_label.rotate(-PI/4, axis=UP)
        chip_label.shift(UP * 0.82)
        
        # === PIN 1 INDICATOR (corner dot) ===
        pin1_dot = Dot3D(point=[-0.7, 0.81, -0.7], radius=0.08, color="#f97316")
        
        # === 3D AXES (X, Y, Z) - THICKER ARROWS ===
        axis_length = 1.5
        axis_thickness = 0.035
        
        x_axis = Arrow3D(
            start=ORIGIN, end=RIGHT * axis_length,
            color="#ef4444", thickness=axis_thickness,
            height=0.22, base_radius=0.07
        )
        y_axis = Arrow3D(
            start=ORIGIN, end=UP * axis_length,
            color="#22c55e", thickness=axis_thickness,
            height=0.22, base_radius=0.07
        )
        z_axis = Arrow3D(
            start=ORIGIN, end=OUT * axis_length,
            color="#3b82f6", thickness=axis_thickness,
            height=0.22, base_radius=0.07
        )
        
        # Axis labels
        x_label = Text("X", font_size=22, color="#ef4444", weight=BOLD)
        x_label.rotate(PI/2, axis=RIGHT)
        x_label.next_to(x_axis.get_end(), RIGHT, buff=0.1)
        
        y_label = Text("Y", font_size=22, color="#22c55e", weight=BOLD)
        y_label.rotate(PI/2, axis=RIGHT)
        y_label.next_to(y_axis.get_end(), UP, buff=0.1)
        
        z_label = Text("Z", font_size=22, color="#3b82f6", weight=BOLD)
        z_label.rotate(PI/2, axis=RIGHT)
        z_label.next_to(z_axis.get_end(), OUT, buff=0.1)
        
        axes_group = VGroup(x_axis, y_axis, z_axis, x_label, y_label, z_label)
        
        # === GROUP ALL ACCELEROMETER ELEMENTS ===
        accel_group = VGroup(cube, chip_label, pin1_dot, axes_group)
        accel_group.move_to(LEFT * 3.8)  # Centered on left half
        
        # === VERTICAL DIVIDER LINE ===
        divider = DashedLine(
            start=UP * 3.5, end=DOWN * 3.5,
            color="#374151", stroke_width=1, dash_length=0.15
        )
        divider.shift(LEFT * 0.3)
        
        # === ACCELERATION GRAPHS (RIGHT SIDE) ===
        graph_y_positions = [1.8, 0, -1.8]
        graph_colors = ["#ef4444", "#22c55e", "#3b82f6"]
        graph_names = ["X", "Y", "Z"]
        
        # Synthetic data - clean signals
        num_samples = 300
        time_range = np.linspace(0, 5, num_samples)
        
        # At rest: Z = -1g, X/Y ≈ 0
        np.random.seed(42)
        z_data = np.full(num_samples, -1.0) + 0.006 * np.random.randn(num_samples)
        x_data = 0.004 * np.random.randn(num_samples)
        y_data = 0.004 * np.random.randn(num_samples)
        
        data_sets = [x_data, y_data, z_data]
        
        # Create graph panels
        graph_axes = []
        graph_lines = []
        graph_groups = []
        
        for i, (y_pos, color, name, data) in enumerate(zip(graph_y_positions, graph_colors, graph_names, data_sets)):
            # Create axes
            axes = Axes(
                x_range=[0, 5, 1],
                y_range=[-1.5, 1.5, 0.5],
                x_length=4.8,
                y_length=1.1,
                axis_config={
                    "stroke_width": 1.2,
                    "stroke_color": "#4a5568",
                    "include_numbers": False,
                    "include_tip": False,
                },
            )
            axes.shift(RIGHT * 3.5 + UP * y_pos)
            
            # Faint grid lines
            grid_lines = VGroup()
            for y_val in [-1, -0.5, 0.5, 1]:
                grid_line = Line(
                    axes.c2p(0, y_val), axes.c2p(5, y_val),
                    color="#2d3748", stroke_width=0.5, stroke_opacity=0.4
                )
                grid_lines.add(grid_line)
            for x_val in [1, 2, 3, 4]:
                grid_line = Line(
                    axes.c2p(x_val, -1.5), axes.c2p(x_val, 1.5),
                    color="#2d3748", stroke_width=0.5, stroke_opacity=0.3
                )
                grid_lines.add(grid_line)
            
            # Y-axis labels
            y_labels = VGroup(
                Text("-1g", font_size=10, color="#718096"),
                Text("0", font_size=10, color="#718096"),
                Text("+1g", font_size=10, color="#718096"),
            )
            y_labels[0].next_to(axes.c2p(0, -1), LEFT, buff=0.06)
            y_labels[1].next_to(axes.c2p(0, 0), LEFT, buff=0.06)
            y_labels[2].next_to(axes.c2p(0, 1), LEFT, buff=0.06)
            
            # X-axis time labels
            x_labels = VGroup()
            for t in [0, 1, 2, 3, 4, 5]:
                x_lbl = Text(f"{t}s", font_size=8, color="#718096")
                x_lbl.next_to(axes.c2p(t, -1.5), DOWN, buff=0.05)
                x_labels.add(x_lbl)
            
            # Axis title with colored dot indicator
            axis_dot = Dot(radius=0.06, color=color)
            axis_title = Text(f"{name}", font_size=16, color=color, weight=BOLD)
            axis_title_group = VGroup(axis_dot, axis_title).arrange(RIGHT, buff=0.08)
            axis_title_group.next_to(axes, LEFT, buff=0.35)
            
            # Zero reference line (emphasized)
            zero_line = Line(
                axes.c2p(0, 0), axes.c2p(5, 0),
                color="#4a5568", stroke_width=1, stroke_opacity=0.7
            )
            
            # Create smooth data line
            points = [axes.c2p(time_range[j], data[j]) for j in range(num_samples)]
            line = VMobject(color=color, stroke_width=2.2)
            line.set_points_smoothly(points[::2])
            
            # Unit label (only on first graph)
            if i == 0:
                unit_label = Text("(m/s²)", font_size=9, color="#718096")
                unit_label.next_to(y_labels[2], UP, buff=0.08)
                y_labels.add(unit_label)
            
            # Group
            graph_group = VGroup(axes, grid_lines, y_labels, x_labels, axis_title_group, zero_line)
            
            graph_axes.append(axes)
            graph_lines.append(line)
            graph_groups.append(graph_group)
        
        # === LEGEND (bottom right) ===
        legend_text = Text("1g = 9.8 m/s²", font_size=12, color="#9ca3af")
        legend_text.to_corner(DR, buff=0.4)
        
        # === ANIMATION SEQUENCE ===
        
        # Fix 2D elements to frame
        self.add_fixed_in_frame_mobjects(title, divider, legend_text)
        for g in graph_groups:
            self.add_fixed_in_frame_mobjects(g)
        for line in graph_lines:
            self.add_fixed_in_frame_mobjects(line)
        
        # [0-2s] Introduce cube with enhancements
        self.play(
            FadeIn(cube, scale=0.9),
            FadeIn(chip_label),
            FadeIn(pin1_dot),
            FadeIn(title),
            run_time=2
        )
        
        # [2-3.5s] Show axes
        self.play(
            Create(axes_group),
            run_time=1.5
        )
        
        # [3.5-4.5s] Show divider and graphs
        self.play(
            FadeIn(divider),
            *[FadeIn(g) for g in graph_groups],
            FadeIn(legend_text),
            run_time=1.5
        )
        
        # [4.5-7s] Animate signal lines with Z-axis highlight
        self.play(
            *[Create(line, run_time=2.5) for line in graph_lines],
            rate_func=linear
        )
        
        # [7-7.5s] Pulse Z-axis to show it's active
        self.play(
            z_axis.animate.set_color(WHITE),
            run_time=0.3
        )
        self.play(
            z_axis.animate.set_color("#3b82f6"),
            run_time=0.3
        )
        
        # [7.5-9s] Narration
        narration = Text(
            "At rest: Gravity shows on Z-axis (-1g)",
            font_size=22,
            color="#fbbf24",
            weight=BOLD
        )
        narration.to_edge(DOWN, buff=0.35)
        self.add_fixed_in_frame_mobjects(narration)
        
        self.play(FadeIn(narration, shift=UP * 0.2), run_time=1)
        
        # [9-11s] Slow camera rotation for 3D effect
        self.move_camera(theta=-35 * DEGREES, run_time=2, rate_func=smooth)
        
        self.wait(1)
        
        # Store for next scene
        self.accel_group = accel_group
        self.graph_axes = graph_axes
        self.graph_groups = graph_groups
        self.narration = narration


class IMUMotion(ThreeDScene):
    """
    Clip 2: IMU Motion Detection (10-30s)
    Shows tilt and walking motion with clean dynamic graphs.
    """
    
    def construct(self):
        # === CAMERA SETUP ===
        self.set_camera_orientation(phi=60 * DEGREES, theta=-45 * DEGREES)
        self.camera.background_color = BLACK
        
        # === TITLE ===
        title = Text("Accelerometer - Motion", font_size=36, weight=BOLD, color=WHITE)
        title.to_edge(UP, buff=0.4)
        
        # === 3D CUBE (matching IMUIntro) ===
        cube = Cube(side_length=1.8, fill_opacity=0.15, stroke_width=2)
        cube.set_fill(BLUE, opacity=0.15)
        cube.set_stroke(WHITE, width=2)
        
        # Axes
        axis_length = 1.6
        axis_thickness = 0.018
        
        x_axis = Arrow3D(ORIGIN, RIGHT * axis_length, color="#ef4444", thickness=axis_thickness, height=0.2, base_radius=0.045)
        y_axis = Arrow3D(ORIGIN, UP * axis_length, color="#22c55e", thickness=axis_thickness, height=0.2, base_radius=0.045)
        z_axis = Arrow3D(ORIGIN, OUT * axis_length, color="#3b82f6", thickness=axis_thickness, height=0.2, base_radius=0.045)
        
        x_label = Text("X", font_size=24, color="#ef4444", weight=BOLD)
        x_label.rotate(PI/2, axis=RIGHT)
        x_label.next_to(x_axis.get_end(), RIGHT, buff=0.12)
        
        y_label = Text("Y", font_size=24, color="#22c55e", weight=BOLD)
        y_label.rotate(PI/2, axis=RIGHT)
        y_label.next_to(y_axis.get_end(), UP, buff=0.12)
        
        z_label = Text("Z", font_size=24, color="#3b82f6", weight=BOLD)
        z_label.rotate(PI/2, axis=RIGHT)
        z_label.next_to(z_axis.get_end(), OUT, buff=0.12)
        
        axes_group = VGroup(x_axis, y_axis, z_axis, x_label, y_label, z_label)
        
        # Position centered on left
        accel_group = VGroup(cube, axes_group)
        accel_group.move_to(LEFT * 3.5)
        
        # === GRAPHS (CLEAN, EXPANDED TIME) ===
        graph_y_positions = [2.0, 0.2, -1.6]
        graph_colors = ["#ef4444", "#22c55e", "#3b82f6"]
        graph_names = ["X", "Y", "Z"]
        
        np.random.seed(42)
        num_samples = 800
        time_range = np.linspace(0, 10, num_samples)
        
        # TILT DATA (0-5s): Z shifts smoothly
        tilt_duration = 400
        z_tilt = np.concatenate([
            -1.0 + 0.5 * np.sin(np.linspace(0, np.pi, tilt_duration)) + 0.01 * np.random.randn(tilt_duration),
            -0.5 + 0.008 * np.random.randn(num_samples - tilt_duration)
        ])
        
        # WALKING DATA (5-10s): Clean oscillations
        walk_start = 400
        x_walk = np.zeros(num_samples) + 0.005 * np.random.randn(num_samples)
        y_walk = np.zeros(num_samples) + 0.005 * np.random.randn(num_samples)
        
        for i in range(walk_start, num_samples):
            t = time_range[i] - 5.0
            x_walk[i] = 0.35 * np.sin(2 * np.pi * 1.8 * t) + 0.015 * np.random.randn()
            y_walk[i] = 0.25 * np.cos(2 * np.pi * 1.8 * t - np.pi/2) + 0.015 * np.random.randn()
        
        data_sets = [x_walk, y_walk, z_tilt]
        
        # Create graphs
        graph_axes = []
        graph_groups = []
        
        for i, (y_pos, color, name) in enumerate(zip(graph_y_positions, graph_colors, graph_names)):
            axes = Axes(
                x_range=[0, 10, 2],
                y_range=[-1.5, 1.5, 0.5],
                x_length=5.0,
                y_length=1.0,
                axis_config={"stroke_width": 1.5, "stroke_color": "#4a5568", "include_tip": False},
            )
            axes.shift(RIGHT * 3.2 + UP * y_pos)
            
            y_labels = VGroup(
                Text("-1g", font_size=10, color="#718096"),
                Text("0", font_size=10, color="#718096"),
                Text("+1g", font_size=10, color="#718096"),
            )
            y_labels[0].next_to(axes.c2p(0, -1), LEFT, buff=0.08)
            y_labels[1].next_to(axes.c2p(0, 0), LEFT, buff=0.08)
            y_labels[2].next_to(axes.c2p(0, 1), LEFT, buff=0.08)
            
            axis_title = Text(f"{name}", font_size=18, color=color, weight=BOLD)
            axis_title.next_to(axes, LEFT, buff=0.5)
            
            zero_line = DashedLine(
                axes.c2p(0, 0), axes.c2p(10, 0),
                color="#4a5568", stroke_width=0.8, stroke_opacity=0.5
            )
            
            graph_group = VGroup(axes, y_labels, axis_title, zero_line)
            
            graph_axes.append(axes)
            graph_groups.append(graph_group)
        
        # === ADD INITIAL ELEMENTS ===
        self.add(cube, axes_group)
        self.add_fixed_in_frame_mobjects(title)
        for g in graph_groups:
            self.add_fixed_in_frame_mobjects(g)
        self.add(*graph_groups)
        
        # === TILT ANIMATION (0-5s) ===
        tilt_narration = Text(
            "Tilting: Z-axis value changes",
            font_size=22,
            color="#fb923c",
            weight=BOLD
        )
        tilt_narration.to_edge(DOWN, buff=0.4)
        self.add_fixed_in_frame_mobjects(tilt_narration)
        
        self.play(FadeIn(tilt_narration), run_time=1)
        
        # Tilt the accelerometer
        self.play(
            Rotate(accel_group, angle=PI/6, axis=RIGHT, about_point=LEFT * 3.5),
            run_time=2.5
        )
        
        # Draw Z-axis graph during tilt (smooth)
        z_points_tilt = [graph_axes[2].c2p(time_range[j], z_tilt[j]) for j in range(0, tilt_duration, 2)]
        z_line_tilt = VMobject(color="#3b82f6", stroke_width=2.0)
        z_line_tilt.set_points_smoothly(z_points_tilt)
        self.add_fixed_in_frame_mobjects(z_line_tilt)
        
        self.play(Create(z_line_tilt, run_time=2.5, rate_func=linear))
        self.wait(0.5)
        
        self.play(FadeOut(tilt_narration))
        
        # === WALKING ANIMATION (5-10s) ===
        walk_narration = Text(
            "Walking: X and Y oscillate",
            font_size=22,
            color="#22c55e",
            weight=BOLD
        )
        walk_narration.to_edge(DOWN, buff=0.4)
        self.add_fixed_in_frame_mobjects(walk_narration)
        
        self.play(FadeIn(walk_narration), run_time=1)
        
        # Gentle bob motion
        original_center = accel_group.get_center()
        
        def gentle_bob(mob, dt):
            t = self.renderer.time
            offset = np.array([
                0.06 * np.sin(2 * np.pi * 1.8 * t),
                0.04 * np.cos(2 * np.pi * 1.8 * t),
                0
            ])
            mob.move_to(original_center + offset)
        
        accel_group.add_updater(gentle_bob)
        
        # Draw X and Y graphs (smooth)
        x_points_walk = [graph_axes[0].c2p(time_range[j], x_walk[j]) for j in range(walk_start, num_samples, 2)]
        y_points_walk = [graph_axes[1].c2p(time_range[j], y_walk[j]) for j in range(walk_start, num_samples, 2)]
        
        x_line_walk = VMobject(color="#ef4444", stroke_width=2.0)
        x_line_walk.set_points_smoothly(x_points_walk)
        
        y_line_walk = VMobject(color="#22c55e", stroke_width=2.0)
        y_line_walk.set_points_smoothly(y_points_walk)
        
        # Complete Z graph
        z_points_rest = [graph_axes[2].c2p(time_range[j], z_tilt[j]) for j in range(tilt_duration, num_samples, 2)]
        z_line_rest = VMobject(color="#3b82f6", stroke_width=2.0)
        z_line_rest.set_points_smoothly(z_points_rest)
        
        self.add_fixed_in_frame_mobjects(x_line_walk, y_line_walk, z_line_rest)
        
        self.play(
            Create(x_line_walk, run_time=3.5, rate_func=linear),
            Create(y_line_walk, run_time=3.5, rate_func=linear),
            Create(z_line_rest, run_time=3.5, rate_func=linear),
        )
        
        accel_group.clear_updaters()
        
        self.wait(1)
        
        # Final message
        final_text = Text(
            "Motion adds to gravity's baseline",
            font_size=24,
            color="#fbbf24",
            weight=BOLD
        )
        final_text.to_edge(DOWN, buff=0.4)
        self.add_fixed_in_frame_mobjects(final_text)
        
        self.play(
            FadeOut(walk_narration),
            FadeIn(final_text)
        )
        self.wait(2)
