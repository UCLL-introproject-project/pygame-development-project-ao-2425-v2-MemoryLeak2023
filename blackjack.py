# black jack in python with pygame!

import random  # om willekeurig kaarten te trekken
import pygame

# Ik heb de module copy weg gelaten. Deze is niet nodig. Je kan perfect met lijsten werken want deze lijst bevat geen geneste lijsten of objecten. Alleen simpele strings.

pygame.init()  # start alle benodigde modules van Pygame op: beeld, events, tijd
pygame.mixer.init()
background_img = pygame.image.load('project/pygame-development-project-ao-2425-v2-MemoryLeak2023/images_blackjack/Unicorn_banner.png')
unicorn_img = pygame.image.load('project/pygame-development-project-ao-2425-v2-MemoryLeak2023/images_blackjack/unicorn_geen_tekst.png')
background_img = pygame.transform.scale(background_img, (1000, 200))
# variabelen van het spel
cards = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
one_deck = 4 * cards  # een deck bevat 4 keer elke kaart

decks = 4  # aantal decks dat wordt gebruikt
WIDTH = 1000
HEIGHT = 700
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('Pygame Blackjack!')
fps = 60  # snelheid van het spel

# Kaartinstellingen
card_width = 120
card_height = 180
card_spacing = 90  # horizontale afstand tussen kaarten

# Posities van speler- en dealerkaarten
player_y = 480
dealer_y = 50

# Afstand tussen boven- en onderwaarde op de kaart
text_offset_y = 15

# klok voor tijdsbeheer en fonts
timer = pygame.time.Clock()
font = pygame.font.Font('project/pygame-development-project-ao-2425-v2-MemoryLeak2023/marimpa_FONT/Marimpa.ttf', 44)
smaller_font = pygame.font.Font('project/pygame-development-project-ao-2425-v2-MemoryLeak2023/marimpa_FONT/Marimpa.ttf', 36)

active = False  # of het spel bezig is

# win, loss, draw/push
records = [0, 0, 0]  # bijhouden van aantal overwinningen, verliezen en gelijke spelen
player_score = 0
dealer_score = 0
initial_deal = False
my_hand = []
dealer_hand = []
outcome = 0  # status van het spel: 0 = geen, 1 = bust, 2 = win, 3 = verlies, 4 = gelijkspel
reveal_dealer = False
hand_active = False
add_score = False  # wordt True wanneer we de score mogen toevoegen

results = [ '',
    'Huilen maar...',
    'Jij wint! Hoera!',
    'Huilen maar...',
    'Gelijkspel!']

# Geluidjes voor intro, winst, verlies, gelijkspel
intro_sound = pygame.mixer.Sound('project/pygame-development-project-ao-2425-v2-MemoryLeak2023/sounds/magic.wav')
win_sound = pygame.mixer.Sound('project/pygame-development-project-ao-2425-v2-MemoryLeak2023/sounds/success.mp3')
loss_sound = pygame.mixer.Sound('project/pygame-development-project-ao-2425-v2-MemoryLeak2023/sounds/scream.mp3')
draw_sound = pygame.mixer.Sound('project/pygame-development-project-ao-2425-v2-MemoryLeak2023/sounds/giggle.mp3')

# Deze functie deelt één willekeurige kaart uit van het deck aan een hand.
def deal_cards(current_hand, current_deck):
    card = random.randint(0, len(current_deck))
    current_hand.append(current_deck[card - 1])  # kaart toevoegen aan de hand
    current_deck.pop(card - 1)  # kaart verwijderen uit het deck
    return current_hand, current_deck

# Toon de scores op het scherm
def draw_scores(player, dealer):
    screen.blit(font.render(f'Score[{player}]', True, 'white'), (600, 400))
    if reveal_dealer:
        screen.blit(font.render(f'Score[{dealer}]', True, 'white'), (600, 100))

