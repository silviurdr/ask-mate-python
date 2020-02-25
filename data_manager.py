import csv
import connection

from datetime import datetime

DATA_HEADER = ['id', 'submission_time', 'view_number',
               "vote_number", "title", "message", "image"]

ANSWER_FIELDNAMES = ["id", "submission_time",
                     "vote_number", "question_id", "message", "image"]


@connection.connection_handler
def get_all_questions(cursor):
    '''
    extracts all the data from the questions table
    '''

    cursor.execute("""
    SELECT * FROM question
    """)
    questions = cursor.fetchall()
    return questions

@connection.connection_handler
def get_all_answers(cursor):
    '''
    extracts all the data from the answer table
    '''

    cursor.execute("""
    SELECT * from answer
        """)
    answers = cursor.fetchall()
    return answers

@connection.connection_handler
def get_all_comments(cursor):
    '''
    extracts all the data from the comment table
    '''
    cursor.execute("""
    SELECT * from comment
    """)
    comments = cursor.fetchall()
    return comments

@connection.connection_handler
def get_all_tags(cursor):
    '''
    extracts all the data from tag table
    '''
    cursor.execute("""
    SELECT * from tag
    """)
    tags = cursor.fetchall()
    return tags


def convert_line_breaks_to_br(original_str):
    return '<br>'.join(original_str.split('\n'))


def sort_questions(sorting_header, reverse_order=True):
    '''
    Returns a dictionary with the questions sorted by submitted time
    '''

    all_questions = get_all_questions()
    sorted_questions = sorted(all_questions,
                              key=lambda dict: dict[sorting_header], reverse=reverse_order)

    return sorted_questions


def get_question_by_id(question_id):
    all_questions = get_all_questions()

    for question in all_questions:
        if question_id == question['id']:
            return question

    return None


def get_answer_by_id(answer_id):
    all_answers = get_all_answers()

    requested_answers = []

    if len(all_answers) == 0:
        return None

    else:
        for answer in all_answers:
            if int(answer_id) == int(answer['question_id']):
                requested_answers.append(answer)
        return requested_answers

@connection.connection_handler
def add_question_to_database(cursor, user_question):

    cursor.execute("""
    INSERT INTO question
    (id, submission_time, view_number, vote_number, title, message, image)
    VALUES ({0}, '{1}', {2}, {3}, '{4}', '{5}', '{6}')
    """.format(user_question['id'], user_question['submission_time'], user_question['view_number'],
               user_question['vote_number'], user_question['title'], user_question['message'], user_question['image']))


def generate_new_id():

    all_stories = get_all_questions()

    if len(all_stories) == 0:
        question_id = 1
    else:
        question_id = str(int(all_stories[-1]['id']) + 1)

    return question_id


def generate_new_id_for_answer():

    all_answers = get_all_answers()

    if len(all_answers) == 0:
        return 1
    else:
        answer_id = str(int(all_answers[-1]['id']) + 1)

    return answer_id

@connection.connection_handler
def add_answer_to_database(cursor, answer):

    cursor.execute("""
    INSERT INTO answer
    (id, submission_time, vote_number, question_id, message, image)
    VALUES ({0}, '{1}', {2}, {3}, '{4}', '{5}')
    """.format(answer['id'], answer['submission_time'], answer['vote_number'], answer['question_id'],
               answer['message'], answer['image']))



@connection.connection_handler
def get_next_id(cursor, table):
    cursor.execute("""
        SELECT id FROM {0} ORDER BY id DESC LIMIT 1;
    """.format(table))
    last_id = cursor.fetchall()
    next_id = last_id[0]['id'] + 1
    return next_id


@connection.connection_handler
def edit_question(cursor, question_id, user_question):
    cursor.execute("""
            UPDATE question
            SET title='{0}', message='{1}'
            WHERE id={2}
            """.format(user_question[0]['title'], user_question[0]['message'], question_id))

@connection.connection_handler
def delete_question(cursor, question_id):
    cursor.execute("""
    DELETE from question
    WHERE id={0}
    """.format(question_id))

@connection.connection_handler
def delete_answer(cursor, answer_id):
    cursor.execute("""
    DELETE FROM answer
    WHERE id={0}
    """.format(answer_id))