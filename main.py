
import streamlit as st
from utility import copywriting_generator, title_template, copywriting_template

st.title("short video script generator 🎞️")

with st.sidebar:
    openai_api_key = st.text_input("Please input your OpenAI API key: ", type="password")
    st.markdown("[Click here to get your own OpenAI api key](https://platform.openai.com/account/api-keys)")
    # if not openai_api_key:
    #     st.write(f"請至以下網站取得你個人OPENAI API 金鑰 https://platform.openai.com/account/api-keys")

st.divider()
theme = st.text_input("🔥Please input your video theme🔥")
short_video_length = st.number_input("⏱️Please input the desired length of the short video (in minutes). ⏱️",
                                     min_value=0.2, step=0.2)
# short_video_length=st.number_input("⏱️請輸入你想要的短影片長度(分鐘) ⏱️",min_value=0.2,step=0.2)

temperature = st.slider(
    "🧠💡Please input the creativity level of the short video (a higher value indicates greater creativity) 💡🧠",
    min_value=0.0, max_value=1.2, value=0.5, step=0.1)
# temperature=st.slider("🧠💡請輸入短影片的創造力(數值越大代表創造力越高) 💡🧠",min_value=0.0,max_value=1.2,value=0.5,step=0.1)



submit = st.button("📃 Generate a short video script 📃")

# submit = st.button("📃 產生短影音文本 📃")


if submit and not openai_api_key:
    st.info("Please input your OpenAI API key: ")
    # st.info("请输入你的OPENAI API 金鑰")
    st.stop()
if submit and not theme:
    st.info("Please input your video theme")
    # st.info("请输入短影音主題")
    st.stop()
if submit and not short_video_length >= 0.2:
    st.info("The length of the short video needs to be greater than or equal to 0.2")

    # st.info("短影音長度需要大於或等於0.2")
    st.stop()
if submit:
    with st.spinner("AI is running, please wait for a minute... "):
        # with st.spinner("AI正在運行中，請稍後..."):
        search_result, title, script = copywriting_generator(theme, short_video_length, temperature, openai_api_key)
    st.success("Short video script completed")
    # st.success("短影音文本 已完成！")
    st.subheader("Theme🔥：")
    # st.subheader("主題🔥：")
    st.write(title)
    st.subheader("Short video script 📃：")

    st.write(script)
    with st.expander("Wikipedia search results "):

        st.info(search_result)

