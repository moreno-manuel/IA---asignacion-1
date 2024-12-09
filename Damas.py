import pygame
import copy



# evalua el estado del tablero
def evaluate_board(matrix):
    human_score = 0
    ai_score = 0
    for row in matrix:
        for cell in row:
            if cell == "H" or cell == "HH":
                human_score += 1
            elif cell == "IA":
                ai_score += 1
    return ai_score - human_score


# posibles movimientos de un jugador
def get_all_moves(matrix, player):
    moves = []
    for row in range(4):
        for col in range(4):
            if matrix[row][col] == player:
                possible_moves = get_possible_moves(matrix, row, col)
                for move in possible_moves:
                    moves.append((row, col, move[0], move[1]))
    return moves


# posibles movimientos de un jugador
def get_possible_moves(matrix, row, col):
    moves = []
    directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
    for dr, dc in directions:
        new_row, new_col = row + dr, col + dc
        if 0 <= new_row < 4 and 0 <= new_col < 4 and matrix[new_row][new_col] == "N":
            moves.append((new_row, new_col))
        elif 0 <= new_row < 4 and 0 <= new_col < 4 and matrix[new_row][new_col] != matrix[row][col]:
            jump_row, jump_col = new_row + dr, new_col + dc
            if 0 <= jump_row < 4 and 0 <= jump_col < 4 and matrix[jump_row][jump_col] == "N":
                moves.append((jump_row, jump_col))
    return moves


# MiniMax poda Alfa-beta
def minimax(matrix, depth, alpha, beta, maximizing_player):
    if depth == 0 or game_over(matrix):
        return evaluate_board(matrix), None
    #maximizador
    if maximizing_player:
        max_eval = float('-inf')
        best_move = None
        for move in get_all_moves(matrix, "IA"):
            new_matrix = make_move(copy.deepcopy(matrix), move)
            eval, _ = minimax(new_matrix, depth - 1, alpha, beta, False)
            if eval > max_eval:
                max_eval = eval
                best_move = move
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval, best_move
    #minimizador
    else:
        min_eval = float('inf')
        best_move = None
        for move in get_all_moves(matrix, "H"):
            new_matrix = make_move(copy.deepcopy(matrix), move)
            eval, _ = minimax(new_matrix, depth - 1, alpha, beta, True)
            if eval < min_eval:
                min_eval = eval
                best_move = move
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval, best_move


# movimiento de fichas
def make_move(matrix, move):
    start_row, start_col, end_row, end_col = move
    matrix[end_row][end_col] = matrix[start_row][start_col]
    matrix[start_row][start_col] = "N"
    if abs(start_row - end_row) == 2:  # si come alguna ficha
        mid_row, mid_col = (start_row + end_row) // 2, (start_col + end_col) // 2
        matrix[mid_row][mid_col] = "N"
    if abs(start_row - end_row) == 3: #mueve tres espacios si es reina
        if((start_row == 0 and start_col == 0) or (start_row == 3 and start_col == 3)): #diagonal principal
            for position in range(2):
                if matrix[position][position] == "IA":
                    matrix[position][position] = "N"
        matrix[end_row][end_col] = matrix[start_row][start_col]
        matrix[start_row][start_col] = "N"
    return matrix


# comprueba si el juego termino y determina el ganador
def game_over(matrix):
    if len(get_all_moves(matrix, "H")) == 0:
        if len(get_all_moves(matrix, "HH")) == 0:
            return "IA"
    if len(get_all_moves(matrix, "IA")) == 0:
        return "H"


#crea los botones
def createButton(frame,button,name):
    if button.collidepoint(pygame.mouse.get_pos()): # si el foco esta en el boton el color es azul
        pygame.draw.rect(frame,"blue",button,0)
    else:
        pygame.draw.rect(frame,"black",button,0)
    
    text = font.render(name,True,"white") 
    screen.blit(text,(button.x + (button.width - text.get_width())/2, #posicion del 
                      button.y + (button.height - text.get_height())/2)) # texto


# valida los movimientos
def move_validate(matrix,row_select,col_select, new_row , new_col):
    if matrix[new_row][new_col] == "N":
        if abs(row_select - new_row) == 1 and abs(col_select - new_col) == 1:#si recorre un espacio
            return True
        elif abs(row_select - new_row) == 2 and abs(col_select - new_col) == 2:#si recorre dos espacios
            mid_row, mid_col = (row_select + new_row) // 2, (col_select + new_col) // 2
            if( matrix[mid_row][mid_col] == "IA"):
                return True
        elif abs(row_select - new_row) == 3 and abs(col_select - new_col) == 3:#si recorre tres espacios <solo reinas> HH
            if(matrix[row_select][col_select] == "HH"):
                return True


