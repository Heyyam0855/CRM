"""
LMS Platform — Draft Data Seed Command
Layihəni test məlumatları ilə doldurur: kurslar, modullar, dərslər, tələbələr, slotlar, bookings.
"""
import random
from datetime import timedelta
from decimal import Decimal

from django.core.management.base import BaseCommand
from django.utils import timezone

from apps.bookings.models import AvailabilitySlot, Booking, WeeklySchedule
from apps.courses.models import Category, Course, Enrollment, Lesson, Module
from apps.payments.models import MonthlySubscription, Payment
from apps.users.models import StudentProfile, User


class Command(BaseCommand):
    help = 'Layihəni draft/test məlumatları ilə doldurur'

    def add_arguments(self, parser):
        parser.add_argument(
            '--flush',
            action='store_true',
            help='Əvvəlcə mövcud draft datanı silir',
        )

    def handle(self, *args, **options):
        if options['flush']:
            self.stdout.write('Mövcud məlumatlar silinir...')
            Booking.objects.all().delete()
            AvailabilitySlot.objects.all().delete()
            WeeklySchedule.objects.all().delete()
            Payment.objects.all().delete()
            MonthlySubscription.objects.all().delete()
            Enrollment.objects.all().delete()
            Lesson.objects.all().delete()
            Module.objects.all().delete()
            Course.objects.all().delete()
            Category.objects.all().delete()
            User.objects.filter(role=User.Role.STUDENT).delete()

        teacher = self._ensure_teacher()
        categories = self._create_categories()
        courses = self._create_courses(categories)
        self._create_modules_and_lessons(courses)
        students = self._create_students()
        self._create_enrollments(students, courses)
        schedule = self._create_weekly_schedule()
        slots = self._create_availability_slots()
        self._create_bookings(students, slots, courses)
        self._create_payments(students)

        self.stdout.write(self.style.SUCCESS('Draft data uğurla yaradıldı!'))

    def _ensure_teacher(self) -> User:
        teacher, created = User.objects.get_or_create(
            role=User.Role.TEACHER,
            defaults={
                'email': 'muellim@pragmalife.az',
                'first_name': 'Samir',
                'last_name': 'Müəllim',
                'is_staff': True,
            }
        )
        if created:
            teacher.set_password('teacher123')
            teacher.save()
            self.stdout.write(f'  Müəllim yaradıldı: {teacher.email}')
        else:
            self.stdout.write(f'  Müəllim mövcuddur: {teacher.email}')
        return teacher

    def _create_categories(self) -> list:
        self.stdout.write('Kateqoriyalar yaradılır...')
        data = [
            {'name': 'Web Development', 'slug': 'web-development',
             'description': 'Veb proqramlaşdırma kursları'},
            {'name': 'Backend Development', 'slug': 'backend-development',
             'description': 'Server tərəfi proqramlaşdırma'},
            {'name': 'Frontend Development', 'slug': 'frontend-development',
             'description': 'İstifadəçi interfeysi inkişafı'},
            {'name': 'Data Science', 'slug': 'data-science',
             'description': 'Data elmi və analitika'},
            {'name': 'DevOps', 'slug': 'devops',
             'description': 'DevOps və bulud texnologiyaları'},
        ]
        categories = []
        for item in data:
            cat, _ = Category.objects.get_or_create(
                slug=item['slug'],
                defaults=item,
            )
            categories.append(cat)
        self.stdout.write(f'  {len(categories)} kateqoriya yaradıldı')
        return categories

    def _create_courses(self, categories: list) -> list:
        self.stdout.write('Kurslar yaradılır...')
        courses_data = [
            {
                'title': 'Python ilə Proqramlaşdırma',
                'slug': 'python-programming',
                'description': 'Python dilinin əsaslarından başlayaraq irəli səviyyəyə qədər.',
                'category': categories[1],  # Backend
                'status': Course.Status.ACTIVE,
                'level': Course.Level.BEGINNER,
                'objectives': 'Python sintaksisi, OOP, fayl əməliyyatları, modullar',
                'prerequisites': 'Heç bir ön biliy tələb olunmur',
                'duration_weeks': 12,
            },
            {
                'title': 'Django Web Development',
                'slug': 'django-web-development',
                'description': 'Django framework ilə tam funksional veb tətbiqlər yaratmaq.',
                'category': categories[0],  # Web
                'status': Course.Status.ACTIVE,
                'level': Course.Level.INTERMEDIATE,
                'objectives': 'Django models, views, templates, REST API, deployment',
                'prerequisites': 'Python əsasları bilinməlidir',
                'duration_weeks': 16,
            },
            {
                'title': 'React.js Frontend Development',
                'slug': 'reactjs-frontend',
                'description': 'React.js ilə müasir single-page tətbiqlər.',
                'category': categories[2],  # Frontend
                'status': Course.Status.ACTIVE,
                'level': Course.Level.INTERMEDIATE,
                'objectives': 'React components, hooks, state management, routing',
                'prerequisites': 'HTML, CSS, JavaScript əsasları',
                'duration_weeks': 14,
            },
            {
                'title': 'Full Stack Development',
                'slug': 'full-stack-development',
                'description': 'Django + React ilə tam stack veb inkişafı.',
                'category': categories[0],  # Web
                'status': Course.Status.ACTIVE,
                'level': Course.Level.ADVANCED,
                'objectives': 'Backend API, Frontend SPA, Docker, CI/CD',
                'prerequisites': 'Python və JavaScript bilikləri',
                'duration_weeks': 24,
            },
            {
                'title': 'Data Structures & Algorithms',
                'slug': 'dsa',
                'description': 'Alqoritmlər və data strukturları — müsahibəyə hazırlıq.',
                'category': categories[3],  # Data Science
                'status': Course.Status.ACTIVE,
                'level': Course.Level.INTERMEDIATE,
                'objectives': 'Arrays, LinkedList, Trees, Graph, DP, Sorting',
                'prerequisites': 'Minimum bir proqramlaşdırma dili biliyiniz olmalıdır',
                'duration_weeks': 10,
            },
            {
                'title': 'API Driven Development',
                'slug': 'api-driven-development',
                'description': 'REST və GraphQL API dizayn və inkişafı.',
                'category': categories[1],  # Backend
                'status': Course.Status.DRAFT,
                'level': Course.Level.ADVANCED,
                'objectives': 'REST API, GraphQL, Authentication, Swagger',
                'prerequisites': 'Django və ya Node.js bilikləri',
                'duration_weeks': 8,
            },
        ]
        courses = []
        for item in courses_data:
            course, _ = Course.objects.get_or_create(
                slug=item['slug'],
                defaults=item,
            )
            courses.append(course)
        self.stdout.write(f'  {len(courses)} kurs yaradıldı')
        return courses

    def _create_modules_and_lessons(self, courses: list) -> None:
        self.stdout.write('Modullar və dərslər yaradılır...')

        modules_map = {
            'python-programming': [
                ('Python Əsasları', [
                    'Python quraşdırma və IDE',
                    'Dəyişənlər və Data Tipləri',
                    'Şərt operatorları (if/elif/else)',
                    'Dövr operatorları (for/while)',
                    'Funksiyalar',
                ]),
                ('Data Strukturları', [
                    'List və Tuple',
                    'Dictionary və Set',
                    'List Comprehension',
                    'String əməliyyatları',
                ]),
                ('OOP — Obyekt Yönümlü Proqramlaşdırma', [
                    'Class və Object anlayışı',
                    'Inheritance (Miras alma)',
                    'Polymorphism',
                    'Encapsulation',
                    'Magic Methods',
                ]),
                ('Fayl və Modul', [
                    'Fayl oxuma / yazma',
                    'JSON və CSV',
                    'Modullar və Paketlər',
                    'Virtual Environment',
                ]),
            ],
            'django-web-development': [
                ('Django Əsasları', [
                    'Django quraşdırma və layihə strukturu',
                    'URL routing və Views',
                    'Django Templates',
                    'Static fayllar',
                ]),
                ('Models və Database', [
                    'Django ORM və Models',
                    'Migrations',
                    'QuerySet API',
                    'Admin paneli',
                ]),
                ('Forms və Authentication', [
                    'Django Forms',
                    'ModelForm',
                    'User Authentication',
                    'Permissions və Mixins',
                ]),
                ('REST API', [
                    'Django REST Framework',
                    'Serializers',
                    'ViewSets və Routers',
                    'Token Authentication',
                    'API Documentation (Swagger)',
                ]),
                ('Deployment', [
                    'Docker ilə konteynerləşdirmə',
                    'PostgreSQL konfiqurasiyası',
                    'Nginx + Gunicorn',
                    'CI/CD pipeline',
                ]),
            ],
            'reactjs-frontend': [
                ('React Əsasları', [
                    'React quraşdırma (Vite/CRA)',
                    'JSX sintaksisi',
                    'Components və Props',
                    'State və Events',
                ]),
                ('Hooks və State Management', [
                    'useState və useEffect',
                    'useContext və useReducer',
                    'Custom Hooks',
                    'Zustand / Redux Toolkit',
                ]),
                ('Routing və API', [
                    'React Router',
                    'Axios ilə API çağırışları',
                    'Authentication flows',
                    'Error handling',
                ]),
            ],
            'full-stack-development': [
                ('Backend — Django API', [
                    'Layihə strukturu',
                    'REST API dizaynı',
                    'Authentication (JWT)',
                ]),
                ('Frontend — React', [
                    'React layihə qurulması',
                    'API inteqrasiyası',
                    'State management',
                ]),
                ('DevOps', [
                    'Docker Compose',
                    'Nginx reverse proxy',
                    'Production deployment',
                ]),
            ],
            'dsa': [
                ('Əsas Data Strukturları', [
                    'Arrays və Strings',
                    'Linked Lists',
                    'Stacks və Queues',
                    'Hash Tables',
                ]),
                ('Ağac və Qraf', [
                    'Binary Trees',
                    'BST əməliyyatları',
                    'Graph BFS/DFS',
                    'Shortest Path alqoritmləri',
                ]),
                ('Alqoritmik Texnikalar', [
                    'Two Pointers',
                    'Sliding Window',
                    'Dynamic Programming',
                    'Backtracking',
                ]),
            ],
            'api-driven-development': [
                ('REST API Dizaynı', [
                    'REST prinsipləri',
                    'Endpoint dizaynı',
                    'Versioning',
                    'Error handling',
                ]),
                ('GraphQL', [
                    'GraphQL əsasları',
                    'Schema və Resolver-lər',
                    'Mutations',
                ]),
            ],
        }

        total_lessons = 0
        for course in courses:
            module_data = modules_map.get(course.slug, [])
            for order, (mod_title, lesson_titles) in enumerate(module_data, 1):
                module, _ = Module.objects.get_or_create(
                    course=course,
                    title=mod_title,
                    defaults={'order': order, 'description': f'{mod_title} modulu'},
                )
                for l_order, l_title in enumerate(lesson_titles, 1):
                    Lesson.objects.get_or_create(
                        module=module,
                        title=l_title,
                        defaults={
                            'order': l_order,
                            'material_type': Lesson.MaterialType.VIDEO,
                            'description': f'{l_title} — dərs materialı',
                        },
                    )
                    total_lessons += 1

        self.stdout.write(f'  {total_lessons} dərs yaradıldı')

    def _create_students(self) -> list:
        self.stdout.write('Tələbələr yaradılır...')
        students_data = [
            {
                'email': 'ali.hasanov@example.com',
                'first_name': 'Əli',
                'last_name': 'Həsənov',
                'phone': '+994501234567',
                'profile': {
                    'status': StudentProfile.Status.ACTIVE,
                    'payment_model': StudentProfile.PaymentModel.MONTHLY,
                    'lessons_per_week': 3,
                    'github_username': 'ali-hasanov',
                    'education_level': 'Bakalavr — Kompüter Elmləri',
                    'goals': 'Full-stack developer olmaq istəyirəm',
                },
            },
            {
                'email': 'leyla.mammadova@example.com',
                'first_name': 'Leyla',
                'last_name': 'Məmmədova',
                'phone': '+994552345678',
                'profile': {
                    'status': StudentProfile.Status.ACTIVE,
                    'payment_model': StudentProfile.PaymentModel.PER_LESSON,
                    'lessons_per_week': 2,
                    'github_username': 'leyla-dev',
                    'education_level': 'Magistr — İnformasiya Texnologiyaları',
                    'goals': 'Backend developer kimi karyera qurmaq',
                },
            },
            {
                'email': 'rashad.aliyev@example.com',
                'first_name': 'Rəşad',
                'last_name': 'Əliyev',
                'phone': '+994703456789',
                'profile': {
                    'status': StudentProfile.Status.ACTIVE,
                    'payment_model': StudentProfile.PaymentModel.MONTHLY,
                    'lessons_per_week': 2,
                    'github_username': 'rashad-codes',
                    'education_level': 'Bakalavr — Riyaziyyat',
                    'goals': 'Data structures və algorithms öyrənmək',
                },
            },
            {
                'email': 'nigar.huseynova@example.com',
                'first_name': 'Nigar',
                'last_name': 'Hüseynova',
                'phone': '+994514567890',
                'profile': {
                    'status': StudentProfile.Status.ACTIVE,
                    'payment_model': StudentProfile.PaymentModel.MONTHLY,
                    'lessons_per_week': 3,
                    'github_username': 'nigar-h',
                    'education_level': 'Bakalavr — Dizayn',
                    'goals': 'Frontend developer olmaq, React öyrənmək',
                },
            },
            {
                'email': 'tural.ismayilov@example.com',
                'first_name': 'Tural',
                'last_name': 'İsmayılov',
                'phone': '+994555678901',
                'profile': {
                    'status': StudentProfile.Status.PENDING,
                    'payment_model': StudentProfile.PaymentModel.PER_LESSON,
                    'lessons_per_week': 1,
                    'github_username': 'tural-dev',
                    'education_level': 'Özünütəhsil',
                    'goals': 'Karyera dəyişikliyi — proqramlaşdırmaya keçmək',
                },
            },
            {
                'email': 'aysel.abdullayeva@example.com',
                'first_name': 'Aysel',
                'last_name': 'Abdullayeva',
                'phone': '+994776789012',
                'profile': {
                    'status': StudentProfile.Status.FROZEN,
                    'payment_model': StudentProfile.PaymentModel.MONTHLY,
                    'lessons_per_week': 2,
                    'github_username': 'aysel-dev',
                    'education_level': 'Bakalavr — İqtisadiyyat',
                    'goals': 'Freelance web developer olmaq',
                },
            },
            {
                'email': 'kamran.orucov@example.com',
                'first_name': 'Kamran',
                'last_name': 'Orucov',
                'phone': '+994507890123',
                'profile': {
                    'status': StudentProfile.Status.ACTIVE,
                    'payment_model': StudentProfile.PaymentModel.MONTHLY,
                    'lessons_per_week': 2,
                    'github_username': 'kamran-o',
                    'education_level': 'Magistr — Proqram Mühəndisliyi',
                    'goals': 'Django ilə SaaS layihə qurmaq',
                },
            },
            {
                'email': 'gunel.valiyeva@example.com',
                'first_name': 'Günəl',
                'last_name': 'Vəliyeva',
                'phone': '+994518901234',
                'profile': {
                    'status': StudentProfile.Status.ACTIVE,
                    'payment_model': StudentProfile.PaymentModel.PER_LESSON,
                    'lessons_per_week': 1,
                    'github_username': 'gunel-v',
                    'education_level': 'Bakalavr — Fizika',
                    'goals': 'Python ilə data science öyrənmək',
                },
            },
        ]

        students = []
        for data in students_data:
            profile_data = data.pop('profile')
            user, created = User.objects.get_or_create(
                email=data['email'],
                defaults={
                    **data,
                    'role': User.Role.STUDENT,
                },
            )
            if created:
                user.set_password('student123')
                user.save()

            # StudentProfile — signal ilə yaranıbsa update et, yaranmayıbsa yarat
            profile, _ = StudentProfile.objects.update_or_create(
                user=user,
                defaults=profile_data,
            )
            students.append(user)

        self.stdout.write(f'  {len(students)} tələbə yaradıldı')
        return students

    def _create_enrollments(self, students: list, courses: list) -> None:
        self.stdout.write('Enrollment-lər yaradılır...')
        # Hər aktiv tələbəni ən az 1 kursa qeydiyyat et
        enrollment_map = {
            0: [0, 1],       # Əli → Python, Django
            1: [1, 3],       # Leyla → Django, Full Stack
            2: [4],          # Rəşad → DSA
            3: [2],          # Nigar → React
            4: [0],          # Tural → Python
            5: [1, 2],       # Aysel → Django, React
            6: [1, 5],       # Kamran → Django, API
            7: [0],          # Günəl → Python
        }
        count = 0
        for s_idx, c_indices in enrollment_map.items():
            for c_idx in c_indices:
                _, created = Enrollment.objects.get_or_create(
                    student=students[s_idx],
                    course=courses[c_idx],
                    defaults={'is_active': True},
                )
                if created:
                    count += 1
        self.stdout.write(f'  {count} enrollment yaradıldı')

    def _create_weekly_schedule(self) -> list:
        self.stdout.write('Həftəlik cədvəl yaradılır...')
        # Bazar ertəsi — Cümə, 10:00-20:00
        schedules = []
        for day in range(5):  # Mon-Fri
            schedule, _ = WeeklySchedule.objects.get_or_create(
                day_of_week=day,
                start_time='10:00:00',
                defaults={
                    'end_time': '20:00:00',
                    'slot_duration': 60,
                    'is_active': True,
                },
            )
            schedules.append(schedule)
        # Şənbə 10:00-15:00
        schedule, _ = WeeklySchedule.objects.get_or_create(
            day_of_week=5,
            start_time='10:00:00',
            defaults={
                'end_time': '15:00:00',
                'slot_duration': 60,
                'is_active': True,
            },
        )
        schedules.append(schedule)
        self.stdout.write(f'  {len(schedules)} həftəlik slot yaradıldı')
        return schedules

    def _create_availability_slots(self) -> list:
        self.stdout.write('Availability slotlar yaradılır...')
        now = timezone.now()
        slots = []

        # Keçmiş slotlar (son 2 həftə) — tamamlanmış dərslər üçün
        for day_offset in range(-14, 0):
            date = now + timedelta(days=day_offset)
            weekday = date.weekday()
            if weekday > 5:  # Bazar — skip
                continue
            hours = [10, 11, 14, 15, 16, 18, 19] if weekday < 5 else [10, 11, 13, 14]
            for hour in hours:
                start = date.replace(hour=hour, minute=0, second=0, microsecond=0)
                end = start + timedelta(hours=1)
                slot, _ = AvailabilitySlot.objects.get_or_create(
                    start_time=start,
                    defaults={
                        'end_time': end,
                        'is_reserved': True,
                        'is_active': True,
                    },
                )
                slots.append(slot)

        # Gələcək slotlar (növbəti 2 həftə)
        for day_offset in range(0, 15):
            date = now + timedelta(days=day_offset)
            weekday = date.weekday()
            if weekday > 5:
                continue
            hours = [10, 11, 14, 15, 16, 18, 19] if weekday < 5 else [10, 11, 13, 14]
            for hour in hours:
                start = date.replace(hour=hour, minute=0, second=0, microsecond=0)
                if start <= now:
                    continue
                end = start + timedelta(hours=1)
                slot, _ = AvailabilitySlot.objects.get_or_create(
                    start_time=start,
                    defaults={
                        'end_time': end,
                        'is_reserved': False,
                        'is_active': True,
                    },
                )
                slots.append(slot)

        self.stdout.write(f'  {len(slots)} slot yaradıldı')
        return slots

    def _create_bookings(self, students: list, slots: list, courses: list) -> None:
        self.stdout.write('Booking-lər yaradılır...')
        now = timezone.now()

        # Aktiv tələbələr — profile refresh
        active_students = []
        for s in students:
            try:
                profile = StudentProfile.objects.get(user=s)
                if profile.status == StudentProfile.Status.ACTIVE:
                    active_students.append(s)
            except StudentProfile.DoesNotExist:
                pass

        if not active_students:
            self.stdout.write(self.style.WARNING('  Aktiv tələbə yoxdur, booking yaradılmadı'))
            return

        # Booked slot ID-ləri
        booked_slot_ids = set(Booking.objects.values_list('slot_id', flat=True))

        past_slots = [s for s in slots if s.start_time < now and s.id not in booked_slot_ids]
        future_slots = [s for s in slots if s.start_time > now and s.id not in booked_slot_ids]

        # Keçmiş dərslər — tamamlanmış
        topics = [
            'Python dəyişənlər', 'Django Models', 'React Components',
            'OOP Əsasları', 'REST API', 'Git & GitHub',
            'Database dizaynı', 'CSS Flexbox', 'JavaScript Əsasları',
            'Django Templates', 'Authentication', 'Deployment',
            'Testing', 'Docker əsasları', 'SQL sorğuları',
        ]
        booking_count = 0

        for i, slot in enumerate(past_slots[:30]):
            student = active_students[i % len(active_students)]
            course = courses[i % len(courses)]
            status = random.choice([
                Booking.Status.COMPLETED,
                Booking.Status.COMPLETED,
                Booking.Status.COMPLETED,
                Booking.Status.NO_SHOW,
            ])
            Booking.objects.get_or_create(
                slot=slot,
                defaults={
                    'student': student,
                    'course': course,
                    'lesson_type': Booking.LessonType.STANDARD,
                    'status': status,
                    'topic': topics[i % len(topics)],
                    'price': Decimal('25.00'),
                    'is_paid': status == Booking.Status.COMPLETED,
                    'completed_at': slot.end_time if status == Booking.Status.COMPLETED else None,
                    'meet_link': 'https://meet.google.com/abc-defg-hij',
                },
            )
            slot.is_reserved = True
            slot.save(update_fields=['is_reserved'])
            booking_count += 1

        # Gələcək dərslər — planlaşdırılmış
        upcoming_topics = [
            'Celery task-lar', 'WebSocket integration', 'GraphQL əsasları',
            'Testing strategiyası', 'CI/CD pipeline', 'Performance tuning',
            'Security best practices', 'Code review', 'Docker Compose',
            'Kubernetes əsasları',
        ]
        for i, slot in enumerate(future_slots[:15]):
            student = active_students[i % len(active_students)]
            course = courses[i % min(len(courses), 4)]
            status = random.choice([
                Booking.Status.CONFIRMED,
                Booking.Status.CONFIRMED,
                Booking.Status.PENDING,
            ])
            Booking.objects.get_or_create(
                slot=slot,
                defaults={
                    'student': student,
                    'course': course,
                    'lesson_type': Booking.LessonType.STANDARD,
                    'status': status,
                    'topic': upcoming_topics[i % len(upcoming_topics)],
                    'price': Decimal('25.00'),
                    'is_paid': False,
                    'meet_link': 'https://meet.google.com/xyz-abcd-efg',
                },
            )
            slot.is_reserved = True
            slot.save(update_fields=['is_reserved'])
            booking_count += 1

        self.stdout.write(f'  {booking_count} booking yaradıldı')

    def _create_payments(self, students: list) -> None:
        self.stdout.write('Ödənişlər yaradılır...')
        now = timezone.now()
        count = 0

        active_students = []
        for s in students:
            try:
                profile = StudentProfile.objects.get(user=s)
                if profile.status == StudentProfile.Status.ACTIVE:
                    active_students.append(s)
            except StudentProfile.DoesNotExist:
                pass

        for student in active_students:
            profile = StudentProfile.objects.get(user=student)

            # Aylıq abunə tələbələr üçün subscription
            if profile.payment_model == StudentProfile.PaymentModel.MONTHLY:
                MonthlySubscription.objects.get_or_create(
                    student=student,
                    defaults={
                        'lessons_per_week': profile.lessons_per_week,
                        'monthly_amount': Decimal(str(profile.lessons_per_week * 4 * 25)),
                        'status': MonthlySubscription.Status.ACTIVE,
                        'next_billing_date': (now + timedelta(days=30)).date(),
                    }
                )

            # Son 2 ay ödənişlər
            for month_offset in range(2):
                payment_date = now - timedelta(days=30 * month_offset)
                amount = Decimal(str(profile.lessons_per_week * 4 * 25))
                Payment.objects.create(
                    student=student,
                    amount=amount,
                    status=Payment.Status.COMPLETED,
                    payment_method=Payment.PaymentMethod.EPOINT,
                    description=f'Aylıq ödəniş — {payment_date:%B %Y}',
                    paid_at=payment_date,
                )
                count += 1

        # Gözləyən ödəniş
        pending_student = active_students[0] if active_students else None
        if pending_student:
            Payment.objects.create(
                student=pending_student,
                amount=Decimal('200.00'),
                status=Payment.Status.PENDING,
                payment_method=Payment.PaymentMethod.EPOINT,
                description='Mart 2026 aylıq ödəniş',
                due_date=now + timedelta(days=5),
            )
            count += 1

        self.stdout.write(f'  {count} ödəniş yaradıldı')
