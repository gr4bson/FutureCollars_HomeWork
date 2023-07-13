"""
Program do obsługi bazy szkolnej

Utwórz program do zarządzania bazą szkolną. Istnieje możliwość tworzenia trzech typów użytkowników (uczeń,
nauczyciel, wychowawca) a także zarządzania nimi.

Po uruchomieniu programu można wpisać jedną z następujących komend: utwórz, zarządzaj, koniec.

    Polecenie "utwórz" - Przechodzi do procesu tworzenia użytkowników.
    Polecenie "zarządzaj" - Przechodzi do procesu zarządzania użytkownikami.
    Polecenie "koniec" - Kończy działanie aplikacji.


Proces tworzenia użytkowników:

    Należy wpisać opcję, którą chcemy wybrać: uczeń, nauczyciel, wychowawca, koniec. Po wykonaniu każdej z opcji (oprócz
        "koniec") wyświetla to menu ponownie.
    Polecenie "uczeń" - Należy pobrać imię i nazwisko ucznia (jako jedna zmienna, można pobrać je jako dwie zmienne,
        jeżeli zostanie to poprawnie obsłużone) oraz nazwę klasy (np. "3C")
    Polecenie "nauczyciel" - Należy pobrać imię i nazwisko nauczyciela (jako jedna zmienna, labo dwie, jeżeli zostanie
        to poprawnie obsłużone), nazwę przedmiotu prowadzonego, a następnie w nowych liniach nazwy klas, które prowadzi
        nauczyciel, aż do otrzymania pustej linii.
    Polecenie "wychowawca" - Należy pobrać imię i nazwisko wychowawcy (jako jedna zmienna, albo dwie, jeżeli zostanie
        to poprawnie obsłużone), a także nazwę prowadzonej klasy.
    Polecenie "koniec" - Wraca do pierwszego menu.


Proces zarządzania użytkownikami:

    Należy wpisać opcję, którą chcemy wybrać: klasa, uczen, nauczyciel, wychowawca, koniec. Po wykonaniu każdej z opcji
        (oprócz "koniec") wyświetla to menu ponownie.
    Polecenie "klasa" - Należy pobrać klasę, którą chcemy wyświetlić (np. "3C") program ma wypisać wszystkich uczniów,
        którzy należą do tej klasy, a także wychowawcę tejże klasy.
    Polecenie "uczeń" - Należy pobrać imię i nazwisko uczenia, program ma wypisać wszystkie lekcje, które ma uczeń
        a także nauczycieli, którzy je prowadzą.
    Polecenie "nauczyciel" - Należy pobrać imię i nazwisko nauczyciela, program ma wypisać wszystkie klasy,
        które prowadzi nauczyciel.
    Polecenie "wychowawca" - Należy pobrać imię i nazwisko nauczyciela, a program ma wypisać wszystkich uczniów,
        których prowadzi wychowawca.
    Polecenie "koniec" - Wraca do pierwszego menu.
"""
import dataclasses

class Person:
    def __init__(self):
        self.name = None
        self.surname = None

    def change_name(self, name):
        self.name = name

class Student(Person):
    def __init__(self):
        super().__init__()
        self.group = None

    def fill_data(self):
        self.name = input(f'Podaj imię nowego ucznia: ')
        self.surname = input(f'Podaj nazwisko nowego ucznia: ')
        self.group = input(f'Podaj klasę nowego ucznia: ')

class Teacher(Person):
    def __init__(self):
        super().__init__()
        self.course_taught = None
        self.groups_taught = []  # Jak przypisać listę do parametru klasy?

    def fill_data(self):
        self.name = input(f'Podaj imię nowego nauczyciela: ')
        self.surname = input(f'Podaj nazwisko nowego nauczyciela: ')
        self.course_taught = input(f'Podaj przedmiot, którego uczy: ')
        print('Podaj nazwy klas, w których uczy, zatwierdź każdą wciskając Enter:')
        group_name = input()
        while group_name:
            self.groups_taught.append(group_name)
            group_name = input()

class ClassTeacher(Person):
    def __init__(self):
        super().__init__()
        self.main_group = None

    def fill_data(self):
        self.name = input(f'Podaj imię nowego nauczyciela: ')
        self.surname = input(f'Podaj nazwisko nowego nauczyciela: ')
        self.main_group = input(f'Podaj klasę, której jest wychowawcą: ')

@dataclasses.dataclass
class School:
    students: list[Student]
    teachers: list[Teacher]
    class_teachers: list[ClassTeacher]

