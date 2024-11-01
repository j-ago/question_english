import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Function to calculate dosha percentages
def calculate_dosha_percentages(df, responses):
    """
    Calculate the percentages of Vata, Pitta, and Kapha based on the user's responses.
    """
    df_responses = df.copy()
    df_responses['Vata_Response'] = responses['Vata']
    df_responses['Pitta_Response'] = responses['Pitta']
    df_responses['Kapha_Response'] = responses['Kapha']
    
    # Calculate the total scores for Vata, Pitta, and Kapha
    vata_score = df_responses['Vata_Response'].sum()
    pitta_score = df_responses['Pitta_Response'].sum()
    kapha_score = df_responses['Kapha_Response'].sum()
    
    total_score = vata_score + pitta_score + kapha_score
    
    if total_score == 0:
        # Avoid division by zero
        return 0, 0, 0
    
    # Calculate percentages
    vata_percentage = (vata_score / total_score) * 100
    pitta_percentage = (pitta_score / total_score) * 100
    kapha_percentage = (kapha_score / total_score) * 100
    
    return vata_percentage, pitta_percentage, kapha_percentage

# Function to display the Dosha description
def display_dosha_description(dosha, texts, language):
    """
    Display the description of each Dosha based on the selected language.
    """
    st.write(texts[language]['doshas'][dosha])

# Load the Japanese and English Excel files
japanese_file_path = 'daiagnosis_rawdata.xlsx'
english_file_path = 'daiagnosis_rawdata_translated.xlsx'

# Load Japanese data
try:
    df_japanese = pd.read_excel(japanese_file_path)
except FileNotFoundError:
    st.error(f"指定された日本語のファイルが見つかりません: {japanese_file_path}")
    st.stop()

# Load English data
try:
    df_english = pd.read_excel(english_file_path)
except FileNotFoundError:
    st.error(f"指定された英語のファイルが見つかりません: {english_file_path}")
    st.stop()

# 言語設定
languages = ['English', '日本語']
default_language = '日本語'

# テキスト辞書
texts = {
    'English': {
        'title': 'Body Type Diagnosis Questionnaire (Simple Version 2024)',
        'description': 'Please read each question and select the "Situation/State" that is closest to your current self.',
        'button': 'Show Diagnosis Result',
        'doshas': {
            'Vata': 'Vata is a body type with the energy of wind and air, symbolizing movement and change. Imaginative and active, but tends to have anxiety and insomnia.',
            'Pitta': 'Pitta is a body type with the energy of fire and water, symbolizing transformation and metabolism. Possesses strong leadership and decisiveness, but can become easily angry.',
            'Kapha': 'Kapha is a body type with the energy of water and earth, symbolizing stability and endurance. Calm and patient, but may tend to be lazy.',
            'Tri Dosha': 'Tri Dosha is an ideal body type with balanced presence of Vata, Pitta, and Kapha. Health and stability are easily maintained, but overall balance is important.'
        },
        'result': 'Your body type is: {dosha}',
        'failure': 'Diagnosis failed.',
        'links': {
            'Vata': 'Here is the [Vata body type diagnosis app](https://fklvzgcyknq9f8zkwsrjm6.streamlit.app/).',
            'Pitta': 'Here is the [Pitta body type diagnosis app](https://lpgh4bpuay8cfqxf7cbhoz.streamlit.app/).',
            'Kapha': 'Here is the [Kapha body type diagnosis app](https://amh8axxvtmeda9te6l4wrk.streamlit.app/).'
        }
    },
    '日本語': {
        'title': '体質診断質問票（簡易版2024）',
        'description': '各質問内容を見て、今の自分に最も近い「状況・状態」を選んでください。',
        'button': '診断結果を表示',
        'doshas': {
            'Vata': 'Vataは風や空気のエネルギーを持つ体質で、動きや変化を象徴します。想像力豊かで活動的ですが、不安や不眠になりやすい傾向があります。',
            'Pitta': 'Pittaは火と水のエネルギーを持つ体質で、変換や代謝を象徴します。強いリーダーシップと決断力を持ちますが、怒りっぽくなることがあります。',
            'Kapha': 'Kaphaは水と地のエネルギーを持つ体質で、安定性や持久力を象徴します。穏やかで忍耐強いですが、怠けがちになることがあります。',
            'Tri Dosha': 'Tri DoshaはVata、Pitta、Kaphaがバランスよく存在する理想的な体質です。健康と安定が保たれやすいですが、全体のバランスが重要です。'
        },
        'result': 'あなたの体質は: {dosha}',
        'failure': '診断に失敗しました。',
        'links': {
            'Vata': 'Vataの体質診断アプリはこちら： [リンク](https://fklvzgcyknq9f8zkwsrjm6.streamlit.app/)。',
            'Pitta': 'Pittaの体質診断アプリはこちら： [リンク](https://lpgh4bpuay8cfqxf7cbhoz.streamlit.app/)。',
            'Kapha': 'Kaphaの体質診断アプリはこちら： [リンク](https://amh8axxvtmeda9te6l4wrk.streamlit.app/)。'
        }
    }
}

