from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification

def load_ai_detector():
    model_name = "optical908/distilBert-Ai-text-detector"
    try:
        # Load model with from_tf=True to convert TensorFlow weights
        model = AutoModelForSequenceClassification.from_pretrained(
            model_name,
            from_tf=True  # Specify that we're loading from TensorFlow weights
        )
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        return model, tokenizer
    except Exception as e:
        print(f"Error loading model: {str(e)}")
        return None, None

def detect_ai_text(text, model, tokenizer):
    try:
        inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
        outputs = model(**inputs)
        probabilities = outputs.logits.softmax(dim=-1)
        
        # Assuming binary classification (human/AI)
        ai_probability = probabilities[0][1].item()
        human_probability = probabilities[0][0].item()
        
        return {
            "ai_probability": round(ai_probability * 100, 2),
            "human_probability": round(human_probability * 100, 2),
            "prediction": "AI-generated" if ai_probability > human_probability else "Human-written"
        }
    except Exception as e:
        print(f"Error during detection: {str(e)}")
        return None

# Usage example
def main():
    # Load model
    model, tokenizer = load_ai_detector()
    if model is None or tokenizer is None:
        return
    
    # Example text
    text = """
Statement of Purpose

When I was a child, I was struck by a thunderstorm while trying to hack into my toaster. This electrifying experience ignited my passion for computer science. From that moment, I realized my destiny lay in transforming the digital world—one nonsensical line of code at a time.

My academic journey has been a rollercoaster of randomness. I majored in “General Curiosity” during my undergraduate studies, where I excelled in procrastination and surviving on caffeine. I spent countless hours pondering why semicolons are mandatory in some programming languages and optional in others. This intellectual curiosity led me to invent my own programming language, "OopsLang," which self-destructs upon execution. While it hasn't gained mainstream traction, it embodies my unique approach to problem-solving.

I am particularly drawn to your institution because of its unparalleled Wi-Fi speeds and the rumor that the cafeteria serves the best pizza in the region. I believe the distinguished faculty can help me refine my groundbreaking research on a highly theoretical topic: “The Philosophy of Null Pointers and Their Emotional Impacts on Developers.” This underexplored area of study promises to revolutionize debugging sessions globally.

My work experience is as unconventional as my academic background. I once worked as a part-time “Internet Explorer Performance Consultant,” helping people switch to Chrome. During this time, I also discovered my talent for multitasking—debugging code while binge-watching cat videos. These skills, coupled with my ability to invent problems where none exist, make me a strong candidate for your program.

In conclusion, my application to your program is driven by my unwavering desire to become a computer scientist of questionable repute. I am confident that with my eccentricities and your resources, we can create chaos, confusion, and possibly an accidental innovation. Thank you for considering this humble attempt at an SOP.

Sincerely,
A Visionary Thinker Who Clicks "I Agree" Without Reading Terms and Conditions
        
"""
    
    # Get prediction
    result = detect_ai_text(text, model, tokenizer)
    if result:
        print(f"Prediction: {result['prediction']}")
        print(f"AI Probability: {result['ai_probability']}%")
        print(f"Human Probability: {result['human_probability']}%")

if __name__ == "__main__":
    main()