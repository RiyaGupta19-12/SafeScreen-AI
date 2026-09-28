import streamlit as st
from PIL import Image
from ocr import extract_text
from detector import analyze_message
from ai_model import predict_phishing
from risk_engine import combined_risk

st.set_page_config(
    page_title="SafeScreen AI",
    page_icon="🛡️"
)

st.title("🛡️ SafeScreen AI")
st.write("Privacy-first AI assistant for analyzing suspicious messages.")

st.subheader("Upload a suspicious screenshot")

uploaded_file = st.file_uploader(
    "Choose a screenshot",
    type=["png", "jpg", "jpeg"]
)

if uploaded_file is not None:

    image = Image.open(uploaded_file)

    st.image(
        image,
        caption="Uploaded Screenshot",
        width="stretch"
    )

    st.success("Screenshot uploaded successfully! ✅")

    st.subheader("📝 Extracted Text")

    extracted_text = extract_text(image)

    if extracted_text.strip():

        st.text_area(
            "Text detected in the screenshot:",
            extracted_text,
            height=200
        )

        # Rule-based analysis
        risk, signals = analyze_message(extracted_text)

        # AI analysis
        prediction, safe_probability, phishing_probability = predict_phishing(
            extracted_text
        )
        final_risk = combined_risk(phishing_probability, risk)
        st.subheader("🤖 AI Analysis")
        st.write(
            f"Phishing probability: "
            f"**{phishing_probability * 100:.2f}%**"
        )
        st.progress(phishing_probability)
        st.write(
            f"Safe probability: "
            f"**{safe_probability * 100:.2f}%**"
        )
        st.progress(safe_probability)
        if prediction == "PHISHING":
            st.error("⚠️ AI Prediction: PHISHING")
        else:
            st.success("✅ AI Prediction: SAFE")
        st.subheader("🛡️ Overall Risk Summary")
        st.write(f"Overall Risk: {final_risk}")
        
        if final_risk == "HIGH":
            st.error("Do not click links, share OTPs/passwords, or make payments.")
        
        elif final_risk == "MEDIUM":
            st.warning("Be cautious and verify the source before taking any action.")
        
        else:
            st.success("No strong phishing signals were detected, but always stay vigilant.")
                      
        if signals:
            st.write("### 🔍 Why was this flagged?")

            for signal in signals:
                st.write("• " + signal)
        else:
            st.info("No obvious suspicious signals were detected.")

    else:
        st.warning("No text could be detected in this screenshot.")
   