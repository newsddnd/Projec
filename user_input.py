
def input_semester():
    """
    Users are prompted to enter the semester they wish to register for.
    Only valid for "Fall" semester.
    """
    semester = input("Which semester do you want to enroll in? ")
    if semester.lower() != "fall":
        print("Sorry, only fall semester courses are available.")
        return False
    return True


def input_course_preferences(courses):
    """
    Prompt the user to input their course preferences and return the matched courses.

    Args:
    courses (list of Course): The list of available courses to choose from.

    Returns:
    list of Course: The list of courses that match the user's preferences.
                    None if the user chooses to exit.
    """
    while True:
        print("List your course preferences by name, separated by commas (or press enter to exit):")
        input_str = input()
        if input_str == "":
            print("Exiting course selection.")
            return None

        preferences = input_str.split(',')
        preferred_courses = []
        not_found_courses = []
        for pref in preferences:
            pref = pref.strip().lower()
            matched_courses = [course for course in courses if course.name.lower() == pref]
            if not matched_courses:
                not_found_courses.append(pref)
            preferred_courses.extend(matched_courses)

        if not_found_courses:
            print(f"No matching courses found for: {', '.join(not_found_courses)}. Please try again.")
        else:
            return preferred_courses


def input_instructor_preferences(courses):
    """
    Prompt the user to input their instructor preferences and return courses that match these preferences.

    If the user does not specify any preferences, all courses are considered as preferred.

    Args:
    courses (list of Course): The list of available courses to choose from.

    Returns:
    list of Course: The list of courses that match the user's instructor preferences. 
                    If no preferences are specified, all courses are returned.
    """
    print("List your instructor preferences by name, separated by commas (optional):")
    preferences = input().split(',')
    preferred_instructors = [pref.strip().lower() for pref in preferences if pref.strip()]
    return [course for course in courses if course.instructor.lower() in preferred_instructors or not preferred_instructors]
