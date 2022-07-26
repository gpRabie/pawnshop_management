# Copyright (c) 2013, Rabie Moses Santillan and contributors
# For license information, please see license.txt

import frappe
from frappe.utils import today

def execute(filters=None):
	columns, data = [], []
	date = ""
	columns = get_columns()
	data = frappe.get_all('Pawn Ticket Jewelry', 
		filters= {
			'date_loan_granted': ['<', today()]
		},
		fields=['date_loan_granted', 'name']
	)
	for i in range(len(data)):
		pass
		
	for i in range(len(data)):
		data[i]['in_count'] = frappe.db.count('Pawn Ticket Jewelry', 
			{'date_loan_granted': data[i]['date_loan_granted'], 'workflow_state': 'Active'}
	)
	for i in range(len(data)):
		data[i]['out_count'] = frappe.db.count('Pawn Ticket Jewelry', 
			{'date_loan_granted': data[i]['date_loan_granted'], 'workflow_state': 'Redeemed'}
	)

	for i in range(len(data)):
		data[i]['total_count'] = frappe.db.count('Pawn Ticket Jewelry', 
			{'workflow_state':['Active', 'Expired']}
	)
	return columns, data


def get_columns():
	columns = [
		{
			'fieldname': 'date_loan_granted',
			'label': 'Date',
			'fieldtype': 'Date',
			'width': 200
		},

		{
			'fieldname': 'in_count',
			'label': 'IN',
			'fieldtype': 'Int',
			'width': 100
		},

		{
			'fieldname': 'out_count',
			'label': 'OUT',
			'fieldtype': 'Int',
			'width': 100
		},

		{
			'fieldname': 'total_count',
			'label': 'Total',
			'fieldtype': 'Int',
			'width': 100
		}
	]
	return columns

def check_date_uplicate(data):
	pass
	# for dates in data:
	# 	if dates['date_loan_granted'] 