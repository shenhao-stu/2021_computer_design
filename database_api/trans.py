# -*- coding: utf-8 -*-
import os
from zhconv import convert_for_mw

POETRY_DIRECTORY = './add_poetry/'


def trans(name):
    file_path = os.path.join(POETRY_DIRECTORY, name)

    raw = open(file_path, 'r', encoding='utf-8').read()

    content = convert_for_mw(raw, 'zh-cn')

    output_path = os.path.join('./simplify_poetry/', name)
    print(output_path)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)


def main():
    print("Waiting to trans......")
    # os.listdir(POETRY_DIRECTORY) is a list type
    # map(function, iterable)
    if list(map(trans, os.listdir(POETRY_DIRECTORY))):
        print("Success trans!")


if __name__ == "__main__":
    main()
