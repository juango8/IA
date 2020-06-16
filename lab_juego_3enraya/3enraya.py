# from lab_juego_3enraya.tictactoe import GeneralVariables
#
#
# class Node:
#     children = []
#     score = 0
#
#     def __init__(self, jugada, isMaxLvl):
#         self.jugada = jugada
#         self.isMaxLvl = isMaxLvl
#
#     def addChild(self, child):
#         self.children.append(child)
#
#
# class Tree:
#     def __init__(self, root):
#         self.root = root
#
#
# def numberSpaces(jugada):
#     count = 0
#     for i in jugada:
#         if i == ' ':
#             count += 1
#     return count
#
#
# def possiblePlays(jugada, turn):
#     plays = []
#     for i in range(len(jugada)):
#         temp = jugada
#         if jugada[i] == ' ':
#             if turn:
#                 temp = temp[:i] + '1' + temp[i + 1:]
#             else:
#                 temp = temp[:i] + '2' + temp[i + 1:]
#             plays.append(temp)
#     return plays
#
#
# def utilityFunction(jugada):
#     CountA = 9
#     CountB = 9
#     for i in range(len(jugada)):
#         if jugada[i] == '1':
#             for fila in GeneralVariables.WinnerCombinations:
#                 for j in range(3):
#                     if i == fila[j]:
#                         CountA -= 1
#         elif jugada[i] == '2':
#             for fila in GeneralVariables.WinnerCombinations:
#                 for j in range(3):
#                     if i == fila[j]:
#                         CountB -= 1
#     return CountA - CountB
#
#     #     if jugada[fila[0]] == " ":
#     #         continue
#     #     if len(set(jugada[casilla] for casilla in fila)) == 1:
#     #         # print(tablero[fila[0]])
#     #         return jugada[fila[0]]
#     # return 0
#
#
# class Minimax:
#     lvl = 0
#
#     def constructTree(self, *args):
#         if len(args) == 2 and isinstance(args[0], str):
#             root = Node(args[0], True)
#             self.tree = Tree(root)
#             self.lvl = args[1]
#             self.constructTree(root)
#         elif len(args) == 1 and isinstance(args[0], Node):
#             isChildMaxLvl = not args[0].isMaxLvl
#             possibleplays = possiblePlays(args[0].jugada, isChildMaxLvl)
#             self.lvl -= 1
#             for i in range(len(possibleplays)):
#                 newNode = Node(possibleplays[i], isChildMaxLvl)
#                 if self.lvl >= 0 and numberSpaces(newNode.jugada) > 0:
#                     self.constructTree(newNode)
#                 # newNode.addChild(newNode)
#                 args[0].addChild(newNode)
#
#     def checkWin(self, *args):
#         if len(args) == 0:
#             root = self.tree.root
#             self.checkWin(root)
#             return root.score == 1
#         elif len(args) == 1 and isinstance(args[0], Node):
#             children = args[0].children
#             isMaxLvl = args[0].isMaxLvl
#             for i in children:
#                 if len(children) == 0:
#                     if isMaxLvl:
#                         i.score = utilityFunction(args[0].jugada)
#                     else:
#                         i.score = -utilityFunction(args[0].jugada)
#                 else:
#                     self.checkWin(i)
#             bestChild = children[0]
#             args[0].score(bestChild.score)
#
#
# def main():
#     x = Minimax()
#     x.constructTree(' 1 21 12 ', 3)
#     # x.checkWin()
#     # x = possiblePlays('  12  12 ')
#     print(x)
#
#

import pygame, time

# colores
from lab_juego_3enraya import tictactoe

blanco = (255, 255, 255)
rojo = (200, 0, 0)
rojo_tomate = (255, 51, 0)
verde = (0, 204, 0)
verde_lima = (0, 255, 0)
azul = (0, 51, 255)
azul_marino = (0, 0, 119)
gris = (150, 150, 150)
gris_claro = (204, 204, 204)

tema = 0  # numero 0-4
color_fondo1 = [blanco, rojo, verde, azul, gris][tema]
color_fondo2 = [gris_claro, rojo_tomate, verde_lima, azul_marino, gris_claro][tema]

# variables ventana
t_casilla = 200
t_letra = 128
resolucion = (t_casilla * 3, t_casilla * 3)
FPS = 30

pygame.init()
clock = pygame.time.Clock()

# imagenes
img = {"X": pygame.transform.smoothscale(pygame.image.load("x.png"), (t_letra, t_letra)),
       "O": pygame.transform.smoothscale(pygame.image.load("o.png"), (t_letra, t_letra))}

# variables juego
VACIO = " "
JUGADOR = "X"
MAQUINA = "O"
dificultad = 2
contador = ""
filas_ganadoras = ((0, 1, 2), (3, 4, 5), (6, 7, 8),
                   (0, 3, 6), (1, 4, 7), (2, 5, 8),
                   (0, 4, 8), (2, 4, 6))

# funciones juego
colisionan = lambda punto, pos, dimensiones: pos[0] <= punto[0] <= pos[0] + dimensiones[0] and pos[1] <= punto[1] <= \
                                             pos[1] + dimensiones[1]


