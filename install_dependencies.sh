
#!/bin/bash

# Install Python dependencies
pip install -r requirements.txt

# Install system dependencies
pip install --upgrade transformers accelerate
sudo apt install nginx -y
sudo apt install bind9-dnsutils