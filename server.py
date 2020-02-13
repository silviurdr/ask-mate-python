from flask import Flask, render_template, request, redirect, url_for

import data_manager as dmg
from datetime import datetime
import time
import csv

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

    user_question = dmg.get_question_by_id(question_id)
    user_answers = dmg.get_answer_by_id(question_id)

    empty = False

    if user_answers == None:
        empty = True

    return render_template('question.html', user_question=user_question, user_answers=user_answers,
                           question_id=question_id, empty=empty)


@app.route('/add-question', methods=['GET', 'POST'])
def add_question():

    if request.method == "POST":

        question_id = dmg.generate_new_id()

        user_question = {
            'id': question_id,
            'submission_time': int(round(time.time() * 1000)),
            'view_number': 0,
            'vote_number': 0,
            'title': request.form['title'],
            'message': request.form['message'],
            'image': ''
        }

        dmg.add_question_to_file(user_question)
        return redirect(url_for('question', question_id=question_id))

    return render_template('add-question.html')


@app.route('/question/<question_id>/new-answer', methods=['GET', 'POST'])
def answer(question_id):

    print(request.form)
    user_question = dmg.get_question_by_id('question_id')
    if request.method == 'POST':

        answer_id = dmg.generate_new_id_for_answer()

        now = datetime.now()

        answer = {
            "id": answer_id,
            "submission_time": now.strftime("%H:%M:%S"),
            'vote_number': "0",
            'question_id': question_id,
            'message': request.form['message'],
            'image': ''
        }
        print(answer)

        dmg.add_answer_to_file(answer)

        return redirect("/question/{0}".format(question_id))

    return render_template('answer.html', user_question=user_question)


if __name__ == '__main__':
    app.run(
        port=5000,
        debug=True
    )
