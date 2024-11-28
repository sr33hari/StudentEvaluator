import json
import numpy as np
import pandas as pd
import parseDocuments
import templates
import ollama
import cmd
from termcolor import colored
from pathlib import Path

class StudentEvaluateTool(cmd.Cmd):
    intro = 'Welcome to the Student Evaluator Tool. Type help or ? to list commands.\n'
    prompt = '(prompt) '

    def do_all_profiles(self, arg: str):
        directories, num_lors = parseDocuments.process_directory('rawProfiles', 'parsedProfiles')
        print(colored(f"Yipee! Processed {len(directories)} profiles.", "cyan"))
    
    def do_split_profile(self, arg: str):
        # Process Name in rawProfiles directory
        profile_o_dir = parseDocuments.process_single_profile(arg, 'parsedProfiles')
        print(colored(f"Processed Profile in {profile_o_dir}", "cyan"))
    
    def do_stats_on_sops(self, arg: str):
        print("Looking at:", arg)
        text_content = parseDocuments.get_text_content(arg)
        filename = parseDocuments.FilenameConstants.STATEMENT_OF_PURPOSE + ".pdf"
        prompt = templates.TEMPLATES.get(filename)

        for temperature in [0.1, 0.2, 0.3, 0.5, 0.7, 0.9]:
            final_scores = []
            for i in range(5):
                print(f"Running {i+1}-th iteration")
                individual_scores = 0
                content_with_prompt = text_content[filename] + '\n' + prompt
                response = ollama.chat(model='llama3.1:8b', messages=[
                    {
                        'role': 'user',
                        'content': content_with_prompt,
                    },
                ], options={"temperature": temperature})

                try:
                    json_data = response['message']['content']
                    json_data = json.loads(json_data)
                    print(colored(f"JSON Data: {json_data}", "green"))

                    for key, value in json_data.items():
                        individual_scores += int(value)
                    final_scores.append(individual_scores)

                except Exception as e:
                    print(colored("Error parsing JSON Data:", "red"))
            
            print(colored(
                        f"For Temperature: {temperature}" + 
                        f"\nScore Mean: {np.mean(final_scores)}" + 
                        f"\nStandard Deviation: {np.std(final_scores)}" + 
                        f"\nLowest Score: {min(final_scores)}" + 
                        f"\nHighest Score: {max(final_scores)}"
                        , "cyan"))
        

    
    def do_run_single_evaluation(self, arg: str):
        print("Looking at:", arg)
        # Get all the filenames in the directory
        filenames = parseDocuments.get_filenames(arg)
        num_lors = 0
        # Run individual prompts to get evaluation
        consolidated_responses = ""

        consolidated_data = {}
        
        for filename in filenames:
            print(f"Processing input for file: {filename}")

            if filename == f"{parseDocuments.FilenameConstants.EVALUATIONS_AND_LORS}.pdf":
                # Identify the number of LoRs
                num_lors = parseDocuments.identify_number_of_lors(arg + "/" + filename)
                print(colored(f"Number of LoRs: {num_lors}", "red", "on_white"))

            text_content = parseDocuments.get_text_content(arg)
            prompt = templates.TEMPLATES.get(filename)
            content_with_prompt = text_content[filename] + '\n' + prompt

            response = ollama.chat(model='llama3.1:8b', messages=[
                {
                    'role': 'user',
                    'content': content_with_prompt,
                },
            ], options={"temperature": 0.2})
            print(colored(f"Response for file {filename}: {response['message']['content']} ", "green"))
            consolidated_responses += f"Response for {filename}:\n{response['message']['content']}\n\n---------------------------\n\n"

            try:
                consolidated_data[filename] = json.loads(response['message']['content'])
            except Exception as e:
                pass
        
        # Run evaluation on the results
        final_response = ollama.chat(model='llama3.1:8b', messages=[
            {
                'role': 'user',
                'content': """You are an assistant for evaluating student profiles. Use the following pieces of retrieved context to answer the questions. Ensure you are unbiased and fair in your evaluation. The student here has """ + str(num_lors) + """Letters of Recommendation. 
                Use the following rubric to evaluate the student's profile and return by adding all the points.
                If the Statment of Purpose is not available, return the score of 0.
                If the Statment of Purpose is available, assign the score evaluated in the passed context.
                If the Letters of Recommendation are not available, please return a score of 0.
                If the Letters of Recommendation are available, give 10 points to each recommendation letter.
                Mention that there is no plagiarism detected between the LoRs, and also no AI content in the SoP.
                If the recommendation letter mentions GPA or CGPA or if the student is within the top percentages among their peers, give 5 points for each mention. 
                If the student has a publication in either IEEE or Springer or ACM, give 5 points for each publication. If the student has a publication any other conference, give 2 points for each publication.
                If the student has listed any awards, give 5 points for each award. If the student has listed any honors, give 5 points for each honor. If the student has participated in any Hackathon, give 5 points. Use the below context to evaluate the score of the student.
                List all the scores assigned and ENSURE YOU scale the score to a maximum of 100 and then give a final score out of HUNDRED(100).
                """ + consolidated_responses
            },
        ])
        # Show final results
        print(colored("Final Response:", "red", "on_white"))
        print(final_response['message']['content'])

        # Save consolidated responses for this student to a file
        data = {}
        df = pd.DataFrame()
        # Pull Student Info
        data ['Name'] = consolidated_data.get(parseDocuments.FilenameConstants.STUDENT_INFORMATION + ".pdf", {}).get('Name', 'N/A')
        data['Email'] = consolidated_data.get(parseDocuments.FilenameConstants.STUDENT_INFORMATION + ".pdf", {}).get('Email', 'N/A')
        # Pull Academic Info
        data ['University'] = consolidated_data.get(parseDocuments.FilenameConstants.ACADEMIC_INFORMATION + ".pdf", {}).get('University', 'N/A')
        data['Graduated'] = consolidated_data.get(parseDocuments.FilenameConstants.ACADEMIC_INFORMATION + ".pdf", {}).get('Graduated', 'N/A')
        # Pull SoP info
        score = 0
        for key, value in consolidated_data.get(parseDocuments.FilenameConstants.STATEMENT_OF_PURPOSE + ".pdf", {}).items():
            data['SoP_' + key] = value
            score += int(value)
        data['SoP_Score'] = score

        # Pull LoR info
        score = 0
        for key, value in consolidated_data.get(parseDocuments.FilenameConstants.EVALUATIONS_AND_LORS + ".pdf", {}).items():
            data['LoR_' + key] = value
            score += int(value)
        data['LoR_Score'] = score

        # Save Dict to Df and to CSV
        df = pd.DataFrame(data, index=[0])
        df.to_csv(f"evaluationScores/{Path(arg).stem}.csv", index=False)

    def do_run_lor_evaluation(self, arg:str):
        print("splitting all pdfs in rawProfiles")
        directories, num_lors = parseDocuments.process_directory('rawProfiles', 'parsedProfiles')
        print(colored(f"Yipee! Processed {len(directories)} profiles.", "cyan"))

        student_data = [] 

        #Run for LoRs only in all of the student's profiles
        for directory in directories:
            print(f"Processing input for directory: {directory}") 
            filenames = parseDocuments.get_filenames(directory)
            student_name = ""
            student_email = ""
            student_name, student_email = parseDocuments.get_student_name_and_email(directory)
            print(colored(f"Student Name: {student_name}", "red", "on_white"))
            print(colored(f"Student Email: {student_email}", "red", "on_white"))
            text_content = parseDocuments.get_text_content(directory)
            for filename in filenames:
                if filename == f"{parseDocuments.FilenameConstants.EVALUATIONS_AND_LORS}.pdf":
                    # Identify the number of LoRs
                    num_lors = parseDocuments.identify_number_of_lors(directory + "/" + filename)

                    print(colored(f"Number of LoRs: {num_lors}", "red", "on_white"))

                    evaluationPrompt = templates.TEMPLATES.get('evaluations_and_lors.pdf')
                    content_with_prompt = text_content[filename] + '\n' + evaluationPrompt
                    response = ollama.chat(model='llama3.1:8b', messages=[
                        {
                            'role': 'user',
                            'content': content_with_prompt,
                        },
                    ], options={"temperature": 0.3})

                    print(colored(f"Response for file {filename}: {response['message']['content']} ", "green"))

                    # Save consolidated responses for this student to a csv file for each key in the JSON response
                    data = {}
                    df = pd.DataFrame()
                    data['Name'] = student_name
                    data['Email'] = student_email
                    score = 0
                    for key, value in json.loads(response['message']['content']).items():
                        data[key] = value
                        score += int(value)
                    data['Total_Score'] = score
                    student_data.append(data)

                    # Save Dict to Df and to CSV
                    df = pd.DataFrame(data, index=[0])
                    #check if lorScores directory exists
                    # Path("lorScores").mkdir(parents=True, exist_ok=True)
                    # df.to_csv(f"lorScores/{Path(directory).stem}.csv", index=False)

        consolidated_df = pd.DataFrame(student_data)
        Path("lorScores").mkdir(parents=True, exist_ok=True)  # Ensure directory exists
        consolidated_df.to_csv("lorScores/consolidated_scores.csv", index=False)
        print(colored("All student information saved to lorScores/consolidated_scores.csv", "cyan"))

    def do_exit(self, arg):
        'Exit the file processor'
        print(colored('Thank you for using the Evaluation Tool! Ciao!', "green"))
        return True

if __name__ == "__main__":
    StudentEvaluateTool().cmdloop()
   

    
    
