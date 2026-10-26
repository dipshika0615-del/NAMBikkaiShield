
import re
import streamlit as st

st.set_page_config(
    page_title="NAMBikkai Shield",
    page_icon="🛡️",
    layout="centered"
)

# ---------- Language translations ----------
TEXT = {
    "English": {
        "tagline": "Pause. Verify. Protect. Report.",
        "intro": "A digital safety assistant that checks messages for common scam warning signs.",
        "privacy": "Never enter real OTPs, passwords, PINs, or bank details.",
        "choose": "Choose your language",
        "calm": "Calm Help Mode (larger text and simpler guidance)",
        "paste": "Paste a suspicious message",
        "placeholder": "Example: Your account will be blocked. Share your OTP immediately.",
        "analyse": "Analyse message",
        "empty": "Please paste a message first.",
        "result": "Analysis result",
        "high": "High warning level",
        "medium": "Medium warning level",
        "low": "Low warning level",
        "disclaimer": "This rule-based score is not a probability or proof of fraud. A low score does not mean a message is safe.",
        "signs": "Warning signs detected",
        "none": "No known warning patterns were detected. This does not prove the message is safe.",
        "steps": "What should you do?",
        "pause": "PAUSE: Don't rush, click links, or send money.",
        "verify": "VERIFY: Contact the organisation using an independently verified phone number or website.",
        "protect": "PROTECT: Never share OTPs, passwords, or PINs.",
        "report": "REPORT: If you suspect cyber fraud in India, visit cybercrime.gov.in.",
        "rules": {
            "Urgency or threats": "The message may use fear or urgency to rush your decision.",
            "Sensitive information requests": "Never share OTPs, passwords, PINs, or verification codes.",
            "Payment pressure": "Verify any payment request independently before paying.",
            "Suspicious links": "Do not open unexpected links before checking them.",
            "Unexpected rewards": "Unexpected prizes may be used to trick you into paying or sharing information.",
            "Pressure to stay silent": "Ask a trusted person for help; scammers may discourage verification."
        }
    },
    "Malayalam": {
        "tagline": "നിർത്തുക. പരിശോധിക്കുക. സംരക്ഷിക്കുക. റിപ്പോർട്ട് ചെയ്യുക.",
        "intro": "സന്ദേശങ്ങളിലെ തട്ടിപ്പിന്റെ മുന്നറിയിപ്പ് സൂചനകൾ പരിശോധിക്കാൻ സഹായിക്കുന്ന ഡിജിറ്റൽ സുരക്ഷാ സഹായി.",
        "privacy": "യഥാർത്ഥ OTP, പാസ്‌വേഡ്, PIN, ബാങ്ക് വിവരങ്ങൾ എന്നിവ നൽകാതിരിക്കുക.",
        "choose": "ഭാഷ തിരഞ്ഞെടുക്കുക",
        "calm": "സഹായ മോഡ് — വലിയ അക്ഷരങ്ങളും ലളിതമായ നിർദേശങ്ങളും",
        "paste": "സംശയാസ്പദമായ സന്ദേശം ഇവിടെ ചേർക്കുക",
        "placeholder": "ഉദാഹരണം: നിങ്ങളുടെ അക്കൗണ്ട് തടയും. OTP ഉടൻ പങ്കിടുക.",
        "analyse": "സന്ദേശം പരിശോധിക്കുക",
        "empty": "ആദ്യം ഒരു സന്ദേശം ചേർക്കുക.",
        "result": "പരിശോധനാ ഫലം",
        "high": "ഉയർന്ന മുന്നറിയിപ്പ് നില",
        "medium": "മധ്യമ മുന്നറിയിപ്പ് നില",
        "low": "കുറഞ്ഞ മുന്നറിയിപ്പ് നില",
        "disclaimer": "ഈ നിയമാധിഷ്ഠിത സ്കോർ തട്ടിപ്പിന്റെ സാധ്യതയോ തെളിവോ അല്ല. കുറഞ്ഞ സ്കോർ സുരക്ഷിതമാണെന്ന് അർത്ഥമാക്കില്ല.",
        "signs": "കണ്ടെത്തിയ മുന്നറിയിപ്പുകൾ",
        "none": "അറിയാവുന്ന മുന്നറിയിപ്പ് സൂചനകൾ കണ്ടെത്തിയില്ല. അതിനാൽ സന്ദേശം സുരക്ഷിതമാണെന്ന് ഉറപ്പില്ല.",
        "steps": "ഇനി എന്ത് ചെയ്യണം?",
        "pause": "നിർത്തുക: തിരക്കിട്ട് പ്രവർത്തിക്കരുത്; ലിങ്ക് തുറക്കുകയോ പണം അയയ്ക്കുകയോ ചെയ്യരുത്.",
        "verify": "പരിശോധിക്കുക: ഔദ്യോഗികമായി സ്ഥിരീകരിച്ച നമ്പറിലൂടെയോ വെബ്സൈറ്റിലൂടെയോ ബന്ധപ്പെടുക.",
        "protect": "സംരക്ഷിക്കുക: OTP, പാസ്‌വേഡ്, PIN എന്നിവ പങ്കിടരുത്.",
        "report": "റിപ്പോർട്ട് ചെയ്യുക: cybercrime.gov.in സന്ദർശിക്കുക.",
        "rules": {
            "Urgency or threats": "ഭയമോ അടിയന്തരതയോ ഉപയോഗിച്ച് വേഗത്തിൽ തീരുമാനിപ്പിക്കാൻ ശ്രമിക്കാം.",
            "Sensitive information requests": "OTP, പാസ്‌വേഡ്, PIN എന്നിവ പങ്കിടരുത്.",
            "Payment pressure": "പണം നൽകുന്നതിന് മുമ്പ് സ്വതന്ത്രമായി പരിശോധിക്കുക.",
            "Suspicious links": "പരിശോധിക്കാത്ത ലിങ്കുകൾ തുറക്കരുത്.",
            "Unexpected rewards": "അപ്രതീക്ഷിത സമ്മാനങ്ങൾ വഴി വിവരങ്ങളോ പണമോ തട്ടിയെടുക്കാം.",
            "Pressure to stay silent": "വിശ്വസിക്കുന്ന ഒരാളോട് സഹായം ചോദിക്കുക."
        }
    },
    "Hindi": {
        "tagline": "रुकें। जाँचें। सुरक्षित रहें। रिपोर्ट करें।",
        "intro": "संदेशों में धोखाधड़ी के सामान्य संकेत पहचानने में मदद करने वाला डिजिटल सुरक्षा सहायक।",
        "privacy": "असली OTP, पासवर्ड, PIN या बैंक विवरण दर्ज न करें।",
        "choose": "अपनी भाषा चुनें",
        "calm": "आसान सहायता मोड — बड़े अक्षर और सरल निर्देश",
        "paste": "संदिग्ध संदेश यहाँ डालें",
        "placeholder": "उदाहरण: आपका खाता बंद हो जाएगा। तुरंत OTP साझा करें।",
        "analyse": "संदेश की जाँच करें",
        "empty": "पहले कोई संदेश डालें।",
        "result": "जाँच का परिणाम",
        "high": "उच्च चेतावनी स्तर",
        "medium": "मध्यम चेतावनी स्तर",
        "low": "कम चेतावनी स्तर",
        "disclaimer": "यह नियम-आधारित स्कोर धोखाधड़ी की संभावना या प्रमाण नहीं है। कम स्कोर का मतलब सुरक्षित होना नहीं है।",
        "signs": "पहचाने गए चेतावनी संकेत",
        "none": "कोई ज्ञात चेतावनी संकेत नहीं मिला। इससे संदेश सुरक्षित साबित नहीं होता।",
        "steps": "अब क्या करें?",
        "pause": "रुकें: जल्दबाज़ी न करें, लिंक न खोलें और पैसे न भेजें।",
        "verify": "जाँचें: आधिकारिक रूप से सत्यापित नंबर या वेबसाइट से संपर्क करें।",
        "protect": "सुरक्षित रहें: OTP, पासवर्ड या PIN साझा न करें।",
        "report": "रिपोर्ट करें: cybercrime.gov.in पर जाएँ।",
        "rules": {
            "Urgency or threats": "डर या जल्दबाज़ी पैदा करके निर्णय करवाने की कोशिश हो सकती है।",
            "Sensitive information requests": "OTP, पासवर्ड, PIN या सत्यापन कोड साझा न करें।",
            "Payment pressure": "भुगतान से पहले स्वतंत्र रूप से जाँचें।",
            "Suspicious links": "अचानक आए लिंक खोलने से पहले जाँचें।",
            "Unexpected rewards": "इनाम के नाम पर पैसे या निजी जानकारी माँगी जा सकती है।",
            "Pressure to stay silent": "किसी भरोसेमंद व्यक्ति से मदद लें।"
        }
    },
    "Tamil": {
        "tagline": "நிறுத்துங்கள். சரிபாருங்கள். பாதுகாப்பாக இருங்கள். புகாரளியுங்கள்.",
        "intro": "செய்திகளில் உள்ள மோசடி எச்சரிக்கை அறிகுறிகளை கண்டறிய உதவும் டிஜிட்டல் பாதுகாப்பு உதவியாளர்.",
        "privacy": "உண்மையான OTP, கடவுச்சொல், PIN அல்லது வங்கி விவரங்களை உள்ளிட வேண்டாம்.",
        "choose": "உங்கள் மொழியைத் தேர்ந்தெடுக்கவும்",
        "calm": "எளிய உதவி முறை — பெரிய எழுத்துகள் மற்றும் எளிய வழிமுறைகள்",
        "paste": "சந்தேகமான செய்தியை இங்கே ஒட்டவும்",
        "placeholder": "எடுத்துக்காட்டு: உங்கள் கணக்கு முடக்கப்படும். உடனே OTP பகிரவும்.",
        "analyse": "செய்தியைச் சரிபார்க்கவும்",
        "empty": "முதலில் ஒரு செய்தியை ஒட்டவும்.",
        "result": "சரிபார்ப்பு முடிவு",
        "high": "அதிக எச்சரிக்கை நிலை",
        "medium": "நடுத்தர எச்சரிக்கை நிலை",
        "low": "குறைந்த எச்சரிக்கை நிலை",
        "disclaimer": "இந்த விதி அடிப்படையிலான மதிப்பெண் மோசடி நிகழ்தகவு அல்லது ஆதாரம் அல்ல. குறைந்த மதிப்பெண் பாதுகாப்பானது என்று பொருளல்ல.",
        "signs": "கண்டறியப்பட்ட எச்சரிக்கை அறிகுறிகள்",
        "none": "அறியப்பட்ட எச்சரிக்கை அறிகுறிகள் கண்டறியப்படவில்லை. அதனால் செய்தி பாதுகாப்பானது என உறுதி செய்ய முடியாது.",
        "steps": "இப்போது என்ன செய்ய வேண்டும்?",
        "pause": "நிறுத்துங்கள்: அவசரப்பட வேண்டாம்; இணைப்புகளைத் திறக்கவோ பணம் அனுப்பவோ வேண்டாம்.",
        "verify": "சரிபாருங்கள்: அதிகாரப்பூர்வமாக உறுதிப்படுத்திய எண் அல்லது இணையதளம் மூலம் தொடர்புகொள்ளுங்கள்.",
        "protect": "பாதுகாக்கவும்: OTP, கடவுச்சொல் அல்லது PIN பகிர வேண்டாம்.",
        "report": "புகாரளியுங்கள்: cybercrime.gov.in இணையதளத்தைப் பார்வையிடுங்கள்.",
        "rules": {
            "Urgency or threats": "பயம் அல்லது அவசரத்தை உருவாக்கி உடனடியாக முடிவெடுக்க வைக்கலாம்.",
            "Sensitive information requests": "OTP, கடவுச்சொல், PIN அல்லது சரிபார்ப்புக் குறியீட்டைப் பகிர வேண்டாம்.",
            "Payment pressure": "பணம் செலுத்துவதற்கு முன் தனியாகச் சரிபாருங்கள்.",
            "Suspicious links": "எதிர்பாராத இணைப்புகளைத் திறப்பதற்கு முன் சரிபாருங்கள்.",
            "Unexpected rewards": "பரிசு என்ற பெயரில் பணம் அல்லது தனிப்பட்ட தகவல்களைக் கேட்கலாம்.",
            "Pressure to stay silent": "நம்பகமான ஒருவரிடம் உதவி கேளுங்கள்."
        }
    }
}

