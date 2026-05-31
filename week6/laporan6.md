# **LAPORAN PRAKTIKUM JARINGAN KOMPUTER - MODUL 6**
## **Transmission Control Protocol (TCP) Analysis**

### **Identitas Mahasiswa**
**Nama:** Albertio Suranta Ginting  
**NIM:** 103072400128  
**Kelas:** IF - 04 - 01

---

## A. Tujuan Praktikum
1. Dapat menginvestigasi cara kerja protokol TCP menggunakan Wireshark

---

## B. Pengantar
Praktikum ini bertujuan untuk mempelajari protokol TCP secara mendetail dengan menganalisis jejak (trace) segmen TCP yang dikirim dan diterima saat transfer file sebesar 150 KB dari komputer ke remote server. File yang digunakan dalam transfer ini berisi teks ASCII dari naskah Alice's Adventures in Wonderland karya Lewis Carrol. Fokus analisis meliputi penggunaan nomor urutan, acknowledgement TCP, algoritma congestion control TCP (mulai lambat atau slow start dan penghindaran kemacetan), mekanisme flow control, hingga investigasi performa (throughput dan round-trip time) koneksi TCP.

---

## C. Langkah Praktikum
1. Buka browser web dan unduh salinan ASCII dari naskah Alice in Wonderland melalui http://gaia.cs.umass.edu/wireshark-labs/alice.txt, lalu simpan di komputer.
2. Buka halaman http://gaia.cs.umass.edu/wireshark-labs/TCP-wireshark-file1.html.
3. Gunakan tombol Browse untuk memilih file teks yang sudah diunduh.
4. Jalankan Wireshark dan mulai penangkapan paket (packet capture).
5. Tekan tombol "Upload file alice.txt" pada browser untuk mentransfer file ke server menggunakan metode HTTP POST.
6. Setelah file berhasil diunggah dan pesan ucapan selamat muncul, hentikan penangkapan paket pada Wireshark.

---

## D. Hasil dan Pembahasan
### 1. Tampilan Awal pada Captured Trace
![Captured Trace](assets/1.png)

**Pembahasan Soal dan Jawaban**  
a. Berapa alamat IP dan nomor port TCP yang digunakan oleh komputer klien (sumber) untuk mentransfer file ke gaia.cs.umass.edu?
> Alamat IP klien (sumber) adalah 192.168.110.6.  
> Nomor port TCP yang digunakan adalah 60064.

b. Apa alamat IP dari gaia.cs.umass.edu? Pada nomor port berapa ia mengirim dan menerima segmen TCP untuk koneksi ini?
> Alamat IP dari server adalah 128.119.245.12.
> Server mengirim dan menerima segmen TCP pada port 80.

c. Berapa alamat IP dan nomor port TCP yang digunakan oleh komputer klien Anda (sumber) untuk mentransfer ke gaia.cs.umass.edu?
> IP sumber: 192.168.110.6, Port: 60064.

### 2. Dasar TCP
![Dasar TCP](assets/2.png)

**Pembahasan Soal dan Jawaban**  
a. Berapa nomor urut segmen TCP SYN yang digunakan untuk memulai sambungan TCP antara komputer klien dan gaia.cs.umass.edu? Apa yang dimiliki segmen tersebut sehingga teridentifikasi sebagai segmen SYN?
> - Nomor urut (Sequence Number) segmen SYN adalah 0 secara relatif, atau 3708119946 (raw).  
> - Segmen ini teridentifikasi sebagai SYN karena pada bagian Flags (0x002), bit Syn di-set menjadi 1, sedangkan flag lainnya tidak.

b. Berapa nomor urut segmen SYNACK yang dikirim oleh gaia.cs.umass.edu ke komputer klien sebagai balasan dari SYN? Berapa nilai dari field Acknowledgement pada segmen SYNACK? Bagaimana gaia.cs.umass.edu menentukan nilai tersebut? Apa yang dimiliki oleh segmen sehingga teridentifikasi sebagai segmen SYNACK?
> - Nomor urut (Sequence Number) segmen SYNACK adalah 0.
> - Nilai field Acknowledgement adalah 1 atau 3708119947.
> - Nilai tersebut ditentukan dengan menambahkan 1 pada raw sequence number dari paket SYN klien sebelumnya (3708119946 + 1).
> - Segmen teridentifikasi sebagai SYNACK karena pada bagian Flags (0x012), bit Acknowledgment dan Syn keduanya di-set menjadi 1.

