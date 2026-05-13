🎓 Öğrenci Not Sistemi Projesi
Bu proje, Python programlama dili kullanılarak geliştirilmiş, öğrenci bilgilerini ve akademik notları yönetmeyi sağlayan kapsamlı bir sistemdir. Modern yazılım geliştirme prensiplerine uygun olarak Nesne Tabanlı Programlama (OOP) ve Modüler Mimari üzerine inşa edilmiştir.

🛠️ Teknik Özellikler
Programlama Dili: Python 3.14.0
Veri Yönetimi: SQlite (Veri serileştirme yöntemiyle kalıcı depolama)
Mimari Yapı: Nesne Tabanlı Programlama (Class, Property, Decorators, Encapsulation)
Arayüz: Konsol (CLI) Tabanlı Etkileşimli Menü
📂 Proje Yapısı ve Modüller
Ogrenci_Not_Sistemi_Proje/
├── main.py          # Uygulamanın giriş noktası ve ana döngü
├── models.py        # OOP Sınıfları (Ogrenci, Ders) ve veri kapsülleme
├── database.py      # JSON veri serileştirme ve dosya işlemleri
├── menu.py          # Konsol arayüzü ve kullanıcı etkileşimi
├── ogrenci_not_sistemi.db  # Verilerin kalıcı olarak saklandığı veritabanı
└── README.md        # Proje dokümantasyonu ve rehberi
1. models.py (Sistemin Temel Taşları)
Ders Sınıfı: Not aralıklarını kontrol eder ve harf notu (AA, BA, vb.) hesaplamalarını yapar.

Öğrenci Sınıfı: Öğrenci bilgilerini tutar, ders ekleme/silme ve genel ortalama/durum (Geçti/Kaldı) hesaplamalarını yönetir.

2. database.py (Veri Kalıcılığı)
Öğrenci nesnelerini ve ders bilgilerini ogrenci_not_sistemi.db  dosyasına kaydeder.

Uygulama başlatıldığında verileri dosyadan çekerek tekrar Python nesnelerine dönüştürür.

3. menu.py (Kullanıcı Arayüzü)
Kullanıcı dostu konsol arayüzünü yönetir.

Veri alma, listeleri tablo halinde ekrana basma ve etkileşimli menüleri sunma görevlerini üstlenir.

4. main.py (Giriş Noktası)
Uygulamanın giriş noktasıdır.

Veritabanındaki mevcut verileri yükler ve ana program döngüsünü başlatarak sistemin çalışmasını sağlar.

🚀 Nasıl Çalıştırılır?
Projeyi yerel makinenizde çalıştırmak için şu adımları izleyin:

Proje klasörünü terminalde (veya CMD) açın.
Aşağıdaki komutu girerek sistemi başlatın:
python main.py
Bu proje akademik bir çalışma kapsamında modüler yapı ve OOP prensiplerini uygulamak amacıyla geliştirilmiştir.

