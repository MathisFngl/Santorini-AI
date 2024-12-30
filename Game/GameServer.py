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
            client_socket.send(response.encode('utf-8'))

    def process_message(self, message):
        parts = message.split()
        if parts[0] == "MOVE":
            pion_id = int(parts[1])
            dx = int(parts[2])
            dy = int(parts[3])
            print("Moving pion_id: ", pion_id, "dx: ", dx, "dy: ", dy)
            return "MOVE processed"
        elif parts[0] == "BUILD":
            bx = int(parts[1])
            by = int(parts[2])
            print("Building in bx: ", bx, "by: ", by)
            return "BUILD processed"
        elif parts[0] == "START":
            mode = int(parts[1])
            if self.game:
                self.game.setMode(mode)
                print("Starting game in mode: ", mode)
            return "START processed"
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
