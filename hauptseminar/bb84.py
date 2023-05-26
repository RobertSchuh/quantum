from manim import *

class BB84_anim(Scene):
    def construct(self):


        # Create the text "Bob"
        text = Text("Bob", font_size=50)
        text.shift(UP*2 + LEFT*3)

        # Create a rounded rectangle around the text
        box = SurroundingRectangle(text, buff=0.2, corner_radius=0.3, color=WHITE, fill_opacity=0)

        self.add(box, text)

        self.wait(10)





if __name__ == "__main__":
    import subprocess
    import os

    filename = os.path.abspath(__file__)

    # Example command that references the file
    command = f"manim {filename} -p"
    # scene = "all_together"
    # command = f"manim {filename} {scene} && manim-slides {scene} --fullscreen --start-paused --hide-mouse"

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
