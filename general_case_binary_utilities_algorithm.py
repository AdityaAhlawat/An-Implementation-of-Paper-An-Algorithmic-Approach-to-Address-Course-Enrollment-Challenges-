#Student should have binary preference for courses. Assume courses have credit 1 each (this is implemented generally in the paper)

from classes.create_data import Data
from implementations.algorithms import binary_utilities_algorithm
from implementations.checker import is_ef, is_ef1, is_efx, optimized_social_welfare

# Generate data
data = Data(121, 50, 20, binary_preferences_per_student=True) 

# Get students and courses
students = data.get_students()
courses = data.get_courses()

# Perform round robin course assignment
allocation = binary_utilities_algorithm(students, courses)

max_social_welfare = optimized_social_welfare(students, courses)

#Lets find the social welfare of our allocation:
total_welfare = sum(student.utility(allocation) for student in students)

# Check for EF, EF1, and EFX
print("Is EF:", is_ef(allocation, students))
print("Is EF1:", is_ef1(allocation, students))
print("Is EFX:", is_efx(allocation, students))
print("Social Welfare: ", total_welfare)
print("Is Social Welfare Optimal?: ", max_social_welfare == total_welfare)
# Print the assignments and utility for each student
for student in students:
    assigned_courses = allocation[student.student_id]
    utility = student.utility(allocation)
    course_details = [
        f"Course {course.course_id} (Start: {course.start_time}, End: {course.end_time})"
        for course in assigned_courses
    ]
    print(f"Student {student.student_id} assigned courses: {course_details}, Utility: {utility}")

#Interestingly Enough Social Welfare has been optimal in all of the tests I have been doing
