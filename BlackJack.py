'''
This is the backend file for the BlackJack game.
'''

class BlackJack:
    '''
    This class contains the backend logic for the BlackJack game.
    '''
    def __init__(self):
        self.userCards = []
        self.dealerCards = []
        
    def setUserCards(self, card):
        '''Stores User's cards.'''
        self.userCards.append(card)
        self.userScore = sum([self.getCardValue(self.getCardTuple(card)) for card in self.userCards])

    def setDealerCards(self, card):
        '''Stores Dealer's cards.'''
        self.dealerCards.append(card)
        self.dealerScore = sum([self.getCardValue(self.getCardTuple(card)) for card in self.dealerCards])
     

    def convertCards(self, cardList):
        '''Converts the cardlist into tupleList.'''
        return [self.getCardTuple(card) for card in cardList]

    def getCardTuple(self, cardIdx):
        '''Returns the respective card Tuple (suit, card) based on 0-52 indices.'''
        cardTuple = ()
        cardname = ''
        
        cardId = (cardIdx) % 13  # Reduce card index to a range of 0-12
        suitId = (cardIdx) // 13 # Reduce card index to a range of 0-3

        if cardId >= 9:
            if cardId == 9:
                cardname = 'Ace'
            elif cardId == 10:
                cardname = 'Jack'
            elif cardId == 11:
                cardname = 'Queen'
            elif cardId == 12:
                cardname = 'King'
        else:
            cardname = str(cardId+2)
        
        # returns the suit
        if suitId == 0:
            cardTuple = ('spades', cardname)
        if suitId == 1:
            cardTuple = ('hearts', cardname)
        if suitId == 2:
            cardTuple = ('clubs', cardname)
        if suitId == 3:
            cardTuple = ('diamonds', cardname)

        return cardTuple

    
    def getCardValue(self, cardTuple):
        '''returns the value of the card'''
        cardValue = 0
        if cardTuple[1] == 'Jack' or cardTuple[1] == 'Queen' or cardTuple[1] == 'King':
            cardValue = 10
        elif cardTuple[1] == 'Ace':
            cardValue = 11
        else:
            cardValue = int(cardTuple[1])
        return cardValue


    def checkCards(self) -> str:
        '''Checks if the user or dealer has a blackjack.'''
        userCardValues = [self.getCardValue(self.getCardTuple(card)) for card in self.userCards]
        dealerCardValues = [self.getCardValue(self.getCardTuple(card)) for card in self.dealerCards]
        userSum = sum(userCardValues)
        dealerSum = sum(dealerCardValues)

        if userSum == 21 and dealerSum == 21:
            return 'draw'
        elif userSum == 21:
            return 'user'
        elif dealerSum == 21:
            return 'dealer'
        elif userSum > 21:
            return 'dealer'
        elif dealerSum > 21:
            return 'user'
        else:
            return 'continue'
        
    
    def checkDealerConditions(self):
        '''Checks if the dealer wins or not.'''
        if self.dealerScore > 21:
            return 'user'
        elif self.dealerScore > self.userScore:
            return 'dealer'
        elif self.dealerScore < self.userScore:
            return 'user'
        else:
            return 'draw'
        