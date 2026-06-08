# FloodWatch - Sistem Peringatan Dini & Stream Processing Banjir DKI Jakarta

FloodWatch adalah aplikasi simulasi *Stream Processing* dan *Early Warning System* (Sistem Peringatan Dini) banjir berbasis sensor untuk wilayah DKI Jakarta. Proyek ini mengimplementasikan berbagai **Design Patterns** (Pola Desain Perangkat Lunak) untuk menghasilkan arsitektur kode yang bersih, modular, dan mudah dipelihara (*maintainable*).

---

## 🛠️ Implementasi Design Patterns

Program ini mendemonstrasikan penerapan 4 design patterns utama:

1. **Strategy Pattern**
   * Digunakan untuk menentukan batas aman (threshold) secara dinamis berdasarkan pintu air tertentu (contoh: `ManggaraiStrategy` dan `KatulampaStrategy`).
2. **Observer Pattern**
   * Digunakan untuk mendorong (*push*) data sensor yang telah diproses secara otomatis ke berbagai sistem pemantau seperti `DashboardPemprov` dan `NotificationAlertSystem` (pembunyian sirine/peringatan warga).
3. **Factory Method Pattern**
   * Memisahkan pembuatan objek sensor (`BaseWaterLevelSensor`, `BaseRainfallSensor`) melalui kelas pembuat terpusat `SensorFactory`.
4. **Decorator Pattern**
   * Digunakan untuk melakukan pemrosesan awal (*preprocessing*) aliran data sensor secara fleksibel:
     * `NoiseFilterDecorator` – Membuang data anomali ekstrem (noise).
     * `AverageSmoothingDecorator` – Menghitung rata-rata bergerak (*moving average*) dari beberapa pembacaan terakhir.

---

## 🚀 Cara Menjalankan Program

### Prasyarat
* Python 3.x terinstal di sistem Anda.

### Langkah-langkah
1. Clone repositori ini atau salin file program.
2. Jalankan program dengan perintah berikut di terminal Anda:
   ```bash
   python FloodWatch.py
   ```

---

## 📊 Contoh Output Simulasi

Saat dijalankan, program akan mensimulasikan pembacaan sensor setiap 5 detik:

```text
=====================================================================
  SIMULASI STREAM PROCESSING & EARLY WARNING SYSTEM - DKI JAKARTA
=====================================================================

[INFO] Memulai Ingestion Data Sensor (Setiap 5 Detik)...

--- Waktu: Detik ke-0 ---
[SMOOTHING] Buffer memori internal: [2.0] -> Rata-rata: 2.00m

[ENGINE] Memproses data akhir: 2.00m di Pintu Air Manggarai...
[DASHBOARD PUSH] Update Area Pintu Air Manggarai: Level Air = 2.00m | Status Aktual: Normal
[INFO] Area Pintu Air Manggarai terpantau aman (Normal).
...
```

---

## 👥 Kontributor
* **Fahryan Amadis**
* **Dian Hermawan**
* **Ivan Maulana Bahtiar**
* **Raushanfikri Abdillah**
* **Risky Aditya Pratama**
