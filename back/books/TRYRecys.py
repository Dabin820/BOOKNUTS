from dotenv import load_dotenv
import os
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

from openai import OpenAI

client = OpenAI(api_key=openai_api_key)

# 1. 파일 업로드
file_response = client.files.create(
    file=open("./fixtures/new_books.json", "rb"),
    purpose="assistants"
)
file_id = file_response.id

# 2. Assistant 생성 (Retrieval tool 활성화)
assistant = client.beta.assistants.create(
    instructions="문서와 사용자 쿼리를 비교해 답변하세요.",
    tools=[{"type": "file_search"}],
    model="gpt-4o-mini"
)

# 3. Thread 생성 및 메시지(파일 첨부)
thread = client.beta.threads.create()
client.beta.threads.messages.create(
    thread.id,
    role="user",
    content="이 문서와 내 쿼리를 비교해줘.",
    file_ids=[file_id]
)

# 4. Assistant 실행 및 결과 확인
run = client.beta.threads.runs.create(
    thread_id=thread.id,
    assistant_id=assistant.id
)
# 결과 polling 및 출력 (생략)
