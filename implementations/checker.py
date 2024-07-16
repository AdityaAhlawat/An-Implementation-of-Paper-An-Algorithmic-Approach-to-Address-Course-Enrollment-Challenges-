#Fairness Metrics 
import pulp 

def is_ef(allocation, students):
    ef_false_count = 0
    for student in students:
        own_utility = student.utility(allocation)
        for other_student in students:
            if student != other_student:
                other_utility = sum(student.valuation_function.get(course.course_id, 0) for course in allocation[other_student.student_id])
                if other_utility > own_utility:
                    ef_false_count += 1
                    return False, ef_false_count
    return True, ef_false_count

def is_ef1(allocation, students):
    ef1_false_count = 0
    for student in students:
        own_utility = student.utility(allocation)
        for other_student in students:
            if student != other_student:
                other_allocation = allocation[other_student.student_id]
                if len(other_allocation) > 0:
                    max_utility_item = max(other_allocation, key=lambda course: student.valuation_function.get(course.course_id, 0))
                    other_utility = sum(student.valuation_function.get(course.course_id, 0) for course in other_allocation) - student.valuation_function.get(max_utility_item.course_id, 0)
                    if other_utility > own_utility:
                        ef1_false_count += 1
                        return False, ef1_false_count
    return True, ef1_false_count

def is_efx(allocation, students):
    efx_false_count = 0
    for student in students:
        own_utility = student.utility(allocation)
        for other_student in students:
            if student != other_student:
                other_allocation = allocation[other_student.student_id]
                if len(other_allocation) > 0:
                    min_utility_item = min(other_allocation, key=lambda course: student.valuation_function.get(course.course_id, 0))
                    other_utility = sum(student.valuation_function.get(course.course_id, 0) for course in other_allocation) - student.valuation_function.get(min_utility_item.course_id, 0)
                    if other_utility > own_utility:
                        efx_false_count += 1
                        return False, efx_false_count
    return True, efx_false_count

#Efficency metrics
def optimized_social_welfare(students, courses):
    # Create a linear programming problem
    prob = pulp.LpProblem("MaximizeSocialWelfare", pulp.LpMaximize)
    
    # Create a dictionary to hold the decision variables
    x = {}
    for student in students:
        for course in courses:
            x[(student.student_id, course.course_id)] = pulp.LpVariable(
                f"x_{student.student_id}_{course.course_id}", cat='Binary')
    
    # Objective function: Maximize the total utility
    prob += pulp.lpSum(x[(student.student_id, course.course_id)] * student.valuation_function.get(course.course_id, 0)
                       for student in students for course in courses)
    
    # Constraints
    for student in students:
        prob += (pulp.lpSum(x[(student.student_id, course.course_id)] for course in courses) <= student.get_max_credits(),
                 f"CreditCap_{student.student_id}")
        
    for course in courses:
        prob += (pulp.lpSum(x[(student.student_id, course.course_id)] for student in students) <= course.get_seat_capacity(),
                 f"SeatCapacity_{course.course_id}")
    # Solve the problem
    prob.solve()
    # Extract the allocation
    allocation = {student.student_id: [] for student in students}
    for student in students:
        for course in courses:
            if pulp.value(x[(student.student_id, course.course_id)]) == 1:
                allocation[student.student_id].append(course)
    
    # Calculate the total social welfare using the existing utility method
    total_welfare = sum(student.utility(allocation) for student in students)
    
    return total_welfare

#Too computationally expensive
# def optimized_max_min_objective(students, courses):
#     # Create a linear programming problem
#     prob = pulp.LpProblem("MaximizeMinUtility", pulp.LpMaximize)
    
#     # Create a dictionary to hold the decision variables
#     x = {}
#     for student in students:
#         for course in courses:
#             x[(student.student_id, course.course_id)] = pulp.LpVariable(
#                 f"x_{student.student_id}_{course.course_id}", cat='Binary')
    
#     # Create a variable to represent the minimum utility
#     min_utility = pulp.LpVariable("min_utility", lowBound=0)
    
#     # Objective function: Maximize the minimum utility
#     prob += min_utility
    
#     # Constraints
#     for student in students:
#         # Ensure the student's utility is at least min_utility
#         prob += (pulp.lpSum(x[(student.student_id, course.course_id)] * student.valuation_function.get(course.course_id, 0)
#                             for course in courses) >= min_utility, f"MinUtility_{student.student_id}")
        
#         # Ensure the total credits do not exceed the student's maximum credits
#         prob += (pulp.lpSum(x[(student.student_id, course.course_id)] for course in courses) <= student.get_max_credits(),
#                  f"CreditCap_{student.student_id}")
    
#     for course in courses:
#         # Ensure the total seats allocated do not exceed the course's capacity
#         prob += (pulp.lpSum(x[(student.student_id, course.course_id)] for student in students) <= course.get_seat_capacity(),
#                  f"SeatCapacity_{course.course_id}")
    
#     # Solve the problem
#     prob.solve()
    
#     return pulp.value(min_utility)