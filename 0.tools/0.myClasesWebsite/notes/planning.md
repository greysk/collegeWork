# My Classes

- [ ] Adjust app.py to use sqlite3 queries rather than views. (Views removed from database schema but not yet from database)
- [ ] Adjust `get_todo_status()` to be part of `get_syllabus()` and a query to get numbers for every ToDo for a course.
- [ ] Rebuild database
  - [ ] Add in courses and subjects first (aka stop trying to make for others)

## My Classes/Home

Course Overview

- [ ] Input: Form: Add Class
  - [ ] Catalog ID -> `courses.catalog_id`
  - [ ] Subject -> `subjects.subject`
    - [ ] remove and use lookup to subjects instead based on catalog id
    - [ ] add course prefix to catalog id
  - [ ] Title -> `courses.title`
  - [ ] Year -> `terms.year`
  - [ ] Month -> `terms.month`
  - [ ] Day -> `terms.day`
- [ ] Output: Table: All classes taken/registered.
  - [ ] Catalog ID <- `courses.catalog_id`
  - [ ] Subject <- `subjects.subject`
  - [ ] Title <- `courses.title`
  - [ ] Start Date <- `terms.start_date`

## Rubrics

That apply to all classes.

- [ ] Discussion Post Rubric 100-200 (image)

## Syllabus

Todos listed on syllabus. Generated by link for each class.

- [ ] ? Input: Form: Add ToDo
- [ ] Output: Table: All ToDos for Class - Ordered by week
  - [ ] Week <- `todos.week`
  - [ ] Status <- calculated by done_tasks/total_tasks
    - [ ] Create using svg?
  - [ ] Action <- `actions.action`
  - [ ] What <- `todos.what`
  - [ ] Grade Category <- `grade_category.category`
  - [ ] Due Date* <- `todos.due_date`
  - [ ] Grade* <- `todos.grade`

## Tasks (every step for each ToDo)

? Own page or expandable under incomplete ToDo?

- [ ] ? Input: Form: Add Task
- [ ] Output: Table: All Tasks for a To-Do (Ordered by `task_id`)
  - [ ] Week <- `todos.week`
  - [ ] Status <- `tasks.is_done`
  - [ ] Action <- `todos.action_id` -> `action.actions`
  - [ ] What <- `todos.what`
  - [ ] Task <- `tasks.task`
  - [ ] Details (expando) <- `tasks.details`
  - [ ] Grade Category <- `todos.grade_category_id` -> `grade_category.category`
  - [ ] Due Date <- `todos.due_date`

## Notes (For each class)

Links to notes which are files/stored in table as [markdown](https://www.digitalocean.com/community/tutorials/how-to-use-python-markdown-with-flask-and-sqlite.amp) and pulled in as a website (in a frame or own page)

- [ ] ? Form field to type in/use to submit markdown note
