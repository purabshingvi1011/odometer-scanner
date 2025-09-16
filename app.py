import streamlit as st
import numpy as np
from PIL import Image
from datetime import datetime
import pandas as pd
import google.generativeai as genai

# Configure page for mobile optimization
st.set_page_config(
    page_title="Odometer Scanner",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for mobile optimization
st.markdown("""
<style>
    .stApp {
        max-width: 100%;
        padding: 1rem;
    }
    
    .main-header {
        text-align: center;
        color: #2E86AB;
        font-size: 2rem;
        margin-bottom: 1rem;
    }
    
    .scan-button {
        background-color: #2E86AB;
        color: white;
        padding: 1rem 2rem;
        border-radius: 10px;
        border: none;
        font-size: 1.2rem;
        width: 100%;
        margin: 1rem 0;
    }
    
    .result-box {
        background-color: #f0f8ff;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #2E86AB;
        margin: 1rem 0;
        color: #222;
    }
    
    .history-item {
        background-color: #f8f9fa;
        padding: 0.5rem;
        margin: 0.5rem 0;
        border-radius: 5px;
        border-left: 3px solid #28a745;
        color: #222;
    }
</style>
""", unsafe_allow_html=True)

def scan_odometer_with_gemini(image, api_key):
    """
    Uses Google Gemini to extract the odometer reading from an image.
    :param image: PIL Image object
    :param api_key: Your Gemini API key as a string
    :return: Extracted odometer reading as a string or None
    """
    import time
    import streamlit as st
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.5-flash')

    prompt = (
        "You are an assistant that extracts odometer readings from car dashboard images. "
        "Given the following image, return only the odometer value as a number (no extra text)."
    )

    start_time = time.time()
    response = model.generate_content(
        [prompt, image],
        stream=False
    )
    # Extract the number from the response
    if response and hasattr(response, 'text') and response.text:
        import re
        match = re.search(r'\d{3,7}', response.text.replace(',', ''))
        if match:
            return int(match.group())
        else:
            return response.text.strip()
    return None

def save_reading(odometer_reading, car_name=None, vin_number=None, timestamp=None, history_file="odometer_history.csv"):
    """Save reading to history CSV file with car_name and vin_number."""
    from datetime import datetime
    import pandas as pd
    import os
    import streamlit as st
    try:
        if timestamp is None:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new_entry = pd.DataFrame({
            'timestamp': [timestamp],
            'car_name': [car_name if car_name else ""],
            'vin_number': [vin_number if vin_number else ""],
            'odometer_reading': [odometer_reading]
        })
        abs_path = os.path.abspath(history_file)
        if os.path.exists(history_file):
            df = pd.read_csv(history_file)
            df = pd.concat([df, new_entry], ignore_index=True)
        else:
            df = new_entry
        df.to_csv(history_file, index=False)
    except Exception as e:
        st.error(f"[ERROR] Failed to save reading: {e}")


def get_history(history_file="odometer_history.csv"):
    import pandas as pd
    import os
    if os.path.exists(history_file):
        return pd.read_csv(history_file)
    return pd.DataFrame(columns=["timestamp", "car_name", "vin_number", "odometer_reading"])

def main():
    st.markdown('<h1 class="main-header">🚗 Odometer Scanner</h1>', unsafe_allow_html=True)
    
    # Create tabs
    tab1, tab2, tab3 = st.tabs(["📱 Scan", "📊 History", "ℹ️ Info"])
    
    with tab1:
        st.subheader("Scan Odometer Reading")
        
        # Camera input
        camera_input = st.camera_input("Take a photo of your odometer")
        
        # File uploader as alternative
        uploaded_file = st.file_uploader(
            "Or upload an image", 
            type=['png', 'jpg', 'jpeg'],
            help="Upload a clear photo of your odometer display"
        )
        
        # Process image
        image_to_process = camera_input or uploaded_file
        
        # Initialize session state for odometer reading
        if "odometer_reading" not in st.session_state:
            st.session_state["odometer_reading"] = None
        
        if image_to_process:
            # Display image
            image = Image.open(image_to_process)
            st.image(image, caption="Original Image", use_column_width=True)
            
            api_key = st.secrets["GEMINI_API_KEY"]
            if st.button("🔍 Scan Odometer", key="scan_gemini_btn"):
                if not api_key:
                    st.error("Gemini API key not found in secrets.toml.")
                else:
                    with st.spinner("Scanning..."):
                        reading = scan_odometer_with_gemini(image, api_key)
                        if reading:
                            st.session_state["odometer_reading"] = reading
                        else:
                            st.session_state["odometer_reading"] = None
                            st.error("❌ No odometer reading detected by Gemini. Please try with a clearer image.")
                            st.info("Tips: Ensure good lighting, focus on the odometer display, and avoid reflections.")
        # Show detected reading and input fields if reading is in session_state
        if st.session_state["odometer_reading"]:
            reading = st.session_state["odometer_reading"]
            st.markdown(f"""
            <div class="result-box">
                <h3>✅ Odometer Reading Detected!</h3>
                <h2 style="color: #2E86AB; font-size: 2.5rem;">{reading:,}</h2>
            </div>
            """, unsafe_allow_html=True)
            car_name = st.text_input("Car Name (optional)", key="car_name_input")
            vin_number = st.text_input("VIN Number (required)", key="vin_number_input")
            autopopulate_disabled = not vin_number.strip()
            if st.button("⚡ Autopopulate", disabled=autopopulate_disabled):
                save_reading(
                    odometer_reading=reading,
                    car_name=car_name,
                    vin_number=vin_number
                )
                st.success("Reading autopopulated and saved successfully!")
                st.session_state["odometer_reading"] = None
                st.rerun()
    
    with tab2:
        st.subheader("📊 Reading History")
        history_df = get_history()
        if not history_df.empty:
            # Sort by timestamp (newest first)
            history_df = history_df.sort_values('timestamp', ascending=False)
            # Display recent readings
            st.write("### Recent Readings")
            for _, row in history_df.head(10).iterrows():
                st.markdown(f"""
                <div class="history-item">
                    <strong>Odometer:</strong> {row['odometer_reading']:,} <br>
                    <strong>Car Name:</strong> {row['car_name']} <br>
                    <strong>VIN:</strong> {row['vin_number']} <br>
                    <strong>Time:</strong> {row['timestamp']}
                </div>
                """, unsafe_allow_html=True)
            # Statistics
            if len(history_df) > 1:
                st.write("### Statistics")
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total Readings", len(history_df))
                with col2:
                    latest_reading = history_df.iloc[0]['odometer_reading']
                    previous_reading = history_df.iloc[1]['odometer_reading'] if len(history_df) > 1 else latest_reading
                    try:
                        diff = int(latest_reading) - int(previous_reading)
                    except Exception:
                        diff = 0
                    st.metric("Latest Reading", f"{latest_reading:,}", f"{diff:,}")
                with col3:
                    try:
                        avg_reading = history_df['odometer_reading'].astype(float).mean()
                    except Exception:
                        avg_reading = 0
                    st.metric("Average Reading", f"{avg_reading:,.0f}")
            # Download history
            csv = history_df.to_csv(index=False)
            st.download_button(
                label="📥 Download History",
                data=csv,
                file_name="odometer_history.csv",
                mime="text/csv"
            )
            # Clear history
            import os
            if st.button("🗑️ Clear History"):
                if os.path.exists("odometer_history.csv"):
                    os.remove("odometer_history.csv")
                st.success("History cleared!")
                st.rerun()
        else:
            st.info("No readings saved yet. Scan your first odometer reading!")
    
    with tab3:
        st.subheader("ℹ️ How to Use")
        st.markdown("""
        ### 📱 Scanning Tips
        **For Best Results:**
        - 📸 Take a clear, well-lit photo
        - 🎯 Focus directly on the odometer display
        - 🔍 Ensure numbers are clearly visible
        - 💡 Avoid reflections and shadows
        - 📐 Hold the camera steady and level
        **Supported Formats:**
        - Digital odometer displays
        - Analog odometer readings
        - Various number formats (123,456 or 123456)
        ### 🚗 Common Use Cases
        - Vehicle maintenance tracking
        - Fuel efficiency monitoring
        - Service interval planning
        - Vehicle history documentation
        - Fleet management
        """)

if __name__ == "__main__":
    main()
