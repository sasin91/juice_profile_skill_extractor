import os
import sys
import json
from spacy.matcher import PhraseMatcher
from skillNer.general_params import SKILL_DB
from skillNer.skill_extractor_class import SkillExtractor
#from danlp.models import load_spacy_model
import spacy
# Input from command line (stdin)
filename = sys.argv[1]

if (filename == ''):
    raise RuntimeError('No filename provided')

# input = "Jeg er en udpræget teamplayer med 20 års erfaring fra den digitale verden. Jeg er god til mennesker og brænder for innovation, forandring og bæredygtighed. Min drøm er at gøre en forskel for jer."

input = """"
As a web programmer with nine years of experience using PHP and JavaScript, I have developed a deep understanding of web development and the technologies used in this field. 

Over the years, I have honed my skills in developing robust and scalable web applications using PHP and JavaScript frameworks. 

I am proficient in developing custom web applications as well as integrating third-party applications into existing ones. 

My proficiency in PHP and JavaScript has enabled me to create dynamic and interactive user interfaces that provide an unparalleled user experience. Additionally, I am adept at debugging and troubleshooting complex issues in web applications, ensuring that they run smoothly and efficiently.

Overall, my experience as a web programmer has given me the knowledge and skills necessary to create high-quality web applications that meet the needs of clients and users alike.    
"""

# init params of skill extractor

# https://danlp-alexandra.readthedocs.io/en/latest/docs/frameworks/spacy.html
# The danish model is buggy, so we use the english model instead
#nlp = load_spacy_model()

# I'm not sure if english web is better than danish news model
# nlp = spacy.load("da_core_news_lg")
nlp = spacy.load("en_core_web_lg")

# init skill extractor
skill_extractor = SkillExtractor(nlp, SKILL_DB, PhraseMatcher)

skills = []

annotations = skill_extractor.annotate(input)

print(annotations)

results = annotations["results"]
full_matches = results["full_matches"]
full_matches.sort(key=lambda match: match["score"])

items = list(
    map(lambda match: match["doc_node_value"], full_matches))

if items:
    for item in items:
        if item not in skills:
            skills.append(item)

if skills:
    json_object = json.dumps(skills, indent=4)

    with open(os.path.join('output', filename + '.json'), 'w') as outfile:
        outfile.write(json_object)
        print(outfile.name)
