import streamlit as st
import whisper
import yt_dlp
import os
from googletrans import Translator
from gtts import gTTS

st.set_page_config(page_title="YouTube بالعربي", layout="centered")
st.title("🎬 YouTube مع صوت عربي – Streamlit")

youtube_url = st.text_input("📺 أدخل رابط فيديو YouTube (مسجّل)")

if youtube_url and st.button("ابدأ"):
    with st.spinner("⏳ المعالجة..."):
        audio_file = "audio.mp3"
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': audio_file,
            'postprocessors': [{'key':'FFmpegExtractAudio','preferredcodec':'mp3'}],
            'quiet': True
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([youtube_url])

        model = whisper.load_model("base")
        result = model.transcribe(audio_file)
        orig_text = result["text"]

        translator = Translator()
        ar_text = translator.translate(orig_text, dest='ar').text

        voice_file = "voice.mp3"
        gTTS(text=ar_text, lang='ar').save(voice_file)

        if "v=" in youtube_url:
            vid = youtube_url.split("v=")[-1]
        elif "youtu.be/" in youtube_url:
            vid = youtube_url.split("youtu.be/")[-1]
        else:
            vid = None

        if vid:
            st.video(f"https://www.youtube.com/watch?v={vid}")
        st.audio(voice_file, format="audio/mp3")

        with open(voice_file, "rb") as f:
            st.download_button("📥 تحميل الصوت", f, file_name="arabic_voiceover.mp3")

        os.remove(audio_file)
        os.remove(voice_file)
