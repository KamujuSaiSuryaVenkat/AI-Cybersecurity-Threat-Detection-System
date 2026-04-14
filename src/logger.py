import datetime
import json
import os

def log_event(data, prediction_result):
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
        
    log_file = os.path.join(log_dir, "detections.log")
    
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = {
        "timestamp": timestamp,
        "data_input": data,
        "result": prediction_result
    }
    
    with open(log_file, "a") as f:
        f.write(json.dumps(log_entry) + "\n")