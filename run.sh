cleanup() {
    echo "Stopping all services..."
    kill 0
}

trap cleanup SIGINT

echo "Installing Python dependencies..."
pip3 install -r requirements.txt

echo "Starting Chatbot..."
streamlit run chatbot.py