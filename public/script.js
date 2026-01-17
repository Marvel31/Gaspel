document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('dateInput').value = new Date().toISOString().split('T')[0];
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