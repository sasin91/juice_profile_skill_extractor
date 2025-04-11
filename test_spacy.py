import spacy
import sys

def test_spacy():
    print(f"Python version: {sys.version}")
    print(f"spaCy version: {spacy.__version__}")
    
    # Try loading a small English model
    try:
        nlp = spacy.load("en_core_web_sm")
        print("Successfully loaded English model")
        
        # Test basic NLP functionality
        doc = nlp("This is a test sentence.")
        print("\nTokenization test:")
        for token in doc:
            print(f"Token: {token.text}, POS: {token.pos_}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_spacy() 