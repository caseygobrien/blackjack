import random
remaining_cards = 0
number_of_decks = 0
stake = 0
bet = 0


# build a playable deck of cards from a specified number of decks
def new_deck(decks):
    global remaining_cards
    deck_of_cards = ["2h", "3h", "4h", "5h", "6h", "7h", "8h", "9h", "10h", "11h", "12h", "13h", "14h",
                     "2d", "3d", "4d", "5d", "6d", "7d", "8d", "9d", "10d", "11d", "12d", "13d", "14d",
                     "2c", "3c", "4c", "5c", "6c", "7c", "8c", "9c", "10c", "11c", "12c", "13c", "14c",
                     "2s", "3s", "4s", "5s", "6s", "7s", "8s", "9s", "10s", "11s", "12s", "13s", "14s"]
    remaining_cards = 52 * decks
    deck = deck_of_cards * decks
    random.shuffle(deck)
    # burn one card
    deck.pop(0)
    remaining_cards -= 1
    return deck


# pull the top card and assign its name and value
def deal_card(deck):
    global remaining_cards
    card = deck.pop(0)
    card_value = int(card[:-1])
    suits = {"s": "Spades", "c": "Clubs", "d": "Diamonds", "h": "Hearts"}
    card_suit = suits[card[-1]]
    card_names = {11: "Jack", 12: "Queen", 13: "King", 14: "Ace"}
    changed_name = ''
    if card_value in card_names:
        changed_name = card_names[card_value]
    # change face cards to 10
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
    return card, card_value


def get_player_choice(hand, bet, card=False):
    global stake
    global number_of_hands
    possible_choices = ["h", "s", "d", "sp"]
    if not card and stake >= bet and number_of_hands < 4:
        if hand[0] == hand[1] or hand[0] == 11 and hand[1] == 1:
            choice = input("""Would you like to
[H]it
[S]tand
[D]ouble Down
[Sp]lit\n""").lower()
            while choice not in possible_choices:
                choice = input("Please enter a valid choice\n")
        else:
            possible_choices.remove("sp")
            choice = input("""Would you like to
[H]it
[S]tand
[D]ouble Down\n""").lower()
            while choice not in possible_choices:
                choice = input("Please enter a valid choice\n")
    else:
        possible_choices.remove("sp")
        possible_choices.remove("d")
        choice = input("""Would you like to
[H]it
[S]tand\n""").lower()
        while choice not in possible_choices:
            choice = input("Please enter a valid choice\n")
    return choice


# player plays out their hand
def play_out_hand(hand, bet, choice):
    global stake
    global working_deck
    hand_value = sum(hand)
    if choice == "d":
        stake -= bet
        bet = bet * 2
        next_card = deal_card(working_deck)
        hand.append(next_card[1])
        hand_value = sum(hand)
        if hand_value > 21 and 11 in hand:
            hand, hand_value = switch_ace_to_1(hand)
        print("You got the {0}\nfor a total of {1}".format(next_card[0], hand_value))
        if hand_value > 21:
            print("BUSTED")
            print("\n*************\n")
            print("You lost ${0}".format(bet))
            return None
        else:
            choice = "s"
    while choice == "h":
        next_card = deal_card(working_deck)
        hand.append(next_card[1])
        hand_value = sum(hand)
        if hand_value > 21 and 11 in hand:
            hand, hand_value = switch_ace_to_1(hand)
        print("You got the {0}\nfor a total of {1}".format(next_card[0], hand_value))
        if hand_value > 21:
            print("BUSTED")
            print("\n*************\n")
            print("You lost ${0}".format(bet))
            return None
        else:
            card = True
            choice = get_player_choice(hand, bet, card)
            continue
    final_hands.append((hand_value, bet))


def play_dealer_hand(dealer_card, dealer_hand):
    global working_deck
    dealer_value = sum(dealer_hand)
    print("\n*************\n")
    print("The dealer's hole card is the {0}\nfor a total of {1}".format(dealer_card[0], dealer_value))
    # dealer hits with less than 17 or a soft 17
    while dealer_value < 17 or dealer_value == 17 and 11 in dealer_hand:
        next_dealer_card = deal_card(working_deck)
        dealer_hand.append(next_dealer_card[1])
        dealer_value += next_dealer_card[1]
        if dealer_value > 21 and 11 in dealer_hand:
            dealer_hand, dealer_value = switch_ace_to_1(dealer_hand)
        print("The dealer gets the {}".format(next_dealer_card[0]))
    if dealer_value > 21:
        return None
    print("\n*************\n")
    return dealer_value


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
        if wager > stake:
            print("You don't have that much money")
            continue
        stake -= wager
        return wager


def end_game():
    global stake
    global initial_stake
    again = input("Play again? (Y/N)\n".lower())
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
        return True
    else:
        return False


