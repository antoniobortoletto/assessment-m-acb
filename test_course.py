import unittest

from app.course_service_impl import CourseServiceImpl
from app.course import Course
from app.assignment import Assignment
from app.student import Student
from app.grade import Grade

# Run: python -m unittest test_course.py
class CourseServiceTest(unittest.TestCase):

    def setUp(self):
        self.service = CourseServiceImpl()

    # Validate a name (Curse_name, Assignment Name)
    def test_validate_name(self):

        # Cannot be none
        self.assertRaises(ValueError, self.service.validate_name, None )
        
        # Name should be a string type
        self.assertRaises( ValueError, self.service.validate_name, 1 )
        self.assertRaises( ValueError, self.service.validate_name, True )
        self.assertEqual( self.service.validate_name("A"), "A" ) # Valid
        
        # Ate least one character non-space
        self.assertRaises( ValueError, self.service.validate_name, " " )
        self.assertRaises( ValueError, self.service.validate_name, "         " )

        # At least one character and Cannot exceed 100
        self.assertRaises( ValueError, self.service.validate_name, "" ) # lower than 1
        self.assertRaises( ValueError, self.service.validate_name, "AssignmentAssignmentAssignmentAssignmentAssignmentAssignmentAssignmentAssignmentAssignmentAssignmentA" ) #101 characters
        self.assertEqual( self.service.validate_name("m"), "m" ) # Valid
        self.assertEqual( self.service.validate_name("AssignmentAssignmentAssignmentAssignmentAssignmentAssignmentAssignmentAssignmentAssignmentAssignment"), 
                          "AssignmentAssignmentAssignmentAssignmentAssignmentAssignmentAssignmentAssignmentAssignmentAssignment") #100 characters: Valid

        # Can contain only letters, numbers, :,./&_- and space
        self.assertRaises( ValueError, self.service.validate_name, "!" ) # invalid
        self.assertRaises( ValueError, self.service.validate_name, "#" ) # invalid
        self.assertEqual( self.service.validate_name("Abc9:,./&Z- z_") , "Abc9:,./&Z- z_") # valid

        # Remove left and right space
        self.assertEqual( self.service.validate_name("    Database    "), "Database" ) # valid
        self.assertEqual( self.service.validate_name("    object     oriented        programming    "), "object oriented programming" ) # valid

    # Create Course
    def test_create_course(self):
        
        # Create simple couse
        course_name = "Database I"
        course = self.service.create_course(course_name)
        self.assertEqual( 1           , course.course_id  ) # course id
        self.assertEqual( course_name , course.course_name  ) # course name

        # course_id should be sequential, so the next course should be 2
        course_name = "Database II"
        course = self.service.create_course(course_name)
        self.assertEqual( 2           , course.course_id  ) # course id
        self.assertEqual( course_name , course.course_name  ) # course name

        # Ensure create_course applies formatting correctly (see test_validate_name() )
        course_name = "    Database    "
        course = self.service.create_course(course_name)
        self.assertEqual(course.course_name, "Database")  # Right/Left spaces removed
        self.assertEqual(3           , course.course_id  ) # course id

        course_name = "    object     oriented        programming    "
        course = self.service.create_course(course_name)
        self.assertEqual(course.course_name, "object oriented programming") # Extra spaces removed
        self.assertEqual(4           , course.course_id  ) # course id
    
    # Get course by id and get all
    def test_create_and_get_course(self):

        # Create a new course
        course = self.service.create_course("Database I")
        self.assertIsInstance(course, Course)
        self.assertEqual(course.course_name, "Database I")
        self.assertEqual(course.course_id, 1)

        # Get this course by ID
        course_search = self.service.get_course_by_id( 1 )
        self.assertIsInstance(course, Course)
        self.assertEqual(course.course_name, "Database I")
        self.assertEqual(course.course_id, 1)

        # Try to get a course that doesn't exist
        course_search = self.service.get_course_by_id( 100 )
        self.assertIsNone(course_search)

        # Get list of courses
        courses = self.service.get_courses()
        self.assertEqual(len(courses), 1)
        self.assertEqual(courses[0].course_name, "Database I")

    # Delete course
    def test_delete_course(self):

        course1 = self.service.create_course("Database I")
        course2 = self.service.create_course("Database II")
        result = self.service.delete_course(course1.course_id) # delete Database I
        self.assertTrue(result) # returns True

        courses = self.service.get_courses()
        self.assertEqual(len(courses), 1)
        self.assertEqual(courses[0].course_name, "Database II")

        # Delete a course that doesn't exist
        result = self.service.delete_course(100)
        self.assertFalse(result) # returns True

    # create_assignment
    def test_add_assignment(self):
        course1 = self.service.create_course("Database I")
        assignment1 = self.service.create_assignment(course1.course_id, "DBS Project")

        self.assertIsInstance(assignment1, Assignment)
        self.assertEqual(assignment1.assignment_id, 1) # assignment ID is sequential
        self.assertEqual(assignment1.assignment_name, "DBS Project")

        # Ensure create_assignment applies formatting correctly (see test_validate_name() )
        assignment_name = "    DBS Final Test    "
        assignment2 = self.service.create_assignment(course1.course_id, assignment_name)
        self.assertEqual(assignment2.assignment_name, "DBS Final Test")  # Right/Left spaces removed
        self.assertEqual(2 , assignment2.assignment_id  ) # assignment id

        assignment_name = "    DBS     Workshop        10    "
        assignment3 = self.service.create_assignment(course1.course_id, assignment_name)
        self.assertEqual(assignment3.assignment_name, "DBS Workshop 10") # Extra spaces removed
        self.assertEqual(3, assignment3.assignment_id  ) # assignment id

    # Enroll and Dropout student
    def test_enroll_and_dropout_student(self):

        # Enroll
        course = self.service.create_course("Database I")
        student = self.service.enroll_student(course.course_id, "JO01")

        self.assertIsInstance(student, Student)
        self.assertIn(student, course.students)

        # Enroll invalid course ID
        result = self.service.enroll_student(100, "JO01")
        self.assertIsNone(result)

        # Enroll duplicated student
        self.service.enroll_student(course.course_id, "JO01")
        # The course should contains only student "JO01"
        self.assertIsNotNone(course.students)
        self.assertEqual( len(course.students), 1 ) # one student
        self.assertEqual( course.students[0].student_id, "JO01" )
        
        # Dropout
        self.service.dropout_student(course.course_id, "JO01")
        self.assertNotIn(student, course.students)

    # Submit Assignment
    def test_create_assignment_and_submit_grade(self):
        
        course = self.service.create_course("Database I")
        self.service.enroll_student(course.course_id, "JO01")

        assignment = self.service.create_assignment(course.course_id, "Lab 1")
        self.assertIsInstance(assignment, Assignment)
        self.assertEqual(assignment.assignment_name, "Lab 1")

        # Invalid: grade lower than zero
        with self.assertRaises(ValueError):
            self.service.submit_assignment(course.course_id, "JO01", assignment.assignment_id, -1)
        # Invalid: grade > 100
        with self.assertRaises(ValueError):
            self.service.submit_assignment(course.course_id, "JO01", assignment.assignment_id, 101)
        # Invalid: grade not integer
        with self.assertRaises(ValueError):
            self.service.submit_assignment(course.course_id, "JO01", assignment.assignment_id, 5.8)

        self.service.submit_assignment(course.course_id, "JO01", assignment.assignment_id, 9)
        grade = next((g for g in self.service.grade_list if g.student.student_id == "JO01"), None)
        self.assertIsNotNone(grade)
        self.assertEqual(grade.grade, 9)

        # Submit a new grade to same course, student and assignment (need to override the previous one)
        self.service.submit_assignment(course.course_id, "JO01", assignment.assignment_id, 8)
        grade = next((g for g in self.service.grade_list if g.student.student_id == "JO01"), None)
        self.assertIsNotNone(grade)
        self.assertEqual(grade.grade, 8)

    # average grade for an assignment
    def test_get_assignment_grade_avg(self):
        course = self.service.create_course("Database I")
        self.service.enroll_student(course.course_id, "JO01")
        self.service.enroll_student(course.course_id, "TO01")

        assignment = self.service.create_assignment(course.course_id, "Test")
        self.service.submit_assignment(course.course_id, "JO01", assignment.assignment_id, 7)
        self.service.submit_assignment(course.course_id, "TO01", assignment.assignment_id, 9)

        avg = self.service.get_assignment_grade_avg(course.course_id, assignment.assignment_id)
        self.assertEqual(avg, 8)

    # average grade for an student
    def test_get_student_grade_avg(self):

        course = self.service.create_course("Database I")
        self.service.enroll_student(course.course_id, "JO01")

        a1 = self.service.create_assignment(course.course_id, "Midterm")
        a2 = self.service.create_assignment(course.course_id, "Final")
        self.service.submit_assignment(course.course_id, "JO01", a1.assignment_id, 6)
        self.service.submit_assignment(course.course_id, "JO01", a2.assignment_id, 8)

        avg = self.service.get_student_grade_avg(course.course_id, "JO01")
        self.assertEqual(avg, 7)

    # Top 5 based on grade
    def test_get_top_five_students(self):

        course = self.service.create_course("Database I")
        # Enroll students
        self.service.enroll_student(course.course_id, "S1")
        self.service.enroll_student(course.course_id, "S2")
        self.service.enroll_student(course.course_id, "S3")
        self.service.enroll_student(course.course_id, "S4")
        self.service.enroll_student(course.course_id, "S5")
        
        # Assignment
        a1 = self.service.create_assignment(course.course_id, "Final Project")
        self.service.submit_assignment(course.course_id, "S1", a1.assignment_id, 10)
        self.service.submit_assignment(course.course_id, "S2", a1.assignment_id, 9)
        self.service.submit_assignment(course.course_id, "S3", a1.assignment_id, 8)
        self.service.submit_assignment(course.course_id, "S4", a1.assignment_id, 7)
        self.service.submit_assignment(course.course_id, "S5", a1.assignment_id, 6)

        top_five = self.service.get_top_five_students(course.course_id)
        self.assertEqual(top_five, ["S1", "S2", "S3", "S4", "S5"])  # Top 5 based on grade

    # Top 5 based on grade (less than 5 students)
    def test_get_top_five_students_less_than_5_students(self):

        course = self.service.create_course("Database I")
        # Enroll students
        self.service.enroll_student(course.course_id, "S1")
        self.service.enroll_student(course.course_id, "S2")
        self.service.enroll_student(course.course_id, "S3")
        
        # Assignment
        a1 = self.service.create_assignment(course.course_id, "Final Project")
        self.service.submit_assignment(course.course_id, "S1", a1.assignment_id, 10)
        self.service.submit_assignment(course.course_id, "S2", a1.assignment_id, 9)
        self.service.submit_assignment(course.course_id, "S3", a1.assignment_id, 8)

        top_five = self.service.get_top_five_students(course.course_id)
        self.assertEqual(top_five, ["S1", "S2", "S3"])  # Top 5 based on grade

    # Top 5 based on grade (more than 5 students)
    def test_get_top_five_students_more_than_5_students(self):

        course = self.service.create_course("Database I")
        # Enroll students
        self.service.enroll_student(course.course_id, "S1")
        self.service.enroll_student(course.course_id, "S2")
        self.service.enroll_student(course.course_id, "S3")
        self.service.enroll_student(course.course_id, "S4")
        self.service.enroll_student(course.course_id, "S5")
        self.service.enroll_student(course.course_id, "S6")
        self.service.enroll_student(course.course_id, "S7")
        
        # Assignment
        a1 = self.service.create_assignment(course.course_id, "Final Project")
        self.service.submit_assignment(course.course_id, "S1", a1.assignment_id, 10)
        self.service.submit_assignment(course.course_id, "S2", a1.assignment_id, 9)
        self.service.submit_assignment(course.course_id, "S3", a1.assignment_id, 8)
        self.service.submit_assignment(course.course_id, "S4", a1.assignment_id, 7)
        self.service.submit_assignment(course.course_id, "S5", a1.assignment_id, 6)
        self.service.submit_assignment(course.course_id, "S6", a1.assignment_id, 5)
        self.service.submit_assignment(course.course_id, "S7", a1.assignment_id, 4)

        top_five = self.service.get_top_five_students(course.course_id)
        self.assertEqual(top_five, ["S1", "S2", "S3", "S4", "S5"])  # Top 5 based on grade

    # Top 5 based on grade (many assignments)
    def test_get_top_five_students_many_assignments(self):

        course = self.service.create_course("Database I")

        # Enroll students
        self.service.enroll_student(course.course_id, "S1")
        self.service.enroll_student(course.course_id, "S2")
        self.service.enroll_student(course.course_id, "S3")
        self.service.enroll_student(course.course_id, "S4")
        self.service.enroll_student(course.course_id, "S5")
        
        # Assignment 1
        a1 = self.service.create_assignment(course.course_id, "Final Project")
        self.service.submit_assignment(course.course_id, "S1", a1.assignment_id, 10)
        self.service.submit_assignment(course.course_id, "S2", a1.assignment_id, 9)
        self.service.submit_assignment(course.course_id, "S3", a1.assignment_id, 8)
        self.service.submit_assignment(course.course_id, "S4", a1.assignment_id, 7)
        self.service.submit_assignment(course.course_id, "S5", a1.assignment_id, 6)

        # Assignment 2
        a2 = self.service.create_assignment(course.course_id, "Workshop")
        self.service.submit_assignment(course.course_id, "S1", a2.assignment_id, 9)
        self.service.submit_assignment(course.course_id, "S2", a2.assignment_id, 8)
        self.service.submit_assignment(course.course_id, "S3", a2.assignment_id, 7)
        self.service.submit_assignment(course.course_id, "S4", a2.assignment_id, 6)
        self.service.submit_assignment(course.course_id, "S5", a2.assignment_id, 5)

        top_five = self.service.get_top_five_students(course.course_id)
        self.assertEqual(top_five, ["S1", "S2", "S3", "S4", "S5"])  # Top 5 based on grade
