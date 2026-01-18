document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('dateInput').value = new Date().toISOString().split('T')[0];
    // Kakao SDK 초기화 (실제 앱 키로 교체 필요)
    Kakao.init('c58a95f377c261c9abb128f41e76dd07');
});

document.getElementById('fetchButton').addEventListener('click', async () => {
    const display = document.getElementById('gospelDisplay');
    display.textContent = '가져오는 중...';
    
    const dateInput = document.getElementById('dateInput').value;
    const formattedDate = dateInput.replace(/-/g, '');
    
    try {
        const response = await fetch(`/api/get_gospel?date=${formattedDate}`);
        if (!response.ok) {
            throw new Error('API 요청 실패');
        }
        const gospel = await response.text();
        display.textContent = gospel;
    } catch (error) {
        display.textContent = '오류: ' + error.message;
    }
});

document.getElementById('shareButton').addEventListener('click', () => {
    const gospelText = document.getElementById('gospelDisplay').textContent;
    if (!gospelText || gospelText === '가져오는 중...' || gospelText.startsWith('오류:')) {
        alert('공유할 복음이 없습니다. 먼저 복음을 가져오세요.');
        return;
    }
    
    Kakao.Share.sendDefault({
        objectType: 'text',
        text: `카톨릭 매일 미사 복음:\n\n${gospelText}`,
        link: {
            mobileWebUrl: window.location.href,
            webUrl: window.location.href
        }
    });
});