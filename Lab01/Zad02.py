DEST_FILENAME = "lab1zad1.png"


def copy_binary_file(save_filename: str):
    filename = input("Podaj nazwę pliku do skopiowania: ")

    with (open(filename, "rb") as file):
        content = file.read()

    with (open(save_filename, "wb") as file):
        file.write(content)


if __name__ == "__main__":
    copy_binary_file(DEST_FILENAME)