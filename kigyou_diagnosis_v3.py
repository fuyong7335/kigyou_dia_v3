import streamlit as st
import plotly.graph_objects as go

# --- ページ設定 ---
st.set_page_config(page_title="起業タイプ診断", layout="centered")
st.title("起業タイプ診断")
st.write("以下の質問に、顔のアイコンであなたの気持ちの度合いを選んでください（左＝まったく当てはまらない　右＝とてもそう思う）。")

# ================================
# 質問セット（5カテゴリ × 10問 = 50問）
# ================================
question_set = {
    "性格傾向": [
        "新しいことを自分で調べて試すことが多い",
        "初対面の人と自然に会話を楽しめる方だ",
        "計画を立ててから行動したいと思う",
        "自分の直感を頼りに決断することがある",
        "何か失敗したとき、自分の責任だと考えやすい",
        "興味を持ったことは、すぐに行動に移してみたくなる",
        "未知の状況でも、なんとかなると楽観的に捉えられる",
        "人と競争するより、自分のペースで進めたい",
        "変化や新しい環境に適応するのが早い方だと思う",
        "物事を多角的に考えてから結論を出したい",
    ],
    "価値観": [
        "自由な働き方を重視したいと感じる",
        "人に感謝されることでやりがいを感じる",
        "ルールが多いとストレスを感じる",
        "お金よりも、自分が納得できる仕事を優先したい",
        "仕事は成長の場だと考えている",
        "誰かの役に立っている実感がないと物足りなさを感じる",
        "決められた枠の中で働くより、自分でルールを作りたい",
        "社会的な評価より、自分の価値基準を大切にしたい",
        "収入の安定より、意味を感じられる仕事を選びたい",
        "自分らしさを表現できることに強く惹かれる",
    ],
    "本気度": [
        "起業について以前から考え続けている",
        "今が行動を起こすタイミングだと思う",
        "不安があってもチャレンジしたい気持ちがある",
        "すでに何らかの準備や調査を始めている",
        "環境が整えばすぐにでも始めたいと感じる",
        "起業に関する情報やセミナーに積極的に触れている",
        "周りに起業の意思を話し始めている",
        "今の仕事や環境に、そろそろ区切りをつけたいと感じている",
        "小さくてもいいので、まず一歩踏み出したいと思っている",
        "起業した後の生活を具体的にイメージすることがある",
    ],
    "仕事スタイル": [
        "一人で計画を実行することに抵抗が少ない",
        "マイペースに仕事を進めるのが心地よい",
        "困ったときは自分で解決策を考えることが多い",
        "集中して自分の世界に没頭する時間が好きだ",
        "チームより個人での裁量を重視したい",
        "誰かに指示されるより、自分で優先順位を決めたい",
        "在宅やカフェなど、場所にとらわれない働き方に魅力を感じる",
        "スケジュールを自分の裁量で調整できる方が力を発揮できる",
        "細かく管理されるより、任される方がやる気が出る",
        "複数のことを同時に進めるより、一つに集中したい",
    ],
    "思考の癖": [
        "どうせ私には無理だと思うことがある",
        "うまくいかないとき、自分を責めることが多い",
        "他人と比べて落ち込むことがよくある",
        "失敗を恐れて行動できないことがある",
        "本当はやりたいのに一歩が踏みだせないことがある",
        "完璧にできないくらいなら、やらない方がましだと思うことがある",
        "人の評価が気になって、本音を出せないことがある",
        "過去の失敗が頭から離れず、慎重になりすぎることがある",
        "「もっと準備が必要だ」と先延ばしにしてしまうことがある",
        "自分の意見よりも、周りの意見に合わせてしまうことがある",
    ],
}

TYPE_AXES = ["性格傾向", "価値観", "仕事スタイル"]

# 上位2軸（＝最下位1軸を除いた組み合わせ）からタイプを決定
# キーは「相対的にスコアが最も低かった軸」
TYPES = {
    "仕事スタイル": {
        "name": "情熱ビジョナリー型",
        "text": """
あなたは、「なぜやるのか」という意味や想いを大切にしながら、自分から新しいことに飛び込んでいけるタイプです。誰かに背中を押されるのを待つより、自分の中に生まれた「これをやりたい」という気持ちを原動力に動き出せる人です。

起業においては、まだ形になっていない構想段階から周囲を巻き込みながら進めていく力になります。特に、社会的な意義や自分の価値観に合った事業ほど、驚くほどの粘り強さを発揮するでしょう。

一方で、仕事の進め方そのものにはまだ自分なりの型ができていないこともあります。最初はチームや外部の力を借りながら、自分に合ったペースやスタイルを探っていくと、より力を発揮しやすくなります。
""",
    },
    "価値観": {
        "name": "自走アクション型",
        "text": """
あなたは、頭で考えるより先に手を動かして確かめていくタイプです。そして、誰かに管理されるよりも、自分で段取りを決めて、自分のペースで進めるときに一番力を発揮します。

起業においては、小さく試して、修正して、また試すというサイクルを自分ひとりで回していける強みになります。市場やお客さんの反応を見ながら、スピーディーに事業を形にしていけるでしょう。

一方で、「これは絶対にやりたい」という核となる想いや価値観が、まだ言葉になっていないこともあります。行動しながらでも構わないので、時々立ち止まって「自分は何のためにこれをやっているのか」を言葉にしてみると、事業に一本の軸が通っていきます。
""",
    },
    "性格傾向": {
        "name": "自分軸クラフト型",
        "text": """
あなたは、自分が心から納得できることを、自分のペースでじっくり形にしていきたいタイプです。周りの評価や一般的な正解よりも、自分の中にある基準を大切にしながら、着実に積み上げていく力があります。

起業においては、流行りに流されず、自分らしさや専門性を活かした事業をコツコツと育てていく強みになります。長く続けられる、意味のある仕事を作っていける人です。

一方で、最初の一歩を踏み出すまでに時間がかかったり、新しいことに飛び込む勢いはやや控えめなこともあります。完璧に準備が整うのを待つより、「6割できたら動いてみる」くらいの気持ちで小さく試してみると、着実な強みがより早く形になっていきます。
""",
    },
}


