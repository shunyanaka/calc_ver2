import random
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

answer = None
coutinue_correct = 2
num = 0

@app.route('/')
def index():
    return render_template('start.html')

@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    global answer
    global num
    global coutinue_correct
    repeat = 8

    if request.method == 'POST':
        num += 1

        user_answer = request.form['answer']
        is_correct = user_answer == str(answer)

        if is_correct:
            coutinue_correct += 1
        else:
            if coutinue_correct >= 1:
                coutinue_correct -= 1
        return redirect(url_for('next_question'))

    if num == repeat:
        num = 0
        return render_template('start.html')

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

    factor = random.randint(1, 2)

    # ランダムで生成された選択肢
    if factor == 1:
        answer = random_integer1 + random_integer2
    else:
        if random_integer1 < random_integer2:
            random_integer1, random_integer2 = random_integer2, random_integer1
        answer = random_integer1 - random_integer2

    # 正解とランダムな間違いを含む選択肢を生成
        # 正解を含む選択肢を生成
    choices = [answer]
    while len(choices) < 5:
        fake_answer = answer + random.randint(-10, 10)
        if fake_answer != answer and fake_answer not in choices:
            choices.append(fake_answer)
    random.shuffle(choices)  # 選択肢をシャッフル

    if factor == 1:
        return render_template('quiz.html', sentence=f"{random_integer1} + {random_integer2} =", choices=choices)
    else:
        return render_template('quiz.html', sentence=f"{random_integer1} - {random_integer2} =", choices=choices)

@app.route('/next_question')
def next_question():
    return render_template('next.html')

if __name__ == '__main__':
    app.run(debug=True)