# English detection rules are used for this first multilingual version.

RULES = {
    "Urgency or threats": [
        # English
        r"\burgent\b",
        r"\bimmediately\b",
        r"\baccount.{0,30}(blocked|suspended|frozen)\b",
        r"\bdigital arrest\b",
        r"\blegal action\b",
        # Malayalam
        r"അടിയന്തിരം",
        r"ഉടൻ.{0,30}(ബ്ലോക്ക്|അടയ്ക്ക|നടപടി)",
        r"അക്കൗണ്ട്.{0,30}(ബ്ലോക്ക്|തടയ|മുടക്ക)",
        r"നിയമനടപടി",
        # Hindi
        r"तुरंत",
        r"तत्काल",
        r"खाता.{0,30}(बंद|ब्लॉक|बन्द)",
        r"कानूनी कार्रवाई",
        # Tamil
        r"உடனடியாக",
        r"உடனே",
        r"கணக்கு.{0,30}(முடக்க|நிறுத்த|மூட)",
        r"சட்ட நடவடிக்கை"
    ],

    "Sensitive information requests": [
        # English
        r"\botp\b",
        r"\bpassword\b",
        r"\bpin number\b",
        r"\bverification code\b",
        r"\bshare.{0,30}\botp\b",
        # Malayalam
        r"ഒടിപി",
        r"പാസ്.?വേഡ്",
        r"പിൻ നമ്പർ",
        r"രഹസ്യ കോഡ്",
        r"പങ്കിടുക",
        # Hindi
        r"ओटीपी",
        r"पासवर्ड",
        r"पिन नंबर",
        r"सत्यापन कोड",
        r"साझा करें",
        # Tamil
        r"ஓடிபி",
        r"கடவுச்சொல்",
        r"பின் எண்",
        r"சரிபார்ப்பு குறியீடு",
        r"பகிரவும்"
    ],

    "Payment pressure": [
        # English
        r"\bpay now\b",
        r"\bpay immediately\b",
        r"\btransfer money\b",
        r"\bpayment required\b",
        r"\bpay the fee\b",
        # Malayalam
        r"പണം അടയ്ക്കുക",
        r"ഫീസ് അടയ്ക്കുക",
        r"പണം അയയ്ക്കുക",
        r"പണമടയ്ക്കണം",
        # Hindi
        r"पैसे भेजें",
        r"अभी भुगतान करें",
        r"फीस जमा करें",
        r"पैसे जमा करें",
        # Tamil
        r"பணம் செலுத்துங்கள்",
        r"கட்டணம் செலுத்துங்கள்",
        r"பணம் அனுப்புங்கள்",
        r"உடனே செலுத்துங்கள்"
    ],

    "Suspicious links": [
        r"https?://\S+",
        r"\bbit\.ly/\S+",
        r"\btinyurl\.com/\S+",
        r"இணைப்பை.{0,20}(கிளிக்|திற)",
        r"लिंक पर क्लिक",
        r"लिंक खोलें",
        r"ലിങ്ക്.{0,20}(തുറക്കുക|ക്ലിക്ക്)"
    ],

    "Unexpected rewards": [
        # English
        r"\byou have won\b",
        r"\bclaim your prize\b",
        r"\blottery winner\b",
        r"\bfree reward\b",
        # Malayalam
        r"സമ്മാനം ലഭിച്ചു",
        r"നിങ്ങൾ വിജയിച്ചു",
        r"ലോട്ടറി സമ്മാനം",
        # Hindi
        r"आप जीत गए",
        r"इनाम मिला",
        r"लॉटरी में जीत",
        r"पुरस्कार प्राप्त",
        # Tamil
        r"பரிசு கிடைத்தது",
        r"நீங்கள் வென்றுள்ளீர்கள்",
        r"லாட்டரியில் வெற்றி"
    ],

    "Pressure to stay silent": [
        # English
        r"\bdon't tell anyone\b",
        r"\bdo not tell anyone\b",
        r"\bkeep this secret\b",
        r"\bdon't disconnect\b",
        # Malayalam
        r"ആരോടും പറയരുത്",
        r"രഹസ്യമായി വെക്കുക",
        r"ആരോടും പങ്കിടരുത്",
        # Hindi
        r"किसी को मत बताएं",
        r"किसी को मत बताइए",
        r"गुप्त रखें",
        # Tamil
        r"யாரிடமும் சொல்லாதீர்கள்",
        r"ரகசியமாக வைத்திருங்கள்",
        r"யாரிடமும் பகிர வேண்டாம்"
    ]
}


