import scapy.all as scapy
from keras._tf_keras.keras.models import load_model
import pandas as pd
import numpy as np
import pickle
import socket

# Load the trained model
model = load_model('backend/model/model.h5')
captured_packets=[]
# Load the scaler
try:
    with open('backend/model/scaler.pkl', 'rb') as file:
        scaler = pickle.load(file)
    # Check the type of the loaded scaler
    if not hasattr(scaler, 'transform'):
        raise TypeError("Loaded scaler does not have 'transform' method.")
except Exception as e:
    print(f"Error loading scaler: {e}")
    exit(1)

def extract_features(packet):
    features = {}
    features['length'] = len(packet)
    if scapy.IP in packet:
        features['src_ip'] = str(packet[scapy.IP].src)
        features['dst_ip'] = str(packet[scapy.IP].dst)
        features['protocol'] = packet[scapy.IP].proto
    else:
        features['src_ip'] = '0.0.0.0'
        features['dst_ip'] = '0.0.0.0'
        features['protocol'] = 0
    
    if scapy.TCP in packet:
        features['src_port'] = packet[scapy.TCP].sport
        features['dst_port'] = packet[scapy.TCP].dport
        features['flags'] = str(packet[scapy.TCP].flags)
    else:
        features['src_port'] = 0
        features['dst_port'] = 0
        features['flags'] = 'NA'

    return features

def process_packet(packet):
    features = extract_features(packet)
    df = pd.DataFrame([features])
    df.fillna(0, inplace=True)

    # Convert IP addresses to numerical format
    def ip_to_int(ip):
        return int.from_bytes(socket.inet_aton(ip), 'big')

    df['src_ip'] = df['src_ip'].apply(ip_to_int)
    df['dst_ip'] = df['dst_ip'].apply(ip_to_int)

    # Encode flags as categorical or numerical
    df['flags'] = df['flags'].astype(str)  # Ensure all are strings

    # Convert all features to numeric, handling non-numeric values
    df = df.apply(pd.to_numeric, errors='coerce')  # Convert to numeric, replacing errors with NaN
    df.fillna(0, inplace=True)  # Replace NaNs with 0

    try:
        # Scale features
        df_scaled = scaler.transform(df)
    except AttributeError:
        print("Error: Scaler object does not have 'transform' method.")
        return
    except Exception as e:
        print(f"Error scaling features: {e}")
        return

    # Predict with the model
    prediction = model.predict(df_scaled)
    
    # Get the prediction result
    result = "Malicious" if prediction[0] > 0.5 else "Normal"
    captured_packets.append({
        "info": features,
        "classification": result
    })
    # Display detailed packet information and classification
    print(f"Packet Info: Length={features['length']}, Src IP={features['src_ip']}, "
          f"Dst IP={features['dst_ip']}, Protocol={features['protocol']}, "
          f"Src Port={features['src_port']}, Dst Port={features['dst_port']}, "
          f"Flags={features['flags']}")
    print(f"Classification: {result}")
    

# Start capturing packets
def start_packet_capture():
    print("STARTING PACKET CAPTURE:")
    scapy.sniff(prn=process_packet, store=0)
def get_captured_packets():
    return captured_packets