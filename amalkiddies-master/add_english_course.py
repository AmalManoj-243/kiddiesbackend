 # ...removed languageleague import...

# Create English Language
english, _ = Language.objects.get_or_create(name="English")

# Create Beginner English Course
course, _ = Course.objects.get_or_create(
    name="Beginner English",
    language=english,
    level="Beginner",
    description="A foundational course for new English learners."
)

# Units and Lessons structure
units_data = [
    {
        "title": "Grammar Basics",
        "lessons": [
            {"title": "Simple Present Tense", "content": "Learn how to use the simple present tense in English."},
            {"title": "Simple Past Tense", "content": "Learn how to use the simple past tense in English."},
            {"title": "Present Continuous", "content": "Learn how to use the present continuous tense in English."},
            {"title": "Articles (a, an, the)", "content": "Learn how to use articles in English."},
            {"title": "Modal Verbs (can, must, should)", "content": "Learn how to use modal verbs in English."},
        ]
    },
    {
        "title": "Vocabulary",
        "lessons": [
            {"title": "Greetings & Introductions", "content": "Common greetings and ways to introduce yourself."},
            {"title": "Numbers & Days of the Week", "content": "Learn numbers and days of the week."},
            {"title": "Food & Restaurants", "content": "Vocabulary for food and dining out."},
            {"title": "Family & People", "content": "Words for family members and people."},
            {"title": "Common Adjectives", "content": "Useful adjectives for describing things."},
        ]
    },
    {
        "title": "Conversation",
        "lessons": [
            {"title": "Asking Questions", "content": "How to ask questions in English."},
            {"title": "Making Requests", "content": "How to make polite requests."},
            {"title": "Describing People & Places", "content": "Describe people and places in English."},
            {"title": "Talking About Daily Routines", "content": "Talk about your daily activities."},
        ]
    },
    {
        "title": "Reading & Writing",
        "lessons": [
            {"title": "Short Stories", "content": "Read and understand short stories."},
            {"title": "Writing Simple Sentences", "content": "Practice writing basic sentences."},
            {"title": "Filling Forms", "content": "Learn to fill out simple forms."},
            {"title": "Describing Pictures", "content": "Describe what you see in pictures."},
        ]
    }
]


for idx, unit_data in enumerate(units_data, start=1):
    unit, _ = Unit.objects.get_or_create(title=unit_data["title"], course=course, defaults={"order": idx})
    # If unit was retrieved and order is not set, update it
    if unit.order is None:
        unit.order = idx
        unit.save()
    for lesson_idx, lesson_data in enumerate(unit_data["lessons"], start=1):
        lesson, _ = Lesson.objects.get_or_create(
            title=lesson_data["title"],
            unit=unit,
            content=lesson_data["content"],
            defaults={"order": lesson_idx}
        )
        # If lesson was retrieved and order is not set, update it
        if lesson.order is None:
            lesson.order = lesson_idx
            lesson.save()
        # Add a sample exercise for each lesson
        Exercise.objects.get_or_create(
            lesson=lesson,
            question=f"Sample question for {lesson.title}",
            exercise_type="quiz",
            options={"A": "Option 1", "B": "Option 2"},
            answer="A",
            order=1
        )
print("Beginner English course, units, lessons, and sample exercises added!")
