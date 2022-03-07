import frappe
from frappe.utils import today


@frappe.whitelist()
def update_pawn_tickets():
    non_jewelry = frappe.db.get_all('Pawn Ticket Non Jewelry', 
        filters={
            'workflow_state': 'Active'
        },
        pluck='name')
    for i in range(len(non_jewelry)):
        pawn_ticket=frappe.get_doc('Pawn Ticket Non Jewelry', non_jewelry[i])
        print(type(pawn_ticket.expiry_date))
        # if pawn_ticket.expiry_date) < str(today()):
        #     print("True")

@frappe.whitelist()
def get_child_table():
    items = frappe.get_doc('Pawn Ticket Non Jewelry', '6B')
    return items