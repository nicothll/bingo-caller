import os
import pickle
import random
import pandas as pd


class BingoGame:
    """A class representing a Bingo 75 game.

    This class provides a simple implementation of the Bingo 75 game. The game
    contains a set of 75 numbers divided into 5 letters: B, I, N, G, and O.

    Attributes
    ----------
    (class)BINGO_75: Dict[str, Tuple[int, int]] - A dictionary holding the range of
            numbers for each letter of the Bingo 75 game.
    (class) SAVE_FILE: str - A string representing the file path to save the game state.
    all_numbers: list[str] - Store the set of numbers used in the game.
    table_numbers: pandas.DataFrame - Store the set of letters and numbers into a DataFrame.
    called_numbers: list[str] - Keeps track of the called numbers during the game.

    Methods
    -------
    init_game() : Initialize the numbers of Bingo 75.
    save_game(Optional[filename]) : Save the state of the game into file.
    load_game(Optional[filename]) : Load the file.
    call() : Call number.
    reset() : Reset the list of numbers called.
    """

    BINGO_75 = {
        "B": (1, 16),
        "I": (16, 31),
        "N": (31, 46),
        "G": (46, 61),
        "O": (61, 76),
    }
    SAVE_FILE = "./.bingo.pkl"

    def __init__(self) -> None:
        """Initialize a new Bingo 75 game."""
        self._all_numbers = list()
        self._table_numbers = dict()
        self._called = list()

        self.init_game()

    def init_game(self) -> None:
        """Initialize the numbers of Bingo 75"""

        for letter, nb_range in self.BINGO_75.items():
            for nb in range(*nb_range):
                self._all_numbers.append(letter + str(nb))
            self._table_numbers[letter] = [nb for nb in range(*self.BINGO_75[letter])]

    def save_game(self, filename: str = SAVE_FILE) -> bool:
        """Save numbers called into a file

        :param filename: str - Name of the file
        :return: bool - Is it successful?
        """

        with open(filename, "wb") as f:
            pickle.dump(self._called, f)
            print(f"{filename} successfully saved")
            return True

    def load_game(self, filename: str = SAVE_FILE) -> bool:
        """Load the numbers of the previous game.

        :param filename: str - Name of the saving file (Optional)
        :return: bool - The file was loaded
        """
        if os.path.exists(filename):
            if filename.endswith(".txt"):
                with open(filename, "r") as f:
                    data = []
                    for line in f.readlines():
                        data.append(line.strip())
                self._called = data

            else:
                with open(filename, "rb") as f:
                    self._called = pickle.load(f)
            return True
        else:
            return False

    def call(self) -> str:
        """Return a pseudo-random Bingo number

        :return: str - Bingo number called
        """
        number = random.choice(list(set(self._all_numbers) - set(self._called)))
        self._called.append(number)
        return number

    def reset(self) -> None:
        """Resets the list of numbers called"""
        self._called = list()

    def __color_cells(self, val):
        """
        Color cells based on the called numbers.

        :param val: int - The value of the cell to be colored
        :return: str - A string representing the CSS style for the cell.
        """
        called_nbs = [int(nb[1:]) for nb in self._called]
        color = "#1d6c3c" if val in called_nbs else ""
        return f"background-color: {color}"

    @property
    def all_numbers(self) -> list[str]:
        """Return the list of all numbers in the Bingo 75 game.

        :return: list[str] - A list of strings representing the all numbers in the game.
        """
        return self._all_numbers

    @property
    def table_numbers(self) -> pd.DataFrame:
        """Return a DataFrame  of all numbers in the Bingo 75 game.

        The background color of each cell in the DataFrame is
        determined by the `__color_cells` method.

        :return: pandas.DataFrance - A pandas DataFrame representing the Bingo 75 game table numbers.
        """
        df = pd.DataFrame(self._table_numbers)
        return df.style.applymap(self.__color_cells)

    @property
    def called_numbers(self) -> list[str]:
        """Return the list of called numbers in the Bingo 75 game.

        :return: list[str] - A list of strings representing the called numbers during the game.
        """
        return self._called
