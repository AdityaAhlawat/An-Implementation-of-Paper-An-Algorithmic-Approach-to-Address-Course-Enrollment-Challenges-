from classes.create_data import Data
from implementations.algorithms import round_robin
from implementations.checker import is_ef, is_ef1, is_efx, optimized_social_welfare

# Experimental proof based on Theorem 12 -> EFX + Social Welfare Optimal when n students, unfirom credit caps, uniform utilities
# Make sure student has a preference of 1 of every course to check this theorem


# Generate data with uniform credit caps and uniform utilities
data = Data(67, 40, 1000, uniform_utilities=True, uniform_credit_caps=True, uniform_course_lengths=True)

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

