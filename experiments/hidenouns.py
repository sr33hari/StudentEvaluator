import re
import nltk
from nltk.corpus import words
from nltk.tokenize import word_tokenize
from nltk import pos_tag, ne_chunk

# Download required NLTK data
nltk.download('words', quiet=True)
nltk.download('averaged_perceptron_tagger', quiet=True)
nltk.download('maxent_ne_chunker', quiet=True)
nltk.download('punkt', quiet=True)

# Create a dictionary of common words
common_words = set(words.words())

# Define placeholders for different types of PII
placeholders = {
    'PERSON': 'PERSON_NAME',
    'ORGANIZATION': 'ORG_NAME',
    'GPE': 'LOCATION_NAME',
    'FACILITY': 'FACILITY_NAME'
}

# Regular expressions for additional PII types
pii_patterns = {
    'EMAIL': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
    'PHONE': r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',
    'SSN': r'\b\d{3}-\d{2}-\d{4}\b',
    'CREDIT_CARD': r'\b(?:\d{4}[-\s]?){3}\d{4}\b',
    # 'DATE': r'\b(?:\d{1,2}[-/]\d{1,2}[-/]\d{2,4}|\d{1,2}\s(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\s\d{2,4})\b',
    'ADDRESS': r'\b\d+\s+[\w\s]+(?:street|st|avenue|ave|road|rd|highway|hwy|square|sq|trail|trl|drive|dr|court|ct|parkway|pkwy|circle|cir|boulevard|blvd)\b',
    'ZIPCODE': r'\b\d{5}(?:-\d{4})?\b'
}

def replace_pii(text):
    # Tokenize the text
    tokens = word_tokenize(text)
    
    # Perform part-of-speech tagging
    tagged = pos_tag(tokens)
    
    # Perform named entity recognition
    named_entities = ne_chunk(tagged)
    
    # Process each word/entity
    result = []
    for chunk in named_entities:
        if isinstance(chunk, nltk.Tree):
            # Named entity
            entity_type = chunk.label()
            if entity_type in placeholders:
                result.append(placeholders[entity_type])
            else:
                result.append('UNKNOWN_ENTITY')
        else:
            # Regular word
            word, tag = chunk
            if word.lower() in common_words or not word[0].isupper():
                result.append(word)
            else:
                result.append('UNKNOWN_PROPER_NOUN')
    
    # Join the processed words back into a string
    processed_text = ' '.join(result)
    
    # Replace additional PII types using regular expressions
    for pii_type, pattern in pii_patterns.items():
        processed_text = re.sub(pattern, f'{pii_type}_PLACEHOLDER', processed_text, flags=re.IGNORECASE)
    
    return processed_text

