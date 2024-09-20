import tkinter as tk
from tkinter import messagebox
import time

# Algoritmo Minimax sin Alpha-Beta Pruning
def minimax(board, depth, is_maximizing, player, opponent):

    """
    Implementa el algoritmo Minimax para determinar la mejor jugada.
    
    :param board: Lista que representa el estado actual del tablero.
    :param depth: Profundidad actual en el árbol de búsqueda.
    :param is_maximizing: Booleano que indica si el jugador actual está maximizando su puntaje.
    :param player: Símbolo del jugador actual.
    :param opponent: Símbolo del oponente.
    :return: La puntuación de la mejor jugada posible.
    """

    winner = check_winner(board)
    if winner == player:
        return 10 - depth
    elif winner == opponent:
        return depth - 10
    elif is_board_full(board):
        return 0

    if is_maximizing:
        best_score = -float('inf')
        for i in range(9):
            if board[i] == '':
                board[i] = player
                score = minimax(board, depth + 1, False, player, opponent)
                board[i] = ''
                best_score = max(score, best_score)
        return best_score
    else:
        best_score = float('inf')
        for i in range(9):
            if board[i] == '':
                board[i] = opponent
                score = minimax(board, depth + 1, True, player, opponent)
                board[i] = ''
                best_score = min(score, best_score)
        return best_score

# Algoritmo Minimax con Alpha-Beta Pruning
def minimax_alpha_beta(board, depth, is_maximizing, player, opponent, alpha, beta):

    """
    Implementa el algoritmo Minimax con Alpha-Beta Pruning para mejorar la eficiencia de la búsqueda.
    
    :param board: Lista que representa el estado actual del tablero.
    :param depth: Profundidad actual en el árbol de búsqueda.
    :param is_maximizing: Booleano que indica si el jugador actual está maximizando su puntaje.
    :param player: Símbolo del jugador actual.
    :param opponent: Símbolo del oponente.
    :param alpha: El mejor valor encontrado hasta ahora para el jugador maximizador.
    :param beta: El mejor valor encontrado hasta ahora para el jugador minimizador.
    :return: La puntuación de la mejor jugada posible.
    """

    winner = check_winner(board)
    if winner == player:
        return 10 - depth
    elif winner == opponent:
        return depth - 10
    elif is_board_full(board):
        return 0

    if is_maximizing:
        best_score = -float('inf')
        for i in range(9):
            if board[i] == '':
                board[i] = player
                score = minimax_alpha_beta(board, depth + 1, False, player, opponent, alpha, beta)
                board[i] = ''
                best_score = max(score, best_score)
                alpha = max(alpha, score)
                if beta <= alpha:
                    break
        return best_score
    else:
        best_score = float('inf')
        for i in range(9):
            if board[i] == '':
                board[i] = opponent
                score = minimax_alpha_beta(board, depth + 1, True, player, opponent, alpha, beta)
                board[i] = ''
                best_score = min(score, best_score)
                beta = min(beta, score)
                if beta <= alpha:
                    break
        return best_score

# Verifica si hay un ganador
def check_winner(board):
    """
    Verifica si hay un ganador

    :param board: Lista que representa el estado actual del tablero.
    :return: El símbolo del ganador si hay uno, None si no hay ganador.
    """
    winning_combinations = [(0, 1, 2), (3, 4, 5), (6, 7, 8),
                            (0, 3, 6), (1, 4, 7), (2, 5, 8),
                            (0, 4, 8), (2, 4, 6)]
    for combo in winning_combinations:
        if board[combo[0]] == board[combo[1]] == board[combo[2]] and board[combo[0]] != '':
            return board[combo[0]]
    return None

# Verifica si el tablero está lleno
def is_board_full(board):

    """
    Verifica si el tablero está lleno

    :param board: Lista que representa el estado actual del tablero.
    :return: Booleano que indica si el tablero está lleno.
    """
    return '' not in board

# Escoge la mejor jugada
def best_move(board, player, opponent, use_alpha_beta):

    """
    Determina la mejor jugada para la IA utilizando Minimax o Minimax con Alpha-Beta Pruning.
    
    :param board: Lista que representa el estado actual del tablero.
    :param player: Símbolo del jugador actual.
    :param opponent: Símbolo del oponente.
    :param use_alpha_beta: Booleano que indica si se debe usar Alpha-Beta Pruning.
    :return: El índice de la mejor jugada en el tablero.
    """

    best_score = -float('inf')
    move = None
    for i in range(9):
        if board[i] == '':
            board[i] = player
            if use_alpha_beta:
                score = minimax_alpha_beta(board, 0, False, player, opponent, -float('inf'), float('inf'))
            else:
                score = minimax(board, 0, False, player, opponent)
            board[i] = ''
            if score > best_score:
                best_score = score
                move = i
    return move

