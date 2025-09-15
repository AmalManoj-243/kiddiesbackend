from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
        ('kids', '0009_force_demo_media_lesson'),
    ]
    operations = [
        migrations.CreateModel(
            name='QuizQuestion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(max_length=255)),
                ('option_a', models.CharField(max_length=100)),
                ('option_b', models.CharField(max_length=100)),
                ('option_c', models.CharField(max_length=100, blank=True)),
                ('option_d', models.CharField(max_length=100, blank=True)),
                ('correct_option', models.CharField(max_length=1, choices=[('A','A'),('B','B'),('C','C'),('D','D')])),
                ('lesson', models.ForeignKey('kids.Lesson', on_delete=models.CASCADE, related_name='quiz_questions')),
            ],
        ),
    ]
