import frappe
from frappe.utils import today


@frappe.whitelist()
def update_fields_after_status_change_review_nj_batch(inventory_tracing_no):
    doc = frappe.get_doc("Non Jewelry Batch", inventory_tracing_no)
    for items in doc.get('items'):
        frappe.db.set_value('Non Jewelry Items', items.item_no, 'workflow_state', 'Returned')
        frappe.db.commit()

@frappe.whitelist()
def update_fields_after_status_change_collect_nj_batch(inventory_tracing_no):
    doc = frappe.get_doc("Non Jewelry Batch", inventory_tracing_no)
    for items in doc.get('items'):
        frappe.db.set_value('Non Jewelry Items', items.item_no, 'workflow_state', 'Collected')
        frappe.db.commit()

@frappe.whitelist()
def update_fields_after_status_change_redeem_nj_batch(inventory_tracing_no):
    doc = frappe.get_doc("Non Jewelry Batch", inventory_tracing_no)
    for items in doc.get('items'):
        frappe.db.set_value('Non Jewelry Items', items.item_no, 'workflow_state', 'Redeemed')
        frappe.db.commit()

@frappe.whitelist()
def update_fields_after_status_change_renew_nj_batch(inventory_tracing_no):
    doc = frappe.get_doc("Non Jewelry Batch", inventory_tracing_no)
    for items in doc.get('items'):
        frappe.db.set_value('Non Jewelry Items', items.item_no, 'workflow_state', 'Renewed')
        frappe.db.commit()
        