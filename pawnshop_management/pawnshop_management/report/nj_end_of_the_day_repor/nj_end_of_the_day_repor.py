# Copyright (c) 2013, Rabie Moses Santillan and contributors
# For license information, please see license.txt

import frappe
from frappe import _ # _ for to set the string into literal string

def execute(filters=None):
	columns, data = [], []
	columns = get_columns()
	data = frappe.get_all("Pawn Ticket Non Jewelry", filters=filters, fields=['pawn_ticket', 'customers_tracking_no', 'inventory_tracking_no', 'desired_principal', 'date_loan_granted', 'expiry_date', 'workflow_state'])
	return columns, data

def get_columns():
	columns = [
		{
			'fieldname': 'pawn_ticket',
			'label': _('Pawn Ticket'),
			'fieldtype': 'Link',
			'options': 'Pawn Ticket Non Jewelry',
			'width': 100
		},

		{
			'fieldname': 'customers_tracking_no',
			'label': _('Customer Tracking No'),
			'fieldtype': 'Link',
			'options': 'Customer',
			'width': 200
		},

		{
			'fieldname': 'inventory_tracking_no',
			'label': _('Inventory Tracking No'),
			'fieldtype': 'Link',
			'options': 'Non Jewelry Batch',
			'width': 100
		},

		{
			'fieldname': 'desired_principal',
			'label': _('Principal'),
			'fieldtype': 'Currency',
			'width': 100
		},

		{
			'fieldname': 'date_loan_granted',
			'label': _('Date Loan Granted'),
			'fieldtype': 'Date',
			'width': 200
		},

		{
			'fieldname': 'expiry_date',
			'label': _('Expiry Date'),
			'fieldtype': 'Date',
			'width': 200
		},

		{
			'fieldname': 'workflow_state',
			'label': _('Status'),
			'fieldtype': 'Data',
			'width': 100
		},
	]
	return columns
