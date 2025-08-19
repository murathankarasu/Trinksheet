# Land/Plot Advertisement Organizer

Modern web application that regulates AI-supported land and land advertisements and saves them to Google Sheets.

## 🚀 Features

- **AI Supported Text Editing**: Professional ad format with Gemini AI

- **Google Sheets Integration**: Automatic registration and history viewing

- **Mobile Compatible**: Responsive design

- **Modern UI**: User-friendly interface

- **Real-Time Processing**: Fast and effective

## 🛠️ Technologies

- **Backend**: Python Flask

- **Frontend**: HTML5, CSS3, JavaScript

- **AI**: Google Gemini API

- **Database**: Google Sheets

- **Authentication**: Google OAuth2

## 📋 Installation

### 1. Requirements

- Python 3.11+

- Google Cloud Console account

- Gemini AI API key

### 2. Project Setup

```bash

# Clone the repository

Git clone <repository-url>

Cd Whatsapp_Excel

# Create a virtual environment

Python -m venv venv

Source venv/bin/activate # Windows: venv\Scripts

# Install dependencies

Pip install -r requirements.txt

```

### 3. Environment Variables

Copy the `env_example.txt` file as `.env` and fill in the values:

```bash

Cp env_example.txt .env

```

Required values:

- `GOOGLE_CLIENT_ID`: Get from Google Cloud Console

- `GOOGLE_CLIENT_SECRET`: Get from Google Cloud Console

- `GEMINI_API_KEY`: Gemini AI API key

- `SECRET_KEY`: Flask secret key (random string)

You can open an issue or send an email for your questions.