# Teken de kaarten van speler en dealer: ik heb bovenaan de code kaartinstellingen geschreven die het veel makkelijker maken om wijzigen door te voeren in de functie in vergelijking met de oorspronkelijk code.
def draw_cards(player, dealer, reveal):
    # Spelerkaarten
    for i in range(len(player)):
        x = 50 + i * card_spacing
        pygame.draw.rect(screen, (255, 255, 240), [x, player_y, card_width, card_height], 0, 5)
        screen.blit(font.render(player[i], True, (255, 105, 180)), (x + 10, player_y + text_offset_y))
        screen.blit(font.render(player[i], True, (255, 105, 180)), (x + 10, player_y + card_height - 50))
        pygame.draw.rect(screen, (255, 182, 193), [x, player_y, card_width, card_height], 5, 5)

    # Dealerkaarten
    for i in range(len(dealer)):
        x = 50 + i * card_spacing
        pygame.draw.rect(screen, (240, 248, 255), [x, dealer_y, card_width, card_height], 0, 5)
        if i != 0 or reveal:
            screen.blit(font.render(dealer[i], True, (100, 149, 237)), (x + 10, dealer_y + text_offset_y))
            screen.blit(font.render(dealer[i], True, (100, 149, 237)), (x + 10, dealer_y + card_height - 50))
        else:
            screen.blit(font.render('??', True, (100, 149, 237)), (x + 10, dealer_y + text_offset_y))
            screen.blit(font.render('??', True, (100, 149, 237)), (x + 10, dealer_y + card_height - 50))
        pygame.draw.rect(screen, (135, 206, 250), [x, dealer_y, card_width, card_height], 5, 5)

# Bereken de waarde van een hand kaarten
def calculate_score(hand):
    hand_score = 0
    aces_count = hand.count('A')
    
    for card in hand:
        if card in ['2', '3', '4', '5', '6', '7', '8', '9']:
            hand_score += int(card)
        elif card in ['10', 'J', 'Q', 'K']:
            hand_score += 10
        elif card == 'A':
            hand_score += 11

    # Corrigeer voor Azen indien nodig
    while hand_score > 21 and aces_count > 0: # als de score in je hand groter is dan 21 en je hebt minstens 1 aas...
        hand_score -= 10 # we geven de aas een waarde van 1 ipv 11
        aces_count -= 1 # we trekken een aas af (anders blijft de while-loop doorlopen)

    return hand_score

