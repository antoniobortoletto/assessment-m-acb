class Course:

    def __init__(self, course_id, couse_name):
        self.course_id = course_id
        self.course_name = couse_name
        self.assignments = [] # A course can have many Assignments
        self.students    = [] # A course can have many Students

    def add_assignment(self, assignment):
        self.assignments.append( assignment )
        
    def add_students(self, student):
        self.students.append( student )