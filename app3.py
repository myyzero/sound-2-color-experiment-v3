import streamlit as st
import pandas as pd
import datetime

st.set_page_config(page_title="Sound-Color Association Experiment", layout="centered")

st.title("🎧 Sound and Color Association Experiment")

# 设定三组声音编号
sound_numbers = [1, 2, 3]

# 记录所有颜色选择
colors = []

for sound_num in sound_numbers:
    st.markdown(f"### Listen to Sound {sound_num} and select the color you associate with it 👇")
    audio_file = open(f"your-audio-{sound_num}.mp3", "rb")
    st.audio(audio_file.read(), format="audio/mp3")

    color = st.color_picker(f"🎨 Select color for Sound {sound_num}", "#ffffff", key=f"color_{sound_num}")
    colors.append((sound_num, color))

# 提交按钮
if st.button("✅ Submit your colors"):
    all_data = []
    for sound_num, color in colors:
        r = int(color[1:3], 16)
        g = int(color[3:5], 16)
        b = int(color[5:7], 16)

        data = {
            "timestamp": datetime.datetime.now().isoformat(),
            "sound_number": sound_num,
            "hex": color,
            "r": r,
            "g": g,
            "b": b
        }
        all_data.append(data)

    try:
        df = pd.read_csv("responses.csv")
        df = pd.concat([df, pd.DataFrame(all_data)], ignore_index=True)
    except FileNotFoundError:
        df = pd.DataFrame(all_data)

    df.to_csv("responses.csv", index=False)
    st.success("✅ Your colors have been saved. Thank you for participating!")
