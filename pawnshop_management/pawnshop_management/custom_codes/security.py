from requests import get
import frappe

@frappe.whitelist()
def get_ip():
    ip = frappe.local.request_ip
    return ip
