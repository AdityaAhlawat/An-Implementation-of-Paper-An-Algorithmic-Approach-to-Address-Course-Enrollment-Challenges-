#Fairness Metrics 
import pulp 

def is_ef(allocation, students):
    for student in students:
        own_utility = student.utility(allocation)
        for other_student in students:
            if student != other_student:
                other_utility = sum(student.valuation_function.get(course.course_id, 0) for course in allocation[other_student.student_id])
                if other_utility > own_utility:
                    return False
    return True

def is_ef1(allocation, students):
    for student in students:
        own_utility = student.utility(allocation)
        for other_student in students:
            if student != other_student:
                other_allocation = allocation[other_student.student_id]
                if len(other_allocation) > 0:
                    max_utility_item = max(other_allocation, key=lambda course: student.valuation_function.get(course.course_id, 0))
                    other_utility = sum(student.valuation_function.get(course.course_id, 0) for course in other_allocation) - student.valuation_function.get(max_utility_item.course_id, 0)
                    if other_utility > own_utility:
                        return False
    return True

def is_efx(allocation, students):
    for student in students:
        own_utility = student.utility(allocation)
        for other_student in students:
            if student != other_student:
                other_allocation = allocation[other_student.student_id]
                if len(other_allocation) > 0:
                    min_utility_item = min(other_allocation, key=lambda course: student.valuation_function.get(course.course_id, 0))
                    other_utility = sum(student.valuation_function.get(course.course_id, 0) for course in other_allocation) - student.valuation_function.get(min_utility_item.course_id, 0)
                    if other_utility > own_utility:
                        return False
    return True

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