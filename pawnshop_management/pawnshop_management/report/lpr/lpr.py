# Copyright (c) 2013, Rabie Moses Santillan and contributors
# For license information, please see license.txt

import frappe
from frappe import _ 
def execute(filters=None):
	columns, data = [], []
	columns = get_columns()
	data = frappe.get_all("Provisional Receipt", filters=filters, fields=['date_issued', 'complete_name', 'pawn_ticket_no', 'principal_amount', 'interest_payment'])
	for i in range(len(data)):
		cash_on_hand = 0.00
		cash_on_hand = data[i]['principal_amount'] + data[i]['interest_payment']
		data[i]['cash_on_hand'] = cash_on_hand
	return columns, data

def get_columns():
	columns = [
		{
			'fieldname': 'date_issued',
			'label': _('Date'),
			'fieldtype': 'Date',
			'width': 120
		},

		{
			'fieldname': 'complete_name',
			'label': _('Customer'),
			'fieldtype': 'Data',
			'width': 120
		},

		{
			'fieldname': 'pawn_ticket_no',
			'label': _('P.T.'),
			'fieldtype': 'Link',
			'options': 'Pawn Ticket Non Jewelry',
			'width': 120
		},

		{
			'fieldname': 'principal_amount',
			'label': _('Pledged Loan'),
			'fieldtype': 'Currency',
			'width': 120
		},

		{
			'fieldname': 'interest_payment',
			'label': _('Accrued Interest'),
			'fieldtype': 'Currency',
			'width': 120
		},

		{
			'fieldname': 'cash_on_hand',
			'label': _('Cash On Hand'),
			'fieldtype': 'Currency',
			'width': 120
		}
	]

	return columns
