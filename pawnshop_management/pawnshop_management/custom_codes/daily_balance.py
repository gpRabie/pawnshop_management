import frappe

@frappe.whitelist()
def get_all_additional_pawn(date):

    total_J_pawn = frappe.db.get_all('Pawn Ticket Jewelry', filters={
				"branch": "Garcia's Pawnshop - GTC",
				"docstatus": 1,
				"date_loan_granted": date
			}, fields=['net_proceeds'], pluck='net_proceeds')

    total_NJ_pawn = frappe.db.get_all('Pawn Ticket Non Jewelry', filters={
				"branch": "Garcia's Pawnshop - GTC",
				"docstatus": 1,
				"date_loan_granted": date
			}, fields=['net_proceeds'], pluck='net_proceeds')

    sum = 0
    for record in total_J_pawn:
        sum += record
    for record in total_NJ_pawn:
        sum += record
    return sum

