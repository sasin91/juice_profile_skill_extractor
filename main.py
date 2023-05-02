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

input = "Jeg er en udpræget teamplayer med 20 års erfaring fra den digitale verden. Jeg er god til mennesker og brænder for innovation, forandring og bæredygtighed. Min drøm er at gøre en forskel for jer."

# init params of skill extractor

# https://danlp-alexandra.readthedocs.io/en/latest/docs/frameworks/spacy.html
# The danish model is buggy, so we use the english model instead
#nlp = load_spacy_model()

# I'm not sure if english web is better than danish news model
nlp = spacy.load("da_core_news_lg")
# nlp = spacy.load("en_core_web_lg")

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
