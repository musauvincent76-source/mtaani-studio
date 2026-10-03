# MTAANI STUDIO - Yako kama Frobits.app

1. Weka REPLICATE_TOKEN:
   - Nenda replicate.com -> Sign up -> API tokens -> Copy
   - Weka kwa Render.com env: REPLICATE_TOKEN=r8_xxx

2. Deploy backend:
   - Push kwa GitHub
   - Nenda render.com -> New Web Service -> Connect repo
   - Build: pip install -r requirements.txt
   - Start: python app.py

3. Badilisha API URL kwa index.html:
   const API = "https://mtaani-studio.onrender.com"

4. WhatsApp (hiari):
   - developers.facebook.com -> WhatsApp -> Get token
   - Weka WHATSAPP_TOKEN kwa Render

5. M-Pesa:
   - developer.safaricom.co.ke -> Daraja -> STK Push

DONE! Sasa uko na Frobits yako mwenyewe.
Kila mtu akituma "Nipe Kamba" WhatsApp, backend inatengeneza ngoma mpya na maelfu tofauti.
