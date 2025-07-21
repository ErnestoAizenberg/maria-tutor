from .models import Teacher

def teacher_context(request):
    teacher = Teacher.objects.filter(is_active=True).first()
    return {
        'teacher': teacher,
    }
