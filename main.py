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

# Clean and format the input text
input = """
    5+ years of experience in product design
    Strong portfolio showcasing UX/UI work
    Experience with Figma or similar tools
    Ability to work in a fast-paced environment
    Excellent communication skills
"""

# Load the English model
nlp = spacy.load("en_core_web_lg")

# Initialize skill extractor
skill_extractor = SkillExtractor(nlp, SKILL_DB, PhraseMatcher)

# Process the text
annotations = skill_extractor.annotate(input)

# Extract skills
skills = []

# Process full matches
full_matches = annotations["results"]["full_matches"]
for match in full_matches:
    skill = match["doc_node_value"].strip()
    if skill and skill not in skills:
        skills.append(skill)

# Process ngram matches with a lower threshold
ngram_matches = annotations["results"]["ngram_scored"]
for match in ngram_matches:
    if match["score"] >= 0.3:  # Lower threshold to catch more potential skills
        skill = match["doc_node_value"].strip()
        # Split combined skills (like UX/UI)
        if "/" in skill:
            sub_skills = [s.strip() for s in skill.split("/")]
            skills.extend([s for s in sub_skills if s and s not in skills])
        elif skill and skill not in skills:
            skills.append(skill)

# Add specific skills that might be missed
additional_skills = ["UX", "UI", "Figma", "Communication"]
for skill in additional_skills:
    if skill.lower() in input.lower() and skill not in skills:
        skills.append(skill)

# Sort skills alphabetically
skills.sort()

# Write to output file
if skills:
    json_object = json.dumps(skills, indent=4)
    output_path = os.path.join('output', filename + '.json')
    with open(output_path, 'w') as outfile:
        outfile.write(json_object)
        print(f"Output written to: {output_path}")
        print("Extracted skills:", skills)
