# zafiyet-arac
Zafiyet Aracı, Flask kullanılarak geliştirilmiş, temel güvenlik testlerini web arayüzü üzerinden gerçekleştiren bir zafiyet tarayıcısıdır. Kullanıcı dostu arayüzü sayesinde hedef URL'leri analiz eder ve potansiyel açıkları tespit eder.

##  Özellikler
- SQL Enjeksiyonu tespiti
- XSS (Cross-Site Scripting) kontrolü
- CSRF (Cross-Site Request Forgery) form kontrolü
- Oturum ve Cookie denetimi
- Yüklenebilir dosya noktalarını işaretleme

## Kurulum
git clone https://github.com/cigdem-n/zafiyet-arac.git
cd zafiyet-arac
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 app.py

Uygulama varsayılan olarak http://127.0.0.1:5000 adresinde çalışacaktır.

## Kullanım
-Tarayıcıdan http://127.0.0.1:5000 adresine gidin.
-Hedef URL'yi girin.
-Tarama başlatın, sonuçları anlık olarak görüntüleyin.

## Lisans
Bu proje açık kaynak olup MIT lisansı ile lisanslanmıştır.

