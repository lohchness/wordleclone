import pygame, sys, random

pygame.init()
pygame.display.set_caption("Wordle Clone")
WIDTH, HEIGHT = 800, 800
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
FPS = 30

GREY = (100, 100, 100)
DARK_GREY = (20, 20, 20)
WHITE = (255, 255, 255)
RED = (255, 108, 108)
COLOR_INCORRECT = (50, 50, 50)
COLOR_MISPLACED = (255, 193, 53)
COLOR_CORRECT = (0, 185, 6)

TEXT_TIMER = 2
NUM_ROWS = 6
NUM_COLS = 5
LETTER_LENGTH = NUM_COLS
RECT_WIDTH = 50
RECT_HEIGHT = 50
# Pixels between each Rect
DX = 10
DY = 10
X_PADDING = 5
Y_PADDING = 5
# Leftmost topmost coordinate where the first rect will be drawn, should be symmetrical. Accounts for number of rects, pixels between rects and rect sizes.
BASE_OFFSET_X = (WIDTH/2)-((NUM_COLS/2)*DX)-((NUM_COLS/2)*RECT_WIDTH)+(((NUM_COLS+1)%2)*(DX/2))
BASE_OFFSET_Y = (HEIGHT/2)-((NUM_ROWS/2)*DY)-((NUM_ROWS/2)*RECT_HEIGHT)+(((NUM_ROWS+1)%2)*(DY/2))

