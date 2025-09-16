# 🚗 Odometer Scanner App

An intelligent mobile-friendly web application that automatically extracts odometer readings from car dashboard photos using AI. Perfect for fleet management, service centers, and individual vehicle maintenance tracking.

## ✨ Features

- **📸 Photo Capture**: Take photos directly with your device camera or upload existing images
- **🤖 AI-Powered Reading**: Uses Google Gemini Vision AI for accurate odometer reading extraction
- **📱 Mobile Optimized**: Works seamlessly on phones, tablets, and desktops
- **💾 Auto-Save**: Automatically saves readings with car name and VIN number to CSV
- **📊 History Tracking**: View and manage all your odometer readings in one place
- **📥 Export Data**: Download your odometer history as CSV files
- **🌐 Network Access**: Access the app from any device on your local network

## 🚀 Quick Start

### Prerequisites

- Python 3.7 or higher
- Google Gemini API key (required for AI functionality)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/purabshingvi1011/odometer-scanner.git
   cd odometer_scanner_app
   ```

2. **Install dependencies**
   ```bash
   pip install streamlit pillow google-generativeai pandas
   ```

3. **Set up your Gemini API key**
   
   Create a `secrets.toml` file in your project directory:
   ```toml
   GEMINI_API_KEY = "your_gemini_api_key_here"
   ```
   
   **How to get a Gemini API key:**
   - Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Sign in with your Google account
   - Click "Create API Key"
   - Copy the generated key and paste it in your `secrets.toml` file

4. **Run the application**
   ```bash
   streamlit run app.py
   ```

5. **Access the app**
   - **Local access**: Open `http://localhost:8501` in your browser
   - **Mobile access**: Run with `streamlit run app.py --server.address=0.0.0.0` and access via `http://YOUR_IP:8501`

## 📱 Mobile Usage

1. **Start the app** on your computer with network access enabled
2. **Find your computer's IP address**:
   - Mac/Linux: `ifconfig | grep inet`
   - Windows: `ipconfig`
3. **On your phone**, open a browser and go to `http://YOUR_IP:8501`
4. **Take photos** of odometers directly with your phone camera
5. **Enter car details** (name and VIN) and click "⚡ Autopopulate"

## 🎯 How It Works

1. **Capture**: Take a photo of the odometer display
2. **Scan**: Click "🔍 Scan Odometer" to process with AI
3. **Verify**: Review the detected reading
4. **Save**: Enter car name (optional) and VIN number, then click "⚡ Autopopulate"
5. **Track**: View all readings in the History tab

## 📊 Data Storage

- All readings are saved to `odometer_history.csv` with the following columns:
  - `timestamp`: Date and time of reading
  - `car_name`: Optional car identifier
  - `vin_number`: Vehicle identification number
  - `odometer_reading`: Extracted odometer value

## 🔧 Technical Details

- **Frontend**: Streamlit web framework
- **AI Engine**: Google Gemini 1.5 Flash Vision model
- **Image Processing**: PIL (Python Imaging Library)
- **Data Storage**: CSV files with pandas
- **OCR Fallback**: Tesseract OCR (for development/testing)

## 💡 Use Cases

- **Fleet Management**: Track mileage across multiple vehicles
- **Service Centers**: Quick odometer logging during maintenance
- **Personal Use**: Monitor your vehicle's mileage for maintenance schedules
- **Insurance**: Accurate mileage records for claims
- **Resale**: Maintain detailed vehicle history

## 🛠️ Troubleshooting

### Common Issues

1. **"Gemini API key not found"**
   - Ensure `secrets.toml` exists with your API key
   - Check that the key is valid and has proper permissions

2. **Slow scanning (30+ seconds)**
   - This is normal for Gemini API processing
   - Consider resizing images before upload for faster processing

3. **Mobile access shows "about:blank"**
   - Ensure both devices are on the same WiFi network
   - Start Streamlit with `--server.address=0.0.0.0`
   - Check firewall settings on your computer

4. **No readings detected**
   - Ensure good lighting and focus on the odometer
   - Avoid reflections and glare
   - Try different angles or distances

### Performance Tips

- **For faster processing**: Resize images to 800x600 pixels before scanning
- **For better accuracy**: Ensure clear, well-lit photos of the odometer display
- **For mobile use**: Use the camera capture feature for best results


## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📞 Support

If you encounter any issues or have questions, please open an issue in the repository.

---
