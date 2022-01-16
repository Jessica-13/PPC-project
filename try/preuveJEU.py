#!/usr/bin/env python3

# Preuve jeu
from random import randint
deck = [4 for foo in range(10)]
score = 0.0
dscore = 0.0
 
def give_card():
    # Return a card and remove it from the deck
    global deck
    while any(deck):
        card = randint(0, 9)
        if deck[card] > 0:
            deck[card] -= 1
            return card
 
def cscore(hit, score):
    # Calculate the score
    if hit < 7:
        return score + hit + 1
    else:
        # Gold King
        if hit == 10 and randint(0, deck[9]-1) == 0:
            print("è uscita la matta!")
            return 7
        else:
            return score + 0.5
 
while True:
    print("***************************************")
    # I need first card value because dealer can't see it
    your_card = fcard = give_card()
    score = cscore(your_card, score)
    dealer_card = give_card()
    dscore = cscore(dealer_card, dscore)
    print("Tua carta: %d (%.1f)" % (your_card+1, score))
    # Card request
    while True:
        # Your turn
        if input("\nAltra carta? [y/n]") == 'y':
            your_card = give_card()
            print("[Carta] %d" % (your_card+1))
            score = cscore(your_card, score)
            print("Punteggio: %.1f" % score)
            if score > 7.5:
                print("**** Hai sballato! ****")
                break
        # Dealer turn
        else:
            # Dealer ask for a card if his score is lower then your shown score
            # Dealer may think you are bluffing (randint)
            print("Il banco ha: %d (%.1f)" % (dealer_card+1, dscore))
            while dscore < score - cscore(fcard, 0) or randint(0, 3) == 0\
                  and dscore < 7.5:
                dealer_card = give_card()
                print("[Carta] %d" % (dealer_card+1))
                dscore = cscore(dealer_card, dscore)
                if dscore > 7.5:
                    break
            print("Punteggio del banco: %.1f" % dscore)
            if score > dscore or dscore > 7.5:
                print("\o/ \o/ \o/ Hai vinto! \o/ \o/ \o/")
            else:
                print("**** Hai perso! ****")
            break
    # Game request
    if input("\nGiochi ancora? [y/n]") == 'y':
        score = 0.0
        dscore = 0.0
        print("\n")
    else:
        break