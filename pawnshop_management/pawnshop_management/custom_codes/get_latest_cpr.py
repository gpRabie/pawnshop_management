import frappe

@frappe.whitelist()
def get_latest_cpr(branch):
    if frappe.db.exists('Cash Position Report', {'branch': branch}):
        cpr = frappe.get_last_doc('Cash Position Report', filters={"branch": branch})
        return cpr.ending_balance
        