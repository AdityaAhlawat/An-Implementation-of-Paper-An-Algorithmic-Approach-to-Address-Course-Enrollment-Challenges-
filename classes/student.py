class Student:
    def __init__(self, student_id, valuation_function, max_credits):
        self.student_id = student_id  # Student ID is used just so we can uniquely identify each Student Object.
        self.valuation_function = valuation_function  # Utility should be a dictionary where keys are course_ids and values are utility values
        self.max_credits = max_credits

    def __repr__(self):
        return (f"Student(id={self.student_id}, valuation_function={self.valuation_function}, "
                f"courses={self.courses}, max_credits={self.max_credits})")
    
    def utility(self, allocation):
        return sum(self.valuation_function.get(course.course_id, 0) for course in allocation[self.student_id])
    
    def get_max_credits(self):
        return self.max_credits


