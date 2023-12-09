
import unittest
from course_selection import Course, parse_course_data, select_courses


class TestCourseSelection(unittest.TestCase):

    def setUp(self):
        # Set up test data 
        self.course_data = [
            "Python, 5, InCampus, Amy, Thursday 4PM, Technical",
            "Java, 5, InCampus, Jane, Monday 10AM, Technical",
            "Cybersecurity, 3, Online, Donald, Friday 8PM, Technical"
        ]
        self.courses = [parse_course_data(data) for data in self.course_data]

    def test_parse_course_data(self):
        # Test the function of parsing course data
        course_str = "Test Course, 4, Online, Test Instructor, Friday 3PM, Technical"
        course = parse_course_data(course_str)
        self.assertEqual(course.name, "Test Course")
        self.assertEqual(course.credits, 4)
        self.assertEqual(course.mode, "Online")
        self.assertEqual(course.instructor, "Test Instructor")
        self.assertEqual(course.day, "Friday")
        self.assertEqual(course.time, "3PM")
        self.assertEqual(course.category, "Technical")

    def test_conflict_detection(self):
        # Test time conflict detection
        course1 = self.courses[0]
        course2 = Course("Conflict Course", 3, "InCampus", "Test", "Thursday", "4PM", "Technical")
        self.assertTrue(course1.occurs_on_same_time(course2))

    def test_select_courses(self):
        # Test course selection logic
        selected_courses = select_courses(self.courses, max_credits=10)
        total_credits = sum(course.credits for course in selected_courses)
        self.assertLessEqual(total_credits, 10)
        online_courses = [course for course in selected_courses if course.mode == "Online"]
        self.assertLessEqual(len(online_courses), 1)

    def test_max_credit_limit_exceeded(self):
        # Test credits exceed maximum limit
        extra_course = Course("Extra Course", 6, "InCampus", "Extra Instructor", "Wednesday", "2PM", "Technical")
        courses_with_extra = self.courses + [extra_course]
        selected_courses = select_courses(courses_with_extra, max_credits=10)
        total_credits = sum(course.credits for course in selected_courses)
        self.assertLessEqual(total_credits, 10, "Total credits should not exceed the maximum limit")
 
    def test_no_time_conflict(self):
        # Test two courses that do not conflict in time
        course1 = Course("Course1", 3, "InCampus", "Instructor1", "Monday", "10AM", "Technical")
        course2 = Course("Course2", 3, "InCampus", "Instructor2", "Monday", "11AM", "Technical")
        self.assertFalse(course1.occurs_on_same_time(course2), "Courses should not have a time conflict")

    def test_no_courses_selected(self):
        # Test when there are no courses to choose from
        selected_courses = select_courses([], max_credits=10)
        self.assertEqual(len(selected_courses), 0, "No courses should be selected if none are available")

    def test_all_courses_time_conflict(self):
        # Test when all courses have time conflicts 
        conflicting_course = Course("Conflicting Course", 3, "InCampus", "Instructor", "Thursday", "4PM", "Technical")
        courses_with_conflict = self.courses + [conflicting_course]
        selected_courses = select_courses(courses_with_conflict, max_credits=15)
        self.assertNotIn(conflicting_course, selected_courses, "Conflicting courses should not be selected")


if __name__ == '__main__':
    unittest.main()
