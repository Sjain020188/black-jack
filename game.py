import random
suits = ('Diamonds', 'Spades', 'Clubs', 'Hearts')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven',
         'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5, 'Six': 6, 'Seven': 7,
          'Eight': 8, 'Nine': 9, 'Ten': 10, 'Jack': 10, 'Queen': 10, 'King': 10, 'Ace': 11}
playing = True


class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return self.rank + ' of ' + self.suit


class Deck:
    def __init__(self):
        self.deck = []
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit, rank))

    def __str__(self):
        deck_comp = ''
        for card in self.deck:
            deck_comp += '\n'+card.__str__()
        return deck_comp

    def shuffle(self):
        random.shuffle(self.deck)

    def deal(self):
        return self.deck.pop()


test_deck = Deck()
test_deck.shuffle()
print(test_deck)


class Hand:
    def __init__(self):
        self.cards = []
        self.value = 0
        self.aces = 0

    def add_card(self, card):
        self.cards.append(card)
        self.value += values[card.rank]

        if card.rank == 'Ace':
            self.aces += 1

    def adjust_aces(self):
        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1


class Chips:
    def __init__(self):
        self.total = 100
        self.bet = 0

    def win_bet(self):
        self.total += self.bet

    def loose_bet(self):
        self.total -= self.bet


def take_bet(chips):
    while True:

        try:
            chips.bet = int(input("How many chips do you want to bet?"))
        except:
            print("Sorry please provide integer")
        else:
            if chips.bet > chips.total:
                print("Sorry you don't have enough chips. You have {}".format(
                    chips.total))
            else:
                break


def hit(deck, hand):
    hand.add_card(deck.deal())
    hand.adjust_aces()


def hit_of_stand(deck, hand):
    global playing

    while True:
        x = input("Hit or Stand? Enter h or s")
        if x[0].lower() == 'h':
            hit(deck, hand)

        elif x[0].lower() == 's':
            print("player stands dealer turn")
            playing = False

        else:
            print("Sorry please enter only h or s")
            continue

        break


def player_busts(player, dealer, chips):
    print("PLAYER BUST")
    chips.loose_bet()


def player_wins(player, dealer, chips):
    print("PLAYER WINS")
    chips.win_bet()


def dealer_busts(player, dealer, chips):
    print("PLAYER WINS. DEALER BUSTED")
    chips.win_bet()


def dealer_wins(player, dealer):
    print("DEALER WIN")
    chips.loose_bet()


def push(player, dealer, chips):
    print("tie")


def show_some(player, dealer):
    print("DEALER HAND, one card hidden")
    print(dealer.cards[1])
    print("\nPLAYER HAND")
    for card in player.cards:
        print(card)


def show_all(player, dealer):
    print("\nDEALER HAND")
    for card in dealer.cards:
        print(card)
    print("\nPLAYER HAND")
    for card in player.cards:
        print(card)


while True:
    print("WELCOME TO BLACK JACK")
    deck = Deck()
    deck.shuffle()

    player_hand = Hand()
    player_hand.add_card(deck.deal())
    player_hand.add_card(deck.deal())

    dealer_hand = Hand()
    dealer_hand.add_card(deck.deal())
    dealer_hand.add_card(deck.deal())

    player_chips = Chips()
    take_bet(player_chips)

    show_some(player_hand, dealer_hand)

    while playing:
        hit_of_stand(deck, player_hand)
        show_some(player_hand, dealer_hand)

        if player_hand.value > 21:
            player_busts(player_hand, dealer_hand, player_chips)
            break

        if player_hand.value < 21:
            while(dealer_hand.value < player_hand.value):
                hit(deck, dealer_hand)

            show_all(player_hand, dealer_hand)

            if dealer_hand.value > 1:
                dealer_busts(player_hand, dealer_hand, player_chips)
            elif dealer_hand.value > player_hand.value:
                dealer_wins(player_hand, dealer_hand, player_chips)
            elif dealer_hand.value < player_hand.value:
                player_wins(player_hand, dealer_hand, player_chips)
            else:
                push(player_hand, dealer_hand)

            print("Player chips {}".format(player_chips.total))

    break
