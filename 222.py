import streamlit as st
import requests
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO
import json
from pathlib import Path
import streamlit.components.v1 as components
import datetime
import random

# 카카오톡 채널 임베딩
today_date = datetime.date.today()
st.title(f"🍽️{today_date} 오늘의 메뉴's🍽️")

# 카카오톡 채널 URL 2개
url1 = "https://pf.kakao.com/_CiVis/posts"
url2 = "https://pf.kakao.com/_vKxgdn/posts"

# 2개의 열로 나누기
col1, col2 = st.columns(2)

# 첫 번째 열에 URL1 임베딩
with col1:
    st.subheader("📌 슈마우스만찬")
    components.iframe(url1, height=600, width=1000)

# 두 번째 열에 URL2 임베딩
with col2:
    st.subheader("     📌 정담식당")
    components.iframe(url2, height=600, width=1000)
    
# 랜덤 식당 추천
if st.button("오늘의 메뉴 추천"):
    restaurants = ["🍽️슈마우스만찬","🍽️슈마우스만찬","🍽️슈마우스만찬", "🍽️정담식당","🍽️정담식당","🍽️정담식당","굶기"]
    random_restaurant = random.choice(restaurants)
# 랜덤 추천 식당 표시
    st.subheader(f"오늘의 추천은: {random_restaurant} 입니다.")


# 저장 파일 경로
SAVE_FILE = "saved_urls.json"

# 저장 함수
def save_urls(url1, url2):
    with open(SAVE_FILE, "w", encoding="utf-8") as f:
        json.dump({"url1": url1, "url2": url2}, f)

# 불러오기 함수
def load_urls():
    if Path(SAVE_FILE).exists():
        with open(SAVE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data.get("url1", ""), data.get("url2", "")
    return "", ""

# og:image 추출 함수
def get_og_image(url):
    headers = {
        'User-Agent': 'Mozilla/5.0',
        'Referer': 'https://pf.kakao.com/'
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        meta_tag = soup.find("meta", property="og:image")
        if meta_tag:
            return meta_tag.get("content")
        return None
    except Exception as e:
        st.error(f"오류 발생: {e}")
        return None

# 이미지 로딩 함수
def load_image_from_url(img_url):
    try:
        response = requests.get(img_url)
        img = Image.open(BytesIO(response.content))
        return img
    except Exception as e:
        return None

# 불러온 값 또는 기본값
default_url1, default_url2 = load_urls()
if default_url1 == "":
    default_url1 = "https://pf.kakao.com/_CiVis/108791568"
if default_url2 == "":
    default_url2 = "https://pf.kakao.com/_vKxgdn/108791400"



# UI 구성
st.title("오늘의 메뉴 이미지만 불러오기")

# 입력창 2개
col_input1, col_input2 = st.columns(2)

with col_input1:
    url1 = st.text_input("URL 1 입력", value=default_url1)
with col_input2:
    url2 = st.text_input("URL 2 입력", value=default_url2)

# 버튼 클릭 시 동작
if st.button("저장하고 이미지 가져오기"):
    # URL 저장
    save_urls(url1, url2)

    col_img1, col_img2 = st.columns(2)

    # URL 1 처리
    with st.spinner("URL 1 처리 중..."):
        img_url1 = get_og_image(url1)
        with col_img1:
            st.subheader("URL 1")
            if img_url1:
                img1 = load_image_from_url(img_url1)
                if img1:
                    st.image(img1, caption="🍽️슈마우스", width=350)
                    st.caption(f"[{img_url1}]({img_url1})")
                else:
                    st.warning("아직 메뉴가 공지되지 않았습니다.")
            else:
                st.warning("아직 메뉴가 공지되지 않았습니다.")

    # URL 2 처리
    with st.spinner("URL 2 처리 중..."):
        img_url2 = get_og_image(url2)
        with col_img2:
            st.subheader("URL 2")
            if img_url2:
                img2 = load_image_from_url(img_url2)
                if img2:
                    st.image(img2, caption="🍽️정담식당", width=300)
                    st.caption(f"[{img_url2}]({img_url2})")
                else:
                    st.warning("🍽️아직 메뉴가 공지되지 않았습니다.")
            else:
                st.warning("🍽️아직 메뉴가 공지되지 않았습니다.")

