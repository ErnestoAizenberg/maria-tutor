from .models import Teacher

def teacher_context(request):
    teacher = Teacher.objects.first()
    return {
        'teacher': teacher,
    }
