import pygame
import random
import time
import csv

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
HIGHLIGHT_BG = (200, 200, 200)  # 강조된 배경 색상

# 키보드 매트릭스 정의
KEYS = [
    ['A', 'B', 'C', 'D', 'E', 'F'],
    ['G', 'H', 'I', 'J', 'K', 'L'],
    ['M', 'N', 'O', 'P', 'Q', 'R'],
    ['S', 'T', 'U', 'V', 'W', 'X'],
    ['Y', 'Z', '1', '2', '3', '4'],
    ['5', '6', '7', '8', '9', '_']
]

# 키 크기 및 위치 설정
KEY_WIDTH, KEY_HEIGHT = 100, 100
MARGIN = 10

# 이벤트 저장 변수
event_markers = []
target_sentence = "HELLO WORLD"  # 타겟 문장 설정 (고정)
selected_text = ""  # 결과 영역에 표시될 선택된 텍스트

def draw_keyboard(highlighted_row=None, highlighted_col=None):
    # 매트릭스 그리기
    for row_idx, row in enumerate(KEYS):
        for col_idx, key in enumerate(row):
            x = col_idx * (KEY_WIDTH + MARGIN) + MARGIN
            y = row_idx * (KEY_HEIGHT + MARGIN) + MARGIN + 150
            
            # 강조된 행 또는 열의 배경 변경
            if row_idx == highlighted_row or col_idx == highlighted_col:
                pygame.draw.rect(screen, HIGHLIGHT_BG, (x, y, KEY_WIDTH, KEY_HEIGHT))
                text_font = pygame.font.SysFont('Arial Bold', 50)
            else:
                pygame.draw.rect(screen, BLACK, (x, y, KEY_WIDTH, KEY_HEIGHT))
                text_font = pygame.font.SysFont('Arial', 50)

            text_surface = text_font.render(key, True, WHITE)
            screen.blit(text_surface, (x + KEY_WIDTH // 4, y + KEY_HEIGHT // 4))

def draw_result_bar():
    # 상단 바에 타겟 문장과 선택된 텍스트 표시
    result_font = pygame.font.SysFont('Arial Bold', 40)
    target_surface = result_font.render(f"TARGET: {target_sentence}", True, WHITE)
    selected_surface = result_font.render(f"RESULT: {selected_text}", True, WHITE)
    screen.blit(target_surface, (MARGIN + 10, MARGIN))
    screen.blit(selected_surface, (MARGIN + 10, MARGIN + 50))

def save_event_marker(marker):
    timestamp = time.time()
    event_markers.append({"marker": marker, "timestamp": timestamp})
    print(f"Event Marker: {marker}, Timestamp: {timestamp}")

def update_system():
    global selected_text

    # 무작위로 행 또는 열 선택
    highlighted_row = random.randint(0, len(KEYS) - 1)
    highlighted_col = random.randint(0, len(KEYS[0]) - 1)

    # 행 강조 표시 및 이벤트 저장
    draw_keyboard(highlighted_row=highlighted_row)
    save_event_marker(f"Row-{highlighted_row}")
    pygame.display.flip()
    time.sleep(0.125)  # 깜빡이는 시간

    # 열 강조 표시 및 이벤트 저장
    draw_keyboard(highlighted_col=highlighted_col)
    save_event_marker(f"Col-{highlighted_col}")
    
    draw_result_bar()
    pygame.display.flip()
    
def process_selection():
    global selected_text

    # 현재 타겟 문자를 결과 텍스트에 추가
    selected_text += target_sentence[len(selected_text)]

def save_data():
    # 이벤트 데이터를 CSV 파일로 저장
    with open("event_markers.csv", "w", newline="") as csvfile:
        fieldnames = ["marker", "timestamp"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(event_markers)

def main():
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # 현재 타겟 문자를 처리한 후 다음 문자로 이동
        for _ in range(15):  # 각 행과 열이 총 15번 반복됨
            update_system()
            time.sleep(0.0625)  # 자극 사이 간격

        process_selection()  # 현재 타겟 문자 처리
        
        if len(selected_text) >= len(target_sentence):  # 모든 문자를 완료하면 종료
            running = False

    save_data()  # 종료 시 데이터 저장
    pygame.quit()

if __name__ == "__main__":
    main()