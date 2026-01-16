import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai

app = Flask(__name__)
CORS(app)

# 1. Habaynta Gemini
GEMINI_API_KEY = os.getenv("GOOGLE_API_KEY", "GELI_API_KEY_GAAGA_HALKAN")
if not GEMINI_API_KEY or GEMINI_API_KEY == "GELI_API_KEY_GAAGA_HALKAN":
    raise RuntimeError("GOOGLE_API_KEY environment variable-ka waa in la deji")

genai.configure(api_key=GEMINI_API_KEY)

# 2. Prompt-ka rasmiga ah (System Instruction)
SYSTEM_PROMPT = """
Waxaad tahay Kaaliye Sharci oo ku takhasusay Shuruucda Somaliland (Somaliland Legal AI). 
Shaqadaadu waa inaad ka jawaabto dacwadaha madaniga ah adigoo isticmaalaya shuruucda Somaliland.

Qawaaniinta aad raacayso:
1. Marka laguu soo diro su'aal, marka hore ka raadi xogta mareegta Somalilandlaw.com iyo ilaha rasmiga ah ee dawladda Somaliland.
2. Jawaabtaadu waa inay ahaataa mid naxariis leh, cad, oo ku qoran luuqadda Soomaaliga.
3. Mar walba tixraac qodobka xeerka aad u cuskatay jawaabta (Tusaale: Xeerka Madaniga, Qodobka 12aad).
4. Haddii su'aashu tahay mid u baahan qareen jidheed, ku tali in qofku la xidhiidho qareen sharciyeed oo ka diiwaangashan Somaliland.
5. Ha bixin talo ka baxsan sharciga Somaliland.
"""

@app.route('/ask', methods=['POST'])
def ask_legal_bot():
    data = request.json or {}
    user_question = data.get('question')

    if not user_question:
        return jsonify({"error": "Fadlan su'aal soo qor"}), 400

    try:
        # Isticmaalka Gemini oo leh awoodda raadinta (Tools: google_search)
        model = genai.GenerativeModel(
            model_name='gemini-1.5-flash',
        )
        
        # Isku darka Prompt-ka iyo su'aasha
        full_query = f"{SYSTEM_PROMPT}\n\nUser Question: {user_question}"
        
        response = model.generate_content(full_query)
        
        return jsonify({
            "answer": response.text,
            "disclaimer": "Xogtan waa kaaliye AI ah, la xidhiidh qareen rasmi ah wixii go'aan sharci ah."
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/', methods=['GET'])
def health():
    return jsonify({"status": "ok", "message": "Somaliland Legal AI backend wuu shaqaynayaa."})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 5000)))
