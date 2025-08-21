# Ollama prompt templates
import yaml

def load_learning_paths(file_path=r"C:\Users\korde\Home\Github\SageEduMint\src\syllabus\paths.yaml"):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

def generate_syllabus_prompt(learning_path_name):
    """
    Generates a prompt for Ollama to create a syllabus based on a learning path.
    """
    paths = load_learning_paths()
    selected_path = None
    for path in paths['learning_paths']:
        if path['path'] == learning_path_name:
            selected_path = path
            break

    if not selected_path:
        return "Error: Learning path not found."

    prompt = f"Generate a detailed syllabus for the \"{selected_path['name']}\" learning path. " \
             f"Include the following modules: {', '.join([m['name'] for m in selected_path['modules']])}. " \
             "For each module, suggest key topics, learning objectives, and a brief description. " \
             "The syllabus should be structured for a self-paced, decentralized learning environment."
    return prompt

if __name__ == "main":
    # Example usage:
    prompt = generate_syllabus_prompt("web_development")
    print(prompt)
