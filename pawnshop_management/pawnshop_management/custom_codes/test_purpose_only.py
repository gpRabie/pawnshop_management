from datetime import datetime
import re # from python std library
from frappe.utils import add_to_date
import frappe

@frappe.whitelist()
def add_months(date):
    months = add_to_date(date, months=-6)
    return months