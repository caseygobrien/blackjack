from random import choice
remaining_cards = 0
suits = []


def new_deck(decks):
    global remaining_cards
    global suits
    suits = ["Spades", "Hearts", "Diamonds", "Clubs"]
    remaining_cards = 52 * decks
    possible_cards = [number for number in range(2, 15)]
    deck = {}
    for suit in suits:
        deck[suit] = []
    for i in range(decks):
        for suit in suits:
            for card in possible_cards:
                deck[suit].append(card)
    return deck


def deal_card(deck):
    global remaining_cards
    global suits
    global number_of_decks
    global working_deck
    card_suit = choice(suits)
    if not deck[card_suit]:
        suits.remove(card_suit)
        card_suit = choice(suits)
    card_value = choice(deck[card_suit])
    card_names = {11: "Jack", 12: "Queen", 13: "King", 14: "Ace"}
    changed_name = ''
    deck[card_suit].remove(card_value)
    for number in card_names:
        if card_value == number:
            changed_name = card_names[number]
    if 10 < card_value < 14:
        card_value = 10
    elif card_value == 14:
        card_value = 11
    if changed_name:
        card = "{0} of {1}".format(changed_name, card_suit)
    else:
        card = "{0} of {1}".format(card_value, card_suit)
    remaining_cards -= 1
    if remaining_cards < (number_of_decks*52)/3:
        working_deck = new_deck(number_of_decks)
        print("SHUFFLING")
    return card, card_value


def play_out_hand(current_deck, current_value, current_hand):
    global remaining_cards
    playing = True
    while playing:
        play = input("Would you like to [H]it or [S]tand?\n".lower())
        possible_answers = ["h", "s"]
        if play not in possible_answers:
            continue
        elif play == "h":
            next_card = deal_card(current_deck)
            current_hand.append(next_card[1])
            current_value = sum(current_hand)
            if current_value > 21:
                if 11 in current_hand:
                    current_hand, current_value = check_for_ace(current_hand, current_value)
                    print("You got the {0}\nfor a total of {1}".format(next_card[0], current_value))
                    continue
                else:
                    print("You got the {0}\nfor a total of {1}".format(next_card[0], current_value))
                    return current_hand, current_value
            else:
                print("You got the {0}\nfor a total of {1}".format(next_card[0], current_value))
                continue
        elif play == "s":
            return current_hand, current_value


def check_for_ace(hand, value):
    if 11 in hand:
        hand.remove(11)
        hand.append(1)
        new_value = sum(hand)
        return hand, new_value
    return hand, value


number_of_decks = int(input("Number of decks:\n"))
stake = int(input("Starting money:\n"))
initial_stake = stake
working_deck = new_deck(number_of_decks)
# deal the cards
dealing = True
while dealing:
    dealer_hand = []
    player_hand = []
    print("You have ${} remaining".format(stake))
    bet = int(input("Your bet:\n"))
    while bet > stake:
        print("You don't have enough money")
        bet = int(input("Your bet\n"))
    stake -= bet
    dealer_card_1 = deal_card(working_deck)
    dealer_hand.append(dealer_card_1[1])
    player_card_1 = deal_card(working_deck)
    player_hand.append(player_card_1[1])
    dealer_card_2 = deal_card(working_deck)
    dealer_hand.append(dealer_card_2[1])
    player_card_2 = deal_card(working_deck)
    if player_card_2[1] == 11 and player_card_2[1] == 11:
        player_hand.append(1)
    else:
        player_hand.append(player_card_2[1])
    dealer_value = sum(dealer_hand)
    player_value = sum(player_hand)
    print("You have the {0} and the {1}\nfor a total of {2}".format(player_card_1[0], player_card_2[0], player_value))
    print("The dealer is showing the {0}".format(dealer_card_2[0]))
    player_hand, hand_total = play_out_hand(working_deck, player_value, player_hand)
    if hand_total > 21:
        print("BUSTED")
    else:
        print("The dealer's hole card is the {0}\nfor a total of {1}".format(dealer_card_1[0], dealer_value))
        while dealer_value < 17 or dealer_value == 17 and 11 in dealer_hand:
            next_dealer_card = deal_card(working_deck)
            dealer_hand.append(next_dealer_card[1])
            print("The dealer gets the {}".format(next_dealer_card[0]))
            dealer_value += next_dealer_card[1]
            if dealer_value > 21:
                if 11 in dealer_hand:
                    dealer_hand.remove(11)
                    dealer_hand.append(1)
                    dealer_value = sum(dealer_hand)
                    continue
        else:
            print("The dealer has {}".format(dealer_value))
            if dealer_value > 21:
                print("DEALER BUSTS")
                print("You won ${}".format(bet))
                stake += bet*2
            elif hand_total > dealer_value:
                print("YOU WIN")
                print("You won ${}".format(bet))
                stake += bet*2
            elif hand_total < dealer_value:
                print("DEALER WINS")
                print("You lost ${}".format(bet))
            else:
                print('PUSH')
                stake += bet
    if stake == 0:
        print("You're out of money\nBetter luck next time!")
        dealing = False
    else:
        again = input("Play again? (Y/N)".lower())
        if again == "n":
            winnings = stake - initial_stake
            if winnings > 0:
                print("You won ${0} and walked away with ${1}".format(winnings, stake))
                print("****CONGRATULATIONS****")
            if winnings == 0:
                print("You broke even and walked away with ${0}".format(stake))
            else:
                print("You lost ${0} and walked away with ${1}".format(-winnings, stake))
            dealing = False