# Inicia el juego
def start_game():

    """
    Inicia el juego

    Configura la interfaz gráfica del juego y maneja la lógica del juego.
    """

    root = tk.Tk()
    root.title("Tres en raya")
    root.geometry("300x400")
    root.resizable(False, False)

    board = [''] * 9
    algo_choice = tk.StringVar(value="minimax")
    
    start_time = 0  # Inicializamos start_time aquí

    # Reiniciar juego
    def reset_game():

        """
        Reinicia el estado del juego y muestra la selección inicial.
        """

        for button in buttons:
            button.config(text="", state=tk.NORMAL)
        start_selection()

    # Muestra el ganador
    def end_game(winner, algo_time):

        """
        Muestra el resultado del juego y el rendimiento del algoritmo.
        
        :param winner: El símbolo del ganador o None si es un empate.
        :param algo_time: Tiempo que tomó el algoritmo para calcular el movimiento.
        """

        for button in buttons:
            button.config(state=tk.DISABLED)
        if winner:
            message_label.config(text=f"Ganador: {winner}")
        else:
            message_label.config(text="Es un empate")
        algo_performance_label.config(text=f"Rendimiento del algoritmo: {algo_time:.4f} segundos")

    # Maneja los clics del usuario
    def handle_click(index):

        """
        Maneja el clic del usuario en un botón del tablero.
        
        :param index: Índice del botón en el tablero.
        """

        if board[index] == '':
            board[index] = player_choice.get()  # Se utiliza el símbolo seleccionado por el jugador
            buttons[index].config(text=player_choice.get(), state=tk.DISABLED)
            winner = check_winner(board)
            if winner or is_board_full(board):
                algo_time = time.time() - start_time
                end_game(winner, algo_time)
            else:
                ai_move()

    # Movimiento de la IA
    def ai_move():

        """
        Realiza el movimiento de la IA en el tablero.
        """

        nonlocal start_time  # Marcamos la variable como nonlocal
        player_symbol = player_choice.get()  # Se obtiene el símbolo del jugador
        opponent_symbol = 'O' if player_symbol == 'X' else 'X'  # La IA usa el símbolo contrario
        start_time = time.time()  # Inicia el contador de tiempo del algoritmo
        move = best_move(board, opponent_symbol, player_symbol, algo_choice.get() == "minimax_alpha_beta")
        if move is not None:
            board[move] = opponent_symbol
            buttons[move].config(text=opponent_symbol, state=tk.DISABLED)
            winner = check_winner(board)
            if winner or is_board_full(board):
                algo_time = time.time() - start_time
                end_game(winner, algo_time)

    # Selección de algoritmo y símbolo
    def start_selection():

        """
        Muestra el marco de selección de algoritmo y símbolo.
        """

        for button in buttons:
            button.config(state=tk.DISABLED)
        selection_frame.grid(row=6, column=0, columnspan=3)

    def begin_game():

        """
        Inicia el juego después de que el usuario haya hecho sus selecciones.
        """

        selection_frame.grid_forget()
        reset_board()
        for button in buttons:
            button.config(state=tk.NORMAL)

    def reset_board():

        """
        Reinicia el estado del tablero y los mensajes.
        """

        nonlocal board
        board = [''] * 9
        for button in buttons:
            button.config(text="", state=tk.NORMAL)
        message_label.config(text="")
        algo_performance_label.config(text="")

    player_choice = tk.StringVar(value="X")
    buttons = []
    for i in range(9):
        button = tk.Button(root, text="", width=10, height=3, command=lambda i=i: handle_click(i))
        button.grid(row=i//3, column=i%3)
        buttons.append(button)

    # Labels para mostrar mensajes
    message_label = tk.Label(root, text="")
    message_label.grid(row=3, columnspan=3)

    algo_performance_label = tk.Label(root, text="")
    algo_performance_label.grid(row=4, columnspan=3)

    # Sección de selección de algoritmo y símbolo
    selection_frame = tk.Frame(root)
    tk.Label(selection_frame, text="Escoge el algoritmo").grid(row=0, columnspan=2)
    tk.Radiobutton(selection_frame, text="Minimax", variable=algo_choice, value="minimax").grid(row=1, column=0)
    tk.Radiobutton(selection_frame, text="Minimax con Alpha-Beta Pruning", variable=algo_choice, value="minimax_alpha_beta").grid(row=1, column=1)

    tk.Label(selection_frame, text="Escoge tu símbolo").grid(row=2, columnspan=2)
    tk.Radiobutton(selection_frame, text="X", variable=player_choice, value="X").grid(row=3, column=0)
    tk.Radiobutton(selection_frame, text="O", variable=player_choice, value="O").grid(row=3, column=1)

    tk.Button(selection_frame, text="Iniciar Juego", command=begin_game).grid(row=4, columnspan=2)

    tk.Button(root, text="Reiniciar", command=reset_game).grid(row=5, columnspan=3)

    start_selection()
    root.mainloop()

start_game()
