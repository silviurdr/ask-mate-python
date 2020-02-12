from flask import Flask, render_template, request, redirect, url_for

import data_manager as dmg
from datetime import datetime

app = Flask('__main__')


@app.route('/')
@app.route('/list')
def home():
    TABLE_HEADING = ['id', "submission time", "view number",
                     "vote number", "title", "message", "image"]
    all_questions = dmg.sort_questions()

    return render_template("list.html", all_questions=all_questions, table_heading=TABLE_HEADING)


@app.route('/question/<question_id>', methods=['GET', 'POST'])
def question(question_id: int):

    now = datetime.now()

    if request.method == 'POST':
        user_question = {
            'id': question_id,
            'submission_time': now.strftime("%H:%M:%S"),
            'view_number': 0,
            'vote_number': 0,
            'title': request.form['title'],
            'message': request.form['message'],
            'image': ''
        }

        dmg.add_question_to_file(user_question)
        return redirect('/')

    user_question = dmg.get_question_by_id(question_id)
    user_answers = dmg.get_answer_by_id(question_id)

    empty = False

    if user_answers == None:
        empty = True

    print(user_answers)

    return render_template('question.html', user_question=user_question, user_answers=user_answers,
                           question_id=question_id, empty=empty)


@app.route('/add-question')
def add_question():
    pass


@app.route('/question/<question_id>/new_answer')
def answer(question_id):
    pass


if __name__ == '__main__':
    app.run(
        port=5000,
        debug=True
    )
