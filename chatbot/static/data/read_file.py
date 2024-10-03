def read_text_file_into_string(file_path, encoding="utf-8"):
    try:
        with open(file_path, 'r', encoding=encoding) as file:
            content = file.read()
        return content
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return ""

def data():
    about = read_text_file_into_string("About.txt")
    admissions = read_text_file_into_string("Admissions.txt")
    departments = read_text_file_into_string('Departments.txt')
    facilities = read_text_file_into_string('Facilities.txt')
    placement = read_text_file_into_string('Placement.txt')

    return about, admissions, departments, facilities, placement

if __name__ == "__main__":
    info = data()
    print(info)
