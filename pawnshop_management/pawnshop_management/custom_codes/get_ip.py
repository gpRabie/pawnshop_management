from requests import get
import frappe

@frappe.whitelist()
def get_ip():
    # ip = get('https://api.ipify.org').text
    # print(f'My public IP address is: {ip}')
    ip = frappe.local.request_ip
    return ip