def split(hand, bet):
    global working_deck
    global stake
    global number_of_hands
    print("\n--SPLITTING--\n")
    hand_1 = [hand[0]]
    hand_1_bet = bet
    hand_2 = [hand[1]]
    hand_2_bet = bet
    hand_1_card_2 = deal_card(working_deck)
    hand_1.append(hand_1_card_2[1])
    hand_1_value = sum(hand_1)
    print("\n*************\n")
    print("\nPLAYING FIRST HAND\n")
    print("You got the {0}\nfor a total of {1}".format(hand_1_card_2[0],
                                                       hand_1_value))
    if hand[0] == 11:
        hand_2[0] = 11
        final_hands.append((hand_1_value, hand_1_bet))
        hand_2_card_2 = deal_card(working_deck)
        hand_2.append(hand_2_card_2[1])
        hand_2_value = sum(hand_2)
        print("\n*************\n")
        print("\nPLAYING NEXT HAND\n")
        print("You got the {0}\nfor a total of {1}".format(hand_2_card_2[0], hand_2_value))
        final_hands.append((hand_2_value, hand_2_bet))
        return
    choice = get_player_choice(hand_1, hand_1_bet)
    if choice == "sp":
        stake -= bet
        number_of_hands += 1
        split(hand_1, hand_1_bet)
    else:
        play_out_hand(hand_1, hand_1_bet, choice)
    hand_2_card_2 = deal_card(working_deck)
    hand_2.append(hand_2_card_2[1])
    hand_2_value = sum(hand_2)
    print("\n*************\n")
    print("\nPLAYING NEXT HAND\n")
    print("You got the {0}\nfor a total of {1}".format(hand_2_card_2[0], hand_2_value))
    choice_2 = get_player_choice(hand_2, hand_2_bet)
    if choice_2 == "sp":
        stake -= bet
        number_of_hands += 1
        split(hand_2, hand_2_bet)
    else:
        play_out_hand(hand_2, hand_2_bet, choice_2)
    return


def check_money():
    global stake
    if stake == 0:
        print("You are out of money. Better luck next time!")
        return False
    return True


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

# deal!
dealing = True
while dealing:
    final_hands = []
    insurance = False
    print("You have ${} remaining\n".format(stake))
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
    number_of_hands = 1
    print("*************\n")
    print("You have the {0} and the {1}\nfor a total of {2}".format(player_card_1[0],
                                                                    player_card_2[0], player_value))
    print("The dealer is showing the {0}".format(dealer_card_2[0]))
    print("\n*************\n")
    if dealer_card_2[1] == 11:
        if stake > insurance_bet:
            ask_insurance = input("Insurance? Y/N:\n".lower())
            if ask_insurance == "y":
                insurance = True
                stake -= insurance_bet
    # check for blackjack!
    if player_value == 21:
        print("You have blackjack!")
        if dealer_value < 21:
            print("You won ${0}".format(int(bet * 1.5)))
            stake += int(bet + (bet * 1.5))
            print("\n*************\n")
            if end_game():
                break
            else:
                continue
        else:
            print("Dealer has blackjack, you have pushed")
            if insurance:
                print("Insurance pays you ${0}".format(int(insurance_bet * 2)))
                stake += int((insurance_bet * 3) + bet)
            else:
                stake += bet
            print("\n*************\n")
        if end_game():
            break
        else:
            continue
    # check for dealer blackjack
    if dealer_value == 21:
        print("Dealer has blackjack!")
        if insurance:
            print("Insurance pays you ${0}".format(int(insurance_bet * 2)))
            stake += int(insurance_bet * 3)
        else:
            print("You lost ${0}".format(bet))
        if not check_money():
            break
        print("\n*************\n")
        if end_game():
            break
        else:
            continue
    elif dealer_card_2[1] == 11:
        print("Dealer does not have blackjack\n")
    # time to play out hands
    player_choice = get_player_choice(player_hand, bet)
    if player_choice == "sp":
        stake -= bet
        number_of_hands += 1
        split(player_hand, bet)
    else:
        play_out_hand(player_hand, bet, player_choice)
    if final_hands:
        dealer_value = play_dealer_hand(dealer_card_1, dealer_hand)
        if not dealer_value:
            print("Dealer Busts!")
            print("\n*************\n")
        for i in range(len(final_hands)):
            final_value = final_hands[i][0]
            final_bet = final_hands[i][1]
            if len(final_hands) > 1:
                print("Hand {0} of {1}".format((i + 1), len(final_hands)))
            if not dealer_value:
                print("You win ${0}".format(final_bet))
                stake += final_bet * 2
                continue
            else:
                print("You have {0}".format(final_value))
                print("The dealer has {0}".format(dealer_value))
            if final_value > dealer_value:
                print("You win ${0}".format(final_bet))
                stake += final_bet * 2
            elif final_value < dealer_value:
                print("You lose ${0}".format(final_bet))
            else:
                print("You have pushed")
                stake += final_bet
            print("\n*************\n")

    if not check_money():
        dealing = False
    if end_game():
        dealing = False
    # build a new deck if the current deck is 2/3rds gone
    if remaining_cards < (number_of_decks*52)/3:
        working_deck = new_deck(number_of_decks)
        print("*****SHUFFLING*****")