st.markdown("""
<style>
.stApp { background: linear-gradient(135deg, #0b1228, #142344); }
div.stButton > button {
    background-color: #39dcbf;
    color: #0b1228;
    border-radius: 10px;
    font-weight: bold;
    min-height: 44px;
}
</style>
""", unsafe_allow_html=True)

st.title("🛡️ NAMBikkai Shield")

language = st.selectbox(
    "Choose your language / மொழியைத் தேர்ந்தெடுக்கவும்",
    list(TEXT.keys())
)

t = TEXT[language]

calm_mode = st.toggle(t["calm"], value=False)

if calm_mode:
    st.markdown(
        "<style>html, body, [data-testid='stAppViewContainer'] "
        "{font-size: 1.25rem !important;} "
        "[data-testid='stMarkdownContainer'] p, "
        "[data-testid='stWidgetLabel'] p {font-size: 1.25rem !important;}"
        "</style>",
        unsafe_allow_html=True
    )

st.subheader(t["tagline"])
st.write(t["intro"])
st.info(t["privacy"])

message = st.text_area(
    t["paste"],
    height=200 if calm_mode else 160,
    placeholder=t["placeholder"]
)

if st.button(t["analyse"], use_container_width=True):
    if not message.strip():
        st.warning(t["empty"])
    else:
        findings = []
        for category, patterns in RULES.items():
            if any(re.search(pattern, message, re.IGNORECASE) for pattern in patterns):
                findings.append(category)

        score = min(len(findings) * 2, 10)

        st.divider()
        st.subheader(t["result"])

        if score >= 6:
            st.error(f"{t['high']} — {score}/10")
        elif score >= 2:
            st.warning(f"{t['medium']} — {score}/10")
        else:
            st.success(f"{t['low']} — {score}/10")

        st.caption(t["disclaimer"])
        st.subheader(t["signs"])

        if findings:
            for finding in findings:
                st.markdown(f"⚠️ **{finding}**")
                st.write(t["rules"][finding])
        else:
            st.write(t["none"])

        st.subheader(t["steps"])
        st.markdown(f"""
        1. **{t['pause']}**
        2. **{t['verify']}**
        3. **{t['protect']}**
        4. **{t['report']}**
        """)

        st.link_button(
            "Open official cybercrime reporting portal",
            "https://www.cybercrime.gov.in/",
            use_container_width=True
        )

