#!/usr/bin/env python3


# Import Dependencies
import curses
import random


# Define Functions
def get_random_food_position(snake: list, x_limit: tuple, y_limit: tuple) -> tuple:
    food_position = None
    while food_position is None:
        food_position = (
            random.randint(min(y_limit), max(y_limit) - 1),
            random.randint(min(x_limit), max(x_limit) - 1)
        )
        if food_position in snake:
            food_position = None
    return food_position


def get_new_head(key: int, head_x: int, head_y: int, MOVEMENT_KEYS: list) -> tuple:
    if key == MOVEMENT_KEYS[0]:
        head_x -= 1
    elif key == MOVEMENT_KEYS[1]:
        head_y += 1
    elif key == MOVEMENT_KEYS[2]:
        head_y -= 1
    else:
        head_x += 1
    return (head_y, head_x)


def reset_game(stdscr, GRID, MOVEMENT_KEYS, FOOD_CHAR) -> tuple:
    snake = [(GRID[0] // 2, GRID[1] // 2)]
    food = get_random_food_position(snake, (1, GRID[1] - 1), (1, GRID[0] - 1))
    stdscr.addch(food[0], food[1], FOOD_CHAR)
    key = random.choice(MOVEMENT_KEYS)
    foo = ' Score: 0 '
    stdscr.addstr(0, GRID[1] // 2 - len(foo) // 2, foo)
    return (snake, food, key)


def main(stdscr):
    # Constants (Y, X)
    GRID = (20, 40)
    TERM = stdscr.getmaxyx()
    OFFSET = ((TERM[0] - GRID[0]) // 2, (TERM[1] - GRID[1]) // 2)
    SNAKE_CHAR, FOOD_CHAR = '#', '*'
    KEY_Q = 113
    MOVEMENT_KEYS = (104, 106, 107, 108) # HJKL

    # Window Setup
    curses.curs_set(False)
    stdscr.nodelay(True)
    stdscr.timeout(120)
    stdscr.resize(GRID[0], GRID[1])
    stdscr.mvwin(OFFSET[0], OFFSET[1])
    stdscr.border()

    # Initialization
    snake, food, key = reset_game(stdscr, GRID, MOVEMENT_KEYS, FOOD_CHAR)

    # Main Loop
    while True:
        # Handle Key Input
        new_key = stdscr.getch()
        if new_key == KEY_Q:
            break
        elif new_key in MOVEMENT_KEYS:
            key = new_key

        # Move Snake
        new_head = get_new_head(key, snake[0][1], snake[0][0], MOVEMENT_KEYS)
        snake.insert(0, new_head)
        stdscr.addch(snake[0][0], snake[0][1], SNAKE_CHAR)

        # Delete or Keep Tail
        if snake[0] == food:
            food = get_random_food_position(snake, (1, GRID[1] - 1), (1, GRID[0] - 1))
            stdscr.addch(food[0], food[1], FOOD_CHAR)
            # Show Score
            score_output = f' Score: {len(snake) - 1} '
            stdscr.addstr(0, GRID[1] // 2 - len(score_output) // 2, score_output)
        else:
            stdscr.addch(snake[-1][0], snake[-1][1], ' ')
            snake.pop()

        # Reset Condition
        if (new_head[0] in (0, GRID[0] - 1) or
            new_head[1] in (0, GRID[1] - 1) or
            snake[0] in snake[1:]):
            stdscr.clear()
            stdscr.border()
            snake, food, key = reset_game(stdscr, GRID, MOVEMENT_KEYS, FOOD_CHAR)


if __name__ == '__main__':
    curses.wrapper(main)
    print('Game Over!')
