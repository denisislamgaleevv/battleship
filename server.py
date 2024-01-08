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
        # Логика для обработки сообщений от клиента
        # ...

        while True:
            data = client_socket.recv(1024)  # Принимаем данные от клиента
            if not data:
                break
            ship_placement = self.process_ship_placement_data(data)  # Обработка данных о расстановке кораблей
            self.player_ship_placements[player_id] = ship_placement
            # Дополнительная логика для обработки ходов игроков и отправки информации о состоянии игры
            # Отправка информации о состоянии игры обоим игрокам
            client_socket.sendall(self.get_game_state().encode())

        client_socket.close()

    def send_start_ship_placement(self, client_socket):
        self.start_ship_placement_event.wait()  # Ждем сигнала о начале расстановки кораблей
        client_socket.sendall("START_SHIP_PLACEMENT".encode())  # Отправка сообщения о начале расстановки кораблей

    def start(self):
        print("Сервер запущен и ожидает подключений...")
        while len(self.players) < 2:
            client_socket, addr = self.server_socket.accept()
            print(f"Подключился игрок {len(self.players) + 1}: {addr}")
            self.players.append((client_socket, addr))

            if len(self.players) == 2:
                print('зашли')
                self.start_ship_placement_event.set()  # Устанавливаем сигнал о начале расстановки кораблей
                for player in self.players:
                    print('отправили', (player[0],))
                    threading.Thread(target=self.send_start_ship_placement, args=(player[0],)).start()

            client_handler = threading.Thread(target=self.handle_client, args=(client_socket, len(self.players)))
            client_handler.start()

if __name__ == "__main__":
    server = BattleshipServer()
    server.start()