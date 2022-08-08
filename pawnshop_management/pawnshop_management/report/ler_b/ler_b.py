# Copyright (c) 2013, Rabie Moses Santillan and contributors
# For license information, please see license.txt

import frappe

def execute(filters=None):
	columns, data = [], []
	columns = get_columns()
	data1 = frappe.get_all("Pawn Ticket Jewelry", filters={'item_series': 'B', 'docstatus': 1}, fields=['pawn_ticket', 'date_loan_granted', 'customers_full_name', 'pawn_ticket', 'desired_principal', 'interest', 'net_proceeds'])
	for i in range(len(data)):
		description = ""
		details = frappe.db.get_list("Jewelry List", filters={'parent': data[i]['pawn_ticket']}, fields=['item_no', 'type', 'karat_category', 'karat', 'weight', 'color'])
		for j in range(len(details)):
			description += details[j]["item_no"] + ", " + details[j]["type"] + ", " + details[j]["karat_category"] + ", " + details[j]["karat"] + ", " + str(details[j]["weight"]) + ", " + details[j]["color"] + "; "
		data[i]['description'] = description
	return columns, data


def get_data():
	data = """
		SELECT 
			`tabPawn Ticket Jewelry`.`date_loan_granted` as "Date:Date/Date:200"

	"""

def get_columns():
	columns = [
		{
			'fieldname': 'date_loan_granted',
			'label': _('Date'),
			'fieldtype': 'Date',
			'width': 120
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

		# {
		# 	'fieldname': 'or',
		# 	'label': _('OR'),
		# 	'fieldtype': 'Link',
		# 	'options': 'Pawn Ticket Non Jewelry',
		# 	'width': 100
		# },

		{
			'fieldname': 'description',
			'label': _('Description of Items'),
			'fieldtype': 'Small Text',
			'width': 300
		},

		{
			'fieldname': 'desired_principal',
			'label': _('Principal'),
			'fieldtype': 'Currency',
			'width': 120
		},

		{
			'fieldname': 'interest',
			'label': _('Advance Interest'),
			'fieldtype': 'Currency',
			'width': 120
		},

		{
			'fieldname': 'net_proceeds',
			'label': _('Cash On Hand'),
			'fieldtype': 'Currency',
			'width': 120
		}

	]
	return columns