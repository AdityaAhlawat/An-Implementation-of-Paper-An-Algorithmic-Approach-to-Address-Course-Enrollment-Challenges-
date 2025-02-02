import random 
from .course import Course
from .student import Student

class Data:
    def __init__(self, num_of_courses, num_of_students, total_school_time, reproducible: bool = False, uniform_credit_caps: bool = False, uniform_utilities: bool = False, uniform_utilities_1: bool = False, uniform_course_lengths: bool = False, binary_preferences_per_student: bool = False):
        if reproducible:
            random.seed(42)
        else:
            random.seed()

        self.num_of_courses = num_of_courses
        self.num_of_students = num_of_students
        self.courses = []
        self.students = []
        self.total_school_time = total_school_time
        
        # Create Courses
        for i in range(num_of_courses):
            course_id = i + 1
            credits = 1  # Set credits to 1 as per the paper
            seat_capacity = 1  # Set seat capacity to 1 as per the paper
            start_time = random.randint(0, self.total_school_time-1)
            if uniform_course_lengths:
                end_time = start_time + 1  
            else:
                end_time = start_time + random.randint(1, 3)
            course = Course(course_id, credits, seat_capacity, start_time, end_time)
            self.courses.append(course)

        # Create Students
        for j in range(num_of_students):
            student_id = j + 1
            if uniform_utilities_1:
                valuation_function = {course.course_id: 1 for course in self.courses}
            elif uniform_utilities:
                valuation_function = {course.course_id: 3 for course in self.courses}  # Uniform utility for each course
            elif binary_preferences_per_student:
                valuation_function = {course.course_id: random.randint(0, 1) for course in self.courses}
            else:
                valuation_function = {course.course_id: random.randint(1, 10) for course in self.courses}  
            if uniform_credit_caps:
                max_credits = 3
            else:
                max_credits = random.randint(3, 6)
            student = Student(student_id, valuation_function, max_credits)
            self.students.append(student)   
            

    def get_students(self):
        return self.students
    
    def get_courses(self):
        return self.courses
    
    def display_courses(self):
        # Display the courses in a tabular format
        print("{:<10} {:<10} {:<10} {:<10}".format('Course ID', 'Credits', 'Start Time', 'End Time'))
        print("-" * 40)
        for course in self.courses:
            print("{:<10} {:<10} {:<10} {:<10}".format(course.course_id, course.credits, course.start_time, course.end_time))
        
        # Display the courses on a timeline
        print("\nCourse Timings:")
        timeline = [" " * self.total_school_time for _ in range(len(self.courses))]
        for i, course in enumerate(self.courses):
            timeline[i] = timeline[i][:course.start_time] + "=" * (course.end_time - course.start_time) + timeline[i][course.end_time:]
            print("Course {}: {}".format(course.course_id, timeline[i]))

# Example usage:
# data = Data(num_of_courses=5, num_of_students=10, total_school_time=10)
# data.display_courses()
