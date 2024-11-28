# templates.py

TEMPLATE_STUDENT_INFORMATION = """
Extract the name of the student in the format of First_Name Last_Name. Extract the email ID of the student.
Extract the country of the student.
Give your response in the following JSON format:
{
    "Name": "First_Name Last_Name",
    "Email": "",
    "Country": ""
}
"""

TEMPLATE_ACADEMIC_HISTORY = """
Extract the major of the student. Based on the start date and the end date of the degree, determine if the student has graduated or will graduate in the future. Extract the name of the University.
If there are multiple degrees, provide a JSON for the degree that was Majored in Computer Science or a relevant field.
They should be in the following format:
{
    "Major": "",
    "Graduated": "Yes or No",
    "University": ""
}
"""

TEMPLATE_SUPPORTING_INFORMATION = """
Count 
Extract the name of the student. Extract the supporting information metrics about the student in a JSON format. 
        'EXPERIENCE': '
    Extract the following fields for each experience listed:
    Experience Type:
    Recognition Type:
    Title:
    Employer:
    Supervisor:
    ',
    'ACHIEVEMENTS': '
    Extract the following fields for each achievement listed:
    Name:
    Organization:
    Date:
    ',
    'AWARDS': '
    Extract the following fields for each award listed:
    Name:
    Organization:
    Date:
    ',
    'PUBLICATIONS': '
    Extract the following fields for each publication listed:
    Name:
    Organization:
    Date:
    ',
    'HONORS':'
    Extract the following fields for each honor listed:
    Name:
    Organization:
    Date:
    Achievements are classified as honors, awards, publications and certifications that are listed. Evaluate a score out of 100 for the achievements based on the following criteria: relevance, impact, and recency. If a student has a publication, that takes precedence over other achievements.

"""

TEMPLATE_STATEMENT_OF_PURPOSE = """
Evaluate the student's statement of purpose and provide a score out of 100, based on the following criteria: clarity, originality, and relevance.
"""

TEMPLATE_EVALUATIONS_AND_LORS = """

"""
TEMPLATES = {
    'academic_information.pdf': TEMPLATE_ACADEMIC_HISTORY,
    'student_information.pdf': TEMPLATE_STUDENT_INFORMATION,

    'supporting_information.pdf': """Extract the name of the student. Extract the supporting information metrics about the student in a JSON format. 
        'EXPERIENCE': '
    Extract the following fields for each experience listed:
    Experience Type:
    Recognition Type:
    Title:
    Employer:
    Supervisor:
    ',
    'ACHIEVEMENTS': '
    Extract the following fields for each achievement listed:
    Name:
    Organization:
    Date:
    ',
    'AWARDS': '
    Extract the following fields for each award listed:
    Name:
    Organization:
    Date:
    ',
    'PUBLICATIONS': '
    Extract the following fields for each publication listed:
    Name:
    Organization:
    Date:
    ',
    'HONORS':'
    Extract the following fields for each honor listed:
    Name:
    Organization:
    Date:
    Achievements and Experience are all of the points listed that are similar to the above format. Evaluate a score out of 100 for the achievements and experiences based on the following criteria: relevance, impact, and recency. Higher scores can be given to students with hobbies and achievements such as chess, olympiads, conference publications, sports and extra curricular activities. The minimum score of 50 should be given to students with no achievements or experiences. If a student has a publication, that takes precedence over other achievements.
    """,
    'statement_of_purpose.pdf': 'Evaluate the student\'s statement of purpose and provide a score out of 100, based on the following criteria: clarity, originality, and relevance.',
    'evaluations_and_lors.pdf': "Extract the field called 'Provide your overall recommendation for this applicant.' Up to 3 letters of recommendation will be provided, with each evaluator offering their recommendation for the student in various forms. Evaluate each recommendation letter with a score out of 100. Once all 3 scores are assigned, sum up the total and divide it by 300 and give one final score out of 100 for the applicant’s overall recommendation.",
}
