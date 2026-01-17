from bs4 import BeautifulSoup
import requests

def handler(request):
    try:
        url = "https://missa.cbck.or.kr/DailyMissa/"
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 복음 본문 찾기: "그때에"로 시작하는 텍스트
        gospel_start = soup.find(string=lambda text: text and text.strip().startswith("그때에"))
        if not gospel_start:
            return {
                'statusCode': 404,
                'body': '복음 본문을 찾을 수 없습니다.'
            }
        
        # 본문이 들어있는 div 찾기: 부모 div의 부모 div
        gospel_div = gospel_start.find_parent('div').find_parent('div')
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