from socket import *

# Tentukan nama host (atau IP) dan nomor port server
serverName = 'localhost' # Ubah 'hostname' menjadi 'localhost' jika jalan di komputer yang sama
serverPort = 12000

# Membuat soket klien untuk TCP (SOCK_STREAM)
clientSocket = socket(AF_INET, SOCK_STREAM)

# Melakukan koneksi ke server
clientSocket.connect((serverName, serverPort))

# Meminta input dari pengguna
sentence = input('Input lowercase sentence: ')

# Mengirim pesan ke dalam koneksi TCP
clientSocket.send(sentence.encode())

# Menerima balasan dari server
modifiedSentence = clientSocket.recv(2048)

# Menampilkan pesan
print(modifiedSentence.decode())

# Menutup soket dan koneksi TCP
clientSocket.close()