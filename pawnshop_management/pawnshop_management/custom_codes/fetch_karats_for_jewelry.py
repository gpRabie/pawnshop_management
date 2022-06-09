import frappe
from frappe.utils import flt

def fetch_weight_of_karats_from_items(item_no):
    total_weight = 0.0
    jewelry_item = frappe.get_doc('Jewelry Item', item_no)
    for child_doc in jewelry_item.get_children():
        total_weight += child_doc.weight
    return total_weight