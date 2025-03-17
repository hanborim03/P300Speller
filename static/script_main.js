document.addEventListener("DOMContentLoaded", function () {
    let keys = [
        ['A', 'B', 'C', 'D', 'E', 'F'],
        ['G', 'H', 'I', 'J', 'K', 'L'],
        ['M', 'N', 'O', 'P', 'Q', 'R'],
        ['S', 'T', 'U', 'V', 'W', 'X'],
        ['Y', 'Z', '1', '2', '3', '4'],
        ['5', '6', '7', '8', '9', '_']
    ];

    let selectedText = ""; // RESULT 문장에 표시될 선택된 텍스트
    let targetSentences = ["THE QUICK BROWN FOX", "JUMP OVER LAZY DOGS", "HELLO WORLD", "SEJONG DATA VISUALIZATION LABORATORY"]; // 타겟 문장들
    let currentSentenceIndex = 0; // 현재 문장의 인덱스
    let currentTargetIndex = 0; // 현재 타겟 문자의 인덱스
    let flashCount = 0; // 깜빡임 횟수
    let isRowFlash = true; // 행과 열 번갈아 깜빡임을 위한 플래그
    let eventMarkers = []; // 이벤트 데이터를 저장할 배열
    let currentAlphabet = ''; // 현재 응시하고 있는 알파벳
    let startTime = 0; // 알파벳을 바라본 시작 시간

    // 행 또는 열 강조 효과 구현
    function highlightRow(rowIndex) {
        const rowElements = document.querySelectorAll(`.row-${rowIndex}`);
        rowElements.forEach(element => {
            element.classList.add('highlight');
        });
    }

    function unhighlightRow(rowIndex) {
        const rowElements = document.querySelectorAll(`.row-${rowIndex}`);
        rowElements.forEach(element => {
            element.classList.remove('highlight');
        });
    }

    function highlightCol(colIndex) {
        const colElements = document.querySelectorAll(`.col-${colIndex}`);
        colElements.forEach(element => {
            element.classList.add('highlight');
        });
    }

    function unhighlightCol(colIndex) {
        const colElements = document.querySelectorAll(`.col-${colIndex}`);
        colElements.forEach(element => {
            element.classList.remove('highlight');
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

        if (flashCount === 1) {
            // 새로운 알파벳을 바라보기 시작할 때 타이머 시작
            startTime = Date.now();
        }

        if (flashCount >= 15) { // 행과 열이 총 15번 깜빡이면 다음 알파벳으로 이동
            flashCount = 0;

            if (currentTargetIndex < targetSentences[currentSentenceIndex].length) {
                selectedText += targetSentences[currentSentenceIndex][currentTargetIndex];
                document.getElementById('selected-text').textContent = `RESULT: ${selectedText}`;
                currentTargetIndex++;
            }

            if (currentTargetIndex >= targetSentences[currentSentenceIndex].length) { // 한 문장이 끝났을 때
                currentSentenceIndex++; // 다음 문장으로 이동
                if (currentSentenceIndex >= targetSentences.length) { // 모든 문장이 끝났을 때
                    clearInterval(flashInterval); // 반복 종료
                    saveData(); // 데이터 저장
                    return;
                }
                // 일정 시간 기다린 후 다음 문장으로 넘어가도록 설정 (1초 대기)
                setTimeout(() => {
                    currentTargetIndex = 0; // 타겟 인덱스 초기화
                    selectedText = ""; // 선택된 텍스트 초기화
                    document.getElementById('selected-text').textContent = `RESULT: ${selectedText}`; // 결과 표시 초기화
                    flashCount = 0; // 깜빡임 횟수 초기화
                    document.getElementById('target-sentence').textContent = `TARGET: ${targetSentences[currentSentenceIndex]}`; // 새로운 문장 표시
                }, 1000); // 1초 대기
            }
        }
    }

    const flashInterval = setInterval(flash, 250); // 250ms 간격으로 반복

    // 첫 번째 문장 표시
    document.getElementById('target-sentence').textContent = `TARGET: ${targetSentences[currentSentenceIndex]}`;

    // EEG 데이터 수신
    socket.on('eeg_data', function(data) {
        console.log('EEG Data:', data);

        // 현재 응시하는 알파벳과 그 시간을 기록합니다.
        if (flashCount === 1) {
            // 첫 깜빡임에서 기록 시작
            currentAlphabet = targetSentences[currentSentenceIndex][currentTargetIndex - 1];
            eventMarkers.push({
                marker: `Started viewing ${currentAlphabet}`,
                timestamp: startTime,
            });
        }

        if (flashCount >= 15) {
            // EEG 데이터에 기반한 행렬 제어 로직을 추가할 수 있습니다.
            // 예를 들어 EEG 데이터의 특정 값을 기반으로 특정 행 또는 열을 강조
            eventMarkers.push({
                marker: `Finished viewing ${currentAlphabet}`,
                timestamp: Date.now(),
            });
        }
    });

    // CSV 파일 저장 기능 추가
    function saveData() {
        let csvContent = "data:text/csv;charset=utf-8,Marker,Timestamp\n";
        eventMarkers.forEach(event => {
            csvContent += `${event.marker},${event.timestamp}\n`;
        });

        const encodedUri = encodeURI(csvContent);
        const link = document.createElement("a");
        link.setAttribute("href", encodedUri);
        link.setAttribute("download", "event_markers.csv");
        document.body.appendChild(link); // 필요 시 링크를 DOM에 추가
        link.click(); // 다운로드 실행
    }
});
