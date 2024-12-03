# DNS client

import socket
from dnslib import DNSRecord

# Server details
dns_server_ip = "127.0.0.1"  # Replace with your DNS server's IP
dns_server_port = 8053       # Replace with your DNS server's port
domain = "phyona.local."     # Domain to query

# Create a DNS query
query = DNSRecord.question(domain)

# Send the query to the DNS server
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client_socket:
    print(f"Sending query for {domain} to {dns_server_ip}:{dns_server_port}")
    client_socket.sendto(query.pack(), (dns_server_ip, dns_server_port))
    
    # Receive the response
    response, _ = client_socket.recvfrom(4096)
    dns_response = DNSRecord.parse(response)
    print("Received response:")
    print(dns_response)
