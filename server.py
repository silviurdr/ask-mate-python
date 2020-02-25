from flask import Flask, render_template, request, redirect, url_for

import data_manager as dmg
from datetime import datetime
import time, calendar, os
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

    if user_answers is None:

        empty = True

    return render_template('question.html', user_question=user_question, user_answers=user_answers,
                           question_id=question_id, empty=empty)


@app.route('/add-question', methods=['GET', 'POST'])
def add_question():

    if request.method == "POST":

        question_id = dmg.generate_new_id()

        submission_time =  datetime.utcfromtimestamp(int(calendar.timegm(time.gmtime())) + 7200).strftime('%Y-%m-%d %H:%M:%S')

        user_question = {
            'id': question_id,
            'submission_time': submission_time,
            'view_number': 0,
            'vote_number': 0,
            'title': request.form['title'],
            'message': request.form['message'],
            'image': ''
        }

        dmg.add_question_to_database(user_question)
        return redirect(url_for('question', question_id=question_id))

    return render_template('add-question.html')


@app.route('/question/<question_id>/new-answer', methods=['GET', 'POST'])
def answer(question_id):

    user_question = dmg.get_question_by_id('question_id')
    if request.method == 'POST':

        submission_time =  datetime.utcfromtimestamp(int(calendar.timegm(time.gmtime())) + 7200)\
            .strftime('%Y-%m-%d %H:%M:%S')
        new_answer_id = dmg.get_next_id('answer')

        answer = {
            "id": new_answer_id,
            "submission_time": submission_time,
            'vote_number': "0",
            'question_id': question_id,
            'message': request.form['message'],
            'image': ''
        }

        dmg.add_answer_to_database(answer)

        return redirect(f"/question/{question_id}")

    return render_template('answer.html', user_question=user_question)


@app.route('/question/<question_id>/edit', methods=['GET', 'POST'])
def edit(question_id: int):

    if request.method == "POST":
        user_question = dmg.get_all_questions()
        user_question[0]['title'] = request.form['title']
        user_question[0]['message'] = request.form['message']

        dmg.edit_question(question_id, user_question)

        return render_template('question.html', user_question=user_question,
                               question_id=question_id)

    user_question = dmg.get_question_by_id(question_id)

    return render_template('edit.html', question_id=question_id, user_question=user_question)


@app.route('/question/<question_id>/delete')
def delete_questions(question_id):

    dmg.delete_question(question_id)
    return redirect('/',)


@app.route('/answer/<question_id>/<answer_id>/delete')
def delete_answer(question_id, answer_id):

    dmg.delete_answer(answer_id)
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


@app.route('/answer/<question_id>/<answer_id>/vote-up')
def vote_up_answers(answer_id, question_id):

    ANSWER_HEADERS = ['id', 'submission_time',
                      'vote_number', 'question_id', 'message', 'image']

    all_answers = dmg.get_all_answers()

    for answer in all_answers:
        if answer['id'] == answer_id:
            answer['vote_number'] = int(answer['vote_number']) + 1

    with open('sample_data/answer.csv', 'w') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=ANSWER_HEADERS)
        csv_writer.writeheader()
        for answer in all_answers:
            csv_writer.writerow(answer)

    return redirect(f"/question/{question_id}")


@app.route('/answer/<question_id>/<answer_id>/vote-down')
def vote_down_answers(answer_id, question_id):

    ANSWER_HEADERS = ['id', 'submission_time',
                      'vote_number', 'question_id', 'message', 'image']

    all_answers = dmg.get_all_answers()

    for answer in all_answers:
        if answer['id'] == answer_id:
            answer['vote_number'] = int(answer['vote_number']) - 1

    with open('sample_data/answer.csv', 'w') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=ANSWER_HEADERS)
        csv_writer.writeheader()
        for answer in all_answers:
            csv_writer.writerow(answer)

    return redirect(f"/question/{question_id}")


if __name__ == '__main__':
    app.run(
        port=5000,
        debug=True
    )
