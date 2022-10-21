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
    card_suit = card[-1]
    suits = {"s": "Spades", "c": "Clubs", "d": "Diamonds", "h": "Hearts"}
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
def play_out_hand(hand, bet):
    global remaining_cards
    global stake
    global working_deck
    hand_value = sum(hand)
    playing = True
    cards_dealt = 0
    while playing:
        play = get_player_choices(hand, cards_dealt)
        if play == "sp":
            if bet > stake:
                print("You don't have enough money to split")
                continue
            else:
                return split(hand, bet)
        elif play == "d":
            if stake < bet:
                print("You don't have enough money to double down")
                continue
            else:
                stake -= bet
                bet = 2 * bet
        # hit or double gets a new card
        if play == "h" or play == "d":
            next_card = deal_card(working_deck)
            cards_dealt += 1
            hand.append(next_card[1])
            hand_value += next_card[1]
            print("\n*************\n")
        # if player busts, check for an ace valued at 11 and change it to a 1
            if hand_value > 21:
                if 11 in hand:
                    hand, hand_value = switch_ace_to_1(hand)
                    print("You got the {0}\nfor a total of {1}".format(next_card[0], hand_value))
                    print("\n*************\n")
                    if play == "d":
                        return hand_value, bet
                    else:
                        continue
                else:
                    print("You got the {0}\nfor a total of {1}".format(next_card[0], hand_value))
                    print("YOU HAVE BUSTED")
                    print("You lose {0}".format(bet))
                    print("\n*************\n")
                    # if not check_money(stake):
                    #     break
                return None
            else:
                print("You got the {0}\nfor a total of {1}".format(next_card[0], hand_value))
                print("\n*************\n")
            # Player ony gets one card for doubling down
                if play == "d":
                    return hand_value, bet
                else:
                    continue
        # stand returns hand and value
        elif play == "s":
            return hand_value, bet
        else:
            continue


def split(hand, bet):
    global working_deck
    bet_1 = bet
    bet_2 = bet
    hand_1 = [hand[0]]
    hand_2 = [hand[1]]
    new_card = deal_card(working_deck)
    hand_1.append(new_card[1])
    hand_1_value = sum(hand_1)
    print("First hand receives the {0}\nfor a total of {1}".format(new_card[0], hand_1_value))
    final_hand_1 = play_out_hand(hand_1, bet_1)
    # hand_1_value, bet_1 = play_out_hand(hand_1, bet_1)
    new_card = deal_card(working_deck)
    hand_2.append(new_card[1])
    hand_2_value = sum(hand_2)
    print("Second hand receives the {0}\nfor a total of {1}".format(new_card[0], hand_2_value))
    final_hand_2 = play_out_hand(hand_2, bet_2)
    # hand_2_value, bet_2 = play_out_hand(hand_2, bet_2)
    if final_hand_1 and final_hand_2:
        return final_hand_1[0], final_hand_1[1], final_hand_2[0], final_hand_2[1]
    elif final_hand_1:
        return final_hand_1[0], final_hand_1[1]
    elif final_hand_2:
        return final_hand_2[0], final_hand_2[1]
    else:
        return None


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
    print("\n*************\n")
    return dealer_value


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
        if wager > stake:
            print("You don't have that much money")
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
    print("\n*************\n")
    print("You have the {0} and the {1}\nfor a total of {2}".format(player_card_1[0], player_card_2[0], player_value))
    print("The dealer is showing the {0}".format(dealer_card_2[0]))
    print("\n*************\n")
    if dealer_card_2[1] == 11:
        ask_insurance = input("Insurance? Y/N:\n".lower())
        if insurance == "y":
            if stake < insurance_bet:
                print("You don't have enough money to purchase insurance")
                insurance = "n"
            else:
                Insurance = True
                stake -= insurance_bet
    # check for blackjack!
    if player_value == 21:
        print("You have blackjack!")
        if dealer_value < 21:
            print("You won {0}".format(int(bet * 1.5)))
            stake += int(bet + (bet * 1.5))
            print("\n*************\n")
            if end_game() == "n":
                break
            else:
                continue
        else:
            print("Dealer has blackjack, you have pushed")
            if insurance:
                print("Insurance pays you ${0}".format(insurance_bet))
                stake += bet * 2
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
            print("Insurance pays you {0}".format(insurance_bet))
            stake += bet
        else:
            print("You lost {0}".format(bet))
        if not check_money(stake):
            break
        print("\n*************\n")
        if end_game() == 'n':
            break
        else:
            continue
    # player plays out his or her hand
    hand_results = play_out_hand(player_hand, bet)
    if hand_results:
        number_of_hands = int(len(hand_results)/2)
        final_hands = {1: (hand_results[0], hand_results[1])}
        if number_of_hands > 1:
            final_hands[2] = (hand_results[2], hand_results[3])
        if number_of_hands > 2:
            final_hands[3] = (hand_results[4], hand_results[5])
        if number_of_hands > 3:
            final_hands[4] = (hand_results[6], hand_results[7])
        final_dealer_value = play_dealer_hand(dealer_card_1, dealer_hand)
        if not final_dealer_value:
            print("DEALER BUSTS")
        for hand in range(number_of_hands):
            if number_of_hands > 1:
                print("HAND {0}".format(hand + 1))
                print("\n*************\n")
            playing_hand = final_hands[hand+1]
            playing_total = playing_hand[0]
            playing_bet = playing_hand[1]
            if not final_dealer_value:
                print("You win ${0}".format(playing_bet))
                stake += playing_bet * 2
            else:
                print("You have {0}".format(playing_total))
                print("The dealer has {0}".format(final_dealer_value))
                if playing_total > final_dealer_value:
                    print("PLAYER WINS")
                    print("You won ${0}".format(playing_bet))
                    stake += playing_bet * 2
                elif playing_total < final_dealer_value:
                    print("DEALER WINS")
                    print("You lost ${0}".format(playing_bet))
                else:
                    print('PUSH')
                    stake += playing_bet
            print("\n*************\n")
        if not check_money(stake):
            break
    else:
        if not check_money(stake):
            break
        elif end_game() == "n":
            break
        else:
            continue
    if end_game() == "n":
        dealing = False
    # build a new deck if the current deck is 2/3rds gone
    elif remaining_cards < (number_of_decks*52)/3:
        working_deck = new_deck(number_of_decks)
        print("*****SHUFFLING*****")
    else:
        continue
