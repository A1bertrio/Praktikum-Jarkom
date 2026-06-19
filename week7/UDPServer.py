from socket import *

serverPort = 12000

# Membuat soket server untuk UDP
serverSocket = socket(AF_INET, SOCK_DGRAM)

# Mengikat (bind) port 12000 ke soket server
serverSocket.bind(('', serverPort))

print("Server UDP sudah siap menerima pesan...")

# Loop tak terbatas untuk terus mendengarkan paket dari klien
while True:
    # Menerima pesan dan alamat klien
    message, clientAddress = serverSocket.recvfrom(2048)
    
    # Mengubah pesan menjadi string dan huruf kapital
    modifiedMessage = message.decode().upper()
    
    # Mengirim kembali pesan yang dimodifikasi ke alamat klien
    serverSocket.sendto(modifiedMessage.encode(), clientAddress)