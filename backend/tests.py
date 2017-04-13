from django.test import TestCase
import datetime,hashlib
from  django.utils import timezone
# Create your tests here.

def calculate_hash(hashstr,salt):
    salt = salt.encode()
    str = hashstr.encode()
    hash = hashlib.md5(salt)
    hash.update(str)
    res = hash.hexdigest()
    return res

a = calculate_hash("zhy200123","0hy1ovOL")
print(a)
