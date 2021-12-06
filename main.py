import pygame
import random
import sys


class Game:
    """
    game main
    """

    def __init__(self, width, height):
        self.width = width
        self.height = height

        # small box location
        self.address = range(40, 480, 40)
        self.food_point = [random.choice(self.address), random.choice(self.address)]

        # bigger box size（width）
        self.snake_size = 40

        # change box size
        self.snake = Snake(snake_size=self.snake_size)

        # bg size
        self.width = 480
        self.height = 480

        # score
        self.score = 0

        # distance of every time
        self.distance = 40

        # draw a bg
        pygame.init()

        # show score
        self.score_font = pygame.font.SysFont("Microsoft YaaHei UI.ttf", 20)

        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Bigger Snake Box")

        self.clock = pygame.time.Clock()

        # game Number of frames
        self.fps = 3

        # Game loop
        self.running = True
        self.main()

    def draw_background(self):
        """
        draw background
        """
        self.screen.fill([204, 184, 175])

    def draw_food(self):
        """
        draw small box
        """
        pygame.draw.rect(self.screen, (255, 133, 94), (self.food_point[0], self.food_point[1], self.snake_size, self.snake_size))

    def draw_item(self):
        """
        draw Gridlines and bigger box
        """
        # bigger box
        for snake in self.snake.snake_list[1:]:
            pygame.draw.rect(self.screen, (246, 232, 206),
                             (snake[0], snake[1], self.snake_size, self.snake_size), 0)
        # first bigger box
        pygame.draw.rect(self.screen, (249, 165, 99), (self.snake.snake_list[0][0], self.snake.snake_list[0][1], self.snake_size, self.snake_size), 0)

        # draw Gridlines
        for i in range(0, 481, self.snake_size):
            pygame.draw.line(self.screen, [190, 175, 161], [i, 0], [i, 480], 5)
            pygame.draw.line(self.screen, [190, 175, 161], [0, i], [480, i], 5)

    def get_user_action(self):
        """
        test
        """
        for event in pygame.event.get():

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    if len(self.snake.snake_list) > 1 and self.snake.snake_list[1][0] == self.snake.snake_list[0][0] and self.snake.snake_list[1][1] < self.snake.snake_list[0][1]:
                        break
                    self.snake.move = "Up"

                elif event.key == pygame.K_DOWN:
                    if len(self.snake.snake_list) > 1 and self.snake.snake_list[1][0] == self.snake.snake_list[0][0] and self.snake.snake_list[1][1] > self.snake.snake_list[0][0]:
                        break
                    self.snake.move = "Down"

                elif event.key == pygame.K_LEFT:
                    if len(self.snake.snake_list) > 1 and self.snake.snake_list[1][1] == self.snake.snake_list[0][1] and self.snake.snake_list[1][0] < self.snake.snake_list[0][0]:
                        break
                    self.snake.move = "Left"

                elif event.key == pygame.K_RIGHT:
                    if len(self.snake.snake_list) > 1 and self.snake.snake_list[1][1] == self.snake.snake_list[0][1] and self.snake.snake_list[1][0] > self.snake.snake_list[0][0]:
                        break
                    self.snake.move = "Right"

            elif event.type == pygame.QUIT:
                sys.exit()

    def main(self):
        """
        game main loop
        """
        while self.running:
            self.clock.tick(self.fps)

            self.draw_background()

             # bigger box touch itself

            if self.snake.snake_list[0] in self.snake.snake_list[3:]:
               self.running = False



            self.draw_food()
            self.draw_item()

            # show socres
            content = self.score_font.render("score: " + str(self.score), True, [0, 0, 0])
            self.screen.blit(content, [20, 20])

            # user control
            self.get_user_action()

            # bigger bpx move
            self.snake.snake_move(self.distance, self.width, self.height)

            # bigger box get small box
            if self.snake.eat_food(self.food_point):
                self.food_point = [random.choice(self.address), random.choice(self.address)]
                self.draw_food()
                         # # when bigger box  get small box speed add 1
                # self.fps += 1
                # score add 1
                self.score += 1
            # refresh screen
            pygame.display.update()


class Snake:
    def __init__(self,snake_size):

        # box size
        self.snake_size = snake_size

        # show box
        self.snake_list = [[self.snake_size * 2, self.snake_size * 2]]

        # initial direction
        self.move = "Right"

    def snake_move(self, distance, width, height):
        # box move

        snake_body = self.snake_list[0:-1]


        if self.move == "Up":
            snake_head = [self.snake_list[0][0], self.snake_list[0][1] - distance]
            # print(snake_head[1])

            snake_body.insert(0, snake_head)
            self.snake_list = snake_body

        elif self.move == "Down":
            snake_head = [self.snake_list[0][0], self.snake_list[0][1] + distance]

            snake_body.insert(0, snake_head)
            self.snake_list = snake_body

        elif self.move == "Left":
            snake_head = [self.snake_list[0][0] - distance, self.snake_list[0][1]]

            snake_body.insert(0, snake_head)
            self.snake_list = snake_body

        elif self.move == "Right":

            snake_head = [self.snake_list[0][0] + distance, self.snake_list[0][1]]
            snake_body.insert(0, snake_head)
            self.snake_list = snake_body

        # print("X--->",self.snake_list[0][0])
        # print("Y------>",self.snake_list[0][1])

        if self.snake_list[0][1] < 0:
            self.snake_list[0][1] = height - 40

        if self.snake_list[0][1] >= height:
            self.snake_list[0][1] = 0

        if self.snake_list[0][0] < 0:
            self.snake_list[0][0] = width - 40

        if self.snake_list[0][0] >= width:
            self.snake_list[0][0] = 0

    def eat_food(self, food_point):
        # bigger box get small box
        if food_point == self.snake_list[0]:
            self.snake_list.insert(0, food_point)
            return True


if __name__ == '__main__':
    game = Game(480, 480)


