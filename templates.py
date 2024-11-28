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

Provide the JSON directly without surronuding backticks.
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

Provide the JSON directly without surronuding backticks. Do not provide any additional ou
"""

TEMPLATE_SUPPORTING_INFORMATION = """
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
You are an expert at evaluating student profiles, specifically their statements of purpose. 
I would like you assign scores based on the number of sentences you find that mention the following categories are matched:
1) Awards won
2) Hackathons participated 
3) Events organized 
4) Honors student
5) Gold medalist
6) Topper of a course 
7) Stood in top 5% of cohort
8) Positive Attitude
9) Relevance to Computer science major
10) References to SJSU

I want you to assign a score out of 10 for each of the above categories. Do not provide justification, just the scores in the format below.

Reply the scores in a JSON format as follows:
{
  "AwardsWon": <float value between 1 and 10>,
  "HackathonsParticipated": <float value between 1 and 10>,
  "EventsOrganized": <float value between 1 and 10>,
  "HonorsStudent": <float value between 1 and 10>,
  "GoldMedalist": <float value between 1 and 10>,
  "TopperOfACourse": <float value between 1 and 10>,
  "StoodInTop5PercentOfCohort": <float value between 1 and 10>,
  "PositiveAttitude": <float value between 1 and 10>,
  "RelevanceToComputerScienceMajor": <float value between 1 and 10>,
  "ReferencesToSJSU": <float value between 1 and 10>
}

Provide the JSON directly without surronuding backticks.
"""


TEMPLATE_EVALUATIONS_AND_LORS = """
You are an expert on evaluating student profiles, specifically the Letters of Recommendation submitted by the reviewers. 
I would like you to assign scores based on the following categories:
1) Reviewers mentioning publications 
2) Reviewers mentioning projects
3) Reviewers mentioning exceptional performance such as topper of a course or gold medalist or standing in top x percentage of a class
4) Mention of scholarships
5) Mention of leadership skills, initiative, innovation, admiration, joy

I want you to assign a score out of 10 for each of the above categories. Do not provide justification, just the scores in the format below.

Reply the scores in a JSON format as follows:
{
  "PublicationsMentioned": <float value between 1 and 10>,
  "ProjectsMentioned": <float value between 1 and 10>,
  "ExceptionalPerformanceMentioned": <float value between 1 and 10>,
  "ScholarshipsMentioned": <float value between 1 and 10>,
  "LeadershipSkillsMentioned": <float value between 1 and 10>,
  "InitiativeMentioned": <float value between 1 and 10>,
  "InnovationMentioned": <float value between 1 and 10>,
  "AdmirationOrJoyMentioned": <float value between 1 and 10>,
}

Provide the JSON directly without surrounding backticks.
"""


TEMPLATES = {
    'academic_information.pdf': TEMPLATE_ACADEMIC_HISTORY,
    'student_information.pdf': TEMPLATE_STUDENT_INFORMATION,

    'supporting_information.pdf': """Use the following rubric to evaluate the student's profile and return by adding all the points. If the student has any awards, assign 5 points for each award. If the student has taken part in any hackathon, assign 5 points for each hackathon. If the student has any honors, assign 5 points for each honor. If the student has a publication in either IEEE, Springer, or ACM, assign 5 points for each publication. If the student has a publication in any other conference, assign 2 points for each publication.
    """,
    'statement_of_purpose.pdf': TEMPLATE_STATEMENT_OF_PURPOSE,
    'evaluations_and_lors.pdf': TEMPLATE_EVALUATIONS_AND_LORS,
}



#Generate a template for rubrics that can be modified at any time to give different priorities for different metrics.

RUBRIC_TEMPLATE = {
    'awards': 5,
    'hackathon': 5,
    'honors': 5,
    'ieee_springer_acm_iclri_mips': 5,
    'other_conference': 2,
    'sop_clarity': 33.33,
    'sop_originality': 33.33,
    'sop_relevance': 33.33,
    'lor1': 33.33,
    'lor2': 33.33,
    'lor3': 33.33,
    'total': 100
}


