from flask import Flask, render_template, request, jsonify, session
import requests
import json
import os
from dotenv import load_dotenv
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import base64

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'your-secret-key-here')

# Google OAuth2 configuration
GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# Development ortamında HTTP'ye izin ver
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

@app.route('/')
def index():
    # Session'da credentials var mı kontrol et
    is_authenticated = 'credentials' in session
    return render_template('index.html', authenticated=is_authenticated)

@app.route('/auth/google')
def google_auth():
    flow = Flow.from_client_config(
        {
            "web": {
                "client_id": GOOGLE_CLIENT_ID,
                "client_secret": GOOGLE_CLIENT_SECRET,
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "redirect_uris": [request.host_url + "auth/callback"]
            }
        },
        scopes=SCOPES
    )
    flow.redirect_uri = request.host_url + "auth/callback"
    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true'
    )
    session['state'] = state
    return jsonify({'auth_url': authorization_url})

@app.route('/auth/callback')
def auth_callback():
    flow = Flow.from_client_config(
        {
            "web": {
                "client_id": GOOGLE_CLIENT_ID,
                "client_secret": GOOGLE_CLIENT_SECRET,
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "redirect_uris": [request.host_url + "auth/callback"]
            }
        },
        scopes=SCOPES
    )
    flow.redirect_uri = request.host_url + "auth/callback"
    
    authorization_response = request.url
    flow.fetch_token(authorization_response=authorization_response)
    
    credentials = flow.credentials
    session['credentials'] = {
        'token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'token_uri': credentials.token_uri,
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret,
        'scopes': credentials.scopes
    }
    
    return render_template('index.html', authenticated=True)

@app.route('/process_text', methods=['POST'])
def process_text():
    data = request.get_json()
    raw_text = data.get('text', '')
    
    if not raw_text:
        return jsonify({'error': 'Metin boş olamaz'}), 400
    
    # Gemini AI ile metni düzenle
    formatted_text = format_with_gemini(raw_text)
    
    # Google Sheets'e kaydet
    if 'credentials' in session:
        try:
            save_to_sheets(formatted_text, raw_text)
            return jsonify({
                'success': True,
                'formatted_text': formatted_text,
                'message': 'Metin başarıyla düzenlendi ve Google Sheets\'e kaydedildi!'
            })
        except Exception as e:
            return jsonify({
                'success': True,
                'formatted_text': formatted_text,
                'message': f'Metin düzenlendi ama Sheets kaydetme hatası: {str(e)}'
            })
    else:
        return jsonify({
            'success': True,
            'formatted_text': formatted_text,
            'message': 'Metin düzenlendi (Google Sheets bağlantısı yok)'
        })

def format_with_gemini(text):
    """Gemini AI ile metni arsa/arazi ilanı formatında düzenle"""
    prompt = f"""
    Aşağıdaki arsa/arazi ilanını belirtilen başlıklarla düzenle:
    
    Orijinal metin: {text}
    
    Lütfen sadece şu başlıkları kullan ve bilgileri düzenle:
    
    **İL:** [İl adını yaz]
    **İLÇE:** [İlçe adını yaz]
    **MAHALLE:** [Mahalle adını yaz - varsa]
    **M2:** [Metrekare bilgisini yaz]
    **PARSEL NO:** [Parsel numarasını yaz - varsa]
    **ADA NO:** [Ada numarasını yaz - varsa]
    **TAPU DURUMU:** [Tapu durumunu yaz - varsa]
    **İMAR DURUMU:** [İmar durumunu yaz - varsa]
    **YOL CEPHESİ:** [Yol cephesi bilgisini yaz - varsa]
    **AVANTAJLAR:** [Avantajları madde halinde yaz]
    **FİYAT:** [Fiyat bilgisini yaz - varsa]
    **İLETİŞİM:** [Telefon numarasını yaz - varsa]
    **EMAIL:** [Email adresini yaz - varsa]
    **İSİM:** [İsim soyisim bilgisini yaz - varsa]
    
    Kurallar:
    1. Sadece yukarıdaki başlıkları kullan
    2. Bilgi yoksa o başlığı atla
    3. Mahalle bilgisini varsa ekle
    4. Parsel ve ada numaralarını ayrı ayrı yaz
    5. Avantajları madde halinde yaz
    6. Fiyatı temiz formatta yaz (2.500.000 TL, 1.5M TL, vb.)
    7. Telefon numarasını temiz formatta yaz (0555 123 45 67)
    8. Email adresini küçük harflerle yaz
    9. İsim soyisim bilgisini düzgün formatta yaz
    10. Gereksiz bilgileri kaldır
    11. Sadece önemli bilgileri dahil et
    12. Profesyonel ve düzenli format kullan
    13. Metin uzunsa bile sadece bu başlıkları kullan
    """
    
    try:
        response = requests.post(
            'https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent',
            headers={
                'Content-Type': 'application/json',
                'X-goog-api-key': GEMINI_API_KEY
            },
            json={
                'contents': [{
                    'parts': [{'text': prompt}]
                }]
            }
        )
        
        if response.status_code == 200:
            result = response.json()
            if 'candidates' in result and len(result['candidates']) > 0:
                return result['candidates'][0]['content']['parts'][0]['text']
        
        return text  # AI çalışmazsa orijinal metni döndür
        
    except Exception as e:
        print(f"Gemini API hatası: {e}")
        return text

