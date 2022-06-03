import frappe
from frappe.utils import today

@frappe.whitelist()
def update_fields_after_status_change_review_j_batch(inventory_tracing_no):
    doc = frappe.get_doc("Jewelry Batch", inventory_tracing_no)
    for items in doc.get('items'):
        frappe.db.set_value('Jewelry Items', items.item_no, 'workflow_state', 'Returned')
        frappe.db.commit()

@frappe.whitelist()
def update_fields_after_status_change_collect_j_batch(inventory_tracing_no):
    doc = frappe.get_doc("Jewelry Batch", inventory_tracing_no)
    for items in doc.get('items'):
        frappe.db.set_value('Jewelry Items', items.item_no, 'workflow_state', 'Collected')
        frappe.db.commit()

@frappe.whitelist()
def update_fields_after_status_change_redeem_j_batch(inventory_tracing_no):
    doc = frappe.get_doc("Jewelry Batch", inventory_tracing_no)
    for items in doc.get('items'):
        frappe.db.set_value('Jewelry Items', items.item_no, 'workflow_state', 'Redeemed')
        frappe.db.commit()