import random
remaining_cards = 0
number_of_decks = 0
stake = 0
bet = 0
suits = {"s": "spades", "c": "clubs", "d": "diamonds", "h": "hearts"}
deck_of_cards = ["2h", "3h", "4h", "h5", "6h", "7h", "8h", "9h", "10h", "11h", "12h", "13h", "14h",
                 "2d", "3d", "4d", "5d", "6d", "7d", "8d", "9d", "10d", "11d", "12d", "13d", "14d",
                 "2c", "3c", "4c", "5c", "6c", "7c", "8c", "9c", "10c", "11c", "12c", "13c", "14c",
                 "2s", "3s", "4s", "5s", "6s", "7s", "8s", "9s", "10s", "11s", "12s", "13s", "14s"]


# build a playable deck of cards from a specified number of decks
def new_deck(decks):
    global remaining_cards
    global deck_of_cards
    remaining_cards = 52 * decks
    deck = deck_of_cards * decks
    random.shuffle(deck)
    # burn one card
    deal_card(deck)
    return deck


# pull one random card out of the deck
def deal_card(deck):
    global remaining_cards
    global suits
    global number_of_decks
    global working_deck
    card = deck.pop(0)
    card_value = int(card[:-1])
    card_suit = card[-1]
    for suit in suits:
        if card_suit == suit:
            card_suit = suits[suit]
    card_names = {11: "Jack", 12: "Queen", 13: "King", 14: "Ace"}
    changed_name = ''
    for number in card_names:
        if card_value == number:
            changed_name = card_names[number]
    # change the values of all face cards to 10
    if 10 < card_value < 14:
        card_value = 10
    # and change aces to 11
    elif card_value == 14:
        card_value = 11
    if changed_name:
        card = "{0} of {1}".format(changed_name, card_suit)
    else:
        card = "{0} of {1}".format(card_value, card_suit)
    remaining_cards -= 1
    # build a new deck if the current deck is 2/3rds gone
    if remaining_cards < (number_of_decks*52)/3:
        working_deck = new_deck(number_of_decks)
        print("*****SHUFFLING*****")
    return card, card_value


# player plays out their hand
def play_out_hand(current_deck, current_value, current_hand):
    global remaining_cards
    global stake
    global bet
    playing = True
    cards_dealt = 0
    while playing:
        if cards_dealt == 0:
            play = input("""Would you like to
[H]it
[S]tand
[D]ouble Down\n""").lower()
        else:
            play = input("""Would you like to
[H]it
[S]tand\n""").lower()
        # Double Down doubles the bet if possible
        if play == "d":
            if stake < bet:
                print("You don't have enough money to double down")
                continue
            else:
                stake -= bet
                bet = 2 * bet
        # hit or double gets a new card
        if play == "h" or play == "d":
            next_card = deal_card(current_deck)
            cards_dealt += 1
            current_hand.append(next_card[1])
            current_value = sum(current_hand)
            # if player busts, check for an ace valued at 11 and change it to a 1
            if current_value > 21:
                if 11 in current_hand:
                    current_hand, current_value = switch_ace_to_1(current_hand)
                    print("You got the {0}\nfor a total of {1}".format(next_card[0], current_value))
                    continue
                else:
                    # player has busted
                    print("You got the {0}\nfor a total of {1}".format(next_card[0], current_value))
                    print("YOU HAVE BUSTED")
                    return current_hand, current_value
            else:
                print("You got the {0}\nfor a total of {1}".format(next_card[0], current_value))
                # Player ony gets one card for doubling down
                if play == "d":
                    return current_hand, current_value
                else:
                    continue
        # stand returns hand and value
        elif play == "s":
            return current_hand, current_value
        else:
            continue


# remove the 11 and add a 1
def switch_ace_to_1(hand):
    hand.remove(11)
    hand.append(1)
    new_value = sum(hand)
    return hand, new_value


def place_your_bet():
    global stake
    betting = True
    while betting:
        try:
            wager = int(input("Your bet:\n"))
        except ValueError:
            print("Please enter a number")
            continue
        stake -= wager
        return wager


def end_game():
    global stake
    global initial_stake
    again = input("Play again? (Y/N)".lower())
    # if no, end the game and inform player of their win or loss
    if again == "n":
        winnings = stake - initial_stake
        if winnings > 0:
            print("You won ${0} and walked away with ${1}".format(winnings, stake))
            print("****CONGRATULATIONS****")
        elif winnings == 0:
            print("You broke even and walked away with ${0}".format(stake))
        else:
            print("You lost ${0} and walked away with ${1}".format(-winnings, stake))
    return again


