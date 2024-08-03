import os


def create_file(file_name):
    f = open(file_name, "w")
    f.close()


def write_file(file_name, content) -> None:
    f = open(file_name, "w")
    f.write(content)
    f.close()


def read_file(file_name) -> str:
    f = open(file_name, "r")
    content = f.read()
    f.close()
    return content


def exists(file_name) -> bool:
    return os.path.exists(file_name)