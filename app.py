import asyncio
import streamlit as st
import edge_tts

st.set_page_config(page_title="Edge TTS Studio", page_icon="🎙️", layout="centered")

st.title("🎙️ Edge TTS 웹 스튜디오")

# 사용자 정의 음성 딕셔너리
VOICE_DICT = {
    # [고음질 / 최신 HD & Multilingual 특화 음성]
    "101: en-US-AvaMultilingualNeural (여성 HD)": "en-US-AvaMultilingualNeural",
    "102: en-US-AndrewMultilingualNeural (남성 HD)": "en-US-AndrewMultilingualNeural",
    "103: en-US-EmmaMultilingualNeural (여성 HD)": "en-US-EmmaMultilingualNeural",
    "104: en-US-BrianMultilingualNeural (남성 HD)": "en-US-BrianMultilingualNeural",
    "105: en-IN-NeerjaExpressiveNeural (여성 HD)": "en-IN-NeerjaExpressiveNeural",

    # [한국어 - Korean]
    "1: ko-KR-SunHiNeural (여성 대표)": "ko-KR-SunHiNeural",
    "2: ko-KR-InJoonNeural (남성 대표)": "ko-KR-InJoonNeural",
    "3: ko-KR-HyunsuNeural (남성 차분함)": "ko-KR-HyunsuNeural",
    "4: ko-KR-BongJinNeural (남성 명확함)": "ko-KR-BongJinNeural",
    "5: ko-KR-JiMinNeural (여성 친근함)": "ko-KR-JiMinNeural",
    "6: ko-KR-SeoHyeonNeural (여성 안내 톤)": "ko-KR-SeoHyeonNeural",
    "7: ko-KR-GookMinNeural (남성 신뢰감)": "ko-KR-GookMinNeural",

    # [미국 영어 - English (US)]
    "10: en-US-JennyNeural (여성 대표)": "en-US-JennyNeural",
    "11: en-US-GuyNeural (남성 대표)": "en-US-GuyNeural",
    "12: en-US-AriaNeural (여성 표현력)": "en-US-AriaNeural",
    "13: en-US-ChristopherNeural (남성 편안함)": "en-US-ChristopherNeural",
    "14: en-US-SteffanNeural (남성 오디오북)": "en-US-SteffanNeural",

    # [영국 / 호주 영어]
    "20: en-GB-SoniaNeural (영국 여성)": "en-GB-SoniaNeural",
    "21: en-GB-RyanNeural (영국 남성)": "en-GB-RyanNeural",
    "30: en-AU-NatashaNeural (호주 여성)": "en-AU-NatashaNeural",
    "31: en-AU-WilliamNeural (호주 남성)": "en-AU-WilliamNeural",
}

async def generate_tts(text, voice_id, rate, pitch, volume):
    rate_str = f"{rate:+d}%"
    pitch_str = f"{pitch:+d}Hz"
    volume_str = f"{volume:+d}%"
    output_path = "output.mp3"
    
    communicate = edge_tts.Communicate(text, voice_id, rate=rate_str, pitch=pitch_str, volume=volume_str)
    await communicate.save(output_path)
    return output_path

# 입력 옵션
uploaded_file = st.file_uploader(".txt 파일 업로드", type=["txt"])
input_text = st.text_area("또는 텍스트 직접 입력", height=150, placeholder="변환할 내용을 입력하세요...")

# 기본 음성을 103번(Emma)으로 설정
default_voice_key = "103: en-US-EmmaMultilingualNeural (여성 HD)"
default_index = list(VOICE_DICT.keys()).index(default_voice_key)

selected_voice_label = st.selectbox("목소리 선택", list(VOICE_DICT.keys()), index=default_index)
voice_id = VOICE_DICT[selected_voice_label]

# 세부 설정 슬라이더 (기본값: rate 0%, pitch +12Hz, volume -50%)
col1, col2, col3 = st.columns(3)
with col1:
    rate = st.slider("속도 (%)", -50, 50, 0, step=5)
with col2:
    pitch = st.slider("피치 (Hz)", -50, 50, 12, step=1)
with col3:
    volume = st.slider("볼륨 (%)", -100, 50, -50, step=5)

# 실행 및 다운로드
if st.button("🎧 MP3 음성 생성", type="primary", use_container_width=True):
    text_content = ""
    if uploaded_file is not None:
        text_content = uploaded_file.read().decode("utf-8").strip()
    elif input_text.strip():
        text_content = input_text.strip()

    if not text_content:
        st.warning("⚠️ 텍스트를 입력하거나 .txt 파일을 업로드해 주세요.")
    else:
        with st.spinner("음성을 생성하고 있습니다..."):
            file_path = asyncio.run(generate_tts(text_content, voice_id, rate, pitch, volume))
            st.success("✅ 변환 완료!")
            
            st.audio(file_path, format="audio/mp3")
            
            with open(file_path, "rb") as f:
                st.download_button(
                    label="📥 MP3 파일 다운로드",
                    data=f,
                    file_name="output.mp3",
                    mime="audio/mp3",
                    use_container_width=True
                )