def render_tablero(screen, tablero):
    """Renderiza el tablero y pinta el fondo con los colores del tema
    ARGUMENTOS:
        -screen. Superficie principal de pygame sobre la que se pinta todo (display).
        -tablero. String de longitud 9 que contiene los valores del tablero."""
    # pintar fondo
    a = False
    for i in range(0, t_casilla * 3, t_casilla):
        for j in range(0, t_casilla * 3, t_casilla):
            a = a == False
            if a:
                pygame.draw.rect(screen, color_fondo1, ((i, j), (t_casilla, t_casilla)))
            else:
                pygame.draw.rect(screen, color_fondo2, ((i, j), (t_casilla, t_casilla)))
    # poner Os y Xs
    for a in range(9):
        if tablero[a] == " ": continue
        screen.blit(img[tablero[a]],
                    (a % 3 * t_casilla + (t_casilla - t_letra) / 2, a // 3 * t_casilla + (t_casilla - t_letra) / 2))


def minimax(tablero, turno_player, profundidad=5):
    """Implementacion del algoritmo minimax a nuestro tres en raya.
    ARGUMENTOS:
        -tablero. String de longitud 9 que contiene los valores del tablero.
        -turno_player. Booleano que indica el turno, si es positivo significa que le toca al jugador humano.
        -profundidad. Valor numerico que limita el numero de veces que la funcion se llama a si misma (dificultad) y que incita a la maquina
                      a realizar los movimientos que impliquen alargar la partida lo maximo posible (intentando ganar siempre)."""
    if ganador(tablero) == MAQUINA:
        return (+10 - profundidad, None)  # gana pc
    elif ganador(tablero) == JUGADOR:
        return (-10 - profundidad, None)  # pierde pc
    elif VACIO not in tablero or profundidad < 1:
        return (0, None)  # empatan
    elif turno_player:  # turno de jugador
        best = (+11, None)
        for a in range(9):
            if tablero[a] == " ":
                valor = minimax(tablero[:a] + JUGADOR + tablero[a + 1:], not turno_player, profundidad - 1)[0]
                if valor < best[0]: best = (valor, a)  # jugador intenta causar el MENOR beneficio a pc
        return best
    else:  # turno de pc
        best = (-11, None)
        for a in range(9):
            if tablero[a] == " ":
                valor = minimax(tablero[:a] + MAQUINA + tablero[a + 1:], not turno_player, profundidad - 1)[0]
                if valor > best[0]: best = (valor, a)  # pc intenta causar el MAYOR beneficio a si mismo
        return best


def ganador(tablero):
    """Indica si alguien ha ganado la partida y en caso verdadero devuelve la letra del ganador.
    Como argumento toma unicamente el tablero como string de longitud 9."""
    for fila in filas_ganadoras:
        if tablero[fila[0]] == VACIO: continue
        if len(set(tablero[casilla] for casilla in fila)) == 1: return tablero[fila[0]]
    return False


def movimiento_pc(tablero):
    """Realiza el movimiento del pc en el tablero"""
    pygame.mouse.set_cursor(*pygame.cursors.broken_x)
    t0 = time.time()  # inicio cronometro
    if tablero[4] == VACIO:
        a = 4  # cuando el centro esta vacio siempre trata de ocuparlo
    elif dificultad < 1:
        a = set(i for i in range(9) if tablero[i] == VACIO).pop()  # uno aleatorio entre los movimientos validos
    elif dificultad >= 1:
        a = minimax(tablero, False, dificultad)[1]  # algoritmo minimax limitado segun la dificultad

    if a is not None: tablero = tablero[:a] + MAQUINA + tablero[
                                                        a + 1:]  # sustituye la posicion a en el tablero por su letra
    print("La maquina ha tardado {:.5f} ms".format((time.time() - t0) * 1000))  # tiempo desde inicio del cronometro
    pygame.mouse.set_cursor(*pygame.cursors.arrow)
    return tablero


screen = pygame.display.set_mode(resolucion)
pygame.display.set_caption("3 en raya")


def main():
    global contador
    # variables que se han de resetear al iniciar la partida
    turno_player = True
    tablero = VACIO * 9
    salir = False
    # dificultad = tictactoe.msg(screen, 'Indica el nivel de dificultad', 'Facil(0), Normal(1), Dificil(2)')
    while not salir:
        clock.tick(FPS)  # limitar los FPS para no consumir recursos innecesarios

        if not turno_player and not ganador(tablero) and VACIO in tablero:
            tablero = movimiento_pc(tablero)
            turno_player = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # click en la cruz roja
                raise SystemExit

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    raise SystemExit

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if ganador(
                        tablero) or not VACIO in tablero: salir = True  # Cuando la partida termina, se espera a clickar para reiniciarla
                    x = event.pos[0] // t_casilla + 3 * (event.pos[1] // t_casilla)
                    if tablero[x] == " ":
                        tablero = tablero[:x] + JUGADOR + tablero[x + 1:]
                        turno_player = False

        render_tablero(screen, tablero)
        pygame.display.flip()

    if ganador(tablero):
        contador = contador + ganador(tablero)
        print("\n" * 100)
        print(ganador(tablero), "ha ganado!    TOTAL: ", "X", str(contador.count("X")) + "-" + str(contador.count("O")),
              "O")
        print("\n")
        salir = True
    elif VACIO not in tablero:
        print("\n" * 100)
        print("EMPATE!!    TOTAL: ", "X", str(contador.count("X")) + "-" + str(contador.count("O")), "O")
        print("\n")
        salir = True


if __name__ == '__main__':
    main()