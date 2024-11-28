
text = """
        Statement of Purpose

        As technology continues to reshape our world, I am driven by a deep desire to be at the forefront of innovation within computer science. My fascination with coding began at an early age, with simple programming exercises that sparked my interest in problem-solving and system design. Since then, I have pursued this interest academically and professionally, leading me to the decision to further my studies in computer science. San Jose State University's MS program in Computer Science, known for its strong focus on practical application and industry relevance, is the ideal place for me to expand my technical knowledge and prepare for a career in computer science.

        I earned my Bachelor’s degree in Computer Science from PES university, where I developed a solid foundation in areas like algorithms, data structures, and database management. During my time as an undergraduate, I was able to explore my interest in machine learning through a capstone project that involved designing a recommender system. This project allowed me to hone my coding skills in Python and solidify my passion for machine learning.
        """

text2 = """

I studied the use of IoT devices infected with the Mirai virus to launch a DDoS attack during the CNS
course and it compelled me to find a solution to BotNet attacks using IoT devices. I collaborated with
my teammates to explore how using Virtual Private Networks’ underlying protocols can aid in masking
data packets from external networks. I was exposed to various technologies in the field, such as Layer
2 and Point to Point Tunneling Protocols that were used for testing this theory. We were successful in
preventing packet sniffing and man in the middle attacks through this research endeavor. This work was
presented at the ICCCES 2019 conference and subsequently published in a reputed Springer journal.
Wanting to extend my boundaries in conducting research, my hard work and perseverance earned me
an internship at the Indian Space Research Organization (ISRO). During my internship, I worked on a
project that aimed to find the polynomial that represented the most influential features for any given
data-set, as a combination of Legendre polynomials. I optimized the evaluation of the best fitting polyno-
mial by using greedy methods gleaned from the Advanced Algorithms elective. This work was extremely
enriching as it allowed me to collaborate with brilliant scientists in the Controls Division in charge of
orbital control of satellites.
"""
import torch
from transformers import BertTokenizer, BertForSequenceClassification

tokenizer = BertTokenizer.from_pretrained("shahxeebhassan/bert_base_ai_content_detector")
model = BertForSequenceClassification.from_pretrained("shahxeebhassan/bert_base_ai_content_detector")

# text = "Distance learning will not benefit students because the students are not able to develop as good of a relationship with their teachers."
inputs = tokenizer(text, return_tensors="pt")

with torch.no_grad():
    outputs = model(**inputs)
    logits = outputs.logits

probabilities = torch.softmax(logits, dim=1).cpu().numpy()[0]

human_probability = probabilities[0] * 100
ai_probability = probabilities[1] * 100

# Format output to match the desired style
print(f"Input text: {text}")
print(f"Prediction: {'Human-written' if human_probability > ai_probability else 'AI-generated'}")
print(f"AI Probability: {ai_probability:.2f}%")
print(f"Human Probability: {human_probability:.2f}%")

# inputs = tokenizer(text2, return_tensors="pt")

# with torch.no_grad():
#     outputs = model(**inputs)
#     logits = outputs.logits

# probabilities = torch.softmax(logits, dim=1).cpu().numpy()[0]

# human_probability = probabilities[0] * 100
# ai_probability = probabilities[1] * 100

# # print(f"Input text: {text}")
# print(f"Probability of being human-generated: {human_probability:.2f}%")
# print(f"Probability of being AI-generated: {ai_probability:.2f}%")