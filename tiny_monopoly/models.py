"""
tiny_monopoly.models
~~~~~~~~~~~~~~~
This module contains the primary objects that power Tiny Monopoly.
"""

import random

from abc import abstractmethod
from operator import attrgetter
from typing import List


class Dice:
    def __init__(self):
        self._faces: range = range(1, 7)

    @property
    def faces(self) -> range:
        return self._faces

    def roll(self) -> int:
        return random.choice(self.faces)


class Player:
    def __init__(self):
        self._dice: Dice = None
        self._budget: int = 300
        self._position: int = 0

    def __repr__(self):
        return self.__class__.__name__

    @property
    def position(self) -> int:
        return self._position

    @position.setter
    def position(self, position: int):
        if position is None or position < 0:
            raise ValueError("Positon must be a valid positive or zero number")
        self._position = position

    @property
    def dice(self) -> Dice:
        return self._dice

    @dice.setter
    def dice(self, dice: Dice) -> None:
        if dice is None:
            raise ValueError("Dice must be a valid Dice")
        self._dice = dice

    @property
    def budget(self) -> int:
        return self._budget

    @budget.setter
    def budget(self, budget: int) -> None:
        if budget is None:
            raise ValueError("Budget must be a valid number")
        self._budget = budget

    @abstractmethod
    def should_buy_property(self, property: "Property") -> bool:
        raise NotImplementedError

    def must_pay_rent(self, property: "Property") -> bool:
        if property.has_owner() and property.owner != self:
            return True
        return False

    def has_budget(self, property: "Property") -> bool:
        if property.price <= self.budget:
            return True
        return False

    def pay_rent(self, property: "Property") -> None:
        self.budget -= property.rental_price
        property.owner.budget += property.rental_price

    def buy_property(self, property: "Property") -> None:
        self.budget -= property.price
        property.owner = self


class ImpulsivePlayer(Player):
    def should_buy_property(self, property: "Property") -> bool:
        return self.has_budget(property) and not property.has_owner()


class StrictPlayer(Player):
    def should_buy_property(self, property: "Property") -> bool:
        return (
            self.has_budget(property)
            and not property.has_owner()
            and property.rental_price > 50
        )


class CautiousPlayer(Player):
    def should_buy_property(self, property: "Property") -> bool:
        return (
            self.has_budget(property)
            and not property.has_owner()
            and (self.budget - property.price) > 80
        )


class RandomPlayer(Player):
    def should_buy_property(self, property: "Property") -> bool:
        return (
            self.has_budget(property)
            and not property.has_owner()
            and random.choice([True, False])
        )


class Property:
    def __init__(self):
        self._owner: Player = None
        self._price: int = random.randint(15, 300)
        self._rental_price: int = random.randint(15, 200)

    @property
    def owner(self) -> Player:
        return self._owner

    @owner.setter
    def owner(self, owner: Player) -> None:
        if owner is not None and not isinstance(owner, Player):
            raise ValueError("Owner must be a valid Player")
        self._owner = owner

    def has_owner(self) -> bool:
        return self.owner is not None

    @property
    def price(self) -> int:
        return self._price

    @property
    def rental_price(self) -> int:
        return self._rental_price


class Match:
    def __init__(self, max_turns: int):
        self._board: List[Property] = []
        self._players: List[Player] = []
        self.max_turns: int = max_turns
        self.played_turns: int = 0
        self.dice: Dice = Dice()

    @property
    def board(self) -> List[Property]:
        return self._board

    @board.setter
    def board(self, properties: List[Property]) -> None:
        if properties is None:
            raise ValueError("Properties must be a valid list of Properties")
        self._board = properties

    @property
    def players(self) -> List[Player]:
        return self._players

    @players.setter
    def players(self, players: List[Player]) -> None:
        if players is None:
            raise ValueError("Players must be a valid list of Players")
        random.shuffle(players)
        self._players = players

    @property
    def winner(self) -> Player:
        return max(self.players, key=attrgetter("budget"))

    def has_winner(self) -> bool:
        return len(self.players) <= 1

    def player_is_broken(self, player: Player) -> bool:
        return player.budget <= 0

    def remove_player(self, player: Player) -> None:
        for property in self.board:
            if property.owner == player:
                property.owner = None
        self.players.remove(player)

    def player_completed_board_path(self, player: Player) -> bool:
        if player.position >= 20:
            player.position = player.position % 20
            return True
        return False

    def gives_player_extra_budget(self, player: Player) -> None:
        player.budget += 100

    def start(self) -> None:
        while not self.has_winner():
            for player in self.players:
                player.dice = self.dice
                player.position += player.dice.roll()

                if self.player_completed_board_path(player):
                    self.gives_player_extra_budget(player)

                property = self.board[player.position]
                if player.must_pay_rent(property):
                    player.pay_rent(property)
                elif player.should_buy_property(property):
                    player.buy_property(property)

                if self.player_is_broken(player):
                    self.remove_player(player)

                if self.has_winner():
                    break

            self.played_turns += 1
            if self.played_turns == 1000:
                break
