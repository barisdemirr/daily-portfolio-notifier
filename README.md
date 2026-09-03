# Kur Takip

Portföyünüzdeki dolar, euro ve altın (gram, çeyrek, yarım, tam) miktarlarını
takip eder ve her gün belirlenen saatte güncel değerleriyle birlikte
e-posta raporu gönderir.

## Kurulum

### 1. Bağımlılıklar

```
pip install -r requirements.txt
```

### 2. Ortam değişkenleri

Aşağıdaki ortam değişkenlerini ayarlayın (yerelde `.env` yerine doğrudan
shell'de export edebilir, GitHub Actions'ta ise repo secret olarak
eklersiniz):

- `RAPIDAPI_KEY` — RapidAPI üzerinden "Döviz ve Altın Fiyatları (TRY)" API'sine ait key
- `GMAIL_ADDRESS` — Gönderici Gmail adresi
- `GMAIL_APP_PASSWORD` — Gmail App Password (normal şifre değil)
- `MAIL_RECIPIENT` — Raporun gönderileceği adres (boş bırakılırsa GMAIL_ADDRESS kullanılır)

Gmail App Password almak için: Google Hesabı > Güvenlik > 2 Adımlı
Doğrulama açık olmalı > Uygulama Şifreleri kısmından yeni bir şifre
oluşturun.

### 3. Portföyü ayarlama

```
python portfolio.py add USD 100
python portfolio.py add EUR 50
python portfolio.py set CEYREK_ALTIN 3
python portfolio.py list
```

Geçerli varlıklar: `USD`, `EUR`, `GRAM_ALTIN`, `CEYREK_ALTIN`, `YARIM_ALTIN`, `TAM_ALTIN`

Bu komutlar `portfolio.json` dosyasını oluşturur/günceller. Bu dosya
`.gitignore` içinde olduğu için repoya gitmez.

### 4. Manuel çalıştırma

```
python main.py
```

## GitHub Actions ile otomatik çalıştırma

`.github/workflows/daily-report.yml` dosyası her gün UTC 06:00'da
(Türkiye saatiyle yaz saatinde 09:00) çalışacak şekilde ayarlıdır.
Saat değiştirmek isterseniz dosyadaki `cron` değerini güncelleyin.

GitHub Actions üzerinden çalıştırmak için repo secret'ları eklemeniz
gerekir (Settings > Secrets and variables > Actions):

- `RAPIDAPI_KEY`
- `GMAIL_ADDRESS`
- `GMAIL_APP_PASSWORD`
- `MAIL_RECIPIENT`
- `PORTFOLIO_JSON` — `portfolio.json` dosyasının tüm içeriği, tek satır JSON olarak

`PORTFOLIO_JSON` secret'ını oluşturmak için yerel `portfolio.json`
dosyasının içeriğini olduğu gibi kopyalayıp secret değeri olarak
yapıştırabilirsiniz.

Workflow'u manuel tetiklemek için repo > Actions > "daily-report" >
"Run workflow" kullanılabilir.