# request a number of decks
ask_decks = True
while ask_decks:
    try:
        number_of_decks = int(input("Number of decks:\n"))
    except ValueError:
        print("Please enter a number")
        continue
    ask_decks = False
# get starting money
ask_stake = True
while ask_stake:
    try:
        stake = int(input("Starting money:\n"))
    except ValueError:
        print("Please enter a number")
        continue
    else:
        ask_stake = False
initial_stake = stake
# build a deck
working_deck = new_deck(number_of_decks)

dealing = True
while dealing:
    insurance = ""
    print("You have ${} remaining".format(stake))
    bet = place_your_bet()
    insurance_bet = 0.5 * bet
    # deal the cards
    dealer_hand = []
    player_hand = []
    dealer_card_1 = deal_card(working_deck)
    dealer_hand.append(dealer_card_1[1])
    player_card_1 = deal_card(working_deck)
    player_hand.append(player_card_1[1])
    dealer_card_2 = deal_card(working_deck)
    player_card_2 = deal_card(working_deck)
    # if anyone has two aces, change one of them from 11 to 1
    if dealer_card_1[1] == 11 and dealer_card_2[1] == 11:
        dealer_hand.append(1)
    else:
        dealer_hand.append(dealer_card_2[1])
    if player_card_1[1] == 11 and player_card_2[1] == 11:
        player_hand.append(1)
    else:
        player_hand.append(player_card_2[1])
    dealer_value = sum(dealer_hand)
    player_value = sum(player_hand)
    print("You have the {0} and the {1}\nfor a total of {2}".format(player_card_1[0], player_card_2[0], player_value))
    print("The dealer is showing the {0}".format(dealer_card_2[0]))
    if dealer_card_2[1] == 11:
        insurance = input("Insurance? Y/N:\n".lower())
        if insurance == "y":
            if stake < insurance_bet:
                print("You don't have enough money to purchase insurance")
                insurance = "n"
            else:
                stake -= insurance_bet
    # check for blackjack!
    if player_value == 21:
        print("You have blackjack!")
        if dealer_value < 21:
            print("You won {0}".format(int(bet * 1.5)))
            stake += int(bet + (bet * 1.5))
            if end_game() == "n":
                break
            else:
                continue
        else:
            print("Dealer has blackjack, you have pushed")
            if insurance == "y":
                print("Insurance pays you ${0}".format(insurance_bet))
                stake += bet
            stake += bet
            if end_game() == "n":
                break
            else:
                continue
    # check for dealer blackjack
    if dealer_value == 21:
        print("Dealer has blackjack!")
        if insurance == "y":
            print("Insurance pays you {0}".format(insurance_bet))
            stake += bet
        else:
            print("You lost {0}".format(bet))
        if end_game() == 'n':
            break
        else:
            continue
    # player plays out his or her hand
    player_hand, hand_total = play_out_hand(working_deck, player_value, player_hand)
    # if player hand is less than 21, dealer plays out their hand
    if hand_total <= 21:
        print("The dealer's hole card is the {0}\nfor a total of {1}".format(dealer_card_1[0], dealer_value))
        # delaler hits with less than 17 or a soft 17
        while dealer_value < 17 or dealer_value == 17 and 11 in dealer_hand:
            next_dealer_card = deal_card(working_deck)
            dealer_hand.append(next_dealer_card[1])
            print("The dealer gets the {}".format(next_dealer_card[0]))
            dealer_value += next_dealer_card[1]
            # if dealer busts, check for an ace
            if dealer_value > 21:
                if 11 in dealer_hand:
                    dealer_hand, dealer_value = switch_ace_to_1(dealer_hand)
                    continue
        # compare dealer total and player total and pay out bets
        else:
            print("The dealer has {0}".format(dealer_value))
            if dealer_value > 21 or hand_total > dealer_value:
                print("PLAYER WINS")
                print("You won ${0}".format(bet))
                stake += bet * 2
            elif hand_total < dealer_value:
                print("DEALER WINS")
                print("You lost ${0}".format(bet))
            else:
                print('PUSH')
                stake += bet
    # end the game if player loses all their money
    if stake == 0:
        print("You're out of money\nBetter luck next time!")
        dealing = False
    if end_game() == "n":
        dealing = False
    else:
        continue
