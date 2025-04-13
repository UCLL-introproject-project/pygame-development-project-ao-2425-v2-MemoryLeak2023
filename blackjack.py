# we importeren de nodige modules
import copy  #twee functies: shallow copy en deep copy. We gaan de DEEPcopy gebruiken.
import random #om willekeurig kaarten te trekken
import pygame

pygame.init() #start alle benodigde modules van Pygame op: beeld, events, tijd

# variabelen van het spel
cards = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A' ]
one_deck = 4 * cards
decks = 4
WIDTH = 600
HEIGHT = 900
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('Pygame Blackjack!')
fps = 60 # snelheid van het spel
timer = pygame.time.Clock()
font = pygame.font.Font('freesansbold.ttf', 44)
smaller_font = pygame.font.Font('freesansbold.ttf', 36)
active = False

#win, loss, draw/push
records = [0,0,0]
player_score = 0
dealer_score = 0
initial_deal = False
my_hand = []
dealer_hand = []
outcome = 0
revael_dealer = False
hand_active = False
outcome = 0
add_score = False
results = ['', 'PLAYER BUSTED o_O', 'Player WINS! :-)', 'DEALER WINS :(', 'TIE GAME...']

# Deze functie deelt één willekeurige kaart uit van het deck aan een hand.
def deal_cards(current_hand, current_deck):
    card = random.randint(0, len(current_deck))
    current_hand.append(current_deck[card-1]) #Neem de kaart op index card - 1 uit het deck en voeg die toe aan de hand.
    current_deck.pop(card-1) #Verwijder diezelfde kaart uit het deck (anders zou ze dubbel kunnen worden uitgedeeld).
    return current_hand, current_deck

# Toon de scores voor de player en de dealer op het scherm
def draw_scores(player, dealer):
    screen.blit(font.render(f'Score[{player}]', True, 'white'), (350, 400)) #font.render maakt een stukje tekst aan. De 'True' geeft aan dat de tekst gladde randen moet hebben. 'White' is de kleur van de tekst.
    if revael_dealer:
        screen.blit(font.render(f'Score[{dealer}]', True, 'white'), (350, 100))

