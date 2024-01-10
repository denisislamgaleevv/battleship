import socket
import threading

class BattleshipServer:
    def __init__(self):

        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(('192.168.0.167', 5555))
        self.server_socket.listen(2)  # Принимаем до двух клиентов

        self.players = []
        self.player_ship_placements = {}

        self.start_ship_placement_event = threading.Event()
    def handle_client(self, client_socket, player_id):
        while True:
            self.start_ship_placement_event.wait()  # Ждем события начала расстановки кораблей
            data = client_socket.recv(1024)  # Принимаем данные от клиента
            if not data:
                # Обработка случая, когда данные не были получены
                print("Ошибка: Данные не были получены")
            else:
                # Обработка полученных данных
                print("Получены данные от клиента:", data)
            # ship_placement = self.process_ship_placement_data(data)  # Обработка данных о расстановке кораблей
            # self.player_ship_placements[player_id] = ship_placement

        client_socket.close()

    def send_start_ship_placement(self, client_socket):
        self.start_ship_placement_event.wait()  # Ждем сигнала о начале расстановки кораблей
        client_socket.sendall("START_SHIP_PLACEMENT".encode())  # Отправка сообщения о начале расстановки кораблей

    def handle_players_after_start(self):
        for player_id, (client_socket, addr) in enumerate(self.players, 1):
            print(f"Обработка игрока {player_id}: {addr}")
            data = client_socket.recv(1024)  # Принимаем данные от клиента
            if not data:
                # Обработка случая, когда данные не были получены
                print("Ошибка: Данные не были получены")
            else:
                # Обработка полученных данных
                print("Получены данные от клиента:", data)
            # ship_placement = self.process_ship_placement_data(data)  # Обработка данных о расстановке кораблей
            # self.player_ship_placements[player_id] = ship_placement

            client_socket.close()
    def start(self):
        print("Сервер запущен и ожидает подключений...")
        while len(self.players) < 2:
            client_socket, addr = self.server_socket.accept()
            print(f"Подключился игрок {len(self.players) + 1}: {addr}")
            self.players.append((client_socket, addr))

            if len(self.players) == 2:
                self.start_ship_placement_event.set()  # Устанавливаем сигнал о начале расстановки кораблей
                self.handle_players_after_start()  # Обработка взаимодействия с игроками после начала расстановки кораблей

            client_handler = threading.Thread(target=self.handle_client, args=(client_socket, len(self.players)))
            client_handler.start()

if __name__ == "__main__":
    server = BattleshipServer()
    server.start()