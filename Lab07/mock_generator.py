import json
import random
import string
import datetime

def generate_mock_emails(num_emails):
    emails = []
    for i in range(num_emails):
        email = {}
        email['id'] = i + 1
        email['recipient'] = ''.join(random.choices(string.ascii_lowercase, k=5)) + '@' + ''.join(random.choices(string.ascii_lowercase, k=5)) + '.com'
        email['sender'] = ''.join(random.choices(string.ascii_lowercase, k=5)) + '@' + ''.join(random.choices(string.ascii_lowercase, k=5)) + '.com'
        email['title'] = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
        email['content'] = ''.join(random.choices(string.ascii_uppercase + string.digits, k=50))
        email['sendDate'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        email['size'] = random.randint(1000, 5000)
        emails.append(email)
    return json.dumps(emails)

print(generate_mock_emails(100))