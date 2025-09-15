from django.db import migrations

def add_demo_media_lesson(apps, schema_editor):
    Lesson = apps.get_model('kids', 'Lesson')
    Course = apps.get_model('kids', 'Course')
    try:
        course = Course.objects.get(name__icontains='Colors & Shapes')
    except Course.DoesNotExist:
        return
    Lesson.objects.create(
        course=course,
        title='Learn Colors with Images and Video',
        content='This lesson teaches colors using images and a fun video.',
        image='/media/movies/635217f73e372771013edb4c-the-avengers-poster-marvel-movie-canvas1.jpg',
        video='https://www.youtube.com/embed/2Vv-BfVoq4g',
    )

class Migration(migrations.Migration):
    dependencies = [
        ('kids', '0007_lesson_image_lesson_video'),
    ]
    operations = [
        migrations.RunPython(add_demo_media_lesson),
    ]
