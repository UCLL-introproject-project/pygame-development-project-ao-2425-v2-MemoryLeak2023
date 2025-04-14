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
reveal_dealer = False
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

# Toon de scores voor de player en de dealer op het scherm -> hiervoor gebruik je .BLIT!!
def draw_scores(player, dealer):
    screen.blit(font.render(f'Score[{player}]', True, 'white'), (350, 400)) #font.render maakt een stukje tekst aan. De 'True' geeft aan dat de tekst gladde randen moet hebben. 'White' is de kleur van de tekst.
    if reveal_dealer:
        screen.blit(font.render(f'Score[{dealer}]', True, 'white'), (350, 100))

# Toon de kaarten op het scherm
def draw_cards(player, dealer, reveal):
    for i in range(len(player)): #Deze lus loopt over alle kaarten die de speler in zijn hand heeft. i is de index van de kaart.
        pygame.draw.rect(screen, 'white', [70 + (70*i), 460+(5*i), 120, 220], 0, 5) #Teken een witte rechthoek als kaart (de “kaartachtergrond”)
        screen.blit(font.render(player[i], True, 'black'), (75+70*i, 465+5*i)) #Tekst van de kaart bovenaan tonen
        screen.blit(font.render(player[i], True, 'black'), (75+70*i, 635+5*i))
        pygame.draw.rect(screen, 'red', [70+(70*i), 460 + (5*i), 120,220], 5,5) #Teken een rode rand rond de kaart

    # Als de speler nog niet klaar is met zijn beurt, verbergt de dealer 1 kaart
    for i in range(len(dealer)): #e loopt over alle kaarten van de dealer, net zoals je bij de speler doet.
        pygame.draw.rect(screen, 'white', [70+(70*i), 160 + (5*i), 120, 220], 0, 5)
        if i!=0 or reveal: #i != 0: dus alle kaarten behalve de eerste worden normaal weergegeven. Verberg de eerste kaart tenzij reveal == True
            screen.blit(font.render(dealer[i], True, 'black'), (75+70*i, 165+5*i))
            screen.blit(font.render(dealer[i], True, 'black'), (75+70*i, 335+5*i))
        else:
            screen.blit(font.render('???', True, 'black'), (75+70*i, 165+5*i)) #Hier wordt de kaart anoniem gemaakt totdat reveal op True staat.
            screen.blit(font.render('???', True, 'black'), (75+70*i, 335+5*i))
        pygame.draw.rect(screen, 'blue', [70+(70*i), 160+(5*i), 120,220], 5,5) #Een blauwe rand i.p.v. rood, zodat je visueel onderscheid maakt tussen speler en dealer.

# een hand met kaarten omzetten naar de beste mogelijke score in blackjack
def calculate_score(hand):
    #bereken de score 'hand' elke keer opnieuw. Check het aantal azen.
    hand_score = 0 
    aces_count = hand.count('A')

    for i in range(len(hand)):
        # 2,3,4,5,6,7,8,9 -> tel op bij het totaal
        for j in range(8):
            if hand[i] == cards[j]:
                hand_score += int(hand[i])
            # 10 en prentjes -> +10
            if hand[i] in ['10', 'J', 'Q', 'K']:
                hand_score += 10
            # Aas -> we tellen 11 op en checken daarna of we dit moeten wijzigen.
            elif hand[i] == 'A': #dit had ook een else kunnen zijn
                hand_score += 11
        # Ga na hoeveel azen een 1 moeten zijn ipv een 11 om onder de 21 te blijven indien mogelijk.
        if hand_score > 21 and aces_count > 0:
            for i in range(aces_count):
                if hand_score>21:
                    hand_score -= 10
        return hand_score
