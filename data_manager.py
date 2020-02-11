import csv


def get_csv_data(question_id=None):
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

            if question_id is not None and question_id == question['id']:
                return question
            user_questions.append(question)
    return user_questions


def get_all_questions(convert_line_breaks=False):

    all_questions = get_csv_data()
    if convert_line_breaks:
        for question in all_questions:
            question['title'] = convert_line_breaks_to_br(question['title'])
            question['message'] = convert_line_breaks_to_br(
                question['message'])

    return all_questions


def convert_line_breaks_to_br(original_str):
    return '<br>'.join(original_str.split('\n'))


def sort_questions():
    ''' 
    Returns a dictionary with the questions sorted by submitted time
    '''
    submission_times = []
    all_questions = get_all_questions(convert_line_breaks=True)
    for question in all_questions:
        submission_times.append(question['submission_time'])
    sorted_times = sorted(submission_times, reverse=True)
    sorted_questions = []
    for time in sorted_times:
        for question in all_questions:
            if question['submission_time'] == time:
                sorted_questions.append(question)
    return sorted_questions
