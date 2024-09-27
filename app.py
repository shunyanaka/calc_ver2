import random
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

answer = None
coutinue_correct = 23
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

    if coutinue_correct >= 21:
        random_integer1 = random.randint(10000, 99999)
        random_integer2 = random.randint(10000, 99999)
        number_chioce = 20


    elif coutinue_correct >= 18:
        random_integer1 = random.randint(10000, 99999)
        random_integer2 = random.randint(10000, 99999)
        number_chioce = 16

    elif coutinue_correct >= 15:
        random_integer1 = random.randint(10000, 99999)
        random_integer2 = random.randint(1000, 9999)
        number_chioce = 16

    elif coutinue_correct >= 12:
        random_integer1 = random.randint(1000, 9999)
        random_integer2 = random.randint(1000, 9999)
        number_chioce = 12

    elif coutinue_correct >= 9:
        random_integer1 = random.randint(1000, 9999)
        random_integer2 = random.randint(100, 999)
        number_chioce = 12

    elif coutinue_correct >= 6:
        random_integer1 = random.randint(100, 999)
        random_integer2 = random.randint(100, 999)
        number_chioce = 8

    elif coutinue_correct >= 3:
        random_integer1 = random.randint(100, 999)
        random_integer2 = random.randint(20, 99)
        number_chioce = 8

    else:
        random_integer1 = random.randint(20, 99)
        random_integer2 = random.randint(20, 99)
        number_chioce = 8

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
    randam_number = random.randint(0, 1)
    if randam_number == 0:
        ten_answer = answer - 10
    else:
        ten_answer = answer + 10
    choices.append(ten_answer)
    while len(choices) < number_chioce:
        fake_answer = answer + random.randint(-20, 20)
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
