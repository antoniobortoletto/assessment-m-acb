from app.course_service import CourseService
from app.course import Course
from app.assignment import Assignment
from app.student import Student
from app.grade import Grade

import re # Regular Expression
import math

class CourseServiceImpl(CourseService):

    def __init__(self):
         # Save objects in memory
        self.course_list = []
        self.assignment_list = []
        self.student_list = []
        self.grade_list = []

        # Unique identifier for course and assignment
        self.serial_course_id = 0 # Course ID serial
        self.serial_assignment_id = 0 # Assignment ID serial

    # ----------------------------------------------------------
    # helper functions for serials
    def generate_course_id(self):
        self.serial_course_id = self.serial_course_id+1
        return self.serial_course_id
    
    def generate_assignment_id(self):
        self.serial_assignment_id = self.serial_assignment_id+1
        return self.serial_assignment_id
    
    # Helper function to find course in a list
    # Returns the index and the course
    def find_course_by_id(self, course_id):
        for i in range(len(self.course_list)) :
            if self.course_list[i].course_id == course_id:
                return [i, self.course_list[i]] # return index and object
        return None
    
    # Helper function to find assignment in a list
    # Returns the index and the assignment
    def find_assignment_by_id(self, assignment_id):
        for i in range(len(self.assignment_list)) :
            if self.assignment_list[i].assignment_id == assignment_id:
                return [i, self.assignment_list[i]] # return index and object
        return None
    
    # Helper function to find student in a list
    # Returns the index and the student
    def find_student_by_id(self, student_id):
        for i in range(len(self.student_list)) :
            if self.student_list[i].student_id == student_id:
                return [i, self.student_list[i]] # return index and object
        return None
    
    # Valiate course name or assignment name. 
    # Cannot be None
    # Should be a string type
    # At least one character.
    # Cannot exceed 100
    # Cannot be empty
    # Can contain only letters, numbers, :,./&_- and space
    # Return: if name is valid, it returns the name formated, otherwise, throw an Exception
    def validate_name(self, name):
        if name == None:
            raise ValueError("Name cannot be None")
        
        if not isinstance(name, str): # should be a string
            raise ValueError("Name should be a valid string")
        
        name = name.strip() # remove left right space
        name = " ".join(name.split()) # remove additional space betwen words
        len_name = len(name)
        if len_name<1 or len_name>100:
            raise ValueError("Name should be at least one character and cannot exceed 100")
        
        pattern = r'^[a-zA-Z0-9:,.//&_\-\s]+$'
        if re.fullmatch(pattern, name):
            return name
        else:
             raise ValueError("Name should contains only numbers, letter and the characters : , . / & _ - ")

    
    # ----------------------------------------------------------
    # Override
    # Returns a list of all courses.
    def get_courses(self):
        return self.course_list

    # Override
    # Returns a course by its id.
    def get_course_by_id(self, course_id):
        result = self.find_course_by_id(course_id) # returns [index, object] or None
        if (result is None):
            return None
        else:
            return result[1]

    # Override
    # Returns a list of all courses.
    def create_course(self, course_name):
        course_name = self.validate_name(course_name)

        course_id = self.generate_course_id()
        course = Course(course_id, course_name)
        # save
        self.course_list.append(course)
        return course
    
    # Override
    # Deletes a course by its id.
    def delete_course(self, course_id):
        result = self.find_course_by_id(course_id) # returns [index, object] or None
        if (result == None):
            return False
        else:
            self.course_list.pop( result[0] ) # remove by index
            return True

    # ----------------------------------------------------------
    # Override
    # Creates a new assignment for a course.
    def create_assignment(self, course_id, assignment_name):
        assignment_name = self.validate_name(assignment_name)
        
        course = self.get_course_by_id(course_id) # find the course
        if (course is None):
            return None
        else:
            assignment_id = self.generate_assignment_id()
            assignment = Assignment(assignment_id, assignment_name, course) # new assignment
            self.assignment_list.append(assignment)

            course.add_assignment(assignment)  # bi-directional : and assignment to the course
            return assignment

    # Override
    # Enrolls a student in a course.
    def enroll_student(self, course_id, student_id):
        course = self.get_course_by_id(course_id) # find the course
        if (course is None):
            return None

        # Check student
        result = self.find_student_by_id( student_id )
        student = None
        if (result is None):
            student = Student(student_id) # create new student
            self.student_list.append( student ) # add to list of student
        else:
            student = result[1] # find_student_by_id returns [index, object] 

        # Prevent duplicates
        if student not in course.students:
            course.add_students(student)
        if course not in student.courses:
            student.courses.append(course)

        return student

    # Override
    # Drops a student from a course.
    def dropout_student(self, course_id, student_id):
        # find the course
        course = self.get_course_by_id(course_id) 
        if (course is None):
            return False
        
        # find the student
        result = self.find_student_by_id( student_id )
        if (result is None):
            return False
        student = result[1] # find_student_by_id returns [index, object]

        # Remove student from course
        if student in course.students:
            course.students.remove(student)

        # Remove course from student
        if course in student.courses:
            student.courses.remove(course)

        # Remove only grades related to this course and student
        self.grade_list = [
                g for g in self.grade_list 
                if not (g.course == course and g.student == student)
            ]
        
        return True


    # Override
    # Submits an assignment for a student. A grade of an assignment will be an integer between 0 and 100 inclusive.
    def submit_assignment(self, course_id, student_id, assignment_id, grade):
        # Validate grade
        if not isinstance(grade, int) or grade < 0 or grade > 100:
            raise ValueError("Grade must be an integer between 0 and 100.")

        course = self.get_course_by_id(course_id)
        if course is None:
            return None

        student_result = self.find_student_by_id(student_id)
        if student_result is None:
            return None
        student = student_result[1] # find_student_by_id returns [index, object]

        assignment_result = self.find_assignment_by_id(assignment_id)
        if assignment_result is None:
            return None
        assignment = assignment_result[1] # find_assignment_by_id returns [index, object]

        # Assignment must belong to course
        if assignment not in course.assignments:
            return None

        # Student must be enrolled in course
        if student not in course.students:
            return None

        # Check if assignment is already submit, if so, override it
        existing_index = None
        for i in range(len(self.grade_list)) :
            g = self.grade_list[i]
            if (g.course == course and g.assignment == assignment and g.student == student):
                existing_index = i
                break

        # New Grade
        grade = Grade(course, student, assignment, grade)
        # if it already exists, just update, otherwise, add a new one
        if (existing_index is None):
            self.grade_list.append( grade )
        else:
            self.grade_list[existing_index] = grade
        
        return grade

    # Override
    # Returns the average grade for an assignment. Floors the result to the nearest integer.
    def get_assignment_grade_avg(self, course_id, assignment_id):
        grades = [
            g.grade for g in self.grade_list
            if g.course.course_id == course_id and g.assignment.assignment_id == assignment_id
        ]

        if not grades:
            return 0

        return math.floor(sum(grades) / len(grades))

    # Override
    # Returns the average grade for a student in a course. Floors the result to the nearest integer.
    def get_student_grade_avg(self, course_id, student_id):
        grades = [
            g.grade for g in self.grade_list
            if g.course.course_id == course_id and g.student.student_id == student_id
        ]

        if not grades:
            return 0

        return math.floor(sum(grades) / len(grades))

    # Returns the IDs of the top 5 students in a course based on their average grades of all assignments.
    def get_top_five_students(self, course_id):
        course = self.get_course_by_id(course_id)
        if course is None:
            return []

        student_averages = [] # example: [(student1, 85), (student2, 91), (student3, 78)]

        for student in course.students:
            avg = self.get_student_grade_avg(course_id, student.student_id)
            student_averages.append((student.student_id, avg))

        # Sort by grade
        student_averages.sort(key=lambda x: x[1], reverse=True) # x[1] is the avg

        # Get top five
        top_five = []
        i = 0
        while i<5 and i<len(student_averages):
            top_five.append( student_averages[i][0] )   # to return only student_id
            # top_five.append( student_averages[i] ) -> # to return (student_id, avg),
            i += 1

        return top_five