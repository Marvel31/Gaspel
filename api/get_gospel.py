from bs4 import BeautifulSoup
import requests

def handler(request):
    try:
        date = request.get('date')
        if date:
            url = f"https://missa.cbck.or.kr/DailyMissa/{date}"
        else:
            url = "https://missa.cbck.or.kr/DailyMissa/"
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 복음 헤더 찾기
        gospel_header = soup.find('h4', string='복음')
        if not gospel_header:
            return {
                'statusCode': 404,
                'body': '복음 섹션을 찾을 수 없습니다.'
            }
        
        # 복음 본문이 들어있는 div 찾기: 헤더 다음 row tjustify div
        gospel_row = gospel_header.find_next('div', class_='row tjustify')
        if not gospel_row:
            return {
                'statusCode': 404,
                'body': '복음 본문을 찾을 수 없습니다.'
            }
        
        gospel_div = gospel_row.find('div', class_='col-12').find('div')
        full_text = gospel_div.get_text()
        
        # "주님의 말씀입니다" 전까지 추출
        end_marker = "주님의 말씀입니다"
        if end_marker in full_text:
            gospel_text = full_text.split(end_marker)[0].strip()
        else:
            gospel_text = full_text.strip()
        
        return {
            'statusCode': 200,
            'body': gospel_text
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': f'오류 발생: {str(e)}'
        }