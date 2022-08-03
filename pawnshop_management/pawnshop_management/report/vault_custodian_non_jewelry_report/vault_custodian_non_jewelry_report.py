# Copyright (c) 2013, Rabie Moses Santillan and contributors
# For license information, please see license.txt

import frappe

def execute(filters=None):
	columns, data = [], []
	columns = get_columns()
	data = frappe.get_all('Inventory Count', fields=['date', 'in_count_nj', 'out_count_nj', 'returned_nj', 'pulled_out_nj', 'total_nj'], order_by='date desc',)
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
			'fieldname': 'in_count_nj',
			'label': 'IN',
			'fieldtype': 'Int',
			'width': 100
		},

		{
			'fieldname': 'out_count_nj',
			'label': 'OUT',
			'fieldtype': 'Int',
			'width': 100
		},

		{
			'fieldname': 'returned_nj',
			'label': 'Returned',
			'fieldtype': 'Int',
			'width': 100
		},

		{
			'fieldname': 'pulled_out_nj',
			'label': 'Pulled Out',
			'fieldtype': 'Int',
			'width': 100
		},

		{
			'fieldname': 'total_nj',
			'label': 'Total',
			'fieldtype': 'Int',
			'width': 100
		}
	]
	return columns

