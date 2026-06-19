# **LAPORAN PRAKTIKUM JARINGAN KOMPUTER - MODUL 10**
## **IP**

### **Identitas Mahasiswa**
**Nama:** Albertio Suranta Ginting  
**NIM:** 103072400128  
**Kelas:** IF - 04 - 01

---

## A. Tujuan Praktikum
1.  Menginvestigasi cara kerja protokol IP menggunakan Wireshark

---

## B. Pengantar
Modul ini memiliki tiga bagian. Pada bagian pertama, kita akan menganalisis paket dalam jejak datagram IPv4 yang dikirim dan diterima oleh program traceroute (program traceroute itu sendiri dieksplorasi lebih detail di lab Wireshark ICMP). Kita akan mempelajari fragmentasi IP di bagian 2 modul ini, dan melihat sekilas IPv6 di bagian 3 modul ini.

## C. Menangkap paket dari eksekusi traceroute
### 1. Fundamental IPv4 (Traceroute & TTL)
**Tujuan Observasi:** Melakukan pengamatan terhadap paket dasar IPv4 serta memahami fungsi kendali *Time-to-Live* (TTL) memanfaatkan utilitas baris perintah *traceroute* atau *tracert*.

**Tangkapan Layar Wireshark:**
![Figure 10.1 Basic IPv4](assets/image/1.png)

**Pembahasan & Analisis:**
Utilitas *traceroute* bekerja dengan melacak rute topologi dari pengirim ke target tujuannya. Cara kerjanya adalah dengan mengirim paket-paket data sembari menaikkan limit masa hidup paket atau *Time-to-Live* (TTL) secara bertahap. Tiap kali paket singgah di sebuah *router* (*hop*), *router* tersebut wajib memotong nilai TTL pada *header* IPv4 sebanyak satu angka. Apabila nilai TTL mencapai batas nol sebelum paket tiba di tujuan akhirnya, *router* secara otomatis akan menggugurkan paket tersebut lalu membalas dengan pesan kegagalan berupa *ICMP Time-to-live exceeded* ke alamat pengirim asal. Memanfaatkan pesan *error* ICMP inilah, perangkat klien dapat merekam dan menampilkan alamat IP dari masing-masing *router* perantara yang menjembatani jalur komunikasi tersebut.

#### 2 Mekanisme Fragmentasi IP
**Tujuan Observasi:** Mengkaji bagaimana protokol IPv4 menangani pemecahan data (fragmentasi) ketika ukuran datagram jauh melampaui kapasitas angkut maksimal atau *Maximum Transmission Unit* (MTU) pada infrastruktur jaringan.

**Tangkapan Layar Wireshark:**
![Figure 10.2 Fragmentasi IP](assets/image/2.png)

**Pembahasan & Analisis:**
Saat sistem mengupayakan pengiriman datagram berukuran jumbo (misalnya 3000 *byte*), transmisi tidak bisa dilakukan dalam sekali jalan karena mentok pada batasan *Maximum Transmission Unit* (MTU) standar yang biasanya bernilai 1500 *byte*. Berdasarkan penelusuran Wireshark (merujuk pada paket ke-343), terlihat *router* memotong-motong pesan tersebut menjadi sejumlah fragmen dengan ukuran paling tinggi 1514 *byte* (telah mencakup kapsulasi *ethernet*). Pada inspeksi lapisan *header* IPv4, parameter *flag* **More fragments** berstatus **Set (1)**, yang secara tegas menandakan bahwa paket terkait hanyalah serpihan awal atau tengah, dan masih ada serpihan berikutnya. Parameter **Fragment Offset** yang menunjuk angka 0 mengonfirmasi bahwa ini adalah *byte* pembuka dari datagram utuh. Seluruh kepingan dari satu pengiriman yang sama akan dibekali ID yang sama persis pada kolom **Identification** (dalam kasus ini bernilai `0x0045`), sehingga perangkat tujuan tidak keliru saat merakit ulang (*reassembly*) kepingan tersebut menjadi berkas utuh.

#### 3. IPv6
**Tujuan Observasi:** Menganalisis perubahan struktur *header*, sistem pengalamatan, serta cara kerja resolusi nama domain pada protokol masa depan, Internet Protocol version 6 (IPv6).

**Tangkapan Layar Wireshark:**
![Figure 10.3 IPv6](assets/image/3.png)

**Pembahasan & Analisis:**
Analisis datagram IPv6 disimulasikan melalui penyadapan paket DNS jenis *Standard Query AAAA* yang mencari domain `youtube.com`. Jika IPv4 menggunakan *query record A*, infrastruktur IPv6 secara khusus mensyaratkan *record AAAA* untuk memetakan nama domain ke dalam format alamat IP generasi keenam. Menilik lebih dalam pada panel rincian *header* IPv6, tampak perubahan sangat kontras di bagian *Source Address* dan *Destination Address*. Formatnya bukan lagi desimal 32-bit yang dipisahkan oleh titik, melainkan barisan panjang 128-bit yang direpresentasikan menggunakan blok karakter heksadesimal. Desain *header* IPv6 ini memang sengaja dibuat lebih ringkas dari sisi hierarki namun membawa kapasitas kuota alamat yang luar biasa besar untuk memecahkan krisis habisnya stok alamat IP global.

---

### D. Kesimpulan
Dari praktikum Modul 10 terkait analisis lalu lintas protokol IP (baik IPv4 maupun IPv6) melalui Wireshark, dapat disimpulkan sebagai berikut:

1. **Pemetaan Jalur Hop-by-Hop:** Protokol IP sangat bergantung pada *field Time-to-Live* (TTL) guna membatasi perputaran paket tanpa henti. Trik menaikkan TTL bertahap oleh utilitas *traceroute* terbukti sukses memicu *router* untuk mengirim balik paket *ICMP Time-to-live exceeded (Type 11)*, sehingga rute komunikasi yang dilalui dapat terpetakan dengan baik.
2. **Kondisi Memicu Fragmentasi:** Lapisan *network* akan langsung menginisiasi fragmentasi IP manakala ukuran paket melebihi batas toleransi kapasitas *link* fisik (MTU). Proses dekonstruksi paket ini dilakukan oleh perangkat *router* secara independen di tengah perjalanan transmisi.
3. **Kunci Rekonstruksi Data:** Agar proses perakitan kembali fragmen di pihak penerima berhasil, protokol IPv4 wajib menyertakan tiga parameter penting: *Identification* (ID unik per datagram), *Flags* (indikator fragmen terakhir via bit *More fragments*), serta *Fragment Offset* (indikator posisi *byte* susunan paket).
4. **Skalabilitas Pengalamatan IPv6:** Transisi menuju IPv6 membawa perombakan radikal dengan peralihan identitas alamat dari format 32-bit menuju 128-bit berbasis heksadesimal, memastikan pasokan alamat IP tercukupi untuk puluhan tahun mendatang.
5. **Dukungan DNS untuk IPv6:** Implementasi jaringan IPv6 sudah difasilitasi dengan mulus oleh sistem penamaan domain (DNS) yang menyediakan *record Query AAAA*, bekerja setara dengan *record A* namun khusus mengembalikan balasan berupa rantai alamat heksadesimal 128-bit.   

---