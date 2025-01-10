from enum import Enum
from typing import List
from dataclasses import dataclass


class Games(Enum):
    CALL_OF_DUTY_WORLD_AT_WAR = 'Call of Duty World at War'
    CALL_OF_DUTY_MODERN_WARFARE_II = 'Call of Duty Modern Warfare II'
    CALL_OF_DUTY_MODERN_WARFARE_III = 'Call of Duty Modern Warfare III'
    CALL_OF_DUTY_BLACK_OPS_I = 'Call of Duty Black Ops I'
    CALL_OF_DUTY_BLACK_OPS_II = 'Call of Duty Black Ops II'
    CALL_OF_DUTY_GHOSTS = 'Call of Duty Ghosts'
    CALL_OF_DUTY_ADVANCED_WARFARE = 'Call of Duty Advanced Warfare'


class GameModes(Enum):
    SINGLE_PLAYER = 'Single Player'
    MULTIPLAYER = 'Multiplayer'
    ALL = 'All'


class GameClients(Enum):
    ALTERWARE = 'AlterWare'
    PLUTONIUM = 'Plutonium'


@dataclass
class GameMode:
    game_mode: str
    arg: str
    client: GameClients


@dataclass
class Game:
    game: Games
    game_modes: List[GameMode]


def get_enum_from_val(enum: Enum, value: str) -> Enum:
    for member in enum:
        if member.value == value:
            return member
    return None


def get_enum_strings_from_enum(enum: Enum) -> list[str]:
    strings = []
    for entry in enum:
        strings.append(entry.value)
    return strings


games_info = [
    Game(
        game=Games.CALL_OF_DUTY_WORLD_AT_WAR,
        game_modes=[
            GameMode(
                game_mode=GameModes.SINGLE_PLAYER,
                arg = 't4sp',
                client=GameClients.PLUTONIUM
            ),
            GameMode(
                game_mode=GameModes.MULTIPLAYER,
                arg = 't4mp',
                client=GameClients.PLUTONIUM
            ),
        ]
    ),
    Game(
        game=Games.CALL_OF_DUTY_MODERN_WARFARE_II,
        game_modes=[
            GameMode(
                game_mode=GameModes.SINGLE_PLAYER,
                arg = 'iw4-sp',
                client=GameClients.ALTERWARE
            ),
            GameMode(
                game_mode=GameModes.MULTIPLAYER,
                arg = 'iw4x',
                client=GameClients.ALTERWARE
            ),
        ]
    ),
    Game(
        game=Games.CALL_OF_DUTY_MODERN_WARFARE_III,
        game_modes=[
            GameMode(
                game_mode=GameModes.SINGLE_PLAYER,
                arg = 'iw5-mod',
                client=GameClients.ALTERWARE
            ),
            GameMode(
                game_mode=GameModes.MULTIPLAYER,
                arg = 'iw5mp',
                client=GameClients.PLUTONIUM
            ),
        ]
    ),
    Game(
        game=Games.CALL_OF_DUTY_BLACK_OPS_I,
        game_modes=[
            GameMode(
                game_mode=GameModes.SINGLE_PLAYER,
                arg = 't5sp',
                client=GameClients.PLUTONIUM
            ),
            GameMode(
                game_mode=GameModes.MULTIPLAYER,
                arg = 't5mp',
                client=GameClients.PLUTONIUM
            ),
        ]
    ),
    Game(
        game=Games.CALL_OF_DUTY_BLACK_OPS_II,
        game_modes=[
            GameMode(
                game_mode=GameModes.SINGLE_PLAYER,
                arg = 't6zm',
                client=GameClients.PLUTONIUM
            ),
            GameMode(
                game_mode=GameModes.MULTIPLAYER,
                arg = 't6mp',
                client=GameClients.PLUTONIUM
            ),
        ]
    ),
    Game(
        game=Games.CALL_OF_DUTY_GHOSTS,
        game_modes=[
            GameMode(
                game_mode=GameModes.ALL,
                arg = 'iw6-mod',
                client=GameClients.ALTERWARE
            )
        ]
    ),
    Game(
        game=Games.CALL_OF_DUTY_ADVANCED_WARFARE,
        game_modes=[
            GameMode(
                game_mode=GameModes.ALL,
                arg = 's1-mod',
                client=GameClients.ALTERWARE
            )
        ]
    )
]
