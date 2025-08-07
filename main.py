import random
import time

# Vertical screen w,h
size: tuple[int, int] = 176, 160
# Horizontal screen w,h
# size: tuple[int, int] = 316, 86
# Laptop screen w,h
# size: tuple[int, int] = 236, 63


filed: list[list[bool]] = [[False for _ in range(size[0])] for _ in range(size[1])]
# filed[0][0] = True


def gen_random() -> None:
    size_square: int = (size[0] + size[1]) // 2
    offsets: int = size[0]

    for _ in range(random.randint(size_square - offsets, size_square + offsets) * (size[0] // 10)):
        filed[random.randint(size[1] // 2 - offsets, size[1] // 2 + offsets) % size[1]][
            random.randint(size[0] // 2 - offsets, size[0] // 2 + offsets) % size[0]
        ] = True


# def is_empty() -> bool:
#     for line in filed:
#         for cell in line:
#             if cell:
#                 return False
#     return True


def cycle(filed: list[list[bool]]) -> tuple[list[list[bool]], int]:
    actions = 0
    next_filed: list[list[bool]] = [[False for _ in range(size[0])] for _ in range(size[1])]
    for y, line in enumerate(filed):
        for x, _ in enumerate(line):
            top: list[bool] = [filed[(y + 1) % size[1]][(x + x_off) % size[0]] for x_off in range(-1, 2)]
            bottom: list[bool] = [filed[(y - 1) % size[1]][(x + x_off) % size[0]] for x_off in range(-1, 2)]

            left: bool = filed[y][(x - 1) % size[0]]
            right: bool = filed[y][(x + 1) % size[0]]

            alive_neighbors: int = [*top, *bottom, left, right].count(True)

            if alive_neighbors == 2:
                next_filed[y][x] = filed[y][x]
                actions += 1
            elif alive_neighbors == 3:
                next_filed[y][x] = True
                actions += 1
            else:
                next_filed[y][x] = False
    return next_filed, actions


gen_random()

steps = 0
last_moves: list[int] = []

highest_step_count: int = 0
try:
    while True:
        steps += 1
        for line in filed:
            for row in line:
                print("+" if row else " ", end="", flush=False)
            print(flush=False)
        print(flush=True)
        # time.sleep(0.1)

        # input()

        filed, actions = cycle(filed=filed)
        last_moves.append(actions)
        if steps > 100:
            if last_moves.count(actions) > 50:
                if highest_step_count < steps:
                    highest_step_count = steps
                steps = 0
                last_moves = []
                gen_random()
                print(f"not enough action. Highest steps so far:{highest_step_count}")
                time.sleep(1)
except KeyboardInterrupt:
    print(f"{highest_step_count=}")
