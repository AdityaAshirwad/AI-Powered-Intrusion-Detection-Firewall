import scapy.all as scapy
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, StandardScaler

# Load the pcap file
packets = scapy.rdpcap('data/raw/packets.pcap')

# Define a function to extract features from a packet
def extract_features(packet):
    features = {}
    
    # Basic packet information
    features['length'] = len(packet)
    
    # IP layer features
    if scapy.IP in packet:
        features['src_ip'] = str(packet[scapy.IP].src)  
        features['dst_ip'] = str(packet[scapy.IP].dst)  
        features['protocol'] = packet[scapy.IP].proto
    
    # TCP layer features
    if scapy.TCP in packet:
        features['src_port'] = packet[scapy.TCP].sport
        features['dst_port'] = packet[scapy.TCP].dport
        features['flags'] = packet[scapy.TCP].flags
    
    return features

# Extract features from all packets
data = []
for packet in packets:
    features = extract_features(packet)
    data.append(features)

# Convert to DataFrame
df = pd.DataFrame(data)

# Fill missing values with 0
df.fillna(0, inplace=True)

# Ensure IP addresses are strings
df['src_ip'] = df['src_ip'].astype(str)
df['dst_ip'] = df['dst_ip'].astype(str)

# Encode IP addresses and protocol as numerical values
label_encoder = LabelEncoder()
df['src_ip'] = label_encoder.fit_transform(df['src_ip'])
df['dst_ip'] = label_encoder.fit_transform(df['dst_ip'])
df['protocol'] = label_encoder.fit_transform(df['protocol'].astype(str))  # Ensure protocol is string

# Encode the flags column
df['flags'] = df['flags'].astype(str) 
flags_encoder = LabelEncoder()
df['flags'] = flags_encoder.fit_transform(df['flags'])


# Here, we can manually label some data as malicious for testing purposes
df['Label'] = 0 
df.loc[0:1000, 'Label'] = 1  

# Ensure all data is numeric
print(df.dtypes) 
df.to_csv('data/processed/dataset.csv', index=False)

print("Data preprocessing completed and saved to dataset.csv")
