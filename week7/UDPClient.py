from socket import *

# Tentukan nama host (atau IP) dan nomor port server
serverName = 'localhost' # Ubah 'hostname' menjadi 'localhost' jika jalan di komputer yang sama
serverPort = 12000

# Membuat soket klien untuk UDP (SOCK_DGRAM)
clientSocket = socket(AF_INET, SOCK_DGRAM)

# Meminta input dari pengguna
message = input('Input lowercase sentence: ')

# Mengirim pesan (dalam bentuk byte) beserta alamat tujuan ke soket
clientSocket.sendto(message.encode(), (serverName, serverPort))

# Menerima balasan dari server
modifiedMessage, serverAddress = clientSocket.recvfrom(2048)

# Menampilkan pesan yang sudah dimodifikasi (kapital) dari server
print(modifiedMessage.decode())

# Menutup soket
clientSocket.close()