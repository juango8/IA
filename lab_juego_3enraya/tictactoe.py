import pygame


class GeneralVariables:
    dif = None
    BackgroundColor1 = (201, 217, 251)  # celeste
    BackgroundColor2 = (209, 165, 230)  # (205,193,207) #morado
    casilla = 200
    letra = 128
    img = {"1": pygame.transform.smoothscale(pygame.image.load("x.png"), (letra, letra)),
           "2": pygame.transform.smoothscale(pygame.image.load("o.png"), (letra, letra))}
    turn = False
    WinnerCombinations = ((0, 1, 2), (3, 4, 5), (6, 7, 8),
                          (0, 3, 6), (1, 4, 7), (2, 5, 8),
                          (0, 4, 8), (2, 4, 6))


class Node:
    children = []
    score = 0

    def __init__(self, jugada, isMaxLvl):
        self.jugada = jugada
        self.isMaxLvl = isMaxLvl

    def addChild(self, child):
        self.children.append(child)


class Tree:
    def __init__(self, root):
        self.root = root


def numberSpaces(jugada):
    count = 0
    for i in jugada:
        if i == ' ':
            count += 1
    return count


def possiblePlays(jugada, turn):
    plays = []
    for i in range(len(jugada)):
        temp = jugada
        if jugada[i] == ' ':
            if turn:
                temp = temp[:i] + '1' + temp[i + 1:]
            else:
                temp = temp[:i] + '2' + temp[i + 1:]
            plays.append(temp)
    return plays


class Minimax:
    lvl = 0

    def constructTree(self, *args):
        if len(args) == 2 and isinstance(args[0], str):
            root = Node(args[0], True)
            self.tree = Tree(root)
            a = root
            self.lvl = args[1]
            self.constructTree(a)
        elif len(args) == 1 and isinstance(args[0], Node):
            isChildMaxLvl = not args[0].isMaxLvl
            possibleplays = possiblePlays(args[0].jugada, isChildMaxLvl)
            self.lvl -= 1
            for i in range(len(possibleplays)):
                newNode = Node(possibleplays[i], isChildMaxLvl)
                args[0].addChild(newNode)
                if numberSpaces(newNode.jugada) > 0 or self.lvl <= 0:
                    a = newNode
                    self.constructTree(a)

    def checkWin(self, *args):
        if len(args) == 0:
            root = self.tree.root
            self.checkWin(root)
            return root.score == 1
        elif len(args) == 1 and isinstance(args[0], Node):
            children = args[0].children
            isMaxLvl = args[0].isMaxLvl
            for i in children:
                if len(children) == 0:
                    if isMaxLvl:
                        i.score = 1
                    else:
                        i.score = -1
                else:
                    self.checkWin(i)
            # bestChild = findBestChild(isMaxLvl, children)
            # args[0].score(bestChild.score)

    # def findBestChild(self, isMaxLvl, children):


# private Node findBestChild(boolean isMaxPlayer, List<Node> children) {
#     Comparator<Node> byScoreComparator = Comparator.comparing(Node::getScore);
#     return children.stream()
#       .max(isMaxPlayer ? byScoreComparator : byScoreComparator.reversed())
#       .orElseThrow(NoSuchElementException::new);
# }

# def constructTree(self, parentNode,jugada = ''):
#     root = Node(jugada, True)
#     self.tree = Tree(root)
#     self.constructTree()
#     possibleplays = []
#     isChildMaxLvl =


def display(screen):
    b = 0
    begin_casilla = int(GeneralVariables.casilla / 2)
    for i in range(begin_casilla, GeneralVariables.casilla * 3, GeneralVariables.casilla):
        for j in range(begin_casilla, GeneralVariables.casilla * 3, GeneralVariables.casilla):
            if b % 2:
                pygame.draw.rect(screen,
                                 GeneralVariables.BackgroundColor1,
                                 ((i, j), (GeneralVariables.casilla, GeneralVariables.casilla)))
            else:
                pygame.draw.rect(screen,
                                 GeneralVariables.BackgroundColor2,
                                 ((i, j), (GeneralVariables.casilla, GeneralVariables.casilla)))
            b = b + 1
    pygame.display.flip()


