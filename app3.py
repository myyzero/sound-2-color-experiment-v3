import streamlit as st
import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import io

st.set_page_config(page_title="音频颜色联想实验", layout="centered")

st.title("🎧 音频颜色联想实验")
st.write("点击按钮播放音频，音频播放结束后，请选择你联想到的颜色，然后点击提交。")

# 播放音频
audio_file = open("your-audio.mp3", "rb")  # 请将你的音频文件命名为 your-audio.mp3 并放在同目录或相对路径下
st.audio(audio_file.read(), format="audio/mp3")

# 颜色选择器
color = st.color_picker("🎨 请选择你联想到的颜色", "#ffffff")

# 初始化 session_state 存储数据
if "records" not in st.session_state:
    st.session_state.records = []

# Google Sheets 设置
SHEET_ID = "1ga4yQT0oUc3X1a1kEO6FdP3vzxdTAV3AwxQ4W2jo_-Q"  # 👈 请替换为你的 Sheet ID
SHEET_NAME = "Sound2ColorOutcome"              # 👈 请确保工作表名正确

# 连接 Google Sheets
def connect_to_gsheet():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("streamlitcolorapp-0a350e473431.json", scope)  # 👈 替换文件名
    client = gspread.authorize(creds)
    sheet = client.open_by_key(SHEET_ID).worksheet(SHEET_NAME)
    return sheet

# 提交按钮
if st.button("✅ 提交你的颜色"):

    # 分解 RGB
    r = int(color[1:3], 16)
    g = int(color[3:5], 16)
    b = int(color[5:7], 16)
    timestamp = datetime.datetime.now().isoformat()

    try:
        sheet = connect_to_gsheet()
        sheet.append_row([timestamp, color, r, g, b])
        st.success("✅ 你的数据已成功保存到 Google 表格！感谢参与！")

        # 同时保存到本地内存
        st.session_state.records.append({
            "timestamp": timestamp,
            "hex_color": color,
            "r": r,
            "g": g,
            "b": b
        })
    except Exception as e:
        st.error(f"❌ 数据保存失败：{e}")

# 如果内存有数据，生成 CSV 并提供下载
if st.session_state.records:
    df = pd.DataFrame(st.session_state.records)
    csv_buffer = io.StringIO()
    df.to_csv(csv_buffer, index=False)
    csv_data = csv_buffer.getvalue()

    st.download_button(
        label="⬇️ 下载已提交的数据 CSV 文件",
        data=csv_data,
        file_name="submitted_colors.csv",
        mime="text/csv"
    )
