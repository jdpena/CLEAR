import json

def formatEntries(system_entries, other_entries):
    # Format system entries
    formatted_system_entries = f"<s>[INST] <<SYS>>\n{' '.join(system_entries)}\n<</SYS>>\n"
    
    # Format other entries
    formatted_other_entries = '\n'.join(other_entries)
    
    # Combine and return the formatted entries
    return formatted_system_entries + formatted_other_entries

def separateEntries(data):
    system_entries = []
    other_entries = []

    for entry in data:
        role = entry.get('role')
        content = entry.get('content')
        if role == 'system':
            system_entries.append(content)
        else:  # This will include both 'user' and 'assistant' roles
            other_entries.append(content)

    return system_entries, other_entries

def parseJson(json_data):
        # If json_data is a list, take the first element (assuming the first element is the desired data)
        if isinstance(json_data, list):
            json_data = json_data[0]

        # If json_data is a dictionary and contains 'generated_text' key
        if isinstance(json_data, dict) and 'generated_text' in json_data:
            inst_index = json_data['generated_text'].find('[/INST]')
            
            if inst_index != -1:
                return json_data['generated_text'][inst_index + len('[/INST] '):].strip()
        # Handle other cases as needed
        else:
            print(f"Unexpected data: {json_data}")
            return None  # or handle in a different way
        
def reformat(json):
    system_entries, other_entries = separateEntries(json)
    information = formatEntries(system_entries, other_entries) + "[/INST]"

    # Construct the input for the LLM
    return {
        "inputs": information,
        "parameters": {
            "max_length": 16384,
            "temperature": 1,
            "top_k": 2000
        },
        "options": {
            "use_cache": False,
            "wait_for_model": True
        }
    }