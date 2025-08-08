import os
import random
import time

type Field = list[list[bool]]

# Vertical screen w,h
# size: tuple[int, int] = 176, 160
# Horizontal screen w,h
size: tuple[int, int] = int(316 * 1.59999), int(86 * 1.59999)
# Laptop screen w,h
# size: tuple[int, int] = 236, 63


def get_clear_field() -> Field:
    return [[False for _ in range(size[0])] for _ in range(size[1])]


def gen_random() -> Field:
    size_square: int = (size[0] + size[1]) // 2
    offsets: int = size[0]

    new_field: Field = get_clear_field()

    l1: int = size[1] // 2 - offsets
    h1: int = size[1] // 2 + offsets

    l2: int = size[0] // 2 - offsets
    h2: int = size[0] // 2 + offsets

    for _ in range(random.randint(size_square - offsets, size_square + offsets) * (size[0] // 30)):
        new_field[random.randint(l1, h1) % size[1]][random.randint(l2, h2) % size[0]] = True

    return new_field


def cycle(filed: Field) -> tuple[Field, int]:
    actions = 0
    next_filed: Field = get_clear_field()
    for y, line in enumerate(filed):
        for x, cell in enumerate(line):
            alive_neighbors: int = [
                *[filed[(y + 1) % size[1]][(x + x_off) % size[0]] for x_off in range(-1, 2)],
                *[filed[(y - 1) % size[1]][(x + x_off) % size[0]] for x_off in range(-1, 2)],
                filed[y][(x - 1) % size[0]],
                filed[y][(x + 1) % size[0]],
            ].count(True)

            if alive_neighbors == 2:
                next_filed[y][x] = cell
                actions += 1
            elif alive_neighbors == 3:
                next_filed[y][x] = True
                actions += 1
            else:
                next_filed[y][x] = False
    return next_filed, actions


def read_form(path: str = "form.gol") -> Field:
    with open(f"forms/{path}", "r") as file:
        return [[True if c != "." else False for c in list(line.strip("\n"))] for line in file.readlines()]


def a(filed: Field, figure: Field, offset: tuple[int, int]) -> Field:
    for y, line in enumerate(figure):
        for x, cell in enumerate(line):
            filed[y + offset[1]][x + offset[0]] = cell

    return filed


steps = 0
last_moves: list[int] = []
filed: Field = get_clear_field()


# filed = gen_random()
form: Field = read_form(path="test.gol")

# filed = a(filed=filed, figure=form, offset=(0, 0))
filed = a(filed=filed, figure=form, offset=(size[0] // 2, size[1] // 2 - 8))

highest_step_count: int = 0
try:
    while True:
        steps += 1
        os.system(command="clear")
        print("\n".join(["".join(["#" if cell else " " for cell in line]) for line in filed]))
        if steps == 1:
            input("Press Enter to start")

        filed, actions = cycle(filed=filed)
        last_moves.append(actions)

        if steps % 100 and False:
            if last_moves.count(actions) > 50:
                highest_step_count = steps if highest_step_count < steps else highest_step_count
                steps = 0
                last_moves = []
                filed: Field = get_clear_field()
                filed = gen_random()
                print(f"not enough action. Highest steps so far:{highest_step_count}")
                time.sleep(1)

except KeyboardInterrupt:
    print(f"{highest_step_count=}")
