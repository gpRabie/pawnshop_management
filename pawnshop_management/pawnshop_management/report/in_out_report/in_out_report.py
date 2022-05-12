# Copyright (c) 2013, Rabie Moses Santillan and contributors
# For license information, please see license.txt

import frappe
from frappe import _ 

def execute(filters=None):
	columns, data = [], []
	columns = get_columns()
	values = {'company': "TEST Garcia's Pawnshop", 'branch': "Rabie's House"}
	data = frappe.db.sql("""
		SELECT 
			cpr.beginning_balance AS start_money,
			cpr.provisional_receipts AS receipt,
			cpr.total_in AS sulod,
			pt.total AS total
		FROM
			(`tabCash Position Report` cpr),
			(`tabProvisional Receipt` pt)
	""", values=values, as_dict=0)
	return columns, data


def get_columns():
	columns = [
		{
			'fieldname': 'start_money',
			'label': _('Beginning Balance'),
			'fieldtype': 'Currency',
			'width': 120
		},

		{
			'fieldname': 'receipt',
			'label': _('PRovisional Receipt'),
			'fieldtype': 'Currency',
			'width': 200
		},

		{
			'fieldname': 'sulod',
			'label': _('Total IN'),
			'fieldtype': 'Currency',
			'width': 200
		}, 

		{
			'fieldname': 'total',
			'label': _('Total PR'),
			'fieldtype': 'Currency',
			'width': 200
		}
	]

	return columns