import django, sys, os
os.environ['DJANGO_SETTINGS_MODULE'] = 'apiserver.settings'
django.setup()

from apiserver.api import models, old_models
from apiserver.api.serializers import process_image

MEMBER_FIELDS = [
    'id',
    'first_name',
    'last_name',
    'preferred_name',
    'status',
    'phone',
    'expire_date',
    'current_start_date',
    'application_date',
    'vetted_date',
    'monthly_fees',
    'emergency_contact_name',
    'emergency_contact_phone',
    # minor -> is_minor
    'birthdate',
    'guardian_name',
    'street_address',
    # city, provice -> city
    'postal_code',
]

TRANSACTION_FIELDS = [
    'id',
    'member_id',
    'date',
    'amount',
    'reference_number',
    'memo',
    'number_of_membership_months',
    'payment_method',
    'category',
    'account_type',
    'info_source',
]

CARD_FIELDS = [
    'id',
    'member_id',
    'card_number',
    'notes',
    'last_seen_at',
    'active_status',
]

COURSE_FIELDS = [
    'id',
    'name',
    'description',
    # True -> is_old
]

SESSION_FIELDS = [
    'id',
    # course_id -> course
    # instructor -> old_instructor
    'datetime',
    'cost',
]

TRAINING_FIELDS = [
    'id',
    # class_session_id -> session
    'member_id',
    'attendance_status',
    'sign_up_date',
    'paid_date',
]

photo_folders = os.listdir('old_photos')
print('Found {} member photo folders'.format(len(photo_folders)))


print('Deleting all members...')
models.Member.objects.all().delete()
print('Importing old members...')
old = old_models.Members.objects.using('old_portal').all()

for o in old:
    new = {}

    for f in MEMBER_FIELDS:
        new[f] = o.__dict__.get(f, None)

    if o.city and o.province:
        new['city'] = '{}, {}'.format(o.city, o.province)
    new['is_minor'] = o.minor

    small, medium, large = None, None, None
    if str(o.id) in photo_folders:
        folder = 'old_photos/' + str(o.id)
        if 'photo.jpg' in os.listdir(folder):
            small, medium, large = process_image(folder + '/photo.jpg')
            print('Found a photo')

    models.Member.objects.create(photo_small=small, photo_medium=medium, photo_large=large, **new)
    print('Imported member #{} - {} {}'.format(
        o.id, o.first_name, o.last_name
    ))


print('Deleting all transactions...')
models.Transaction.objects.all().delete()
print('Importing old transactions...')
old = old_models.Transactions.objects.using('old_portal').all()

for o in old:
    new = {}

    for f in TRANSACTION_FIELDS:
        new[f] = o.__dict__.get(f, None)

    models.Transaction.objects.create(**new)
    print('Imported transaction #{} - {} {}'.format(
        o.id, o.member_id, o.category
    ))


print('Deleting all cards...')
models.Card.objects.all().delete()
print('Importing old cards...')
old = old_models.AccessKeys.objects.using('old_portal').all()

for o in old:
    new = {}

    for f in CARD_FIELDS:
        new[f] = o.__dict__.get(f, None)

    models.Card.objects.create(**new)
    print('Imported card #{} - {} {}'.format(
        o.id, o.card_number, o.notes
    ))


print('Deleting all courses...')
models.Course.objects.all().delete()
print('Importing old courses...')
old = old_models.Courses.objects.using('old_portal').all()

for o in old:
    new = {}

    for f in COURSE_FIELDS:
        new[f] = o.__dict__.get(f, None)
    new['name'] = new['name'].split('<',1)[0]
    new['is_old'] = True

    models.Course.objects.create(**new)
    print('Imported course #{} - {}'.format(
        o.id, new['name']
    ))


print('Deleting all sessions...')
models.Session.objects.all().delete()
print('Importing old session...')
old = old_models.ClassSessions.objects.using('old_portal').all()

for o in old:
    new = {}

    for f in SESSION_FIELDS:
        new[f] = o.__dict__.get(f, None)
    new['course'] = models.Course.objects.get(id=o.course_id)
    new['old_instructor'] = o.instructor

    models.Session.objects.create(**new)
    print('Imported session #{} - {} {}'.format(
        o.id, o.instructor, new['course']
    ))


print('Deleting all training...')
models.Training.objects.all().delete()
print('Importing old training...')
old = old_models.ClassRegistrants.objects.using('old_portal').all()

for o in old:
    new = {}

    for f in TRAINING_FIELDS:
        new[f] = o.__dict__.get(f, None)
    new['session'] = models.Session.objects.get(id=o.class_session_id)

    models.Training.objects.create(**new)
    print('Imported training #{} - {} {}'.format(
        o.id, new['session'], o.member_id
    ))


print('Done.')