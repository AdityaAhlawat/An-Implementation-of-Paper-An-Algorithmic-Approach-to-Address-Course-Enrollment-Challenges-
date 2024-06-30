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