# el juego comienza
def createMatrix():
    #tablero
    matrix = [
        ["IA", " ", "IA", " "],
        [" ", "N", " ", "N"],
        ["N", " ", "N", " "],
        [" ","H", " ", "H"]
    ]
    
    #tamaño de celdas del tablero
    cellSize = 400 // 4

    piece_select = None
    running = True

    playing = 0

    message = None

    while running:
        screen.fill("gray")

        #dibuja el tablero
        for row in range(4):
            for col in range(4):
                color = "black " if (row + col) % 2 == 0 else "white" 
                pygame.draw.rect(screen, color, (col * cellSize, row * cellSize, cellSize, cellSize))
    
                piece = matrix [row][col]

                #dibuja piezas del humano
                if piece == "IA":
                    pygame.draw.circle(screen, "red" ,(col * cellSize + cellSize // 2, row * cellSize + cellSize // 2), 
                                   cellSize // 2 - 5)
                
                #dibuja piezas de la ia
                elif piece == "H" or piece =="HH": 
                    pygame.draw.circle(screen, "white" ,(col * cellSize + cellSize // 2, row * cellSize + cellSize // 2), 
                                   cellSize // 2 - 5)

        # marca la pieza seleccionada con un circulo verde
        if piece_select: 
            row, col = piece_select
            pygame.draw.circle(screen, "green" ,(col * cellSize + cellSize // 2, row * cellSize + cellSize // 2), 
                                cellSize // 2 - 5,3)
        
        
        pygame.display.flip() #actualiza la pantalla

        #eventos discretos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            #captura la posicion de la ficha seleccionada
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_x, mouse_y = event.pos
                col = mouse_x // cellSize
                row = mouse_y // cellSize

                if (matrix[row][col] == "H" or matrix[row][col] == "HH") and not piece_select:
                    piece_select = (row, col)
                elif piece_select:
                    row_select, col_select = piece_select
                   
                    #posibles movimientos Humano
                    if move_validate(matrix, row_select, col_select, row, col):
                        matrix = make_move(matrix, (row_select, col_select, row, col))
                        if(row == 0):
                            matrix[row][col] = "HH"
                        piece_select = None

                        # turno de la ia
                        _, ai_move = minimax(matrix, 3, float('-inf'), float('inf'), True)
                        if ai_move:
                            matrix = make_move(matrix, ai_move)
                        
                        playing = playing+2 # numero de movimientos

        if playing == 64:
            message = "Empate"
            player = None
            running = False
            
        if game_over(matrix) == "IA":
            message = "Gana IA"
            player = "IA"
            running = False
        
        if game_over(matrix) == "H":
            message = "Gana Humano"
            player = "H"
            running = False
        
    return message,player


#mensaje final del juego
def dialog(message,player):
    screen.fill("white")
    label = font2.render(message, True, "black")
    if player == "H":
        screen.blit(label, (110, 140))
    if player == "IA":
        screen.blit(label, (140, 140))
    else:
        screen.blit(label, (150, 140))



if __name__ == "__main__":
    
    #configuracion de interfaz
    pygame.init()
    screen = pygame.display.set_mode((400, 400))
    pygame.display.set_caption("Damas con Minimax")
    clock = pygame.time.Clock()
    
    #fuentes para label
    font = pygame.font.SysFont("arial", 20)
    font2 = pygame.font.SysFont("arial", 35)

    #rectangulos para botones
    init = pygame.Rect(50, 240, 100, 40)
    quit = pygame.Rect(250, 240, 100, 40)

    play = False
    running = True

    message = None

    while running:
        
        #eventos discretos
        for event in pygame.event.get():
            #click en quit del frame
            if event.type == pygame.QUIT:
                running = False
            #click en salir
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if quit.collidepoint(pygame.mouse.get_pos()):
                    if not play:
                        running = False
                #click en iniciar
                if init.collidepoint(pygame.mouse.get_pos()):
                    play = True
        
        if message != None:
            dialog(message,player)
            quit = pygame.Rect(150, 240, 100, 40)
            createButton(screen, quit, "Salir")
            play = False
        #inicio del juego
        elif play:
            message , player = createMatrix()
            if message == None:
                running = False
        #menu 
        else:
            screen.fill("white")
            label = font2.render("Juego de Damas", True, "black")
            label2 = font.render("Humano VS IA (Minimax)", True, "black")
            screen.blit(label, (90, 72))
            screen.blit(label2, (120, 114))
            createButton(screen, init, "Iniciar")
            createButton(screen, quit, "Salir")

        pygame.display.flip()#atualiza pantalla
        clock.tick(60)#60 fps

    pygame.quit()








