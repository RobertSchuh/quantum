from manim import *
from manim_slides import Slide

class CreateCircle(Scene):
    def construct(self):
        circle = Circle()  # create a circle
        circle.set_fill(PINK, opacity=0.5)  # set the color and transparency
        self.play(Create(circle))  # show the circle on screen


class CreateCircle2(Scene):
    def construct(self):
        circle = Circle()  # create a circle
        circle.set_fill(RED, opacity=0.5)  # set the color and transparency
        self.play(Create(circle))  # show the circle on screen


class AddPackageLatex(Scene):
    def construct(self):
        myTemplate = TexTemplate()
        myTemplate.add_to_preamble(r"\usepackage{mathrsfs}")
        tex = Tex(
            r"$\mathscr{H} \rightarrow \mathbb{H}$}",
            tex_template=myTemplate,
            font_size=144,
        )
        self.add(tex)


class all_together(Slide):
    def construct(self):
        CreateCircle.construct(self)
        self.next_slide()
        CreateCircle2.construct(self)
        self.next_slide()
        AddPackageLatex.construct(self)
        self.wait(1)
        self.next_slide()


class BasicExample(Slide):
    def construct(self):
        circle = Circle(radius=3, color=BLUE)
        dot = Dot()

        self.play(GrowFromCenter(circle))
        self.next_slide()  # Waits user to press continue to go to the next slide

        self.start_loop()  # Start loop
        self.play(MoveAlongPath(dot, circle), run_time=2, rate_func=linear)
        self.end_loop()  # This will loop until user inputs a key

        self.play(dot.animate.move_to(ORIGIN))
        self.next_slide()  # Waits user to press continue to go to the next slide


if __name__ == "__main__":
    import subprocess
    import os

    filename = os.path.abspath(__file__)

    # Example command that references the file
    # command = f"manim {filename} -p"
    scene = "all_together"
    command = f"manim {filename} {scene} && manim-slides {scene} --fullscreen --start-paused --hide-mouse"

    # Start the command process and redirect input and output
    p = subprocess.Popen(command, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)

    # Provide input to the process
    input_str = "1"  # replace with user input as needed
    p.stdin.write(input_str.encode("utf-8"))
    p.stdin.flush()

    # Wait for the process to finish and get the output
    output, _ = p.communicate()

    # Print the output
    print(output.decode("utf-8"))
