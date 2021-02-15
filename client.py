import pygame
from network import Network
from grids import ShipsGrid, FireGrid
from buttons import Button

pygame.font.init()

width = 600
height = 800
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Client")

SIZE = 50
offsetx = 1
offsety = 3
font = pygame.font.SysFont("Arial", 40)

BLUE = (120, 170, 255)
GREY = (75, 75, 75)
RED = (255, 0, 0)
GREEN = (0, 175, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

colors = [BLUE, GREY, RED, GREEN, WHITE, BLACK]
mode = "setup"


class Random_funcs:
    @staticmethod
    def grid_borders(rows, cols):
        for i in range(rows + 1):
            pygame.draw.line(win, GREY, (SIZE * offsetx, (i + offsety) * SIZE),
                             (width - (SIZE * offsetx), (i + offsety) * SIZE), 1)
        for j in range(cols + 1):
            pygame.draw.line(win, GREY, ((j + offsetx) * SIZE, SIZE * offsety),
                             ((j + offsetx) * SIZE, height - (SIZE * offsety)), 1)

    @staticmethod
    def get_colrow(mouse_pos):
        x, y = mouse_pos
        col = (x // SIZE) - 1
        row = (y // SIZE) - 3
        return (col, row)

    @staticmethod
    def get_colrow_mouse(grid, mouse_pos, moving_ship):
        col, row = Random_funcs.get_colrow(mouse_pos)
        col2, row2 = grid.within_border(moving_ship, col, row)

        return col2, row2


class Mouse_Movements:
    @staticmethod
    def setup_clicking(mouse_pos, shipGrid, btn, n, playerID):
        col, row = Random_funcs.get_colrow(mouse_pos)
        if 10 > col > -1 and 10 > row > -1:
            clicked_pos = (row, col)

            if clicked_pos in shipGrid.ship_blocks:
                for a in range(len(shipGrid.all_ships)):
                    if clicked_pos in shipGrid.all_ships[a][3]:
                        moving_ship = shipGrid.all_ships[a]
                        return moving_ship
            return False
        else:
            global mode
            if btn.click(mouse_pos):
                n.send(str(playerID))
                mode = "setup_wait"

    @staticmethod
    def setup_moving(grid, mouse_pos, moving_ship):
        m_col, m_row = Random_funcs.get_colrow_mouse(grid, mouse_pos, moving_ship)
        grid.moving_ships(moving_ship, m_col, m_row)

    @staticmethod
    def setup_end(grid, mouse_pos, moving_ship):
        e_col, e_row = Random_funcs.get_colrow_mouse(grid, mouse_pos, moving_ship)
        grid.placed_ship(moving_ship, e_col, e_row)

    @staticmethod
    def setup_rotate(grid, mouse_pos):
        col, row = Random_funcs.get_colrow(mouse_pos)
        if (row, col) in grid.ship_blocks:  # if mouse is on a ship
            for a in range(len(grid.all_ships)):  # find the ship
                if (row, col) in grid.all_ships[a][3]:  # rotate the ship
                    rotating_ship = grid.all_ships[a]
                    rot_ship = grid.rotate_ship(grid, rotating_ship)
                    rrow, rcol = rot_ship[3][0]
                    grid.placed_ship(rot_ship, rcol, rrow)

    @staticmethod
    def fire_spot(mouse_pos, fireGrid, firebtn, n):
        global mode
        col, row = Random_funcs.get_colrow(mouse_pos)
        if 10 > col > -1 and 10 > row > -1:
            clicked_pos = (row, col)
            fireGrid.selected = clicked_pos
        else:
            if firebtn.click(mouse_pos):
                fireGrid.shots.append(fireGrid.selected)
                shot = str(fireGrid.selected)
                n.send(shot)

                if fireGrid.win():
                    n.send("end")

    @staticmethod
    def restart_game(mouse_pos, rematchbtn, n):
        global mode
        if rematchbtn.click(mouse_pos):
            n.send("restart")
            mode = "end_wait"


class Drawing_funcs:
    @staticmethod
    def drawBlocks(grid):
        grid.update_blocks()
        for i in grid.blocks:
            i.status_check()
            x = (i.row + offsetx) * SIZE
            y = (i.col + offsety) * SIZE
            pygame.draw.rect(win, i.color, (x, y, SIZE, SIZE))
            if i.circle:
                pygame.draw.circle(win, i.circle, (x + SIZE // 2, y + SIZE // 2), 5)
        Random_funcs.grid_borders(10, 10)

    @staticmethod
    def drawBtns(b, grid):
        b.draw(grid)
        pygame.draw.rect(win, b.color, (b.x, b.y, b.width, b.height))
        text = font.render(b.text, 1, colors[4])
        win.blit(text, (b.x + 75 - int(text.get_width() / 2), b.y + 40 - int(text.get_height() / 2)))

    @staticmethod
    def drawWords(text, x, y):
        text = font.render(text, 1, colors[1])
        win.blit(text, (x, y))

    @staticmethod
    def draw_setup_screen(shipsGrid, btn):
        Drawing_funcs.drawBlocks(shipsGrid)
        Drawing_funcs.drawBtns(btn, shipsGrid)

    @staticmethod
    def draw_setup_wait(shipsGrid):
        Drawing_funcs.drawBlocks(shipsGrid)
        Drawing_funcs.drawWords("Waiting for an Opponent...", 100, 100)

    @staticmethod
    def draw_your_screen(shipsGrid):
        Drawing_funcs.drawBlocks(shipsGrid)
        Drawing_funcs.drawWords("Your Ships", 200, 100)

    @staticmethod
    def draw_fire_screen(fireGrid, firebtn):
        Drawing_funcs.drawBlocks(fireGrid)
        Drawing_funcs.drawWords("Attack Enemy", 200, 100)
        Drawing_funcs.drawBtns(firebtn, fireGrid)

    @staticmethod
    def draw_wait_screen(fireGrid):
        Drawing_funcs.drawBlocks(fireGrid)
        Drawing_funcs.drawWords("Waiting for Opponent...", 150, 100)

    @staticmethod
    def draw_end_screen(fireGrid, text, rematchbtn):
        Drawing_funcs.drawBlocks(fireGrid)
        Drawing_funcs.drawWords(text, 150, 100)
        Drawing_funcs.drawBtns(rematchbtn, fireGrid)


def drawWin(shipsGrid, fireGrid, readybtn, firebtn, rematchbtn, game, playerID):
    win.fill((255, 255, 255))
    if mode == "setup":
        Drawing_funcs.draw_setup_screen(shipsGrid, readybtn)
    elif mode == "setup_wait":
        Drawing_funcs.draw_setup_wait(shipsGrid)
    elif mode == "play":
        Drawing_funcs.draw_your_screen(shipsGrid)
    elif mode == "fire":
        if int(game.winnerP) == -1:
            if str(game.turn) == str(playerID):
                Drawing_funcs.draw_fire_screen(fireGrid, firebtn)
            else:
                Drawing_funcs.draw_wait_screen(fireGrid)
        else:
            if playerID == int(game.winnerP):
                text = "You Win!"
            else:
                text = "You Lost..."
            Drawing_funcs.draw_end_screen(fireGrid, text, rematchbtn)
    elif mode == "end_wait":
        text = "Waiting for Opponent..."
        Drawing_funcs.draw_end_screen(fireGrid, text, rematchbtn)
        rematchbtn.change_text("waiting")

    pygame.display.update()


def updates(game, playerID, fireGrid, shipsGrid, n, rematchbtn):
    global mode
    if playerID == 0:
        fireGrid.other_ships = game.all_ships2
        fireGrid.other_az = game.azs2
    else:
        fireGrid.other_ships = game.all_ships1
        fireGrid.other_az = game.azs1

    if playerID == 0:
        shipsGrid.shots = game.shots2
    else:
        shipsGrid.shots = game.shots1

    if game.both_reset():
        rematchbtn.change_text("Rematch?")
        shipsGrid.reset()
        fireGrid.reset()
        n.send("new")
        mode = "setup"


def main():
    global mode
    network = Network()
    playerID = int(network.getP())

    shipGrid = ShipsGrid(colors)
    fireGrid = FireGrid(colors)

    readybtn = Button(225, 700, colors, "Ready!")
    firebtn = Button(225, 700, colors, "Fire!")
    rematchbtn = Button(225, 700, colors, "Rematch?")

    clock = pygame.time.Clock()
    moving = False
    run = True
    while run:
        clock.tick(20)
        try:
            game = network.send("get")
        except:
            run = False
            print("Couldn't get game")
            break

        if game.both_ready() and mode == "setup_wait":
            for s in shipGrid.all_ships:
                text = str(s)
                network.send(text)
            network.send("ship")

            for a in shipGrid.around_zones:
                text = str(a)
                network.send(text)
            network.send("az")

            mode = "play"

        if mode != "setup" and mode != "setup_wait":
            updates(game, playerID, fireGrid, shipGrid, network, rematchbtn)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_down_pos = pygame.mouse.get_pos()
                if mode == "setup":
                    moving_ship = Mouse_Movements.setup_clicking(mouse_down_pos, shipGrid, readybtn, network, playerID)
                    if moving_ship:
                        moving = True
                elif mode == "fire":
                    if game.winnerP == -1:
                        Mouse_Movements.fire_spot(mouse_down_pos, fireGrid, firebtn, network)
                    else:
                        Mouse_Movements.restart_game(mouse_down_pos, rematchbtn, network)

            if event.type == pygame.MOUSEMOTION:
                mouse_moving = pygame.mouse.get_pos()
                if moving:
                    Mouse_Movements.setup_moving(shipGrid, mouse_moving, moving_ship)

            if event.type == pygame.MOUSEBUTTONUP:
                mouse_up_pos = pygame.mouse.get_pos()
                if moving:
                    Mouse_Movements.setup_end(shipGrid, mouse_up_pos, moving_ship)
                    moving = False

            if event.type == pygame.KEYDOWN:
                if mode == "setup":
                    if event.key == pygame.K_SPACE:
                        mouse_pos = pygame.mouse.get_pos()
                        Mouse_Movements.setup_rotate(shipGrid, mouse_pos)
                elif mode == "play":
                    if event.key == pygame.K_RIGHT:
                        mode = "fire"
                elif mode == "fire":
                    if event.key == pygame.K_LEFT:
                        mode = "play"

        drawWin(shipGrid, fireGrid, readybtn, firebtn, rematchbtn, game, playerID)


def menu_screen():
    run = True
    clock = pygame.time.Clock()

    while run:
        clock.tick(24)
        win.fill(colors[0])
        tfont = pygame.font.SysFont("Arial", 80)
        title = tfont.render("Battleship", 1, colors[1])
        win.blit(title, (100, 200))
        text = font.render("Click to Play!", 1, colors[4])
        win.blit(text, (200, 400))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:  # if they disconnect and click
                run = False

    main()  # they can reconnect


while True:
    menu_screen()