st.divider()
st.caption("NAMBikkai Shield • Prototype v0.2")


# ---------- Scam-Pressure Simulator ----------
st.divider()
st.header("🎭 Scam-Pressure Simulator")

SIMULATOR = {
    "English": {
        "intro": "Practise how to respond to a fictional scam attempt. No real personal information is needed.",
        "scenario": "Scenario: A caller claims to be from your bank and says your account will be blocked unless you share an OTP immediately.",
        "question": "What would you do?",
        "choices": [
            "A. Share the OTP to prevent the account from being blocked",
            "B. End the call and contact the bank using its verified official number",
            "C. Ask the caller to send a link and enter my details there"
        ],
        "answer": "B. End the call and contact the bank using its verified official number",
        "correct": "Correct! Ending the call and independently contacting your bank is the safer choice. Never share an OTP with a caller.",
        "wrong": "That choice is risky. Never share an OTP or use a link supplied by a suspicious caller. End the call and contact the bank through a verified channel.",
        "button": "Check my answer",
        "lesson": "Remember: Pause. Verify. Protect. Report."
    },
    "Malayalam": {
        "intro": "ഒരു സാങ്കൽപ്പിക തട്ടിപ്പ് സാഹചര്യം എങ്ങനെ കൈകാര്യം ചെയ്യണമെന്ന് പരിശീലിക്കാം. യഥാർത്ഥ വ്യക്തിഗത വിവരങ്ങൾ ആവശ്യമില്ല.",
        "scenario": "സാഹചര്യം: നിങ്ങളുടെ ബാങ്കിൽ നിന്നാണെന്ന് പറഞ്ഞ് ഒരാൾ വിളിക്കുന്നു. ഉടൻ OTP നൽകിയില്ലെങ്കിൽ അക്കൗണ്ട് ബ്ലോക്ക് ചെയ്യുമെന്ന് പറയുന്നു.",
        "question": "നിങ്ങൾ എന്ത് ചെയ്യും?",
        "choices": [
            "A. അക്കൗണ്ട് ബ്ലോക്ക് ചെയ്യാതിരിക്കാൻ OTP നൽകും",
            "B. കോൾ അവസാനിപ്പിച്ച് ഔദ്യോഗികമായി സ്ഥിരീകരിച്ച ബാങ്ക് നമ്പറിൽ ബന്ധപ്പെടും",
            "C. വിളിച്ചയാളോട് ലിങ്ക് അയയ്ക്കാൻ പറഞ്ഞ് അതിൽ വിവരങ്ങൾ നൽകും"
        ],
        "answer": "B. കോൾ അവസാനിപ്പിച്ച് ഔദ്യോഗികമായി സ്ഥിരീകരിച്ച ബാങ്ക് നമ്പറിൽ ബന്ധപ്പെടും",
        "correct": "ശരി! കോൾ അവസാനിപ്പിച്ച് ബാങ്കുമായി സ്വതന്ത്രമായി ബന്ധപ്പെടുന്നതാണ് സുരക്ഷിതം. വിളിക്കുന്നയാളോട് OTP പങ്കിടരുത്.",
        "wrong": "ഈ തിരഞ്ഞെടുപ്പ് അപകടകരമാണ്. OTP പങ്കിടരുത്; സംശയകരമായ ലിങ്കുകൾ ഉപയോഗിക്കരുത്. കോൾ അവസാനിപ്പിച്ച് സ്ഥിരീകരിച്ച മാർഗത്തിലൂടെ ബാങ്കുമായി ബന്ധപ്പെടുക.",
        "button": "എന്റെ ഉത്തരം പരിശോധിക്കുക",
        "lesson": "ഓർക്കുക: നിർത്തുക. പരിശോധിക്കുക. സംരക്ഷിക്കുക. റിപ്പോർട്ട് ചെയ്യുക."
    },
    "Hindi": {
        "intro": "एक काल्पनिक धोखाधड़ी की स्थिति में सुरक्षित प्रतिक्रिया देने का अभ्यास करें। किसी वास्तविक निजी जानकारी की ज़रूरत नहीं है।",
        "scenario": "स्थिति: एक व्यक्ति बैंक से होने का दावा करता है और कहता है कि तुरंत OTP नहीं दिया तो आपका खाता बंद हो जाएगा।",
        "question": "आप क्या करेंगे?",
        "choices": [
            "A. खाता बंद होने से बचाने के लिए OTP साझा करूँगा",
            "B. कॉल काटकर बैंक के सत्यापित आधिकारिक नंबर पर संपर्क करूँगा",
            "C. कॉल करने वाले से लिंक मँगाकर उसमें अपनी जानकारी भरूँगा"
        ],
        "answer": "B. कॉल काटकर बैंक के सत्यापित आधिकारिक नंबर पर संपर्क करूँगा",
        "correct": "सही! कॉल काटकर बैंक से स्वतंत्र रूप से संपर्क करना अधिक सुरक्षित है। कॉल करने वाले को OTP कभी न बताएँ।",
        "wrong": "यह विकल्प जोखिम भरा है। OTP साझा न करें और संदिग्ध लिंक का उपयोग न करें। कॉल काटकर सत्यापित माध्यम से बैंक से संपर्क करें।",
        "button": "मेरा उत्तर जाँचें",
        "lesson": "याद रखें: रुकें। जाँचें। सुरक्षित रहें। रिपोर्ट करें।"
    },
    "Tamil": {
        "intro": "கற்பனையான மோசடி சூழ்நிலையை எவ்வாறு பாதுகாப்பாக கையாள்வது என்று பயிற்சி செய்யுங்கள். உண்மையான தனிப்பட்ட தகவல்கள் தேவையில்லை.",
        "scenario": "சூழ்நிலை: வங்கியிலிருந்து பேசுவதாக ஒருவர் கூறுகிறார். உடனே OTP பகிராவிட்டால் உங்கள் கணக்கு முடக்கப்படும் என்கிறார்.",
        "question": "நீங்கள் என்ன செய்வீர்கள்?",
        "choices": [
            "A. கணக்கு முடங்காமல் இருக்க OTP பகிர்வேன்",
            "B. அழைப்பைத் துண்டித்து, சரிபார்க்கப்பட்ட அதிகாரப்பூர்வ வங்கி எண்ணைத் தொடர்புகொள்வேன்",
            "C. அழைத்தவரிடம் இணைப்பைக் கேட்டு அதில் என் விவரங்களை உள்ளிடுவேன்"
        ],
        "answer": "B. அழைப்பைத் துண்டித்து, சரிபார்க்கப்பட்ட அதிகாரப்பூர்வ வங்கி எண்ணைத் தொடர்புகொள்வேன்",
        "correct": "சரி! அழைப்பைத் துண்டித்து வங்கியைத் தனியாகத் தொடர்புகொள்வதே பாதுகாப்பானது. அழைப்பவரிடம் OTP பகிர வேண்டாம்.",
        "wrong": "இந்தத் தேர்வு ஆபத்தானது. OTP பகிர வேண்டாம்; சந்தேகமான இணைப்புகளைப் பயன்படுத்த வேண்டாம். அழைப்பைத் துண்டித்து சரிபார்க்கப்பட்ட வழியில் வங்கியைத் தொடர்புகொள்ளுங்கள்.",
        "button": "என் பதிலைச் சரிபார்க்கவும்",
        "lesson": "நினைவில் கொள்ளுங்கள்: நிறுத்துங்கள். சரிபாருங்கள். பாதுகாப்பாக இருங்கள். புகாரளியுங்கள்."
    }
}