c. Berapa nomor urut segmen TCP yang berisi perintah HTTP POST?
> Nomor urut (Sequence Number) paket HTTP POST adalah 1 secara relatif, atau 3210585950.

d. Berapa nomor urut dari enam segmen pertama dalam TCP (termasuk segmen HTTP POST)? Pada jam berapa setiap segmen dikirim?
> Dari daftar paket (paket nomor 245 hingga 250), berikut adalah nomor urut (Sequence Number) dan waktu pengiriman (Time) untuk 6 segmen data pertama:
> - Segmen 1 (HTTP POST): Seq = 1. Dikirim pada waktu 2.232787500.
> - Segmen 2: Seq = 729. Dikirim pada waktu 2.232939300.
> - Segmen 3: Seq = 2129. Dikirim pada waktu 2.232939300.
> - Segmen 4: Seq = 3529. Dikirim pada waktu 2.232939300.
> - Segmen 5: Seq = 4929. Dikirim pada waktu 2.232939300.
> - Segmen 6: Seq = 6329. Dikirim pada waktu 2.232939300.

e. Berapa panjang setiap enam segmen TCP pertama?
> Dilihat dari kolom Length (sebagai payload TCP / Len di kolom info), panjang dari enam segmen pertama adalah:
> - Segmen 1: 728 bytes
> - Segmen 2: 1400 bytes
> - Segmen 3: 1400 bytes
> - Segmen 4: 1400 bytes
> - Segmen 5: 1400 bytes
> - Segmen 6: 1400 bytes

f. Berapa jumlah minimum ruang buffer tersedia yang disarankan kepada penerima dan diterima untuk seluruh trace? Apakah kurangnya ruang buffer penerima pernah menghambat pengiriman?
> Penawaran buffer (Window Size) awal dari pihak Server (penerima data) pada paket nomor 243 (SYN, ACK). Nilai ruang buffernya adalah Win=64240.

g. Apakah ada segmen yang ditransmisikan ulang dalam file trace?
> Tidak terlihat adanya segmen yang ditransmisikan ulang (biasanya ditandai dengan sorotan warna hitam/merah dengan teks [TCP Retransmission]).

h. Berapa banyak data yang biasanya diakui oleh penerima dalam ACK? Dapatkah anda mengidentifikasi kasus-kasus di mana penerima melakukan ACK untuk setiap segmen yang diterima?
> Sama seperti RTT di nomor 4, jawaban untuk nomor 8 (pola Acknowledgment dari penerima).

i. Berapa throughput (byte yang ditransfer per satuan waktu) untuk sambungan TCP? Jelaskan bagaimana Anda menghitung nilai ini.
> Berdasarkan statistik Conversations dari rekaman Wireshark, throughput rata-rata untuk sambungan TCP (dari klien ke server) tercatat sebesar 630 kbps (kilo-bits per second).  
> Rumus dasarnya adalah:$$\text{Throughput} = \frac{\text{Total Data}}{\text{Durasi Waktu}}$$Jika kita hitung secara manual menjadi bit per detik (bps):$$\text{Throughput} = \frac{159 \times 1024 \times 8 \text{ bits}}{2.020576 \text{ s}} \approx 644.705 \text{ bits/s} \approx 644 \text{ kbps}$$

### 3. Congestion Control pada TCP
![Congestion Control](assets/3.png)
![Congestion Control](assets/4.png)

**Pembahasan Soal dan Jawaban**  
a. Dapatkah Anda mengidentifikasi di mana fase “slow start” TCP dimulai dan berakhir, dan pada bagian mana algoritma ”congestion avoidance” mengambil alih? Berikan komentar tentang bagaimana data yang diukur berbeda dari perilaku ideal TCP yang telah kita pelajari.
> - Berdasarkan grafik Sequence Numbers (Stevens) yang diunggah, fase slow start dimulai pada detik ke ~45 ms dan berlangsung hingga sekitar ~65 ms. Hal ini terlihat dari kurva garis yang melonjak ke atas secara tiba-tiba (eksponensial) dari 0 bytes hingga mencapai titik 8.5 kB dalam waktu yang sangat singkat.
> - Pada grafik ini, transisi ke fase congestion avoidance (pertumbuhan linear) tidak terlihat dengan jelas. Hal ini umumnya terjadi karena ukuran file yang ditransfer relatif kecil, sehingga proses transfer selesai sepenuhnya saat koneksi masih berada di fase slow start dan belum sempat mencapai batas threshold kemacetan (ssthresh).

---