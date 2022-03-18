from requests import get
import frappe

@frappe.whitelist()
def get_ip():
    ip = get('https://api.ipify.org').text
    return ip
