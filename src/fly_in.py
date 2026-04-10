import os
from tkinter import filedialog
from parsing import Parser, Validator


class Main:
    def __init__(self) -> None:
        self.file_path: str = filedialog.askopenfilename(
            title="Please select a map:",
            initialdir=f"{os.getcwd()}/assets/maps",
            filetypes=[("Maps", "*.txt")],
        )

        try:
            Validator().validate_file_path(self.file_path)
            self.data = Parser().parse(self.file_path)
        except Exception as e:
            print(f"Error parsing map: {e}")
            exit(1)

        self.run()

    def run(self) -> None: ...


if __name__ == "__main__":
    main = Main()
    print(main.data)
