import csv


DATA_HEADER = ['id', 'submission_time', 'view_number',
               "vote_number", "title", "message", "image"]

ANSWER_FIELDNAMES = ["id", "submission_time",
                     "vote_number", "question_id", "message", "image"]


def get_all_questions():
    '''
    param question_id:
        If given it will act as a filter and return the dictionary of a specific Question
        If not give it will return a list of dictionaries with all the given details
    '''

    user_questions = []

    with open('sample_data/question.csv', 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)

        for row in csv_reader:
            question = dict(row)
            user_questions.append(question)
    return user_questions


def get_all_answers():
    '''
    param question_id:
        If given it will act as a filter and return the dictionary of a specific Question
        If not give it will return a list of dictionaries with all the given details
    '''

    user_answers = []

    with open('sample_data/answer.csv') as csv_file:
        csv_reader = csv.DictReader(csv_file)

        for row in csv_reader:
            answer = dict(row)

            user_answers.append(answer)

    return user_answers


def convert_line_breaks_to_br(original_str):
    return '<br>'.join(original_str.split('\n'))


def sort_questions(sorting_header, reverse_order=True):
    '''
    Returns a dictionary with the questions sorted by submitted time
    '''

    all_questions = get_all_questions()
    sorted_questions = sorted(all_questions,
                              key=lambda dict: int(dict[sorting_header]), reverse=reverse_order)

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

    for answer in all_answers:
        if answer_id == answer['question_id']:
            requested_answers.append(answer)
    if len(requested_answers) == 0:
        return None

    else:
        return requested_answers


def add_question_to_file(new_question):

    all_questions = get_all_questions()

    with open('sample_data/question.csv', 'a') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=DATA_HEADER)
        if all_questions is False:
            csv_writer.writeheader()

        csv_writer.writerow(new_question)


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
        answer_id = 1
    else:
        answer_id = str(int(all_answers[-1]['id']) + 1)

    return answer_id


def add_answer_to_file(answer):

    all_answers = get_all_answers()

    with open('sample_data/answer.csv', 'a') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=ANSWER_FIELDNAMES)
        if all_answers is False:
            csv_writer.writeheader()
        csv_writer.writerow(answer)
