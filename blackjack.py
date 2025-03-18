import random
import numpy as np
import statistics

class Blackjack():

    def __init__(self, epsilon = 0.05):
        # Drawable cards
        self.cards = ["A",2,3,4,5,6,7,8,9,10,"J","Q","K"]
        
        # Hyperparameters
        self.epsilon = epsilon

        # Q table enumerations
        self.hand_sum = [12,13,14,15,16,17,18,19,20]
        self.dealer_card = ["A",2,3,4,5,6,7,8,9,10]
        self.playable_ace = [True, False]
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
        self.q_table = np.zeros((len(self.actions),len(self.hand_sum),len(self.dealer_card),len(self.playable_ace)))


    def draw(self, n):
        """Draws n cards from the deck"""
        drawn_cards = []
        for i in range(n):
            card = random.choice(self.cards)
            drawn_cards.append(card)
        return drawn_cards


    def play(self, human_user = False):
        """Play a hand of blackjack. Returns a tuple of (reward, state history). Reward is 1 for a win, 0 for a draw, -1 for a loss"""
        player_cards = self.draw(2)
        dealer_cards = self.draw(1)
        if human_user:
            for card in player_cards:
                print(f"You drew {card}")
            print(f"Dealer card is {dealer_cards[0]}")

        player_hand_sum, player_playable_ace = self.check_hand(player_cards)
        if human_user:
            print(f"Hand sum is {player_hand_sum}")

        # Automatically draw another card if hand_sum is <12 (cannot bust)
        while player_hand_sum < 12:
            card = self.draw(1)
            player_cards = player_cards + card
            player_hand_sum, player_playable_ace = self.check_hand(player_cards)
            if human_user:
                print(f"You drew {card[0]}. Hand sum is {player_hand_sum}")
        
        # Check for immediate blackjack
        if player_hand_sum == 21:
            if human_user:
                print("Lucky blackjack!")
            return 1, []
        
        # Play player
        state_history = []
        action = None
        while not action == "stick":
            # Get player input if human user
            if human_user:
                action = input("stick or hit?")
            # Use epsilon greedy policy to select action 
            else:
                action = self.get_action(player_hand_sum, self.dealer_card_conversion[dealer_cards[0]], player_playable_ace)
            
            # Save state / action pair to history
            if action in ["stick", "hit"]:
                state_history.append((action, player_hand_sum, self.dealer_card_conversion[dealer_cards[0]], player_playable_ace))

            if action == "hit":
                # Draw a card
                card = self.draw(1)
                player_cards = player_cards + card
                player_hand_sum, player_playable_ace = self.check_hand(player_cards)
                if human_user:
                    print(f"You drew {card[0]}. Hand sum is {player_hand_sum}")

                # Check for player_bust
                if player_hand_sum > 21:
                    if human_user:
                        print("You bust!")
                    return -1, state_history

                # Check for blackjack
                if player_hand_sum == 21:
                    if human_user:
                        print("Blackjack!")
                    return 1, state_history

        # Play dealer
        while True:
            # Draw a card
            card = self.draw(1)
            dealer_cards = dealer_cards + card
            dealer_hand_sum, _ = self.check_hand(dealer_cards)
            if human_user:
                print(f"Dealer drew {card[0]}. Hand sum is {dealer_hand_sum}")
            
            # Win / loss / draw checks
            if dealer_hand_sum >= 17:

                # Check for dealer bust
                if dealer_hand_sum > 21:
                    if human_user:
                        print("Dealer bust. You win!")
                    return 1, state_history
            
                # Check for dealer win
                if dealer_hand_sum > player_hand_sum:
                    if human_user:
                        print("Dealer won!")
                    return -1, state_history
                
                # Check for draw
                if dealer_hand_sum == player_hand_sum:
                    if human_user:
                        print("Draw!")
                    return 0, state_history
                
                # Check for player win
                if dealer_hand_sum < player_hand_sum:
                    if human_user:
                        print(f"Dealer sticks on {dealer_hand_sum}. You win!")
                    return 1, state_history


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
        # Check for epsilon random action
        random_number = random.random()
        if random_number <= self.epsilon:
            return random.choice(["stick","hit"])
        
        stick_q_value = self.get_q_value("stick", hand_sum, dealer_card, playble_ace)
        hit_q_value = self.get_q_value("hit", hand_sum, dealer_card, playble_ace)
        
        if stick_q_value > hit_q_value:
            return "stick"
        
        elif hit_q_value > stick_q_value:
            return "hit"
        
        else:
            return random.choice(["stick","hit"])


    def get_q_value(self, action, hand_sum, dealer_card, playable_ace):
        """Returns a Q value for a given state / action pair"""
        return self.q_table[self.action_dict[action]][self.hand_sum_dict[hand_sum]][self.dealer_card_dict[dealer_card]][self.playable_ace_dict[playable_ace]]


    def set_q_value(self, action, hand_sum, dealer_card, playable_ace, value):
        """Sets a Q value for a given state / action pair"""
        self.q_table[self.action_dict[action]][self.hand_sum_dict[hand_sum]][self.dealer_card_dict[dealer_card]][self.playable_ace_dict[playable_ace]] = value
        return
    

    def train(self, epochs, alpha = 0.1, track_states = None):
        """Trains the bot using monte carlo control. Will train for epochs, with a learning rate alpha.
        Can track q values for a given state / action pair by setting track_states.
        For example track_states = [("stick",20,5,False), ("hit",16,10,False),("stick",16,10,False)]"""
        
        reward_history = []
        
        # Validate tracked states
        if track_states:
            tracked_states_q_value_history = []
            for i, track_state in enumerate(track_states):
                if len(track_state) != 4:
                    raise ValueError("Tracked state must be tuple of action, hand_sum, dealer_card, playable_ace")
                if track_state[0] not in ["stick", "hit"]:
                    raise ValueError("Tracked action must be stick or hit")
                if track_state[1] not in [12,13,14,15,16,17,18,19,20]:
                    raise ValueError("Tracked hand_sum must be 12, 13, 14, 15, 16, 17, 18, 19, or 20")
                if track_state[2] not in ["A",2,3,4,5,6,7,8,9,10]:
                    raise ValueError("Tracked dealer_card must be 'A', 2, 3, 4, 5, 6, 7, 8, 9, or 10")
                if track_state[3] not in [True, False]:
                    raise ValueError("Tracked playable_ace must be True or False")
                tracked_states_q_value_history.append([])
        
        for i in range(epochs):
            # Simulates a hand
            reward, states = self.play()
            
            # Save reward to reward history
            reward_history.append(reward)
            
            # Loops over all state / action pairs in hand and updates q values 
            for state in states:
                action = state[0]
                hand_sum = state[1]
                dealer_card = state[2]
                playable_ace = state[3]
                
                # Applies monte carlo control update rule
                old_q_value = self.get_q_value(action, hand_sum, dealer_card, playable_ace)
                new_q_value = old_q_value + alpha * (reward - old_q_value)
                self.set_q_value(action, hand_sum, dealer_card, playable_ace, new_q_value)

                # Save q value history for tracked state
                if track_states:
                    for i, track_state in enumerate(track_states):
                        tracked_states_q_value_history[i].append(self.get_q_value(track_state[0],track_state[1],track_state[2],track_state[3]))
        
        if track_state:
            return reward_history, tracked_states_q_value_history
        
        else:
            return reward_history
    

    def moving_average_reward(self, reward_history, n):
        """Converts training reward history to a rolling reward over n hands"""
        return np.convolve(reward_history, np.ones(n), 'valid') / n



