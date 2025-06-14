import streamlit as st
import openai
import random
import os
from dotenv import load_dotenv
import base64

# 主角设定（随机MBTI，初始化后固定）
mbti_options = [
    "INTJ", "INTP", "ENTJ", "ENTP",
    "INFJ", "INFP", "ENFJ", "ENFP",
    "ISTJ", "ISFJ", "ESTJ", "ESFJ",
    "ISTP", "ISFP", "ESTP", "ESFP"
]

if "character_mbti" not in st.session_state:
    st.session_state.character_mbti = random.choice(mbti_options)
mbti_type = st.session_state.character_mbti

page_title = f"恋愛番組シミュレーション"

st.set_page_config(page_title=page_title, page_icon="🌹")

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = openai.OpenAI(api_key=api_key)

if "start" not in st.session_state:
    st.session_state.start = False
if "history" not in st.session_state:
    st.session_state.history = []
if "scene" not in st.session_state:
    st.session_state.scene = ""
if "episode_started" not in st.session_state:
    st.session_state.episode_started = False
if "rounds" not in st.session_state:
    st.session_state.rounds = 0
if "max_rounds" not in st.session_state:
    st.session_state.max_rounds = random.randint(2, 3)
if "generating" not in st.session_state:
    st.session_state.generating = False
if "reviewed" not in st.session_state:
    st.session_state.reviewed = False

with st.sidebar:
    st.header("你的角色设定")
    user_name = st.text_input("你的名字：", value="小萌")
    user_mbti = st.selectbox("你的MBTI类型：", mbti_options, index=1)
    user_job = st.text_input("你的职业：", value="")
    user_gender = st.selectbox("你的性别", ["女", "男"], index=0)
    user_language = st.selectbox("请选择语言 / 言語を選んでください", ["中文 (zh)", "日本語 (jp)"], index=0)
    # 添加音乐播放器到侧边栏
    # 音乐播放器已移至侧边栏，此处删除

    audio_file = open("tenderness.mp3", "rb")
    audio_bytes = audio_file.read()
    base64_audio = base64.b64encode(audio_bytes).decode()

    st.markdown(f"""
        <audio controls>
            <source src="data:audio/mp3;base64,{base64_audio}" type="audio/mp3">
            Your browser does not support the audio element.
        </audio>
    """, unsafe_allow_html=True)

    start_clicked = st.button("🌹 点击开始恋综之旅")
    if start_clicked:
        st.session_state.start = True
        st.rerun()

if not st.session_state.start:
    st.stop()

if user_gender == "男":
    st.title(f"🎬 バチェロレッテ - {mbti_type}")
else:
    st.title(f"🎬 バチェラー - {mbti_type}")

if not st.session_state.scene:
    episode_prompt = f"""
    你现在扮演一位恋爱真人秀节目的主角，节目名称为《逆転バチェロレッテ》。你的MBTI类型是{mbti_type}，你来设定一个比较有性格和性别特色的名字和职业。
    节目设定为：共有15位异性嘉宾争夺你的芳心，而你将通过多个阶段，逐步了解并淘汰不适合的异性嘉宾。最终你会选择最契合的人进入恋爱关系。
    现在你正在和其中一位异性嘉宾对话（用户扮演），对方的名字是{user_name}，mbti类型为{user_mbti}，职业是{user_job}。
    你通过与{user_name}的真实互动，对对方进行观察和测试，以判断自己是否喜欢对方。
    在对话中，你可以充分展现自己MBTI和性别的特点。性别的浓度可以高一点，比如女性可以更温柔、撒娇，男性可以更直接、幽默等。
    这次对话场景设定为Cocktail Party中的1对1场景。你可以聊一下任何你这个人设觉得应该聊的内容，比如工作、兴趣爱好、旅行经历等。你们之前已经有了一定了解，所以可以直接进入较为深入的对话。
    先自我介绍一下，然后开始先开启对话，只生成对话开始的部分。
    【风格基调】
    - 自然、有代入感，像真人在现场聊天。语句应流畅，随和，日常化（勾起恋爱的欲望，重要！）
    - 可以俏皮、真诚、迟疑、撒娇、挑逗等，但都应自然
    - 主角会根据对方异性嘉宾的mbti偏好，调整自己的表达方式（重要！）
    - 双方虽然是第一次见面，但设定为之前已经有了一定了解
    - 让主角接住异性嘉宾的情绪（重要！）
    - 不要像采访、主持，咨询或面试
    - 发言中，可以考虑加入细节动作
    - 角色不会像采访者一样频繁抛出“你有没有…”、“你觉得呢”这样的问题。
    - 你更倾向于用自己的情绪、回忆、行为来影响场景氛围，引发共鸣或冲突，而非引导对方自我揭示。
    - 你应以自己的感受和思考为出发点进行表达，而非依赖问题引导对话。
    - 推荐使用“我刚刚在想…”、“我有个奇怪的感觉…”、“刚才那一下，其实有点心动…”这类句式。
    - 你应以自己的感受和思考为出发点，例如：“我刚刚在想…”、“我总觉得你今天看起来特别不一样…”、“其实我也有点紧张，不知道你是不是看出来了”。
    - 请在每次发言中优先考虑你的语气变化、内心波动等表达形式。
    - 表达方式可包含迟疑、逞强、突然安静、强烈情绪或逃避反应等。
    """
    if user_language == "日本語 (jp)":
        episode_prompt += "请用日语表达。"
    if user_gender == "男":
        episode_prompt = "主角为女性" + episode_prompt
    else:
        episode_prompt = "主角为男性" + episode_prompt
    scene_resp = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": episode_prompt}],
        temperature=0.9
    )
    st.session_state.scene = scene_resp.choices[0].message.content.strip()

