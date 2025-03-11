import pygame
import random
import time
import json
from websocket import create_connection
import ssl
import certifi

# Pygame 초기화
pygame.init()

# 화면 설정
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("P300 Speller")
font = pygame.font.SysFont('Arial', 50)

# 색상 정의
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
HIGHLIGHT_BG = (200, 200, 200)

# 키보드 매트릭스 정의
KEYS = [
    ['A', 'B', 'C', 'D', 'E', 'F'],
    ['G', 'H', 'I', 'J', 'K', 'L'],
    ['M', 'N', 'O', 'P', 'Q', 'R'],
    ['S', 'T', 'U', 'V', 'W', 'X'],
    ['Y', 'Z', '_', '1', '2', '3'],
    ['4', '5', '6', '7', '8', '9']
]

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

def collect_eeg_data():
    # Cortex API에서 EEG 데이터 수집
    try:
        response = json.loads(ws.recv())
        if "eeg" in response:
            print("EEG Data:", response["eeg"])
            # 데이터를 저장하거나 분석에 사용 가능
    except Exception as e:
        print(f"Error collecting EEG data: {e}")

def main():
    start_eeg_stream()  # EEG 스트림 시작

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        collect_eeg_data()  # EEG 데이터 실시간 수집

        time.sleep(0.0625)  # 자극 사이 간격

    ws.close()
    pygame.quit()

if __name__ == "__main__":
    main()