class SchoolHandler:
    def __init__(self):
        self.school = School(students=[], teachers=[], class_teachers=[])

    def add_student(self, student: Student):
        self.school.students.append(student)

    def add_teacher(self, teacher: Teacher):
        self.school.teachers.append(teacher)

    def add_class_teacher(self, class_teacher: ClassTeacher):
        self.school.class_teachers.append(class_teacher)

    def get_input_name(self):
        name_saught = input("Podaj imię: ")
        surname_saught = input("Podaj nazwisko: ")
        return name_saught, surname_saught

    def find_students_by_group(self, group):
        students_inside_group = []
        for student in self.school.students:
            if student.group == group:
                students_inside_group.append(student)
        return students_inside_group

    def find_class_teacher_by_group(self, group):
        for class_teacher in self.school.class_teachers:
            if class_teacher.main_group == group:
                return class_teacher.name, class_teacher.surname

    def find_student(self, name_to_check, surname_to_check):
        for student in self.school.students:
            if student.name == name_to_check:
                if student.surname == surname_to_check:
                    return student.group

    def find_lessons_and_teachers_of_student(self, name_to_check, surname_to_check):
        courses_taken = {}
        for student in self.school.students:
            if student.name == name_to_check:
                if student.surname == surname_to_check:
                    for teacher in self.school.teachers:
                        if student.group in teacher.groups_taught:
                            courses_taken[f'{teacher.name}, {teacher.surname}'] = teacher.course_taught
        return courses_taken

    def find_groups_taught_by_teacher(self, teacher_name, teacher_surname):
        for teacher in self.school.teachers:
            if teacher.name == teacher_name:
                if teacher.surname == teacher_surname:
                    return teacher.groups_taught

    def find_students_by_class_teacher(self, class_teacher_name, class_teacher_surname):
        student_list = []
        for class_teacher in self.school.class_teachers:
            if class_teacher.name == class_teacher_name:
                if class_teacher.surname == class_teacher_surname:
                    for student in self.school.students:
                        if student.group == class_teacher.main_group:
                            student_list.append(f'{student.name} {student.surname}')
        return student_list

available_prompts = {
    1: 'Utwórz / Create',
    2: 'Zarządzaj / Manage',
    3: 'Koniec / End'
}

further_1_prompts = {
    1: 'Uczeń / Student',
    2: 'Nauczyciel / Teacher',
    3: 'Wychowawca / Class Teacher',
    4: 'Koniec / End'
}

further_2_prompts = {
    1: 'Klasa / Class',
    2: 'Uczeń / Student',
    3: 'Nauczyciel / Teacher',
    4: 'Wychowawca / Class Teacher',
    5: 'Koniec / End'
}

def print_availabale_prompts(source_dictionary):
    choice = None
    while not choice:
        print('Wybierz numer operacji spośród następujących dostępnych:')
        for keys, prompts in source_dictionary.items():
            print(f'{keys}: {prompts}')
        try:
            choice = int(input("Wybierz operację z powyższych: "))
        except ValueError:
            print('Nie podałeś liczby. Spróbuj jeszcze raz.')
            continue
        if choice not in source_dictionary.keys():
            print(f'Operacja "{choice}" jest niedostępna. Spróbuj jeszcze raz. ')
            choice = None
            continue
        return choice

prompt = None
school = SchoolHandler()
while prompt != 3:
    prompt = print_availabale_prompts(available_prompts)
    if prompt == 1:
        sub_prompt = None
        while sub_prompt != 4:
            sub_prompt = print_availabale_prompts(further_1_prompts)
            if sub_prompt == 1:
                student = Student()
                student.fill_data()
                school.add_student(student)
            if sub_prompt == 2:
                teacher = Teacher()
                teacher.fill_data()
                school.add_teacher(teacher)
            if sub_prompt == 3:
                class_teacher = ClassTeacher()
                class_teacher.fill_data()
                school.add_class_teacher(class_teacher)
    if prompt == 2:
        sub_prompt = None
        while sub_prompt != 5:
            sub_prompt = print_availabale_prompts(further_2_prompts)
            if sub_prompt == 1:
                group = input('Podaj nazwę klasy: ')
                students_found = school.find_students_by_group(group)
                print(f'Lista studentów klasy {group}:')
                for student in students_found:
                    print(f'{student.name} {student.surname}')
                print(f'Wychowawca: {school.find_class_teacher_by_group(group)}')
            if sub_prompt == 2:
                print("Podaj dane ucznia.")
                student_name, student_surname = school.get_input_name()
                courses = school.find_lessons_and_teachers_of_student(student_name, student_surname)
                for keys, values in courses.items():
                    print (f'{keys}: {values}')
            if sub_prompt == 3:
                print("Podaj dane nauczyciela:")
                teacher_name, teacher_surname = school.get_input_name()
                groups_found = school.find_groups_taught_by_teacher(teacher_name, teacher_surname)
                print(f'Klasy, w których naucza {teacher_name} {teacher_surname}:')
                for groups in groups_found:
                    print(groups)
            if sub_prompt == 4:
                print('Podaj dane wychowawcy:')
                class_teacher_name, class_teacher_surname = school.get_input_name()
                student_list = school.find_students_by_class_teacher(class_teacher_name, class_teacher_surname)
                print(f'Lista uczniów wychowawcy {class_teacher_name} {class_teacher_surname}:')
                for student in student_list:
                    print(student)
