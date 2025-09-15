from django.db import migrations

def add_colors_and_shapes_lesson(apps, schema_editor):
    Course = apps.get_model('kids', 'Course')
    Lesson = apps.get_model('kids', 'Lesson')
    try:
        course = Course.objects.get(name__icontains='colors')
        Lesson.objects.create(
            course=course,
            title='Primary Colors',
            content='Learn about the three primary colors: red, blue, and yellow.\nActivity:\n- Find objects that are red, blue, or yellow.\n- Draw each color on paper.\n- Mix two colors and see what new color you get.',
            order=1
        )
    except Course.DoesNotExist:
        pass

class Migration(migrations.Migration):
    dependencies = [
        ('kids', '0003_initial_data'),
    ]

    operations = [
        migrations.RunPython(add_colors_and_shapes_lesson),
    ]
