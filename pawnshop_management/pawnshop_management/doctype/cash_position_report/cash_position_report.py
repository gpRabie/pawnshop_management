# Copyright (c) 2022, Rabie Moses Santillan and contributors
# For license information, please see license.txt

import frappe
from frappe.utils import flt
from frappe.model.document import Document

class CashPositionReport(Document):
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
				row_values1.account = "Cash/Shortage Overage - Pawnshop - GTC - MPConso"
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
				row_values2.account = "Cash/Shortage Overage - Pawnshop - GTC - MPConso"
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
		