from django.db import migrations

def add_initial_data(apps, schema_editor):
    AgeGroup = apps.get_model('kids', 'AgeGroup')
    Subject = apps.get_model('kids', 'Subject')
    Course = apps.get_model('kids', 'Course')

    # Age Groups
    ag1 = AgeGroup.objects.create(name='Ages 3-6', min_age=3, max_age=6)
    ag2 = AgeGroup.objects.create(name='Ages 7-10', min_age=7, max_age=10)
    ag3 = AgeGroup.objects.create(name='Ages 11-14', min_age=11, max_age=14)

    # Subjects
    s_math = Subject.objects.create(name='Mathematics')
    s_science = Subject.objects.create(name='Science')
    s_english = Subject.objects.create(name='English')
    s_coding = Subject.objects.create(name='Coding')
    s_art = Subject.objects.create(name='Art & Craft')

    # Courses for Ages 3-6
    Course.objects.create(name='Alphabet & Phonics', description='Learn the alphabet and phonics.', age_group=ag1, subject=s_english, level='Beginner', language='English')
    Course.objects.create(name='Numbers & Counting', description='Learn numbers and counting.', age_group=ag1, subject=s_math, level='Beginner', language='English')
    Course.objects.create(name='Colors & Shapes', description='Learn colors and shapes.', age_group=ag1, subject=s_art, level='Beginner', language='English')

    # Courses for Ages 7-10
    Course.objects.create(name='Mathematics Basics', description='Addition, subtraction, multiplication, division.', age_group=ag2, subject=s_math, level='Basic', language='English')
    Course.objects.create(name='Science Explorers', description='Nature, animals, simple physics.', age_group=ag2, subject=s_science, level='Basic', language='English')
    Course.objects.create(name='Coding for Kids', description='Learn coding with Scratch and Blockly.', age_group=ag2, subject=s_coding, level='Basic', language='English')

    # Courses for Ages 11-14
    Course.objects.create(name='Advanced Math', description='Fractions, decimals, geometry.', age_group=ag3, subject=s_math, level='Intermediate', language='English')
    Course.objects.create(name='Science Lab', description='Biology, chemistry, physics.', age_group=ag3, subject=s_science, level='Intermediate', language='English')
    Course.objects.create(name='Python Programming', description='Learn Python programming.', age_group=ag3, subject=s_coding, level='Intermediate', language='English')

class Migration(migrations.Migration):
    dependencies = [
        ('kids', '0002_agegroup_subject_course_lesson'),
    ]

    operations = [
        migrations.RunPython(add_initial_data),
    ]
