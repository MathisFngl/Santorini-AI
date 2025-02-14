import threading
import socket
import queue

class GameServer:
    def __init__(self, host='localhost', port=12345):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((host, port))
        self.server.listen(5)
        self.clients = []
        self.message_queue = queue.Queue()
        self.connection_accepted = threading.Event()  # Signal pour la connexion
        self.game = None
        self.waiting_for_confirmation = True  # Indicateur pour attendre la confirmation

    def handle_client(self, client_socket):
        self.connection_accepted.set()  # Déclencher le signal
        while True:
            try:
                message = client_socket.recv(1024).decode('utf-8')
                if not message:
                    break
                print(f"Received: {message}")
                self.message_queue.put((client_socket, message))
            except ConnectionResetError:
                break
        client_socket.close()

    def process_messages(self):
        while True:
            client_socket, message = self.message_queue.get()
            response = self.process_message(message)
            if response:
                client_socket.send(response.encode('utf-8'))

    def process_message(self, message):
        parts = message.split()
        if parts[0] == "MOVE":
            pion_id = 1 if parts[1] == "Perso1" else 2
            target_x = int(parts[2])
            target_y = int(parts[3])
            player = self.game.players[0]
            pion = player.pion1 if pion_id == 1 else player.pion2
            dx = target_x - pion.x
            dy = target_y - pion.y
            self.game.last_move_x = target_x  # Store the last move coordinates
            self.game.last_move_y = target_y
            self.game.moveDirection = (pion, dx, dy)
            print(f"Moved {pion_id} to ({target_x}, {target_y})")
            self.game.moveReceived = True
            return "MOVE processed"

        elif parts[0] == "BUILD":
            target_x = int(parts[1])
            target_y = int(parts[2])
            player = self.game.players[0]
            pion = player.pion1 if player.pion1.x == target_x and player.pion1.y == target_y else player.pion2
            bx = target_x - pion.x
            by = target_y - pion.y
            self.game.buildDirection = (bx, by)
            print(f"Built at ({target_x}, {target_y})")
            self.game.buildReceived = True
            return "BUILD processed"
        elif parts[0] == "START":
            mode = int(parts[1])
            if self.game:
                self.game.setMode(mode)
            return "START processed"
        elif parts[0] == "INIT":
            if parts[1] == "Player1":
                if parts[2] == "Perso1":
                    self.game.players[0].pion1.x = int(parts[3])
                    self.game.players[0].pion1.y = int(parts[4])
                elif parts[2] == "Perso2":
                    self.game.players[0].pion2.x = int(parts[3])
                    self.game.players[0].pion2.y = int(parts[4])
            elif parts[1] == "Player2":
                if parts[2] == "Perso1":
                    self.game.players[1].pion1.x = int(parts[3])
                    self.game.players[1].pion1.y = int(parts[4])
                elif parts[2] == "Perso2":
                    self.game.players[1].pion2.x = int(parts[3])
                    self.game.players[1].pion2.y = int(parts[4])
            print("INIT processed")
            self.waiting_for_confirmation = True
            return "INIT processed"
        elif parts[0] == "CONFIRM":
            self.waiting_for_confirmation = False
            print(f"Confirmation received for {parts[1]} {parts[2]}")
            return None  # Pas de réponse nécessaire pour la confirmation
        return "Unknown command"

    def start(self):
        print("Server started")
        threading.Thread(target=self.process_messages, daemon=True).start()
        while True:
            client_socket, addr = self.server.accept()
            print(f"Accepted connection from {addr}")
            self.clients.append(client_socket)
            client_handler = threading.Thread(target=self.handle_client, args=(client_socket,))
            client_handler.start()

    def sendMessageToServer(self, message):
        if self.clients:
            client_socket = self.clients[0]
            client_socket.send(message.encode('utf-8'))
            print(f"Sent: {message}")
            # Attendre la confirmation avant d'envoyer le message suivant
            #while self.waiting_for_confirmation:
                #pass

