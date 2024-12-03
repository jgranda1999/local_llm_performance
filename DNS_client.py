import socket
from dnslib import DNSRecord
import requests
import time

# DNS server details
dns_server_ip = "127.0.0.1"
dns_server_port = 8053
domain = "phyona.local."

# Create a DNS query
query = DNSRecord.question(domain)

# Measure DNS throughput and latency
print(f"Sending query for {domain} to {dns_server_ip}:{dns_server_port}")

# Start timing for DNS query
dns_start_time = time.time()

# Send the query to the DNS server
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client_socket:
    client_socket.sendto(query.pack(), (dns_server_ip, dns_server_port))
    
    # Receive the response
    response, _ = client_socket.recvfrom(4096)
    dns_end_time = time.time()

# Parse the DNS response
dns_response = DNSRecord.parse(response)
print("Received DNS response:")
print(dns_response)

# Extract the resolved IP address from the DNS response
resolved_ip = None
for rr in dns_response.rr:
    if rr.rtype == 1:  # A record
        resolved_ip = str(rr.rdata)
        break

if not resolved_ip:
    print("Error: No A record found in the DNS response.")
    exit(1)

# Output DNS throughput
dns_time_taken = dns_end_time - dns_start_time
print(f"DNS query throughput: {dns_time_taken:.6f} seconds")
print(f"Resolved IP: {resolved_ip}")

# Measure latency for interacting with the local server
local_server_url = f"http://{resolved_ip}:8000"  # Replace with your local server's port and endpoint
try:
    print(f"Connecting to local server at {local_server_url}")
    
    # Start timing for local server interaction
    local_start_time = time.time()
    
    # Example request to the local server
    response = requests.get(local_server_url)
    local_end_time = time.time()
    
    # Output local server latency
    local_time_taken = local_end_time - local_start_time
    print(f"Local server response: {response.status_code}")
    print(f"Local server latency: {local_time_taken:.6f} seconds")
except Exception as e:
    print(f"Error connecting to local server: {e}")
