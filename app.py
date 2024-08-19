import random
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

answer = None
coutinue_correct = 2
num = 0

# 最初のスタート画面
@app.route('/')
def index():
    return render_template('start.html')

# 計算式が映し出される画面
@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    global answer # 計算の答えを記憶
    global num # 今何回目の課題かを記憶
    global coutinue_correct # 連続で正解している回数を記憶(2で初期化)
    repeat = 8 # 計算を繰り返す回数

    if request.method == 'POST':

        num += 1

        # タイムアウトや不正解を判定する処理
        user_answer = request.form['answer']
        is_correct = user_answer == str(answer)

        # タイムアウトまたは不正解なら、連続正解の数を1減らし、不正解の画面に遷移
        if user_answer == 'timeout' or not is_correct:
            if coutinue_correct >= 1:
                coutinue_correct -= 1
            return redirect(url_for('incorrect'))
        # 正解なら連続正解の数を1増やし、正解の画面に遷移
        else:
            coutinue_correct += 1
            return redirect(url_for('correct'))

    # 課題が既定の数行ったら、スタート画面に戻る
    if num == repeat:
        num = 0
        return render_template('start.html')

    # coutinue_correct(正解数)の数に応じて暗算の桁数を変え、難易度を変化させる
    if coutinue_correct >= 12:
        random_integer1 = random.randint(1000, 9999)
        random_integer2 = random.randint(1000, 9999)

    elif coutinue_correct >= 9:
        random_integer1 = random.randint(1000, 9999)
        random_integer2 = random.randint(100, 999)

    elif coutinue_correct >= 6:
        random_integer1 = random.randint(100, 999)
        random_integer2 = random.randint(100, 999)

    elif coutinue_correct >= 3:
        random_integer1 = random.randint(100, 999)
        random_integer2 = random.randint(10, 99)

    else:
        random_integer1 = random.randint(10, 99)
        random_integer2 = random.randint(10, 99)

    # ランダムで生成した数によって加算か減算か判断
    factor = random.randint(1, 2)

    if factor == 1:
        answer = random_integer1 + random_integer2
        sentence = f"{random_integer1} + {random_integer2} ="
    else:
        if random_integer1 < random_integer2:
            random_integer1, random_integer2 = random_integer2, random_integer1
        answer = random_integer1 - random_integer2
        sentence = f"{random_integer1} - {random_integer2} ="

    # 正解を含む選択肢を生成
    choices = [answer]
    while len(choices) < 5:
        fake_answer = answer + random.randint(-10, 10)
        if fake_answer != answer and fake_answer not in choices:
            choices.append(fake_answer)

    # 選択肢をランダムにシャッフル
    random.shuffle(choices)

    return render_template('quiz.html', sentence=sentence, choices=choices)

# 正解画面
@app.route('/correct')
def correct():
    return render_template('result.html', result='〇')

# 不正解画面
@app.route('/incorrect')
def incorrect():
    return render_template('result.html', result='×')

if __name__ == '__main__':
    app.run(debug=True)
