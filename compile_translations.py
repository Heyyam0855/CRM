import polib
import os

translations = {
    'en': {
        'Aktiv Tələbələr': 'Active Students',
        'Xoş gəldiniz, %(name)s. Bütün göstəricilər burada.': 'Welcome, %(name)s. All metrics are here.',
        'Keçirilən Dərslər': 'Conducted Lessons',
        'Aylıq Gəlir': 'Monthly Revenue',
        'Gözləyən Müraciətlər': 'Pending Applications',
        'Aylıq Statistika': 'Monthly Statistics',
        'Gəlir': 'Revenue',
        'Ümumi Baxış': 'Overview',
        'Bu ay dərslər': 'Lessons this month',
        'Gecikmiş ödəniş': 'Overdue payments',
        'Yaxınlaşan Dərslər': 'Upcoming Lessons',
        'Hamısına bax': 'See all',
        'Qoşul': 'Join',
        'Yaxınlaşan dərs yoxdur': 'No upcoming lessons',
        'Dərslər bölməsindən yeni dərs planlaşdırın': 'Plan a new lesson from the lessons section',
        'dərs': 'lesson',
        'Hələ məlumat yoxdur': 'No data yet',
        'İdarəçilik Paneli': 'Dashboard',
        'Tələbələr': 'Students',
        'Status': 'Status',
        'Tarix': 'Date'
    },
    'ru': {
        'Aktiv Tələbələr': 'Активные студенты',
        'Xoş gəldiniz, %(name)s. Bütün göstəricilər burada.': 'Добро пожаловать, %(name)s. Все показатели здесь.',
        'Keçirilən Dərslər': 'Проведенные уроки',
        'Aylıq Gəlir': 'Ежемесячный доход',
        'Gözləyən Müraciətlər': 'Ожидающие заявки',
        'Aylıq Statistika': 'Ежемесячная статистика',
        'Gəlir': 'Доход',
        'Ümumi Baxış': 'Обзор',
        'Bu ay dərslər': 'Уроки в этом месяце',
        'Gecikmiş ödəniş': 'Просроченные платежи',
        'Yaxınlaşan Dərslər': 'Предстоящие уроки',
        'Hamısına bax': 'Смотреть все',
        'Qoşul': 'Присоединиться',
        'Yaxınlaşan dərs yoxdur': 'Нет предстоящих уроков',
        'Dərslər bölməsindən yeni dərs planlaşdırın': 'Запланируйте новый урок в разделе уроков',
        'dərs': 'урок',
        'Hələ məlumat yoxdur': 'Пока нет данных',
        'İdarəçilik Paneli': 'Панель управления',
        'Tələbələr': 'Студенты',
        'Status': 'Статус',
        'Tarix': 'Дата'
    }
}

for lang in ['en', 'ru']:
    po_path = f'locale/{lang}/LC_MESSAGES/django.po'
    mo_path = f'locale/{lang}/LC_MESSAGES/django.mo'
    if os.path.exists(po_path):
        po = polib.pofile(po_path)
        for msgid, msgstr in translations[lang].items():
            entry = po.find(msgid)
            if entry:
                entry.msgstr = msgstr
            else:
                po.append(polib.POEntry(msgid=msgid, msgstr=msgstr))
        
        po.save(po_path)
        po.save_as_mofile(mo_path)
        print(f"Compiled translations for {lang}")
