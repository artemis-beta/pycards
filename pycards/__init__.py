from random import shuffle, randint

import logging

logging.basicConfig()

class Card(object):
    def __init__(self, suit, num):
        '''
        Single playing card object

        Arguments
        ---------

        suit   string      Card suit, e.g. 'H' for hearts

        num    string      Rank within that suit, e.g. 'K' for king

        '''
        self._logger = logging.getLogger('{}.Card'.format(__name__))
        self.Suit = suit
        self.Rank = num

    def Score(self, ace_high=False, score_dict=None):
        '''
        Score the card with option to set Ace to be 11 as opposed to 1

        Optional Arguments
        ------------------

        ace_high     bool    Set Ace to be 11 instead of 1
                             Default is False

        score_dict   dict    Overwrite default scoring with a dictionary
                             Default is None

        '''
        try:
            return int(self.Rank)
        except ValueError:
            other = {'A' : 11 if ace_high else 1,
                     'J' : 10, 'Q' : 10, 'K' : 10}
            return score_dict[self.Rank] if score_dict else other[self.Rank]

    def __str__(self):
        return self.Rank+self.Suit

class Deck(object):
    def __init__(self, empty=False):
        '''
        Object representing a standard deck of cards

        Optional Arguments
        ------------------

        empty     bool      Create an empty deck (e.g. for discard pile)
                            Default is False

        '''
        self._logger = logging.getLogger('{}.Deck'.format(__name__))
        self._cards = self._create_deck() if not empty else []
        self.shuffle()
        self._drawn = []

    def get_ncards_drawn(self):
        '''Returns the number of cards which have been drawn from the deck'''
        return len(self._drawn)

    def get_ncards_deck(self):
        '''Returns the number of cards left in the deck'''
        return len(self._cards)-len(self._drawn)

    def shuffle(self):
        '''Shuffles the deck'''
        shuffle(self._cards)

    def draw(self, from_top=True, replace=False):
        '''
        Draw a card from the deck

        Optional Arguments
        ------------------

        from_top     bool      Draw cards from top of deck, else
                               randomly take a card.
                               Default is True

        replace      bool      Replace the card after drawing.
                               Default is False

        '''
        if from_top:
            i = 0
            while self._cards[i].__str__() in self._drawn:
                i+=1
        else:
            i = randint(0,len(self._cards)-1)
            while self._cards[i].__str__() in self._drawn:
                i = random.randint(len(self._cards))
        if not replace:
            self._drawn.append(self._cards[i].__str__())
        return self._cards[i]

    def _create_deck(self):
        _cards = []
        for rank in [str(i) for i in range(2,11)]+['A','J','K','Q']:
            for suit in ['C', 'S', 'D', 'H']:
                _cards.append(Card(suit, rank))
        return _cards

    def __str__(self):
        _in_deck = []
        for i in self._cards:
            if i.__str__() not in self._drawn:
                _in_deck.append(i.__str__())
        return _in_deck.__str__()

    def draw_hand(self, ncards):
        '''
        Form a hand of 'ncards' from the deck

        Arguments
        ---------

        ncards    int    Number of cards to draw

        '''
        return Hand(self, ncards)

    def deal(self, ncards, nplayers):
        '''
        Deal cards to a number of players

        Arguments
        ---------

        ncards    int     Number of cards per hand

        nplayers  int     Number of hands to deal

        '''
        return [self.draw_hand(ncards) for i in range(nplayers)]

    def __add__(self, other):
        _tmp = Deck()
        if isinstance(other, Deck):
            _tmp._cards = self._cards + other._cards
            
            # Cheaty way of doing this, if card has been removed from deck A
            # but not deck B, treat deck as still having card. Behaviour is
            # same for multiple card occurence as single

            _drawn = []
            for i in self._drawn:
                if i in other._drawn:
                    _drawn.append(i)
            tmp._drawn = _drawn

            return _tmp
        elif isinstance(other, Card):
            _tmp._cards = [i for i in self._cards]
            if other.__str__() not in [i.__str__() for i in _tmp._cards]:
                _tmp._cards.append(other)
            _tmp._drawn = [i for i in self._drawn]
            if other.__str__() in _tmp._drawn:
                _tmp._drawn.remove(other.__str__())
            return _tmp


    def __repr__(self):
        return '<{}.Deck, ncards_total={}, ncards_current={}, addr={}>'.format(__name__,
                                                                     len(self._cards),
                                                                     len(self._cards)-len(self._drawn),
                                                                     hex(id(self)))

class Hand(object):
    def __init__(self, deck, ncards, _no_draw=False):
        '''
        Object representing a hand of cards

        Arguments
        ---------

        deck    Deck    Parent deck from which to draw from.

        ncards  int     Number of cards within the hand

        '''
        self._logger = logging.getLogger('{}.Hand'.format(__name__))
        self._deck = deck
        self._cards = self._draw_hand(ncards) if not _no_draw else []

    def _draw_hand(self, ncards):
        return [self._deck.draw() for i in range(ncards)]
    
    def __str__(self):
        return [i.__str__() for i in self._cards].__str__()

    def __repr__(self):
        return '<{}.Hand, ncards={}, addr={}, hand_addr={}>'.format(__name__,
                                                      len(self._cards),
                                                      hex(id(self)),
                                                      hex(id(self._deck)))

    def get_deck(self):
        '''Returns parent deck'''
        return self._deck()

    def __add__(self, other):
        if self._deck != other._deck:
            self._logger.error('Hands must be drawn from same deck! Consider adding decks together first')
            raise ArithmeticError

        _tmp = Hand(self._deck, ncards=len(self._cards)+len(other._cards), _no_draw=True)
        _tmp._cards = self._cards + other._cards

        return _tmp

    def __sub__(self, card):
        def _index_based(is_tuple, card):
            if is_tuple:
                arg = card[0]
                card = card[1]
            _tmp = Hand(self._deck, ncards=len(self._cards)-card, _no_draw=True)
            _tmp._cards = [i for i in self._cards]

            for i in range(card):
                del _tmp._cards[arg]
            return _tmp
        if isinstance(card, str):
            _tmp = Hand(self._deck, ncards=len(self._cards)-1, _no_draw=True)
            _tmp._cards = [i for i in self._cards]
            for i, c in enumerate(tmp._cards):
                if c.__str__() == card:
                    del _tmp._cards[i]

            return _tmp
        elif isinstance(card, int):
            return _index_based(False, card)

        elif isinstance(card, tuple):
            return _index_based(True, card)

        else:
            self._logger.error('Invalid types of {} and {}'.format(type(self), type(other)))
            raise ArithmeticError

    def discard(self, n=1, to_deck=None, random=False):
        '''
        Discard cards from the hand

        Optional Arguments
        ------------------

        n          int     Number of cards to discard. Default is 1.

        to_deck    Deck    Deck to discard to. Default is parent.

        random     bool    Discard randomly as opposed to from the top.
                           Default is False.

        '''
        _tmp = Hand(self._deck, ncards=len(self._cards), _no_draw=True)
        _tmp._cards = [i for i in self._cards]
        for i in range(n):
            index = 0 if not random else randint(0, len(_tmp._cards)-1)
            if to_deck:
                to_deck.__dict__.update((to_deck + _tmp._cards[index]).__dict__)
            else:
                self._deck.__dict__.update((self._deck + _tmp._cards[index]).__dict__)
            _tmp -= (index, 1)
        self.__dict__.update(_tmp.__dict__)

