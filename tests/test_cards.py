import unittest
import pycards
import random

from hypothesis import strategies, given, settings

import logging
logger = logging.getLogger('PyCardsTesting')
logging.basicConfig()
logger.setLevel('DEBUG')

std_deck_size = 52

class PyCardsTest(unittest.TestCase):
 
    @settings(max_examples=20)
    @given(n_cards = strategies.integers(min_value=1, max_value=30))
    def test_draw(self, n_cards):
        deck_orig = pycards.Deck()
        deck_orig.draw_hand(n_cards)
        logger.debug('TestDraw: Deck: {}, Expected: {}\n'.format(deck_orig.get_ncards_deck(), std_deck_size-n_cards))
        assert deck_orig.get_ncards_deck() == std_deck_size-n_cards

    @settings(max_examples=20)
    @given(n_cards   = strategies.integers(min_value=1, max_value=10),
           is_random = strategies.booleans(),
           new_deck  = strategies.booleans())
    def test_discard(self, n_cards, new_deck, is_random):
        deck_orig = pycards.Deck()
        hand_orig = deck_orig.draw_hand(20)
        if new_deck:
            discard_pile = pycards.Deck(empty=True)
            hand_orig.discard(n=n_cards,
                                   to_deck = discard_pile,
                                   random=is_random)
            logger.debug('TestDiscard: Deck: {}, Expected: {}\n'.format(discard_pile.get_ncards_deck(), n_cards))
            assert discard_pile.get_ncards_deck() == n_cards
        else:
            hand_orig.discard(n=n_cards,random=is_random)
            logger.debug('TestDiscard: Deck: {}, Expected: {}\n'.format(deck_orig.get_ncards_deck(), 
                                                                     std_deck_size-20+n_cards))
            assert deck_orig.get_ncards_deck() == std_deck_size-20+n_cards
        logger.debug('TestDiscard: Hand: {}, Expected: {}\n'.format(len(hand_orig._cards), 20-n_cards))
        assert len(hand_orig._cards) == 20-n_cards

    @settings(max_examples=20)
    @given(new_dict = strategies.booleans(),
           ace_high = strategies.booleans(),
           n_cards  = strategies.integers(min_value=1,max_value=10))
    def test_score(self, new_dict, ace_high, n_cards):
        my_deck = pycards.Deck()
        if new_dict:
            dict_score = {}
            for i in [j for j in range(0,11)]+['A','K','Q','J']:
                dict_score[i] = random.randint(0,30)
            for k in range(n_cards):
                card = my_deck.draw()
                card.score(score_dict=dict_score)
        else:
            for k in range(n_cards):
                card = my_deck.draw()
                card.score(ace_high=ace_high)

if __name__ in "__main__":
    unittest.main()
