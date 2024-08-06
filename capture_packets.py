from scapy.all import sniff, wrpcap

def capture_traffic(packet_count, output_file):
    packets = sniff(count=packet_count)
    wrpcap(output_file, packets)

# Capture normal traffic
capture_traffic(2000, 'data/raw/packets.pcap')