
import datetime
from user_input import input_semester, input_course_preferences, input_instructor_preferences


class Course:
    """Represents courses with various attributes."""
    def __init__(self, name, credits, mode, instructor, day, time, category):
        self.name = name
        self.credits = credits
        self.mode = mode
        self.instructor = instructor
        self.day = day
        self.time = time
        self.category = category

    def parse_time(self):
        """Convert a time string into a datetime object."""
        days = {"Monday": 0, "Tuesday": 1, "Wednesday": 2, "Thursday": 3, "Friday": 4}
        day_number = days[self.day]
        hour = int(self.time[:-2]) % 12 + (12 if 'PM' in self.time else 0)

        # Use 1-1-2023 as baseline
        base_date = datetime.datetime(2023, 1, 1)
        day_delta = datetime.timedelta(days=day_number)
        return base_date + day_delta + datetime.timedelta(hours=hour)

    def occurs_on_same_time(self, other):
        """Check if this course occurs at the same time as another course."""
        return self.day == other.day and self.parse_time() == other.parse_time()


def parse_course_data(data):
    """
    Parse a string containing course data and return a Course object.

    Args:
    data (str): A string containing course details.

    Returns:
    Course: An instance of Course with the provided data.
    """
    name, credits, mode, instructor, schedule, category = data.split(', ')
    day, time = schedule.rsplit(' ', 1)
    return Course(name, int(credits), mode, instructor, day, time, category)


def select_courses(courses, max_credits=10):
    """
    Select courses based on provided courses list and credit limits.

    Args:
    courses (list of Course): A list of Course objects to select from.
    max_credits (int): The maximum number of credits to select. Default is 10.

    Returns:
    list of Course: A list of selected courses within the credit limit.
    """
    selected_courses = []
    total_credits = 0
    online_course_selected = False
    for course in courses:
        if total_credits + course.credits > max_credits:
            continue
        if course.mode.lower() == 'online':
            if online_course_selected:
                continue
            else:
                online_course_selected = True
        conflict = False
        for selected_course in selected_courses:
            if course.occurs_on_same_time(selected_course):
                conflict = True
                break
        if not conflict:
            selected_courses.append(course)
            total_credits += course.credits
    return selected_courses


def display_courses(courses):
    """
    Display a list of selected courses.

    Args:
    courses (list of Course): A list of Course objects to be displayed.
    """
    if courses:
        print("Selected Courses:")
        for course in courses:
            print(f"{course.name}, {course.credits} Credits, {course.mode}, {course.instructor}, {course.day} {course.time}, {course.category}")
    else:
        print("No courses could be selected based on the preferences and constraints.")


def advise_credit_distribution(selected_courses):
    """
    Provide advice on credit distribution based on selected courses.

    Args:
    selected_courses (list of Course): A list of selected Course objects.

    Returns:
    list of str: Advice strings on credit distribution.
    """
    category_credits = {}
    for course in selected_courses:
        category_credits[course.category] = category_credits.get(course.category, 0) + course.credits

    advice = []
    for category, credits in category_credits.items():
        if credits / sum(category_credits.values()) < 0.3:
            advice.append(f"Increase your credits in {category} for a more balanced course load.")

    return advice if advice else ["Your credit distribution is well balanced across categories."]


# Course data with categories
course_data = [
    "Python, 5, InCampus, Amy, Thursday 4PM, Technical",
    "Python, 5, InCampus, Amy, Friday 4PM, Technical",
    "Python, 5, InCampus, Andrew, Thursday 4PM, Technical",
    "Python, 5, InCampus, Andrew, Friday 4PM, Technical",
    "Java, 5, InCampus, Jane, Monday 10AM, Technical",
    "Java, 5, InCampus, Jane, Monday 2PM, Technical",
    "Java, 5, InCampus, John, Monday 10AM, Technical",
    "Java, 5, InCampus, Jane, Thursday 10AM, Technical",
    "Game Design Basics, 3, InCampus, James, Monday 10AM, Practical",
    "Game Design Basics, 3, InCampus, Duncan, Monday 10AM, Practical",
    "Game Design Basics, 3, InCampus, Jordan, Friday 2PM, Practical",
    "Foundations of Natural Language Processing, 3, Online, Adams, Tuesday 2PM, Theoretical",
    "Foundations of Natural Language Processing, 3, InCampus, Williams, Tuesday 10AM, Theoretical",
    "Foundations of Natural Language Processing, 3, InCampus, Taylor, Tuesday 2PM, Theoretical",
    "Foundations of Natural Language Processing, 3, Online, David, Wednesday 2PM, Theoretical",
    "Advanced Machine Learning, 3, Online, John Wick, Wednesday 4PM, Technical",
    "Advanced Machine Learning, 3, Online, John Wick, Friday 4PM, Technical",
    "Advanced Machine Learning, 3, InCampus, Jane, Wednesday 4PM, Technical",
    "Advanced Machine Learning, 3, InCampus, John Wick, Thursday 4PM, Technical",
    "Web Development Fundamentals, 3, InCampus, Tom Cruise, Monday 4PM, Practical",
    "Web Development Fundamentals, 3, InCampus, Tom Cruise, Tuesday 4PM, Practical",
    "Web Development Fundamentals, 3, InCampus, Tom Cruise, Thursday 4PM, Practical",
    "Web Development Fundamentals, 3, Online, Tom Cruise, Friday 4PM, Practical",
    "Algorithms, 5, InCampus, Jessie J, Monday 10AM, Theoretical",
    "Algorithms, 5, InCampus, Jessie J, Tuesday 10AM, Theoretical",
    "Algorithms, 5, InCampus, Jessie J, Wednesday 2PM, Theoretical",
    "Algorithms, 5, InCampus, Jessie J, Friday 2PM, Theoretical",
    "Operating Systems, 3, InCampus, Lady Gaga, Monday 8AM, Technical",
    "Operating Systems, 3, InCampus, Lady Gaga, Tuesday 8AM, Technical",
    "Operating Systems, 3, InCampus, Lady Gaga, Friday 8AM, Technical",
    "Computer Graphics, 3, InCampus, John Mayer, Monday 6PM, Practical",
    "Computer Graphics, 3, InCampus, John Mayer, Tuesday 6PM, Practical",
    "Computer Graphics, 3, InCampus, John Mayer, Wednesday 6PM, Practical",
    "Cybersecurity, 3, Online, Donald, Monday 8PM, Technical",
    "Cybersecurity, 3, Online, Donald, Friday 8PM, Technical"
]


def main():
    if input_semester():
        fall_courses = [parse_course_data(data) for data in course_data]
        course_pref = input_course_preferences(fall_courses)
        if course_pref is None:
            return  # Exit the main program
        instructor_pref = input_instructor_preferences(course_pref)
        selected_courses = select_courses(instructor_pref)
        display_courses(selected_courses)

        credit_advice = advise_credit_distribution(selected_courses)
        for advice in credit_advice:
            print(advice)


if __name__ == "__main__":
    main()
