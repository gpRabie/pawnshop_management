import frappe

@frappe.whitelist()
def get_loyalty_program():
    doc2 = frappe.get_doc('Customer', "1-238-10202020")
    return doc2.loyalty_program