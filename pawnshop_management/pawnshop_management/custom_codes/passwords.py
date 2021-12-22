from __future__ import unicode_literals
import string
import frappe
import base64
from frappe import _
from frappe.utils import cstr, encode
from cryptography.fernet import Fernet, InvalidToken
from passlib.hash import pbkdf2_sha256, mysql41
from passlib.registry import register_crypt_handler
from passlib.context import CryptContext
from frappe.utils.password import get_decrypted_password, decrypt, get_encryption_key,encrypt

@frappe.whitelist()
def validate_user(doctype, name, fieldname='password', raise_exception=True):
    auth = frappe.db.sql("""select `password` from `__Auth` where doctype=%(doctype)s and name=%(name)s 
                        and fieldname=%(fieldname)s and encrypted=0""", {
                            'doctype': doctype, 'name': name, 'fieldname': fieldname})
    password = encode(auth[0][0])
    while len(password) % 4 != 0:
        password += b'='
    return decrypt(encode(password))
    
    
    
