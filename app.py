from flask import Flask, request, jsonify
from flask_cors import CORS
from spacy.matcher import PhraseMatcher
from skillNer.general_params import SKILL_DB
from skillNer.skill_extractor_class import SkillExtractor
import spacy
from langdetect import detect
from googletrans import Translator

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Load the English model
nlp = spacy.load("en_core_web_sm")

# Initialize skill extractor
skill_extractor = SkillExtractor(nlp, SKILL_DB, PhraseMatcher)

# Initialize translator
translator = Translator()

@app.route('/health', methods=['GET'])
def health_check():
    try:
        # Test if NLP model is working
        test_doc = nlp("Test")
        # Test if skill extractor is working
        test_annotations = skill_extractor.annotate("Test")
        return jsonify({
            "status": "healthy",
            "nlp_model": "en_core_web_sm",
            "skill_extractor": "ready"
        }), 200
    except Exception as e:
        return jsonify({
            "status": "unhealthy",
            "error": str(e)
        }), 500

@app.route('/extract-skills', methods=['POST'])
def extract_skills():
    try:
        # Get input text from request
        data = request.get_json()
        if not data or 'text' not in data:
            return jsonify({'error': 'No text provided'}), 400
        
        input_text = data['text']
        
        # Detect language
        try:
            lang = detect(input_text)
        except:
            lang = 'en'  # Default to English if language detection fails
        
        # If text is not in English, translate it
        if lang != 'en':
            translated = translator.translate(input_text, dest='en')
            input_text = translated.text
        
        # Process the text
        annotations = skill_extractor.annotate(input_text)
        
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
            if skill.lower() in input_text.lower() and skill not in skills:
                skills.append(skill)
        
        # Sort skills alphabetically
        skills.sort()
        
        return jsonify({'skills': skills, 'original_language': lang})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000) 