import os
import logging
import time
from functools import lru_cache
from flask import Flask, request, jsonify
from flask_cors import CORS
from groq import Groq
import requests

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Environment variables
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY", "")
PORT = int(os.getenv('PORT', 5000))
MAX_QUESTION_LENGTH = int(os.getenv('MAX_QUESTION_LENGTH', 2000))

# Validate API keys
if not GROQ_API_KEY and not HUGGINGFACE_API_KEY:
    raise RuntimeError("At least one API key (GROQ_API_KEY or HUGGINGFACE_API_KEY) is required")

# Initialize Groq client (cached at module level)
groq_client = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None

# Hugging Face configuration
HF_API_URL = "https://api-inference.huggingface.co/models/mistralai/Mixtral-8x7B-Instruct-v0.1"
HF_HEADERS = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"} if HUGGINGFACE_API_KEY else None

# Optimized system prompt (shorter, focused)
SYSTEM_PROMPT = """Waxaad tahay Kaaliye Sharci oo Somaliland ah. Jawaab su'aalaha sharciga Somaliland:
1. Isticmaal Somalilandlaw.com iyo ilaha rasmiga ah
2. Ku qor Soomaali oo cad
3. Tixraac xeerarka (Tusaale: Xeerka Madaniga, Qodobka 12)
4. Haddii loo baahan yahay qareen, ku talin in la la xidhiidho qareen Somaliland
5. Kaliya sharci Somaliland"""

# Simple in-memory cache for common questions
question_cache = {}
CACHE_MAX_SIZE = 50
CACHE_TTL = 3600  # 1 hour

def clean_cache():
    """Remove expired cache entries"""
    current_time = time.time()
    expired_keys = [k for k, v in question_cache.items() if current_time - v['time'] > CACHE_TTL]
    for key in expired_keys:
        del question_cache[key]
    
    # Limit cache size
    if len(question_cache) > CACHE_MAX_SIZE:
        oldest_keys = sorted(question_cache.keys(), key=lambda k: question_cache[k]['time'])[:10]
        for key in oldest_keys:
            del question_cache[key]

def get_cached_answer(question):
    """Get cached answer if available"""
    clean_cache()
    cache_key = question.strip().lower()[:200]  # Normalize and limit key length
    if cache_key in question_cache:
        logger.info(f"Cache hit for question: {cache_key[:50]}...")
        return question_cache[cache_key]['answer']
    return None

def cache_answer(question, answer):
    """Cache an answer"""
    cache_key = question.strip().lower()[:200]
    question_cache[cache_key] = {
        'answer': answer,
        'time': time.time()
    }

def query_huggingface(question):
    """Query Hugging Face Inference API"""
    if not HF_HEADERS:
        return None, "Hugging Face API not configured"
    
    try:
        payload = {
            "inputs": f"{SYSTEM_PROMPT}\n\nSu'aal: {question}\n\nJawaab:",
            "parameters": {
                "max_new_tokens": 800,
                "temperature": 0.4,
                "top_p": 0.9,
                "do_sample": True
            }
        }
        
        response = requests.post(HF_API_URL, headers=HF_HEADERS, json=payload, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            if isinstance(result, list) and len(result) > 0:
                return result[0].get('generated_text', '').replace(payload['inputs'], '').strip(), None
            return str(result), None
        elif response.status_code == 503:
            return None, "Model is loading, please try again in a moment"
        else:
            return None, f"HuggingFace API error: {response.status_code}"
    except Exception as e:
        logger.error(f"HuggingFace API error: {str(e)}")
        return None, str(e)

def query_groq(question):
    """Query Groq API"""
    if not groq_client:
        return None, "Groq API not configured"
    
    try:
        message = groq_client.chat.completions.create(
            model="mixtral-8x7b-32768",
            max_tokens=1024,
            temperature=0.4,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": question}
            ]
        )
        
        answer = message.choices[0].message.content if message.choices else None
        return answer, None
    except Exception as e:
        logger.error(f"Groq API error: {str(e)}")
        return None, str(e)

