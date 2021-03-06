# Copyright (c) 2013, Rabie Moses Santillan and contributors
# For license information, please see license.txt

import frappe

def execute(filters=None):
	columns, data = [], []
	columns = get_columns()
	data2 = frappe.get_all('Pawn Ticket Jewelry', filters={'item_series': 'B'}, fields=['date_loan_granted'], order_by='date_loan_granted desc',)
	for i in range(len(data2)):
		if not date_has_duplicate(data2[i]['date_loan_granted'], data):
			in_count_of_the_day_active = frappe.db.count('Pawn Ticket Jewelry', {'date_loan_granted': data2[i]['date_loan_granted'], 'workflow_state': 'Active', 'item_series': 'B'})

			renewed_count_of_the_day = frappe.db.count('Pawn Ticket Jewelry', {'change_status_date': data2[i]['date_loan_granted'], 'workflow_state': 'Renewed', 'item_series': 'B'})

			out_count = frappe.db.count('Pawn Ticket Jewelry', {'change_status_date': data2[i]['date_loan_granted'], 'workflow_state': 'Redeemed', 'item_series': 'B'})

			total_count_active = frappe.db.count('Pawn Ticket Jewelry', {'date_loan_granted': ['<=', data2[i]['date_loan_granted']], 'item_series': 'B', 'workflow_state': 'Active'})

			total_count_expire = frappe.db.count('Pawn Ticket Jewelry', {'change_status_date': ['<=', data2[i]['date_loan_granted']], 'item_series': 'B', 'workflow_state': 'Expired'})

			total_renewed = frappe.db.count('Pawn Ticket Jewelry', {'change_status_date': ['<=', data2[i]['date_loan_granted']], 'item_series': 'B', 'workflow_state':'Renewed'})

			in_for_today = in_count_of_the_day_active - renewed_count_of_the_day
			total = total_count_active + total_count_expire

			total_in_for_today = round_up_to_zero(in_for_today)
			total_pt_count = round_up_to_zero(total)

			data.append({'date_loan_granted': data2[i]['date_loan_granted'], 'in_count': total_in_for_today, 'out_count': out_count, 'total_count':total_pt_count})
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

def date_has_duplicate(date, data):
	has_duplicate = False
	for i in range(len(data)):
		if str(data[i]['date_loan_granted']) == str(date):
			has_duplicate = True
			return has_duplicate
	return has_duplicate


def round_up_to_zero(num):
	if int(num) < 0:
		num = 0
		return num
	return num