import os
import sys
from tkinter import filedialog
from parsing import Parser, Validator
from simulation import Simulator
from visualization import Renderer


class Main:
    def __init__(self) -> None:
        self.debug = "--debug" in sys.argv

        self.prompt()
        self.parse()
        self.run()

    def prompt(self) -> None:
        maps_dir = f"{os.getcwd()}/assets/maps"
        default_map = f"{maps_dir}/challenger/01_the_impossible_dream.txt"

        self.file_path: str = (
            filedialog.askopenfilename(
                title="Please select a map:",
                initialdir=maps_dir,
                filetypes=[("Maps", "*.txt")],
            )
            if not self.debug
            else default_map
        )

    def parse(self) -> None:
        try:
            Validator().validate_file_path(self.file_path)
            self.data = Parser().parse(self.file_path)
        except Exception as e:
            print(f"Error parsing map: {e}")
            exit(1)

    def run(self) -> None:
        try:
            Renderer(
                data=self.data,
                movements=Simulator(self.data).simulate(),
                debug=self.debug,
            )
        except Exception as e:
            print(f"Error displaying map: {e}")
            exit(1)


if __name__ == "__main__":
    Main()
