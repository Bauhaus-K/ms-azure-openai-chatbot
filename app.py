import streamlit as st
import os
from openai import AzureOpenAI
from dotenv import load_dotenv

# 1. 환경 변수 로드
load_dotenv()

st.title("🧿 Dreamcatcher")

# 2. Azure OpenAI 클라이언트 설정
client = AzureOpenAI(
    api_key=os.getenv("AZURE_OAI_KEY"),
    api_version="2024-05-01-preview",
    azure_endpoint=os.getenv("AZURE_OAI_ENDPOINT")
)

# 3. 대화기록 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []

# 4. 기존 대화 출력
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. 사용자 입력 받기
if prompt := st.chat_input("무엇을 도와드릴까요?"):
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # 6. 이미지 생성 요청 여부 확인
    if "이미지" in prompt or "그림" in prompt or "image" in prompt.lower():
        with st.chat_message("assistant"):
            st.markdown("🖼️ 이미지 생성 중입니다…")
            # 이미지 생성 요청
            image_response = client.images.generate(
                prompt=prompt,
                n=1,
                size="512x512"
            )
            image_url = image_response.data[0].url
            st.image(image_url, caption="✨ 생성된 이미지")
            assistant_reply = "이미지를 생성했어요!"
    else:
        # 일반 텍스트 응답
        with st.chat_message("assistant"):
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ]
            )
            assistant_reply = response.choices[0].message.content
            st.markdown(assistant_reply)

    # 7. 응답 저장
    st.session_state.messages.append({"role": "assistant", "content": assistant_reply})
