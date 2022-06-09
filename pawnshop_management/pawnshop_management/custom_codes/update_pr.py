from typing import List, Set

import frappe
from frappe import _
from frappe.core.doctype.doctype.doctype import validate_series
from frappe.model.document import Document
from frappe.model.naming import NamingSeries
from frappe.permissions import get_doctypes_with_read
from frappe.utils import cint

@frappe.whitelist()
def increment_pr_no(prefix):
    naming_series = NamingSeries(prefix)
    previous_value = naming_series.get_current_value()
    naming_series.update_counter(previous_value + 1)
    return previous_value
