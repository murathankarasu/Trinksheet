# 🚀 Vercel Deployment Rehberi

## 📋 Ön Gereksinimler

1. **GitHub Hesabı**
2. **Google Cloud Console Hesabı**
3. **Gemini AI API Key** (zaten var: `AIzaSyCl43mCHT9DGs9MiBrX7wQeAS9ZoTD5vSs`)

## 🔑 Google OAuth2 Credentials Alma

### 1. Google Cloud Console
1. [Google Cloud Console](https://console.cloud.google.com/)'a gidin
2. Yeni proje oluşturun: `Arsa-Arazi-Ilan-Duzenleyici`

### 2. Google Sheets API
1. "API'ler ve Hizmetler" > "Kütüphane"
2. "Google Sheets API" aratın ve etkinleştirin

### 3. OAuth2 Credentials
1. "API'ler ve Hizmetler" > "Credentials"
2. "Credentials Oluştur" > "OAuth 2.0 Client ID"
3. Uygulama türü: "Web application"
4. **Authorized redirect URIs** ekleyin:
   - `https://your-app-name.vercel.app/auth/callback`
   - `http://localhost:8000/auth/callback` (development)

## 🚀 Vercel Deployment

### 1. GitHub'a Push
```bash
git add .
git commit -m "Vercel deployment için hazır"
git push origin main
```

### 2. Vercel'de Deploy
1. [Vercel](https://vercel.com)'e gidin
2. GitHub hesabınızla giriş yapın
3. "New Project" seçin
4. Repository'nizi seçin
5. **Environment Variables** ekleyin:
   ```
   GOOGLE_CLIENT_ID=your_client_id_here
   GOOGLE_CLIENT_SECRET=your_client_secret_here
   GEMINI_API_KEY=AIzaSyCl43mCHT9DGs9MiBrX7wQeAS9ZoTD5vSs
   SECRET_KEY=arsa-arazi-ilan-duzenleyici-secret-key-2024
   ```
6. "Deploy" butonuna tıklayın

### 3. Domain Güncelleme
1. Vercel'de projenizin domain'ini kopyalayın
2. Google Cloud Console'a geri dönün
3. OAuth2 credentials'da redirect URI'yi güncelleyin:
   - `https://your-actual-domain.vercel.app/auth/callback`

## ✅ Test Etme

1. Vercel'deki uygulamanızı açın
2. "Google Sheets'e Bağlan" butonuna tıklayın
3. Google hesabınızla giriş yapın
4. Test ilanı girin ve AI düzenlemesini deneyin

## 🔧 Sorun Giderme

### Yaygın Hatalar:
1. **OAuth Hatası**: Redirect URI'leri kontrol edin
2. **API Hatası**: Google Sheets API'nin etkin olduğundan emin olun
3. **Environment Variables**: Vercel'de doğru ayarlandığından emin olun

### Log Kontrolü:
- Vercel Dashboard > Functions > app.py > View Function Logs

## 📱 Özellikler

✅ **AI Düzenleme**: Gemini AI ile profesyonel ilan formatı
✅ **Google Sheets**: Otomatik kayıt ve geçmiş görüntüleme
✅ **Mobile Uyumlu**: Responsive tasarım
✅ **Modern UI**: Kullanıcı dostu arayüz
✅ **Ücretsiz Hosting**: Vercel'in ücretsiz tier'ı

## 🎯 Sonuç

Uygulamanız artık `https://your-app-name.vercel.app` adresinde çalışıyor!

Kullanıcılar:
1. Google Sheets'e bağlanabilir
2. Arsa/arazi ilanı girebilir
3. AI ile düzenlenmiş metni alabilir
4. Geçmiş ilanları görüntüleyebilir 