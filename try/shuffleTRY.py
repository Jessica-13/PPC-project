#!/usr/bin/env python3

# Try shuffle

from random import shuffle 
  
  
class Cards: 
    global suites, values 
    suites = ['Hearts', 'Diamonds', 'Clubs', 'Spades'] 
    values = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K'] 
  
    def __init__(self): 
        pass
  
  
class Deck(Cards): 
    def __init__(self): 
        Cards.__init__(self) 
        self.mycardset = [] 
        for n in suites: 
            for c in values: 
                self.mycardset.append((c)+" "+"of"+" "+n) 
  
    
    def popCard(self): 
        if len(self.mycardset) == 0: 
            return "NO CARDS CAN BE POPPED FURTHER"
        else: 
            cardpopped = self.mycardset.pop() 
            print("Card removed is", cardpopped) 
  
  
class ShuffleCards(Deck): 
  
    
    def __init__(self): 
        Deck.__init__(self) 
  
    
    def shuffle(self): 
        if len(self.mycardset) < 52: 
            print("cannot shuffle the cards") 
        else: 
            shuffle(self.mycardset) 
            return self.mycardset 
  
    
    def popCard(self): 
        if len(self.mycardset) == 0: 
            return "NO CARDS CAN BE POPPED FURTHER"
        else: 
            cardpopped = self.mycardset.pop() 
            return (cardpopped) 
  
  
objCards = Cards() 
objDeck = Deck() 
  
player1Cards = objDeck.mycardset 
print('\n Player 1 Cards: \n', player1Cards) 
  
objShuffleCards = ShuffleCards() 
  
player2Cards = objShuffleCards.shuffle() 
print('\n Player 2 Cards: \n', player2Cards) 
  
print('\n Removing a card from the deck:', objShuffleCards.popCard()) 
print('\n Removing another card from the deck:', objShuffleCards.popCard()) 
