import unittest
import random

from tiny_monopoly.models import (
    Property,
    Player,
    Dice,
    ImpulsivePlayer,
    StrictPlayer,
    CautiousPlayer,
    RandomPlayer,
    Match,
)


class DiceTestCase(unittest.TestCase):
    def test_dice_roll(self):
        random.seed(10)
        dice = Dice()
        assert dice.roll() == 5
        assert dice.roll() == 1


class PlayerTestCase(unittest.TestCase):
    def test_player_should_buy_property(self):
        player = Player()
        with self.assertRaises(NotImplementedError):
            player.should_buy_property(None)

    def test_player_must_pay_rent(self):
        player1 = Player()
        property = Property()
        property.owner = player1
        player2 = Player()
        assert player2.must_pay_rent(property) == True
        property.owner = player2
        assert player2.must_pay_rent(property) == False


class ImpulsivePlayerTestCase(unittest.TestCase):
    def test_player_should_but_property(self):
        property = Property()
        impulsive_player = ImpulsivePlayer()
        assert impulsive_player.should_buy_property(property) == True
        impulsive_player.budget = 0
        assert impulsive_player.should_buy_property(property) == False


class StrictPlayerTestCase(unittest.TestCase):
    def test_player_should_but_property(self):
        random.seed(200)
        property = Property()
        strict_player = StrictPlayer()
        assert strict_player.should_buy_property(property) == True
        random.seed(90000000000)
        property2 = Property()
        assert strict_player.should_buy_property(property2) == False


class CautiousPlayerTestCase(unittest.TestCase):
    def test_player_should_but_property(self):
        random.seed(100)
        property = Property()
        cautious_player = CautiousPlayer()
        assert cautious_player.should_buy_property(property) == True
        random.seed(9)
        property2 = Property()
        assert cautious_player.should_buy_property(property2) == False


class RandomPlayerTestCase(unittest.TestCase):
    def test_player_should_but_property(self):
        random.seed(99)
        property = Property()
        random_player = RandomPlayer()
        assert random_player.should_buy_property(property) == True
        random.seed(100)
        property2 = Property()
        assert random_player.should_buy_property(property2) == False


class PropertyTestCase(unittest.TestCase):
    def test_property_has_owner(self):
        property = Property()
        assert property.has_owner() == False
        property.owner = Player()
        assert property.has_owner() == True

    def test_property_price(self):
        random.seed(300)
        property = Property()
        assert property.price == 197

    def test_property_rental_price(self):
        random.seed(200)
        property = Property()
        assert property.rental_price == 67


class MatchTestCase(unittest.TestCase):
    def test_match_result(self):
        random.seed(1000)
        players = [
            ImpulsivePlayer(),
            StrictPlayer(),
            CautiousPlayer(),
            RandomPlayer(),
        ]
        match = Match(1000)
        match.players = players
        board = [Property() for i in range(20)]
        match.board = board
        match.start()
        player = ImpulsivePlayer()
        winner = match.winner
        assert isinstance(winner, type(player)) == True