#spelvoorwaarden en knoppen
def draw_game(act, record, result):
    button_list = []
    #initiële startup van het spel: deal new hand
    if not act:
        deal = pygame.draw.rect(screen, 'white', [150, 20, 300, 100], 0, 5) #Witte knop DEAL HAND
        pygame.draw.rect(screen, 'green', [150, 20, 300, 100], 3, 5) #Groene rand
        deal_text = font.render('DEAL HAND', True, 'black') #toevoegen tekst
        screen.blit(deal_text, (165,50)) #Teken de tekst op het scherm
        button_list.append(deal) #deal-button toevoegen aan button-lijst

    else:
        # HIT-knop
        hit = pygame.draw.rect(screen, 'white', [0, 700, 300, 100], 0, 5)
        pygame.draw.rect(screen, 'green', [0, 700, 300, 100], 3, 5)
        hit_text = font.render('HIT ME', True, 'Black')
        screen.blit(hit_text, (55, 735))
        button_list.append(hit)
        # STAND-knop
        stand = pygame.draw(screen, 'white', [300, 700, 300, 100], 0, 5)
        pygame.draw.rect(screen, 'green', [300, 700, 300, 100], 3, 5)
        stand_text = font.render('STAND', True, 'Black')
        screen.blit(stand_text, (355, 735))
        button_list.append(stand)

        # Scores (win/verlies/gelijk)
        score_text = smaller_font.render(f'Wins: {record[0]} Losses: {record[1]} Draws: {record[2]}', True, 'white')
        screen.blit(score_text, (15, 840))

    # Als het spel een resultaat heeft (win/verlies/gelijk), toon dan resultaat + restart knop
    if result != 0:
        screen.blit(font.render(results[result], True, 'white'), (15, 25)) # Toon resultaattekst
        deal = pygame.draw.rect(screen, 'white', [150, 220, 300, 100], 0, 5)
        pygame.draw.rect(screen, 'green', [150, 220, 300, 100], 3, 5)
        pygame.draw.rect(screen, 'black', [153, 223, 294, 94], 3, 5) # Extra zwarte rand
        deal_text = font.render('NEW HAND', True, 'black')  # Tekst "NEW HAND"
        screen.blit(deal_text, (165, 250))
        button_list.append(deal)
    return button_list  # Geef de knoppenlijst terug voor gebruik in event handling

#Deze functie controleert of het spel is afgelopen, en zo ja: wie heeft gewonnen? + pas scoreborde aan + geef resultaat terug
def check_endgame(hand_act, deal_score, play_score, result, totals, add): 
#hand_act: is de speler nog actief? add: Boolean: mogen we de score nog aanpassen? (zodat we het niet 2 keer doen)

    if not hand_act and deal_score >= 17: # Alleen als de speler klaar is (hand_act is False) én de dealer minstens 17 heeft, mag het spel afgelopen zijn. Dat volgt de Blackjack-regels: de dealer speelt altijd tot hij minstens 17 heeft.
        if play_score > 21:
            result = 1 # speler is gebust (verloren)
        elif deal_score < play_score <= 21 or deal_score >21:
            result = 2 # speler wint (meer dan dealer of dealer bust)
        elif play_score < deal_score <= 21: # dealer wint
            result = 3
        else: # gelijkspel (push)
            result = 4

        # Alleen als add nog True is (dat betekent: scores zijn nog niet bijgewerkt), worden de juiste teller verhoogd in de totals-lijst. Daarna zetten we add = False, zodat dit maar één keer gebeurt.

        #totals is een lijst met drie getallen. Die lijst houdt de spelgeschiedenis bij: hoeveel keer de speler gewonnen, verloren of gelijkgespeeld heeft.

        if add:
            if result == 1 or result == 3:
                totals[1] += 1 #Aantal keer speler gewonnen

            elif result == 2:
                totals[0] += 1 #Aantal keer speler verloren (dealer gewonnen)

            else:
                totals[2] += 1 #Aantal gelijkspellen

            add = False
        return result, totals, add

#main game loop
run = True
while run:
    # Zorg dat het spel draait aan de ingestelde frames per second (fps)
    # Dit maakt de animaties en updates vloeiend
    timer.tick(fps)
    # Vul het scherm telkens met een zwarte achtergrond (maakt oude visuals onzichtbaar)
    screen.fill('black')

    # INITIËLE DELING van kaarten: 2 voor de speler, 2 voor de dealer
    # Dit gebeurt maar één keer per ronde, zodra 'initial_deal' True is
    if initial_deal:
        for i in range(2):
            my_hand, game_deck = deal_cards(my_hand, game_deck)#De speler krijgt een kaart, en het deck wordt weer geüpdatet (omdat die kaart eruit is).
            dealer_hand, game_deck = deal_cards(dealer_hand, game_deck) #De dealer krijgt een kaart, en het deck wordt weer geüpdatet (omdat die kaart eruit is).
        initial_deal = False # Zet terug op False zodat dit blok niet opnieuw gebeurt
 
    # ACTIEVE SPEELFASE: toon kaarten, bereken scores, controleer dealer
    if active:
        player_score = calculate_score(my_hand)  # Bereken de score van de speler op basis van zijn hand
        draw_cards(my_hand, dealer_hand, reveal_dealer)  # Teken de kaarten op het scherm voor zowel speler als dealer

        # Als de kaarten van de dealer mogen getoond worden (reveal dealer == True)
        # Bereken de score en geef hem extra kaarten als hij onder 17 zit (volgens blackjackregels)
        if reveal_dealer:
            dealer_score = calculate_score(dealer_hand)
            if dealer_score < 17:
                dealer_hand, game_deck = deal_cards(dealer_hand, game_deck)
        draw_scores(player_score, dealer_score) # Toon de actuele scores op het scherm
        buttons = draw_game(active, records, outcome) # Teken de knoppen ('HIT ME', 'STAND', etc.) en sla ze op voor eventlisteners