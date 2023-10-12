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

        # 正解か不正解を判定する処理を行う
        user_answer = request.form['answer']
        is_correct = user_answer == str(answer)

        # 正解なら連続正解の数を1増やし、正解の画面に遷移
        if is_correct:
            coutinue_correct += 1
            return redirect(url_for('correct'))
        # 不正解なら連続正解の数を1減らし、不正解の画面に遷移
        else:
            if coutinue_correct >= 1:
                coutinue_correct -= 1
            #elif coutinue_correct == 1:
            #    coutinue_correct -= 1
            return redirect(url_for('incorrect'))

    # 課題が既定の数行ったら、スタート画面に戻る
    if num == repeat:
        num = 0
        return render_template('start.html')

    # coutinue_correct(連続正解数)が6以上なら３桁の暗算
    if coutinue_correct >= 6:
        random_integer1 = random.randint(100, 999)
        random_integer2 = random.randint(100, 999)
    # coutinue_correct(連続正解数)が3~5なら３桁と２桁の暗算
    elif coutinue_correct >= 3:
        random_integer1 = random.randint(100, 999)
        random_integer2 = random.randint(10, 99)
    # coutinue_correct(連続正解数)がそれた以下なら２桁の暗算
    else:
        random_integer1 = random.randint(10, 99)
        random_integer2 = random.randint(10, 99)

    # ランダムで生成した数によって加算か減算か判断
    factor = random.randint(1, 2)

    if factor == 1:
        answer = random_integer1 + random_integer2
        return render_template('quiz.html', sentence = f"{random_integer1} + {random_integer2} =")
    else:
        if random_integer1 < random_integer2:
            random_integer1, random_integer2 = random_integer2, random_integer1
        answer = random_integer1 - random_integer2
        return render_template('quiz.html', sentence = f"{random_integer1} - {random_integer2} =")

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
