import frappe
import frappe.permissions
from frappe.utils import get_fullname
from frappe import _
from frappe.core.doctype.activity_log.activity_log import add_authentication_log

def login_feed(login_manager):
    ip = frappe.local.request_ip
    user = frappe.get_doc('User', login_manager.user)
    if user.role_profile_name == "Cashier" or user.role_profile_name == "Appraiser" or user.role_profile_name == "Vault Custodian" or user.role_profile_name == "Supervisor/Cashier" or user.role_profile_name == "Appraiser/Cashier" or user.role_profile_name == "Supervisor":
        # if ip == "127.0.0.1":
        if ip == "180.195.203.152" or ip == "180.191.229.200" or ip == "49.144.96.243" or ip == "49.144.15.239" or ip == "112.210.69.32":
            frappe.msgprint(
                msg = 'Welcome ' + user.full_name,
                title = 'Welcome'
            )
        # user = frappe.get_doc('user', login_manager.user)
        # print(user.role_profile_name)
            # frappe.throw(
            #     title='Error',
            #     msg='test',
            #     exc= RuntimeError
            # )
        else:
            frappe.throw(
                title = 'Log In Restricted',
                msg = 'You are not authorized to login in this station',
                exc = RuntimeError
            )