def parse_ai_response(text):
    """AI'dan gelen metni parse edip başlıkları ayır"""
    result = {}
    lines = text.split('\n')
    
    for line in lines:
        line = line.strip()
        if line.startswith('**İL:**'):
            result['İL'] = line.replace('**İL:**', '').strip()
        elif line.startswith('**İLÇE:**'):
            result['İLÇE'] = line.replace('**İLÇE:**', '').strip()
        elif line.startswith('**MAHALLE:**'):
            result['MAHALLE'] = line.replace('**MAHALLE:**', '').strip()
        elif line.startswith('**M2:**'):
            result['M2'] = line.replace('**M2:**', '').strip()
        elif line.startswith('**PARSEL NO:**'):
            result['PARSEL NO'] = line.replace('**PARSEL NO:**', '').strip()
        elif line.startswith('**ADA NO:**'):
            result['ADA NO'] = line.replace('**ADA NO:**', '').strip()
        elif line.startswith('**TAPU DURUMU:**'):
            result['TAPU DURUMU'] = line.replace('**TAPU DURUMU:**', '').strip()
        elif line.startswith('**İMAR DURUMU:**'):
            result['İMAR DURUMU'] = line.replace('**İMAR DURUMU:**', '').strip()
        elif line.startswith('**YOL CEPHESİ:**'):
            result['YOL CEPHESİ'] = line.replace('**YOL CEPHESİ:**', '').strip()
        elif line.startswith('**AVANTAJLAR:**'):
            # Avantajları topla
            advantages = []
            for adv_line in lines[lines.index(line)+1:]:
                adv_line = adv_line.strip()
                if adv_line.startswith('•') or adv_line.startswith('-'):
                    advantages.append(adv_line)
                elif adv_line and not adv_line.startswith('**'):
                    break
            result['AVANTAJLAR'] = '\n'.join(advantages)
        elif line.startswith('**FİYAT:**'):
            result['FİYAT'] = line.replace('**FİYAT:**', '').strip()
        elif line.startswith('**İLETİŞİM:**'):
            result['İLETİŞİM'] = line.replace('**İLETİŞİM:**', '').strip()
        elif line.startswith('**EMAIL:**'):
            result['EMAIL'] = line.replace('**EMAIL:**', '').strip()
        elif line.startswith('**İSİM:**'):
            result['İSİM'] = line.replace('**İSİM:**', '').strip()
    
    return result

