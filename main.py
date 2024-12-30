import threading
import socket
import time
from Game.GameHandler import Game
from Game.GameServer import GameServer

def start_server(game):
    server = GameServer()
    server.game = game
    server.start()

if __name__ == "__main__":
    # Demander à l'utilisateur s'il souhaite jouer en 3D
    online_play = input("Souhaitez-vous jouer avec le jeu 3D ? (oui/non) : ").strip().lower()

    if online_play == 'oui':
        # Démarrer le serveur dans un thread séparé
        server = GameServer()

        # Démarrer le jeu
        new_game = Game(skip_initialization=True, isServerActive=True, server=server)

        server.game = new_game
        server_thread = threading.Thread(target=server.start)
        server_thread.start()
        print("Starting server...")

        # Attendre que le serveur accepte une connexion
        print("Waiting for a client to connect...")
        server.connection_accepted.wait()  # Bloque jusqu'à ce qu'une connexion soit acceptée
        print("Client connected. Starting game with server support.")

        # Démarrer le jeu
        new_game.play()
    else:
        print("Starting game in console mode only.")
        new_game = Game()