# Teken de knoppen en spelstatus op het scherm. Ik maak een klasse aan om de knoppen mét hover effect makkelijker aan te roepen om herhaling in mijn code te vermijden.
class Button:
    def __init__(self, text, x, y, width, height, font, base_color, hover_color, text_color, hover_text_color):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.font = font
        self.base_color = base_color
        self.hover_color = hover_color
        self.text_color = text_color
        self.hover_text_color = hover_text_color

    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        is_hovered = self.rect.collidepoint(mouse_pos)

        # Kies de juiste kleuren op basis van hover
        bg_color = self.hover_color if is_hovered else self.base_color
        txt_color = self.hover_text_color if is_hovered else self.text_color

        # Teken knop en rand
        pygame.draw.rect(screen, bg_color, self.rect, 0, 5)  # knop-achtergrond
        pygame.draw.rect(screen, (255, 215, 0), self.rect, 3, 5)  # rand (goud)

        # Teken tekst in het midden
        text_surface = self.font.render(self.text, True, txt_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONUP:
            if self.rect.collidepoint(event.pos):
                return True
        return False

def draw_game(act, record, result, font, smaller_font):
    button_list = []
    #plaatsing van objecten dynamisch maken -> responsief!
    screen_width = screen.get_width() #geeft de breedte van het venster terug in pixels.
    screen_height = screen.get_height() #geeft de hoogte van het venster terug in pixels.

    button_width = 250
    button_height = 80
    spacing = 20  # ruimte tussen knoppen

    # Posities berekenen
    mid_x = screen_width // 2
    y_position = screen_height - button_height - 30  # onderaan met beetje marge

    # MOUSE POS VOOR ALLE KNOPPEN
    mouse_pos = pygame.mouse.get_pos()

    if not act:
        # Startknop: DEAL HAND
        intro_sound.play(0)
        deal_btn = Button(
            text="DEAL HAND",
            x=mid_x - button_width // 2,
            y=y_position,
            width=button_width,
            height=button_height,
            font=font,
            base_color=(255, 255, 255),
            hover_color=(200, 162, 200),  # zachte paarstint
            text_color='black',
            hover_text_color=(75, 0, 130)  # indigo
        )
        deal_btn.draw(screen)
        button_list.append(deal_btn)

    else:
        # HIT ME knop links van het midden
        hit_btn = Button(
            text="HIT ME",
            x=0.95 * mid_x,
            y=y_position,
            width=button_width - 30,
            height=button_height,
            font=font,
            base_color=(255, 255, 255),
            hover_color=(255, 182, 193),
            text_color='black',
            hover_text_color=(255, 105, 180)
        )
        hit_btn.draw(screen)
        button_list.append(hit_btn)

        # STAND-knop rechts van midden
        stand_btn = Button(
            text="STAND",
            x=1.45 * mid_x,
            y=y_position,
            width=button_width - 30,
            height=button_height,
            font=font,
            base_color=(255, 255, 255),
            hover_color=(255, 182, 193),
            text_color='black',
            hover_text_color=(255, 105, 180)
        )
        stand_btn.draw(screen)
        button_list.append(stand_btn)

        # Scoretekst
        score_text = smaller_font.render(f'Wins: {record[0]}   Losses: {record[1]}   Draws: {record[2]}', True, 'white')
        screen.blit(score_text, (0.95 * mid_x, 20))

    # Bij einde spel: restart-knop
    if result != 0:
        result_text = font.render(results[result], True, 'white')
        screen.blit(result_text, (550, 180))

        new_hand_btn = Button(
            text="NEW HAND",
            x=1.4 * mid_x,
            y=y_position - 100,
            width=button_width,
            height=button_height,
            font=smaller_font,  # kleinere font voor deze knop
            base_color=(255, 255, 255),
            hover_color=(221, 160, 221),  # plum
            text_color='black',
            hover_text_color=(128, 0, 128)  # paars
        )
        new_hand_btn.draw(screen)
        button_list.append(new_hand_btn)

    return button_list

# Controleer of het spel is afgelopen en wie er gewonnen heeft
def check_endgame(hand_act, deal_score, play_score, result, totals, add):
    if not hand_act and deal_score >= 17:
        if play_score > 21:
            result = 1
        elif deal_score < play_score <= 21 or deal_score > 21:
            result = 2
        elif play_score < deal_score <= 21:
            result = 3
        else:
            result = 4
        if add:
            if result == 1 or result == 3:# verlies voor speler
                loss_sound.play()
                totals[1] += 1  
            elif result == 2:  # winst voor speler
                win_sound.play()
                totals[0] += 1 
            else: # gelijkspel
                draw_sound.play()
                totals[2] += 1  
            add = False
    return result, totals, add

# hoofdloop van het spel
run = True
while run:
    timer.tick(fps)
    
    screen.fill((255, 200, 255))  # een zachtroze achtergrond (RGB)
    screen.blit(background_img, (0, 250))  # banner
    if initial_deal:
        for i in range(2):
            my_hand, game_deck = deal_cards(my_hand, game_deck)
            dealer_hand, game_deck = deal_cards(dealer_hand, game_deck)
        initial_deal = False

    if active:
        player_score = calculate_score(my_hand)
        draw_cards(my_hand, dealer_hand, reveal_dealer)
        if reveal_dealer:
            dealer_score = calculate_score(dealer_hand)
            if dealer_score < 17:
                dealer_hand, game_deck = deal_cards(dealer_hand, game_deck)
        draw_scores(player_score, dealer_score)
    buttons = draw_game(active, records, outcome, font, smaller_font)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONUP:
            if not active:
                if buttons[0].is_clicked(event):
                    active = True
                    initial_deal = True
                    game_deck = list(decks * one_deck)
                    my_hand = []
                    dealer_hand = []
                    outcome = 0
                    hand_active = True
                    reveal_dealer = False
                    add_score = True
            else:
                if buttons[0].is_clicked(event) and player_score < 21 and hand_active:
                    my_hand, game_deck = deal_cards(my_hand, game_deck)
                elif buttons[1].is_clicked(event) and not reveal_dealer:
                    reveal_dealer = True
                    hand_active = False
                elif len(buttons) == 3 and buttons[2].is_clicked(event):
                    if buttons[2].is_clicked(event):
                        active = True
                        initial_deal = True
                        game_deck = list(decks * one_deck)
                        my_hand = []
                        dealer_hand = []
                        outcome = 0
                        hand_active = True
                        reveal_dealer = False
                        add_score = True
                        dealer_score = 0
                        player_score = 0

    if hand_active and player_score >= 21:
        hand_active = False
        reveal_dealer = True

    outcome, records, add_score = check_endgame(hand_active, dealer_score, player_score, outcome, records, add_score)

    pygame.display.flip()
pygame.quit()
