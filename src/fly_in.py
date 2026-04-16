import os
import sys
from tkinter import filedialog
from parsing import Parser, Validator
from simulation import Simulator, Debugger
from visualization import Viewer


class Main:
    def __init__(self) -> None:
        self.file_path: str = filedialog.askopenfilename(
            title="Please select a map:",
            initialdir=f"{os.getcwd()}/assets/maps",
            filetypes=[("Maps", "*.txt")],
        )
        self.parse()
        if "--debug" in sys.argv:
            self.debug()
        self.run()

    def parse(self) -> None:
        try:
            Validator().validate_file_path(self.file_path)
            self.data = Parser().parse(self.file_path)
        except Exception as e:
            print(f"Error parsing map: {e}")
            exit(1)

    def debug(self) -> None:
        try:
            Debugger()
        except Exception as e:
            print(f"Error starting debugger: {e}")
            exit(1)

    def run(self) -> None:
        try:
            simulator = Simulator(self.data)
            movements: list[list[str]] = []

            while not simulator.is_done():
                movements.append(simulator.step())
                print(" ".join(movements[-1]))

            print(f"\nTotal turns: {len(movements)}")
            Viewer(self.data, movements)
        except Exception as e:
            print(f"Error displaying map: {e}")
            exit(1)


if __name__ == "__main__":
    Main()
