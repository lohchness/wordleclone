import pygame, sys

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
LETTER_LIMIT = NUM_COLS
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
    curr_word = ""
    word_count = 0
    curr_letter = 0
    rects = []

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    # Prevents IndexErrors
                    if curr_word: 
                        curr_word = curr_word[:-1]
                        curr_letter -= 1
                elif event.key == pygame.K_RETURN:
                    continue
                else:
                    if len(curr_word) < LETTER_LIMIT:
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

        if curr_word:
            for letter_index in range(curr_letter):
                word_surface = font.render(curr_word[letter_index], True, WHITE)
                # [0] represents X coord, [1] Y.
                SCREEN.blit(word_surface, (rects[word_count][letter_index][0]+X_PADDING, rects[word_count][letter_index][1]+Y_PADDING))

        pygame.display.update()
        clock.tick(FPS)

if __name__ == "__main__":
    print(BASE_OFFSET_X)
    print(BASE_OFFSET_Y)
    main()