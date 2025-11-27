from manim import *

class HelloWorld(Scene):
    def construct(self):
        text = Text("Hello, Manim!")
        self.play(Write(text))
        self.wait(1)

class ShapesDemo(Scene):
    def construct(self):
        # Create objects
        circle = Circle().set_fill(opacity=0.5).set_stroke(width=4)
        square = Square().shift(LEFT*3)
        triangle = Triangle().shift(RIGHT*3)

        # Show title
        title = Text("Shapes Demo").to_edge(UP)
        self.play(Write(title))

        # Fade in the shapes
        self.play(FadeIn(square), FadeIn(circle), FadeIn(triangle))
        self.wait(0.5)

        # Move square to center and transform it into circle
        self.play(square.animate.shift(RIGHT*3), run_time=1)
        self.play(Transform(square, circle), run_time=1)
        self.wait(0.5)

        # Rotate triangle
        self.play(Rotate(triangle, angle=PI), run_time=1)
        self.wait(1)
