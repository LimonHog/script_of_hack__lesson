from datacenter.models import Chastisement, Lesson, Commendation, Schoolkid, Mark
import argparse
from random import choice


def remove_chastisements(schoolkid):
    Chastisement.objects.filter(schoolkid=schoolkid).delete()


def  fix_marks(schoolkid):
	Mark.objects.filter(schoolkid=schoolkid, points__lt=4).update(points = 5)


def create_commendation(schoolkid, subject, commendation):
    student_lessons = Lesson.objects.filter(year_of_study=schoolkid.year_of_study, group_letter=schoolkid.group_letter, subject__title__contains=subject)
    if not student_lessons.exists():
        print(f"Уроки по предмету '{subject}' для {schoolkid.full_name} не найдены.")
        return 

    Commendation.objects.create(teacher=student_lessons.teacher, created=student_lessons.date, subject=student_lessons.subject, text=commendation, schoolkid=schoolkid)


def get_schoolkid(full_name):
    try:  
        return Schoolkid.objects.filter(full_name__contains=full_name)
    except Schoolkid.MultipleObjectsReturned:
        print(f"Найдено несколько учеников по запросу '{full_name}'. Уточните ФИО.")
        return
    except Schoolkid.DoesNotExist:
        print(f"Ученик с ФИО, содержащим '{full_name}', не найден.")
        return
	

def main():
    parser = argparse.ArgumentParser(description='для выражения похвалы ученику, удаления его плохих оценок и замечаний')
    parser.add_argument("subject", type=str, help='Название предмета (например: Музыка)')
    parser.add_argument("name", type=str, help='Имя ученика (например: Огурцов Артём)')
    args = parser.parse_args()
    name = args.name
    subject = args.subject

    commendations = [
        'Monqueu!', 
        'Отлично!', 
        'Хорошо!', 
        'Гораздо лучше, чем я ожидал!', 
        'Ты меня приятно удивил!', 
        'Великолепно!', 
        'Прекрасно!', 
        'Ты меня очень обрадовал!', 
        'Именно этого я давно ждал от тебя!', 
        'Сказано здорово - просто и ясно!', 
        'Ты, как всегда, точен!', 
        'Очень хороший ответ!'
    ]

    client_name = get_schoolkid(name)
    fix_marks(client_name[0])
    remove_chastisements(client_name[0])
    create_commendation(client_name[0], subject, choice(commendations))


if __name__ == "__main__":
     main()