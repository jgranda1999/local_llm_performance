#Imports 
import socket
from dnslib import DNSRecord
import requests
import time

# Main function
def main():

    # Define the DNS server IP and port
    dns_server_ip = "0.0.0.0"
    dns_server_port = 8053
    # Define the port mapping for the local LLM servers
    PORT_MAPPING = {
        "phyona.local.": "8001",
        "jonathan.local.": "8002",
        "james.local.": "8003",
        "joseph.local.": "8004",
        "doug.local.": "8005",
    }

    # Interactive loop
    print("Welcome to your AI assistant. Ask anything or type 'exit' to quit.")
    while True:
        print("Please choose which domain to query: phyona.local, jonathan.local, james.local, joseph.local, doug.local")
        domain = input("Example: phyona.local.\n")

        if domain.lower() == "exit":
            break

        question = input("Ask a question: ")
        if question.lower() == "exit":
            break
   
        payload = {
            "prompt": f"{question}"
        }

        # Create a DNS query
        query = DNSRecord.question(domain)

        # Measure DNS throughput and latency
        print(f"Sending query for {domain} to {dns_server_ip}:{dns_server_port}")

        # Start timing for DNS query
        dns_start_time = time.time()

        # Send the query to the DNS server
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client_socket:
            client_socket.sendto(query.pack(), (dns_server_ip, dns_server_port))
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

        # Get the port based on the queried domain
        resolved_port = None
        if domain in PORT_MAPPING:
            resolved_port = PORT_MAPPING[domain]
        else:
            print(f"Error: No port mapping found for {domain}.")
            exit(1)

        # Output DNS throughput
        dns_time_taken = dns_end_time - dns_start_time
        print(f"DNS query throughput: {dns_time_taken:.6f} seconds")
        print(f"Resolved IP: {resolved_ip}")

        # Measure latency and throughput for the local LLM server
        local_server_url = f"http://{resolved_ip}:{resolved_port}/generate"
        try:
            print(f"Connecting to local server at {local_server_url}")

            # Measure latency for a single request
            local_start_time = time.time()

            # Send POST request
            response = requests.post(local_server_url, json=payload)

            # Print the response
            if response.status_code == 200:
                generated_text = response.json().get("response")
                if generated_text:
                    print()
                    print(f"{generated_text}\n")
                else:
                    print("No response generated.")
            else:
                print("Error:", response.status_code, response.text)

            # Throughput test (multiple requests)
            num_requests = 10
            throughput_start_time = time.time()

            for _ in range(num_requests):
                response = requests.post(local_server_url, json=payload)

            throughput_end_time = time.time()

            total_time = throughput_end_time - throughput_start_time

            # Calculate throughput
            throughput = num_requests / total_time
            print(f"Throughput: {throughput:.2f} requests/second over {num_requests} requests")
            
        except Exception as e:
            print(f"Error connecting to local server: {e}")


if __name__ == "__main__":
    print("Starting DNS client...")
    main()


