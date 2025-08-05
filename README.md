# Arsa/Arazi İlan Düzenleyici

AI destekli arsa ve arazi ilanlarını düzenleyen ve Google Sheets'e kaydeden modern web uygulaması.

## 🚀 Özellikler

- **AI Destekli Metin Düzenleme**: Gemini AI ile profesyonel ilan formatı
- **Google Sheets Entegrasyonu**: Otomatik kayıt ve geçmiş görüntüleme
- **Mobile Uyumlu**: Responsive tasarım
- **Modern UI**: Kullanıcı dostu arayüz
- **Gerçek Zamanlı İşleme**: Hızlı ve etkili

## 🛠️ Teknolojiler

- **Backend**: Python Flask
- **Frontend**: HTML5, CSS3, JavaScript
- **AI**: Google Gemini API
- **Database**: Google Sheets
- **Authentication**: Google OAuth2

## 📋 Kurulum

### 1. Gereksinimler
- Python 3.11+
- Google Cloud Console hesabı
- Gemini AI API anahtarı

### 2. Proje Kurulumu
```bash
# Repository'yi klonlayın
git clone <repository-url>
cd Whatsapp_Excel

# Virtual environment oluşturun
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Bağımlılıkları yükleyin
pip install -r requirements.txt
```

### 3. Environment Değişkenleri
`env_example.txt` dosyasını `.env` olarak kopyalayın ve değerleri doldurun:

```bash
cp env_example.txt .env
```

Gerekli değerler:
- `GOOGLE_CLIENT_ID`: Google Cloud Console'dan alın
- `GOOGLE_CLIENT_SECRET`: Google Cloud Console'dan alın
- `GEMINI_API_KEY`: Gemini AI API anahtarı
- `SECRET_KEY`: Flask secret key (rastgele string)

### 4. Google Cloud Console Kurulumu

1. [Google Cloud Console](https://console.cloud.google.com/)'a gidin
2. Yeni proje oluşturun
3. Google Sheets API'yi etkinleştirin
4. OAuth2 credentials oluşturun:
   - Application type: Web application
   - Authorized redirect URIs: `http://localhost:5000/auth/callback` (development)
   - Production için: `https://your-domain.com/auth/callback`

### 5. Gemini AI API Kurulumu

1. [Google AI Studio](https://makersuite.google.com/app/apikey)'ya gidin
2. API anahtarı oluşturun
3. `.env` dosyasına ekleyin

## 🚀 Çalıştırma

### Development
```bash
python app.py
```

Uygulama `http://localhost:5000` adresinde çalışacak.

### Production (Vercel) - Önerilen
```bash
# 1. GitHub'a push edin
git add .
git commit -m "Vercel deployment için hazır"
git push origin main


### Production (Heroku)
```bash
# Heroku CLI ile
heroku create your-app-name
heroku config:set GOOGLE_CLIENT_ID=your_client_id
heroku config:set GOOGLE_CLIENT_SECRET=your_client_secret
heroku config:set GEMINI_API_KEY=your_api_key
heroku config:set SECRET_KEY=your_secret_key
git push heroku main
```

## 📱 Kullanım

1. **Google Sheets Bağlantısı**: "Google Sheets'e Bağlan" butonuna tıklayın
2. **Metin Girişi**: İlan metnini textarea'ya yapıştırın
3. **AI Düzenleme**: "AI ile Düzenle ve Kaydet" butonuna tıklayın
4. **Sonuç**: Düzenlenmiş metin görüntülenir ve Google Sheets'e kaydedilir
5. **Geçmiş**: Önceki ilanları görüntüleyin

## 🔧 API Endpoints

- `GET /`: Ana sayfa
- `GET /auth/google`: Google OAuth başlat
- `GET /auth/callback`: OAuth callback
- `POST /process_text`: Metin işleme
- `GET /get_sheets_data`: Sheets verilerini getir

## 📊 AI Düzenleme Kuralları

Gemini AI şu kurallara göre metinleri düzenler:
1. Başlık ekleme (örn: "ARSA SATILIK")
2. Önemli bilgileri madde halinde düzenleme
3. Konum, metrekare, fiyat bilgilerini belirginleştirme
4. İletişim bilgilerini düzenleme
5. Türkçe dilbilgisi kurallarına uygunluk
6. Gereksiz tekrarları kaldırma
7. Profesyonel ton kullanma

## 🎨 Özelleştirme

### Stil Değişiklikleri
`templates/index.html` dosyasındaki CSS'i düzenleyebilirsiniz.

### AI Prompt Değişiklikleri
`app.py` dosyasındaki `format_with_gemini` fonksiyonunu düzenleyebilirsiniz.

## 🚀 Deployment Seçenekleri

### Ücretsiz Hosting Platformları

1. **Vercel** (Önerilen)
   - Hızlı deployment
   - Ücretsiz tier
   - Otomatik SSL
   - Edge functions desteği
   - Kolay GitHub entegrasyonu

2. **Railway**
   - Hızlı deployment
   - Ücretsiz kredi
   - Otomatik SSL

3. **Render**
   - Ücretsiz tier
   - Otomatik deployment
   - SSL dahil

4. **Heroku**
   - Kolay deployment
   - Ücretsiz tier mevcut
   - SSL sertifikası dahil

### Deployment Adımları

1. Repository'yi GitHub'a push edin
2. Hosting platformunda yeni proje oluşturun
3. GitHub repository'yi bağlayın
4. Environment değişkenlerini ayarlayın
5. Deploy edin

## 🔒 Güvenlik

- OAuth2 ile güvenli Google bağlantısı
- Environment değişkenleri ile API anahtarları korunması
- HTTPS zorunluluğu (production)
- Session yönetimi

## 🐛 Sorun Giderme

### Yaygın Hatalar

1. **Google OAuth Hatası**
   - Redirect URI'ları kontrol edin
   - API'lerin etkin olduğundan emin olun

2. **Gemini API Hatası**
   - API anahtarının doğru olduğunu kontrol edin
   - Quota limitlerini kontrol edin

3. **Sheets Bağlantı Hatası**
   - OAuth scope'larını kontrol edin
   - Credentials'ları yenileyin

## 📈 Gelecek Özellikler

- [ ] Çoklu dil desteği
- [ ] İlan şablonları
- [ ] Fiyat analizi
- [ ] Konum haritası entegrasyonu
- [ ] Email bildirimleri
- [ ] İstatistikler ve raporlar

## 🤝 Katkıda Bulunma

1. Fork edin
2. Feature branch oluşturun (`git checkout -b feature/amazing-feature`)
3. Commit edin (`git commit -m 'Add amazing feature'`)
4. Push edin (`git push origin feature/amazing-feature`)
5. Pull Request oluşturun

## 📄 Lisans

Bu proje MIT lisansı altında lisanslanmıştır.

## 📞 İletişim

Sorularınız için issue açabilir veya email gönderebilirsiniz. 