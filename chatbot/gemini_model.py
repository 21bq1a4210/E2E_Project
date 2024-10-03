# Import the Python SDK
import google.generativeai as genai

def read_text_file_into_string(file_path, encoding="utf-8"):
    try:
        with open(file_path, 'r', encoding=encoding) as file:
            content = file.read()
        return content
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return ""

def data():
    about = read_text_file_into_string("chatbot/About.txt")
    admissions = read_text_file_into_string("chatbot/Admissions.txt")
    departments = read_text_file_into_string('chatbot/Departments.txt')
    facilities = read_text_file_into_string('chatbot/Facilities.txt')
    placement = read_text_file_into_string('chatbot/Placement.txt')

    return about.strip(), admissions.strip(), departments.strip(), facilities.strip(), placement.strip()

def format_response(response_text):
    # Convert Markdown-like elements to HTML
    html_response = response_text
    html_response = html_response.replace("**", "<strong>").replace("**", "</strong>")  # Bold
    html_response = html_response.replace("*", "<em>").replace("*", "</em>")  # Italics
    html_response = html_response.replace("\n", "<br>")  # New line to line break
    html_response = html_response.replace("### ", "<h3>").replace("###", "</h3>")  # H3 Header
    html_response = html_response.replace("## ", "<h2>").replace("##", "</h2>")  # H2 Header
    # html_response = html_response.replace("# ", "<h1>").replace("#", "</h1>")  # H1 Header
    html_response = html_response.replace("`", "<code>").replace("`", "</code>")  # Code blocks
    return f"<div>{html_response}</div>"

def chat(message):
    try:
        # GOOGLE_API_KEY=userdata.get('GOOGLE_API_KEY')
        genai.configure(api_key='AIzaSyCcTYrQWo2eUfKl4grSZKlnTJ_s48KJf98')

        model = genai.GenerativeModel('gemini-pro')

        about, admissions, departments, facilities, placement = data()

        # Extract the section and question from the combined message
        if message.startswith("[ABOUT]"):
            relevant_info = about
        elif message.startswith("[ADMISSIONS]"):
            relevant_info = admissions
        elif message.startswith("[DEPARTMENTS]"):
            relevant_info = departments
        elif message.startswith("[FACILITIES]"):
            relevant_info = facilities
        elif message.startswith("[PLACEMENT]"):
            relevant_info = placement
        else:
            relevant_info = "Sorry, I couldn't understand the section you are asking about."
        # print(relevant_info)
        question = message.split("]")[1].strip()  # Extract the actual question

        prompt = f"""
                You are a highly knowledgeable assistant specializing in the following college data:
                {relevant_info}

                User Question: {question}
                Assistant Response:
                """

        response = model.generate_content(prompt)
        return response.text.strip()

    except Exception as e:
        print(f"An error occurred: {e}")
        return "An error occurred while processing your request. Please try again later."

if __name__ == '__main__':
    print(chat(input('Enter your message: ')))
