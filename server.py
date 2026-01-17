import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from groq import Groq

app = Flask(__name__)
CORS(app)

# Groq API Key
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
if not GROQ_API_KEY:
    raise RuntimeError("GROQ_API_KEY environment variable is required")

client = Groq(api_key=GROQ_API_KEY)

# System prompt for Somaliland Legal AI
SYSTEM_PROMPT = """Waxaad tahay Kaaliye Sharci oo ku takhasusay Shuruucda Somaliland (Somaliland Legal AI). 
Shaqadaadu waa inaad ka jawaabto dacwadaha madaniga ah adigoo isticmaalaya shuruucda Somaliland.
Qawaaniinta aad raacayso:
1. Marka laguu soo diro su'aal, marka hore ka raadi xogta mareegta Somalilandlaw.com iyo ilaha rasmiga ah ee dawladda Somaliland.
2. Jawaabtaadu waa inay ahaataa mid naxariis leh, cad, oo ku qoran luuqadda Soomaaliga.
3. Mar walba tixraac qodobka xeerka aad u cuskatay jawaabta (Tusaale: Xeerka Madaniga, Qodobka 12aad).
4. Haddii su'aashu tahay mid u baahan qareen jidheed, ku tali in qofku la xidhiidho qareen sharciyeed oo ka diiwaangashan Somaliland.
5. Ha bixin talo ka baxsan sharciga Somaliland."""

@app.route('/ask', methods=['POST'])
def ask_legal_bot():
    data = request.json or {}
    user_question = data.get('question')
    
    if not user_question:
        return jsonify({"error": "Fadlan su'aal soo qor"}), 400
    
    try:
        message = client.chat.completions.create(
            model="mixtral-8x7b-32768",
            max_tokens=1024,
                        messages=[
                                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_question}
            ]
        
        
        answer = message.choices[0].message.content if message.content else "Maleesh, wax waaye"
        
        return jsonify({
            "answer": answer,
            "disclaimer": "Xogtan waa kaaliye AI ah, la xidhiidh qareen rasmi ah wixii go'aan sharci ah."
        })
    
    except Exception as e:
        return jsonify({
            "error": str(e),
            "disclaimer": "Xogtan waa kaaliye AI ah, la xidhiidh qareen rasmi ah wixii go'aan sharci ah."
        }), 500

@app.route('/', methods=['GET'])
def health():
    return jsonify({
        "status": "ok",
        "message": "Somaliland Legal AI backend wuu shaqaynayaa."
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 5000)))
