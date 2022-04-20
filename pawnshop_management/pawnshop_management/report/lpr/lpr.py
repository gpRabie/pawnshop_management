# Copyright (c) 2013, Rabie Moses Santillan and contributors
# For license information, please see license.txt

import frappe
from frappe import _ 
def execute(filters=None):
	columns, data = [], []
	data = frappe.get_all("Provisional Receipt", filters=filters, fields=['date_issued', 'complete_name', 'pawn_ticket_no', 'principal_amount', 'interest_payment'])
	print(cash_on_hand)
	return columns, data