sim = SIMULATOR[language]

st.write(sim["intro"])
st.info(sim["scenario"])
st.write(f"**{sim['question']}**")

selected_choice = st.radio(
    "Choose one response:",
    sim["choices"],
    index=None,
    key="simulator_choice"
)

if st.button(sim["button"], key="check_simulator"):
    if selected_choice is None:
        st.warning("Please choose an answer first.")
    elif selected_choice == sim["answer"]:
        st.success(sim["correct"])
    else:
        st.error(sim["wrong"])

    st.markdown(f"**{sim['lesson']}**")

    
# ---------- Evidence-Organising Guidance ----------
st.divider()
st.header("🗂️ Evidence-Organising Guidance")

EVIDENCE_TEXT = {
    "English": {
        "intro": "If you suspect a scam, use this checklist to organise information before making a report.",
        "warning": "Do not enter OTPs, passwords, PINs, full bank details, or other sensitive personal information into this app.",
        "items": [
            "Save a screenshot of the suspicious message.",
            "Keep the original message, email, or call details if available.",
            "Note the date and approximate time of the incident.",
            "Keep transaction receipts or reference numbers, if money was sent.",
            "Save relevant links without opening them.",
            "Keep any complaint or acknowledgement number after reporting."
        ],
        "next": "If money has been lost in India, contact your bank immediately and report cyber financial fraud through 1930 or the official cybercrime portal.",
        "button": "Prepare my checklist",
        "download": "Download checklist",
        "result": "Your evidence checklist",
        "none": "Select at least one item to prepare your checklist."
    },
    "Malayalam": {
        "intro": "തട്ടിപ്പ് സംശയിക്കുന്നുവെങ്കിൽ റിപ്പോർട്ട് ചെയ്യുന്നതിന് മുമ്പ് വിവരങ്ങൾ ക്രമീകരിക്കാൻ ഈ പട്ടിക ഉപയോഗിക്കുക.",
        "warning": "OTP, പാസ്‌വേഡ്, PIN, ബാങ്ക് വിവരങ്ങൾ, മറ്റ് രഹസ്യ വിവരങ്ങൾ എന്നിവ ഇവിടെ നൽകാതിരിക്കുക.",
        "items": [
            "സംശയകരമായ സന്ദേശത്തിന്റെ സ്ക്രീൻഷോട്ട് സൂക്ഷിക്കുക.",
            "സന്ദേശം, ഇമെയിൽ, അല്ലെങ്കിൽ കോൾ വിവരങ്ങൾ ലഭ്യമെങ്കിൽ സൂക്ഷിക്കുക.",
            "സംഭവത്തിന്റെ തീയതിയും ഏകദേശ സമയവും കുറിക്കുക.",
            "പണം അയച്ചിട്ടുണ്ടെങ്കിൽ ഇടപാട് രസീതോ റഫറൻസ് നമ്പറോ സൂക്ഷിക്കുക.",
            "സംശയകരമായ ലിങ്കുകൾ തുറക്കാതെ അവയുടെ വിവരങ്ങൾ സൂക്ഷിക്കുക.",
            "പരാതി നൽകിയ ശേഷം ലഭിക്കുന്ന നമ്പർ സൂക്ഷിക്കുക."
        ],
        "next": "ഇന്ത്യയിൽ പണം നഷ്ടപ്പെട്ടാൽ ഉടൻ ബാങ്കുമായി ബന്ധപ്പെടുക. 1930 എന്ന നമ്പറിലോ ഔദ്യോഗിക സൈബർ ക്രൈം പോർട്ടലിലോ റിപ്പോർട്ട് ചെയ്യുക.",
        "button": "ചെക്ക്ലിസ്റ്റ് തയ്യാറാക്കുക",
        "download": "ചെക്ക്ലിസ്റ്റ് ഡൗൺലോഡ് ചെയ്യുക",
        "result": "നിങ്ങളുടെ തെളിവ് ചെക്ക്ലിസ്റ്റ്",
        "none": "ചെക്ക്ലിസ്റ്റ് തയ്യാറാക്കാൻ കുറഞ്ഞത് ഒരു ഇനം തിരഞ്ഞെടുക്കുക."
    },
    "Hindi": {
        "intro": "यदि आपको धोखाधड़ी का संदेह है, तो शिकायत करने से पहले जानकारी व्यवस्थित करने के लिए इस सूची का उपयोग करें।",
        "warning": "इस ऐप में OTP, पासवर्ड, PIN, बैंक विवरण या अन्य संवेदनशील निजी जानकारी न डालें।",
        "items": [
            "संदिग्ध संदेश का स्क्रीनशॉट सुरक्षित रखें।",
            "मूल संदेश, ईमेल या कॉल की जानकारी उपलब्ध हो तो सुरक्षित रखें।",
            "घटना की तारीख और अनुमानित समय लिख लें।",
            "पैसे भेजे हों तो रसीद या लेन-देन संदर्भ संख्या सुरक्षित रखें।",
            "संदिग्ध लिंक खोले बिना उसका विवरण सुरक्षित रखें।",
            "शिकायत करने के बाद प्राप्त शिकायत संख्या सुरक्षित रखें।"
        ],
        "next": "भारत में पैसे का नुकसान हुआ हो तो तुरंत अपने बैंक से संपर्क करें और 1930 या आधिकारिक साइबर अपराध पोर्टल पर रिपोर्ट करें।",
        "button": "चेकलिस्ट तैयार करें",
        "download": "चेकलिस्ट डाउनलोड करें",
        "result": "आपकी साक्ष्य चेकलिस्ट",
        "none": "चेकलिस्ट बनाने के लिए कम से कम एक विकल्प चुनें।"
    },
    "Tamil": {
        "intro": "மோசடி நடந்திருக்கலாம் எனச் சந்தேகித்தால், புகார் அளிப்பதற்கு முன் தகவல்களை ஒழுங்குபடுத்த இந்தப் பட்டியலைப் பயன்படுத்துங்கள்.",
        "warning": "OTP, கடவுச்சொல், PIN, வங்கி விவரங்கள் அல்லது பிற ரகசியத் தனிப்பட்ட தகவல்களை இந்தச் செயலியில் உள்ளிட வேண்டாம்.",
        "items": [
            "சந்தேகமான செய்தியின் ஸ்கிரீன்ஷாட்டைச் சேமிக்கவும்.",
            "அசல் செய்தி, மின்னஞ்சல் அல்லது அழைப்பு விவரங்கள் இருந்தால் பாதுகாக்கவும்.",
            "சம்பவத்தின் தேதி மற்றும் தோராயமான நேரத்தைக் குறிக்கவும்.",
            "பணம் அனுப்பியிருந்தால் ரசீது அல்லது பரிவர்த்தனை குறிப்பு எண்ணைச் சேமிக்கவும்.",
            "சந்தேகமான இணைப்புகளைத் திறக்காமல் அவற்றின் விவரங்களைச் சேமிக்கவும்.",
            "புகார் அளித்த பிறகு கிடைக்கும் புகார் எண்ணைப் பாதுகாக்கவும்."
        ],
        "next": "இந்தியாவில் பண இழப்பு ஏற்பட்டால் உடனே உங்கள் வங்கியைத் தொடர்புகொண்டு 1930 என்ற எண்ணிலோ அதிகாரப்பூர்வ சைபர் குற்ற இணையதளத்திலோ புகார் அளிக்கவும்.",
        "button": "சரிபார்ப்புப் பட்டியலைத் தயாரிக்கவும்",
        "download": "பட்டியலைப் பதிவிறக்கவும்",
        "result": "உங்கள் ஆதாரப் பட்டியல்",
        "none": "பட்டியலைத் தயாரிக்க குறைந்தது ஒரு உருப்படியையாவது தேர்வு செய்யவும்."
    }
}

ev = EVIDENCE_TEXT.get(language, EVIDENCE_TEXT["English"])

st.write(ev["intro"])
st.warning(ev["warning"])

evidence_selected = []

for i, item in enumerate(ev["items"]):
    if st.checkbox(item, key=f"evidence_item_{i}"):
        evidence_selected.append(item)

if st.button(ev["button"], key="prepare_evidence_checklist"):
    if evidence_selected:
        st.subheader(ev["result"])
        checklist_text = ev["result"] + "\n\n"
        for item in evidence_selected:
            st.write(f"✅ {item}")
            checklist_text += f"[x] {item}\n"

        st.download_button(
            label=ev["download"],
            data=checklist_text,
            file_name="NAMBikkaiShield_evidence_checklist.txt",
            mime="text/plain",
            key="download_evidence_checklist"
        )
    else:
        st.info(ev["none"])

st.info(ev["next"])
st.caption(
    "Safety note: This feature creates a checklist only. "
    "It does not verify evidence or submit a police complaint."
)


