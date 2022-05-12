import frappe
import frappe.permissions 
from frappe import _
from frappe.sessions import delete_session


def login_feed(login_manager):
    ip = frappe.local.request_ip
    print(ip)
    user = frappe.get_doc('User', login_manager.user)
    cavite_city = frappe.get_doc('Branch IP Addressing', "Garcia's Pawnshop - CC")
    poblacion = frappe.get_doc('Branch IP Addressing', "Garcia's Pawnshop - POB")
    tanza = frappe.get_doc('Branch IP Addressing', "Garcia's Pawnshop - TNZ")
    gtc = frappe.get_doc('Branch IP Addressing', "Garcia's Pawnshop - GTC")
    molino = frappe.get_doc('Branch IP Addressing', "Garcia's Pawnshop - MOL")
    rabies_house = frappe.get_doc('Branch IP Addressing', "Rabie's House")
    branch = {
        cavite_city.ip_address : "Garcia's Pawnshop Cavite City Branch",
        gtc.ip_address : "Garcia's Pawnshop GTC Branch",
        molino.ip_address : "Garcia's Pawnshop Molino Branch",
        poblacion.ip_address : "Garcia's Pawnshop Poblacion Branch",
        tanza.ip_address : "Garcia's Pawnshop Tanza Branch",
        rabies_house.ip_address : "Rabie's House"
    }
    if user.role_profile_name == "Cashier" or user.role_profile_name == "Appraiser" or user.role_profile_name == "Vault Custodian" or user.role_profile_name == "Supervisor/Cashier" or user.role_profile_name == "Appraiser/Cashier" or user.role_profile_name == "Supervisor":
        # if ip != "127.0.0.1":
        if ip == cavite_city.ip_address or ip == gtc.ip_address or ip == molino.ip_address or ip == poblacion.ip_address or ip == tanza.ip_address or ip == rabies_house.ip_address:  # or ip == rabies_house.ip_address
            frappe.msgprint(
                msg = 'Welcome, ' + user.full_name,
                title = 'Welcome to ' + branch[ip]
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
            return 0

def post_login(login_manager):
    if login_feed(login_manager) == 0:
        delete_session()
