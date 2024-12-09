## Imports the required modules
from dnslib import DNSRecord, RR, QTYPE, A
from socketserver import UDPServer, BaseRequestHandler
import logging
logging.basicConfig(level=logging.DEBUG)

# Define the DNS records to be resolved by the DNS server
DNS_RECORDS = {
    "phyona.local.": "127.0.0.1",
    "jonathan.local.": "127.0.0.1",
    "james.local.": "127.0.0.1",
    "joseph.local.": "127.0.0.1",
    "doug.local.": "127.0.0.1",
}
PORT_MAPPING = {
    "phyona.local.": "8001",
    "jonathan.local.": "8002",
    "james.local.": "8003",
    "joseph.local.": "8004",
    "doug.local.": "8005",
}

class DNSHandler(BaseRequestHandler):
    def handle(self):
        data, socket = self.request
        logging.debug(f"Received query: {data} from {self.client_address}")

        # Parse the incoming DNS request packet
        request = DNSRecord.parse(data)
        queried_domain = str(request.q.qname)
        qtype = QTYPE[request.q.qtype]
        reply = request.reply()

        if queried_domain in DNS_RECORDS and qtype == "A":
            # Resolve the IP address without port
            resolved_ip = DNS_RECORDS[queried_domain]
            reply.add_answer(RR(queried_domain, QTYPE.A, rdata=A(resolved_ip)))

        # Send the response
        socket.sendto(reply.pack(), self.client_address)

# Create a custom request handler by subclassing BaseRequestHandler
class DNSHandler(BaseRequestHandler):
    def handle(self):
        # The `self.request` attribute contains the client data and the socket
        data, socket = self.request
        logging.debug(f"Received query: {data} from {self.client_address}")

        # Parse the incoming DNS request packet
        request = DNSRecord.parse(data)

        # Extract the queried domain name from the DNS request
        queried_domain = str(request.q.qname)

        # Extract the query type (e.g., 'A' for Address record) from the request
        qtype = QTYPE[request.q.qtype]

        # Prepare a DNS response by copying the original request
        reply = request.reply()

        # Check if the queried domain exists in our DNS records and is an A (Address) query
        if queried_domain in DNS_RECORDS and qtype == "A":
            # Add an answer to the DNS response with the resolved IP address
            reply.add_answer(RR(queried_domain, QTYPE.A, rdata=A(DNS_RECORDS[queried_domain])))
        
        # Send the constructed DNS response back to the client
        socket.sendto(reply.pack(), self.client_address)

# Start the DNS server
if __name__ == "__main__":
    print("Starting DNS server on port 8053...")  

    # Create a UDP server that listens on all network interfaces (0.0.0.0) at port 8053 (default DNS port)
    with UDPServer(("0.0.0.0", 8053), DNSHandler) as server:
        server.serve_forever()  # Keep the server running indefinitely
