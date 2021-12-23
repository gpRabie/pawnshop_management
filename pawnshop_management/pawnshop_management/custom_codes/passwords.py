from __future__ import unicode_literals
import string
import frappe
from frappe import _
from frappe.query_builder import Table
from frappe.utils import cstr, encode
from cryptography.fernet import Fernet, InvalidToken
from passlib.hash import pbkdf2_sha256, mysql41
from passlib.registry import register_crypt_handler
from passlib.context import CryptContext
from pypika.terms import Values
from frappe.utils.password import get_decrypted_password, decrypt, get_encryption_key,encrypt, check_password

Auth = Table("__Auth")

passlibctx = CryptContext(
	schemes=[
		"pbkdf2_sha256",
		"argon2",
		"frappe_legacy",
	],
	deprecated=[
		"frappe_legacy",
	],
)

@frappe.whitelist()
def validate_user(doctype, name, fieldname='password', raise_exception=True):
    auth = frappe.db.sql("""select `password` from `__Auth` where doctype=%(doctype)s and name=%(name)s 
                        and fieldname=%(fieldname)s and encrypted=0""", {
                            'doctype': doctype, 'name': name, 'fieldname': fieldname})
    password = encode(auth[0][0])
    while len(password) % 4 != 0:
        password += b'='
    return decrypt(encode(password))

def delete_login_failed_cache(user):
	frappe.cache().hdel("last_login_tried", user)
	frappe.cache().hdel("login_failed_count", user)
	frappe.cache().hdel("locked_account_time", user)


@frappe.whitelist()
def check_password(user, pwd, doctype="User", fieldname="password", delete_tracker_cache=True):
	"""Checks if user and password are correct, else raises frappe.AuthenticationError"""

	result = (
		frappe.qb.from_(Auth)
		.select(Auth.name, Auth.password)
		.where(
			(Auth.doctype == doctype)
			& (Auth.name == user)
			& (Auth.fieldname == fieldname)
			& (Auth.encrypted == 0)
		)
		.limit(1)
		.run(as_dict=True)
	)

	print(pwd)
	if not result or not passlibctx.verify(pwd, result[0].password):
		frappe.throw(
			title='Invalid Password',
			msg='Assistant Appriaser\'s password is incorrect',
		)

	# lettercase agnostic
	user = result[0].name
	return user
