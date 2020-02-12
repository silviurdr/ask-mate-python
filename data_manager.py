import csv


DATA_HEADER = ['id', 'submission_time', 'view_number',
               "vote_number", "title", "message", "image"]


def get_all_questions():
    '''
    param question_id:
        If given it will act as a filter and return the dictionary of a specific Question
        If not give it will return a list of dictionaries with all the given details
    '''

    user_questions = []

    with open('sample_data/question.csv') as csv_file:
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


def sort_questions():
    '''
    Returns a dictionary with the questions sorted by submitted time
    '''
    submission_times = []
    all_questions = get_all_questions()
    for question in all_questions:
        submission_times.append(question['submission_time'])
    sorted_times = sorted(submission_times, reverse=True)
    sorted_questions = []
    for time in sorted_times:
        for question in all_questions:
            if question['submission_time'] == time:
                sorted_questions.append(question)
    return sorted_questions


def get_question_by_id(question_id):
    all_questions = get_all_questions()

    for question in all_questions:
        if question_id == question['id']:
            return question

    return None


def get_answer_by_id(answer_id):
    all_answers = get_all_answers()

    for answer in all_answers:
        if answer_id == answer['id']:
            return answer

    return None


def add_question_to_file(question, append=True):

    existing_data = get_all_questions()

    with open('question.csv', 'a') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=DATA_HEADER)
        csv_writer.writeheader()
        for row in existing_data:
            if not append:
                if row['id'] == question['id']:
                    row = question

            csv_writer.writerow()

        if append:
            csv_writer.writerow(question)
