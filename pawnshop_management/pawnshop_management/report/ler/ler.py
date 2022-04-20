# Copyright (c) 2013, Rabie Moses Santillan and contributors
# For license information, please see license.txt

import frappe
from frappe import _ 

def execute(filters=None):
	columns, data = [], []
	columns = get_columns()
	data = frappe.get_all("Pawn Ticket Non Jewelry", filters=filters, fields=['date_loan_granted', 'customers_full_name', 'pawn_ticket', 'desired_principal', 'interest', 'net_proceeds'])
	return columns, data

def get_columns():
	columns = [
		{
			'fieldname': 'date_loan_granted',
			'label': _('Date'),
			'fieldtype': 'Date',
			'width': 150
		},

		{
			'fieldname': 'customers_full_name',
			'label': _('Name'),
			'fieldtype': 'Link',
			'options': 'Customer',
			'width': 200
		},

		{
			'fieldname': 'pawn_ticket',
			'label': _('P.T.'),
			'fieldtype': 'Link',
			'options': 'Pawn Ticket Non Jewelry',
			'width': 150
		},

		{
			'fieldname': 'or',
			'label': _('OR'),
			'fieldtype': 'Link',
			'options': 'Pawn Ticket Non Jewelry',
			'width': 100
		},


		{
			'fieldname': 'desired_principal',
			'label': _('Principal'),
			'fieldtype': 'Currency',
			'width': 150
		},

		{
			'fieldname': 'interest',
			'label': _('Advance Interest'),
			'fieldtype': 'Currency',
			'width': 150
		},

		{
			'fieldname': 'net_proceeds',
			'label': _('Cash On Hand'),
			'fieldtype': 'Currency',
			'width': 150
		}

	]
	return columns