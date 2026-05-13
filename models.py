


class Ders:
    """
    Tek bir dersi temsil eder.

    Özellikler (attributes):
        ders_adi : str   → Dersin adı         (örn. "Matematik")
        not_degeri: float → 0-100 arası not
    """

    # --- Harf notu sınırları: tek yerden değiştirilebilir ---
    HARF_SINIRLARI = [
        (90, "AA"),
        (80, "BA"),
        (70, "BB"),
        (60, "CB"),
        (50, "CC"),
        (40, "DC"),
        (30, "DD"),
        (0,  "FF"),
    ]

    def __init__(self, ders_adi: str, not_degeri: float):
        # Kapsülleme: dışarıdan doğrudan erişimi kısıtlamak için
        # setter üzerinden atama yapıyoruz (değer kontrolü için)
        self.ders_adi = ders_adi
        self.not_degeri = not_degeri   # property setter çağrılır

    # ── Property: not_degeri için doğrulama ──────────────────
    @property
    def not_degeri(self):
        return self._not_degeri

    @not_degeri.setter
    def not_degeri(self, deger):
        if not (0 <= deger <= 100):
            raise ValueError(f"Not 0-100 arasında olmalı! Girilen: {deger}")
        self._not_degeri = deger

    # ── Hesaplama metodu ──────────────────────────────────────
    def harf_notu(self) -> str:
        """Sayısal notu harf notuna çevirir."""
        for sinir, harf in self.HARF_SINIRLARI:
            if self._not_degeri >= sinir:
                return harf
        return "FF"

    # ── JSON'a dönüştürme (database.py için) ─────────────────
    def to_dict(self) -> dict:
        return {
            "ders_adi": self.ders_adi,
            "not_degeri": self._not_degeri
        }

    @classmethod
    def from_dict(cls, veri: dict):
        """Sözlükten Ders nesnesi oluşturur (dosyadan yüklerken)."""
        return cls(veri["ders_adi"], veri["not_degeri"])

    def __str__(self):
        return f"{self.ders_adi:<20} | Not: {self._not_degeri:>5.1f} | Harf: {self.harf_notu()}"


# ─────────────────────────────────────────────────────────────

class Ogrenci:
    """
    Bir öğrenciyi temsil eder.

    Özellikler:
        ad_soyad  : str        → Öğrencinin tam adı
        numara    : str        → Okul numarası
        dersler   : list[Ders] → Öğrenciye ait ders nesneleri listesi

    Kalıtım notu: Bu sınıf tek başına kullanılıyor; ilerletmek
    isteyenler BursluOgrenci(Ogrenci) gibi alt sınıf türetebilir.
    """

    def __init__(self, ad_soyad: str, numara: str):
        self.ad_soyad = ad_soyad
        self.numara   = numara
        self._dersler: list[Ders] = []   # Kapsülleme: liste private

    # ── Ders ekleme / silme ───────────────────────────────────
    def ders_ekle(self, ders: Ders):
        """Öğrenciye yeni ders ekler. Aynı ders adı varsa hata verir."""
        mevcutlar = [d.ders_adi.lower() for d in self._dersler]
        if ders.ders_adi.lower() in mevcutlar:
            raise ValueError(f"'{ders.ders_adi}' dersi zaten kayıtlı!")
        self._dersler.append(ders)

    def ders_sil(self, ders_adi: str) -> bool:
        """İsme göre dersi siler. Silindiyse True döner."""
        for i, d in enumerate(self._dersler):
            if d.ders_adi.lower() == ders_adi.lower():
                self._dersler.pop(i)
                return True
        return False

    def ders_guncelle(self, ders_adi: str, yeni_not: float) -> bool:
        """Var olan dersin notunu günceller."""
        for d in self._dersler:
            if d.ders_adi.lower() == ders_adi.lower():
                d.not_degeri = yeni_not   # setter doğrulama yapar
                return True
        return False

    # ── Hesaplama metotları ───────────────────────────────────
    def ortalama(self) -> float:
        """Tüm derslerin aritmetik ortalaması. Ders yoksa 0.0 döner."""
        if not self._dersler:
            return 0.0
        return sum(d.not_degeri for d in self._dersler) / len(self._dersler)

    def dersler(self) -> list:
        """Ders listesinin salt okunur kopyasını döner."""
        return list(self._dersler)

    def ders_sayisi(self) -> int:
        return len(self._dersler)

    def durum(self) -> str:
        """Ortalaması 50 ve üzeriyse 'Geçti', altındaysa 'Kaldı'."""
        return "✅ Geçti" if self.ortalama() >= 50 else "❌ Kaldı"

    # ── JSON dönüşümleri ──────────────────────────────────────
    def to_dict(self) -> dict:
        return {
            "ad_soyad": self.ad_soyad,
            "numara"  : self.numara,
            "dersler" : [d.to_dict() for d in self._dersler]
        }

    @classmethod
    def from_dict(cls, veri: dict):
        ogr = cls(veri["ad_soyad"], veri["numara"])
        for d in veri.get("dersler", []):
            ogr._dersler.append(Ders.from_dict(d))
        return ogr

    def __str__(self):
        return (f"[{self.numara}] {self.ad_soyad} | "
                f"Ders: {self.ders_sayisi()} | "
                f"Ort: {self.ortalama():.1f} | {self.durum()}")
