import time
from abc import ABC, abstractmethod
from typing import List

# =====================================================================
# 1. STRATEGY PATTERN (Penentuan Batas Aman / Threshold)
# =====================================================================
class ThresholdStrategy(ABC):
    @abstractmethod
    def determine_status(self, water_level: float) -> str:
        pass

class ManggaraiStrategy(ThresholdStrategy):
    """Rumus penentuan batas aman khusus untuk Pintu Air Manggarai"""
    def determine_status(self, water_level: float) -> str:
        if water_level < 6.0:
            return "Normal"
        elif water_level < 7.5:
            return "Siaga 3 (Waspada)"
        elif water_level < 8.5:
            return "Siaga 2 (Kritis)"
        else:
            return "Siaga 1 (Bencana)"

class KatulampaStrategy(ThresholdStrategy):
    """Rumus penentuan batas aman khusus untuk Bendung Katulampa"""
    def determine_status(self, water_level: float) -> str:
        if water_level < 0.5:
            return "Normal"
        elif water_level < 1.0:
            return "Siaga 3 (Waspada)"
        elif water_level < 1.5:
            return "Siaga 2 (Kritis)"
        else:
            return "Siaga 1 (Bencana)"


# =====================================================================
# 2. OBSERVER PATTERN (Push Notification ke Dashboard & Alert)
# =====================================================================
class Observer(ABC):
    @abstractmethod
    def update(self, area: str, status: str, value: float) -> None:
        pass

class DashboardPemprov(Observer):
    """Aplikasi Dashboard Pemprov menerima push update otomatis"""
    def update(self, area: str, status: str, value: float) -> None:
        print(f"[DASHBOARD PUSH] Update Area {area}: Level Air = {value:.2f}m | Status Aktual: {status}")

class NotificationAlertSystem(Observer):
    """Sistem notifikasi warga yang membunyikan sirine/alert jika bahaya"""
    def update(self, area: str, status: str, value: float) -> None:
        if "Siaga 1" in status or "Siaga 2" in status:
            print(f"[CRITICAL ALERT] BUNYIKAN SIRINE BAHAYA! Area {area} memasuki status {status} (Nilai: {value:.2f}m). Notifikasi dikirim ke warga!")
        else:
            print(f"[INFO ALERT] Area {area} terpantau aman ({status}).")

class DataProcessorSubject:
    """Subject pusat pengolah data yang mengelola Observer dan Strategy"""
    def __init__(self, area_name: str, strategy: ThresholdStrategy):
        self.area_name = area_name
        self.strategy = strategy
        self._observers: List[Observer] = []

    def add_observer(self, observer: Observer) -> None:
        self._observers.append(observer)

    def set_strategy(self, strategy: ThresholdStrategy) -> None:
        print(f"[SYSTEM] Menukar strategi penentuan threshold secara dinamis untuk {self.area_name}...")
        self.strategy = strategy

    def notify_observers(self, status: str, value: float) -> None:
        for observer in self._observers:
            observer.update(self.area_name, status, value)

    def process_data(self, final_value: float) -> None:
        # Menentukan status menggunakan Strategy Pattern
        status = self.strategy.determine_status(final_value)
        
        # Mendorong (Push) update secara otomatis ke seluruh Observer
        print(f"\n[ENGINE] Memproses data akhir: {final_value:.2f}m di {self.area_name}...")
        self.notify_observers(status, final_value)


# =====================================================================
# 3. COMPONENT INTERFACE & FACTORY METHOD (Produksi Sensor)
# =====================================================================
class Sensor(ABC):
    @abstractmethod
    def read_data(self) -> float:
        pass

    @abstractmethod
    def get_unit(self) -> str:
        pass

class BaseWaterLevelSensor(Sensor):
    """Sensor aktual yang membaca nilai dari lingkungan dalam satuan Meter"""
    def __init__(self, raw_values: List[float]):
        self.raw_values = raw_values
        self.index = 0

    def read_data(self) -> float:
        # Mensimulasikan data mengalir berurutan
        val = self.raw_values[self.index % len(self.raw_values)]
        self.index += 1
        return val

    def get_unit(self) -> str:
        return "Meter"

class BaseRainfallSensor(Sensor):
    """Sensor aktual curah hujan dalam satuan mm/jam"""
    def __init__(self, raw_values: List[float]):
        self.raw_values = raw_values
        self.index = 0

    def read_data(self) -> float:
        val = self.raw_values[self.index % len(self.raw_values)]
        self.index += 1
        return val

    def get_unit(self) -> str:
        return "mm/jam"

class SensorFactory:
    """Factory Method bertugas memproduksi tipe objek sensor yang tepat"""
    @staticmethod
    def create_sensor(sensor_type: str, raw_data: List[float]) -> Sensor:
        if sensor_type.upper() == "WATER_LEVEL":
            return BaseWaterLevelSensor(raw_data)
        elif sensor_type.upper() == "RAINFALL":
            return BaseRainfallSensor(raw_data)
        else:
            raise ValueError(f"Tipe sensor {sensor_type} tidak didukung.")


