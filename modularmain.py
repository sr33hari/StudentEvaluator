import parseDocuments
import templates
import os
import ollama
import time
import json
import csv
import mergecsv

# Process the directory
directories, num_lors = parseDocuments.process_directory('rawProfiles', 'parsedProfiles')

# # Initialize a list to hold all responses
# all_responses = []

# total_time_taken = 0

# # Open the output file once
# with open('contents.txt', 'w') as f:
#     for directory in directories:
#         consolidated_responses = ""
#         text_content = parseDocuments.get_text_content(directory)
#         # with open(f"text_content_{os.path.basename(directory)}.txt", "w") as text_file:
#         #     text_file.write(str(text_content))

        
#         for filename, text in text_content.items():
#             # Save the contents to a text file
#             # print(f"Attempting to write the following content {text} typeof {type(text)}")
#             f.write(text)
#             # f.write('\n\n---------------------------')

#             # Select the appropriate prompt based on the filename
#             prompt = templates.TEMPLATES.get(filename)
            
#             # If there's no specific prompt for the file, continue to the next file
#             if not prompt:
#                 print("No prompt found for file:", filename)
#                 continue

#             # Append the prompt to the content
#             content_with_prompt = text + '\n' + prompt
            
#             # Print statement to indicate processing
#             print(f"Processing input for file: {filename}")

#             # Measure time taken for the model to return a response
#             start_time = time.time()
            
#             # Get response from the model
#             response = ollama.chat(model='llama3', messages=[
#                 {
#                     'role': 'user',
#                     'content': content_with_prompt,
#                 },
#             ])
            
#             end_time = time.time()
#             duration = end_time - start_time
#             total_time_taken += duration

#             # Print the response time
#             print(f"Response time for {filename}: {duration:.2f} seconds")

#             # Consolidate the responses
#             consolidated_responses += f"Response for {filename}:\n{response['message']['content']}\n\n---------------------------\n\n"

#             print(f"Response for file {filename}:", response['message']['content'])

#         # Save consolidated responses for this student to a file
#         # with open(f'responses_{os.path.basename(directory)}.txt', 'w') as response_file:
#         #     response_file.write(consolidated_responses)

#         # Generate final response with JSON extraction instruction

#         final_response = ollama.chat(model='llama3', messages=[
#             {
#                 'role': 'user',
#                 'content': """You are an assistant for evaluating student profiles. Use the following pieces of retrieved context to answer the questions. Ensure you are unbiased and fair in your evaluation. The student here has """ + str(num_lors) + """Letters of Recommendation. 
#                 Use the following rubric to evaluate the student's profile and return by adding all the points.
#                 If the Letters of Recommendation are not available, please return a score of 0.
#                 If the Letters of Recommendation are available, give 10 points to each recommendation letter. If the recommender in the letter is from SJSU, give 15 points for each recommendation letter.
#                 If the recommendation letter mentions GPA or CGPA or if the student is within the top percentages among their peers, give 5 points for each mention. 
#                 If the student has a publication in either IEEE or Springer or ACM, give 5 points for each publication. If the student has a publication any other conference, give 2 points for each publication.
#                 If the student has listed any awards, give 5 points for each award. If the student has listed any honors, give 5 points for each honor. If the student has participated in any Hackathon, give 5 points. Use the below context to evaluate the score of the student.
#                 """ + consolidated_responses
#             },
#         ])

#         # final_response = ollama.chat(model='llama3', messages=[
#         #     {
#         #         'role': 'user',
#         #         'content': consolidated_responses + """\nReturn the Name, EmailID, Country, Achievements (scored out of 100), Statement of Purpose (scored out of 100), Evaluations and LORs (scored out of 100) in a JSON format. Do not include anything else in your response. Ensure the name is formatted as a single string as First_Name followed by Last_Name, do not include commas in the Name. The values should be numbers in the range 0-100, ensure all numbers are whole numbers and do not include decimals.
#         #         The JSON response should be in the following format:
#         #         {
#         #             "Name:": "First_Name Last_Name",
#         #             "EmailID": "",
#         #             "Country": "",
#         #             "Achievements": number from 0 to 100,
#         #             "StatementofPurpose": number from 0 to 100,
#         #             "EvaluationsandLORs": number from 0 to 100
#         #         }

#         #         Ensure the JSON is correctly formatted and enclosed within the curly braces. Do not include any additional information in the response.
#         #         """,
#         #     },
#         # ])

#         # Print the final response
#         print(f"Final response for {os.path.basename(directory)}:")
#         print(final_response['message']['content'])

#         # Extract JSON data from the final response
#         # final_response_content = final_response['message']['content']
        
#         # Load JSON data
#         # try:
#         #     data = json.loads(final_response_content)
#         # except json.JSONDecodeError as e:
#         #     print(f"Error decoding JSON: {e}")
#         #     print("Original content:", final_response_content)
#         #     continue
        
#         # Add the parsed data to all_responses
#         # all_responses.append(data)

# # Write all data to a CSV file
# # with open('final_scores.csv', mode='w', newline='') as file:
# #     writer = csv.writer(file)
# #     writer.writerow(["Name", "EmailID", "Achievements", "StatementofPurpose", "EvaluationsandLORs"])
# #     for data in all_responses:
# #         writer.writerow([data.get('Name', ''), data.get('EmailID', ''), data.get('Achievements', ''), data.get('StatementofPurpose', ''), data.get('EvaluationsandLORs', '')])


# time.sleep(5)
# # mergecsv.generate_and_merge_csv()

# print(f"Total time taken: {total_time_taken:.2f} seconds")