from app.course_service_impl import CourseServiceImpl

if __name__ == "__main__":
    course_service = CourseServiceImpl()

    # Start receiving requests...

    # New courses
    print("> create_course")
    database_course = course_service.create_course("Database I")
    database_course = course_service.create_course("Database II - Advanced")
    dsa_course      = course_service.create_course("Data Structure Algorithm")
    comm_course     = course_service.create_course("Business Communication")

    # List courses
    print("> get_courses")
    course_list = course_service.get_courses()
    for course in course_list:
        print("   ",course.course_id , ",", course.course_name)
    '''
    > get_courses
        2 , Database II - Advanced
        3 , Data Structure Algorithm
        4 , Business Communication
    '''

    # Get course by ID
    print("> get_course_by_id")
    # Couses ID for testing
    COURSE_ID_DBS_I = 1   # Database I
    COURSE_ID_DBS_II = 2  # Database II - Advanced
    COURSE_ID_DSA = 3     # Data Structure Algorithm
    COURSE_ID_COMM = 4    # Business Communication
    course = course_service.get_course_by_id( COURSE_ID_DSA ) # should return "Data Structure Algorithm"
    print("   ",course.course_id , ",", course.course_name)
    '''
    > get_course_by_id
        3 , Data Structure Algorithm
    '''

    # Delete course
    print("> delete_course")
    course_service.delete_course( COURSE_ID_DBS_II ) # remove "Database II - Advanced"
    course_service.delete_course( COURSE_ID_COMM )   # remove "Business Communication"
    # List after deletion
    course_list = course_service.get_courses()
    for course in course_list:
        print("   ", course.course_id , ",", course.course_name)
    '''
    > delete_course
        1 , Database I
        3 , Data Structure Algorithm
    '''

    # Add assignment
    print("> create_assignment")
    assignment = course_service.create_assignment(COURSE_ID_DSA, "Assignment 1 - Tables")
    # List after creation
    print("   ",assignment.assignment_id , ",", assignment.assignment_name, ",", assignment.course.course_name)
    '''
    > create_assignment
        1 , Assignment 1 - Tables , Data Structure Algorithm
    '''

    # Enroll_student
    print("> Enroll_student")
    STUDENT_ID_JOHN  = "JO01"
    STUDENT_ID_MIKE  = "MI01"
    STUDENT_ID_SARAH = "SA01"
    STUDENT_ID_SMITH = "SM01"
    STUDENT_ID_BEN   = "BEN01"
    STUDENT_ID_ARTUR = "AR01"
    STUDENT_ID_TONI  = "TO01"

    # Add students to Database couse:
    student = course_service.enroll_student( COURSE_ID_DBS_I, STUDENT_ID_JOHN ) 
    student = course_service.enroll_student( COURSE_ID_DBS_I, STUDENT_ID_MIKE ) 
    student = course_service.enroll_student( COURSE_ID_DBS_I, STUDENT_ID_SARAH ) 
    student = course_service.enroll_student( COURSE_ID_DBS_I, STUDENT_ID_SMITH ) 
    student = course_service.enroll_student( COURSE_ID_DBS_I, STUDENT_ID_BEN ) 
    student = course_service.enroll_student( COURSE_ID_DBS_I, STUDENT_ID_ARTUR ) 
    student = course_service.enroll_student( COURSE_ID_DBS_I, STUDENT_ID_TONI )
    # Add students to DSA couse:
    student = course_service.enroll_student( COURSE_ID_DSA, STUDENT_ID_JOHN )
    student = course_service.enroll_student( COURSE_ID_DSA, STUDENT_ID_TONI ) 
    # List courses and students
    course_list = course_service.get_courses()
    for c in course_list:
        print("   ", c.course_name, ":", end="" )
        for s in c.students:
            print(s.student_id, "," , end="")
        print()
    '''
    > Enroll_student
        Database I :JO01 ,MI01 ,SA01 ,SM01 ,BEN01 ,AR01 ,TO01 ,
        Data Structure Algorithm :JO01 ,TO01 ,
    '''

    # dropout_student
    print("> dropout_student")
    # Drop Sarah and Arthur from DBS
    course_service.dropout_student( COURSE_ID_DBS_I, STUDENT_ID_SARAH )
    course_service.dropout_student( COURSE_ID_DBS_I, STUDENT_ID_ARTUR )
    # List courses and students
    course_list = course_service.get_courses()
    for c in course_list:
        print("   ", c.course_name, ":", end="" )
        for s in c.students:
            print(s.student_id, "," , end="")
        print()
    '''
    > dropout_student
        Database I :JO01 ,MI01 ,SM01 ,BEN01 ,TO01 ,
        Data Structure Algorithm :JO01 ,TO01 ,
    '''

    # submit_assignment
    print("> submit_assignment")
    # Create new assignment for DBS
    assignment_dbsproject = course_service.create_assignment(COURSE_ID_DBS_I, "DBS Project")
    ASSIGNMENT_DBS_PROJECT_ID = assignment_dbsproject.assignment_id
    # Submit grade
    course_service.submit_assignment(COURSE_ID_DBS_I, STUDENT_ID_JOHN, ASSIGNMENT_DBS_PROJECT_ID, 8)
    course_service.submit_assignment(COURSE_ID_DBS_I, STUDENT_ID_MIKE, ASSIGNMENT_DBS_PROJECT_ID, 7)
    course_service.submit_assignment(COURSE_ID_DBS_I, STUDENT_ID_SMITH, ASSIGNMENT_DBS_PROJECT_ID, 7)
    course_service.submit_assignment(COURSE_ID_DBS_I, STUDENT_ID_BEN, ASSIGNMENT_DBS_PROJECT_ID, 5)
    course_service.submit_assignment(COURSE_ID_DBS_I, STUDENT_ID_TONI, ASSIGNMENT_DBS_PROJECT_ID, 6)
    course_service.submit_assignment(COURSE_ID_DBS_I, STUDENT_ID_TONI, ASSIGNMENT_DBS_PROJECT_ID, 10) # overhide Toni grade

    # Create new assignment for DBS
    assignment_dbsfinaltest = course_service.create_assignment(COURSE_ID_DBS_I, "DBS Final Test")
    ASSIGNMENT_DBS_FINALTEST_ID = assignment_dbsfinaltest.assignment_id
    # Submit grade
    course_service.submit_assignment(COURSE_ID_DBS_I, STUDENT_ID_JOHN, ASSIGNMENT_DBS_FINALTEST_ID, 8)
    course_service.submit_assignment(COURSE_ID_DBS_I, STUDENT_ID_MIKE, ASSIGNMENT_DBS_FINALTEST_ID, 9)
    course_service.submit_assignment(COURSE_ID_DBS_I, STUDENT_ID_SMITH, ASSIGNMENT_DBS_FINALTEST_ID, 6)
    course_service.submit_assignment(COURSE_ID_DBS_I, STUDENT_ID_BEN, ASSIGNMENT_DBS_FINALTEST_ID, 5)
    course_service.submit_assignment(COURSE_ID_DBS_I, STUDENT_ID_TONI, ASSIGNMENT_DBS_FINALTEST_ID, 10)

    # Create new assignment for DSA
    assignment_dsaworkshop = course_service.create_assignment(COURSE_ID_DSA, "DSA Workshop")
    ASSIGNMENT_DSA_WORKSHOP_ID = assignment_dsaworkshop.assignment_id
    # Submit grade
    course_service.submit_assignment(COURSE_ID_DSA, STUDENT_ID_JOHN, ASSIGNMENT_DSA_WORKSHOP_ID, 8)
    course_service.submit_assignment(COURSE_ID_DSA, STUDENT_ID_TONI, ASSIGNMENT_DSA_WORKSHOP_ID, 10) 

    # List: 
    grade_list = course_service.grade_list
    for g in grade_list:
        print("   ", g.course.course_name, ",", 
                    g.assignment.assignment_name, ",", 
                    g.student.student_id, ",", g.grade)
    '''
    > submit_assignment
        Database I , DBS Project , JO01 , 8
        Database I , DBS Project , MI01 , 7
        Database I , DBS Project , SM01 , 7
        Database I , DBS Project , BEN01 , 5
        Database I , DBS Project , TO01 , 10
        Database I , DBS Final Test , JO01 , 8
        Database I , DBS Final Test , MI01 , 9
        Database I , DBS Final Test , SM01 , 6
        Database I , DBS Final Test , BEN01 , 5
        Database I , DBS Final Test , TO01 , 10
        Data Structure Algorithm , DSA Workshop , JO01 , 8
        Data Structure Algorithm , DSA Workshop , TO01 , 10
    '''

    # get_assignment_grade_avg
    print("> get_assignment_grade_avg")
    avg = course_service.get_assignment_grade_avg( COURSE_ID_DBS_I, ASSIGNMENT_DBS_PROJECT_ID )
    print("   ", avg)
    '''
    > get_assignment_grade_avg
        7
    '''

    # get_student_grade_avg
    print("> get_student_grade_avg")
    avg = course_service.get_student_grade_avg( COURSE_ID_DBS_I, STUDENT_ID_JOHN )
    print("   ", avg)
    '''
    > get_assignment_grade_avg
        8
    '''

    # get_top_five_students
    print("> get_top_five_students")
    top_five = course_service.get_top_five_students( COURSE_ID_DBS_I )
    if (top_five is not None):
        for s in top_five:
            print("   ", s)
    '''
    > get_top_five_students
        TO01
        JO01
        MI01
        SM01
        BEN01
    '''