# =====================================================================
# 4. DECORATOR PATTERN (Filtering & Smoothing Aliran Data)
# =====================================================================
class SensorDecorator(Sensor):
    """Kelas abstrak pembungkus (wrapper) aliran data mentah dari sensor"""
    def __init__(self, wrapped_sensor: Sensor):
        self.wrapped_sensor = wrapped_sensor

    def get_unit(self) -> str:
        return self.wrapped_sensor.get_unit()

class NoiseFilterDecorator(SensorDecorator):
    """Membuang lonjakan data anomali yang tidak masuk akal (misal: burung hinggap)"""
    def __init__(self, wrapped_sensor: Sensor, max_allowed_jump: float):
        super().__init__(wrapped_sensor)
        self.max_allowed_jump = max_allowed_jump
        self.last_valid_value: float = None

    def read_data(self) -> float:
        current_value = self.wrapped_sensor.read_data()
        
        # Inisialisasi nilai referensi pertama
        if self.last_valid_value is None:
            self.last_valid_value = current_value
            return current_value
        
        # Deteksi lonjakan ekstrem yang tidak realistis dalam hitungan detik
        if abs(current_value - self.last_valid_value) > self.max_allowed_jump:
            print(f"[FILTER WARNING] Anomali/Noise terdeteksi! Lonjakan dari {self.last_valid_value}m ke {current_value}m diabaikan.")
            # Mengembalikan nilai valid terakhir agar tidak memicu sirine keliru (False Alarm)
            return self.last_valid_value
        
        self.last_valid_value = current_value
        return current_value

class AverageSmoothingDecorator(SensorDecorator):
    """Mengambil nilai rata-rata dari pembacaan 5 detik terakhir"""
    def __init__(self, wrapped_sensor: Sensor, window_size: int = 3):
        super().__init__(wrapped_sensor)
        self.window_size = window_size
        self.history: List[float] = []

    def read_data(self) -> float:
        val = self.wrapped_sensor.read_data()
        self.history.append(val)
        if len(self.history) > self.window_size:
            self.history.pop(0)
        
        avg_value = sum(self.history) / len(self.history)
        print(f"[SMOOTHING] Buffer memori internal: {[round(x, 2) for x in self.history]} -> Rata-rata: {avg_value:.2f}m")
        return avg_value


# =====================================================================
# SIMULASI UTAMA (MAIN EXECUTION)
# =====================================================================
def main():
    print("=====================================================================")
    print("  SIMULASI STREAM PROCESSING & EARLY WARNING SYSTEM - DKI JAKARTA")
    print("=====================================================================")

    # 1. Mendaftarkan Observers pada ekosistem
    dashboard = DashboardPemprov()
    alert_system = NotificationAlertSystem()

    # 2. Inisialisasi Subject dengan Topologi & Strategi Manggarai
    processor = DataProcessorSubject("Pintu Air Manggarai", ManggaraiStrategy())
    processor.add_observer(dashboard)
    processor.add_observer(alert_system)

    # 3. Aliran Data Dummy Sensor Ketinggian Air (Mengandung kasus anomali lonjakan 10m)
    # Skenario: 2.0m (Aman), 2.1m (Aman), 10.0m (Burung lewat/Noise), 6.5m (Siaga 3), 8.6m (Siaga 1)
    raw_data_stream = [2.0, 2.1, 10.0, 6.5, 8.6]

    # 4. Inisialisasi objek dasar menggunakan Factory Method
    base_sensor = SensorFactory.create_sensor("WATER_LEVEL", raw_data_stream)

    # 5. Membungkus (Wrap) objek dasar menggunakan Decorator berlapis
    # Batas toleransi perubahan ekstrem antar pembacaan di-set ke 1.5 meter.
    filtered_sensor = NoiseFilterDecorator(base_sensor, max_allowed_jump=1.5)
    smoothed_sensor = AverageSmoothingDecorator(filtered_sensor, window_size=3)

    # 6. Eksekusi pengiriman data secara berkala (Setiap 5 detik)
    print("\n[INFO] Memulai Ingestion Data Sensor (Setiap 5 Detik)...")
    for i in range(len(raw_data_stream)):
        print(f"\n--- Waktu: Detik ke-{i*5} ---")
        # Mengambil data dari lapisan pelapis paling luar (decorator tertinggi)
        final_clean_value = smoothed_sensor.read_data()
        
        # Mendorong hasil akhir ke Subject untuk evaluasi logika bahaya dan broadcasting
        processor.process_data(final_clean_value)
        
        # Simulasi keterlambatan/jeda waktu operasi
        time.sleep(1) 

if __name__ == "__main__":
    main()