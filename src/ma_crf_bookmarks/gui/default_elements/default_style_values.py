from enum import Enum


class DefaultFont(Enum):
    family: str = "Calibri"
    size: int = 20


class DefaultBorder(Enum):
    radius: int = 10
    color: str = "#000000"
    size: int = 2
    padding: int = 5


class DefaultColors(Enum):
    light_blue: str = "#66C7FF"
    dark_blue: str = "#0043BF"
    dark_grey: str = "#404040"
    light_grey: str = "#D9D9D9"
    red: str = "#E38687"
    pure_white: str = "#FFFFFF"
    pure_black: str = "#000000"
