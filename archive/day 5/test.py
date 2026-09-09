
from textblob import TextBlob

# A simulated list of feedback reports from the ground crew
crew_reports = [
    "The new cargo loading process is incredibly fast and efficient.",
    "Lighting on the tarmac is terrible, it is completely unsafe for night shifts.",
    "Operations are running normally today with no major issues.",
    "The updated security protocols are very confusing and slowing us down."
]

def analyze_crew_feedback(reports):
    print("--- Starting Automated NLP Sentiment Analysis ---\n")
    
    for report in reports:
        # 1. Initialize the TextBlob object with the report string
        blob = TextBlob(report)
        
        # 2. Extract the polarity score using blob.sentiment.polarity
        # (This will give you a float between -1.0 and 1.0)
        polarity_score = blob.sentiment.polarity
        
        # 3. Write your conditional logic here:
        
        # If the score is less than 0 (negative), print a warning with the report text.
        # If the score is greater than 0 (positive), print a success message.
        
        if polarity_score < 0:
            print(f"Warning: Negative feedback detected! Report: {report}")
        elif polarity_score > 0:
            print(f"Success: Positive feedback detected! Report: {report}")
        else:
            print(f"Info: Neutral statement detected. Report: {report}")
analyze_crew_feedback(crew_reports)