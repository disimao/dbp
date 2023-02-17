from pprint import pprint
from collections import Counter

from .models import (
    Property,
    ImpulsivePlayer,
    StrictPlayer,
    CautiousPlayer,
    RandomPlayer,
    Match,
)


SIMULATION_NUMBERS = 300
PROPERTY_NUMBERS = 20
MAX_TURNS = 1000


def victory_percentage_by_player(winners_list):
    counter = Counter(winners_list)
    list_size = len(winners_list)
    return dict(
        [
            (item, "{:0.2f}%".format((counter[item] * 100) / list_size))
            for item in counter
        ]
    )


if __name__ == "__main__":
    stats = {
        "played_turns": [],
        "winners": [],
    }

    for i in range(SIMULATION_NUMBERS):
        players = [
            ImpulsivePlayer(),
            StrictPlayer(),
            CautiousPlayer(),
            RandomPlayer(),
        ]
        board = [Property() for i in range(PROPERTY_NUMBERS)]
        match = Match(MAX_TURNS)
        match.players = players
        match.board = board
        match.start()
        stats["winners"].append(str(match.winner))
        stats["played_turns"].append(match.played_turns)

    print("Timed out matches:", stats["played_turns"].count(MAX_TURNS))
    print(
        "Average played turns by matches:",
        sum(stats["played_turns"]) / SIMULATION_NUMBERS,
    )
    print(
        "Vitory percentage by players' behavior:",
    )
    pprint(victory_percentage_by_player(stats["winners"]))
    print(
        "Top winner player:", max(stats["winners"], key=stats["winners"].count)
    )