def main():
    clock = pygame.time.Clock()
    letter_font = pygame.font.Font(None, 65)
    text = pygame.font.Font(None, 40)
    used_words = []
    curr_word = ""
    word_count = 0
    curr_letter = 0
    rects = []
    flag_win = False
    flag_lose = False
    flag_invalid_word = False
    flag_not_enough_letters = False
    timer_flag_1 = 0
    timer_flag_2 = 0
    wordlist = [word.replace("\n","") for word in list(open("wordlist.txt"))]
    # guess_word = random.choice(wordlist)
    guess_word = "beast"
    assert(len(guess_word) == LETTER_LENGTH)
    assert(guess_word.islower())

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            # Option to restart game
            if flag_win or flag_lose:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        main()
            else:
                # Upon keypress
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        # Prevents IndexErrors
                        if curr_word: 
                            curr_word = curr_word[:-1]
                            curr_letter -= 1
                    elif event.key == pygame.K_RETURN:
                        if len(curr_word) == 5:
                            if curr_word.lower() in wordlist:
                                word_count += 1
                                used_words.append(curr_word)
                                curr_word = ""
                                curr_letter = 0
                            else:
                                flag_invalid_word = True
                                timer_flag_1 = 0
                        else:
                            flag_not_enough_letters = True
                            timer_flag_2 = 0
                    else:
                        if len(curr_word) < LETTER_LENGTH:
                            if event.unicode.isalpha():
                                curr_word += event.unicode.upper()
                                curr_letter += 1
          
        SCREEN.fill(DARK_GREY)
        # Draw title and underline
        draw_title(letter_font)
        # Draws base 5x6 grid for letters
        for y in range(NUM_ROWS):
            row_rects = []  
            for x in range(NUM_COLS):
                x_pos = BASE_OFFSET_X+(x*DX)+(x*RECT_WIDTH)
                y_pos = BASE_OFFSET_Y+(y*DY)+(y*RECT_HEIGHT)
                curr_rect = pygame.Rect((x_pos, y_pos), (RECT_WIDTH, RECT_HEIGHT))
                pygame.draw.rect(SCREEN,GREY,curr_rect,2)
                row_rects.append((x_pos, y_pos))
            rects.append(row_rects)
        
        # Alerts player that word is not in wordlist. Text appears for 2 seconds.
        if flag_invalid_word:
            timer_flag_2 = 0
            flag_not_enough_letters = False
            text_surface = text.render("Not in word list", True, RED)
            # Should be about center aligned. Use of magic numbers, but not serious.
            x_pos = BASE_OFFSET_X + (RECT_WIDTH * (NUM_COLS/5))
            y_pos = BASE_OFFSET_Y - (DY*4)
            SCREEN.blit(text_surface, (x_pos, y_pos))
            timer_flag_1 += 1
        if flag_not_enough_letters:
            timer_flag_1 = 0
            flag_invalid_word = False
            text_surface = text.render("Not enough letters", True, RED)
            x_pos = BASE_OFFSET_X + (RECT_WIDTH * (NUM_COLS/10))
            y_pos = BASE_OFFSET_Y - (DY*4)
            SCREEN.blit(text_surface, (x_pos, y_pos))
            timer_flag_2 += 1
        if timer_flag_1 == TEXT_TIMER * FPS:
            flag_invalid_word = False
            timer_flag_1 = 0
        if timer_flag_2 == TEXT_TIMER * FPS:
            flag_not_enough_letters = False
            timer_flag_2 = 0

        if flag_win:
            text_surface = text.render("Correct! Press 'R' to play again", True, WHITE)
            x_pos = BASE_OFFSET_X - (RECT_WIDTH * (NUM_COLS/5))
            y_pos = BASE_OFFSET_Y + (DY*7) + (RECT_HEIGHT * NUM_ROWS)
            SCREEN.blit(text_surface, (x_pos, y_pos))
        if flag_lose:
            text_surface = text.render("Try again! Press 'R' to play again", True, WHITE)
            x_pos = BASE_OFFSET_X - (RECT_WIDTH * (NUM_COLS/5))
            y_pos = BASE_OFFSET_Y + (DY*7) + (RECT_HEIGHT * NUM_ROWS)
            SCREEN.blit(text_surface, (x_pos, y_pos))

        # Blits each letter of the current word the user is currently typing.
        # Firstly renders each letter, then blits it on the appropriate rectangle according to which letter it is.
        if curr_word:
            for letter_index in range(len(curr_word)):
                word_surface = letter_font.render(curr_word[letter_index], True, WHITE)
                # [0] represents X coord, [1] Y.
                SCREEN.blit(word_surface, (rects[word_count][letter_index][0]+X_PADDING, rects[word_count][letter_index][1]+Y_PADDING))

        # Renders letters and rects of words already inputted by player.
        if used_words:
            for word_index in range(len(used_words)):
                remaining_letters = list(guess_word)
                num_correct = 0
                
                # Used to make sure that letters that appear more than once don't get counted if that letter appears in guess_word only once.
                # EG: guess_word = "proxy", word = "droop", and 'o' appears more than once. The second 'o' in droop does not get counted.
                same_indeces = [i for i,x in enumerate(zip(guess_word,used_words[word_index].lower())) if all(y==x[0] for y in x)]
                # Same indeces - if guessword is "beast" and usedword[word_index] is "toast", same indeces contains the indeces where same letters in the same positions collide, in this case, "a","s","t" - which have indeces of [2,3,4] respectively.
                if same_indeces:
                    for index in range(len(same_indeces)):
                        num_correct += 1
                        remaining_letters[same_indeces[index]] = ""
                        curr_rect = pygame.Rect((rects[word_index][same_indeces[index]][0], rects[word_index][same_indeces[index]][1]), (RECT_WIDTH, RECT_HEIGHT))
                        pygame.draw.rect(SCREEN,COLOR_CORRECT,curr_rect)
                        past_letter_surface = letter_font.render(used_words[word_index][same_indeces[index]].upper(), True, WHITE)
                        SCREEN.blit(past_letter_surface,(rects[word_index][same_indeces[index]][0]+X_PADDING, rects[word_index][same_indeces[index]][1]+Y_PADDING))

                for letter_index in range(LETTER_LENGTH):
                    if letter_index not in same_indeces:
                        curr_rect = pygame.Rect((rects[word_index][letter_index][0], rects[word_index][letter_index][1]), (RECT_WIDTH, RECT_HEIGHT))
                        cur_past_letter = used_words[word_index][letter_index].lower()
                        past_letter_surface = letter_font.render(cur_past_letter.upper(), True, WHITE)
                        # Incorrect Letters
                        if cur_past_letter not in remaining_letters:
                            pygame.draw.rect(SCREEN,COLOR_INCORRECT,curr_rect)
                        # Letter exists in word, but wrong position.
                        else:
                            pygame.draw.rect(SCREEN,COLOR_MISPLACED,curr_rect)
                            remaining_letters[remaining_letters.index(cur_past_letter)] = ""
                        SCREEN.blit(past_letter_surface,(rects[word_index][letter_index][0]+X_PADDING, rects[word_index][letter_index][1]+Y_PADDING))
                        
                # Win/lose condition
                if num_correct == 5:
                    flag_win = True
                elif len(used_words) == NUM_ROWS:
                    flag_lose = True  

        pygame.display.update()
        clock.tick(FPS)

def draw_title(font):
    pygame.draw.line(SCREEN, WHITE, (BASE_OFFSET_X-RECT_WIDTH, BASE_OFFSET_Y-RECT_HEIGHT), (BASE_OFFSET_X + (RECT_WIDTH*(NUM_COLS+1)) + (DX*(NUM_COLS-1)), BASE_OFFSET_Y-RECT_HEIGHT), width=1)
    title_surface = font.render("WORDLE", True, WHITE)
    SCREEN.blit(title_surface, (BASE_OFFSET_X+RECT_WIDTH, BASE_OFFSET_Y-(RECT_HEIGHT*2)))

if __name__ == "__main__":
    main()