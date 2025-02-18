import random

class Blackjack():

    def __init__(self):
        self.cards = ["A",2,3,4,5,6,7,8,9,10,"J","Q","K"]
    

    def draw(self, n):
        """Draws n cards from the deck"""
        drawn_cards = []
        for i in range(n):
            card = random.choice(self.cards)
            drawn_cards.append(card)
        return drawn_cards


    def play(self):
        """Play a hand of blackjack. Returns 1 for a win and 0 for a loss"""
        player_cards = self.draw(2)
        dealer_cards = self.draw(1)
        for card in player_cards:
            print(f"You drew {card}")
        print(f"Dealer card is {dealer_cards[0]}")

        player_hand_sum, playable_ace = self.check_hand(player_cards)
        print(f"Hand sum is {player_hand_sum}")

        inp = None
        while not inp == "s":
            inp = input("hit (h) or stick (s)?")
            if inp == "h":
                # Draw a card
                card = self.draw(1)
                player_cards = player_cards + card
                player_hand_sum, playable_ace = self.check_hand(player_cards)
                print(f"You drew {card[0]}. Hand sum is {player_hand_sum}")

                # Check for player_bust
                if player_hand_sum > 21:
                    print("You bust!")
                    return 0

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
            
            # Check for dealer bust
            if dealer_hand_sum > 21:
                print("Dealer bust. You win!")
                return 1
            
            # Check for dealer win
            if dealer_hand_sum >= player_hand_sum:
                print("Dealer won!")
                return 0
            
            # End the game if dealer hand > 16
            if dealer_hand_sum > 16:
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





