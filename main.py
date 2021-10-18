from game_of_life import GameOfLife


def main():
    game = GameOfLife(500, 500, 100, 100, True)

    game.main_loop()


if __name__ == '__main__':
    main()
