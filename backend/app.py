from flask import Flask, render_template, jsonify
import threading
import packet_capture

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/packets')
def get_packets():
    packets = packet_capture.get_captured_packets()  # Function to get packets from the capture
    return jsonify(packets)

if __name__ == '__main__':
    # Start packet capture in a separate thread
    
    capture_thread = threading.Thread(target=packet_capture.start_packet_capture, daemon=True)
    capture_thread.start()

    # Start Flask server
    app.run(debug=True, host='0.0.0.0')