st.subheader("🎬 Episode 1")
st.markdown(f"{st.session_state.scene}\n\n")

if not st.session_state.episode_started:
    with st.form(key="first_input_form"):
        user_first_line = st.text_input("你想怎么回应？")
        submitted = st.form_submit_button("发送")

    if submitted and user_first_line:
        st.session_state.history.append({"role": "user", "content": user_first_line})
        st.session_state.episode_started = True
        st.session_state.generating = True
        st.rerun()

else:
    for msg in st.session_state.history:
        st.markdown("---")
        if msg["role"] == "assistant" and user_gender == "男":
            st.markdown(f"<div style='background-color:#fce4ec;color:#000;padding:10px;border-radius:10px'><strong> 对方：</strong> {msg['content']}</div>", unsafe_allow_html=True)
        elif msg["role"] == "user" and user_gender == "女":
            st.markdown(f"<div style='background-color:#fce4ec;color:#000;padding:10px;border-radius:10px'><strong> 你：</strong> {msg['content']}</div>", unsafe_allow_html=True)
        elif msg["role"] == "assistant" and user_gender == "女":        
            st.markdown(f"<div style='background-color:#e3f2fd;color:#000;padding:10px;border-radius:10px'><strong> 对方：</strong> {msg['content']}</div>", unsafe_allow_html=True)
        elif msg["role"] == "user" and user_gender == "女":    
            st.markdown(f"<div style='background-color:#e3f2fd;color:#000;padding:10px;border-radius:10px'><strong> 你：</strong> {msg['content']}</div>", unsafe_allow_html=True)
        
        if msg["role"] == "review":
            st.markdown(f"🔎 **专家点评：**\n\n{msg['content']}")

    if st.session_state.rounds >= st.session_state.max_rounds:
        if not st.session_state.reviewed:
            full_dialogue = "\n".join([
                f"{('对方' if msg['role']=='assistant' else '你')}：{msg['content']}"
                for msg in st.session_state.history if msg["role"] in ["user", "assistant"]
            ])
            review_prompt = (
                f"你是恋综节目《逆転バチェロレッテ》的专业评论员。请阅读以下对话历史，对这位名叫{user_name}的嘉宾在节目中的整体表现进行点评。请结合主角（MBTI为{mbti_type}）的性格特征，给出真实、中肯、有情感洞察力的评价，并且以满分为10分制给这名嘉宾打一个分，字数控制在150字以内。\n\n{full_dialogue}"
            )
            if user_language == "日本語 (jp)":
                review_prompt += "请用日语表达。"
            review = client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": review_prompt}],
                temperature=0.8
            )
            review_text = review.choices[0].message.content.strip()
            st.session_state.history.append({"role": "review", "content": review_text})
            st.session_state.reviewed = True
            st.markdown(f"🔎 **专家点评：**\n\n{review_text}")
        else:
            for msg in st.session_state.history:
                if msg["role"] == "review":
                    st.markdown(f"🔎 **专家点评：**\n\n{msg['content']}")
            st.stop()

    elif st.session_state.generating:
        messages = [
            {"role": "system", "content": f"场景是：{st.session_state.scene}。你要根据以下对话记录回应对方。"}
        ] + [
            {"role": msg["role"], "content": msg["content"]} for msg in st.session_state.history if msg["role"] in ["user", "assistant"]
        ]
        with st.spinner(f"对方正在回应..."):
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=messages,
                temperature=0.9
            )
            reply = response.choices[0].message.content.strip()
            st.session_state.history.append({"role": "assistant", "content": reply})
            st.session_state.rounds += 1
            st.session_state.generating = False
            st.rerun()

    else:
        with st.form(key="chat_form", clear_on_submit=True):
            user_input = st.text_input("你想怎么回应？")
            submitted = st.form_submit_button("发送")

        if submitted and user_input:
            st.session_state.history.append({"role": "user", "content": user_input})
            st.session_state.generating = True
            st.rerun()
