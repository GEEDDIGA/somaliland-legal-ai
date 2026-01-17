# 🏛️ Somaliland Legal AI

**Kaaliye Sharci oo AI ah oo ku takhasusay Shuruucda Somaliland**

A Flask-based REST API that provides AI-powered legal assistance for Somaliland law using the Groq API with Mixtral model.

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/flask-3.0.0-green.svg)](https://flask.palletsprojects.com/)
[![Groq API](https://img.shields.io/badge/Groq-API-orange.svg)](https://groq.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 🌟 Features

- ✅ **Somali Language Support** - Provides legal assistance in Somali (af-Soomaali)
- ✅ **Somaliland Law Focus** - References Somalilandlaw.com and official government sources
- ✅ **Fast AI Responses** - Powered by Groq's Mixtral-8x7b-32768 model
- ✅ **Rate Limiting** - API protection with configurable limits
- ✅ **CORS Enabled** - Ready for web application integration
- ✅ **Error Handling** - Comprehensive logging and error management
- ✅ **Input Validation** - Secure request validation
- ✅ **Production Ready** - Configured for deployment with Gunicorn

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Groq API Key ([Get one free at console.groq.com](https://console.groq.com))

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/GEEDDIGA/somaliland-legal-ai.git
cd somaliland-legal-ai
```

2. **Create virtual environment**
```bash
python -m venv venv

# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set environment variables**
```bash
# Create .env file
echo "GROQ_API_KEY=your_api_key_here" > .env
echo "PORT=5000" >> .env
echo "FLASK_ENV=development" >> .env
```

5. **Run the server**
```bash
python server.py
```

The API will be available at `http://localhost:5000`

## 📡 API Documentation

### 🔹 Health Check
**GET** `/health`

Check if the API is running.

**Response:**
```json
{
  "status": "healthy",
  "message": "Somaliland Legal AI backend wuu shaqaynayaa.",
  "version": "1.0.0"
}
```

### 🔹 Ask Legal Question
**POST** `/ask`

Submit a legal question in Somali and receive AI-powered advice based on Somaliland law.

**Request Body:**
```json
{
  "question": "Maxay tahay xaqiijinta guurka Somaliland?"
}
```

**Successful Response (200 OK):**
```json
{
  "answer": "Guurka Somaliland waxaa lagu xaqiijiyaa saddex hab...",
  "disclaimer": "Xogtan waa kaaliye AI ah, la xidhiidh qareen rasmi ah wixii go'aan sharci ah.",
  "model": "mixtral-8x7b-32768"
}
```

**Error Response (400 Bad Request):**
```json
{
  "error": "Fadlan su'aal soo qor"
}
```

**Error Response (500 Internal Server Error):**
```json
{
  "error": "Cilad ayaa dhacday. Fadlan isku day mar kale",
  "disclaimer": "Xogtan waa kaaliye AI ah, la xidhiidh qareen rasmi ah wixii go'aan sharci ah."
}
```

### 🔹 Root Endpoint
**GET** `/`

Get API information and available endpoints.

**Response:**
```json
{
  "service": "Somaliland Legal AI",
  "version": "1.0.0",
  "endpoints": {
    "/ask": "POST - Ask legal questions",
    "/health": "GET - Health check"
  }
}
```

## 🔐 Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `GROQ_API_KEY` | Your Groq API key from console.groq.com | ✅ Yes | - |
| `PORT` | Server port number | ❌ No | 5000 |
| `FLASK_ENV` | Environment (development/production) | ❌ No | production |

## 🛡️ Rate Limiting

The API implements rate limiting to prevent abuse:

- **Global Limit**: 100 requests per hour per IP address
- **Ask Endpoint**: 20 requests per minute per IP address

When rate limit is exceeded, the API returns a `429 Too Many Requests` error.

## 🚢 Deployment

### Deploy to Render

1. Fork this repository
2. Go to [Render Dashboard](https://dashboard.render.com/)
3. Click "New +" → "Web Service"
4. Connect your GitHub repository
5. Configure:
   - **Name**: somaliland-legal-ai
   - **Environment**: Python
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn server:app`
6. Add Environment Variable:
   - Key: `GROQ_API_KEY`
   - Value: Your Groq API key
7. Click "Create Web Service"

### Deploy to Railway

1. Click: [![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new/template)
2. Connect your GitHub account
3. Select this repository
4. Add `GROQ_API_KEY` environment variable
5. Deploy!

### Deploy to Heroku

```bash
# Install Heroku CLI, then:
heroku login
heroku create somaliland-legal-ai
heroku config:set GROQ_API_KEY=your_api_key_here
git push heroku main
```

## 📂 Project Structure

```
somaliland-legal-ai/
├── server.py              # Main Flask application
├── requirements.txt       # Python dependencies
├── Procfile              # Process configuration for deployment
├── .env.example          # Environment variables template
├── .gitignore           # Git ignore rules
└── README.md            # This file
```

## 🔧 Development

### Running Tests
```bash
# Install dev dependencies
pip install pytest pytest-flask

# Run tests
pytest
```

### Code Style
```bash
# Format code
black server.py

# Lint code
flake8 server.py
```

## ⚠️ Important Disclaimer

**Ogeysiis Muhiim ah:**

Xogtan waa kaaliye AI ah oo ku salaysan macluumaad guud. Waxay bixisaa talo guud oo ku saabsan sharciga Somaliland, laakiin ma noqon karto talo sharci oo rasmi ah.

**English:**

This is an AI-powered legal assistant based on general information. It provides general guidance on Somaliland law but cannot replace official legal advice from a registered lawyer.

**⚖️ Always consult with a licensed lawyer in Somaliland for:**
- Official legal representation
- Court proceedings
- Legal document preparation
- Binding legal advice

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Groq** for providing fast AI inference
- **Somalilandlaw.com** for legal resource references
- **Mixtral-8x7b** model for AI capabilities
- **Flask** web framework community

## 📧 Contact & Support

- **GitHub**: [@GEEDDIGA](https://github.com/GEEDDIGA)
- **Project Link**: [https://github.com/GEEDDIGA/somaliland-legal-ai](https://github.com/GEEDDIGA/somaliland-legal-ai)
- **Issues**: [Report a bug or request a feature](https://github.com/GEEDDIGA/somaliland-legal-ai/issues)

## 🗺️ Roadmap

- [ ] Add support for English language queries
- [ ] Implement conversation history
- [ ] Add legal document templates
- [ ] Create web frontend interface
- [ ] Add authentication/authorization
- [ ] Implement caching for common questions
- [ ] Add support for legal document analysis
- [ ] Multi-language support (Somali, English, Arabic)

---

**Made with ❤️ for Somaliland's legal community**

*Waxaa loo sameeyay bulshada sharciga Somaliland* 🇸🇴
