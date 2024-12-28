import socket
import threading

class GameServer:
    def __init__(self, host='localhost', port=12345):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((host, port))
        self.server_socket.listen(5)
        print(f"Server started on {host}:{port}")
        self.clients = []

    def handle_client(self, client_socket):
        while True:
            try:
                message = client_socket.recv(1024).decode('utf-8')
                if not message:
                    break
                print(f"Received: {message}")
                response = self.process_message(message)
                client_socket.send(response.encode('utf-8'))
            except ConnectionResetError:
                break
        client_socket.close()

    def process_message(self, message):
        parts = message.split()
        if parts[0] == "MOVE":
            pion_id = int(parts[1])
            dx = int(parts[2])
            dy = int(parts[3])
            # Traitez le mouvement ici
            return f"Moved pion {pion_id} to ({dx}, {dy})"
        elif parts[0] == "BUILD":
            bx = int(parts[1])
            by = int(parts[2])
            # Traitez la construction ici
            return f"Built at ({bx}, {by})"
        return "Unknown command"

    def send_message_to_client(self, message):
        for client in self.clients:
            try:
                client.send(message.encode('utf-8'))
            except Exception as e:
                print(f"Error sending message to client: {e}")

    def start(self):
        while True:
            client_socket, addr = self.server_socket.accept()
            print(f"Connection from {addr}")
            self.clients.append(client_socket)
            client_handler = threading.Thread(target=self.handle_client, args=(client_socket,))
            client_handler.start()

if __name__ == "__main__":
    server = GameServer()
    server.start()
