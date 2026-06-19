from socket import *

serverPort = 12000

# Membuat soket server penyambutan untuk TCP
serverSocket = socket(AF_INET, SOCK_STREAM)

# Mengikat (bind) port 12000 ke soket server
serverSocket.bind(('', serverPort))

# Mendengarkan permintaan koneksi (maksimal 1 antrean)
serverSocket.listen(1)

print("Server TCP sudah siap menerima koneksi...")

# Loop tak terbatas untuk menerima klien
while True:
    # Menerima koneksi baru dan membuat soket khusus untuk klien ini
    connectionSocket, addr = serverSocket.accept()
    
    # Menerima data dari klien
    sentence = connectionSocket.recv(2048).decode()
    
    # Mengubah teks menjadi huruf kapital
    capitalizedSentence = sentence.upper()
    
    # Mengirimkan teks modifikasi kembali ke klien
    connectionSocket.send(capitalizedSentence.encode())
    
    # Menutup soket koneksi untuk klien ini (soket penyambutan tetap buka)
    connectionSocket.close()