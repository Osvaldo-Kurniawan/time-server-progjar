import socket
import threading
import datetime
import pytz

# Kelas yang menangani setiap koneksi klien secara terpisah
class ProcessTheClient(threading.Thread):
    def __init__(self, connection, address):
        self.connection = connection
        self.address = address
        threading.Thread.__init__(self)

    def run(self):
        # Menampilkan informasi koneksi klien yang diterima
        print(f"Connection from {self.address}")
        while True:
            # Menerima data dari klien
            data = self.connection.recv(1024).decode('utf-8').strip()
            if not data:
                break
            # Menampilkan data yang diterima dari klien
            print(f"Received data: '{data}'")
            if data == "TIME1310":
                # Mengirim respon berupa waktu saat ini jika permintaan adalah 'TIME1310'
                current_time = datetime.datetime.now(pytz.timezone('Asia/Jakarta')).strftime("%H:%M:%S")
                response = f"JAM {current_time} 1310\r\n"
                self.connection.sendall(response.encode('utf-8'))
            elif data == "QUIT1310":
                # Mengirim pesan penutup jika permintaan adalah 'QUIT1310'
                self.connection.sendall("Closing connection...\r\n".encode('utf-8'))
                break
            else:
                # Mengirim pesan kesalahan jika permintaan tidak valid
                self.connection.sendall("Invalid command\r\n".encode('utf-8'))
        # Menutup koneksi dengan klien setelah selesai
        self.connection.close()
        print(f"Connection from {self.address} closed")

# Kelas untuk menjalankan server
class Server(threading.Thread):
    def __init__(self):
        self.the_clients = []
        self.my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        threading.Thread.__init__(self)

    def run(self):
        # Mengikat socket pada alamat tertentu dan mulai mendengarkan koneksi masuk
        self.my_socket.bind(('0.0.0.0', 45000))
        self.my_socket.listen(5)
        print("Server is listening...")
        while True:
            # Menerima koneksi masuk
            connection, client_address = self.my_socket.accept()
            # Membuat instance ProcessTheClient untuk menangani koneksi
            clt = ProcessTheClient(connection, client_address)
            clt.start()
            # Menambahkan instance ke daftar klien aktif
            self.the_clients.append(clt)

def main():
    svr = Server()
    svr.start()

if __name__ == "__main__":
    main()
