import os
from pyngrok import ngrok
from dotenv import load_dotenv

load_dotenv()

# Load environment variables
port = 8000
authtoken = os.getenv("NGROK_AUTHTOKEN")
domain = os.getenv("NGROK_DOMAIN")

# Set authtoken
ngrok.set_auth_token(authtoken)

# Open tunnel with custom domain
public_url = ngrok.connect(addr=port, domain=domain)
print(f" * ngrok tunnel: {public_url}")

# Start Django server
os.system(f"python manage.py runserver {port}")