def score_category(responses: dict, start_idx: int) -> float:
    total = sum(responses[start_idx + i] for i in range(10))
    avg = total / 10
    return (avg - 1) * 25  # 1〜5 の回答を 0〜100 に換算


def determine_type(scores: dict) -> dict:
    # TYPE_AXES の中で最もスコアが低い軸を「除外軸」とし、そこからタイプを決める
    lowest_axis = min(TYPE_AXES, key=lambda axis: scores[axis])
    return TYPES[lowest_axis]


def readiness_comment(score: float) -> str:
    if score >= 70:
        return "今まさに、一歩を踏み出すタイミングを迎えているようです。少しずつでも行動に移してみることをおすすめします。"
    elif score >= 40:
        return "起業への気持ちは育ちつつある段階です。情報収集や小さな行動を重ねながら、タイミングを見極めていくとよいでしょう。"
    else:
        return "今はまだ、じっくり考える時期なのかもしれません。焦らず、自分にとって本当に大切なことを見つめる時間も大切です。"


def mindset_comment(score: float) -> str:
    if score >= 60:
        return "自分を責めたり、一歩を踏みとどまらせるような考え方のクセが、少し強めに出やすいようです。これは性格の欠点ではなく、多くの人が持っている自然な反応です。ただ、起業のように正解のない道を進むときには、この考え方のクセが行動のブレーキになることがあります。"
    elif score >= 30:
        return "誰にでもあるような、自分を疑ってしまう瞬間が時々顔を出すようです。無理に消そうとせず、「またこの考えが出てきたな」と気づけるだけでも、行動への影響は小さくなっていきます。"
    else:
        return "比較的、自分を否定する考え方に振り回されにくいタイプのようです。この強みを活かして、これからも自分のペースで挑戦を重ねていけるでしょう。"


# ================================
# 回答（顔アイコン5段階：st.feedback／カテゴリごとに1ページずつ表示）
# ================================
categories = list(question_set.keys())
total_steps = len(categories)

if "step" not in st.session_state:
    st.session_state.step = 0
if "answers" not in st.session_state:
    st.session_state.answers = {}

step = st.session_state.step

if step < total_steps:
    category = categories[step]
    questions = question_set[category]
    start_idx = sum(len(question_set[c]) for c in categories[:step]) + 1

    st.progress(step / total_steps)
    st.caption(f"ステップ {step + 1} / {total_steps}")
    st.markdown(f"### {category}")

    current_responses = {}
    for i, question in enumerate(questions):
        q_num = start_idx + i
        st.write(f"No.{q_num} {question}")
        value = st.feedback("faces", key=f"Q{q_num}")
        # 未回答（None）は中間の「3」として扱う
        current_responses[q_num] = (value if value is not None else 2) + 1

    col1, col2 = st.columns([1, 1])
    with col1:
        if step > 0 and st.button("戻る"):
            st.session_state.answers.update(current_responses)
            st.session_state.step -= 1
            st.rerun()
    with col2:
        button_label = "次へ" if step < total_steps - 1 else "診断する"
        if st.button(button_label):
            st.session_state.answers.update(current_responses)
            st.session_state.step += 1
            st.rerun()

# ================================
# 結果表示
# ================================
if step >= total_steps:
    responses = st.session_state.answers
    scores = {}
    idx = 1
    for category in question_set:
        scores[category] = score_category(responses, idx)
        idx += 10

    diagnosed_type = determine_type(scores)

    st.markdown("---")
    st.subheader(f"あなたのタイプは「{diagnosed_type['name']}」")
    st.write(diagnosed_type["text"])

    # --- レーダーチャート（タイプ判定に使う3軸のみ） ---
    cats = TYPE_AXES.copy()
    vals = [scores[c] for c in cats]
    cats.append(cats[0])
    vals.append(vals[0])
    fig = go.Figure(
        data=[go.Scatterpolar(r=vals, theta=cats, fill="toself")],
        layout=go.Layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
            showlegend=False,
            dragmode=False,
        ),
    )
    fig.update_layout(uirevision=True)
    st.subheader("タイプを構成する3つの軸")
    st.plotly_chart(fig, use_container_width=True, config={"staticPlot": True})

    # --- 本気度ゲージ ---
    st.subheader("今の起業準備度")
    readiness = scores["本気度"]
    st.progress(int(readiness) / 100)
    st.write(f"{int(readiness)}%")
    st.write(readiness_comment(readiness))

    # --- 思考の癖 ---
    st.subheader("気づいておきたい心のクセ")
    st.write(mindset_comment(scores["思考の癖"]))

    st.markdown("---")
    st.write("この診断は、あなたの今の傾向を知るための「目安」です。答えは一つではありません。気づいたことをきっかけに、次の一歩を考えてみてくださいね。")

    if st.button("もう一度診断する"):
        st.session_state.step = 0
        st.session_state.answers = {}
        st.rerun()
