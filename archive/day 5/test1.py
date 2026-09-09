import re
import pandas as pd

# The messy text message from the duty manager
dispatch_message = "Update from the tarmac: Flight QJ-309 has landed safely. The total payload unloaded was 4500 kg. No delays reported.Update from the tarmac: Flight QJ-301 has landed safely. The total payload unloaded was 400 kg. No delays reported."

def parse_dispatch_text(text):
    print("__Extraction  of filght nunmber an payload__")
    
    pattern = r"[A-Z]{2}-\d{3}"
    flight_number = re.findall(pattern,text)
    print(f"Flight Number: {flight_number[0] if flight_number else 'Not found'}")
    
    payLoad_pattern = r"\d+\skg"
    
    payLoad = re.findall(payLoad_pattern,text)
    print(f"Payload: {payLoad[0] if payLoad else 'Not found'}")
    
    df = pd.DataFrame({'Flight Number': flight_number, 'Payload': payLoad})
    print("\n__Dataframe of extracted information__")
    print(df)
    return df 
parse_dispatch_text(dispatch_message)