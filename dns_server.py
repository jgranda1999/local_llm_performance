from dnslib import DNSRecord, RR, QTYPE, A
from socketserver import UDPServer, BaseRequestHandler
from queue import Queue
import threading
import logging

logging.basicConfig(level=logging.DEBUG)

DNS_RECORDS = {
    "phyona.local.": "127.0.0.1",
    "jonathan.local": "172.26.127.94"
}

# Queue to store incoming requests
request_queue = Queue()

# Create a custom request handler
class DNSHandler(BaseRequestHandler):
    def handle(self):
        data, socket = self.request
        logging.debug(f"Received query: {data} from {self.client_address}")

        # Add request to the queue
        request_queue.put((data, socket, self.client_address))


# Worker function to process DNS requests from the queue
def process_dns_requests():
    while True:
        # Get the next request from the queue
        data, socket, client_address = request_queue.get()

        # Parse the incoming DNS request
        request = DNSRecord.parse(data)
        queried_domain = str(request.q.qname)
        qtype = QTYPE[request.q.qtype]

        # Prepare a DNS response
        reply = request.reply()
        if queried_domain in DNS_RECORDS and qtype == "A":
            reply.add_answer(RR(queried_domain, QTYPE.A, rdata=A(DNS_RECORDS[queried_domain])))

        # Send the response back to the client
        socket.sendto(reply.pack(), client_address)
        logging.debug(f"Sent response for {queried_domain} to {client_address}")

        # Mark the task as done
        request_queue.task_done()


if __name__ == "__main__":
    print("Starting DNS server on port 8053...")

    # Start a worker thread to process requests
    threading.Thread(target=process_dns_requests, daemon=True).start()

    # Create a UDP server that listens on all interfaces
    with UDPServer(("0.0.0.0", 8053), DNSHandler) as server:
        server.serve_forever()
