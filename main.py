import asyncio
import websockets
import json
from websocket import create_connection
import ssl
import certifi

# Cortex API 연결 설정
CORTEX_URL = "wss://localhost:6868"

try:
    ws = create_connection(CORTEX_URL, sslopt={"ca_certs": certifi.where()})
    print("Connected to Cortex API!")
except Exception as e:
    print(f"Failed to connect to Cortex API: {e}")
    exit()

def send_command(command):
    ws.send(json.dumps(command))
    return json.loads(ws.recv())

def start_eeg_stream():
    # Cortex API 인증 및 EEG 스트림 시작
    auth_request = {
        "jsonrpc": "2.0",
        "method": "authorize",
        "params": {
            "clientId": "your-client-id",  # Cortex Apps에서 발급받은 Client ID
            "clientSecret": "your-client-secret"  # Cortex Apps에서 발급받은 Client Secret
        },
        "id": 1
    }
    auth_response = send_command(auth_request)
    if "result" in auth_response:
        cortex_token = auth_response['result']['cortexToken']
        print("Authorization successful!")
    else:
        print("Authorization failed:", auth_response)
        return

    subscribe_request = {
        "jsonrpc": "2.0",
        "method": "subscribe",
        "params": {
            "cortexToken": cortex_token,
            "streams": ["eeg"]
        },
        "id": 2
    }
    send_command(subscribe_request)

async def handle_connection(websocket):
    start_eeg_stream()  # EEG 스트림 시작

    while True:
        try:
            response = json.loads(ws.recv())
            if "eeg" in response:
                await websocket.send(json.dumps(response["eeg"]))
        except Exception as e:
            print(f"Error collecting EEG data: {e}")
            break

async def main():
    async with websockets.serve(handle_connection, "localhost", 8080):
        print("Server started on port 8080")
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())
