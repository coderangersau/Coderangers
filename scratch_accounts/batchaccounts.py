import csv
import string
import sys
import traceback

from scratch_accounts.scratch import create_account


def fix(name):
    for value in string.punctuation + ' ':
        name = name.replace(value, '')
    return name.upper()


def csv_batch_create(filename, firstnamefield, lastnamefield, username_fn, password_fn, **kwargs):
    read = open(filename + '.csv')
    write = open(filename + '_out.csv', 'w')

    fieldnames = (firstnamefield, lastnamefield, 'Username', 'Password')
    result = csv.DictWriter(write, fieldnames)
    result.writeheader()

    for row in csv.DictReader(read):
        fname = fix(row[firstnamefield])
        lname = fix(row[lastnamefield])
        row['Username'] = username_fn(fname, lname, row)
        row['Password'] = username_fn(fname, lname, row)
        newrow = {}
        for field in fieldnames:
            newrow[field] = row[field]
        try:
            create_account(row['Username'], row['Password'], **kwargs)
        except Exception as e:
            newrow['Username'] = 'ERROR'
            newrow['Password'] = 'ERROR'
            traceback.print_tb(sys.exc_info()[2])
        result.writerow(newrow)

    write.close()

# csv_batch_create('mhs', 'First Name', 'Last Name',
#                  lambda fname, lname, row: 'MHS7%s%s' % (lname[:3], fname[0]),
#                  lambda fname, lname, row: '7%s%s%s' % (lname[:3], fname[0], str(random.randint(0, 99)).zfill(2)),
#                  email='coderangersau1@gmail.com'
# )


def csv_batch_details_create(filename):
    f = open(filename + '_out.csv', 'w')
    writer = csv.DictWriter(f, ('User Name', 'Password', 'Scratch account created'))
    writer.writeheader()
    for row in csv.DictReader(open(filename + '.csv')):
        if row['Scratch account created'] == '1' or row['Enrolled Student'] == 'FALSE':
            username = row['User Name']
            password = row['Password']
            created = row['Scratch account created']
        else:
            for i in range(999):
                i = '' if i == 0 else str(i)
                username = row['User Name'] + i
                password = row['Password'][:4] + i + row['Password'][4:]
                if create_account(username, password): break
            created = '1'
        writer.writerow({'User Name': username, 'Password': password, 'Scratch account created': created})
    f.close()

csv_batch_details_create('batch3')