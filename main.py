import asyncio
import websockets
import json
import ssl
from flask import Flask, render_template
from flask_socketio import SocketIO, emit

# Flask 애플리케이션 설정
app = Flask(__name__)
socketio = SocketIO(app, async_mode="eventlet")  # async_mode 설정

# Cortex API 연결 설정
CORTEX_URL = "wss://localhost:6868"

# SSL 인증서 검증을 무시하는 코드 추가
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

# EEG 스트림 시작 및 데이터 수집
async def start_eeg_stream():
    try:
        ws = await websockets.connect(CORTEX_URL, ssl_context=ssl_context)
        print("Connected to Cortex API!")
        
        # 인증 요청
        auth_request = {
            "jsonrpc": "2.0",
            "method": "authorize",
            "params": {
                "clientId": "qnEtmyPfWRmos8lUGoocBPQSYLldPxcrj2wyiXuM",  # clientId
                "clientSecret": "Bi0z7iyn2ca6F1fnxbKzSDZ1F9HeloOUfaJPcL4oktqdaLy5Bw5pqFywFLAtS0CjraGtnjkFIRT8oaqr8ZPO72VEYBNkJmLWj0eN2oWgJEyAFHqQoXe8kI1488BY7y64"  # clientSecret
            },
            "id": 1
        }
        await ws.send(json.dumps(auth_request))
        auth_response = await ws.recv()
        auth_data = json.loads(auth_response)
        
        if "result" in auth_data:
            cortex_token = auth_data['result']['cortexToken']
            print("Authorization successful!")
        else:
            print("Authorization failed:", auth_data)
            return None
        
        # EEG 스트림 구독 요청
        subscribe_request = {
            "jsonrpc": "2.0",
            "method": "subscribe",
            "params": {
                "cortexToken": cortex_token,
                "streams": ["eeg"]
            },
            "id": 2
        }
        await ws.send(json.dumps(subscribe_request))

        # EEG 데이터 수신
        while True:
            try:
                response = await ws.recv()
                response_data = json.loads(response)
                if "eeg" in response_data:
                    return response_data["eeg"]  # EEG 데이터 반환
            except Exception as e:
                print(f"Error collecting EEG data: {e}")
                break

    except Exception as e:
        print(f"Failed to connect to Cortex API: {e}")
        return None

# Flask-SocketIO 연결 이벤트 처리
@socketio.on('connect')
def handle_connect():
    print("Client connected")
    # EEG 데이터 수집을 백그라운드 작업으로 실행
    socketio.start_background_task(eeg_data_task)

# 비동기 백그라운드 작업 함수
def eeg_data_task():
    async def get_eeg_data():
        eeg_data = await start_eeg_stream()
        if eeg_data:
            # 클라이언트에게 EEG 데이터 전송
            emit('eeg_data', eeg_data, broadcast=True)

    # 비동기 작업을 실행
    asyncio.run(get_eeg_data())

# 기본 라우트 (HTML 렌더링)
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    socketio.run(app, host='0.0.0.0', port=5000)
