import requests
import openai
from pathlib import Path
from django.conf import settings
import uuid
from django.core.files.base import ContentFile

def summarize_thread_content(client, title, content):
    summarizing_prompt = f"""
    아래는 독서 다이어리의 본문입니다. 이 내용을 바탕으로 감정 중심의 요약을 300자 이내로 작성하십시오.
    설명은 생략하고 요약만 출력하십시오.

    
    <제목>
    {title}
    </제목>

    <본문>
    {content}
    </본문>

    요약:
    """

    try:
        summary_response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "당신은 감정 요약을 잘하는 작가입니다."},
                {"role": "user", "content": summarizing_prompt},
            ],
            max_tokens=300,
            temperature=0.5
        )
        summary = summary_response.choices[0].message.content.strip()
        print("[DEBUG] 요약된 본문:", summary)
        return summary
    except Exception as e:
        print(f"[ERROR] 본문 요약 실패: {e}")
        return content[:500]  # 요약 실패 시 앞 500자 대체


def generate_image_with_openai(thread,thread_title, thread_content, book_title, book_author):
    try:
        # 1. OpenAI 클라이언트 초기화
        client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)

        # 2. 긴 본문 요약 처리
        summarized_content = summarize_thread_content(client, thread_title, thread_content)

        # 3. 키워드 추출 및 프롬프트 생성 요청 프롬프트
        keyword_extractor_prompt = f"""
        {book_author}의 책 {book_title}을 읽고 쓴 독서 다이어리의 감정을 분석해 키워드 5개를 추출하시오.
        키워드 추출이 완료됐다면 키워드를 기반으로 **이미지 생성에 바로 쓸 수 있는 프롬프트 문장만 출력하시오.**
        설명, 라벨("키워드:", "프롬프트:" 등)은 포함하지 말 것.
        생성할 최종 이미지는 **4컷 만화**이고 **감성적이고 따뜻한 색감**이어야 함. 

        <독서 다이어리>
            <제목>{thread_title}</제목>
            <본문>{summarized_content}</본문>
        </독서 다이어리>

        <답변 예시 - 참고용입니다. 실제 응답에는 "키워드:", "프롬프트:" 등의 라벨은 포함하지 마십시오>
            키워드: 그리움, 가족, 회상, 따뜻함, 추억  
            프롬프트:  
            1컷 - 해질녘 창가에 앉아 가족 사진을 바라보는 인물  
            2컷 - 어린 시절 가족과 웃으며 뛰놀던 추억의 장면  
            3컷 - 인물이 눈을 감고 미소 짓는 장면  
            4컷 - 따뜻한 햇살 아래 새 사진을 책장에 올려두는 장면  
            전체적으로 따뜻한 파스텔 톤, 감성적이고 차분한 분위기
        </답변 예시>

        답변 : 
        """


        # 3. GPT를 통해 이미지 생성용 프롬프트 생성
        chat_response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "당신은 이미지 생성 AI를 위한 프롬프트 작성 비서입니다."},
                {"role": "user", "content": keyword_extractor_prompt},
            ],
            max_tokens=2040,
            temperature=0.5
        )
        keyword_extractor_response = chat_response.choices[0].message.content.strip()

        # ✅ GPT 응답에 라벨이 섞여있는지 검사
        if any(kw in keyword_extractor_response.lower() for kw in ["키워드:", "프롬프트:", "답변:"]):
            print("[WARNING] GPT 응답에 라벨 포함됨 → 이미지 생성 중단")
            return None

        # 4. 이미지 생성용 프롬프트 완성
        img_generator_prompt = (
            keyword_extractor_response
            + "\n주의: 생성되는 이미지는 어떠한 텍스트, 글자, 숫자, 심볼도 포함하지 않아야 함."
        )
        print(img_generator_prompt)

        # 5. DALL-E로 이미지 생성 요청
        image_response = client.images.generate(
            model="dall-e-3",
            prompt=img_generator_prompt,
            size="1792x1024",
            quality="standard",
            n=1,
        )

        image_url = image_response.data[0].url

        # 6. 이미지 다운로드 및 저장
        response_img = requests.get(image_url)
        if response_img.status_code == 200:
            file_name = f"{uuid.uuid4()}.png"
            print('[DEBUG] 저장할 파일명:', file_name)
            thread.cover_img.save(file_name, ContentFile(response_img.content), save=True)
            print('[DEBUG] 실제 저장된 경로:', thread.cover_img.name)
            return thread.cover_img.name  # 예: 'thread_cover_img/xxx.png'

    except Exception as e:
        print(f"[ERROR] 이미지 생성 실패: {e}")

    return None  # 실패 시 None 반환