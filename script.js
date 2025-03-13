// 매트릭스 데이터 정의
let keys = [
    ['A', 'B', 'C', 'D', 'E', 'F'],
    ['G', 'H', 'I', 'J', 'K', 'L'],
    ['M', 'N', 'O', 'P', 'Q', 'R'],
    ['S', 'T', 'U', 'V', 'W', 'X'],
    ['Y', 'Z', '1', '2', '3', '4'],
    ['5', '6', '7', '8', '9', '_']
];

let selectedText = ""; // RESULT 문장에 표시될 선택된 텍스트
let targetSentence = "HELLO WORLD"; // 타겟 문장 (고정)
let currentTargetIndex = 0; // 현재 타겟 문자의 인덱스
let flashCount = 0; // 깜빡임 횟수
let isRowFlash = true; // 행과 열 번갈아 깜빡임을 위한 플래그

// 행 또는 열 강조 효과 구현
function highlightRow(rowIndex) {
    const rowElements = document.querySelectorAll(`.row-${rowIndex}`);
    rowElements.forEach(element => {
        element.classList.add('highlight');
        element.style.transition = "all 0.125s"; // 부드러운 전환 효과 추가
        element.style.color = "#fff"; // 강조된 글자 색상 변경
        element.style.fontWeight = "bold"; // 폰트 굵게 설정
        element.style.textShadow = "0px 0px 10px #fff"; // 밝은 효과 추가
    });
}

function unhighlightRow(rowIndex) {
    const rowElements = document.querySelectorAll(`.row-${rowIndex}`);
    rowElements.forEach(element => {
        element.classList.remove('highlight');
        element.style.transition = "all 0.125s"; // 부드러운 전환 효과 추가
        element.style.color = "#666"; // 기본 색상 복원
        element.style.fontWeight = "normal"; // 폰트 굵기 복원
        element.style.textShadow = "none"; // 밝은 효과 제거
    });
}

function highlightCol(colIndex) {
    const colElements = document.querySelectorAll(`.col-${colIndex}`);
    colElements.forEach(element => {
        element.classList.add('highlight');
        element.style.transition = "all 0.125s";
        element.style.color = "#fff";
        element.style.fontWeight = "bold";
        element.style.textShadow = "0px 0px 10px #fff";
    });
}

function unhighlightCol(colIndex) {
    const colElements = document.querySelectorAll(`.col-${colIndex}`);
    colElements.forEach(element => {
        element.classList.remove('highlight');
        element.style.transition = "all 0.125s";
        element.style.color = "#666";
        element.style.fontWeight = "normal";
        element.style.textShadow = "none";
    });
}

// 매트릭스 요소 생성 및 추가
keys.forEach((row, rowIndex) => {
    row.forEach((key, colIndex) => {
        const keyDiv = document.createElement('div');
        keyDiv.classList.add('key');
        keyDiv.textContent = key;
        keyDiv.classList.add(`row-${rowIndex}`);
        keyDiv.classList.add(`col-${colIndex}`);
        
        document.getElementById('keyboard').appendChild(keyDiv);
    });
});

// 깜빡임 반복
function flash() {
    if (isRowFlash) { // 행 깜빡임 처리
        const randomRow = Math.floor(Math.random() * keys.length);
        highlightRow(randomRow);
        setTimeout(() => unhighlightRow(randomRow), 125); // 깜빡임 후 원래 상태로 복원
        isRowFlash = false; // 다음에는 열이 깜빡이도록 설정
    } else { // 열 깜빡임 처리
        const randomCol = Math.floor(Math.random() * keys[0].length);
        highlightCol(randomCol);
        setTimeout(() => unhighlightCol(randomCol), 125); // 깜빡임 후 원래 상태로 복원
        isRowFlash = true; // 다음에는 행이 깜빡이도록 설정
    }

    flashCount++;

    if (flashCount >= 15) { // 행과 열이 총 15번 깜빡이면 다음 알파벳으로 이동
        flashCount = 0;

        if (currentTargetIndex < targetSentence.length) {
            selectedText += targetSentence[currentTargetIndex];
            document.getElementById('selected-text').textContent = `RESULT: ${selectedText}`;
            currentTargetIndex++;
        }

        if (currentTargetIndex >= targetSentence.length) {
            clearInterval(flashInterval); // 모든 알파벳 선택 완료 시 반복 종료
            return;
        }
    }
}

const flashInterval = setInterval(flash, 250); // 250ms 간격으로 반복

// 타겟 문장 표시
document.getElementById('target-sentence').textContent = `TARGET: ${targetSentence}`;