def save_to_sheets(formatted_text, original_text):
    """Düzenlenmiş metni Google Sheets'e kaydet"""
    if 'credentials' not in session:
        raise Exception("Google Sheets bağlantısı yok")
    
    creds = Credentials(**session['credentials'])
    service = build('sheets', 'v4', credentials=creds)
    
    # Yeni bir spreadsheet oluştur veya mevcut olanı kullan
    spreadsheet_id = session.get('spreadsheet_id')
    
    if not spreadsheet_id:
        # Yeni spreadsheet oluştur
        spreadsheet = {
            'properties': {
                'title': 'Trinkarazi Text2Sheets - İlanlar'
            },
            'sheets': [
                {
                    'properties': {
                        'title': 'İlanlar',
                        'gridProperties': {
                            'rowCount': 1000,
                            'columnCount': 16
                        }
                    }
                }
            ]
        }
        
        spreadsheet = service.spreadsheets().create(body=spreadsheet).execute()
        spreadsheet_id = spreadsheet['spreadsheetId']
        session['spreadsheet_id'] = spreadsheet_id
        
        # Başlıkları ekle
        headers = [['Tarih', 'İl', 'İlçe', 'Mahalle', 'M2', 'Parsel No', 'Ada No', 'Tapu Durumu', 'İmar Durumu', 'Yol Cephesi', 'Avantajlar', 'Fiyat', 'İletişim', 'Email', 'İsim', 'Orijinal Metin']]
        service.spreadsheets().values().update(
            spreadsheetId=spreadsheet_id,
            range='A1:P1',
            valueInputOption='RAW',
            body={'values': headers}
        ).execute()
    else:
        # Mevcut tabloyu kontrol et, yoksa yeniden oluştur
        try:
            service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()
        except:
            # Tablo silinmiş, yeniden oluştur
            spreadsheet = {
                'properties': {
                    'title': 'Trinkarazi Text2Sheets - İlanlar'
                },
                'sheets': [
                    {
                        'properties': {
                            'title': 'İlanlar',
                            'gridProperties': {
                                'rowCount': 1000,
                                'columnCount': 9
                            }
                        }
                    }
                ]
            }
            
            spreadsheet = service.spreadsheets().create(body=spreadsheet).execute()
            spreadsheet_id = spreadsheet['spreadsheetId']
            session['spreadsheet_id'] = spreadsheet_id
            
            # Başlıkları ekle
            headers = [['Tarih', 'İl', 'İlçe', 'Mahalle', 'M2', 'Parsel No', 'Ada No', 'Tapu Durumu', 'İmar Durumu', 'Yol Cephesi', 'Avantajlar', 'Fiyat', 'İletişim', 'Email', 'İsim', 'Orijinal Metin']]
            service.spreadsheets().values().update(
                spreadsheetId=spreadsheet_id,
                range='A1:P1',
                valueInputOption='RAW',
                body={'values': headers}
            ).execute()
    
    # Yeni satır ekle
    from datetime import datetime
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # Mevcut satır sayısını bul
    result = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id,
        range='A:A'
    ).execute()
    
    next_row = len(result.get('values', [])) + 1
    
    # AI'dan gelen metni parse et
    parsed_data = parse_ai_response(formatted_text)
    
    # Veriyi hazırla
    values = [[
        current_time,
        parsed_data.get('İL', ''),
        parsed_data.get('İLÇE', ''),
        parsed_data.get('MAHALLE', ''),
        parsed_data.get('M2', ''),
        parsed_data.get('PARSEL NO', ''),
        parsed_data.get('ADA NO', ''),
        parsed_data.get('TAPU DURUMU', ''),
        parsed_data.get('İMAR DURUMU', ''),
        parsed_data.get('YOL CEPHESİ', ''),
        parsed_data.get('AVANTAJLAR', ''),
        parsed_data.get('FİYAT', ''),
        parsed_data.get('İLETİŞİM', ''),
        parsed_data.get('EMAIL', ''),
        parsed_data.get('İSİM', ''),
        original_text
    ]]
    
    service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id,
        range=f'A{next_row}:P{next_row}',
        valueInputOption='RAW',
        body={'values': values}
    ).execute()