@app.route('/ask', methods=['POST'])
def ask_legal_bot():
    """Main endpoint for asking legal questions"""
    start_time = time.time()
    
    data = request.json or {}
    user_question = data.get('question', '').strip()
    
    # Validation
    if not user_question:
        return jsonify({"error": "Fadlan su'aal soo qor"}), 400
    
    if len(user_question) > MAX_QUESTION_LENGTH:
        return jsonify({
            "error": f"Su'aashu way dheer tahay. Fadlan soo qor wax ka yar {MAX_QUESTION_LENGTH} xaraf"
        }), 400
    
    # Check cache first
    cached_answer = get_cached_answer(user_question)
    if cached_answer:
        response_time = (time.time() - start_time) * 1000
        logger.info(f"Cached response in {response_time:.2f}ms")
        return jsonify({
            "answer": cached_answer,
            "disclaimer": "Xogtan waa kaaliye AI ah, la xidhiidh qareen rasmi ah wixii go'aan sharci ah.",
            "model": "cached",
            "response_time_ms": round(response_time, 2)
        })
    
    # Try Groq first (faster), fallback to Hugging Face
    answer = None
    error_msg = None
    model_used = None
    
    if groq_client:
        answer, error_msg = query_groq(user_question)
        model_used = "groq-mixtral-8x7b"
        
    if not answer and HF_HEADERS:
        logger.info("Falling back to Hugging Face API")
        answer, error_msg = query_huggingface(user_question)
        model_used = "huggingface-mixtral-8x7b"
    
    response_time = (time.time() - start_time) * 1000
    
    if answer:
        # Cache successful answer
        cache_answer(user_question, answer)
        
        logger.info(f"Question answered in {response_time:.2f}ms using {model_used}")
        return jsonify({
            "answer": answer,
            "disclaimer": "Xogtan waa kaaliye AI ah, la xidhiidh qareen rasmi ah wixii go'aan sharci ah.",
            "model": model_used,
            "response_time_ms": round(response_time, 2)
        })
    else:
        logger.error(f"All API calls failed: {error_msg}")
        return jsonify({
            "error": "Cilad ayaa dhacday. Fadlan isku day mar kale",
            "disclaimer": "Xogtan waa kaaliye AI ah, la xidhiidh qareen rasmi ah wixii go'aan sharci ah.",
            "debug": error_msg if app.debug else None
        }), 500

@app.route('/', methods=['GET'])
def root():
    """Root endpoint with API information"""
    return jsonify({
        "service": "Somaliland Legal AI",
        "version": "2.0.0",
        "providers": {
            "groq": groq_client is not None,
            "huggingface": HF_HEADERS is not None
        },
        "endpoints": {
            "/ask": "POST - Ask legal questions",
            "/health": "GET - Health check",
            "/stats": "GET - Cache statistics"
        },
        "features": [
            "Multi-provider AI (Groq + HuggingFace)",
            "Response caching",
            "Input validation",
            "Automatic fallback"
        ]
    })

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "message": "Somaliland Legal AI backend wuu shaqaynayaa.",
        "version": "2.0.0",
        "providers": {
            "groq": "active" if groq_client else "disabled",
            "huggingface": "active" if HF_HEADERS else "disabled"
        }
    })

@app.route('/stats', methods=['GET'])
def stats():
    """Cache statistics endpoint"""
    clean_cache()
    return jsonify({
        "cache_size": len(question_cache),
        "cache_max_size": CACHE_MAX_SIZE,
        "cache_ttl_seconds": CACHE_TTL
    })

if __name__ == '__main__':
    logger.info(f"Starting Somaliland Legal AI v2.0.0 on port {PORT}")
    logger.info(f"Groq API: {'enabled' if groq_client else 'disabled'}")
    logger.info(f"Hugging Face API: {'enabled' if HF_HEADERS else 'disabled'}")
    app.run(host='0.0.0.0', port=PORT, debug=False)
