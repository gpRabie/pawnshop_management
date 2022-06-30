# Copyright (c) 2022, Rabie Moses Santillan and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import flt

class PawnTicketJewelry(Document):
	def before_save(self):
		if frappe.db.exists('Pawn Ticket Jewelry', self.name) == None:
			if self.amended_from == None:
				if self.branch == "Garcia's Pawnshop - CC":
					settings = frappe.get_doc('Pawnshop Naming Series', "Garcia's Pawnshop - CC")
					if self.item_series == 'A':
						settings.a_series += 1
					elif self.item_series == 'B':
						settings.b_series += 1
					settings.save(ignore_permissions=True)
				elif self.branch == "Garcia's Pawnshop - GTC":
					settings = frappe.get_doc('Pawnshop Naming Series', "Garcia's Pawnshop - GTC")
					if self.item_series == 'A':
						settings.a_series += 1
					elif self.item_series == 'B':
						settings.b_series += 1
					settings.save(ignore_permissions=True)
				elif self.branch == "Garcia's Pawnshop - MOL":
					settings = frappe.get_doc('Pawnshop Naming Series', "Garcia's Pawnshop - MOL")
					if self.item_series == 'A':
						settings.a_series += 1
					elif self.item_series == 'B':
						settings.b_series += 1
					settings.save(ignore_permissions=True)
				elif self.branch == "Garcia's Pawnshop - POB":
					settings = frappe.get_doc('Pawnshop Naming Series', "Garcia's Pawnshop - POB")
					if self.item_series == 'A':
						settings.a_series += 1
					elif self.item_series == 'B':
						settings.b_series += 1
					settings.save(ignore_permissions=True)
				elif self.branch == "Garcia's Pawnshop - TNZ":
					settings = frappe.get_doc('Pawnshop Naming Series', "Garcia's Pawnshop - TNZ")
					if self.item_series == 'A':
						settings.a_series += 1
					elif self.item_series == 'B':
						settings.b_series += 1
					settings.save(ignore_permissions=True)
				elif self.branch == "Rabie's House":
					settings = frappe.get_doc('Pawnshop Naming Series', "Rabie's House")
					if self.item_series == 'A':
						settings.a_series += 1
					elif self.item_series == 'B':
						settings.b_series += 1
					settings.save(ignore_permissions=True)

	def on_submit(self):
		if frappe.db.exists('Jewelry Batch', self.inventory_tracking_no) != self.inventory_tracking_no: #Copies Items table from pawnt ticket to non jewelry batch doctype
			new_jewelry_batch = frappe.new_doc('Jewelry Batch')
			new_jewelry_batch.inventory_tracking_no = self.inventory_tracking_no
			new_jewelry_batch.branch = self.branch
			items = self.jewelry_items
			for i in range(len(items)):
				new_jewelry_batch.append('items', {
					"item_no": items[i].item_no,
					"type": items[i].type,
					"karat_category": items[i].karat_category,
					"karat": items[i].karat,
					"weight": items[i].weight,
					"color": items[i].color,
					"colors_if_multi": items[i].colors_if_multi,
					"additional_for_stone": items[i].additional_for_stone,
					"suggested_appraisal_value": items[i].suggested_appraisal_value,
					"desired_principal": items[i].desired_principal,
					"comments": items[i].comments
				})
			new_jewelry_batch.save(ignore_permissions=True)

		# Journal Entry for Pawn Ticket Jewelry
		doc1 = frappe.new_doc('Journal Entry')
		doc1.voucher_type = 'Journal Entry'
		doc1.company = 'MP Consolidated'
		doc1.posting_date = self.date_loan_granted
		doc1.reference_doctype = "Pawn Ticket Jewelry"
		doc1.reference_document = self.name
		doc1.document_status = "New Sangla"

		row_values1 = doc1.append('accounts', {})
		if self.branch == "Garcia's Pawnshop - CC":
			row_values1.account = "1610-001 - Pawned Items Inventory - J - CC - MPConso"
		elif self.branch == "Garcia's Pawnshop - GTC":
			row_values1.account = "1610-002 - Pawned Items Inventory - J - GTC - MPConso"
		elif self.branch == "Garcia's Pawnshop - MOL":
			row_values1.account = "1610-003 - Pawned Items Inventory - J - MOL - MPConso"
		elif self.branch == "Garcia's Pawnshop - POB":
			row_values1.account = "1610-004 - Pawned Items Inventory - J - POB - MPConso"
		elif self.branch == "Garcia's Pawnshop - TNZ":
			row_values1.account = "1610-005 - Pawned Items Inventory - J - TNZ - MPConso"
		elif self.branch == "Rabie's House":
			row_values1.account = "1610-001 - Pawned Items Inventory - J - CC - MPConso"
		row_values1.debit_in_account_currency = flt(self.desired_principal)
		row_values1.credit_in_account_currency = flt(0)

		row_values2 = doc1.append('accounts', {})
		if self.branch == "Garcia's Pawnshop - CC":
			row_values2.account = "4112-001 - Interest on Past Due Loans - J - CC - MPConso"
		elif self.branch == "Garcia's Pawnshop - GTC":
			row_values2.account = "4112-002 - Interest on Past Due Loans - J - GTC - MPConso"
		elif self.branch == "Garcia's Pawnshop - MOL":
			row_values2.account = "4112-003 - Interest on Past Due Loans - J - MOL - MPConso"
		elif self.branch == "Garcia's Pawnshop - POB":
			row_values2.account = "4112-004 - Interest on Past Due Loans - J - POB - MPConso"
		elif self.branch == "Garcia's Pawnshop - TNZ":
			row_values2.account = "4112-005 - Interest on Past Due Loans - J - TNZ - MPConso"
		elif self.branch == "Rabie's House":
			row_values2.account = "4112-001 - Interest on Past Due Loans - J - CC - MPConso"
		row_values2.debit_in_account_currency = flt(0)
		row_values2.credit_in_account_currency = flt(self.interest)

		row_values3 = doc1.append('accounts', {})
		if self.branch == "Garcia's Pawnshop - CC":
			row_values3.account = "1110-001 - Cash on Hand - Pawnshop - CC - MPConso"
		elif self.branch == "Garcia's Pawnshop - GTC":
			row_values3.account = "1110-002 - Cash on Hand - Pawnshop - GTC - MPConso"
		elif self.branch == "Garcia's Pawnshop - MOL":
			row_values3.account = "1110-003 - Cash on Hand - Pawnshop - MOL - MPConso"
		elif self.branch == "Garcia's Pawnshop - POB":
			row_values3.account = "1110-004 - Cash on Hand - Pawnshop - POB - MPConso"
		elif self.branch == "Garcia's Pawnshop - TNZ":
			row_values3.account = "1110-005 - Cash on Hand - Pawnshop - TNZ - MPConso"
		elif self.branch == "Rabie's House":
			row_values3.account = "1110-001 - Cash on Hand - Pawnshop - CC - MPConso"
		row_values3.debit_in_account_currency = flt(0)
		row_values3.credit_in_account_currency = flt(self.net_proceeds)
		
		doc1.save(ignore_permissions=True)

	def before_cancel(self):
		name = frappe.db.get_value('Journal Entry', {'reference_document': self.name, "document_status": "Active"}, 'name')
		frappe.db.set_value('Journal Entry', name, 'docstatus', 2)
		frappe.db.commit()

