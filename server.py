from flask import Flask, render_template, request, redirect, url_for

import data_manager as dmg
from datetime import datetime
import csv

app = Flask('__main__')


@app.route('/', methods=['GET', 'POST'])
@app.route('/list', methods=['get', 'post'])
def home():

    SORTING_HEADERS = ['id', 'submission_time', 'view_number', "vote_number"]

    TABLE_HEADING = ['id', "submission time", "view number",
                     "vote number", "title", "message", "image"]
    all_answers = dmg.get_all_answers()

    if request.method == 'POST':
        sorting_header = request.form['sorting-headers']
        sorting_order = request.form['sorting-order']

        if sorting_order == "descending":
            order = True
        else:
            order = False
        all_questions = dmg.sort_questions(sorting_header, order)

        return render_template('list.html', all_answers=all_answers, all_questions=all_questions,
                               table_heading=TABLE_HEADING, sorting_headers=SORTING_HEADERS)

    all_questions = dmg.sort_questions("submission_time")

    return render_template("list.html", all_answers=all_answers, all_questions=all_questions,
                           table_heading=TABLE_HEADING, sorting_headers=SORTING_HEADERS)


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

        dt = datetime.today()
        post_time = dt.timestamp()

        user_question = {
            'id': question_id,
            'submission_time': int(post_time),
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

    user_question = dmg.get_question_by_id('question_id')
    if request.method == 'POST':

        now = datetime.now()
        new_answer_id = dmg.generate_new_id_for_answer()

        answer = {
            "id": new_answer_id,
            "submission_time": now.strftime("%H:%M:%S"),
            'vote_number': "0",
            'question_id': question_id,
            'message': request.form['message'],
            'image': ''
        }

        dmg.add_answer_to_file(answer)

        return redirect(f"/question/{question_id}")

    return render_template('answer.html', user_question=user_question)


@app.route('/question/<question_id>/edit', methods=['GET', 'POST'])
def edit(question_id: int):

    user_question = dmg.get_question_by_id(question_id)
    DATA_HEADER = ['id', 'submission_time', 'view_number',
                   "vote_number", "title", "message", "image"]

    if request.method == "POST":
        user_question['title'] = request.form['title']
        user_question['message'] = request.form['message']

        all_user_questions = dmg.get_all_questions()

        for question in all_user_questions:
            if question['id'] == question_id:
                question['title'] = user_question['title']
                question['message'] = user_question['message']

        with open('sample_data/question.csv', 'w') as csv_file:
            csv_writer = csv.DictWriter(csv_file, fieldnames=DATA_HEADER)
            csv_writer.writeheader()
            for question in all_user_questions:
                csv_writer.writerow(question)

        return render_template('question.html', user_question=user_question,
                               question_id=question_id)

    return render_template('edit.html', question_id=question_id, user_question=user_question)


@app.route('/question/<question_id>/delete')
def delete_questions(question_id):

    DATA_HEADER = ['id', 'submission_time', 'view_number',
                   "vote_number", "title", "message", "image"]

    ANSWER_HEADERS = ['id', 'submission_time',
                      'vote_number', 'question_id', 'message', 'image']

    all_user_questions = dmg.get_all_questions()

    new_all_user_questions = []

    for question in all_user_questions:
        if question['id'] == question_id:
            new_all_user_questions.remove(question)

    all_user_answers = dmg.get_all_answers()

    new_all_user_answers = []

    for answer in all_user_answers:
        if int(answer['question_id']) != int(question_id):
            new_all_user_answers.append(answer)

    with open('sample_data/answer.csv', 'w') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=ANSWER_HEADERS)
        csv_writer.writeheader()
        for answer in new_all_user_answers:
            csv_writer.writerow(answer)

    with open('sample_data/question.csv', 'w') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=DATA_HEADER)
        csv_writer.writeheader()
        for question in all_user_questions:
            csv_writer.writerow(question)

    return redirect('/',)


@app.route('/answer/<question_id>/<answer_id>/delete')
def delete_answer(question_id, answer_id):

    ANSWER_HEADERS = ['id', 'submission_time',
                      'vote_number', 'question_id', 'message', 'image']
    all_user_answers = dmg.get_all_answers()

    new_all_user_answers = []

    for answer in all_user_answers:
        if answer['id'] != answer_id:
            new_all_user_answers.append(answer)

    with open('sample_data/answer.csv', 'w') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=ANSWER_HEADERS)
        csv_writer.writeheader()
        for answer in new_all_user_answers:
            csv_writer.writerow(answer)
    return redirect(f'/question/{question_id}')


@app.route('/question/<question_id>/vote-up')
def vote_up_questions(question_id):

    DATA_HEADER = ['id', 'submission_time', 'view_number',
                   "vote_number", "title", "message", "image"]
    all_questions = dmg.get_all_questions()

    for question in all_questions:
        if question['id'] == question_id:
            question['vote_number'] = int(question['vote_number']) + 1

    with open('sample_data/question.csv', 'w') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=DATA_HEADER)
        csv_writer.writeheader()
        for question in all_questions:
            csv_writer.writerow(question)

    return redirect(f'/question/{question_id}')


@app.route('/question/<question_id>/vote-down')
def vote_down_questions(question_id):

    DATA_HEADER = ['id', 'submission_time', 'view_number',
                   "vote_number", "title", "message", "image"]
    all_questions = dmg.get_all_questions()

    for question in all_questions:
        if question['id'] == question_id:
            question['vote_number'] = int(question['vote_number']) - 1

    with open('sample_data/question.csv', 'w') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=DATA_HEADER)
        csv_writer.writeheader()
        for question in all_questions:
            csv_writer.writerow(question)

    return redirect(f'/question/{question_id}')


if __name__ == '__main__':
    app.run(
        port=5000,
        debug=True
    )
