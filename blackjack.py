import random
import numpy as np

class Blackjack():

    def __init__(self, epsilon = 0.05):
        # Drawable cards
        self.cards = ["A",2,3,4,5,6,7,8,9,10,"J","Q","K"]
        
        # Hyperparameters
        self.epsilon = epsilon

        # Q table enumerations
        self.hand_sum = [12,13,14,15,16,17,18,19,20]
        self.dealer_card = ["A",2,3,4,5,6,7,8,9,10]
        self.usable_ace = [True, False]
        self.actions = ["stick","hit"]

        # Map for compressing dealer card
        self.dealer_card_conversion = {
                        "A": "A",
                        2: 2,
                        3: 3,
                        4: 4,
                        5: 5,
                        6: 6,
                        7: 7,
                        8: 8,
                        9: 9,
                        10: 10,
                        "J": 10,
                        "Q": 10,
                        "K": 10
        }
        
        # Maps for state variables to locations in q table
        self.action_dict = {
                        "stick": 0,
                        "hit": 1
                    }
        
        self.hand_sum_dict = {
                        12: 0,
                        13: 1,
                        14: 2,
                        15: 3,
                        16: 4,
                        17: 5,
                        18: 6,
                        19: 7,
                        20: 8
        }

        self.dealer_card_dict = {
                        "A": 0,
                        2: 1,
                        3: 2,
                        4: 3,
                        5: 4,
                        6: 5,
                        7: 6,
                        8: 7,
                        9: 8,
                        10: 9
        }

        self.playable_ace_dict = {
                        True: 0,
                        False: 1
        }

        # Q table
        self.q_table = np.zeros((len(self.actions),len(self.hand_sum),len(self.dealer_card),len(self.usable_ace)))


    def draw(self, n):
        """Draws n cards from the deck"""
        drawn_cards = []
        for i in range(n):
            card = random.choice(self.cards)
            drawn_cards.append(card)
        return drawn_cards


    def play(self, human_user = False):
        """Play a hand of blackjack. Returns 1 for a win and 0 for a loss"""
        player_cards = self.draw(2)
        dealer_cards = self.draw(1)
        for card in player_cards:
            print(f"You drew {card}")
        print(f"Dealer card is {dealer_cards[0]}")

        player_hand_sum, playable_ace = self.check_hand(player_cards)
        print(f"Hand sum is {player_hand_sum}")
        
        # Play player
        state_history = []
        inp = None
        while not inp == "stick":
            # Get player input if human user
            if human_user:
                inp = input("stick or hit?")
            # Use epsilon greedy policy to select action 
            else:
                inp = self.get_action(player_hand_sum, self.dealer_card_conversion[dealer_cards[0]], playable_ace)
            
            # Save state / action pair to history
            if inp in ["stick", "hit"]:
                state_history.append((inp, player_hand_sum, self.dealer_card_conversion[dealer_cards[0], player_playable_ace]))

            if inp == "h":
                # Draw a card
                card = self.draw(1)
                player_cards = player_cards + card
                player_hand_sum, player_playable_ace = self.check_hand(player_cards)
                print(f"You drew {card[0]}. Hand sum is {player_hand_sum}")

                # Check for player_bust
                if player_hand_sum > 21:
                    print("You bust!")
                    return -1

                # Check for blackjack
                if player_hand_sum == 21:
                    print("Blackjack!")
                    return 1

        # Play dealer
        while True:
            # Draw a card
            card = self.draw(1)
            dealer_cards = dealer_cards + card
            dealer_hand_sum, _ = self.check_hand(dealer_cards)
            print(f"Dealer drew {card[0]}. Hand sum is {dealer_hand_sum}")
            
            # Win / loss / draw checks
            if dealer_hand_sum >= 17:

                # Check for dealer bust
                if dealer_hand_sum > 21:
                    print("Dealer bust. You win!")
                    return 1
            
                # Check for dealer win
                if dealer_hand_sum > player_hand_sum:
                    print("Dealer won!")
                    return -1
                
                # Check for draw
                if dealer_hand_sum == player_hand_sum:
                    print("Draw!")
                    return 0
                
                # Check for player win
                if dealer_hand_sum < player_hand_sum:
                    print(f"Dealer sticks on {dealer_hand_sum}. You win!")
                    return 1


    def check_hand(self, card_list):
        """Calculates the sum of a hand, and checks whether it has a playable ace"""
        hand_sum = 0
        playable_ace = False
        playable_ace_count = 0

        # Add sum of cards in hand and keep track of playable aces
        for card in card_list:
            if isinstance(card, int):
                hand_sum = hand_sum + card
            elif card in ["J","Q","K"]:
                hand_sum = hand_sum + 10
            elif card == "A":
                playable_ace_count = playable_ace_count + 1
                hand_sum = hand_sum + 11


        # Adjust sum for playable aces if bust
        while playable_ace_count > 0 and hand_sum > 21:
            playable_ace_count = playable_ace_count - 1
            hand_sum = hand_sum - 10

        if playable_ace_count > 0:
            playable_ace = True

        return hand_sum, playable_ace

    def get_action(self, hand_sum, dealer_card, playble_ace):
        """Epsilon greedy action selection"""
        stick_value = self.get_q_value("stick", hand_sum, dealer_card, playble_ace)

        return

    def get_q_value(self, action, hand_sum, dealer_card, playable_ace):
        """Returns a Q value for a given state / action pair"""
        return self.q_table[self.action_dict[action]][self.hand_sum_dict[hand_sum]][self.dealer_card_dict[dealer_card]][self.playable_ace_dict[playable_ace]]


    def set_q_value(self, action, hand_sum, dealer_card, playable_ace, value):
        """Sets a Q value for a given state / action pair"""
        self.q_table[self.action_dict[action]][self.hand_sum_dict[hand_sum]][self.dealer_card_dict[dealer_card]][self.playable_ace_dict[playable_ace]] = value
        return
    

    def train(self, epochs):
        return



