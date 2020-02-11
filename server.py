from flask import Flask, render_template, request, url_for

import data_manager as dmg

app = Flask('__main__')


@app.route('/')
@app.route('/list')
def home():
    TABLE_HEADING = ['id', "submission time", "view number",
                     "vote number", "title", "message", "image"]
    all_questions = dmg.sort_questions()

    print(all_questions)

    return render_template("list.html", all_questions=all_questions, table_heading=TABLE_HEADING)


@app.route('/question/<question_id>')
def question(question_id):
    pass


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
