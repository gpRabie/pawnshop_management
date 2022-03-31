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
			doc1.company = 'TEST Garcia\'s Pawnshop'
			doc1.posting_date = self.date

			row_values1 = doc1.append('accounts', {})
			row_values1.account = "Cash Shortage/Overage - NJ - TGP"
			row_values1.debit_in_account_currency = flt(self.shortage_overage)
			row_values1.credit_in_account_currency = flt(0)

			row_values2 = doc1.append('accounts', {})
			row_values2.account = "Cash on Hand - Pawnshop - NJ - TGP"
			row_values2.debit_in_account_currency = flt(0)
			row_values2.credit_in_account_currency = flt(self.shortage_overage)

			doc1.save(ignore_permissions=True)
			doc1.submit()
		elif self.shortage_overage < 0:
			doc1 = frappe.new_doc('Journal Entry')
			doc1.voucher_type = 'Journal Entry'
			doc1.company = 'TEST Garcia\'s Pawnshop'
			doc1.posting_date = self.date

			row_values1 = doc1.append('accounts', {})
			row_values1.account = "Cash on Hand - Pawnshop - NJ - TGP"
			row_values1.debit_in_account_currency = flt(abs(self.shortage_overage))
			row_values1.credit_in_account_currency = flt(0)

			row_values2 = doc1.append('accounts', {})
			row_values2.account = "Cash Shortage/Overage - NJ - TGP"
			row_values2.debit_in_account_currency = flt(0)
			row_values2.credit_in_account_currency = flt(abs(self.shortage_overage))

			doc1.save(ignore_permissions=True)
			doc1.submit()