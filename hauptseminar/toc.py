from manim import *
from manim_slides import Slide


class TableOfContents(Scene):
    def construct(self):
        # Title
        title = Text("Table of Contents").scale(1.5)
        self.play(Write(title))

        # List of sections
        sections = VGroup(
            Text("Section 1: Introduction"),
            Text("Section 2: Main Content"),
            Text("Section 3: Conclusion")
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.5)

        self.play(
            FadeIn(sections[0]),
            title.animate.next_to(sections[0], UP, buff=0.5)
        )

        self.wait(0.4)
        for section in sections[1:]:
            self.play(FadeIn(section), run_time=0.4)

        self.wait()





class BB84_anim(Slide):
    def construct(self):

        test = Title("test")
        self.play(Write(test), run_time=0.3)

        # self.next_slide()

        box_width = self.camera.frame_width * 0.25
        box_height = self.camera.frame_height - 1.6

        # Create left box
        left_box = RoundedRectangle(width=box_width, height=box_height, corner_radius=0.4, fill_opacity=0.3, stroke_opacity=0.8)
        left_box.to_corner(LEFT + DOWN, buff=0.3)
        self.add(left_box)
        # Create right box
        right_box = RoundedRectangle(width=box_width, height=box_height, corner_radius=0.4, fill_opacity=0.3, stroke_opacity=0.8)
        right_box.to_corner(RIGHT + DOWN, buff=0.3)
        self.add(right_box)

        left_table = MobjectTable([[Text("Alice")], [MathTex(r"\vec{r} = (0 1 1 0 1)")], [Text("2")]])
        left_table.move_to(left_box)
        right_table = Table([["Bob"], ["1"], ["2"]])
        right_table.move_to(right_box)

        self.add(left_table.get_horizontal_lines())
        self.add(right_table.get_horizontal_lines())


        # self.wait(0.1)
        self.next_slide()

        # Animate each row of the table
        for row in left_table.get_rows():
            self.play(Write(row))
            self.next_slide()
            self.wait(0.1)

        # # Create left box title
        # left_box_title = Text("Alice", font_size=30)
        # left_box_title.next_to(left_box.get_corner(UP+LEFT), DOWN+RIGHT, buff=0.3)
        # self.add(left_box_title)

        # # Create left box equations
        # left_equations = VGroup()
        # for i in range(5):
        #     equation = Tex(f"Equation {i}")
        #     equation.next_to(left_box_title, DOWN, aligned_edge=LEFT, buff=0.5)
        #     left_equations.add(equation)
        # left_equations.arrange(DOWN, buff=0.5, aligned_edge=LEFT)
        # left_equations.next_to(left_box_title, DOWN, aligned_edge=LEFT, buff=0.5)
        # self.add(left_equations)


        # # Create the table
        # rows = [
        #     [(r"\sin(x) = \frac{1}{2}")],
        #     [(r"\cos(x) = \frac{\sqrt{3}}{2}")],
        #     [(r"\tan(x) = \frac{\sin(x)}{\cos(x)}")],
        # ]
        # table = Table(rows, h_buff=0.5, v_buff=0.6, line_config={"stroke_width": 0.3, "color": WHITE})
        # table.to_corner(LEFT+DOWN, buff=0.3)
        #
        # # Add the table to the scene
        # self.add(table)
        #
        #
        # # Create right box
        # right_box_width = self.camera.frame_width / 4
        # right_box_height = self.camera.frame_height - 1
        # right_box = RoundedRectangle(width=right_box_width, height=right_box_height, corner_radius=0.5, fill_opacity=0.5, stroke_opacity=0.8)
        # right_box.to_edge(RIGHT, buff=0.5)
        # right_box.shift(UP * 0.5)
        # self.add(right_box)
        #
        # # Create right box title
        # right_box_title = Text("Right Box", font_size=30)
        # right_box_title.next_to(right_box.get_top(), DOWN, buff=0.3)
        # self.add(right_box_title)
        #
        # # Create right box equations
        # right_equations = VGroup()
        # for i in range(5):
        #     equation = Tex(f"Equation {i}")
        #     equation.next_to(right_box_title, DOWN, aligned_edge=LEFT, buff=0.5)
        #     right_equations.add(equation)
        # right_equations.arrange(DOWN, buff=0.5, aligned_edge=LEFT)
        # right_equations.next_to(right_box_title, DOWN, aligned_edge=LEFT, buff=0.5)
        # self.add(right_equations)

        # self.wait(0.1)
        # self.next_slide()


        self.wait(0.1)