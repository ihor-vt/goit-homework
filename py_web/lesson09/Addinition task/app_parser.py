import argparse


"""
Parser command in script.
Commands for script.
py main.py -a create -m Teacher -n 'Boris Jonson'
py main.py -a create -m Group -n 'AD-101' 
"""


def arg_parser():
    parser = argparse.ArgumentParser(description='A console utility for CRUD operations with a db.')

    parser.add_argument('-a', '--action', choices=["create", "list", "update", "remove"], type=str, required=True)
    parser.add_argument('-m', '--model', choices=["Group", "Student", "Teacher", "Discipline", "Grade"], type=str, required=True)
    parser.add_argument('-n', '--name', type=str, default=None)
    parser.add_argument('-i', '--id', type=int, default=None)
    parser.add_argument('-gi', '--group_id', type=int, default=None)
    parser.add_argument('-ti', '--teacher_id', type=int, default=None)
    parser.add_argument('-di', '--discipline_id', type=int, default=None)
    parser.add_argument('-si', '--student_id', type=int, default=None)
    parser.add_argument('-gri', '--grade_id', type=int, default=None)
    parser.add_argument('-fn', '--full_name', type=str, default=None)
    parser.add_argument('-g', '--grade', type=int, default=None)
    parser.add_argument('-d', '--date_of', type=str, default=None)

    args = parser.parse_args()  # object -> dict

    return args
