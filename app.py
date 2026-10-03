from flask import Flask, request, jsonify
from flask_cors import CORS
import random, time, os

app = Flask(__name__)
CORS(app)

# --- CONFIG YAKO ---
# 1. Replicate API kwa Music (free credits) - weka key yako hapa
REPLICATE_TOKEN = os.getenv("REPLICATE_TOKEN", "r8_xxx_...weka_yako")
# 2. WhatsApp Cloud API
WHATSAPP_TOKEN = os.getenv("WHATSAPP_TOKEN", "weka_yako")
# 3. M-Pesa Daraja
MPESA_KEY = os.getenv("MPESA_KEY", "weka_yako")

# Memory ya ngoma zilizotengenezwa - maelfu
songs_db = {}

def make_kamba_prompt(vibe, genre, lang):
    # HII NDIO INAFANYA KILA NGOMA IWE TOFAUTI LAKINI MZURI KAMA VIDEO YAKO
    bass_patterns = ["G (98Hz) -> D (147Hz) Kativoi", "G -> C -> D", "G -> D -> A", "G -> B -> E"]
    solo_patterns = [
        "solo 0-2-4-6-7-6-4-2 Kativoi",
        "solo 2-4-6-7-9-7-6-4 with harmony",
        "solo 5-7-9-10-9-7-5-3 tweng tweng",
        "solo fast 0-2-4-7-9-12-9-7"
    ]
    bass = random.choice(bass_patterns)
    solo = random.choice(solo_patterns)
    seed = random.randint(1000,9999)

    prompt = f"""
    Kenyan {genre}, {bass}, {solo},
    90 BPM, Key G, Rhumba guitar picking,
    Language: {lang}, Lyrics theme: {vibe},
    Vocals: male lead + female chorus, field celebration vibe like Muchinah Motions,
    Original composition, no copyright, high quality
    ID: {seed}
    """
    return prompt.strip(), seed

@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    vibe = data.get('vibe','')
    genre = data.get('genre','Kamba Benga')
    lang = data.get('lang','Kikamba')

    prompt, seed = make_kamba_prompt(vibe, genre, lang)

    # --- HAPA NDIPO UNACALL AI YA KWELI ---
    # Option A: Replicate MusicGen
    # import replicate
    # output = replicate.run("meta/musicgen:...", input={"prompt": prompt, "duration": 30})
    # audio_url = output

    # Kwa sasa kwa demo bila API key, tunarudisha placeholder
    # Badilisha na audio halisi ukiweka REPLICATE_TOKEN

    song_id = seed
    title = f"Kamba Benga #{song_id} - {vibe[:30]}"
    # Hii itakuwa URL ya mp3 kutoka Replicate / S3 yako
    audio_url = f"https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3" # placeholder

    songs_db[song_id] = {"title": title, "prompt": prompt, "vibe": vibe}

    print(f"[{song_id}] GENERATED: {prompt}")

    return jsonify({
        "id": song_id,
        "title": title,
        "audio_url": audio_url,
        "prompt": prompt,
        "message": f"Ngoma #{song_id} tayari - {genre} na solo {prompt}"
    })

@app.route('/whatsapp', methods=['POST'])
def whatsapp_webhook():
    # WhatsApp Cloud API inatuma hapa
    body = request.json
    try:
        msg = body['entry'][0]['changes'][0]['value']['messages'][0]['text']['body']
        from_num = body['entry'][0]['changes'][0]['value']['messages'][0]['from']

        # Generate kama Frobits
        prompt, seed = make_kamba_prompt(msg, "Kamba Benga 90 BPM", "Kiswahili")

        # Jibu WhatsApp (unahitaji requests.post kwa graph.facebook.com)
        print(f"WhatsApp from {from_num}: {msg} -> Generating #{seed}")

        return jsonify({"status":"ok", "generated_id": seed})
    except Exception as e:
        return jsonify({"error": str(e)}), 200

@app.route('/pay', methods=['POST'])
def pay():
    data = request.json
    phone = data.get('phone')
    amount = data.get('amount', 100)
    # Hapa unaweka M-Pesa Daraja STK Push
    # requests.post("https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest",...)
    return jsonify({"message": f"STK Push imetumwa kwa {phone} - {amount} KES. Lipa upakue full song!"})

@app.route('/')
def home():
    return jsonify({"msg":"MTAANI STUDIO YAKO LIVE kama Frobits.app", "songs_generated": len(songs_db)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
