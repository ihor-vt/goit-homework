from app_parser import arg_parser
from src.models import Discipline, Group, Grade, Student, Teacher
from src.db import session


def main():

    models_create = {
        "Group": create_group,
        "Teacher": create_teacher,
        "Student": create_student,
        "Discipline": create_discipline,
        "Grade": create_grade
    }

    models_update = {
        "Group": update_group,
        "Teacher": update_teacher,
        "Student": update_student,
        "Discipline": update_discipline,
        "Grade": update_grade
    }

    models_remove = {
        "Group": remove_group,
        "Teacher": remove_teacher,
        "Student": remove_student,
        "Discipline": remove_discipline,
        "Grade": remove_grade
    }

    models_show = {
        "Group": show_group,
        "Teacher": show_teacher,
        "Student": show_student,
        "Discipline": show_discipline,
        "Grade": show_grade
    }

    arg = arg_parser()

    if arg.action in "create":
        if arg.model in models_create.keys():
            result = models_create.get(arg.model)(arg)
            return result

    elif arg.action in "update":
        if arg.model in models_update.keys():
            result = models_update.get(arg.model)(arg)
            return result

    elif arg.action in "remove":
        if arg.model in models_remove.keys():
            result = models_remove.get(arg.model)(arg)
            return result

    elif arg.action in "list":
        if arg.model in models_show.keys():
            result = models_show.get(arg.model)()
            return result


def create_group(args):
    result = Group(name=args.name)
    session.add(result)
    session.commit()
    return f"Group {args.name} added."


def create_teacher(args):
    result = Teacher(fullname=args.name)
    session.add(result)
    session.commit()
    return f"Teacher {args.name} added."


def create_student(args):
    result = Student(fullname=args.name, group_id=args.group_id)
    session.add(result)
    session.commit()
    return f"Student {args.name} , group_id {args.group_id} added."


def create_discipline(args):
    result = Discipline(name=args.name, teacher_id=args.teacher_id)
    session.add(result)
    session.commit()
    return f"Discipline {args.name}, teacher_id {args.teacher_id} added."


def create_grade(args):
    result = Grade(grade=args.grade, date_of=args.date_of, student_id=args.student_id, discipline_id=args.discipline_id)
    session.add(result)
    session.commit()
    return f"Grade {args.grade}, date_of {args.date_of}, date_of {args.student_id}, date_of {args.discipline_id}, added."


def update_group(args):
    try:
        group = session.query(Group).get(args.group_id)
        group.name = args.name
    except Exception as er:
        return f"Failed: {er}"

    session.add(group)
    session.commit()

    return f"Group {args.group_id}, update {args.name}."


def update_teacher(args):
    try:
        teacher = session.query(Teacher).get(args.teacher_id)
        teacher.name = args.fullname
    except Exception as er:
        return f"Failed: {er}"

    session.add(teacher)
    session.commit()

    return f"Teacher {args.teacher_id}, update {args.fullname}."


def update_student(args):
    try:
        student = session.query(Student).get(args.student_id)
        student.name = args.fullname
    except Exception as er:
        return f"Failed: {er}"

    session.add(student)
    session.commit()

    return f"Student {args.student_id}, update {args.fullname}."


def update_discipline(args):
    try:
        discipline = session.query(Discipline).get(args.discipline_id)
        discipline.name = args.name
    except Exception as er:
        return f"Failed: {er}"

    session.add(discipline)
    session.commit()

    return f"Discipline {args.discipline_id}, update {args.name}."


def update_grade(args):
    try:
        grade = session.query(Grade).get(args.grade_id)
        grade.grade = args.grade
        grade.date_of = args.date_of
    except Exception as er:
        return f"Failed: {er}"

    session.add(grade)
    session.commit()

    return f"Grade {args.grade_id}, update {args.grade} and date_of {args.date_of}."


def remove_group(args):
    try:
        group = session.query(Group).get(args.group_id)
    except Exception as er:
        return f"Failed: {er}"

    session.delete(group)
    session.commit()

    return f"Group {args.group_id} remove."


def remove_teacher(args):
    try:
        teacher = session.query(Teacher).get(args.teacher_id)
    except Exception as er:
        return f"Failed: {er}"

    session.delete(teacher)
    session.commit()

    return f"Teacher {args.teacher_id} remove."


def remove_student(args):
    try:
        student = session.query(Student).get(args.student_id)
    except Exception as er:
        return f"Failed: {er}"

    session.delete(student)
    session.commit()

    return f"Student {args.student_id} remove."


def remove_discipline(args):
    try:
        discipline = session.query(Discipline).get(args.discipline_id)
    except Exception as er:
        return f"Failed: {er}"

    session.delete(discipline)
    session.commit()

    return f"Discipline {args.discipline_id} remove."


def remove_grade(args):
    try:
        grade = session.query(Grade).get(args.grade_id)
    except Exception as er:
        return f"Failed: {er}"

    session.delete(grade)
    session.commit()

    return f"Grade {args.grade_id} remove."


def show_group():
    groups = session.query(Group).all()
    result = [x.name for x in groups]
    return result


def show_teacher():
    teachers = session.query(Teacher).all()
    result = [x.fullname for x in teachers]
    return result


def show_student():
    students = session.query(Student).all()
    result = [x.fullname for x in students]
    return result


def show_discipline():
    disciplines = session.query(Discipline).all()
    result = [x.name for x in disciplines]
    return result


def show_grade():
    grades = session.query(Grade).all()
    result = [x.grade for x in grades]
    return result


if __name__ == "__main__":
    print(main())
