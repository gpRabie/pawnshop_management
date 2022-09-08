# Copyright (c) 2022, Rabie Moses Santillan and contributors
# For license information, please see license.txt

import frappe
from frappe.utils import flt
from frappe.model.document import Document
from frappe.utils import today

class CashPositionReport(Document):
	def create_inventory_count_document(self):
		a_in_count_of_the_day = frappe.db.count('Pawn Ticket Jewelry', {'date_loan_granted': self.date ,'item_series': 'A', 'workflow_state': 'Active', 'branch': self.branch})
		a_renewed_count_of_the_day = frappe.db.count('Pawn Ticket Jewelry', {'change_status_date': self.date, 'workflow_state': 'Renewed', 'item_series': 'A', 'branch': self.branch})
		a_in_count = a_in_count_of_the_day - a_renewed_count_of_the_day
		a_out_count = frappe.db.count('Pawn Ticket Jewelry', {'change_status_date': self.date, 'workflow_state': 'Redeemed', 'item_series': 'A', 'branch': self.branch})
		a_pulled_out_of_the_day = frappe.db.count('Pawn Ticket Jewelry', {'change_status_date': self.date, 'item_series': 'A', 'workflow_state': 'Pulled Out', 'branch': self.branch})
		a_returned_of_the_day = frappe.db.count('Pawn Ticket Jewelry', {'change_status_date': self.date, 'item_series': 'A', 'workflow_state': 'Returned', 'branch': self.branch})
		a_total_active = frappe.db.count('Pawn Ticket Jewelry', {'date_loan_granted': ['<=', self.date], 'item_series': 'A', 'workflow_state': ['in', ['Active', 'Expired', 'Returned']], 'branch': self.branch})

		b_in_count_of_the_day = frappe.db.count('Pawn Ticket Jewelry', {'date_loan_granted': self.date ,'item_series': 'B', 'workflow_state': 'Active', 'branch': self.branch})
		b_renewed_count_of_the_day = frappe.db.count('Pawn Ticket Jewelry', {'change_status_date': self.date, 'workflow_state': 'Renewed', 'item_series': 'B', 'branch': self.branch})
		b_in_count = b_in_count_of_the_day - b_renewed_count_of_the_day
		b_out_count = frappe.db.count('Pawn Ticket Jewelry', {'change_status_date': self.date, 'workflow_state': 'Redeemed', 'item_series': 'B', 'branch': self.branch})
		b_pulled_out_of_the_day = frappe.db.count('Pawn Ticket Jewelry', {'change_status_date': self.date, 'item_series': 'B', 'workflow_state': 'Pulled Out', 'branch': self.branch})
		b_returned_of_the_day = frappe.db.count('Pawn Ticket Jewelry', {'change_status_date': self.date, 'item_series': 'B', 'workflow_state': 'Returned', 'branch': self.branch})
		b_total_active = frappe.db.count('Pawn Ticket Jewelry', {'date_loan_granted': ['<=', self.date], 'item_series': 'B', 'workflow_state': ['in', ['Active', 'Expired', 'Returned']], 'branch': self.branch})

		nj_in_count_of_the_day = frappe.db.count('Pawn Ticket Non Jewelry', {'date_loan_granted': self.date , 'workflow_state': 'Active', 'branch': self.branch})
		nj_renewed_count_of_the_day = frappe.db.count('Pawn Ticket Non Jewelry', {'change_status_date': self.date, 'workflow_state': 'Renewed', 'branch': self.branch})
		nj_in_count = nj_in_count_of_the_day - nj_renewed_count_of_the_day
		nj_out_count = frappe.db.count('Pawn Ticket Non Jewelry', {'change_status_date': self.date, 'workflow_state': 'Redeemed', 'branch': self.branch})
		nj_pulled_out_of_the_day = frappe.db.count('Pawn Ticket Non Jewelry', {'change_status_date': self.date, 'workflow_state': 'Pulled Out', 'branch': self.branch})
		nj_returned_of_the_day = frappe.db.count('Pawn Ticket Non Jewelry', {'change_status_date': self.date, 'workflow_state': 'Returned', 'branch': self.branch})
		nj_total_active = frappe.db.count('Pawn Ticket Non Jewelry', {'date_loan_granted': ['<=', self.date], 'workflow_state': ['in', ['Active', 'Expired', 'Returned']], 'branch': self.branch})

		invetory_count_doc = frappe.new_doc('Inventory Count')
		invetory_count_doc.date = self.date
		invetory_count_doc.branch = self.branch
		invetory_count_doc.in_count_a = a_in_count
		invetory_count_doc.out_count_a = a_out_count
		invetory_count_doc.returned_a = a_returned_of_the_day
		invetory_count_doc.pulled_out_a = a_pulled_out_of_the_day
		invetory_count_doc.total_a = a_total_active

		invetory_count_doc.in_count_b = b_in_count
		invetory_count_doc.out_count_b = b_out_count
		invetory_count_doc.returned_b = b_returned_of_the_day
		invetory_count_doc.pulled_out_b = b_pulled_out_of_the_day
		invetory_count_doc.total_b = b_total_active

		invetory_count_doc.in_count_nj = nj_in_count
		invetory_count_doc.out_count_nj = nj_out_count
		invetory_count_doc.returned_nj = nj_returned_of_the_day
		invetory_count_doc.pulled_out_nj = nj_pulled_out_of_the_day
		invetory_count_doc.total_nj = nj_total_active
		invetory_count_doc.save(ignore_permissions=True)
