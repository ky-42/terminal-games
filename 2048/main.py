from enum import Enum
from random import choice, randint
from typing import List, Optional, Tuple


class Direction(Enum):
    """Enum representing the four directions in the game."""

    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4


class Game:
    """Game of 2048.

    Class Variables (private):
        ROWS (int): Number of rows in the game grid.
        COLS (int): Number of columns in the game grid.

    Attributes (private):
        grid (2D int list): 2D list representing the game grid.
    """

    __ROWS: int = 4
    __COLS: int = 4

    def __init__(self, grid: Optional[List[List[int]]] = None) -> None:
        # Create new grid
        if grid is None:
            self.__grid = [[0 for _ in range(Game.__COLS)] for _ in range(Game.__ROWS)]

            # Add starting tiles
            for _ in range(2):
                self.__place_random_tile()

        # Use existing grid
        else:
            if len(grid) != Game.__ROWS or any(len(row) != Game.__COLS for row in grid):
                raise ValueError("Invalid grid dimensions")

            self.__grid = grid

    def __str__(self) -> str:
        return "\n".join([str(row) for row in self.__grid]) + "\n"

    def get_grid(self) -> List[List[int]]:
        return self.__grid

    def get_biggest_block(self) -> int:
        biggest_block = 0

        for y in range(Game.__ROWS):
            for x in range(Game.__COLS):
                biggest_block = max(biggest_block, self.__grid[y][x])

        return biggest_block

    def make_move(self, direction: Direction) -> Tuple[int, bool]:
        """Makes a move in the game.

        Args:
            direction (Direction): Direction to move the tiles.

        Returns:
            Tuple[int, bool]: Score generated by the move and if the game is over.
                True if the game is over, False otherwise.
        """

        move_score, moved = self.__move_tiles(direction)

        if moved:
            empty_space = self.__place_random_tile()

            # Game can only be over if no empty spaces are left
            if not empty_space:
                return (move_score, self.__check_game_over())

        return (move_score, False)

    def __move_tiles(self, direction: Direction) -> Tuple[int, bool]:
        """Moves the tiles in the game grid in a given direction.

        Args:
            direction (Direction): Direction to move the tiles.

        Returns:
            Tuple[int, bool]: Score generated by the move, and if any tiles were moved
                in the turn.
        """

        move_score = 0

        to_combine: List[List[int]] = []

        if direction == Direction.UP or direction == Direction.DOWN:
            # Get columns
            for x in range(Game.__COLS):
                to_combine.append([self.__grid[y][x] for y in range(Game.__ROWS)])
        else:
            to_combine = self.__grid

        # Down is combined as right and up is combined as left
        # This is because columns are combined as if the grid is rotated 90 degrees clockwise
        combine_right = direction == Direction.RIGHT or direction == Direction.DOWN

        moved = False

        for merge_index in range(len(to_combine)):

            combined_tiles, merge_score, move = self.__combine_tiles(
                to_combine[merge_index], combine_right
            )

            moved = moved or move

            move_score += merge_score

            for merged_tile_index in range(len(combined_tiles)):
                if direction == Direction.UP or direction == Direction.DOWN:
                    # Set columns
                    self.__set_tile(
                        x=merge_index,
                        y=merged_tile_index,
                        value=combined_tiles[merged_tile_index],
                    )
                else:
                    # Set rows
                    self.__set_tile(
                        x=merged_tile_index,
                        y=merge_index,
                        value=combined_tiles[merged_tile_index],
                    )

        return (move_score, moved)

    def __combine_tiles(
        self, tiles: List[int], right: bool
    ) -> Tuple[List[int], int, bool]:
        """Combines a list of tiles in a given direction.

        Args:
            tiles (List[int]): List of tiles to combine.
            right (bool): If the tiles should be combined to the right.

        Returns:
            Tuple[List[int], int, bool]: List of tiles after combining, the score generated
                and if there was and movement in the tiles.
        """

        merge_score = 0

        old_tiles = tiles.copy()

        # Remove zeros and reverse if moving right
        if right:
            tiles = [tile for tile in tiles[::-1] if tile != 0]
        else:
            tiles = [tile for tile in tiles if tile != 0]

        # Combine tiles
        current_tile = 0
        while current_tile < len(tiles) - 1:
            if tiles[current_tile] == tiles[current_tile + 1]:
                tiles[current_tile] *= 2
                merge_score += tiles[current_tile]
                tiles.pop(current_tile + 1)

            current_tile += 1

        # Add zeros back
        tiles += [0] * (Game.__COLS - len(tiles))

        if right:
            tiles.reverse()

        return (tiles, merge_score, old_tiles != tiles)

    def __place_random_tile(self) -> bool:
        """Adds a random tile to the game grid.

        Returns:
            bool: True if there are empty spaces remaining, False otherwise.
                Also returns False if no tile was added because there were no spaces.
        """

        added_value = 2 if randint(0, 9) > 0 else 4

        potential_coords: List[Tuple[int, int]] = []

        for y in range(Game.__ROWS):
            for x in range(Game.__COLS):
                if self.__grid[y][x] == 0:
                    potential_coords.append((x, y))

        if not potential_coords:
            return False

        x, y = choice(potential_coords)

        self.__set_tile(x, y, added_value)

        return bool(len(potential_coords) - 1)

    def __set_tile(self, x: int, y: int, value: int) -> None:
        """Sets the value of a tile in the game grid.

        Args:
            x (int): X coordinate of the tile.
            y (int): Y coordinate of the tile.
            value (int): Value of the tile.

        Raises:
            ValueError: If the tile position is invalid or the value is not a power of 2.
        """

        if value % 2 != 0:
            raise ValueError("Tile value must be a power of 2")

        if 0 <= x < Game.__COLS and 0 <= y < Game.__ROWS:
            self.__grid[y][x] = value

        else:
            raise ValueError("Invalid tile position")

    def __check_game_over(self) -> bool:
        """Checks if the game is over. Only works if there are no empty spaces left.

        Returns:
            bool: True if the game is over, False otherwise.
        """

        for y in range(Game.__ROWS):
            for x in range(Game.__COLS - 1):
                if self.__grid[y][x] == self.__grid[y][x + 1]:
                    return False

        for y in range(Game.__ROWS - 1):
            for x in range(Game.__COLS):
                if self.__grid[y][x] == self.__grid[y + 1][x]:
                    return False

        return True

    @staticmethod
    def get_dimensions() -> Tuple[int, int]:
        """Returns the dimensions of the game grid in form (rows, columns)."""

        return (Game.__ROWS, Game.__COLS)


    def __str__(self) -> str:

        max_num_length = max(map(lambda x: max(map(lambda y: len(str(y)), x)), self.__grid))
        square_size = max_num_length + 2

        row_size = square_size * Game.__COLS + Game.__COLS + 1

        final = "-" * row_size + "\n"

        for row in self.__grid:
            for square in row:
                final += f"|{square:^{square_size}}"
            final += "|\n" + "-" * row_size + "\n"

        return final


if __name__ == "__main__":
    print("Welcome to 2048!")
    print("Enter w to move up, s for down, a for left, and d for right. To exit the game enter q.\n")

    score = 0

    game = Game()
    print(f"Current Score: {score}")
    print(game)

    while True:
        move = input("Enter move: ")
        move = move.lower()

        if move == "w":
            add_score, game_over = game.make_move(Direction.UP)
        elif move == "s":
            add_score, game_over = game.make_move(Direction.DOWN)
        elif move == "a":
            add_score, game_over = game.make_move(Direction.LEFT)
        elif move == "d":
            add_score, game_over = game.make_move(Direction.RIGHT)
        elif move == "q":
            break
        else:
            print()
            print("Please enter valid move\n")
            continue
        
        score += add_score

        if game_over:
            print()
            print(f"Game is over! Your score was {score}!")
            restart_input = input("Would you like to play again? [y/n] ")

            if restart_input == "y":
                score = 0
                game = Game()

                print()
                print(f"Current Score: {score}")
                print(game)

                continue
            else:
                break

        print()
        print(f"Current Score: {score}")
        print(game)

    print()
    print("Thanks for playing")
