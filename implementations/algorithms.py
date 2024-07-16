from collections import defaultdict, deque
from classes.course import Course
#Algorithm 1
def round_robin(students, courses):
    # Sort courses by earliest finish time
    courses.sort(key=lambda course: course.end_time)
    
    # Initialize student allocation to empty lists
    allocation = {student.student_id: [] for student in students}
    
    for course in courses:
        # Get eligible students who can take the course
        eligible_students = []
        
        for student in students:
            if len(allocation[student.student_id]) < student.max_credits:
                has_conflict = False
                for assigned_course in allocation[student.student_id]:
                    if (assigned_course.start_time < course.end_time and 
                        course.start_time < assigned_course.end_time):
                        has_conflict = True
                        break
                
                if not has_conflict:
                    eligible_students.append(student)
        
        if eligible_students:
            # Find the student with the fewest assigned courses
            selected_student = min(eligible_students, key=lambda student: len(allocation[student.student_id]))
            # Assign the course to the selected student
            allocation[selected_student.student_id].append(course)
    
    return allocation

#Algorithm 2 
def binary_utilities_algorithm(students, courses):
    # Sort students by credit caps in non-increasing order
    students.sort(key=lambda student: student.get_max_credits(), reverse=True)
    
    # Initialize student assignments to empty sets
    allocation = {student.student_id: [] for student in students}
    
    # Iterate over each student in sorted order
    for student in students:
        # Find the courses that the student values
        valued_courses = [course for course in courses if student.valuation_function.get(course.course_id, 0) > 0]
        
        # Initialize the MIS (Maximum Independent Set) to be empty
        mis_courses = []
        
        # Add courses to MIS if they don't conflict with already selected courses
        for course in valued_courses:
            if len(mis_courses) < student.get_max_credits():
                has_conflict = False
                for assigned_course in mis_courses:
                    if (assigned_course.start_time < course.end_time and 
                        course.start_time < assigned_course.end_time):
                        has_conflict = True
                        break
                
                if not has_conflict:
                    mis_courses.append(course)
        
        # If the size of the MIS is greater than the student's credit cap, resize the MIS
        if len(mis_courses) > student.get_max_credits():
            # Sort the MIS by end time
            mis_courses.sort(key=lambda course: course.end_time)
            # Resize the MIS to be the first Ci courses in the MIS
            mis_courses = mis_courses[:student.get_max_credits()]
        
        # Assign the resized MIS to the student
        allocation[student.student_id] = mis_courses
        
        # Remove the assigned courses from the set of available courses
        courses = [course for course in courses if course not in mis_courses]
    
    return allocation

#Algorithm 3 
def round_robin_for_binary_utilities(students, courses):
    # Sort courses chronologically by earliest finish time
    courses.sort(key=lambda course: course.end_time)
    
    # Initialize student assignments to empty sets
    allocation = {student.student_id: [] for student in students}
    
    # Iterate over each course in sorted order
    for course in courses:
        # Find all students who value this course, have not exceeded their credit cap,
        # and do not have a conflict with the course
        eligible_students = []
        for student in students:
            if (student.valuation_function.get(course.course_id, 0) == 1 and 
                len(allocation[student.student_id]) < student.get_max_credits()):
                has_conflict = False
                for assigned_course in allocation[student.student_id]:
                    if (assigned_course.start_time < course.end_time and 
                        course.start_time < assigned_course.end_time):
                        has_conflict = True
                        break
                if not has_conflict:
                    eligible_students.append(student)
        
        # If there are eligible students, assign the course to the one with the fewest courses assigned
        if eligible_students:
            eligible_students.sort(key=lambda student: len(allocation[student.student_id]))
            selected_student = eligible_students[0]
            allocation[selected_student.student_id].append(course)
    
    return allocation

#Algorithm #4 
def max_min_assignment_for_binary_utilities(students, courses):
    # Sort courses by end time from earliest to latest
    courses.sort(key=lambda course: course.end_time)
    
    # Initialize data structures
    D = set()
    Q = deque()
    allocation = {student.student_id: [] for student in students}
    graph = defaultdict(list)  # To store the edges of the graph
    
    # Assign courses to students initially
    for course in courses:
        eligible_students = [student for student in students if student.max_credits > len(allocation[student.student_id]) and student.valuation_function.get(course.course_id, 0) > 0 and not any(conflicts_with(c, course) for c in allocation[student.student_id])]
        if eligible_students:
            student = min(eligible_students, key=lambda s: len(allocation[s.student_id]))
            allocation[student.student_id].append(course)
            Q.append(student)
    
    def draw_edge(from_node, to_node):
        graph[from_node].append(to_node)
    
    def find_augmenting_path(source, sink):
        visited = set()
        parent = {}
        queue = deque([source])
        
        while queue:
            node = queue.popleft()
            if node == sink:
                path = []
                while node in parent:
                    path.append(node)
                    node = parent[node]
                path.append(source)
                return path[::-1]
            
            for neighbor in graph[node]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    parent[neighbor] = node
                    queue.append(neighbor)
        return None

    def reassign_courses(augmenting_path):
        for i in range(len(augmenting_path) - 1):
            from_node = augmenting_path[i]
            to_node = augmenting_path[i + 1]
            
            # Remove the course from the current student's allocation
            if isinstance(from_node, Course) and isinstance(to_node, Course):
                for student_id, courses in allocation.items():
                    if to_node in courses:
                        allocation[student_id].remove(to_node)
                        allocation[student_id].append(from_node)
                        break
    
    # Find and process augmenting paths
    AugPath = True
    while AugPath:
        while Q:
            student_i_prime = Q.popleft()
            for course_j in allocation[student_i_prime.student_id]:
                for student_b in students:
                    if student_b != student_i_prime:
                        if any(conflicts_with(course_j, course_j_prime) for course_j_prime in allocation[student_b.student_id]):
                            eligible_courses = [course_j_prime for course_j_prime in allocation[student_b.student_id] if conflicts_with(course_j, course_j_prime) and len(allocation[student_b.student_id]) < len(allocation[student_i_prime.student_id]) and student_b not in D]
                            for course_j_prime in eligible_courses:
                                Q.append(student_b)
                                D.add(student_i_prime)
                                draw_edge(course_j_prime, course_j)
                        
                        if not any(conflicts_with(course_j, course_j_prime) for course_j_prime in allocation[student_b.student_id]) and len(allocation[student_b.student_id]) <= len(allocation[student_i_prime.student_id]):
                            Q.append(student_b)
                            draw_edge(DummyCourse(student_b.student_id), course_j)
            
            D.add(student_i_prime)
            
            # Find an augmenting path
            source = DummyCourse(student_i_prime.student_id)
            sink = course_j
            augmenting_path = find_augmenting_path(source, sink)
            if augmenting_path:
                reassign_courses(augmenting_path)
            else:
                AugPath = False
    
    return allocation

class DummyCourse:
    def __init__(self, student_id):
        self.student_id = student_id

def conflicts_with(course1, course2):
    # Assuming a course conflicts with another if they overlap in time
    return not (course1.end_time <= course2.start_time or course1.start_time >= course2.end_time)
