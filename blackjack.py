import random

suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 'Nine':9, 'Ten':10, 'Jack':10,
         'Queen':10, 'King':10, 'Ace':11}

playing = True

class Card:
    
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
    
    def __str__(self):
        return self.rank + ' of ' + self.suit

class Deck:
    
    def __init__(self):
        self.deck = []  # start with an empty list
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit,rank))
    
    def __str__(self):
        return ', '.join(map(str,self.deck))

    def shuffle(self):
        random.shuffle(self.deck)
        
    def deal(self):
        return self.deck.pop()

class Hand:
    def __init__(self):
        self.cards = []  # start with an empty list as we did in the Deck class
        self.value = 0   # start with zero value
        self.aces = 0    # add an attribute to keep track of aces
    
    def add_card(self,card):
        self.cards.append(card)
        self.value += values[card.rank]
    
        if card.rank == 'Ace':
            self.aces += 1
            
    def adjust_for_ace(self):
        while self.value > 21 and self.aces > 0:
            self.value -= 10
            self.aces -= 1
        
class Chips:
    
    def __init__(self):
        self.total = 100  # This can be set to a default value or supplied by a user input
        self.bet = 0
        
    def win_bet(self):
        self.total += self.bet
    
    def lose_bet(self):
        self.total -= self.bet

def take_bet(chips):
    while True:
        try:
            chips.bet = int(input("You have ${}. How much do you want to bet? $".format(chips.total)))
        except:
            print('That is an invalid entry, please enter a number.')    
        else: 
            if chips.bet > chips.total:
                print("Sorry, you don't have enough chips to bet that. Try again")
            else:
                break

def hit(deck,hand):
    hand.add_card(deck.deal())
    hand.adjust_for_ace()

def hit_or_stand(deck,hand):
    global playing  # to control an upcoming while loop
    
    while True:
        next_play = input("Do you want to hit or stand? ")
        if next_play == 'hit':
            hit(deck,hand)
        elif next_play == 'stand':
            print("Player stands and dealer's turn next.")
            playing = False
        else:
            print('Sorry, please try again, enter "hit" or "stand".')
            continue
        break
        
def show_some(player,dealer):
    print("\nDealer's Hand:")
    print(" <card hidden>")
    print('',dealer.cards[1])  
    print("\nPlayer's Hand:", *player.cards, sep='\n ')
    
def show_all(player,dealer):
    print("\nDealer's Hand:", *dealer.cards, sep='\n ')
    print("Dealer's Hand =",dealer.value)
    print("\nPlayer's Hand:", *player.cards, sep='\n ')
    print("Player's Hand =",player.value)

def player_busts(player,dealer,chips):
    chips.lose_bet()
    print("Player busts and loses chips. The dealer wins!")

def player_wins(player,dealer,chips):
    chips.win_bet()
    print("Player wins and takes chips! The dealer loses.")

def dealer_busts(player,dealer,chips):
    chips.win_bet()
    print("Dealer busts. Player wins and takes chips!")
    
def dealer_wins(player,dealer,chips):
    chips.lose_bet()
    print("Dealer wins! Player loses chips.")
    
def push(player,dealer):
    print("Dealer and Player tie! It's a push.")

# Game setup
while True:
    # Print an opening statement
    print("Welcome to Black Jack! Get as close to 21 as you can without going over!\n\
    Dealer hits until they reach 17. Aces count as 1 or 11")
    
    # Create & shuffle the deck, deal two cards to each player
    new_deck = Deck()
    new_deck.shuffle()
    
    player_hand = Hand()
    player_hand.add_card(new_deck.deal())
    player_hand.add_card(new_deck.deal())
    
    dealer_hand = Hand()
    dealer_hand.add_card(new_deck.deal())
    dealer_hand.add_card(new_deck.deal())
    
        
    # Set up the Player's chips
    player_chips = Chips()
    
    # Prompt the Player for their bet
    take_bet(player_chips)
    
    # Show cards (but keep one dealer card hidden)
    show_some(player_hand,dealer_hand)
    
    while playing:  # recall this variable from our hit_or_stand function
        
        # Prompt for Player to Hit or Stand
        hit_or_stand(new_deck,player_hand)

        # If player's hand exceeds 21, run player_busts() and break out of loop
        if player_hand.value > 21:
            show_all(player_hand,dealer_hand)
            player_busts(player_hand,dealer_hand,player_chips)
            break
        # Show cards (but keep one dealer card hidden)
        else:
            show_some(player_hand,dealer_hand)
        

    # If Player hasn't busted, play Dealer's hand until Dealer reaches 17
    if player_hand.value <= 21:
        while dealer_hand.value < 17:
            hit(new_deck,dealer_hand)
            break
    
        # Show all cards
        show_all(player_hand,dealer_hand)
        
        # Run different winning scenarios
        if dealer_hand.value > 21:
            dealer_busts(player_hand,dealer_hand,player_chips)
        elif dealer_hand.value > player_hand.value:
            dealer_wins(player_hand,dealer_hand,player_chips)
        elif player_hand.value > dealer_hand.value:
            player_wins(player_hand,dealer_hand,player_chips)
        else:
            push(player_hand,dealer_hand)
            
        
    # Inform Player of their chips total 
    print("\n Player's chip total: ${}".format(player_chips.total))
    # Ask to play again
    new_game = input("Would you like to play again? Enter yes or no: ")
    
    if new_game == 'yes':
        playing = True
        continue
    else:
        print("Thank you for playing!")
        break

        