# Doshaの日本語名
dosha_names_japanese = {
    'Vata': 'ヴァータ',
    'Pitta': 'ピッタ',
    'Kapha': 'カパ',
    'Tri Dosha': 'トリ・ドーシャ'
}

# Streamlit UIのヘッダー部分に言語選択プルダウンを追加
st.set_page_config(layout="wide")  # レイアウトをワイドに設定

with st.container():
    col1, col2 = st.columns([3, 1])
    with col1:
        pass  # 左側のカラムは空白
    with col2:
        # 言語選択のラベルを追加
        st.write("言語 - Language")  # 追加部分
        language = st.selectbox('', options=languages, index=languages.index(default_language))

# ロードする言語のテキストを設定
current_text = texts[language]

# アプリケーションのタイトル
st.title(current_text['title'])

# アプリケーションの説明文
st.write(current_text['description'])

# 質問データを言語に応じて選択
df = df_japanese if language == '日本語' else df_english

# 回答を格納する辞書
responses = {
    'Vata': [],
    'Pitta': [],
    'Kapha': []
}

# 各質問を表示し、ラジオボタンで回答を収集
for i in range(len(df)):
    if language == '日本語':
        question_text = f"質問 {i+1}: {df.iloc[i, 1]}"
        select_text = "選択してください:"
    else:
        question_text = f"Question {i+1}: {df.iloc[i, 1]}"
        select_text = "Please select:"
    
    st.write(question_text)  # 質問を表示
    
    # 選択肢の表示（言語に応じた選択肢を使用）
    choice = st.radio(
        select_text, 
        options=['Vata', 'Pitta', 'Kapha'], 
        format_func=lambda x: {
            'Vata': df.iloc[i, 2],   # Column 3 for Vata
            'Pitta': df.iloc[i, 4],  # Column 5 for Pitta
            'Kapha': df.iloc[i, 6]   # Column 7 for Kapha
        }[x], 
        key=f'choice_{i}',
        label_visibility="collapsed"  # ラベルを非表示にしてUIをすっきりさせる
    )
    
    # 回答に基づいてカウント
    responses['Vata'].append(1 if choice == 'Vata' else 0)
    responses['Pitta'].append(1 if choice == 'Pitta' else 0)
    responses['Kapha'].append(1 if choice == 'Kapha' else 0)

# 診断結果を表示するボタン
if st.button(current_text['button']):
    # Doshaの割合を計算
    vata_percentage, pitta_percentage, kapha_percentage = calculate_dosha_percentages(df, responses)
    
    # 割合を表示
    if language == '日本語':
        st.write(f'ヴァータ: {vata_percentage:.2f}%')
        st.write(f'ピッタ: {pitta_percentage:.2f}%')
        st.write(f'カパ: {kapha_percentage:.2f}%')
    else:
        st.write(f'Vata: {vata_percentage:.2f}%')
        st.write(f'Pitta: {pitta_percentage:.2f}%')
        st.write(f'Kapha: {kapha_percentage:.2f}%')
    
    # 円グラフを表示（ラベルは常に英語）
    labels = ['Vata', 'Pitta', 'Kapha']  # 常に英語で表示
    sizes = [vata_percentage, pitta_percentage, kapha_percentage]
    colors = ['#ff9999','#66b3ff','#99ff99']
    
    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', colors=colors, startangle=90)
    ax.axis('equal')  # 円グラフを円形に保つ
    
    st.pyplot(fig)
    
    # Doshaを判定して説明を表示
    # まずTri Doshaをチェック
    if 28 <= vata_percentage <= 38 and 28 <= pitta_percentage <= 38 and 28 <= kapha_percentage <= 38:
        doshas = ['Tri Dosha']
    else:
        # 最大割合を見つける
        max_percentage = max(vata_percentage, pitta_percentage, kapha_percentage)
        # 最大割合を持つDoshaをリストに追加
        doshas = []
        if vata_percentage == max_percentage:
            doshas.append('Vata')
        if pitta_percentage == max_percentage:
            doshas.append('Pitta')
        if kapha_percentage == max_percentage:
            doshas.append('Kapha')
    
    # Doshaが決定された場合
    if doshas:
        if 'Tri Dosha' in doshas:
            dosha = 'Tri Dosha'
            st.write(current_text['result'].format(dosha=dosha))
            display_dosha_description(dosha, texts, language)
        else:
            if language == 'English':
                dosha_text = ' and '.join(doshas)
            else:
                dosha_text = ' と '.join([dosha_names_japanese[d] for d in doshas])
            st.write(current_text['result'].format(dosha=dosha_text))
            for d in doshas:
                display_dosha_description(d, texts, language)
        
        # 判定されたDoshaに応じてリンクを表示
        for d in doshas:
            if d in ['Vata', 'Pitta', 'Kapha']:
                link_text = current_text['links'][d]
                st.markdown(link_text)
    else:
        st.write(current_text['failure'])