@app.route('/get_sheets_data')
def get_sheets_data():
    """Google Sheets'ten verileri getir"""
    if 'credentials' not in session:
        return jsonify({'error': 'Google Sheets bağlantısı yok'}), 401
    
    try:
        creds = Credentials(**session['credentials'])
        service = build('sheets', 'v4', credentials=creds)
        
        spreadsheet_id = session.get('spreadsheet_id')
        if not spreadsheet_id:
            return jsonify({'data': []})
        
        result = service.spreadsheets().values().get(
            spreadsheetId=spreadsheet_id,
            range='A:P'
        ).execute()
        
        values = result.get('values', [])
        if len(values) <= 1:  # Sadece başlık varsa
            return jsonify({'data': []})
        
        # Başlığı atla, verileri döndür
        data = []
        for row in values[1:]:
            if len(row) >= 2:
                data.append({
                    'date': row[0] if len(row) > 0 else '',
                    'il': row[1] if len(row) > 1 else '',
                    'ilce': row[2] if len(row) > 2 else '',
                    'mahalle': row[3] if len(row) > 3 else '',
                    'm2': row[4] if len(row) > 4 else '',
                    'parsel_no': row[5] if len(row) > 5 else '',
                    'ada_no': row[6] if len(row) > 6 else '',
                    'tapu_durumu': row[7] if len(row) > 7 else '',
                    'imar_durumu': row[8] if len(row) > 8 else '',
                    'yol_cephe': row[9] if len(row) > 9 else '',
                    'avantajlar': row[10] if len(row) > 10 else '',
                    'fiyat': row[11] if len(row) > 11 else '',
                    'iletisim': row[12] if len(row) > 12 else '',
                    'email': row[13] if len(row) > 13 else '',
                    'isim': row[14] if len(row) > 14 else '',
                    'original_text': row[15] if len(row) > 15 else ''
                })
        
        return jsonify({'data': data})
        
    except Exception as e:
        return jsonify({'error': f'Veri getirme hatası: {str(e)}'}), 500

@app.route('/logout')
def logout():
    """Kullanıcıyı logout yap"""
    # Session'dan credentials'ları temizle
    session.pop('credentials', None)
    session.pop('spreadsheet_id', None)
    return jsonify({'success': True, 'message': 'Başarıyla çıkış yapıldı'})

@app.route('/get_sheets_url')
def get_sheets_url():
    """Google Sheets URL'sini döndür"""
    if 'credentials' not in session:
        return jsonify({'error': 'Google Sheets bağlantısı yok'}), 401
    
    spreadsheet_id = session.get('spreadsheet_id')
    if not spreadsheet_id:
        return jsonify({'error': 'Tabloya erişim yok'}), 404
    
    sheets_url = f"https://docs.google.com/spreadsheets/d/{spreadsheet_id}/edit"
    return jsonify({
        'success': True,
        'url': sheets_url,
        'spreadsheet_id': spreadsheet_id
    })

@app.route('/create_table', methods=['POST'])
def create_table():
    """Yeni Google Sheets tablosu oluştur"""
    if 'credentials' not in session:
        return jsonify({'error': 'Google Sheets bağlantısı yok'}), 401
    
    try:
        creds = Credentials(**session['credentials'])
        service = build('sheets', 'v4', credentials=creds)
        
        # Yeni spreadsheet oluştur
        spreadsheet = {
            'properties': {
                'title': 'Trinkarazi Text2Sheets - İlanlar'
            },
            'sheets': [
                {
                    'properties': {
                        'title': 'İlanlar',
                        'gridProperties': {
                            'rowCount': 1000,
                            'columnCount': 16
                        }
                    }
                }
            ]
        }
        
        spreadsheet = service.spreadsheets().create(body=spreadsheet).execute()
        spreadsheet_id = spreadsheet['spreadsheetId']
        session['spreadsheet_id'] = spreadsheet_id
        
        # Başlıkları ekle
        headers = [['Tarih', 'İl', 'İlçe', 'Mahalle', 'M2', 'Parsel No', 'Ada No', 'Tapu Durumu', 'İmar Durumu', 'Yol Cephesi', 'Avantajlar', 'Fiyat', 'İletişim', 'Email', 'İsim', 'Orijinal Metin']]
        service.spreadsheets().values().update(
            spreadsheetId=spreadsheet_id,
            range='A1:P1',
            valueInputOption='RAW',
            body={'values': headers}
        ).execute()
        
        return jsonify({
            'success': True,
            'message': 'Yeni tablo başarıyla oluşturuldu!',
            'spreadsheet_id': spreadsheet_id
        })
        
    except Exception as e:
        return jsonify({'error': f'Tablo oluşturma hatası: {str(e)}'}), 500

# Production için debug'ı kapat
app.debug = False

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000) 