# Example usage
if __name__ == "__main__":
    sample_text = """
"Speed. Faster than fast, quicker than quick. I am Lightning." - Lightning McQueen. The ingenuous
8 year old me, inspired by anthropomorphic cars, was eager to be the fastest at everything. With this
newfound zeal, I ensured that I fulfilled my desires, whether it was to achieve the highest grade in class,
to win a quiz, or to outperform others in abacus competitions. Being an avid fan of Formula 1, I acknowl-
edge the impact of a fraction of a second in information flow and the ramifications it may have on end
results. My experience in designing algorithms and conceptual understanding of networks deepened my
realization of how existing designs can be transformed into vastly superior models by optimization. I am
keen on improving the efficiency of algorithms and networks, by fortifying my skills at the San Jose State
University (SJSU).
In my first semester of college, I witnessed real-world applications of algorithmic solutions, when I
attended a roadshow presented by Microsoft Innovation Labs, a lab setup in PES University that funds
internships and events for selected students in college. Determined to bolster my experience in inter-
domain projects, I was among the top 4 percent off freshmen who secured an internship at the lab for the
summer. I worked on a project that detects user sentiments in a Twitter account over a period of time
and provides suggestions to lift the mood of the user, by using events detected in their positively catego-
rized tweets. This project was awarded 4th place amidst 25 teams in Honeywell’s “Power Of Connected
Hackathon”. My knack for public speaking, people management, logistical skills, and contributions to the
projects, earned me the prestigious role as the student head for the lab, where I co-led the internship
program for 40 students, the following year. Constant involvement in the student community, shouldering
responsibilities for events, winning beatbox competitions, partaking in team sports, and regularly con-
tributing to the Akshaya Patra Foundation which aims to counter classroom hunger and aid education of
underprivileged kids have broadly developed my personality.
The level of efficiency with which Peer-to-Peer (P2P) networks share large files at blazing speeds ex-
cites me. Intrigued by the piece selection algorithm, I implemented a pure P2P chat and file sharing client
that was tested on multiple users and successfully transferred large files through the campus network. My
professor’s valuable insights on data-stealing vulnerabilities that my implementation was susceptible to
taught me about how it can be optimized into a hybrid P2P network. The depth of complexity in Net-
working inspired me to choose the Computer Network Security (CNS) and Advanced Computer Networks
electives for my 6th semester.
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
1
The Netflix documentary “The Social Dilemma” displayed how social media can be leveraged as a
tool to sway the opinions of the masses. Witnessing the negative effects of misinformation spread and
biased opinions on the CAA-NRC legislation that was shared on Twitter inspired me to work on the
problem, as a part of my capstone project in my final semester. Our team analyzed Twitter users who
had any activity regarding the topic and classified their tweets as positive, negative, or neutral using
stance detection. Working on Long Short Term Memory (LSTM) networks as part of the Topics In Deep
Learning elective enabled me to duly apply my knowledge and implement a multiclass classifier using
bi-directional LSTMs and Convolutional Neural Networks. Unsettled by the initial accuracy, I procured
a much larger data set from Dr. Marjan Hosseinia from the University of Houston that helped our model
achieve a 93 percent accuracy in classifying tweets. The established metrics resulted in successfully detecting
bots and identifying accounts that were spreading propaganda. This echoed the observation from “The
Social Dilemma” where a user was influenced by an online profile that led to his arrest. With invaluable
mentorship from Prof. Bhaskarjyoti Das, this study was published in the Emerging Technologies in Data
Mining and Information Security book as part of the proceedings in the IEMIS 2020 conference.
Alongside the capstone project, I opted to pursue an internship at Epsilon (Digital Marketing), Ben-
galuru as a Software Developer for five months, where my technical competence and commitment earned
meanofferfortheroleofapermanentemployee. UsingmystrongfoundationinJavaandPythonprogram-
ming, I contributed to modifying and developing new REST APIs, Angular applications, AWS Lambdas,
and setting up the CI/CD infrastructure for a centralized service. Consistently exceeding expectations
and being a strong performer, I was recognized and awarded multiple prizes and several appreciation
emails. This professional association enabled me to learn multiple tech stacks and implement practical
solutions with utmost commitment to deliver impactful work while working within strict boundaries of
time. I intend to complement my learning in the industry with a master’s degree in SJSU to develop skills
that will be valuable in my goal to build optimized networks and systems.
SJSU’s MS in Computer Science promises to give me a taste of all aspects of networking and systems
pertinent to my areas of interest. I wish to gain insights in this direction, by opting for courses on Social
Network Analysis, Parallel Processing, and Database Systems, taught by revered professors Dr. Katerina
Potika, Dr. Robert K Chun and Dr. Tsau Lin. Published work on "Overlapping Community Detection"
and "Fake News Analysis and Graph Classification" by Dr. Katerina Potika are examples of projects that
I would like to build upon. I am captivated by the prospect of unearthing insights on how the effects of
social networks influence individuals.
The heavy influence technology has on our minds is exponentially greater than any previous genera-
tion. It is of paramount importance that we solve issues in a manner that does not have profound negative
impacts on the human mind and society. The wealth of knowledge I will amass from graduate courses,
combined with my strong foundation in Computer Science and experience in conducting research will
equip me with technical skills to build scalable, efficient, and ethical software and systems.
Initiatives such as CommUniverCity are specifically relevant to my interests and highlight the support
that SJSU provides for holistic development. Furthermore, I am keen on joining student organizations
such as the Developer Student Club and Computer Science Club to collaborate with like-minded individ-
uals from across disciplines, as well as be in touch with its illustrious Alumni Network.
I am glad that the mission of SJSU’s Computer Science Program is to ensure the responsible de-
velopment of systems and networks to benefit society. It reassures me that SJSU will be the perfect
university for me to explore the interdisciplinary links between networking, algorithms, and governance
for the betterment of society.
    """
    
    processed_text = replace_pii(sample_text)
    print("Original text:")
    print(sample_text)
    print("\nProcessed text:")
    print(processed_text)