import json
def jsonParse(content):
    try:
        return json.loads(content)
    except ValueError:
        return "Error parsing json"
    except Exception as e:
        print(f"Error: {e}")    
        return "Error parsing json"
