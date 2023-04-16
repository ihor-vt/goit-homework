/* 5 студентів із найбільшим середнім балом з усіх предметів. */
SELECT name, AVG(mark) as avg_mark
FROM students, marks
where students.id = marks.student_id
GROUP BY name
ORDER BY  avg_mark DESC
LIMIT 5;

/* 1 студент із найвищим середнім балом з одного предмета. */
SELECT students.name, AVG(mark) as avg_mark, subjects.name
FROM marks, students,subjects
where marks.subject_id = subjects.id and students.id = marks.student_id and subjects.name = "Python"
GROUP BY students.name
ORDER BY avg_mark DESC
LIMIT 1;

/* середній бал в групі по одному предмету. */
SELECT groups.group_name as N_group, ROUND(AVG(mark), 2) as avg_mark, subjects.name as subject
FROM marks, groups, students, subjects
WHERE marks.subject_id = subjects.id and students.group_id = groups.id and subjects.name = "Python"
and groups.group_name = "A" and students.id = marks.student_id;

/* Середній бал у потоці. */
SELECT round(AVG(mark),2)
FROM marks;

/* Які курси читає викладач. */
SELECT teachers.name, subjects.name
FROM teachers, subjects
WHERE teachers.id = subjects.teacher_id and teachers.name = 'Matthew Obrien';

/* Список студентів у групі. */
SELECT students.name
FROM groups, students
WHERE students.group_id = groups.id and groups.group_name = 'B'
ORDER BY students.name;

/* Оцінки студентів у групі з предмета. */
SELECT students.name, marks.mark
FROM groups, students, subjects, marks
WHERE students.group_id = groups.id and groups.group_name = 'B' and subjects.name = 'Python' and marks.student_id = students.id
ORDER BY students.name;

/* Оцінки студентів у групі з предмета на останньому занятті. */
SELECT students.name, marks.mark
FROM groups, students, subjects, marks
WHERE students.group_id = groups.id and groups.group_name = 'A' and subjects.name = 'Python' and marks.student_id = students.id
and created_at = (SELECT max(created_at) FROM marks)
GROUP BY students.name;

/* Список курсів, які відвідує студент. */
SELECT subjects.name
FROM subjects, students, marks
WHERE students.id = marks.student_id and subjects.id = marks.subject_id  and students.name = 'Robert Lopez'
GROUP BY subjects.name;

/* Список курсів, які студенту читає викладач. */
SELECT subjects.name
FROM subjects, students, marks, teachers
WHERE students.id = marks.student_id and subjects.id = marks.subject_id  and students.name = 'Robert Lopez'
and teachers.name = 'Sydney Bryant' and subjects.teacher_id = teachers.id
GROUP BY subjects.name;

/* Середній бал, який викладач ставить студенту */
SELECT AVG(marks.mark)
FROM groups, students, subjects, marks, teachers
WHERE students.id = marks.student_id and subjects.id = marks.subject_id  and students.name = 'Robert Lopez'
and teachers.name = 'Sydney Bryant' and subjects.teacher_id = teachers.id;

/* Середній бал, який ставить викладач. */
SELECT teachers.name as Techers_name, ROUND(AVG(marks.mark), 2) as avg_mark
FROM groups, students, subjects, marks, teachers
WHERE subjects.id = marks.subject_id  and subjects.teacher_id = teachers.id
GROUP BY teachers.name;
