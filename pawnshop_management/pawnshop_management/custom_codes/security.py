import socket
import frappe

@frappe.whitelist()
def get_ip():
    return socket.gethostbyname(socket.gethostname())
