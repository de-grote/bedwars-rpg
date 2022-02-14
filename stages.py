from typing import Any


class Stages:
    stages: dict[int: dict[str: Any]] = {
        0: {
            "platforms": {
                ("bedrock.png", (144, 128), (16, 16)),
                ("bedrock.png", (128, 112), (16, 16)),
                ("bedrock.png", (96, 128), (16, 16)),
                ("bedrock.png", (112, 112), (16, 16)),
                ("bed.png", (112, 135), (32, 9)),
            },
            "occupied": {
                (6, 8), (7, 8), (8, 8), (9, 8), (7, 7), (8, 7),
            },
            "cam": {
                "x": 0,
                "y": 0,
                "max_x": None,
                "min_x": None,
                "max_y": None,
                "min_y": 0,
            },
            "player": {
                "x": 0,
                "y": 0,
            }
        }
    }
