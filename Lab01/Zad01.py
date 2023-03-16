DEST_FILENAME = "lab1zad1.txt"


def copy_text_file(dest_filename: str):
    filename = input("Podaj nazwę pliku do skopiowania: ")

    with (open(filename, "r") as file):
        content = file.read()

    with (open(dest_filename, "w") as file):
        file.write(content)


if __name__ == "__main__":
    copy_text_file(DEST_FILENAME)