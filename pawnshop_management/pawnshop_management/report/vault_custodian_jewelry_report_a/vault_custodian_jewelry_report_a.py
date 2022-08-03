# Copyright (c) 2013, Rabie Moses Santillan and contributors
# For license information, please see license.txt

import frappe

def execute(filters=None):
	columns, data = [], []
	columns = get_columns()
	data = frappe.get_all('Inventory Count', fields=['date', 'in_count_a', 'out_count_a', 'returned_a', 'pulled_out_a', 'total_a'], order_by='date desc')
	return columns, data


def get_columns():
	columns = [
		{
			'fieldname': 'date',
			'label': 'Date',
			'fieldtype': 'Date',
			'width': 200
		},

		{
			'fieldname': 'in_count_a',
			'label': 'IN',
			'fieldtype': 'Int',
			'width': 100
		},

		{
			'fieldname': 'out_count_a',
			'label': 'OUT',
			'fieldtype': 'Int',
			'width': 100
		},

		{
			'fieldname': 'returned_a',
			'label': 'Returned',
			'fieldtype': 'Int',
			'width': 100
		},

		{
			'fieldname': 'pulled_out_a',
			'label': 'Pulled Out',
			'fieldtype': 'Int',
			'width': 100
		},

		{
			'fieldname': 'total_a',
			'label': 'Total',
			'fieldtype': 'Int',
			'width': 100
		}
	]
	return columns
