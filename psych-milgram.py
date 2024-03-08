import pygame
import math
import random
import time
from import_file import import_file

pygame.init()

screen = pygame.display.set_mode()
WIDTH, HEIGHT = screen.get_size()
WIN = pygame.display.set_mode()
pygame.display.set_caption("Matching Card Game")
TIME_FONT = pygame.font.SysFont("comicsansms", 30)
QUESTION_FONT = pygame.font.SysFont("arial", 20)

FPS = 24

PLAYING_AREA_WIDTH, PLAYING_AREA_HEIGHT = HEIGHT, HEIGHT
PLAYING_AREA = pygame.Rect((WIDTH/2)-(PLAYING_AREA_WIDTH/2), (HEIGHT/2)-(PLAYING_AREA_HEIGHT/2), PLAYING_AREA_WIDTH, PLAYING_AREA_HEIGHT)
border_width = 2

# questions_dict = {
#     "age of experimenter": "31",
#     "age of stooge learner": "47",
#     "age of participants": "20-50",
#     "sample size": "40",
#     "maximum voltage": "450",
#     "number of people went to max voltage": "26",
#     "lowest voltage stopped": "300",
#     "num of people who had seizures": "3",
#     "num of people who showed signs of nervous laughter and smiling": "14"
# }

questions_dict = import_file()

questions = list(questions_dict.keys())
answers = list(questions_dict.values())
questions_and_answers = questions + answers
q_and_a_copy = questions_and_answers[:]
randomised_q_and_a = []
card_list = []

for i in range(0, len(questions_and_answers)):

    each_q_or_a = random.randint(0, len(q_and_a_copy) - 1)
    randomised_q_and_a.append(q_and_a_copy[each_q_or_a])
    q_and_a_copy.remove(q_and_a_copy[each_q_or_a])

q_per_side = math.ceil(math.sqrt((len(questions)*2)))

CARD_WIDTH = math.floor((PLAYING_AREA_WIDTH - border_width*(q_per_side+1))/q_per_side)
CARD_HEIGHT = math.floor((PLAYING_AREA_HEIGHT - border_width*(q_per_side+1))/q_per_side)

def renderTextCenteredAt(text, font, colour, x, y, screen, allowed_width):
    words = text.split()

    lines = []
    while len(words) > 0:
        line_words = []
        while len(words) > 0:
            line_words.append(words.pop(0))
            fw, fh = font.size(' '.join(line_words + words[:1]))
            if fw > allowed_width:
                break

        line = ' '.join(line_words)
        lines.append(line)

    y_offset = 0
    for line in lines:
        fw, fh = font.size(line)

        tx = x - fw / 2
        ty = y + y_offset

        font_surface = font.render(line, True, colour)
        screen.blit(font_surface, (tx, ty))

        y_offset += fh




def load_card(pos_x, pos_y, width, height, card_list):
    card = pygame.Rect(pos_x, pos_y, width, height)
    card_list.append(card)




def draw_text(pos_x, pos_y, width, height, text):
    card_center_x = pos_x + (width/2)
    card_center_y = pos_y + (height/2) - 20
    renderTextCenteredAt(text, QUESTION_FONT, "black", card_center_x, card_center_y, WIN, width - 5)

def main():
    run = True
    clock = pygame.time.Clock()

    first_click = False
    start_time = time.time()
    elapsed_time = 0
    click1 = False
    click2 = False
    both_clicked = False
    both_clicked_time = None
    selected_cards = []

    slot_number = 0
    for row in range(1, q_per_side + 1):
        for column in range(1, q_per_side + 1):
            if slot_number > (len(randomised_q_and_a)-1):
                break
            else:
                slot_location_x = math.floor(PLAYING_AREA.x + (PLAYING_AREA_WIDTH*(column/q_per_side) - PLAYING_AREA_WIDTH/q_per_side) + border_width)
                slot_location_y = math.floor(PLAYING_AREA.y + (PLAYING_AREA_HEIGHT*(row/q_per_side) - PLAYING_AREA_HEIGHT/q_per_side) + border_width)
            
                load_card(slot_location_x, slot_location_y, CARD_WIDTH, CARD_HEIGHT, card_list)
                slot_number += 1
    card_list_copy = card_list[:]

    while run:
        clock.tick(FPS)

        if not first_click:
            first_click_time = time.time() - start_time
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    first_click = True


        if card_list:
            elapsed_time = time.time() - start_time - first_click_time
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                        run = False
                        break
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if not click1:
                        mouse_x, mouse_y = pygame.mouse.get_pos()
                        for card in card_list:
                            if card.collidepoint(mouse_x, mouse_y):
                                selected_cards.append(card)
                                click1 = True

                    elif not click2:
                        mouse_x, mouse_y = pygame.mouse.get_pos()
                        for card in card_list:
                            if card.collidepoint(mouse_x, mouse_y):
                                if card in selected_cards:
                                    pass
                                else:
                                    selected_cards.append(card)
                                    both_clicked_time = pygame.time.get_ticks()
                                    click2 = True
                    
                
            if click1 and click2:
                both_clicked = True 
                if both_clicked and pygame.time.get_ticks() - both_clicked_time >= 500:
                    click1, click2 = False, False

                    option1 = randomised_q_and_a[card_list_copy.index(selected_cards[0])]
                    option2 = randomised_q_and_a[card_list_copy.index(selected_cards[1])]

                    if option1 in list(questions_dict.keys()):
                        if questions_dict[option1] == option2:
                            card_list.remove(selected_cards[0])
                            card_list.remove(selected_cards[1])
                    elif option2 in list(questions_dict.keys()):
                        if questions_dict[option2] == option1:
                            card_list.remove(selected_cards[0])
                            card_list.remove(selected_cards[1])   
                    else:
                        print("Wrong")

                    selected_cards = []

                    both_clicked = False
                    both_clicked_time = None

            WIN.fill("white")

            pygame.draw.rect(WIN ,"black", PLAYING_AREA)

            for card in card_list:
                if card in selected_cards:
                    pygame.draw.rect(WIN, "white", card)

            slot_number = 0
            for row in range(1, q_per_side + 1):
                for column in range(1, q_per_side + 1):
                    if slot_number > (len(randomised_q_and_a)-1):
                        break
                    else:
                        slot_location_x = PLAYING_AREA.x + (PLAYING_AREA_WIDTH*(column/q_per_side) - PLAYING_AREA_WIDTH/q_per_side)
                        slot_location_y = PLAYING_AREA.y + (PLAYING_AREA_HEIGHT*(row/q_per_side) - PLAYING_AREA_HEIGHT/q_per_side)
                        draw_text(slot_location_x, slot_location_y, CARD_WIDTH, CARD_HEIGHT, str(randomised_q_and_a[slot_number]))
                        slot_number += 1

            for card in card_list:
                if card not in selected_cards:
                    pygame.draw.rect(WIN, "white", card)
            
            time_text = TIME_FONT.render(f"Time: {round(elapsed_time * 100)/100}s", 1, "black")
            WIN.blit(time_text, (10,10))
            pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                    run = False
                    break
    
    pygame.quit()

if __name__ == "__main__":
    main()