def msg(screen, GameText1, GameText2):
    pygame.draw.rect(screen, (255, 255, 255), ((120, 270), (560, 210)))

    font = pygame.font.Font('freesansbold.ttf', 32)
    text1 = font.render(GameText1, True, (109, 143, 191))
    text2 = font.render(GameText2, True, (109, 143, 191))
    text3 = font.render("Llene en la terminal", True, (109, 143, 191))
    textRect1 = text1.get_rect()
    textRect2 = text2.get_rect()
    textRect3 = text3.get_rect()
    textRect1.center = (400, 350)
    textRect2.center = (400, 400)
    textRect3.center = (400, 450)
    screen.blit(text1, textRect1)
    screen.blit(text2, textRect2)
    screen.blit(text3, textRect3)
    pygame.display.update()
    result = input("Introduzca su respuesta: ")
    return int(result)


def update(tablero, screen):
    for a in range(9):
        if tablero[a] == " ":
            continue
        screen.blit(GeneralVariables.img[tablero[a]],
                    (a % 3 * GeneralVariables.casilla + 100 + (GeneralVariables.casilla - GeneralVariables.letra) / 2,
                     a // 3 * GeneralVariables.casilla + 100 + (GeneralVariables.casilla - GeneralVariables.letra) / 2))
        pygame.display.update()


def GameLogic(tablero, ini, dif):
    coincidence = False
    for i in range(len(tablero)):
        coincidence = (coincidence or tablero[i] == ' ')
    while not bool(isWinner(tablero)) and coincidence:
        if ini:
            # jugador
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        x = (event.pos[0] - 100) // GeneralVariables.casilla + \
                            3 * ((event.pos[1] - 100) // GeneralVariables.casilla)
                        if tablero[x] == " ":
                            tablero = tablero[:x] + '1' + tablero[x + 1:]
                            GeneralVariables.turn = False
        else:
            if GeneralVariables.dif < 1:
                tablero = set(i for i in range(9) if tablero[i] == ' ').pop()
            elif GeneralVariables.dif >= 1:
                tablero = miniMax(tablero, GeneralVariables.turn, GeneralVariables.dif)
            GeneralVariables.turn = True
            # computadora
            # for event in pygame.event.get():
            #     if event.type == pygame.MOUSEBUTTONDOWN:
            #         if event.button == 1:
            #             x = (event.pos[0] - 100) // GeneralVariables.casilla + 3 * (
            #                     (event.pos[1] - 100) // GeneralVariables.casilla)
            #             if tablero[x] == " ":
            #                 tablero = tablero[:x] + '2' + tablero[x + 1:]
            #                 GeneralVariables.turn = True
        return tablero
    return tablero + "E"


def isWinner(tablero):
    for fila in GeneralVariables.WinnerCombinations:
        if tablero[fila[0]] == " ":
            continue
        if len(set(tablero[casilla] for casilla in fila)) == 1:
            # print(tablero[fila[0]])
            return tablero[fila[0]]
    return 0


def miniMax(tablero, turn, dif):
    if isWinner(tablero) == '2':
        return +10 - dif, None
    elif isWinner(tablero) == '1':
        return -10 - dif, None
    elif ' ' not in tablero or dif < 1:
        return 0, None
    elif turn:
        best = (+11, None)
        for a in range(9):
            if tablero[a] == " ":
                valor = miniMax(tablero[:a] + '1' + tablero[a + 1:], not turn, dif - 1)[0]
                if valor < best[0]: best = (valor, a)  # jugador intenta causar el MENOR beneficio a pc
        return best
    else:  # turno de pc
        best = (-11, None)
        for a in range(9):
            if tablero[a] == " ":
                valor = miniMax(tablero[:a] + '2' + tablero[a + 1:], not turn, dif - 1)[0]
                if valor > best[0]: best = (valor, a)  # pc intenta causar el MAYOR beneficio a si mismo
        return best

    return tablero


def GUI():
    pygame.init()
    screen = pygame.display.set_mode((800, 800))
    pygame.display.set_caption('Tic Tak Toe')
    screen.fill((109, 143, 191))  # ((95,155,160)) #((255, 255, 255))
    GeneralVariables.dif = msg(screen, 'Indica el nivel de dificultad', 'Facil(0), Normal(1), Dificil(2)')
    GeneralVariables.turn = bool(msg(screen, 'Quien va a empezar', 'Computadora(0), Tu(1)'))
    display(screen)
    tablero = " " * 9
    while True and len(tablero) == 9:
        tablero = GameLogic(tablero, GeneralVariables.turn, GeneralVariables.dif)
        update(tablero, screen)
    x = isWinner(tablero[:-1])
    if x == "1":
        print("\nGano X")
    elif x == "2":
        print("\nGano O")
    else:
        print("\nEmpate")
    return


if __name__ == '__main__':
    GUI()
