-- Add my courses_taken
INSERT INTO courses_taken (term_id, course_catalog_id)
VALUES (1, 1), -- 1 CO120 2022.01.12
       (1, 2); -- 2 CS192 2022.01.12

-- Add course-specific grading rubric
INSERT INTO course_rubrics (course_taken_id, grade_category_id, percent)
VALUES (1, 1, 0),   -- 1 CO120 2022.01.12 Not Graded
       (1, 2, 11),  -- 2 CO120 2022.01.12 Final
       (1, 3, 11),  -- 3 CO120 2022.01.12 Midterm
       (1, 4, 27),  -- 4 CO120 2022.01.12 Quiz
       (1, 5, 15),  -- 5 CO120 2022.01.12 Discussion
       (1, 6, 36),  -- 6 CO120 2022.01.12 Assignment
       (2, 1, 0),   -- 7 CS192 2022.01.12 Not Graded
       (2, 2, 15),  -- 8 CS192 2022.01.12 Final
       (2, 3, 15),  -- 9 CS192 2022.01.12 Midterm
       (2, 4, 10),  -- 10 CS192 2022.01.12 Quiz
       (2, 5, 20),  -- 11 CS192 2022.01.12 Discussion
       (2, 6, 30),  -- 12 CS192 2022.01.12 Assignment
       (2, 7, 10);  -- 13 CS192 2022.01.12 Application

-- Add Weekly Topics for courses_taken.
-- CO120 (1 - 8)
INSERT INTO weeks (course_taken_id, week, topic)
VALUES (1, 1, 'What is Interpersonal Communication?'),               -- 1
       (1, 2, 'Who Am I?'),                                          -- 2
       (1, 3, 'What Do You Mean?'),                                  -- 3
       (1, 4, 'What Are Up Saying?'),                                -- 4
       (1, 5, 'Do You Really Mean That?'),                           -- 5
       (1, 6, 'What Did You Say?'),                                  -- 6
       (1, 7, "Can't We All Just Get Along?"),                       -- 7
       (1, 8, 'We Are Family'),                                      -- 8
       (2, 1, 'Introductions'),                                      -- 9
       (2, 2, 'Software Development, Data Types, and Expressions'),  -- 10
       (2, 3, 'Selection Statements'),                               -- 11
       (2, 4, 'Loops'),                                              -- 12
       (2, 5, 'List, Dictionaries, and Functions'),                  -- 13
       (2, 6, 'Design with Classes'),                                -- 14
       (2, 7, 'Simple Graphics and Image Processing'),               -- 15
       (2, 8, 'Error Handling');                                     -- 16


-- ToDos
INSERT INTO ToDos (week_id, course_rubric_id, action_id, what, is_done)
VALUES (1, 1, 1, 'Textbook: Ch 1', 1),
       (1, 1, 2, 'Lecture: A First Look at Interpersonal Communication', 1);
       (1, 7, 1, 'MindTap: Unit 1', 1),
       (1, 7, 2, 'MindTap: What is Computer Programming', 1),
       (1, 7, 1, 'Getting Started With Python', 1),
       (1, 7, 3, 'Review Unit 1', 1),
       (1, 7, 3, 'MindTap: Exercises 1.1 and 1.3', 1),
       (1, 7, 3, 'MindTap: Crossword Puzzle', 1);

INSERT INTO ToDos (week_id, course_rubric_id, action_id, what, due_date)
VALUES (1, 5, 4, 'Introduction', '2022-01-16'),
       (1, 6, 4, 'Communication Ethics', '2022-01-18'),
       (1, 4, 6, 'Quiz', '2022-01-18');
       (9, 11, 4, 'Introduction', '2022-01-16')

INSERT INTO ToDos (week_id, course_rubric_id, action_id, what, due_date, is_done, done_date, grade)
VALUES (9, 10, 6, 'MindTap: Exercise 1.4', '2022-01-18', 1, '2022-01-12', '3/3');

INSERT INTO ToDos (week_id, course_rubric_id, action_id, what, due_date, is_done, done_date)
VALUES (9, 12, 5, 'Inputs and Outputs', '2022-01-16', 1, '2022-01-12');

-- Tasks
INSERT INTO tasks (ToDo_id, task, details, is_done, done_date)
VALUES (3, 'Initial Post', '', 1, '2022-01-14'),
       (8, 'Initial Post', '', 1, '2022-01-13')
       (4, 'Set up template', '', 1, '2022-01-15');

INSERT INTO tasks (ToDo_id, task, details)
VALUES (3, 'Response Post 1', ''),
       (8, 'Response Post 1', ''),
       (8, 'Response Post 2', '');
