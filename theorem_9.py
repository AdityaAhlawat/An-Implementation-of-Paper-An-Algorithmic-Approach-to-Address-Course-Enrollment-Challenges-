#Proof of Theorem 9 : Algorithm 1 solves CAUTC-SW 
#Make sure student has a preference of 1 of every course to check this theorem
#Make sure Uniform Credits (since Research Paper said to keep 1 for all credits this is already uniform), Uniform Course Lengths, Uniform Utilities

from classes.create_data import Data
from implementations.algorithms import round_robin
from implementations.checker import is_ef, is_ef1, is_efx, optimized_social_welfare

# Generate data
data = Data(300, 50, 20, uniform_course_lengths=True, uniform_utilities_1=True)

# Get students and courses
students = data.get_students()
courses = data.get_courses()

# Perform round robin course assignment
allocation = round_robin(students, courses)

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
    print(f"Student {student.student_id} assigned courses: {[course.course_id for course in assigned_courses]}, Utility: {utility}")


