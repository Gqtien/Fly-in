import os
from tkinter import filedialog
from parsing import Parser


class Main:
    def __init__(self) -> None:
        self.file_path: str = filedialog.askopenfilename(
            title="Please select a map:",
            initialdir=f"{os.getcwd()}/assets/maps",
            filetypes=[("Maps", "*.txt")],
        )
        self.data = Parser().parse(self.file_path)

    def run(self) -> None: ...


if __name__ == "__main__":
    main = Main()
    print(main.data)
