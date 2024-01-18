<!-- UNDERSTANDING THIS APPLICATION -->

# application name : flask_app

# application description : This is a flask application

# What is flask?

Flask is a web application framework written in Python. It is developed by Armin Ronacher, who leads an international group of Python enthusiasts named Pocco. Flask is based on the Werkzeug WSGI toolkit and Jinja2 template engine. Both are Pocco projects.

# what librarires are used in this flask application?

to see what libraries are used in this flask application, you can see the requirements.txt file in the root directory of this project.

# Purpose of this flask application?

the purpose of this flask application is to create a REST API for a school management system.

# Major features of this flask application?

1. create a new assignment
2. get all assignments
3. get assignments by id
4. submit an assignment
5. grade an assignment
6. get all assignments of a teacher
7. get all assignments of a student
8. get all assignments in various states
9. get all assignments by grade
10. get all assignments by grade and state
11. get all assignments by grade and state for a teacher
12. get all assignments by grade and state for a student
13. get all assignments by grade and state for a teacher and student

# What are the conditions for submitting an assignment?

1. assignment should exist
2. assignment state should be draft
3. assignment should be submitted by the student who is assigned the assignment
4. assignment content should not be null

# What are the condition for marking grade ?

1. assignment should exist
2. assignment state should be submitted
3. assignment grade should be not be null
4. assignment should be graded by the teacher who created the assignment

# What are the conditions for grading an assignment?

1. assignment should exist
2. assignment state should be submitted
3. assignment grade should be not be null
4. assignment should be graded by the teacher who created the assignment

there are sufficient test cases to test the above mentioned conditions.
additionally there are debug statements in the code to check the state of the assignment before and after the changes.
