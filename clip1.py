from manim import *
import numpy as np


config.quality = "high_quality"  # ensure 1080p export
config.frame_rate = 60


class AccelerometerSample(ThreeDScene):
	"""Five-second teaser showing 3-axis accelerometer basics."""

	def construct(self):
		# Camera and subtle background grid
		self.set_camera_orientation(phi=60 * DEGREES, theta=-45 * DEGREES)
		self.camera.background_color = "#0f1116"

		grid = NumberPlane(
			x_range=(-6, 6, 1),
			y_range=(-4, 4, 1),
			background_line_style={"stroke_color": GREY_E, "stroke_width": 1, "stroke_opacity": 0.3},
			faded_line_style={"stroke_width": 0},
		)
		grid.scale(1.8)
		grid.rotate(PI / 2, axis=RIGHT)
		grid.shift(DOWN * 0.5)
		self.add(grid)

		# IMU body (cube) with axis arrows
		device = Cube(side_length=1.8, stroke_width=2.5).set_fill(BLUE_D, opacity=0.18)
		device.shift(LEFT * 2.7 + UP * 0.4)

		axis_len = 1.8
		x_axis = Arrow3D(ORIGIN, RIGHT * axis_len, color=RED, thickness=0.025, base_radius=0.045)
		y_axis = Arrow3D(ORIGIN, UP * axis_len, color=GREEN, thickness=0.025, base_radius=0.045)
		z_axis = Arrow3D(ORIGIN, OUT * axis_len, color=BLUE, thickness=0.025, base_radius=0.045)
		axes = VGroup(x_axis, y_axis, z_axis)
		axes.move_to(device.get_center())

		axis_labels = VGroup()
		for letter, color, arrow, direction in [
			("X", RED, x_axis, RIGHT),
			("Y", GREEN, y_axis, UP),
			("Z", BLUE, z_axis, OUT),
		]:
			label = Text(letter, color=color, font_size=26, weight=BOLD)
			label.add_background_rectangle(color="#050505", opacity=0.85, buff=0.04)
			label.next_to(arrow.get_end(), direction, buff=0.25)
			axis_labels.add(label)
		self.add_fixed_orientation_mobjects(*axis_labels)

		# Gravity vs motion arrows
		gravity_arrow = Arrow3D(
			start=device.get_center() + UP * 1.2,
			end=device.get_center() + DOWN * 1.2,
			color=BLUE_E,
			thickness=0.04,
			base_radius=0.08,
		)
		gravity_label = Text("Gravity", font_size=24, color=BLUE_E, weight=BOLD)
		gravity_label.add_background_rectangle(color="#050505", opacity=0.85, buff=0.04)
		gravity_label.next_to(gravity_arrow.get_end(), LEFT, buff=0.2)
		self.add_fixed_orientation_mobjects(gravity_label)

		device_group = VGroup(device, axes, axis_labels, gravity_arrow, gravity_label)

		# Graph panels for each axis (fixed to camera)
		graph_y_positions = [1.6, 0.1, -1.4]
		colors = [RED, GREEN, BLUE]
		axis_names = ["X", "Y", "Z"]

		num_samples = 240
		time_range = np.linspace(0, 5, num_samples)
		still_samples = num_samples

		rng = np.random.default_rng(4)
		x_signal = 0.02 * rng.standard_normal(num_samples)
		y_signal = 0.02 * rng.standard_normal(num_samples)
		z_signal = -1.0 + 0.02 * rng.standard_normal(num_samples)

		signal_bank = [x_signal, y_signal, z_signal]

		graph_groups = []
		partial_lines = []
		trackers = []

		for y_pos, color, name, data in zip(graph_y_positions, colors, axis_names, signal_bank):
			axes_2d = Axes(
				x_range=[0, 5, 1],
				y_range=[-1.5, 1.5, 0.5],
				x_length=4.2,
				y_length=1.2,
				axis_config={"stroke_color": GREY_B, "stroke_width": 2, "include_tip": False},
			)
			axes_2d.shift(RIGHT * 3.2 + UP * y_pos)

			title = Text(f"{name}-axis", color=color, font_size=22, weight=BOLD)
			title.next_to(axes_2d, UP, buff=0.1)

			zero = DashedLine(axes_2d.c2p(0, 0), axes_2d.c2p(5, 0), color=GREY_C, stroke_opacity=0.4)

			graph_group = VGroup(axes_2d, title, zero)
			graph_groups.append(graph_group)

			points = [axes_2d.c2p(t, val) for t, val in zip(time_range, data)]
			full_line = VMobject(color=color, stroke_width=3)
			full_line.set_points_as_corners(points)

			tracker = ValueTracker(0)
			trackers.append(tracker)

			partial_line = VMobject(color=color, stroke_width=3)

			def make_updater(ref_line, linked_tracker):
				def updater(mob):
					mob.pointwise_become_partial(ref_line, 0, linked_tracker.get_value())

				return updater

			partial_line.add_updater(make_updater(full_line, tracker))
			partial_lines.append(partial_line)

		# On-screen labels (fixed to frame for clarity)
		caption = Text("3-axis accelerometer", font_size=32, weight=BOLD, color=YELLOW)
		caption.to_edge(UP).shift(DOWN * 0.3)

		still_text = Text("Still → Gravity dominates Z-axis", font_size=26, color=BLUE_C)
		still_text.to_edge(DOWN).shift(UP * 0.2)

		self.add(device_group)
		self.add_fixed_in_frame_mobjects(caption)
		for group, line in zip(graph_groups, partial_lines):
			self.add_fixed_in_frame_mobjects(group, line)
			self.add(line)

		# Stage 1: device at rest (0-2s)
		self.play(FadeIn(caption, shift=UP * 0.2), FadeIn(still_text), run_time=0.8)
		for tracker in trackers:
			tracker.set_value(0)

		self.play(
			*[tracker.animate.set_value(still_samples / num_samples) for tracker in trackers],
			run_time=2,
			rate_func=linear,
		)

		# Hold the calm state and let the traces settle
		self.wait(2)
		self.play(FadeOut(still_text), run_time=0.4)

		for line in partial_lines:
			line.clear_updaters()

		self.play(FadeOut(caption), run_time=0.4)

