from multiprocessing.context import assert_spawning
import pygame, sys, random

pygame.init()
pygame.display.set_caption("Wordle Clone")
WIDTH, HEIGHT = 800, 800
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
FPS = 30

GREY = (100, 100, 100)
DARK_GREY = (20, 20, 20)
WHITE = (255, 255, 255)
COLOR_INCORRECT = (50, 50, 50)
COLOR_MISPLACED = (255, 193, 53)
COLOR_CORRECT = (0, 185, 6)

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
    font = pygame.font.Font(None, 65)
    used_words = []
    curr_word = ""
    word_count = 0
    curr_letter = 0
    rects = []
    flag_win = False
    flag_lose = False

    guess_word = word = random.choice(list(open("wordlist.txt"))).replace("\n", "")
    # guess_word = "proxy"
    assert(len(guess_word) == LETTER_LENGTH)
    assert(guess_word.islower())

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if flag_win or flag_lose:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        main()
            else:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        # Prevents IndexErrors
                        if curr_word: 
                            curr_word = curr_word[:-1]
                            curr_letter -= 1
                    elif event.key == pygame.K_RETURN:
                        if len(curr_word) == 5:
                            word_count += 1
                            used_words.append(curr_word)
                            curr_word = ""
                            curr_letter = 0
                    else:
                        if len(curr_word) < LETTER_LENGTH:
                            curr_word += event.unicode.upper()
                            curr_letter += 1

        SCREEN.fill(DARK_GREY)
        
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

        # Blits each letter of the current word the user is typing.
        # Firstly renders each letter, then blits it on the appropriate rectangle according to which letter it is.
        if curr_word:
            for letter_index in range(len(curr_word)):
                word_surface = font.render(curr_word[letter_index], True, WHITE)
                # [0] represents X coord, [1] Y.
                SCREEN.blit(word_surface, (rects[word_count][letter_index][0]+X_PADDING, rects[word_count][letter_index][1]+Y_PADDING))

        # Renders all past words if available, using similar steps as above block
        if used_words:
            # Renders colors for the squares that the past words' letters are sitting on
            for word in range(len(used_words)):
                num_correct = 0
                # Each iteration of each word in used_words, make a list of remaining letters.
                # Used to make sure that letters that appear more than once don't get counted if that letter appears in guess_word only once.
                # EG: guess_word = "proxy", word = "droop", and 'o' appears more than once. The second 'o' in droop does not get counted.
                remaining_letters = list(guess_word)
                for letter in range(LETTER_LENGTH):
                    curr_rect = pygame.Rect((rects[word][letter][0], rects[word][letter][1]), (RECT_WIDTH, RECT_HEIGHT))
                    # Incorrect letter
                    if used_words[word][letter].lower() not in remaining_letters:
                        pygame.draw.rect(SCREEN,COLOR_INCORRECT,curr_rect)
                    # Letter in word, but incorrect position
                    if used_words[word][letter].lower() in remaining_letters:
                        pygame.draw.rect(SCREEN,COLOR_MISPLACED,curr_rect)
                        # Multi-letter functionality (read above)
                        remaining_letters.remove(used_words[word][letter].lower())
                    # Correct letter
                    if used_words[word][letter].lower() == guess_word[letter]:
                        pygame.draw.rect(SCREEN,COLOR_CORRECT,curr_rect)
                        num_correct += 1

                if num_correct == 5:
                    flag_win = True
                elif len(used_words) == NUM_ROWS:
                    flag_lose = True

            # Renders letters of the word
            for word in range(len(used_words)):
                for letter in range(LETTER_LENGTH):
                    letter_surface = font.render(used_words[word][letter], True, WHITE)
                    SCREEN.blit(letter_surface, (rects[word][letter][0]+X_PADDING, rects[word][letter][1]+Y_PADDING))
        


        pygame.display.update()
        clock.tick(FPS)


if __name__ == "__main__":
    main()