# Added Comment
	def before_save(self):
		if self.shortage_overage > 0:
			doc1 = frappe.new_doc('Journal Entry')
			doc1.voucher_type = 'Journal Entry'
			doc1.company = 'MP Consolidated'
			doc1.posting_date = self.date
			doc1.reference_doctype = "Cash Position Report"
			doc1.reference_document = self.name

			row_values1 = doc1.append('accounts', {})
			if self.branch == "Garcia's Pawnshop - CC":
				row_values1.account = "Cash/Shortage Overage - Pawnshop - CC - MPConso"
			elif self.branch == "Garcia's Pawnshop - GTC":
				row_values1.account = "5300-002 - Cash Shortage / Overage - Pawnshop - GTC - MPConso"
				row_values1.branch = "Garcia's Pawnshop - GTC"
				row_values1.cost_center = "4 - Gen. Trias - MPConso"
			elif self.branch == "Garcia's Pawnshop - MOL":
				row_values1.account = "Cash/Shortage Overage - Pawnshop - MOL - MPConso"
			elif self.branch == "Garcia's Pawnshop - POB":
				row_values1.account = "Cash/Shortage Overage - Pawnshop - POB - MPConso"
			elif self.branch == "Garcia's Pawnshop - TNZ":
				row_values1.account = "Cash/Shortage Overage - Pawnshop - TNZ - MPConso"
			elif self.branch == "Rabie's House":
				row_values1.account = "Cash/Shortage Overage - Pawnshop - CC - MPConso"
			row_values1.debit_in_account_currency = flt(self.shortage_overage)
			row_values1.credit_in_account_currency = flt(0)

			row_values2 = doc1.append('accounts', {})
			if self.branch == "Garcia's Pawnshop - CC":
				row_values2.account = "1110-001 - Cash on Hand - Pawnshop - CC - MPConso"
			elif self.branch == "Garcia's Pawnshop - GTC":
				row_values2.account = "1110-002 - Cash on Hand - Pawnshop - GTC - MPConso"
				row_values2.branch = "Garcia's Pawnshop - GTC"
				row_values2.cost_center = "4 - Gen. Trias - MPConso"
			elif self.branch == "Garcia's Pawnshop - MOL":
				row_values2.account = "1110-003 - Cash on Hand - Pawnshop - MOL - MPConso"
			elif self.branch == "Garcia's Pawnshop - POB":
				row_values2.account = "1110-004 - Cash on Hand - Pawnshop - POB - MPConso"
			elif self.branch == "Garcia's Pawnshop - TNZ":
				row_values2.account = "1110-005 - Cash on Hand - Pawnshop - TNZ - MPConso"
			elif self.branch == "Rabie's House":
				row_values2.account = "1110-001 - Cash on Hand - Pawnshop - CC - MPConso"
			row_values2.debit_in_account_currency = flt(0)
			row_values2.credit_in_account_currency = flt(self.shortage_overage)

			doc1.save(ignore_permissions=True)
			doc1.submit()
		elif self.shortage_overage < 0:
			doc1 = frappe.new_doc('Journal Entry')
			doc1.voucher_type = 'Journal Entry'
			doc1.company = 'MP Consolidated'
			doc1.posting_date = self.date
			doc1.reference_doctype = "Cash Position Report"
			doc1.reference_document = self.name

			row_values1 = doc1.append('accounts', {})
			if self.branch == "Garcia's Pawnshop - CC":
				row_values1.account = "1110-001 - Cash on Hand - Pawnshop - CC - MPConso"
			elif self.branch == "Garcia's Pawnshop - GTC":
				row_values1.account = "1110-002 - Cash on Hand - Pawnshop - GTC - MPConso"
				row_values1.branch = "Garcia's Pawnshop - GTC"
				row_values1.cost_center = "4 - Gen. Trias - MPConso"
			elif self.branch == "Garcia's Pawnshop - MOL":
				row_values1.account = "1110-003 - Cash on Hand - Pawnshop - MOL - MPConso"
			elif self.branch == "Garcia's Pawnshop - POB":
				row_values1.account = "1110-004 - Cash on Hand - Pawnshop - POB - MPConso"
			elif self.branch == "Garcia's Pawnshop - TNZ":
				row_values1.account = "1110-005 - Cash on Hand - Pawnshop - TNZ - MPConso"
			elif self.branch == "Rabie's House":
				row_values1.account = "1110-001 - Cash on Hand - Pawnshop - CC - MPConso"
			row_values1.debit_in_account_currency = flt(0)
			row_values1.credit_in_account_currency = flt(abs(self.shortage_overage))

			row_values2 = doc1.append('accounts', {})
			if self.branch == "Garcia's Pawnshop - CC":
				row_values2.account = "Cash/Shortage Overage - Pawnshop - CC - MPConso"
			elif self.branch == "Garcia's Pawnshop - GTC":
				row_values2.account = "5300-002 - Cash Shortage / Overage - Pawnshop - GTC - MPConso"
				row_values2.branch = "Garcia's Pawnshop - GTC"
				row_values2.cost_center = "4 - Gen. Trias - MPConso"
			elif self.branch == "Garcia's Pawnshop - MOL":
				row_values2.account = "Cash/Shortage Overage - Pawnshop - MOL - MPConso"
			elif self.branch == "Garcia's Pawnshop - POB":
				row_values2.account = "Cash/Shortage Overage - Pawnshop - POB - MPConso"
			elif self.branch == "Garcia's Pawnshop - TNZ":
				row_values2.account = "Cash/Shortage Overage - Pawnshop - TNZ - MPConso"
			elif self.branch == "Rabie's House":
				row_values2.account = "Cash/Shortage Overage - Pawnshop - CC - MPConso"
			row_values2.debit_in_account_currency = flt(abs(self.shortage_overage))
			row_values2.credit_in_account_currency = flt(0)

			doc1.save(ignore_permissions=True)
			doc1.submit()
		self.create_inventory_count_document()

			