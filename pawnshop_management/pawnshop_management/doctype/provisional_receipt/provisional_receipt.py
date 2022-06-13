# Copyright (c) 2022, Rabie Moses Santillan and contributors
# For license information, please see license.txt

from datetime import datetime
from pydoc import Doc, doc
from frappe.utils import add_to_date, today
import frappe
from frappe.model.document import Document
from frappe.utils import flt

class ProvisionalReceipt(Document):
	def before_submit(self):
		if self.transaction_type == "Redemption":
			frappe.db.set_value(self.pawn_ticket_type, self.pawn_ticket_no, 'workflow_state', 'Redeemed')
			frappe.db.commit()
			doc = frappe.get_doc(self.pawn_ticket_type, self.pawn_ticket_no)
			if self.pawn_ticket_type == 'Pawn Ticket Non Jewelry':
				for items in doc.get('non_jewelry_items'):
					frappe.db.set_value('Non Jewelry Items', items.item_no, 'workflow_state', 'Redeemed')
					frappe.db.commit()
			elif self.pawn_ticket_type == 'Pawn Ticket Jewelry':
				for items in doc.get('jewelry_items'):
					frappe.db.set_value('Jewelry Items', items.item_no, 'workflow_state', 'Redeemed')
					frappe.db.commit()
		elif self.transaction_type == "Amortization":
			self.amortization += self.additional_amortization

		if self.transaction_type == "Renewal":
			frappe.db.set_value(self.pawn_ticket_type, self.pawn_ticket_no, 'workflow_state', 'Renewed')
			frappe.db.commit()
			if self.pawn_ticket_no != "":
				frappe.db.set_value(self.pawn_ticket_type, self.pawn_ticket_no, 'change_status_date', today())
				frappe.db.commit()
		elif self.transaction_type == "Redemption":
			frappe.db.set_value(self.pawn_ticket_type, self.pawn_ticket_no, 'workflow_state', 'Redeemed')
			frappe.db.commit()
			if self.pawn_ticket_no != "":
				frappe.db.set_value(self.pawn_ticket_type, self.pawn_ticket_no, 'change_status_date', today())
				frappe.db.commit()
		elif self.transaction_type == "Renewal w/ Amortization":
			frappe.db.set_value(self.pawn_ticket_type, self.pawn_ticket_no, 'workflow_state', 'Renewed')
			frappe.db.commit()
			if self.pawn_ticket_no != "":
				frappe.db.set_value(self.pawn_ticket_type, self.pawn_ticket_no, 'change_status_date', today())
				frappe.db.commit()

	def on_submit(self):
		if self.transaction_type == "Renewal": # Create New Pawn Ticket
			previous_pawn_ticket = frappe.get_doc(self.pawn_ticket_type, self.pawn_ticket_no)
			new_pawn_ticket = frappe.new_doc(self.pawn_ticket_type)
			new_pawn_ticket.pawn_ticket = self.new_pawn_ticket_no
			new_pawn_ticket.branch = self.branch
			new_pawn_ticket.series = previous_pawn_ticket.item_series
			new_pawn_ticket.date_loan_granted = self.date_issued
			new_pawn_ticket.maturity_date = add_to_date(self.date_issued, days=30)
			new_pawn_ticket.expiry_date = add_to_date(self.date_issued, days=120)
			new_pawn_ticket.customers_tracking_no = previous_pawn_ticket.customers_tracking_no
			new_pawn_ticket.customers_full_name = previous_pawn_ticket.customers_full_name
			new_pawn_ticket.inventory_tracking_no = previous_pawn_ticket.inventory_tracking_no
			if self.pawn_ticket_type == "Pawn Ticket Non Jewelry":
				previous_items = previous_pawn_ticket.non_jewelry_items
				for i in range(len(previous_items)):
					new_pawn_ticket.append("non_jewelry_items", {
						"item_no": previous_items[i].item_no,
						"type": previous_items[i].type,
						"brand": previous_items[i].brand,
						"model": previous_items[i].model,
						"model_number": previous_items[i].model_number,
						"suggested_appraisal_value": previous_items[i].suggested_appraisal_value
					})
			elif self.pawn_ticket_type == "Pawn Ticket Jewelry":
				previous_items = previous_pawn_ticket.jewelry_items
				for i in range(len(previous_items)):
					new_pawn_ticket.append("jewelry_items", {
						"item_no": previous_items[i].item_no,
						"type": previous_items[i].type,
						"karat_category": previous_items[i].karat_category,
						"karat": previous_items[i].karat,
						"weight": previous_items[i].weight,
						"color": previous_items[i].color,
						"colors_if_multi": previous_items[i].colors_if_multi,
						"additional_for_stone": previous_items[i].additional_for_stone,
						"suggested_appraisal_value": previous_items[i].suggested_appraisal_value,
						"desired_principal": previous_items[i].desired_principal,
						"comments": previous_items[i].comments
					})
			new_pawn_ticket.desired_principal = previous_pawn_ticket.desired_principal
			new_pawn_ticket.interest = previous_pawn_ticket.interest
			new_pawn_ticket.net_proceeds = previous_pawn_ticket.net_proceeds
			new_pawn_ticket.save(ignore_permissions=True)
			new_pawn_ticket.submit()

		elif self.transaction_type == "Amortization":
			interest_rate = frappe.get_doc('Pawnshop Management Settings')
			if self.pawn_ticket_type == "Pawn Ticket Non Jewelry":
				desired_principal = self.principal_amount - self.additional_amortization
				interest = desired_principal * (interest_rate.gadget_interest_rate/100)
				net_proceeds = desired_principal - interest
				frappe.db.set_value(self.pawn_ticket_type, self.pawn_ticket_no, {
					'desired_principal': desired_principal,
					'interest': interest,
					'net_proceeds': net_proceeds
				})
				frappe.db.commit()

			elif self.pawn_ticket_type == "Pawn Ticket Jewelry":
				desired_principal = self.principal_amount - self.additional_amortization
				interest = desired_principal * (interest_rate.jewelry_interest_rate/100)
				net_proceeds = desired_principal - interest
				frappe.db.set_value(self.pawn_ticket_type, self.pawn_ticket_no, {
					'desired_principal': desired_principal,
					'interest': interest,
					'net_proceeds': net_proceeds
				})
				frappe.db.commit()
		elif self.transaction_type == "Renewal w/ Amortization":
			previous_pawn_ticket = frappe.get_doc(self.pawn_ticket_type, self.pawn_ticket_no)
			new_pawn_ticket = frappe.new_doc(self.pawn_ticket_type)
			new_pawn_ticket.pawn_ticket = self.new_pawn_ticket_no
			new_pawn_ticket.branch = self.branch
			new_pawn_ticket.series = previous_pawn_ticket.item_series
			new_pawn_ticket.date_loan_granted = self.date_issued
			new_pawn_ticket.maturity_date = add_to_date(self.date_issued, days=30)
			new_pawn_ticket.expiry_date = add_to_date(self.date_issued, days=120)
			new_pawn_ticket.customers_tracking_no = previous_pawn_ticket.customers_tracking_no
			new_pawn_ticket.customers_full_name = previous_pawn_ticket.customers_full_name
			new_pawn_ticket.inventory_tracking_no = previous_pawn_ticket.inventory_tracking_no
			if self.pawn_ticket_type == "Pawn Ticket Non Jewelry":
				previous_items = previous_pawn_ticket.non_jewelry_items
				for i in range(len(previous_items)):
					new_pawn_ticket.append("non_jewelry_items", {
						"item_no": previous_items[i].item_no,
						"type": previous_items[i].type,
						"brand": previous_items[i].brand,
						"model": previous_items[i].model,
						"model_number": previous_items[i].model_number,
						"suggested_appraisal_value": previous_items[i].suggested_appraisal_value
					})
			elif self.pawn_ticket_type == "Pawn Ticket Jewelry":
				previous_items = previous_pawn_ticket.jewelry_items
				for i in range(len(previous_items)):
					new_pawn_ticket.append("jewelry_items", {
						"item_no": previous_items[i].item_no,
						"type": previous_items[i].type,
						"karat_category": previous_items[i].karat_category,
						"karat": previous_items[i].karat,
						"weight": previous_items[i].weight,
						"color": previous_items[i].color,
						"colors_if_multi": previous_items[i].colors_if_multi,
						"additional_for_stone": previous_items[i].additional_for_stone,
						"suggested_appraisal_value": previous_items[i].suggested_appraisal_value,
						"desired_principal": previous_items[i].desired_principal,
						"comments": previous_items[i].comments
					})
			new_pawn_ticket.desired_principal = self.principal_amount - self.additional_amortization
			new_pawn_ticket.interest = self.advance_interest
			new_pawn_ticket.net_proceeds = self.principal_amount - self.additional_amortization - self.advance_interest
			new_pawn_ticket.save(ignore_permissions=True)
			new_pawn_ticket.submit()
			



		# For Journal Entry Creation NJ
		if self.pawn_ticket_type == "Pawn Ticket Non Jewelry":
			# For Cash Accounts
			if self.transaction_type == "Renewal" and self.mode_of_payment == "Cash":			
				doc1 = frappe.new_doc('Journal Entry')
				doc1.voucher_type = 'Journal Entry'
				doc1.company = 'TEST Garcia\'s Pawnshop'
				doc1.posting_date = self.date_issued
				doc1.reference_doctype = "Provisional Receipt"
				doc1.reference_document = self.name
				doc1.document_status = "Renewal"

				row_values1 = doc1.append('accounts', {})
				row_values1.account = "Cash on Hand - Pawnshop - TGP"
				row_values1.debit_in_account_currency = flt(self.total)
				row_values1.credit_in_account_currency = flt(0)
				if self.interest_payment > 0:
					row_values2 = doc1.append('accounts', {})
					row_values2.account = "Interest on Past Due Loans - NJ - TGP"
					row_values2.debit_in_account_currency = flt(0)
					row_values2.credit_in_account_currency = flt(self.interest_payment)

				if flt(self.discount) > 0:
					row_values4 = doc1.append('accounts', {})
					row_values4.account = "Discount - NJ - TGP"
					row_values4.debit_in_account_currency = flt(self.discount)
					row_values4.credit_in_account_currency = flt(0)

				row_values3 = doc1.append('accounts', {})
				row_values3.account = "Interest on Loans and Advances - NJ - TGP"
				row_values3.debit_in_account_currency = flt(0)
				row_values3.credit_in_account_currency = flt(self.advance_interest)

				doc1.save(ignore_permissions=True)
				doc1.submit()

			elif self.transaction_type == "Redemption" and self.mode_of_payment == "Cash":
				doc1 = frappe.new_doc('Journal Entry')
				doc1.voucher_type = 'Journal Entry'
				doc1.company = 'TEST Garcia\'s Pawnshop'
				doc1.posting_date = self.date_issued
				doc1.reference_doctype = "Provisional Receipt"
				doc1.reference_document = self.name
				doc1.document_status = "Redemption"

				row_values1 = doc1.append('accounts', {})
				row_values1.account = "Cash on Hand - Pawnshop - TGP"
				row_values1.debit_in_account_currency = flt(self.total)
				row_values1.credit_in_account_currency = flt(0)

				if flt(self.interest_payment) > 0:
					row_values2 = doc1.append('accounts', {})
					row_values2.account = "Interest on Past Due Loans - NJ - TGP"
					row_values2.debit_in_account_currency = flt(0)
					row_values2.credit_in_account_currency = flt(self.interest_payment)

				if flt(self.discount) > 0:
					row_values4 = doc1.append('accounts', {})
					row_values4.account = "Discount - NJ - TGP"
					row_values4.debit_in_account_currency = flt(self.discount)
					row_values4.credit_in_account_currency = flt(0)

				row_values3 = doc1.append('accounts', {})
				row_values3.account = "Pawned Items Inventory - NJ - TGP"
				row_values3.debit_in_account_currency = flt(0)
				row_values3.credit_in_account_currency = flt(self.principal_amount)

				doc1.save(ignore_permissions=True)
				doc1.submit()

			elif self.transaction_type == "Amortization" and self.mode_of_payment == "Cash":
				doc1 = frappe.new_doc('Journal Entry')
				doc1.voucher_type = 'Journal Entry'
				doc1.company = 'TEST Garcia\'s Pawnshop'
				doc1.posting_date = self.date_issued
				doc1.reference_doctype = "Provisional Receipt"
				doc1.reference_document = self.name
				doc1.document_status = "Amortization"

				row_values1 = doc1.append('accounts', {})
				row_values1.account = "Cash on Hand - Pawnshop - TGP"
				row_values1.debit_in_account_currency = flt(self.total)
				row_values1.credit_in_account_currency = flt(0)

				if self.interest_payment > 0:
					row_values2 = doc1.append('accounts', {})
					row_values2.account = "Interest on Past Due Loans - NJ - TGP"
					row_values2.debit_in_account_currency = flt(0)
					row_values2.credit_in_account_currency = flt(self.interest_payment)

				row_values3 = doc1.append('accounts', {})
				row_values3.account = "Pawned Items Inventory - NJ - TGP"
				row_values3.debit_in_account_currency = flt(0)
				row_values3.credit_in_account_currency = flt(self.total)

				doc1.save(ignore_permissions=True)
				doc1.submit()

			elif self.transaction_type == "Renewal w/ Amortization" and self.mode_of_payment == "Cash":
				doc1 = frappe.new_doc('Journal Entry')
				doc1.voucher_type = 'Journal Entry'
				doc1.company = 'TEST Garcia\'s Pawnshop'
				doc1.posting_date = self.date_issued
				doc1.reference_doctype = "Provisional Receipt"
				doc1.reference_document = self.name
				doc1.document_status = "Renewal w/ Amortization"

				row_values1 = doc1.append('accounts', {})
				row_values1.account = "Cash on Hand - Pawnshop - TGP"
				row_values1.debit_in_account_currency = flt(self.total)
				row_values1.credit_in_account_currency = flt(0)
				
				if self.interest_payment > 0:
					row_values2 = doc1.append('accounts', {})
					row_values2.account = "Interest on Past Due Loans - NJ - TGP"
					row_values2.debit_in_account_currency = flt(0)
					row_values2.credit_in_account_currency = flt(self.interest_payment)
				
				row_values3 = doc1.append('accounts', {})
				row_values3.account = "Interest on Loans and Advances - NJ - TGP"
				row_values3.debit_in_account_currency = flt(0)
				row_values3.credit_in_account_currency = flt(self.advance_interest)

				row_values4 = doc1.append('accounts', {})
				row_values4.account = "Pawned Items Inventory - NJ - TGP"
				row_values4.debit_in_account_currency = flt(0)
				row_values4.credit_in_account_currency = flt(self.additional_amortization)

				if flt(self.discount) > 0:
					row_values4 = doc1.append('accounts', {})
					row_values4.account = "Discount - NJ - TGP"
					row_values4.debit_in_account_currency = flt(self.discount)
					row_values4.credit_in_account_currency = flt(0)

				doc1.save(ignore_permissions=True)
				doc1.submit()
				
			elif self.transaction_type == "Interest Payment" and self.mode_of_payment == "Cash":
				doc1 = frappe.new_doc('Journal Entry')
				doc1.voucher_type = 'Journal Entry'
				doc1.company = 'TEST Garcia\'s Pawnshop'
				doc1.posting_date = self.date_issued
				doc1.reference_doctype = "Provisional Receipt"
				doc1.reference_document = self.name
				doc1.document_status = "Interest Payment"

				row_values1 = doc1.append('accounts', {})
				row_values1.account = "Cash on Hand - Pawnshop - TGP"
				row_values1.debit_in_account_currency = flt(self.total)
				row_values1.credit_in_account_currency = flt(0)

				row_values2 = doc1.append('accounts', {})
				row_values2.account = "Interest on Past Due Loans - NJ - TGP"
				row_values2.debit_in_account_currency = flt(0)
				row_values2.credit_in_account_currency = flt(self.total)

				doc1.save(ignore_permissions=True)
				doc1.submit()

			# For GCash Accounts
			elif self.transaction_type == "Renewal" and self.mode_of_payment == "GCash":			
				doc1 = frappe.new_doc('Journal Entry')
				doc1.voucher_type = 'Journal Entry'
				doc1.company = 'TEST Garcia\'s Pawnshop'
				doc1.posting_date = self.date_issued
				doc1.reference_doctype = "Provisional Receipt"
				doc1.reference_document = self.name
				doc1.document_status = "Renewal"

				row_values1 = doc1.append('accounts', {})
				row_values1.account = "Cash in Bank - EW Cavite - J - TGP"
				row_values1.debit_in_account_currency = (flt(self.total) - (flt(self.total) * 0.02)) + (((flt(self.total) * 0.02) / 1.12) * 0.02)
				row_values1.credit_in_account_currency = flt(0)

				row_values2 = doc1.append('accounts', {})
				row_values2.account = "Merchant Fee - COS - Gcash - TGP"
				row_values2.debit_in_account_currency = (flt(self.total) * 0.02)
				row_values2.credit_in_account_currency = flt(0)

				if self.interest_payment > 0:
					row_values3 = doc1.append('accounts', {})
					row_values3.account = "Interest on Past Due Loans - J - TGP"
					row_values3.debit_in_account_currency = flt(0)
					row_values3.credit_in_account_currency = flt(self.interest_payment)

				if flt(self.discount) > 0:
					row_values6 = doc1.append('accounts', {})
					row_values6.account = "Discount - NJ - TGP"
					row_values6.debit_in_account_currency = flt(self.discount)
					row_values6.credit_in_account_currency = flt(0)
				
				row_values4 = doc1.append('accounts', {})
				row_values4.account = "Interest on Loans and Advances - NJ - TGP"
				row_values4.debit_in_account_currency = flt(0)
				row_values4.credit_in_account_currency = flt(self.advance_interest)
				
				row_values5 = doc1.append('accounts', {})
				row_values5.account = "Withholding Tax Payable - Expanded - TGP"
				row_values5.debit_in_account_currency = flt(0)
				row_values5.credit_in_account_currency = ((flt(self.total) * 0.02) / 1.12) * 0.02

				doc1.save(ignore_permissions=True)
				doc1.submit()

			elif self.transaction_type == "Redemption" and self.mode_of_payment == "GCash":
				doc1 = frappe.new_doc('Journal Entry')
				doc1.voucher_type = 'Journal Entry'
				doc1.company = 'TEST Garcia\'s Pawnshop'
				doc1.posting_date = self.date_issued
				doc1.reference_doctype = "Provisional Receipt"
				doc1.reference_document = self.name
				doc1.document_status = "Redemption"

				row_values1 = doc1.append('accounts', {})
				row_values1.account = "Cash in Bank - EW Cavite - NJ - TGP"
				row_values1.debit_in_account_currency = (flt(self.total) - (flt(self.total) * 0.02)) + (((flt(self.total) * 0.02) / 1.12) * 0.02)
				row_values1.credit_in_account_currency = flt(0)

				row_values2 = doc1.append('accounts', {})
				row_values2.account = "Merchant Fee - COS - Gcash - TGP"
				row_values2.debit_in_account_currency = (flt(self.total) * 0.02)
				row_values2.credit_in_account_currency = flt(0)

				if self.interest_payment > 0:
					row_values4 = doc1.append('accounts', {})
					row_values4.account = "Interest on Past Due Loans - NJ - TGP"
					row_values4.debit_in_account_currency = flt(0)
					row_values4.credit_in_account_currency = flt(self.interest_payment)

				if flt(self.discount) > 0:
					row_values7 = doc1.append('accounts', {})
					row_values7.account = "Discount - NJ - TGP"
					row_values7.debit_in_account_currency = flt(self.discount)
					row_values7.credit_in_account_currency = flt(0)

				row_values5 = doc1.append('accounts', {})
				row_values5.account = "Pawned Items Inventory - NJ - TGP"
				row_values5.debit_in_account_currency = flt(0)
				row_values5.credit_in_account_currency = flt(self.principal_amount)
				
				row_values6 = doc1.append('accounts', {})
				row_values6.account = "Withholding Tax Payable - Expanded - TGP"
				row_values6.debit_in_account_currency = flt(0)
				row_values6.credit_in_account_currency = ((flt(self.total) * 0.02) / 1.12) * 0.02

				doc1.save(ignore_permissions=True)
				doc1.submit()

			elif self.transaction_type == "Amortization" and self.mode_of_payment == "GCash":
				doc1 = frappe.new_doc('Journal Entry')
				doc1.voucher_type = 'Journal Entry'
				doc1.company = 'TEST Garcia\'s Pawnshop'
				doc1.posting_date = self.date_issued
				doc1.reference_doctype = "Provisional Receipt"
				doc1.reference_document = self.name
				doc1.document_status = "Amortization"

				row_values1 = doc1.append('accounts', {})
				row_values1.account = "Cash in Bank - EW Cavite - NJ - TGP"
				row_values1.debit_in_account_currency = (flt(self.total) - (flt(self.total) * 0.02)) + (((flt(self.total) * 0.02) / 1.12) * 0.02)
				row_values1.credit_in_account_currency = flt(0)

				row_values2 = doc1.append('accounts', {})
				row_values2.account = "Merchant Fee - COS - Gcash - TGP"
				row_values2.debit_in_account_currency = (flt(self.total) * 0.02)
				row_values2.credit_in_account_currency = flt(0)

				row_values5 = doc1.append('accounts', {})
				row_values5.account = "Pawned Items Inventory - NJ - TGP"
				row_values5.debit_in_account_currency = flt(0)
				row_values5.credit_in_account_currency = flt(self.total)

				row_values6 = doc1.append('accounts', {})
				row_values6.account = "Withholding Tax Payable - Expanded - TGP"
				row_values6.debit_in_account_currency = flt(0)
				row_values6.credit_in_account_currency = ((flt(self.total) * 0.02) / 1.12) * 0.02

				doc1.save(ignore_permissions=True)
				doc1.submit()

			elif self.transaction_type == "Renewal w/ Amortization" and self.mode_of_payment == "GCash":
				doc1 = frappe.new_doc('Journal Entry')
				doc1.voucher_type = 'Journal Entry'
				doc1.company = 'TEST Garcia\'s Pawnshop'
				doc1.posting_date = self.date_issued
				doc1.reference_doctype = "Provisional Receipt"
				doc1.reference_document = self.name
				doc1.document_status = "Renewal w/ Amortization"

				row_values1 = doc1.append('accounts', {})
				row_values1.account = "Cash in Bank - EW Cavite - NJ - TGP"
				row_values1.debit_in_account_currency = (flt(self.total) - (flt(self.total) * 0.02)) + (((flt(self.total) * 0.02) / 1.12) * 0.02)
				row_values1.credit_in_account_currency = flt(0)

				row_values2 = doc1.append('accounts', {})
				row_values2.account = "Merchant Fee - COS - Gcash - TGP"
				row_values2.debit_in_account_currency = (flt(self.total) * 0.02)
				row_values2.credit_in_account_currency = flt(0)

				if self.interest_payment > 0:
					row_values4 = doc1.append('accounts', {})
					row_values4.account = "Interest on Past Due Loans - NJ - TGP"
					row_values4.debit_in_account_currency = flt(0)
					row_values4.credit_in_account_currency = flt(self.interest_payment)

				row_values5 = doc1.append('accounts', {})
				row_values5.account = "Pawned Items Inventory - NJ - TGP"
				row_values5.debit_in_account_currency = flt(0)
				row_values5.credit_in_account_currency = flt(self.additional_amortization)

				row_values6 = doc1.append('accounts', {})
				row_values6.account = "Interest on Loans and Advances - NJ - TGP"
				row_values6.debit_in_account_currency = flt(0)
				row_values6.credit_in_account_currency = flt(self.advance_interest)

				row_values7 = doc1.append('accounts', {})
				row_values7.account = "Withholding Tax Payable - Expanded - TGP"
				row_values7.debit_in_account_currency = flt(0)
				row_values7.credit_in_account_currency = ((flt(self.total) * 0.02) / 1.12) * 0.02

				if flt(self.discount) > 0:
					row_values8 = doc1.append('accounts', {})
					row_values8.account = "Discount - NJ - TGP"
					row_values8.debit_in_account_currency = flt(self.discount)
					row_values8.credit_in_account_currency = flt(0)

				doc1.save(ignore_permissions=True)
				doc1.submit()
				
			elif self.transaction_type == "Interest Payment" and self.mode_of_payment == "GCash":
				doc1 = frappe.new_doc('Journal Entry')
				doc1.voucher_type = 'Journal Entry'
				doc1.company = 'TEST Garcia\'s Pawnshop'
				doc1.posting_date = self.date_issued
				doc1.reference_doctype = "Provisional Receipt"
				doc1.reference_document = self.name
				doc1.document_status = "Interest Payment"

				row_values1 = doc1.append('accounts', {})
				row_values1.account = "Cash in Bank - EW Cavite - NJ - TGP"
				row_values1.debit_in_account_currency = (flt(self.total) - (flt(self.total) * 0.02)) + (((flt(self.total) * 0.02) / 1.12) * 0.02)
				row_values1.credit_in_account_currency = flt(0)

				row_values2 = doc1.append('accounts', {})
				row_values2.account = "Merchant Fee - COS - Gcash - TGP"
				row_values2.debit_in_account_currency = (flt(self.total) * 0.02)
				row_values2.credit_in_account_currency = flt(0)

				row_values4 = doc1.append('accounts', {})
				row_values4.account = "Interest on Past Due Loans - NJ - TGP"
				row_values4.debit_in_account_currency = flt(0)
				row_values4.credit_in_account_currency = flt(self.total)

				row_values5 = doc1.append('accounts', {})
				row_values5.account = "Withholding Tax Payable - Expanded - TGP"
				row_values5.debit_in_account_currency = flt(0)
				row_values5.credit_in_account_currency = ((flt(self.total) * 0.02) / 1.12) * 0.02

				doc1.save(ignore_permissions=True)
				doc1.submit()
			
			# For Bank Transfer Transaction
			elif self.transaction_type == "Renewal" and self.mode_of_payment == "Bank Transfer":
				doc1 = frappe.new_doc('Journal Entry')
				doc1.voucher_type = 'Journal Entry'
				doc1.company = 'TEST Garcia\'s Pawnshop'
				doc1.posting_date = self.date_issued
				doc1.reference_doctype = "Provisional Receipt"
				doc1.reference_document = self.name
				doc1.document_status = "Renewal"

				row_values1 = doc1.append('accounts', {})
				if self.bank == "BDO":
					row_values1.account = "Cash in Bank - BDO - TGP"
				elif self.bank == "BPI":
					row_values1.account = "Cash in Bank - BPI - TGP"
				elif self.bank == "East West Cavite Branch":
					row_values1.account = "Cash in Bank - EW Cavite - NJ - TGP"
				row_values1.debit_in_account_currency = flt(self.total)
				row_values1.credit_in_account_currency = flt(0)
				if self.interest_payment > 0:
					row_values2 = doc1.append('accounts', {})
					row_values2.account = "Interest on Past Due Loans - NJ - TGP"
					row_values2.debit_in_account_currency = flt(0)
					row_values2.credit_in_account_currency = flt(self.interest_payment)

				row_values3 = doc1.append('accounts', {})
				row_values3.account = "Interest on Loans and Advances - NJ - TGP"
				row_values3.debit_in_account_currency = flt(0)
				row_values3.credit_in_account_currency = flt(self.advance_interest)

				if flt(self.discount) > 0:
					row_values4 = doc1.append('accounts', {})
					row_values4.account = "Discount - NJ - TGP"
					row_values4.debit_in_account_currency = flt(self.discount)
					row_values4.credit_in_account_currency = flt(0)

				doc1.save(ignore_permissions=True)
				doc1.submit()

			elif self.transaction_type == "Redemption" and self.mode_of_payment == "Bank Transfer":
				doc1 = frappe.new_doc('Journal Entry')
				doc1.voucher_type = 'Journal Entry'
				doc1.company = 'TEST Garcia\'s Pawnshop'
				doc1.posting_date = self.date_issued
				doc1.reference_doctype = "Provisional Receipt"
				doc1.reference_document = self.name
				doc1.document_status = "Redemption"

				row_values1 = doc1.append('accounts', {})
				if self.bank == "BDO":
					row_values1.account = "Cash in Bank - BDO - TGP"
				elif self.bank == "BPI":
					row_values1.account = "Cash in Bank - BPI - TGP"
				elif self.bank == "East West Cavite Branch":
					row_values1.account = "Cash in Bank - EW Cavite - NJ - TGP"
				row_values1.debit_in_account_currency = flt(self.total)
				row_values1.credit_in_account_currency = flt(0)

				if flt(self.interest_payment) > 0:
					row_values2 = doc1.append('accounts', {})
					row_values2.account = "Interest on Past Due Loans - NJ - TGP"
					row_values2.debit_in_account_currency = flt(0)
					row_values2.credit_in_account_currency = flt(self.interest_payment)

				row_values3 = doc1.append('accounts', {})
				row_values3.account = "Pawned Items Inventory - NJ - TGP"
				row_values3.debit_in_account_currency = flt(0)
				row_values3.credit_in_account_currency = flt(self.principal_amount)

				if flt(self.discount) > 0:
					row_values4 = doc1.append('accounts', {})
					row_values4.account = "Discount - NJ - TGP"
					row_values4.debit_in_account_currency = flt(self.discount)
					row_values4.credit_in_account_currency = flt(0)

				doc1.save(ignore_permissions=True)
				doc1.submit()

			elif self.transaction_type == "Amortization" and self.mode_of_payment == "Bank Transfer":
				doc1 = frappe.new_doc('Journal Entry')
				doc1.voucher_type = 'Journal Entry'
				doc1.company = 'TEST Garcia\'s Pawnshop'
				doc1.posting_date = self.date_issued
				doc1.reference_doctype = "Provisional Receipt"
				doc1.reference_document = self.name
				doc1.document_status = "Amortization"

				row_values1 = doc1.append('accounts', {})
				if self.bank == "BDO":
					row_values1.account = "Cash in Bank - BDO - TGP"
				elif self.bank == "BPI":
					row_values1.account = "Cash in Bank - BPI - TGP"
				elif self.bank == "East West Cavite Branch":
					row_values1.account = "Cash in Bank - EW Cavite - NJ - TGP"
				row_values1.debit_in_account_currency = flt(self.total)
				row_values1.credit_in_account_currency = flt(0)
				
				if self.interest_payment > 0:
					row_values2 = doc1.append('accounts', {})
					row_values2.account = "Interest on Past Due Loans - NJ - TGP"
					row_values2.debit_in_account_currency = flt(0)
					row_values2.credit_in_account_currency = flt(self.interest_payment)

				row_values3 = doc1.append('accounts', {})
				row_values3.account = "Pawned Items Inventory - NJ - TGP"
				row_values3.debit_in_account_currency = flt(0)
				row_values3.credit_in_account_currency = flt(self.total)

				doc1.save(ignore_permissions=True)
				doc1.submit()

			elif self.transaction_type == "Renewal w/ Amortization" and self.mode_of_payment == "Bank Transfer":
				doc1 = frappe.new_doc('Journal Entry')
				doc1.voucher_type = 'Journal Entry'
				doc1.company = 'TEST Garcia\'s Pawnshop'
				doc1.posting_date = self.date_issued
				doc1.reference_doctype = "Provisional Receipt"
				doc1.reference_document = self.name
				doc1.document_status = "Renewal w/ Amortization"

				row_values1 = doc1.append('accounts', {})
				if self.bank == "BDO":
					row_values1.account = "Cash in Bank - BDO - TGP"
				elif self.bank == "BPI":
					row_values1.account = "Cash in Bank - BPI - TGP"
				elif self.bank == "East West Cavite Branch":
					row_values1.account = "Cash in Bank - EW Cavite - NJ - TGP"
				row_values1.debit_in_account_currency = flt(self.total)
				row_values1.credit_in_account_currency = flt(0)
				
				if self.interest_payment > 0:
					row_values2 = doc1.append('accounts', {})
					row_values2.account = "Interest on Past Due Loans - NJ - TGP"
					row_values2.debit_in_account_currency = flt(0)
					row_values2.credit_in_account_currency = flt(self.interest_payment)

				row_values3 = doc1.append('accounts', {})
				row_values3.account = "Interest on Loans and Advances - NJ - TGP"
				row_values3.debit_in_account_currency = flt(0)
				row_values3.credit_in_account_currency = flt(self.advance_interest)

				row_values4 = doc1.append('accounts', {})
				row_values4.account = "Pawned Items Inventory - NJ - TGP"
				row_values4.debit_in_account_currency = flt(0)
				row_values4.credit_in_account_currency = flt(self.additional_amortization)

				if flt(self.discount) > 0:
					row_values5 = doc1.append('accounts', {})
					row_values5.account = "Discount - NJ - TGP"
					row_values5.debit_in_account_currency = flt(self.discount)
					row_values5.credit_in_account_currency = flt(0)

				doc1.save(ignore_permissions=True)
				doc1.submit()

			elif self.transaction_type == "Interest Payment" and self.mode_of_payment == "Bank Transfer":
				doc1 = frappe.new_doc('Journal Entry')
				doc1.voucher_type = 'Journal Entry'
				doc1.company = 'TEST Garcia\'s Pawnshop'
				doc1.posting_date = self.date_issued
				doc1.reference_doctype = "Provisional Receipt"
				doc1.reference_document = self.name
				doc1.document_status = "Interest Payment"

				row_values1 = doc1.append('accounts', {})
				if self.bank == "BDO":
					row_values1.account = "Cash in Bank - BDO - TGP"
				elif self.bank == "BPI":
					row_values1.account = "Cash in Bank - BPI - TGP"
				elif self.bank == "East West Cavite Branch":
					row_values1.account = "Cash in Bank - EW Cavite - NJ - TGP"
				row_values1.debit_in_account_currency = flt(self.total)
				row_values1.credit_in_account_currency = flt(0)
				
				row_values2 = doc1.append('accounts', {})
				row_values2.account = "Interest on Past Due Loans - NJ - TGP"
				row_values2.debit_in_account_currency = flt(0)
				row_values2.credit_in_account_currency = flt(self.total)

				doc1.save(ignore_permissions=True)
				doc1.submit()

		# Journal Entry Creation for Jewelry
		elif self.pawn_ticket_type == "Pawn Ticket Jewelry":  #Renewal Cash
			# For Cash Accounts
			if self.transaction_type == "Renewal" and self.mode_of_payment == "Cash":			
				doc1 = frappe.new_doc('Journal Entry')
				doc1.voucher_type = 'Journal Entry'
				doc1.company = 'TEST Garcia\'s Pawnshop'
				doc1.posting_date = self.date_issued
				doc1.reference_doctype = "Provisional Receipt"
				doc1.reference_document = self.name
				doc1.document_status = "Renewal"

				row_values1 = doc1.append('accounts', {})
				row_values1.account = "Cash on Hand - Pawnshop - TGP"
				row_values1.debit_in_account_currency = flt(self.total)
				row_values1.credit_in_account_currency = flt(0)
				if self.interest_payment > 0:
					row_values2 = doc1.append('accounts', {})
					row_values2.account = "Interest on Past Due Loans - J - TGP"
					row_values2.debit_in_account_currency = flt(0)
					row_values2.credit_in_account_currency = flt(self.interest_payment)

				if flt(self.discount) > 0:
					row_values4 = doc1.append('accounts', {})
					row_values4.account = "Discount - J - TGP"
					row_values4.debit_in_account_currency = flt(self.discount)
					row_values4.credit_in_account_currency = flt(0)

				row_values3 = doc1.append('accounts', {})
				row_values3.account = "Interest on Loans and Advances - J - TGP"
				row_values3.debit_in_account_currency = flt(0)
				row_values3.credit_in_account_currency = flt(self.advance_interest)

				doc1.save(ignore_permissions=True)
				doc1.submit()

			elif self.transaction_type == "Redemption" and self.mode_of_payment == "Cash":
				doc1 = frappe.new_doc('Journal Entry')
				doc1.voucher_type = 'Journal Entry'
				doc1.company = 'TEST Garcia\'s Pawnshop'
				doc1.posting_date = self.date_issued
				doc1.reference_doctype = "Provisional Receipt"
				doc1.reference_document = self.name
				doc1.document_status = "Redemption"

				row_values1 = doc1.append('accounts', {})
				row_values1.account = "Cash on Hand - Pawnshop - TGP"
				row_values1.debit_in_account_currency = flt(self.total)
				row_values1.credit_in_account_currency = flt(0)

				if flt(self.interest_payment) > 0:
					row_values2 = doc1.append('accounts', {})
					row_values2.account = "Interest on Past Due Loans - J - TGP"
					row_values2.debit_in_account_currency = flt(0)
					row_values2.credit_in_account_currency = flt(self.interest_payment)

				if flt(self.discount) > 0:
					row_values4 = doc1.append('accounts', {})
					row_values4.account = "Discount - J - TGP"
					row_values4.debit_in_account_currency = flt(self.discount)
					row_values4.credit_in_account_currency = flt(0)

				row_values3 = doc1.append('accounts', {})
				row_values3.account = "Pawned Items Inventory - J - TGP"
				row_values3.debit_in_account_currency = flt(0)
				row_values3.credit_in_account_currency = flt(self.principal_amount)

				doc1.save(ignore_permissions=True)
				doc1.submit()

			elif self.transaction_type == "Amortization" and self.mode_of_payment == "Cash":
				doc1 = frappe.new_doc('Journal Entry')
				doc1.voucher_type = 'Journal Entry'
				doc1.company = 'TEST Garcia\'s Pawnshop'
				doc1.posting_date = self.date_issued
				doc1.reference_doctype = "Provisional Receipt"
				doc1.reference_document = self.name
				doc1.document_status = "Amortization"

				row_values1 = doc1.append('accounts', {})
				row_values1.account = "Cash on Hand - Pawnshop - TGP"
				row_values1.debit_in_account_currency = flt(self.total)
				row_values1.credit_in_account_currency = flt(0)

				if self.interest_payment > 0:
					row_values2 = doc1.append('accounts', {})
					row_values2.account = "Interest on Past Due Loans - J - TGP"
					row_values2.debit_in_account_currency = flt(0)
					row_values2.credit_in_account_currency = flt(self.interest_payment)

				row_values3 = doc1.append('accounts', {})
				row_values3.account = "Pawned Items Inventory - J - TGP"
				row_values3.debit_in_account_currency = flt(0)
				row_values3.credit_in_account_currency = flt(self.total)

				doc1.save(ignore_permissions=True)
				doc1.submit()

			elif self.transaction_type == "Renewal w/ Amortization" and self.mode_of_payment == "Cash":
				doc1 = frappe.new_doc('Journal Entry')
				doc1.voucher_type = 'Journal Entry'
				doc1.company = 'TEST Garcia\'s Pawnshop'
				doc1.posting_date = self.date_issued
				doc1.reference_doctype = "Provisional Receipt"
				doc1.reference_document = self.name
				doc1.document_status = "Renewal w/ Amortization"

				row_values1 = doc1.append('accounts', {})
				row_values1.account = "Cash on Hand - Pawnshop - TGP"
				row_values1.debit_in_account_currency = flt(self.total)
				row_values1.credit_in_account_currency = flt(0)
				
				if self.interest_payment > 0:
					row_values2 = doc1.append('accounts', {})
					row_values2.account = "Interest on Past Due Loans - J - TGP"
					row_values2.debit_in_account_currency = flt(0)
					row_values2.credit_in_account_currency = flt(self.interest_payment)
				
				row_values3 = doc1.append('accounts', {})
				row_values3.account = "Interest on Loans and Advances - J - TGP"
				row_values3.debit_in_account_currency = flt(0)
				row_values3.credit_in_account_currency = flt(self.advance_interest)

				row_values4 = doc1.append('accounts', {})
				row_values4.account = "Pawned Items Inventory - J - TGP"
				row_values4.debit_in_account_currency = flt(0)
				row_values4.credit_in_account_currency = flt(self.additional_amortization)

				if flt(self.discount) > 0:
					row_values4 = doc1.append('accounts', {})
					row_values4.account = "Discount - J - TGP"
					row_values4.debit_in_account_currency = flt(self.discount)
					row_values4.credit_in_account_currency = flt(0)

				doc1.save(ignore_permissions=True)
				doc1.submit()
				
			elif self.transaction_type == "Interest Payment" and self.mode_of_payment == "Cash":
				doc1 = frappe.new_doc('Journal Entry')
				doc1.voucher_type = 'Journal Entry'
				doc1.company = 'TEST Garcia\'s Pawnshop'
				doc1.posting_date = self.date_issued
				doc1.reference_doctype = "Provisional Receipt"
				doc1.reference_document = self.name
				doc1.document_status = "Interest Payment"

				row_values1 = doc1.append('accounts', {})
				row_values1.account = "Cash on Hand - Pawnshop - TGP"
				row_values1.debit_in_account_currency = flt(self.total)
				row_values1.credit_in_account_currency = flt(0)

				row_values2 = doc1.append('accounts', {})
				row_values2.account = "Interest on Past Due Loans - J - TGP"
				row_values2.debit_in_account_currency = flt(0)
				row_values2.credit_in_account_currency = flt(self.total)

				doc1.save(ignore_permissions=True)
				doc1.submit()

			elif self.transaction_type == "Renewal" and self.mode_of_payment == "GCash":			
				doc1 = frappe.new_doc('Journal Entry')
				doc1.voucher_type = 'Journal Entry'
				doc1.company = 'TEST Garcia\'s Pawnshop'
				doc1.posting_date = self.date_issued
				doc1.reference_doctype = "Provisional Receipt"
				doc1.reference_document = self.name
				doc1.document_status = "Renewal"

				row_values1 = doc1.append('accounts', {})
				row_values1.account = "Cash in Bank - EW Cavite - NJ - TGP"
				row_values1.debit_in_account_currency = (flt(self.total) - (flt(self.total) * 0.02)) + (((flt(self.total) * 0.02) / 1.12) * 0.02)
				row_values1.credit_in_account_currency = flt(0)

				row_values2 = doc1.append('accounts', {})
				row_values2.account = "Merchant Fee - COS - Gcash - TGP"
				row_values2.debit_in_account_currency = (flt(self.total) * 0.02)
				row_values2.credit_in_account_currency = flt(0)

				if self.interest_payment > 0:
					row_values3 = doc1.append('accounts', {})
					row_values3.account = "Interest on Past Due Loans - NJ - TGP"
					row_values3.debit_in_account_currency = flt(0)
					row_values3.credit_in_account_currency = flt(self.interest_payment)

				if flt(self.discount) > 0:
					row_values6 = doc1.append('accounts', {})
					row_values6.account = "Discount - NJ - TGP"
					row_values6.debit_in_account_currency = flt(self.discount)
					row_values6.credit_in_account_currency = flt(0)
				
				row_values4 = doc1.append('accounts', {})
				row_values4.account = "Interest on Loans and Advances - NJ - TGP"
				row_values4.debit_in_account_currency = flt(0)
				row_values4.credit_in_account_currency = flt(self.advance_interest)
				
				row_values5 = doc1.append('accounts', {})
				row_values5.account = "Withholding Tax Payable - Expanded - TGP"
				row_values5.debit_in_account_currency = flt(0)
				row_values5.credit_in_account_currency = ((flt(self.total) * 0.02) / 1.12) * 0.02

				doc1.save(ignore_permissions=True)
				doc1.submit()

			elif self.transaction_type == "Redemption" and self.mode_of_payment == "GCash":
				doc1 = frappe.new_doc('Journal Entry')
				doc1.voucher_type = 'Journal Entry'
				doc1.company = 'TEST Garcia\'s Pawnshop'
				doc1.posting_date = self.date_issued
				doc1.reference_doctype = "Provisional Receipt"
				doc1.reference_document = self.name
				doc1.document_status = "Redemption"

				row_values1 = doc1.append('accounts', {})
				row_values1.account = "Cash in Bank - EW Cavite - NJ - TGP"
				row_values1.debit_in_account_currency = (flt(self.total) - (flt(self.total) * 0.02)) + (((flt(self.total) * 0.02) / 1.12) * 0.02)
				row_values1.credit_in_account_currency = flt(0)

				row_values2 = doc1.append('accounts', {})
				row_values2.account = "Merchant Fee - COS - Gcash - TGP"
				row_values2.debit_in_account_currency = (flt(self.total) * 0.02)
				row_values2.credit_in_account_currency = flt(0)

				if self.interest_payment > 0:
					row_values4 = doc1.append('accounts', {})
					row_values4.account = "Interest on Past Due Loans - NJ - TGP"
					row_values4.debit_in_account_currency = flt(0)
					row_values4.credit_in_account_currency = flt(self.interest_payment)

				if flt(self.discount) > 0:
					row_values7 = doc1.append('accounts', {})
					row_values7.account = "Discount - NJ - TGP"
					row_values7.debit_in_account_currency = flt(self.discount)
					row_values7.credit_in_account_currency = flt(0)

				row_values5 = doc1.append('accounts', {})
				row_values5.account = "Pawned Items Inventory - NJ - TGP"
				row_values5.debit_in_account_currency = flt(0)
				row_values5.credit_in_account_currency = flt(self.principal_amount)
				
				row_values6 = doc1.append('accounts', {})
				row_values6.account = "Withholding Tax Payable - Expanded - TGP"
				row_values6.debit_in_account_currency = flt(0)
				row_values6.credit_in_account_currency = ((flt(self.total) * 0.02) / 1.12) * 0.02

				doc1.save(ignore_permissions=True)
				doc1.submit()

			elif self.transaction_type == "Amortization" and self.mode_of_payment == "GCash":
				doc1 = frappe.new_doc('Journal Entry')
				doc1.voucher_type = 'Journal Entry'
				doc1.company = 'TEST Garcia\'s Pawnshop'
				doc1.posting_date = self.date_issued
				doc1.reference_doctype = "Provisional Receipt"
				doc1.reference_document = self.name
				doc1.document_status = "Amortization"

				row_values1 = doc1.append('accounts', {})
				row_values1.account = "Cash in Bank - EW Cavite - NJ - TGP"
				row_values1.debit_in_account_currency = (flt(self.total) - (flt(self.total) * 0.02)) + (((flt(self.total) * 0.02) / 1.12) * 0.02)
				row_values1.credit_in_account_currency = flt(0)

				row_values2 = doc1.append('accounts', {})
				row_values2.account = "Merchant Fee - COS - Gcash - TGP"
				row_values2.debit_in_account_currency = (flt(self.total) * 0.02)
				row_values2.credit_in_account_currency = flt(0)

				row_values5 = doc1.append('accounts', {})
				row_values5.account = "Pawned Items Inventory - NJ - TGP"
				row_values5.debit_in_account_currency = flt(0)
				row_values5.credit_in_account_currency = flt(self.total)

				row_values6 = doc1.append('accounts', {})
				row_values6.account = "Withholding Tax Payable - Expanded - TGP"
				row_values6.debit_in_account_currency = flt(0)
				row_values6.credit_in_account_currency = ((flt(self.total) * 0.02) / 1.12) * 0.02

				doc1.save(ignore_permissions=True)
				doc1.submit()

			elif self.transaction_type == "Renewal w/ Amortization" and self.mode_of_payment == "GCash":
				doc1 = frappe.new_doc('Journal Entry')
				doc1.voucher_type = 'Journal Entry'
				doc1.company = 'TEST Garcia\'s Pawnshop'
				doc1.posting_date = self.date_issued
				doc1.reference_doctype = "Provisional Receipt"
				doc1.reference_document = self.name
				doc1.document_status = "Renewal w/ Amortization"

				row_values1 = doc1.append('accounts', {})
				row_values1.account = "Cash in Bank - EW Cavite - NJ - TGP"
				row_values1.debit_in_account_currency = (flt(self.total) - (flt(self.total) * 0.02)) + (((flt(self.total) * 0.02) / 1.12) * 0.02)
				row_values1.credit_in_account_currency = flt(0)

				row_values2 = doc1.append('accounts', {})
				row_values2.account = "Merchant Fee - COS - Gcash - TGP"
				row_values2.debit_in_account_currency = (flt(self.total) * 0.02)
				row_values2.credit_in_account_currency = flt(0)

				if self.interest_payment > 0:
					row_values4 = doc1.append('accounts', {})
					row_values4.account = "Interest on Past Due Loans - NJ - TGP"
					row_values4.debit_in_account_currency = flt(0)
					row_values4.credit_in_account_currency = flt(self.interest_payment)

				row_values5 = doc1.append('accounts', {})
				row_values5.account = "Pawned Items Inventory - NJ - TGP"
				row_values5.debit_in_account_currency = flt(0)
				row_values5.credit_in_account_currency = flt(self.additional_amortization)

				row_values6 = doc1.append('accounts', {})
				row_values6.account = "Interest on Loans and Advances - NJ - TGP"
				row_values6.debit_in_account_currency = flt(0)
				row_values6.credit_in_account_currency = flt(self.advance_interest)

				row_values7 = doc1.append('accounts', {})
				row_values7.account = "Withholding Tax Payable - Expanded - TGP"
				row_values7.debit_in_account_currency = flt(0)
				row_values7.credit_in_account_currency = ((flt(self.total) * 0.02) / 1.12) * 0.02

				if flt(self.discount) > 0:
					row_values8 = doc1.append('accounts', {})
					row_values8.account = "Discount - NJ - TGP"
					row_values8.debit_in_account_currency = flt(self.discount)
					row_values8.credit_in_account_currency = flt(0)

				doc1.save(ignore_permissions=True)
				doc1.submit()
				
			elif self.transaction_type == "Interest Payment" and self.mode_of_payment == "GCash":
				doc1 = frappe.new_doc('Journal Entry')
				doc1.voucher_type = 'Journal Entry'
				doc1.company = 'TEST Garcia\'s Pawnshop'
				doc1.posting_date = self.date_issued
				doc1.reference_doctype = "Provisional Receipt"
				doc1.reference_document = self.name
				doc1.document_status = "Interest Payment"

				row_values1 = doc1.append('accounts', {})
				row_values1.account = "Cash in Bank - EW Cavite - NJ - TGP"
				row_values1.debit_in_account_currency = (flt(self.total) - (flt(self.total) * 0.02)) + (((flt(self.total) * 0.02) / 1.12) * 0.02)
				row_values1.credit_in_account_currency = flt(0)

				row_values2 = doc1.append('accounts', {})
				row_values2.account = "Merchant Fee - COS - Gcash - TGP"
				row_values2.debit_in_account_currency = (flt(self.total) * 0.02)
				row_values2.credit_in_account_currency = flt(0)

				row_values4 = doc1.append('accounts', {})
				row_values4.account = "Interest on Past Due Loans - NJ - TGP"
				row_values4.debit_in_account_currency = flt(0)
				row_values4.credit_in_account_currency = flt(self.total)

				row_values5 = doc1.append('accounts', {})
				row_values5.account = "Withholding Tax Payable - Expanded - TGP"
				row_values5.debit_in_account_currency = flt(0)
				row_values5.credit_in_account_currency = ((flt(self.total) * 0.02) / 1.12) * 0.02

				doc1.save(ignore_permissions=True)
				doc1.submit()

		