import random
remaining_cards = 0
number_of_decks = 0
stake = 0
bet = 0
final_hands = {}
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


def get_player_choices(hand, cards=0):
    if cards == 0 and hand[0] == hand[1] or cards == 0 and hand[0] == 11 and hand[1] == 1:
        choice = input("""Would you like to
[H]it
[S]tand
[D]ouble Down
[Sp]lit\n""").lower()
    elif cards == 0:
        choice = input("""Would you like to
[H]it
[S]tand
[D]ouble Down\n""").lower()
    else:
        choice = input("""Would you like to
[H}it
[S]tand\n""").lower()
    return choice


# player plays out their hand
def play_out_hand():
    global final_hands
    global remaining_cards
    global stake
    global working_deck
    current_hand = []
    cards_dealt = 0
    for hand in final_hands:
        if len(final_hands) > 1:
            print("\n************\n")
            print("Playing hand {0}\n".format(hand))
        current_hand = final_hands[hand][0]
        current_bet = final_hands[hand][1]
        current_hand_value = sum(current_hand)
        play = get_player_choices(current_hand, cards_dealt)
        #splits!
        if play == "sp":
            split(current_hand, current_bet)
        # hit or double gets a new card
        if play == "d" and cards_dealt == 0:
            if stake < current_bet:
                print("You don't have enough money to double down\n")
                play = get_player_choices(current_hand)
            else:
                stake -= current_bet
                current_bet = current_bet * 2
                next_card = deal_card(working_deck)
                cards_dealt += 1
                current_hand.append(next_card[1])
                current_hand_value += next_card[1]
            # if player busts, check for an ace valued at 11 and change it to a 1
                if current_hand_value > 21 and 11 in current_hand:
                    current_hand, current_hand_value = switch_ace_to_1(current_hand)
                print("You got the {0}\nfor a total of {1}".format(next_card[0], current_hand_value))
                play = 's'
        while play == "h":
            next_card = deal_card(working_deck)
            cards_dealt += 1
            current_hand.append(next_card[1])
            current_hand_value += next_card[1]
            # if player busts, check for an ace valued at 11 and change it to a 1
            if current_hand_value > 21 and 11 in current_hand:
                current_hand, current_hand_value = switch_ace_to_1(current_hand)
            print("You got the {0}\nfor a total of {1}".format(next_card[0], current_hand_value))
            if current_hand_value > 21:
                play = 's'
                continue
            play = get_player_choices(current_hand, cards_dealt)
        if play == "s":
            final_hands[hand] = current_hand, current_bet


def split(hand, bet):
    global final_hands
    global remaining_cards
    global stake
    global working_deck
    stake -= bet
    print("Splitting hand:")
    hand_1 = [hand[0]]
    hand_2 = [hand[1]]
    hand_1_new_card = deal_card(working_deck)
    hand_1.append(hand_1_new_card[1])
    hand_1_total = sum(hand_1)
    print("Your first hand got the {0}\nfor a total of {1}".format(hand_1_new_card[0], hand_1_total))
    print("**********\n")
    hand_2_new_card = deal_card(working_deck)
    hand_2.append(hand_2_new_card[1])
    hand_2_total = sum(hand_2)
    print("And your second hand got the {0}\n for a total of {1}".format(hand_2_new_card[0], hand_2_total))
    final_hands[1] = [hand_1], bet
    final_hands[2] = [hand_2], bet


def play_dealer_hand(dealer_card, dealer_hand):
    global working_deck
    dealer_value = sum(dealer_hand)
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
    print("The dealer has {0}".format(dealer_value))
    print("\n*************\n")
    return dealer_value


# remove an 11 and add a 1
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
    print("You have ${0}".format(stake))
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


def check_money(stake):
    money = True
    if stake == 0:
        money = False
        print("You are out of money. Better luck next time!")
    return money


# request a number of decks
ask_decks = True
while ask_decks:
    try:
        number_of_decks = int(input("Number of decks:\n"))
    except ValueError:
        print("Please enter a number")
        continue
    ask_decks = False

# # get starting money
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
    insurance = False
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
    print("\n*************\n")
    print("You have the {0} and the {1}\nfor a total of {2}".format(player_card_1[0], player_card_2[0], player_value))
    print("The dealer is showing the {0}".format(dealer_card_2[0]))
    print("\n*************\n")
    if dealer_card_2[1] == 11:
        ask_insurance = input("Insurance? Y/N:\n".lower())
        if ask_insurance == "y":
            if stake < insurance_bet:
                print("You don't have enough money to purchase insurance")
                ask_insurance = "n"
            else:
                insurance = True
                stake -= insurance_bet
    # check for blackjack!
    if player_value == 21:
        print("You have blackjack!")
        if dealer_value < 21:
            print("You won ${0}".format(int(bet * 1.5)))
            stake += int(bet + (bet * 1.5))
            print("\n*************\n")
            if end_game() == "n":
                break
            else:
                continue
        else:
            print("Dealer has blackjack, you have pushed")
            if insurance:
                print("Insurance pays you ${0}".format(bet * 1.5))
                stake += bet * 2.5
            else:
                stake += bet
            print("\n*************\n")
        if end_game() == "n":
            break
        else:
            continue
    # check for dealer blackjack
    if dealer_value == 21:
        print("Dealer has blackjack!")
        if insurance:
            print("Insurance pays you ${0}".format(bet * 1.5))
            stake += bet + insurance_bet
        else:
            print("You lost ${0}".format(bet))
        if not check_money(stake):
            break
        print("\n*************\n")
        if end_game() == 'n':
            break
        else:
            continue
    # player plays out his or her hand
    final_hands[1] = player_hand, bet
    play_out_hand()
    for hand in final_hands:
        current_hand = final_hands[hand][0]
        hand_total = sum(current_hand)
        current_bet = final_hands[hand][1]
        if len(final_hands) > 1:
            print("*" * 20 + "\n")
            print("Playing hand {0} of {1}\n".format(hand, len(final_hands)))
        print("\n*************\n")
        print("Your total is {0}".format(hand_total))
        if hand_total > 21:
            print("YOU HAVE BUSTED")
            print("You lost {0}".format(current_bet))
            bust = True
            continue
        else:
            bust = False
    if not bust:
        final_dealer_value = play_dealer_hand(dealer_card_1, dealer_hand)
        if not final_dealer_value:
            print("DEALER BUSTS")
            print("\n*************\n")
    for hand in final_hands:
            if len(final_hands) > 1:
                print("HAND {0}".format(hand))
                print("\n*************\n")
            hand_total = sum(final_hands[hand][0])
            hand_bet = final_hands[hand][1]
            if hand_total <= 21:
                if not final_dealer_value:
                    print("You win ${0}".format(hand_bet))
                    stake += hand_bet * 2
                    continue
                elif hand_total > final_dealer_value:
                    print("You won ${0}".format(hand_bet))
                    stake += hand_bet * 2
                elif hand_total < final_dealer_value:
                    print("You lost ${0}".format(hand_bet))
                else:
                    print('PUSH')
                    stake += hand_bet
            print("\n*************\n")
    if not check_money(stake):
        break
    if end_game() == "n":
        dealing = False
    # # build a new deck if the current deck is 2/3rds gone
    elif remaining_cards < (number_of_decks*52)/3:
        working_deck = new_deck(number_of_decks)
        print("*****SHUFFLING*****")
