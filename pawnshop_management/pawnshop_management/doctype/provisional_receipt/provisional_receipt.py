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
			new_pawn_ticket.branch = self.branch
			new_pawn_ticket.series = previous_pawn_ticket.item_series
			new_pawn_ticket.pawn_ticket = self.new_pawn_ticket_no
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
				doc1.company = 'MP Consolidated'
				doc1.posting_date = self.date_issued
				doc1.reference_doctype = "Provisional Receipt"
				doc1.reference_document = self.name
				doc1.document_status = "Renewal"

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
				row_values1.debit_in_account_currency = flt(self.total)
				row_values1.credit_in_account_currency = flt(0)

				if self.interest_payment > 0:
					row_values2 = doc1.append('accounts', {})
					if self.branch == "Garcia's Pawnshop - CC":
						row_values2.account = "4113-001 - Interest on Past Due Loans - NJ - CC - MPConso"
					elif self.branch == "Garcia's Pawnshop - GTC":
						row_values2.account = "4113-002 - Interest on Past Due Loans - NJ - GTC - MPConso"
					elif self.branch == "Garcia's Pawnshop - MOL":
						row_values2.account = "4113-003 - Interest on Past Due Loans - NJ - MOL - MPConso"
					elif self.branch == "Garcia's Pawnshop - POB":
						row_values2.account = "4113-004 - Interest on Past Due Loans - NJ - POB - MPConso"
					elif self.branch == "Garcia's Pawnshop - TNZ":
						row_values2.account = "4113-005 - Interest on Past Due Loans - NJ - TNZ - MPConso"
					elif self.branch == "Rabie's House":
						row_values2.account = "4113-001 - Interest on Past Due Loans - NJ - CC - MPConso"
					row_values2.debit_in_account_currency = flt(0)
					row_values2.credit_in_account_currency = flt(self.interest_payment)

				if flt(self.discount) > 0:
					row_values4 = doc1.append('accounts', {})
					if self.branch == "Garcia's Pawnshop - CC":
						row_values4.account = "4121-001 - Discount - NJ - CC - MPConso"
					elif self.branch == "Garcia's Pawnshop - GTC":
						row_values4.account = "4121-002 - Discount - NJ - GTC - MPConso"
					elif self.branch == "Garcia's Pawnshop - MOL":
						row_values4.account = "4121-003 - Discount - NJ - MOL - MPConso"
					elif self.branch == "Garcia's Pawnshop - POB":
						row_values4.account = "4121-004 - Discount - NJ - POB - MPConso"
					elif self.branch == "Garcia's Pawnshop - TNZ":
						row_values4.account = "4121-005 - Discount - NJ - TNZ - MPConso"
					elif self.branch == "Rabie's House":
						row_values4.account = "4121-001 - Discount - NJ - CC - MPConso"
					row_values4.debit_in_account_currency = flt(self.discount)
					row_values4.credit_in_account_currency = flt(0)

				row_values3 = doc1.append('accounts', {})
				if self.branch == "Garcia's Pawnshop - CC":
					row_values3.account = "4111-001 - Interest on Loans and Advances - NJ - CC - MPConso"
				elif self.branch == "Garcia's Pawnshop - GTC":
					row_values3.account = "4111-002 - Interest on Loans and Advances - NJ - GTC - MPConso"
				elif self.branch == "Garcia's Pawnshop - MOL":
					row_values3.account = "4111-003 - Interest on Loans and Advances - NJ - MOL - MPConso"
				elif self.branch == "Garcia's Pawnshop - POB":
					row_values3.account = "4111-004 - Interest on Loans and Advances - NJ - POB - MPConso"
				elif self.branch == "Garcia's Pawnshop - TNZ":
					row_values3.account = "4111-005 - Interest on Loans and Advances - NJ - TNZ - MPConso"
				elif self.branch == "Rabie's House":
					row_values3.account = "4111-001 - Interest on Loans and Advances - NJ - CC - MPConso"
				row_values3.debit_in_account_currency = flt(0)
				row_values3.credit_in_account_currency = flt(self.advance_interest)

				doc1.save(ignore_permissions=True)
				# doc1.submit()

			elif self.transaction_type == "Redemption" and self.mode_of_payment == "Cash":
				doc1 = frappe.new_doc('Journal Entry')
				doc1.voucher_type = 'Journal Entry'
				doc1.company = 'MP Consolidated'
				doc1.posting_date = self.date_issued
				doc1.reference_doctype = "Provisional Receipt"
				doc1.reference_document = self.name
				doc1.document_status = "Redemption"

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
				row_values1.debit_in_account_currency = flt(self.total)
				row_values1.credit_in_account_currency = flt(0)

				if flt(self.interest_payment) > 0:
					row_values2 = doc1.append('accounts', {})
					if self.branch == "Garcia's Pawnshop - CC":
						row_values2.account = "4113-001 - Interest on Past Due Loans - NJ - CC - MPConso"
					elif self.branch == "Garcia's Pawnshop - GTC":
						row_values2.account = "4113-002 - Interest on Past Due Loans - NJ - GTC - MPConso"
					elif self.branch == "Garcia's Pawnshop - MOL":
						row_values2.account = "4113-003 - Interest on Past Due Loans - NJ - MOL - MPConso"
					elif self.branch == "Garcia's Pawnshop - POB":
						row_values2.account = "4113-004 - Interest on Past Due Loans - NJ - POB - MPConso"
					elif self.branch == "Garcia's Pawnshop - TNZ":
						row_values2.account = "4113-005 - Interest on Past Due Loans - NJ - TNZ - MPConso"
					elif self.branch == "Rabie's House":
						row_values2.account = "4113-001 - Interest on Past Due Loans - NJ - CC - MPConso"
					row_values2.debit_in_account_currency = flt(0)
					row_values2.credit_in_account_currency = flt(self.interest_payment)

				if flt(self.discount) > 0:
					row_values4 = doc1.append('accounts', {})
					if self.branch == "Garcia's Pawnshop - CC":
						row_values4.account = "4121-001 - Discount - NJ - CC - MPConso"
					elif self.branch == "Garcia's Pawnshop - GTC":
						row_values4.account = "4121-002 - Discount - NJ - GTC - MPConso"
					elif self.branch == "Garcia's Pawnshop - MOL":
						row_values4.account = "4121-003 - Discount - NJ - MOL - MPConso"
					elif self.branch == "Garcia's Pawnshop - POB":
						row_values4.account = "4121-004 - Discount - NJ - POB - MPConso"
					elif self.branch == "Garcia's Pawnshop - TNZ":
						row_values4.account = "4121-005 - Discount - NJ - TNZ - MPConso"
					elif self.branch == "Rabie's House":
						row_values4.account = "4121-001 - Discount - NJ - CC - MPConso"
					row_values4.debit_in_account_currency = flt(self.discount)
					row_values4.credit_in_account_currency = flt(0)

				row_values3 = doc1.append('accounts', {})
				if self.branch == "Garcia's Pawnshop - CC":
					row_values3.account = "1615-001 - Pawned Items Inventory - NJ - CC - MPConso"
				elif self.branch == "Garcia's Pawnshop - GTC":
					row_values3.account = "1615-002 - Pawned Items Inventory - NJ - GTC - MPConso"
				elif self.branch == "Garcia's Pawnshop - MOL":
					row_values3.account = "1615-003 - Pawned Items Inventory - NJ - MOL - MPConso"
				elif self.branch == "Garcia's Pawnshop - POB":
					row_values3.account = "1615-004 - Pawned Items Inventory - NJ - POB - MPConso"
				elif self.branch == "Garcia's Pawnshop - TNZ":
					row_values3.account = "1615-005 - Pawned Items Inventory - NJ - TNZ - MPConso"
				elif self.branch == "Rabie's House":
					row_values3.account = "1615-001 - Pawned Items Inventory - NJ - CC - MPConso"
				row_values3.debit_in_account_currency = flt(0)
				row_values3.credit_in_account_currency = flt(self.principal_amount)

				doc1.save(ignore_permissions=True)
				# doc1.submit()

			elif self.transaction_type == "Amortization" and self.mode_of_payment == "Cash":
				doc1 = frappe.new_doc('Journal Entry')
				doc1.voucher_type = 'Journal Entry'
				doc1.company = 'MP Consolidated'
				doc1.posting_date = self.date_issued
				doc1.reference_doctype = "Provisional Receipt"
				doc1.reference_document = self.name
				doc1.document_status = "Amortization"

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
				row_values1.debit_in_account_currency = flt(self.total)
				row_values1.credit_in_account_currency = flt(0)

				if self.interest_payment > 0:
					row_values2 = doc1.append('accounts', {})
					if self.branch == "Garcia's Pawnshop - CC":
						row_values2.account = "4113-001 - Interest on Past Due Loans - NJ - CC - MPConso"
					elif self.branch == "Garcia's Pawnshop - GTC":
						row_values2.account = "4113-002 - Interest on Past Due Loans - NJ - GTC - MPConso"
					elif self.branch == "Garcia's Pawnshop - MOL":
						row_values2.account = "4113-003 - Interest on Past Due Loans - NJ - MOL - MPConso"
					elif self.branch == "Garcia's Pawnshop - POB":
						row_values2.account = "4113-004 - Interest on Past Due Loans - NJ - POB - MPConso"
					elif self.branch == "Garcia's Pawnshop - TNZ":
						row_values2.account = "4113-005 - Interest on Past Due Loans - NJ - TNZ - MPConso"
					elif self.branch == "Rabie's House":
						row_values2.account = "4113-001 - Interest on Past Due Loans - NJ - CC - MPConso"
					row_values2.debit_in_account_currency = flt(0)
					row_values2.credit_in_account_currency = flt(self.interest_payment)

				row_values3 = doc1.append('accounts', {})
				if self.branch == "Garcia's Pawnshop - CC":
					row_values3.account = "4111-001 - Interest on Loans and Advances - NJ - CC - MPConso"
				elif self.branch == "Garcia's Pawnshop - GTC":
					row_values3.account = "4111-002 - Interest on Loans and Advances - NJ - GTC - MPConso"
				elif self.branch == "Garcia's Pawnshop - MOL":
					row_values3.account = "4111-003 - Interest on Loans and Advances - NJ - MOL - MPConso"
				elif self.branch == "Garcia's Pawnshop - POB":
					row_values3.account = "4111-004 - Interest on Loans and Advances - NJ - POB - MPConso"
				elif self.branch == "Garcia's Pawnshop - TNZ":
					row_values3.account = "4111-005 - Interest on Loans and Advances - NJ - TNZ - MPConso"
				elif self.branch == "Rabie's House":
					row_values3.account = "4111-001 - Interest on Loans and Advances - NJ - CC - MPConso"
				row_values3.debit_in_account_currency = flt(0)
				row_values3.credit_in_account_currency = flt(self.total)

				doc1.save(ignore_permissions=True)
				# doc1.submit()

			elif self.transaction_type == "Renewal w/ Amortization" and self.mode_of_payment == "Cash":
				doc1 = frappe.new_doc('Journal Entry')
				doc1.voucher_type = 'Journal Entry'
				doc1.company = 'MP Consolidated'
				doc1.posting_date = self.date_issued
				doc1.reference_doctype = "Provisional Receipt"
				doc1.reference_document = self.name
				doc1.document_status = "Renewal w/ Amortization"

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
				row_values1.debit_in_account_currency = flt(self.total)
				row_values1.credit_in_account_currency = flt(0)
				
				if self.interest_payment > 0:
					row_values2 = doc1.append('accounts', {})
					if self.branch == "Garcia's Pawnshop - CC":
						row_values2.account = "4113-001 - Interest on Past Due Loans - NJ - CC - MPConso"
					elif self.branch == "Garcia's Pawnshop - GTC":
						row_values2.account = "4113-002 - Interest on Past Due Loans - NJ - GTC - MPConso"
					elif self.branch == "Garcia's Pawnshop - MOL":
						row_values2.account = "4113-003 - Interest on Past Due Loans - NJ - MOL - MPConso"
					elif self.branch == "Garcia's Pawnshop - POB":
						row_values2.account = "4113-004 - Interest on Past Due Loans - NJ - POB - MPConso"
					elif self.branch == "Garcia's Pawnshop - TNZ":
						row_values2.account = "4113-005 - Interest on Past Due Loans - NJ - TNZ - MPConso"
					elif self.branch == "Rabie's House":
						row_values2.account = "4113-001 - Interest on Past Due Loans - NJ - CC - MPConso"
					row_values2.debit_in_account_currency = flt(0)
					row_values2.credit_in_account_currency = flt(self.interest_payment)
				
				row_values3 = doc1.append('accounts', {})
				if self.branch == "Garcia's Pawnshop - CC":
					row_values3.account = "4111-001 - Interest on Loans and Advances - NJ - CC - MPConso"
				elif self.branch == "Garcia's Pawnshop - GTC":
					row_values3.account = "4111-002 - Interest on Loans and Advances - NJ - GTC - MPConso"
				elif self.branch == "Garcia's Pawnshop - MOL":
					row_values3.account = "4111-003 - Interest on Loans and Advances - NJ - MOL - MPConso"
				elif self.branch == "Garcia's Pawnshop - POB":
					row_values3.account = "4111-004 - Interest on Loans and Advances - NJ - POB - MPConso"
				elif self.branch == "Garcia's Pawnshop - TNZ":
					row_values3.account = "4111-005 - Interest on Loans and Advances - NJ - TNZ - MPConso"
				elif self.branch == "Rabie's House":
					row_values3.account = "4111-001 - Interest on Loans and Advances - NJ - CC - MPConso"
				row_values3.debit_in_account_currency = flt(0)
				row_values3.credit_in_account_currency = flt(self.advance_interest)

				row_values4 = doc1.append('accounts', {})
				if self.branch == "Garcia's Pawnshop - CC":
					row_values4.account = "1615-001 - Pawned Items Inventory - NJ - CC - MPConso"
				elif self.branch == "Garcia's Pawnshop - GTC":
					row_values4.account = "1615-002 - Pawned Items Inventory - NJ - GTC - MPConso"
				elif self.branch == "Garcia's Pawnshop - MOL":
					row_values4.account = "1615-003 - Pawned Items Inventory - NJ - MOL - MPConso"
				elif self.branch == "Garcia's Pawnshop - POB":
					row_values4.account = "1615-004 - Pawned Items Inventory - NJ - POB - MPConso"
				elif self.branch == "Garcia's Pawnshop - TNZ":
					row_values4.account = "1615-005 - Pawned Items Inventory - NJ - TNZ - MPConso"
				elif self.branch == "Rabie's House":
					row_values4.account = "1615-001 - Pawned Items Inventory - NJ - CC - MPConso"
				row_values4.debit_in_account_currency = flt(0)
				row_values4.credit_in_account_currency = flt(self.additional_amortization)

				if flt(self.discount) > 0:
					row_values5 = doc1.append('accounts', {})
					if self.branch == "Garcia's Pawnshop - CC":
						row_values5.account = "4121-001 - Discount - NJ - CC - MPConso"
					elif self.branch == "Garcia's Pawnshop - GTC":
						row_values5.account = "4121-002 - Discount - NJ - GTC - MPConso"
					elif self.branch == "Garcia's Pawnshop - MOL":
						row_values5.account = "4121-003 - Discount - NJ - MOL - MPConso"
					elif self.branch == "Garcia's Pawnshop - POB":
						row_values5.account = "4121-004 - Discount - NJ - POB - MPConso"
					elif self.branch == "Garcia's Pawnshop - TNZ":
						row_values5.account = "4121-005 - Discount - NJ - TNZ - MPConso"
					elif self.branch == "Rabie's House":
						row_values5.account = "4121-001 - Discount - NJ - CC - MPConso"
					row_values5.debit_in_account_currency = flt(self.discount)
					row_values5.credit_in_account_currency = flt(0)

				doc1.save(ignore_permissions=True)
				# doc1.submit()
				
			elif self.transaction_type == "Interest Payment" and self.mode_of_payment == "Cash":
				doc1 = frappe.new_doc('Journal Entry')
				doc1.voucher_type = 'Journal Entry'
				doc1.company = 'MP Consolidated'
				doc1.posting_date = self.date_issued
				doc1.reference_doctype = "Provisional Receipt"
				doc1.reference_document = self.name
				doc1.document_status = "Interest Payment"

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
				row_values1.debit_in_account_currency = flt(self.total)
				row_values1.credit_in_account_currency = flt(0)

				row_values2 = doc1.append('accounts', {})
				if self.branch == "Garcia's Pawnshop - CC":
					row_values2.account = "4113-001 - Interest on Past Due Loans - NJ - CC - MPConso"
				elif self.branch == "Garcia's Pawnshop - GTC":
					row_values2.account = "4113-002 - Interest on Past Due Loans - NJ - GTC - MPConso"
				elif self.branch == "Garcia's Pawnshop - MOL":
					row_values2.account = "4113-003 - Interest on Past Due Loans - NJ - MOL - MPConso"
				elif self.branch == "Garcia's Pawnshop - POB":
					row_values2.account = "4113-004 - Interest on Past Due Loans - NJ - POB - MPConso"
				elif self.branch == "Garcia's Pawnshop - TNZ":
					row_values2.account = "4113-005 - Interest on Past Due Loans - NJ - TNZ - MPConso"
				elif self.branch == "Rabie's House":
					row_values2.account = "4113-001 - Interest on Past Due Loans - NJ - CC - MPConso"
				row_values2.debit_in_account_currency = flt(0)
				row_values2.credit_in_account_currency = flt(self.total)

				doc1.save(ignore_permissions=True)
				# doc1.submit()

			# For GCash Accounts
			elif self.transaction_type == "Renewal" and self.mode_of_payment == "GCash":			
				doc1 = frappe.new_doc('Journal Entry')
				doc1.voucher_type = 'Journal Entry'
				doc1.company = 'MP Consolidated'
				doc1.posting_date = self.date_issued
				doc1.reference_doctype = "Provisional Receipt"
				doc1.reference_document = self.name
				doc1.document_status = "Renewal"

				row_values1 = doc1.append('accounts', {})
				if self.branch == "Garcia's Pawnshop - CC":
					row_values1.account = "1235-001 - Cash in Bank - Eastwest PHP - CC - MPConso"
				elif self.branch == "Garcia's Pawnshop - POB":
					row_values1.account = "1235-004 - Cash in Bank - Eastwest PHP - POB - MPConso"
				elif self.branch == "Garcia's Pawnshop - MOL":
					row_values1.account = "1235-003 - Cash in Bank - Eastwest PHP - MOL - MPConso"
				elif self.branch == "Garcia's Pawnshop - GTC":
					row_values1.account = "1235-002 - Cash in Bank - Eastwest PHP - GTC - MPConso"
				elif self.branch == "Garcia's Pawnshop - TNZ":
					row_values1.account = "1235-005 - Cash in Bank - Eastwest PHP - TNZ - MPConso"
				elif self.branch == "Rabie's House":
					row_values1.account = "1235-001 - Cash in Bank - Eastwest PHP - CC - MPConso"
				row_values1.debit_in_account_currency = (flt(self.total) - (flt(self.total) * 0.02)) + (((flt(self.total) * 0.02) / 1.12) * 0.02)
				row_values1.credit_in_account_currency = flt(0)

				row_values2 = doc1.append('accounts', {})
				if self.branch == "Garcia's Pawnshop - CC":
					row_values2.account = "4122-001 - Discount - GCash - CC - MPConso"
				elif self.branch == "Garcia's Pawnshop - POB":
					row_values2.account = "4122-004 - Discount - GCash - POB - MPConso"
				elif self.branch == "Garcia's Pawnshop - MOL":
					row_values2.account = "4122-003 - Discount - GCash - MOL - MPConso"
				elif self.branch == "Garcia's Pawnshop - GTC":
					row_values2.account = "4122-002 - Discount - GCash - GTC - MPConso"
				elif self.branch == "Garcia's Pawnshop - TNZ":
					row_values2.account = "4122-005 - Discount - GCash - TNZ - MPConso"
				elif self.branch == "Rabie's House":
					row_values2.account = "4122-001 - Discount - GCash - CC - MPConso"
				row_values2.debit_in_account_currency = (flt(self.total) * 0.02)
				row_values2.credit_in_account_currency = flt(0)

				if self.interest_payment > 0:
					row_values3 = doc1.append('accounts', {})
					if self.branch == "Garcia's Pawnshop - CC":
						row_values3.account = "4113-001 - Interest on Past Due Loans - NJ - CC - MPConso"
					elif self.branch == "Garcia's Pawnshop - GTC":
						row_values3.account = "4113-002 - Interest on Past Due Loans - NJ - GTC - MPConso"
					elif self.branch == "Garcia's Pawnshop - MOL":
						row_values3.account = "4113-003 - Interest on Past Due Loans - NJ - MOL - MPConso"
					elif self.branch == "Garcia's Pawnshop - POB":
						row_values3.account = "4113-004 - Interest on Past Due Loans - NJ - POB - MPConso"
					elif self.branch == "Garcia's Pawnshop - TNZ":
						row_values3.account = "4113-005 - Interest on Past Due Loans - NJ - TNZ - MPConso"
					elif self.branch == "Rabie's House":
						row_values3.account = "4113-001 - Interest on Past Due Loans - NJ - CC - MPConso"
					row_values3.debit_in_account_currency = flt(0)
					row_values3.credit_in_account_currency = flt(self.interest_payment)

				if flt(self.discount) > 0:
					row_values6 = doc1.append('accounts', {})
					if self.branch == "Garcia's Pawnshop - CC":
						row_values6.account = "4121-001 - Discount - NJ - CC - MPConso"
					elif self.branch == "Garcia's Pawnshop - POB":
						row_values6.account = "4121-004 - Discount - NJ - POB - MPConso"
					elif self.branch == "Garcia's Pawnshop - MOL":
						row_values6.account = "4121-003 - Discount - NJ - MOL - MPConso"
					elif self.branch == "Garcia's Pawnshop - GTC":
						row_values6.account = "4121-002 - Discount - NJ - GTC - MPConso"
					elif self.branch == "Garcia's Pawnshop - TNZ":
						row_values6.account = "4121-005 - Discount - NJ - TNZ - MPConso"
					elif self.branch == "Rabie's House":
						row_values6.account = "4121-001 - Discount - NJ - CC - MPConso"
					row_values6.debit_in_account_currency = flt(self.discount)
					row_values6.credit_in_account_currency = flt(0)
				
				row_values4 = doc1.append('accounts', {})
				if self.branch == "Garcia's Pawnshop - CC":
					row_values4.account = "4111-001 - Interest on Loans and Advances - NJ - CC - MPConso"
				elif self.branch == "Garcia's Pawnshop - GTC":
					row_values4.account = "4111-002 - Interest on Loans and Advances - NJ - GTC - MPConso"
				elif self.branch == "Garcia's Pawnshop - MOL":
					row_values4.account = "4111-003 - Interest on Loans and Advances - NJ - MOL - MPConso"
				elif self.branch == "Garcia's Pawnshop - POB":
					row_values4.account = "4111-004 - Interest on Loans and Advances - NJ - POB - MPConso"
				elif self.branch == "Garcia's Pawnshop - TNZ":
					row_values4.account = "4111-005 - Interest on Loans and Advances - NJ - TNZ - MPConso"
				elif self.branch == "Rabie's House":
					row_values4.account = "4111-001 - Interest on Loans and Advances - NJ - CC - MPConso"
				row_values4.debit_in_account_currency = flt(0)
				row_values4.credit_in_account_currency = flt(self.advance_interest)
				
				row_values5 = doc1.append('accounts', {})
				if self.branch == "Garcia's Pawnshop - CC":
					row_values5.account = "2315-001 - Withholding Tax Payable - Expanded - CC - MPConso"
				elif self.branch == "Garcia's Pawnshop - GTC":
					row_values5.account = "2315-002 - Withholding Tax Payable - Expanded - GTC - MPConso"
				elif self.branch == "Garcia's Pawnshop - MOL":
					row_values5.account = "2315-003 - Withholding Tax Payable - Expanded - MOL - MPConso"
				elif self.branch == "Garcia's Pawnshop - POB":
					row_values5.account = "2315-004 - Withholding Tax Payable - Expanded - POB - MPConso"
				elif self.branch == "Garcia's Pawnshop - TNZ":
					row_values5.account = "2315-005 - Withholding Tax Payable - Expanded - TNZ - MPConso"
				elif self.branch == "Rabie's House":
					row_values5.account = "2315-001 - Withholding Tax Payable - Expanded - CC - MPConso" 
				row_values5.debit_in_account_currency = flt(0)
				row_values5.credit_in_account_currency = ((flt(self.total) * 0.02) / 1.12) * 0.02

				doc1.save(ignore_permissions=True)
				# doc1.submit()

			elif self.transaction_type == "Redemption" and self.mode_of_payment == "GCash":
				doc1 = frappe.new_doc('Journal Entry')
				doc1.voucher_type = 'Journal Entry'
				doc1.company = 'MP Consolidated'
				doc1.posting_date = self.date_issued
				doc1.reference_doctype = "Provisional Receipt"
				doc1.reference_document = self.name
				doc1.document_status = "Redemption"

				row_values1 = doc1.append('accounts', {})
				if self.branch == "Garcia's Pawnshop - CC":
					row_values1.account = "1235-001 - Cash in Bank - Eastwest PHP - CC - MPConso"
				elif self.branch == "Garcia's Pawnshop - POB":
					row_values1.account = "1235-004 - Cash in Bank - Eastwest PHP - POB - MPConso"
				elif self.branch == "Garcia's Pawnshop - MOL":
					row_values1.account = "1235-003 - Cash in Bank - Eastwest PHP - MOL - MPConso"
				elif self.branch == "Garcia's Pawnshop - GTC":
					row_values1.account = "1235-002 - Cash in Bank - Eastwest PHP - GTC - MPConso"
				elif self.branch == "Garcia's Pawnshop - TNZ":
					row_values1.account = "1235-005 - Cash in Bank - Eastwest PHP - TNZ - MPConso"
				elif self.branch == "Rabie's House":
					row_values1.account = "1235-001 - Cash in Bank - Eastwest PHP - CC - MPConso"
				row_values1.debit_in_account_currency = (flt(self.total) - (flt(self.total) * 0.02)) + (((flt(self.total) * 0.02) / 1.12) * 0.02)
				row_values1.credit_in_account_currency = flt(0)

				row_values2 = doc1.append('accounts', {})
				if self.branch == "Garcia's Pawnshop - CC":
					row_values2.account = "4122-001 - Discount - GCash - CC - MPConso"
				elif self.branch == "Garcia's Pawnshop - POB":
					row_values2.account = "4122-004 - Discount - GCash - POB - MPConso"
				elif self.branch == "Garcia's Pawnshop - MOL":
					row_values2.account = "4122-003 - Discount - GCash - MOL - MPConso"
				elif self.branch == "Garcia's Pawnshop - GTC":
					row_values2.account = "4122-002 - Discount - GCash - GTC - MPConso"
				elif self.branch == "Garcia's Pawnshop - TNZ":
					row_values2.account = "4122-005 - Discount - GCash - TNZ - MPConso"
				elif self.branch == "Rabie's House":
					row_values2.account = "4122-001 - Discount - GCash - CC - MPConso"
				row_values2.debit_in_account_currency = (flt(self.total) * 0.02)
				row_values2.credit_in_account_currency = flt(0)

				if self.interest_payment > 0:
					row_values4 = doc1.append('accounts', {})
					if self.branch == "Garcia's Pawnshop - CC":
						row_values4.account = "4113-001 - Interest on Past Due Loans - NJ - CC - MPConso"
					elif self.branch == "Garcia's Pawnshop - GTC":
						row_values4.account = "4113-002 - Interest on Past Due Loans - NJ - GTC - MPConso"
					elif self.branch == "Garcia's Pawnshop - MOL":
						row_values4.account = "4113-003 - Interest on Past Due Loans - NJ - MOL - MPConso"
					elif self.branch == "Garcia's Pawnshop - POB":
						row_values4.account = "4113-004 - Interest on Past Due Loans - NJ - POB - MPConso"
					elif self.branch == "Garcia's Pawnshop - TNZ":
						row_values4.account = "4113-005 - Interest on Past Due Loans - NJ - TNZ - MPConso"
					elif self.branch == "Rabie's House":
						row_values4.account = "4113-001 - Interest on Past Due Loans - NJ - CC - MPConso"
					row_values4.debit_in_account_currency = flt(0)
					row_values4.credit_in_account_currency = flt(self.interest_payment)

				if flt(self.discount) > 0:
					row_values7 = doc1.append('accounts', {})
					if self.branch == "Garcia's Pawnshop - CC":
						row_values7.account = "4121-001 - Discount - NJ - CC - MPConso"
					elif self.branch == "Garcia's Pawnshop - POB":
						row_values7.account = "4121-004 - Discount - NJ - POB - MPConso"
					elif self.branch == "Garcia's Pawnshop - MOL":
						row_values7.account = "4121-003 - Discount - NJ - MOL - MPConso"
					elif self.branch == "Garcia's Pawnshop - GTC":
						row_values7.account = "4121-002 - Discount - NJ - GTC - MPConso"
					elif self.branch == "Garcia's Pawnshop - TNZ":
						row_values7.account = "4121-005 - Discount - NJ - TNZ - MPConso"
					elif self.branch == "Rabie's House":
						row_values7.account = "4121-001 - Discount - NJ - CC - MPConso"
					row_values7.debit_in_account_currency = flt(self.discount)
					row_values7.credit_in_account_currency = flt(0)

				row_values5 = doc1.append('accounts', {})
				if self.branch == "Garcia's Pawnshop - CC":
					row_values5.account = "1615-001 - Pawned Items Inventory - NJ - CC - MPConso"
				elif self.branch == "Garcia's Pawnshop - GTC":
					row_values5.account = "1615-002 - Pawned Items Inventory - NJ - GTC - MPConso"
				elif self.branch == "Garcia's Pawnshop - MOL":
					row_values5.account = "1615-003 - Pawned Items Inventory - NJ - MOL - MPConso"
				elif self.branch == "Garcia's Pawnshop - POB":
					row_values5.account = "1615-004 - Pawned Items Inventory - NJ - POB - MPConso"
				elif self.branch == "Garcia's Pawnshop - TNZ":
					row_values5.account = "1615-005 - Pawned Items Inventory - NJ - TNZ - MPConso"
				elif self.branch == "Rabie's House":
					row_values5.account = "1615-001 - Pawned Items Inventory - NJ - CC - MPConso"
				row_values5.debit_in_account_currency = flt(0)
				row_values5.credit_in_account_currency = flt(self.principal_amount)
				
				row_values6 = doc1.append('accounts', {})
				row_values6.account = "Withholding Tax Payable - Expanded - MPConso"
				row_values6.debit_in_account_currency = flt(0)
				row_values6.credit_in_account_currency = ((flt(self.total) * 0.02) / 1.12) * 0.02

				doc1.save(ignore_permissions=True)
				# doc1.submit()

			elif self.transaction_type == "Amortization" and self.mode_of_payment == "GCash":
				doc1 = frappe.new_doc('Journal Entry')
				doc1.voucher_type = 'Journal Entry'
				doc1.company = 'MP Consolidated'
				doc1.posting_date = self.date_issued
				doc1.reference_doctype = "Provisional Receipt"
				doc1.reference_document = self.name
				doc1.document_status = "Amortization"

				row_values1 = doc1.append('accounts', {})
				if self.branch == "Garcia's Pawnshop - CC":
					row_values1.account = "1235-001 - Cash in Bank - Eastwest PHP - CC - MPConso"
				elif self.branch == "Garcia's Pawnshop - POB":
					row_values1.account = "1235-004 - Cash in Bank - Eastwest PHP - POB - MPConso"
				elif self.branch == "Garcia's Pawnshop - MOL":
					row_values1.account = "1235-003 - Cash in Bank - Eastwest PHP - MOL - MPConso"
				elif self.branch == "Garcia's Pawnshop - GTC":
					row_values1.account = "1235-002 - Cash in Bank - Eastwest PHP - GTC - MPConso"
				elif self.branch == "Garcia's Pawnshop - TNZ":
					row_values1.account = "1235-005 - Cash in Bank - Eastwest PHP - TNZ - MPConso"
				elif self.branch == "Rabie's House":
					row_values1.account = "1235-001 - Cash in Bank - Eastwest PHP - CC - MPConso"
				row_values1.debit_in_account_currency = (flt(self.total) - (flt(self.total) * 0.02)) + (((flt(self.total) * 0.02) / 1.12) * 0.02)
				row_values1.credit_in_account_currency = flt(0)

				row_values2 = doc1.append('accounts', {})
				if self.branch == "Garcia's Pawnshop - CC":
					row_values2.account = "4122-001 - Discount - GCash - CC - MPConso"
				elif self.branch == "Garcia's Pawnshop - POB":
					row_values2.account = "4122-004 - Discount - GCash - POB - MPConso"
				elif self.branch == "Garcia's Pawnshop - MOL":
					row_values2.account = "4122-003 - Discount - GCash - MOL - MPConso"
				elif self.branch == "Garcia's Pawnshop - GTC":
					row_values2.account = "4122-002 - Discount - GCash - GTC - MPConso"
				elif self.branch == "Garcia's Pawnshop - TNZ":
					row_values2.account = "4122-005 - Discount - GCash - TNZ - MPConso"
				elif self.branch == "Rabie's House":
					row_values2.account = "4122-001 - Discount - GCash - CC - MPConso"
				row_values2.debit_in_account_currency = (flt(self.total) * 0.02)
				row_values2.credit_in_account_currency = flt(0)

				row_values5 = doc1.append('accounts', {})
				if self.branch == "Garcia's Pawnshop - CC":
					row_values5.account = "1615-001 - Pawned Items Inventory - NJ - CC - MPConso"
				elif self.branch == "Garcia's Pawnshop - GTC":
					row_values5.account = "1615-002 - Pawned Items Inventory - NJ - GTC - MPConso"
				elif self.branch == "Garcia's Pawnshop - MOL":
					row_values5.account = "1615-003 - Pawned Items Inventory - NJ - MOL - MPConso"
				elif self.branch == "Garcia's Pawnshop - POB":
					row_values5.account = "1615-004 - Pawned Items Inventory - NJ - POB - MPConso"
				elif self.branch == "Garcia's Pawnshop - TNZ":
					row_values5.account = "1615-005 - Pawned Items Inventory - NJ - TNZ - MPConso"
				elif self.branch == "Rabie's House":
					row_values5.account = "1615-001 - Pawned Items Inventory - NJ - CC - MPConso"
				row_values5.debit_in_account_currency = flt(0)
				row_values5.credit_in_account_currency = flt(self.total)

				row_values6 = doc1.append('accounts', {})
				if self.branch == "Garcia's Pawnshop - CC":
					row_values6.account = "2315-001 - Withholding Tax Payable - Expanded - CC - MPConso"
				elif self.branch == "Garcia's Pawnshop - GTC":
					row_values6.account = "2315-002 - Withholding Tax Payable - Expanded - GTC - MPConso"
				elif self.branch == "Garcia's Pawnshop - MOL":
					row_values6.account = "2315-003 - Withholding Tax Payable - Expanded - MOL - MPConso"
				elif self.branch == "Garcia's Pawnshop - POB":
					row_values6.account = "2315-004 - Withholding Tax Payable - Expanded - POB - MPConso"
				elif self.branch == "Garcia's Pawnshop - TNZ":
					row_values6.account = "2315-005 - Withholding Tax Payable - Expanded - TNZ - MPConso"
				elif self.branch == "Rabie's House":
					row_values6.account = "2315-001 - Withholding Tax Payable - Expanded - CC - MPConso"
				row_values6.debit_in_account_currency = flt(0)
				row_values6.credit_in_account_currency = ((flt(self.total) * 0.02) / 1.12) * 0.02

				doc1.save(ignore_permissions=True)
				# doc1.submit()

			elif self.transaction_type == "Renewal w/ Amortization" and self.mode_of_payment == "GCash":
				doc1 = frappe.new_doc('Journal Entry')
				doc1.voucher_type = 'Journal Entry'
				doc1.company = 'MP Consolidated'
				doc1.posting_date = self.date_issued
				doc1.reference_doctype = "Provisional Receipt"
				doc1.reference_document = self.name
				doc1.document_status = "Renewal w/ Amortization"

				row_values1 = doc1.append('accounts', {})
				if self.branch == "Garcia's Pawnshop - CC":
					row_values1.account = "1235-001 - Cash in Bank - Eastwest PHP - CC - MPConso"
				elif self.branch == "Garcia's Pawnshop - POB":
					row_values1.account = "1235-004 - Cash in Bank - Eastwest PHP - POB - MPConso"
				elif self.branch == "Garcia's Pawnshop - MOL":
					row_values1.account = "1235-003 - Cash in Bank - Eastwest PHP - MOL - MPConso"
				elif self.branch == "Garcia's Pawnshop - GTC":
					row_values1.account = "1235-002 - Cash in Bank - Eastwest PHP - GTC - MPConso"
				elif self.branch == "Garcia's Pawnshop - TNZ":
					row_values1.account = "1235-005 - Cash in Bank - Eastwest PHP - TNZ - MPConso"
				elif self.branch == "Rabie's House":
					row_values1.account = "1235-001 - Cash in Bank - Eastwest PHP - CC - MPConso"
				row_values1.debit_in_account_currency = (flt(self.total) - (flt(self.total) * 0.02)) + (((flt(self.total) * 0.02) / 1.12) * 0.02)
				row_values1.credit_in_account_currency = flt(0)

				row_values2 = doc1.append('accounts', {})
				if self.branch == "Garcia's Pawnshop - CC":
					row_values2.account = "4122-001 - Discount - GCash - CC - MPConso"
				elif self.branch == "Garcia's Pawnshop - POB":
					row_values2.account = "4122-004 - Discount - GCash - POB - MPConso"
				elif self.branch == "Garcia's Pawnshop - MOL":
					row_values2.account = "4122-003 - Discount - GCash - MOL - MPConso"
				elif self.branch == "Garcia's Pawnshop - GTC":
					row_values2.account = "4122-002 - Discount - GCash - GTC - MPConso"
				elif self.branch == "Garcia's Pawnshop - TNZ":
					row_values2.account = "4122-005 - Discount - GCash - TNZ - MPConso"
				elif self.branch == "Rabie's House":
					row_values2.account = "4122-001 - Discount - GCash - CC - MPConso"
				row_values2.debit_in_account_currency = (flt(self.total) * 0.02)
				row_values2.credit_in_account_currency = flt(0)

				if self.interest_payment > 0:
					row_values4 = doc1.append('accounts', {})
					if self.branch == "Garcia's Pawnshop - CC":
						row_values4.account = "4113-001 - Interest on Past Due Loans - NJ - CC - MPConso"
					elif self.branch == "Garcia's Pawnshop - GTC":
						row_values4.account = "4113-002 - Interest on Past Due Loans - NJ - GTC - MPConso"
					elif self.branch == "Garcia's Pawnshop - MOL":
						row_values4.account = "4113-003 - Interest on Past Due Loans - NJ - MOL - MPConso"
					elif self.branch == "Garcia's Pawnshop - POB":
						row_values4.account = "4113-004 - Interest on Past Due Loans - NJ - POB - MPConso"
					elif self.branch == "Garcia's Pawnshop - TNZ":
						row_values4.account = "4113-005 - Interest on Past Due Loans - NJ - TNZ - MPConso"
					elif self.branch == "Rabie's House":
						row_values4.account = "4113-001 - Interest on Past Due Loans - NJ - CC - MPConso"
					row_values4.debit_in_account_currency = flt(0)
					row_values4.credit_in_account_currency = flt(self.interest_payment)

				row_values5 = doc1.append('accounts', {})
				if self.branch == "Garcia's Pawnshop - CC":
					row_values5.account = "1615-001 - Pawned Items Inventory - NJ - CC - MPConso"
				elif self.branch == "Garcia's Pawnshop - GTC":
					row_values5.account = "1615-002 - Pawned Items Inventory - NJ - GTC - MPConso"
				elif self.branch == "Garcia's Pawnshop - MOL":
					row_values5.account = "1615-003 - Pawned Items Inventory - NJ - MOL - MPConso"
				elif self.branch == "Garcia's Pawnshop - POB":
					row_values5.account = "1615-004 - Pawned Items Inventory - NJ - POB - MPConso"
				elif self.branch == "Garcia's Pawnshop - TNZ":
					row_values5.account = "1615-005 - Pawned Items Inventory - NJ - TNZ - MPConso"
				elif self.branch == "Rabie's House":
					row_values5.account = "1615-001 - Pawned Items Inventory - NJ - CC - MPConso"
				row_values5.debit_in_account_currency = flt(0)
				row_values5.credit_in_account_currency = flt(self.additional_amortization)

				row_values6 = doc1.append('accounts', {})
				if self.branch == "Garcia's Pawnshop - CC":
					row_values6.account = "4111-001 - Interest on Loans and Advances - NJ - CC - MPConso"
				elif self.branch == "Garcia's Pawnshop - GTC":
					row_values6.account = "4111-002 - Interest on Loans and Advances - NJ - GTC - MPConso"
				elif self.branch == "Garcia's Pawnshop - MOL":
					row_values6.account = "4111-003 - Interest on Loans and Advances - NJ - MOL - MPConso"
				elif self.branch == "Garcia's Pawnshop - POB":
					row_values6.account = "4111-004 - Interest on Loans and Advances - NJ - POB - MPConso"
				elif self.branch == "Garcia's Pawnshop - TNZ":
					row_values6.account = "4111-005 - Interest on Loans and Advances - NJ - TNZ - MPConso"
				elif self.branch == "Rabie's House":
					row_values6.account = "4111-001 - Interest on Loans and Advances - NJ - CC - MPConso"
				row_values6.debit_in_account_currency = flt(0)
				row_values6.credit_in_account_currency = flt(self.advance_interest)

				row_values7 = doc1.append('accounts', {})
				if self.branch == "Garcia's Pawnshop - CC":
					row_values7.account = "2315-001 - Withholding Tax Payable - Expanded - CC - MPConso"
				elif self.branch == "Garcia's Pawnshop - GTC":
					row_values7.account = "2315-002 - Withholding Tax Payable - Expanded - GTC - MPConso"
				elif self.branch == "Garcia's Pawnshop - MOL":
					row_values7.account = "2315-003 - Withholding Tax Payable - Expanded - MOL - MPConso"
				elif self.branch == "Garcia's Pawnshop - POB":
					row_values7.account = "2315-004 - Withholding Tax Payable - Expanded - POB - MPConso"
				elif self.branch == "Garcia's Pawnshop - TNZ":
					row_values7.account = "2315-005 - Withholding Tax Payable - Expanded - TNZ - MPConso"
				elif self.branch == "Rabie's House":
					row_values7.account = "2315-001 - Withholding Tax Payable - Expanded - CC - MPConso"
				row_values7.debit_in_account_currency = flt(0)
				row_values7.credit_in_account_currency = ((flt(self.total) * 0.02) / 1.12) * 0.02

				if flt(self.discount) > 0:
					row_values8 = doc1.append('accounts', {})
					if self.branch == "Garcia's Pawnshop - CC":
						row_values8.account = "4122-001 - Discount - GCash - CC - MPConso"
					elif self.branch == "Garcia's Pawnshop - POB":
						row_values8.account = "4122-004 - Discount - GCash - POB - MPConso"
					elif self.branch == "Garcia's Pawnshop - MOL":
						row_values8.account = "4122-003 - Discount - GCash - MOL - MPConso"
					elif self.branch == "Garcia's Pawnshop - GTC":
						row_values8.account = "4122-002 - Discount - GCash - GTC - MPConso"
					elif self.branch == "Garcia's Pawnshop - TNZ":
						row_values8.account = "4122-005 - Discount - GCash - TNZ - MPConso"
					elif self.branch == "Rabie's House":
						row_values8.account = "4122-001 - Discount - GCash - CC - MPConso"
					row_values8.debit_in_account_currency = flt(self.discount)
					row_values8.credit_in_account_currency = flt(0)

				doc1.save(ignore_permissions=True)
				# doc1.submit()
				
			elif self.transaction_type == "Interest Payment" and self.mode_of_payment == "GCash":
				doc1 = frappe.new_doc('Journal Entry')
				doc1.voucher_type = 'Journal Entry'
				doc1.company = 'MP Consolidated'
				doc1.posting_date = self.date_issued
				doc1.reference_doctype = "Provisional Receipt"
				doc1.reference_document = self.name
				doc1.document_status = "Interest Payment"

				row_values1 = doc1.append('accounts', {})
				if self.branch == "Garcia's Pawnshop - CC":
					row_values1.account = "1235-001 - Cash in Bank - Eastwest PHP - CC - MPConso"
				elif self.branch == "Garcia's Pawnshop - POB":
					row_values1.account = "1235-004 - Cash in Bank - Eastwest PHP - POB - MPConso"
				elif self.branch == "Garcia's Pawnshop - MOL":
					row_values1.account = "1235-003 - Cash in Bank - Eastwest PHP - MOL - MPConso"
				elif self.branch == "Garcia's Pawnshop - GTC":
					row_values1.account = "1235-002 - Cash in Bank - Eastwest PHP - GTC - MPConso"
				elif self.branch == "Garcia's Pawnshop - TNZ":
					row_values1.account = "1235-005 - Cash in Bank - Eastwest PHP - TNZ - MPConso"
				elif self.branch == "Rabie's House":
					row_values1.account = "1235-001 - Cash in Bank - Eastwest PHP - CC - MPConso"
				row_values1.debit_in_account_currency = (flt(self.total) - (flt(self.total) * 0.02)) + (((flt(self.total) * 0.02) / 1.12) * 0.02)
				row_values1.credit_in_account_currency = flt(0)

				row_values2 = doc1.append('accounts', {})
				if self.branch == "Garcia's Pawnshop - CC":
					row_values1.account = "4122-001 - Discount - GCash - CC - MPConso"
				elif self.branch == "Garcia's Pawnshop - POB":
					row_values1.account = "4122-004 - Discount - GCash - POB - MPConso"
				elif self.branch == "Garcia's Pawnshop - MOL":
					row_values1.account = "4122-003 - Discount - GCash - MOL - MPConso"
				elif self.branch == "Garcia's Pawnshop - GTC":
					row_values1.account = "4122-002 - Discount - GCash - GTC - MPConso"
				elif self.branch == "Garcia's Pawnshop - TNZ":
					row_values1.account = "4122-005 - Discount - GCash - TNZ - MPConso"
				elif self.branch == "Rabie's House":
					row_values1.account = "4122-001 - Discount - GCash - CC - MPConso"
				row_values2.debit_in_account_currency = (flt(self.total) * 0.02)
				row_values2.credit_in_account_currency = flt(0)

				row_values4 = doc1.append('accounts', {})
				if self.branch == "Garcia's Pawnshop - CC":
					row_values4.account = "4113-001 - Interest on Past Due Loans - NJ - CC - MPConso"
				elif self.branch == "Garcia's Pawnshop - GTC":
					row_values4.account = "4113-002 - Interest on Past Due Loans - NJ - GTC - MPConso"
				elif self.branch == "Garcia's Pawnshop - MOL":
					row_values4.account = "4113-003 - Interest on Past Due Loans - NJ - MOL - MPConso"
				elif self.branch == "Garcia's Pawnshop - POB":
					row_values4.account = "4113-004 - Interest on Past Due Loans - NJ - POB - MPConso"
				elif self.branch == "Garcia's Pawnshop - TNZ":
					row_values4.account = "4113-005 - Interest on Past Due Loans - NJ - TNZ - MPConso"
				elif self.branch == "Rabie's House":
					row_values4.account = "4113-001 - Interest on Past Due Loans - NJ - CC - MPConso"
				row_values4.debit_in_account_currency = flt(0)
				row_values4.credit_in_account_currency = flt(self.total)

				row_values5 = doc1.append('accounts', {})
				if self.branch == "Garcia's Pawnshop - CC":
					row_values5.account = "2315-001 - Withholding Tax Payable - Expanded - CC - MPConso"
				elif self.branch == "Garcia's Pawnshop - GTC":
					row_values5.account = "2315-002 - Withholding Tax Payable - Expanded - GTC - MPConso"
				elif self.branch == "Garcia's Pawnshop - MOL":
					row_values5.account = "2315-003 - Withholding Tax Payable - Expanded - MOL - MPConso"
				elif self.branch == "Garcia's Pawnshop - POB":
					row_values5.account = "2315-004 - Withholding Tax Payable - Expanded - POB - MPConso"
				elif self.branch == "Garcia's Pawnshop - TNZ":
					row_values5.account = "2315-005 - Withholding Tax Payable - Expanded - TNZ - MPConso"
				elif self.branch == "Rabie's House":
					row_values5.account = "2315-001 - Withholding Tax Payable - Expanded - CC - MPConso"
				row_values5.debit_in_account_currency = flt(0)
				row_values5.credit_in_account_currency = ((flt(self.total) * 0.02) / 1.12) * 0.02

				doc1.save(ignore_permissions=True)
				# doc1.submit()
			
			# For Bank Transfer Transaction
			elif self.transaction_type == "Renewal" and self.mode_of_payment == "Bank Transfer":
				doc1 = frappe.new_doc('Journal Entry')
				doc1.voucher_type = 'Journal Entry'
				doc1.company = 'MP Consolidated'
				doc1.posting_date = self.date_issued
				doc1.reference_doctype = "Provisional Receipt"
				doc1.reference_document = self.name
				doc1.document_status = "Renewal"

				row_values1 = doc1.append('accounts', {})
				if self.bank == "BDO":
					row_values1.account = "1215-000 - Cash in Bank - BDO SM Ros - Php - MPConso"
				elif self.bank == "BPI":
					row_values1.account = "1205-000 - Cash in Bank - BPI Marquesa - MPConso"
				elif self.bank == "East West Cavite Branch":
					if self.branch == "Garcia's Pawnshop - CC":
						row_values1.account = "1235-001 - Cash in Bank - Eastwest PHP - CC - MPConso"
					elif self.branch == "Garcia's Pawnshop - POB":
						row_values1.account = "1235-004 - Cash in Bank - Eastwest PHP - POB - MPConso"
					elif self.branch == "Garcia's Pawnshop - MOL":
						row_values1.account = "1235-003 - Cash in Bank - Eastwest PHP - MOL - MPConso"
					elif self.branch == "Garcia's Pawnshop - GTC":
						row_values1.account = "1235-002 - Cash in Bank - Eastwest PHP - GTC - MPConso"
					elif self.branch == "Garcia's Pawnshop - TNZ":
						row_values1.account = "1235-005 - Cash in Bank - Eastwest PHP - TNZ - MPConso"
					elif self.branch == "Rabie's House":
						row_values1.account = "1235-001 - Cash in Bank - Eastwest PHP - CC - MPConso"
				row_values1.debit_in_account_currency = flt(self.total)
				row_values1.credit_in_account_currency = flt(0)

				if self.interest_payment > 0:
					row_values2 = doc1.append('accounts', {})
					if self.branch == "Garcia's Pawnshop - CC":
						row_values2.account = "4113-001 - Interest on Past Due Loans - NJ - CC - MPConso"
					elif self.branch == "Garcia's Pawnshop - GTC":
						row_values2.account = "4113-002 - Interest on Past Due Loans - NJ - GTC - MPConso"
					elif self.branch == "Garcia's Pawnshop - MOL":
						row_values2.account = "4113-003 - Interest on Past Due Loans - NJ - MOL - MPConso"
					elif self.branch == "Garcia's Pawnshop - POB":
						row_values2.account = "4113-004 - Interest on Past Due Loans - NJ - POB - MPConso"
					elif self.branch == "Garcia's Pawnshop - TNZ":
						row_values2.account = "4113-005 - Interest on Past Due Loans - NJ - TNZ - MPConso"
					elif self.branch == "Rabie's House":
						row_values2.account = "4113-001 - Interest on Past Due Loans - NJ - CC - MPConso"
					row_values2.debit_in_account_currency = flt(0)
					row_values2.credit_in_account_currency = flt(self.interest_payment)

				row_values3 = doc1.append('accounts', {})
				if self.branch == "Garcia's Pawnshop - CC":
					row_values3.account = "4111-001 - Interest on Loans and Advances - NJ - CC - MPConso"
				elif self.branch == "Garcia's Pawnshop - GTC":
					row_values3.account = "4111-002 - Interest on Loans and Advances - NJ - GTC - MPConso"
				elif self.branch == "Garcia's Pawnshop - MOL":
					row_values3.account = "4111-003 - Interest on Loans and Advances - NJ - MOL - MPConso"
				elif self.branch == "Garcia's Pawnshop - POB":
					row_values3.account = "4111-004 - Interest on Loans and Advances - NJ - POB - MPConso"
				elif self.branch == "Garcia's Pawnshop - TNZ":
					row_values3.account = "4111-005 - Interest on Loans and Advances - NJ - TNZ - MPConso"
				elif self.branch == "Rabie's House":
					row_values3.account = "4111-001 - Interest on Loans and Advances - NJ - CC - MPConso"
				row_values3.debit_in_account_currency = flt(0)
				row_values3.credit_in_account_currency = flt(self.advance_interest)

				if flt(self.discount) > 0:
					row_values4 = doc1.append('accounts', {})
					if self.branch == "Garcia's Pawnshop - CC":
						row_values4.account = "4122-001 - Discount - GCash - CC - MPConso"
					elif self.branch == "Garcia's Pawnshop - POB":
						row_values4.account = "4122-004 - Discount - GCash - POB - MPConso"
					elif self.branch == "Garcia's Pawnshop - MOL":
						row_values4.account = "4122-003 - Discount - GCash - MOL - MPConso"
					elif self.branch == "Garcia's Pawnshop - GTC":
						row_values4.account = "4122-002 - Discount - GCash - GTC - MPConso"
					elif self.branch == "Garcia's Pawnshop - TNZ":
						row_values4.account = "4122-005 - Discount - GCash - TNZ - MPConso"
					elif self.branch == "Rabie's House":
						row_values4.account = "4122-001 - Discount - GCash - CC - MPConso"
					row_values4.debit_in_account_currency = flt(self.discount)
					row_values4.credit_in_account_currency = flt(0)

				doc1.save(ignore_permissions=True)
				# doc1.submit()

			elif self.transaction_type == "Redemption" and self.mode_of_payment == "Bank Transfer":
				doc1 = frappe.new_doc('Journal Entry')
				doc1.voucher_type = 'Journal Entry'
				doc1.company = 'MP Consolidated'
				doc1.posting_date = self.date_issued
				doc1.reference_doctype = "Provisional Receipt"
				doc1.reference_document = self.name
				doc1.document_status = "Redemption"

				row_values1 = doc1.append('accounts', {})
				if self.bank == "BDO":
					row_values1.account = "1215-000 - Cash in Bank - BDO SM Ros - Php - MPConso"
				elif self.bank == "BPI":
					row_values1.account = "1205-000 - Cash in Bank - BPI Marquesa - MPConso"
				elif self.bank == "East West Cavite Branch":
					if self.branch == "Garcia's Pawnshop - CC":
						row_values1.account = "1235-001 - Cash in Bank - Eastwest PHP - CC - MPConso"
					elif self.branch == "Garcia's Pawnshop - POB":
						row_values1.account = "1235-004 - Cash in Bank - Eastwest PHP - POB - MPConso"
					elif self.branch == "Garcia's Pawnshop - MOL":
						row_values1.account = "1235-003 - Cash in Bank - Eastwest PHP - MOL - MPConso"
					elif self.branch == "Garcia's Pawnshop - GTC":
						row_values1.account = "1235-002 - Cash in Bank - Eastwest PHP - GTC - MPConso"
					elif self.branch == "Garcia's Pawnshop - TNZ":
						row_values1.account = "1235-005 - Cash in Bank - Eastwest PHP - TNZ - MPConso"
					elif self.branch == "Rabie's House":
						row_values1.account = "1235-001 - Cash in Bank - Eastwest PHP - CC - MPConso"
				row_values1.debit_in_account_currency = flt(self.total)
				row_values1.credit_in_account_currency = flt(0)

				if flt(self.interest_payment) > 0:
					row_values2 = doc1.append('accounts', {})
					if self.branch == "Garcia's Pawnshop - CC":
						row_values2.account = "4113-001 - Interest on Past Due Loans - NJ - CC - MPConso"
					elif self.branch == "Garcia's Pawnshop - GTC":
						row_values2.account = "4113-002 - Interest on Past Due Loans - NJ - GTC - MPConso"
					elif self.branch == "Garcia's Pawnshop - MOL":
						row_values2.account = "4113-003 - Interest on Past Due Loans - NJ - MOL - MPConso"
					elif self.branch == "Garcia's Pawnshop - POB":
						row_values2.account = "4113-004 - Interest on Past Due Loans - NJ - POB - MPConso"
					elif self.branch == "Garcia's Pawnshop - TNZ":
						row_values2.account = "4113-005 - Interest on Past Due Loans - NJ - TNZ - MPConso"
					elif self.branch == "Rabie's House":
						row_values2.account = "4113-001 - Interest on Past Due Loans - NJ - CC - MPConso"
					row_values2.debit_in_account_currency = flt(0)
					row_values2.credit_in_account_currency = flt(self.interest_payment)

				row_values3 = doc1.append('accounts', {})
				if self.branch == "Garcia's Pawnshop - CC":
					row_values3.account = "1615-001 - Pawned Items Inventory - NJ - CC - MPConso"
				elif self.branch == "Garcia's Pawnshop - GTC":
					row_values3.account = "1615-002 - Pawned Items Inventory - NJ - GTC - MPConso"
				elif self.branch == "Garcia's Pawnshop - MOL":
					row_values3.account = "1615-003 - Pawned Items Inventory - NJ - MOL - MPConso"
				elif self.branch == "Garcia's Pawnshop - POB":
					row_values3.account = "1615-004 - Pawned Items Inventory - NJ - POB - MPConso"
				elif self.branch == "Garcia's Pawnshop - TNZ":
					row_values3.account = "1615-005 - Pawned Items Inventory - NJ - TNZ - MPConso"
				elif self.branch == "Rabie's House":
					row_values3.account = "1615-001 - Pawned Items Inventory - NJ - CC - MPConso"
				row_values3.debit_in_account_currency = flt(0)
				row_values3.credit_in_account_currency = flt(self.principal_amount)

				if flt(self.discount) > 0:
					row_values4 = doc1.append('accounts', {})
					if self.branch == "Garcia's Pawnshop - CC":
						row_values4.account = "4122-001 - Discount - GCash - CC - MPConso"
					elif self.branch == "Garcia's Pawnshop - POB":
						row_values4.account = "4122-004 - Discount - GCash - POB - MPConso"
					elif self.branch == "Garcia's Pawnshop - MOL":
						row_values4.account = "4122-003 - Discount - GCash - MOL - MPConso"
					elif self.branch == "Garcia's Pawnshop - GTC":
						row_values4.account = "4122-002 - Discount - GCash - GTC - MPConso"
					elif self.branch == "Garcia's Pawnshop - TNZ":
						row_values4.account = "4122-005 - Discount - GCash - TNZ - MPConso"
					elif self.branch == "Rabie's House":
						row_values4.account = "4122-001 - Discount - GCash - CC - MPConso"
					row_values4.debit_in_account_currency = flt(self.discount)
					row_values4.credit_in_account_currency = flt(0)

				doc1.save(ignore_permissions=True)
				# doc1.submit()

			elif self.transaction_type == "Amortization" and self.mode_of_payment == "Bank Transfer":
				doc1 = frappe.new_doc('Journal Entry')
				doc1.voucher_type = 'Journal Entry'
				doc1.company = 'MP Consolidated'
				doc1.posting_date = self.date_issued
				doc1.reference_doctype = "Provisional Receipt"
				doc1.reference_document = self.name
				doc1.document_status = "Amortization"

				row_values1 = doc1.append('accounts', {})
				if self.bank == "BDO":
					row_values1.account = "1215-000 - Cash in Bank - BDO SM Ros - Php - MPConso"
				elif self.bank == "BPI":
					row_values1.account = "1205-000 - Cash in Bank - BPI Marquesa - MPConso"
				elif self.bank == "East West Cavite Branch":
					if self.branch == "Garcia's Pawnshop - CC":
						row_values1.account = "1235-001 - Cash in Bank - Eastwest PHP - CC - MPConso"
					elif self.branch == "Garcia's Pawnshop - POB":
						row_values1.account = "1235-004 - Cash in Bank - Eastwest PHP - POB - MPConso"
					elif self.branch == "Garcia's Pawnshop - MOL":
						row_values1.account = "1235-003 - Cash in Bank - Eastwest PHP - MOL - MPConso"
					elif self.branch == "Garcia's Pawnshop - GTC":
						row_values1.account = "1235-002 - Cash in Bank - Eastwest PHP - GTC - MPConso"
					elif self.branch == "Garcia's Pawnshop - TNZ":
						row_values1.account = "1235-005 - Cash in Bank - Eastwest PHP - TNZ - MPConso"
					elif self.branch == "Rabie's House":
						row_values1.account = "1235-001 - Cash in Bank - Eastwest PHP - CC - MPConso"
				row_values1.debit_in_account_currency = flt(self.total)
				row_values1.credit_in_account_currency = flt(0)
				
				if self.interest_payment > 0:
					row_values2 = doc1.append('accounts', {})
					if self.branch == "Garcia's Pawnshop - CC":
						row_values2.account = "4113-001 - Interest on Past Due Loans - NJ - CC - MPConso"
					elif self.branch == "Garcia's Pawnshop - GTC":
						row_values2.account = "4113-002 - Interest on Past Due Loans - NJ - GTC - MPConso"
					elif self.branch == "Garcia's Pawnshop - MOL":
						row_values2.account = "4113-003 - Interest on Past Due Loans - NJ - MOL - MPConso"
					elif self.branch == "Garcia's Pawnshop - POB":
						row_values2.account = "4113-004 - Interest on Past Due Loans - NJ - POB - MPConso"
					elif self.branch == "Garcia's Pawnshop - TNZ":
						row_values2.account = "4113-005 - Interest on Past Due Loans - NJ - TNZ - MPConso"
					elif self.branch == "Rabie's House":
						row_values2.account = "4113-001 - Interest on Past Due Loans - NJ - CC - MPConso"
					row_values2.debit_in_account_currency = flt(0)
					row_values2.credit_in_account_currency = flt(self.interest_payment)

				row_values3 = doc1.append('accounts', {})
				if self.branch == "Garcia's Pawnshop - CC":
					row_values3.account = "1615-001 - Pawned Items Inventory - NJ - CC - MPConso"
				elif self.branch == "Garcia's Pawnshop - GTC":
					row_values3.account = "1615-002 - Pawned Items Inventory - NJ - GTC - MPConso"
				elif self.branch == "Garcia's Pawnshop - MOL":
					row_values3.account = "1615-003 - Pawned Items Inventory - NJ - MOL - MPConso"
				elif self.branch == "Garcia's Pawnshop - POB":
					row_values3.account = "1615-004 - Pawned Items Inventory - NJ - POB - MPConso"
				elif self.branch == "Garcia's Pawnshop - TNZ":
					row_values3.account = "1615-005 - Pawned Items Inventory - NJ - TNZ - MPConso"
				elif self.branch == "Rabie's House":
					row_values3.account = "1615-001 - Pawned Items Inventory - NJ - CC - MPConso"
				row_values3.debit_in_account_currency = flt(0)
				row_values3.credit_in_account_currency = flt(self.total)

				doc1.save(ignore_permissions=True)
				# doc1.submit()

			elif self.transaction_type == "Renewal w/ Amortization" and self.mode_of_payment == "Bank Transfer":
				doc1 = frappe.new_doc('Journal Entry')
				doc1.voucher_type = 'Journal Entry'
				doc1.company = 'MP Consolidated'
				doc1.posting_date = self.date_issued
				doc1.reference_doctype = "Provisional Receipt"
				doc1.reference_document = self.name
				doc1.document_status = "Renewal w/ Amortization"

				row_values1 = doc1.append('accounts', {})
				if self.bank == "BDO":
					row_values1.account = "1215-000 - Cash in Bank - BDO SM Ros - Php - MPConso"
				elif self.bank == "BPI":
					row_values1.account = "1205-000 - Cash in Bank - BPI Marquesa - MPConso"
				elif self.bank == "East West Cavite Branch":
					if self.branch == "Garcia's Pawnshop - CC":
						row_values1.account = "1235-001 - Cash in Bank - Eastwest PHP - CC - MPConso"
					elif self.branch == "Garcia's Pawnshop - POB":
						row_values1.account = "1235-004 - Cash in Bank - Eastwest PHP - POB - MPConso"
					elif self.branch == "Garcia's Pawnshop - MOL":
						row_values1.account = "1235-003 - Cash in Bank - Eastwest PHP - MOL - MPConso"
					elif self.branch == "Garcia's Pawnshop - GTC":
						row_values1.account = "1235-002 - Cash in Bank - Eastwest PHP - GTC - MPConso"
					elif self.branch == "Garcia's Pawnshop - TNZ":
						row_values1.account = "1235-005 - Cash in Bank - Eastwest PHP - TNZ - MPConso"
					elif self.branch == "Rabie's House":
						row_values1.account = "1235-001 - Cash in Bank - Eastwest PHP - CC - MPConso"
				row_values1.debit_in_account_currency = flt(self.total)
				row_values1.credit_in_account_currency = flt(0)
				
				if self.interest_payment > 0:
					row_values2 = doc1.append('accounts', {})
					if self.branch == "Garcia's Pawnshop - CC":
						row_values2.account = "4113-001 - Interest on Past Due Loans - NJ - CC - MPConso"
					elif self.branch == "Garcia's Pawnshop - GTC":
						row_values2.account = "4113-002 - Interest on Past Due Loans - NJ - GTC - MPConso"
					elif self.branch == "Garcia's Pawnshop - MOL":
						row_values2.account = "4113-003 - Interest on Past Due Loans - NJ - MOL - MPConso"
					elif self.branch == "Garcia's Pawnshop - POB":
						row_values2.account = "4113-004 - Interest on Past Due Loans - NJ - POB - MPConso"
					elif self.branch == "Garcia's Pawnshop - TNZ":
						row_values2.account = "4113-005 - Interest on Past Due Loans - NJ - TNZ - MPConso"
					elif self.branch == "Rabie's House":
						row_values2.account = "4113-001 - Interest on Past Due Loans - NJ - CC - MPConso"
					row_values2.debit_in_account_currency = flt(0)
					row_values2.credit_in_account_currency = flt(self.interest_payment)

				row_values3 = doc1.append('accounts', {})
				if self.branch == "Garcia's Pawnshop - CC":
					row_values3.account = "4111-001 - Interest on Loans and Advances - NJ - CC - MPConso"
				elif self.branch == "Garcia's Pawnshop - GTC":
					row_values3.account = "4111-002 - Interest on Loans and Advances - NJ - GTC - MPConso"
				elif self.branch == "Garcia's Pawnshop - MOL":
					row_values3.account = "4111-003 - Interest on Loans and Advances - NJ - MOL - MPConso"
				elif self.branch == "Garcia's Pawnshop - POB":
					row_values3.account = "4111-004 - Interest on Loans and Advances - NJ - POB - MPConso"
				elif self.branch == "Garcia's Pawnshop - TNZ":
					row_values3.account = "4111-005 - Interest on Loans and Advances - NJ - TNZ - MPConso"
				elif self.branch == "Rabie's House":
					row_values3.account = "4111-001 - Interest on Loans and Advances - NJ - CC - MPConso"
				row_values3.debit_in_account_currency = flt(0)
				row_values3.credit_in_account_currency = flt(self.advance_interest)

				row_values4 = doc1.append('accounts', {})
				if self.branch == "Garcia's Pawnshop - CC":
					row_values4.account = "1615-001 - Pawned Items Inventory - NJ - CC - MPConso"
				elif self.branch == "Garcia's Pawnshop - GTC":
					row_values4.account = "1615-002 - Pawned Items Inventory - NJ - GTC - MPConso"
				elif self.branch == "Garcia's Pawnshop - MOL":
					row_values4.account = "1615-003 - Pawned Items Inventory - NJ - MOL - MPConso"
				elif self.branch == "Garcia's Pawnshop - POB":
					row_values4.account = "1615-004 - Pawned Items Inventory - NJ - POB - MPConso"
				elif self.branch == "Garcia's Pawnshop - TNZ":
					row_values4.account = "1615-005 - Pawned Items Inventory - NJ - TNZ - MPConso"
				elif self.branch == "Rabie's House":
					row_values4.account = "1615-001 - Pawned Items Inventory - NJ - CC - MPConso"
				row_values4.debit_in_account_currency = flt(0)
				row_values4.credit_in_account_currency = flt(self.additional_amortization)

				if flt(self.discount) > 0:
					row_values5 = doc1.append('accounts', {})
					if self.branch == "Garcia's Pawnshop - CC":
						row_values5.account = "4122-001 - Discount - GCash - CC - MPConso"
					elif self.branch == "Garcia's Pawnshop - POB":
						row_values5.account = "4122-004 - Discount - GCash - POB - MPConso"
					elif self.branch == "Garcia's Pawnshop - MOL":
						row_values5.account = "4122-003 - Discount - GCash - MOL - MPConso"
					elif self.branch == "Garcia's Pawnshop - GTC":
						row_values5.account = "4122-002 - Discount - GCash - GTC - MPConso"
					elif self.branch == "Garcia's Pawnshop - TNZ":
						row_values5.account = "4122-005 - Discount - GCash - TNZ - MPConso"
					elif self.branch == "Rabie's House":
						row_values5.account = "4122-001 - Discount - GCash - CC - MPConso"
					row_values5.debit_in_account_currency = flt(self.discount)
					row_values5.credit_in_account_currency = flt(0)

				doc1.save(ignore_permissions=True)
				# doc1.submit()

			elif self.transaction_type == "Interest Payment" and self.mode_of_payment == "Bank Transfer":
				doc1 = frappe.new_doc('Journal Entry')
				doc1.voucher_type = 'Journal Entry'
				doc1.company = 'MP Consolidated'
				doc1.posting_date = self.date_issued
				doc1.reference_doctype = "Provisional Receipt"
				doc1.reference_document = self.name
				doc1.document_status = "Interest Payment"

				row_values1 = doc1.append('accounts', {})
				if self.bank == "BDO":
					row_values1.account = "1215-000 - Cash in Bank - BDO SM Ros - Php - MPConso"
				elif self.bank == "BPI":
					row_values1.account = "1205-000 - Cash in Bank - BPI Marquesa - MPConso"
				elif self.bank == "East West Cavite Branch":
					if self.branch == "Garcia's Pawnshop - CC":
						row_values1.account = "1235-001 - Cash in Bank - Eastwest PHP - CC - MPConso"
					elif self.branch == "Garcia's Pawnshop - POB":
						row_values1.account = "1235-004 - Cash in Bank - Eastwest PHP - POB - MPConso"
					elif self.branch == "Garcia's Pawnshop - MOL":
						row_values1.account = "1235-003 - Cash in Bank - Eastwest PHP - MOL - MPConso"
					elif self.branch == "Garcia's Pawnshop - GTC":
						row_values1.account = "1235-002 - Cash in Bank - Eastwest PHP - GTC - MPConso"
					elif self.branch == "Garcia's Pawnshop - TNZ":
						row_values1.account = "1235-005 - Cash in Bank - Eastwest PHP - TNZ - MPConso"
					elif self.branch == "Rabie's House":
						row_values1.account = "1235-001 - Cash in Bank - Eastwest PHP - CC - MPConso"
				row_values1.debit_in_account_currency = flt(self.total)
				row_values1.credit_in_account_currency = flt(0)
				
				row_values2 = doc1.append('accounts', {})
				if self.branch == "Garcia's Pawnshop - CC":
					row_values2.account = "4113-001 - Interest on Past Due Loans - NJ - CC - MPConso"
				elif self.branch == "Garcia's Pawnshop - GTC":
					row_values2.account = "4113-002 - Interest on Past Due Loans - NJ - GTC - MPConso"
				elif self.branch == "Garcia's Pawnshop - MOL":
					row_values2.account = "4113-003 - Interest on Past Due Loans - NJ - MOL - MPConso"
				elif self.branch == "Garcia's Pawnshop - POB":
					row_values2.account = "4113-004 - Interest on Past Due Loans - NJ - POB - MPConso"
				elif self.branch == "Garcia's Pawnshop - TNZ":
					row_values2.account = "4113-005 - Interest on Past Due Loans - NJ - TNZ - MPConso"
				elif self.branch == "Rabie's House":
					row_values2.account = "4113-001 - Interest on Past Due Loans - NJ - CC - MPConso"
				row_values2.debit_in_account_currency = flt(0)
				row_values2.credit_in_account_currency = flt(self.total)

				doc1.save(ignore_permissions=True)
				# doc1.submit()

		# Journal Entry Creation for Jewelry
		elif self.pawn_ticket_type == "Pawn Ticket Jewelry":  #Renewal Cash
			# For Cash Accounts
			if self.transaction_type == "Renewal" and self.mode_of_payment == "Cash":			
				doc2 = frappe.new_doc('Journal Entry')
				doc2.voucher_type = 'Journal Entry'
				doc2.company = 'MP Consolidated'
				doc2.posting_date = self.date_issued
				doc2.reference_doctype = "Provisional Receipt"
				doc2.reference_document = self.name
				doc2.document_status = "Renewal"

				row_values1 = doc2.append('accounts', {})
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
				row_values1.debit_in_account_currency = flt(self.total)
				row_values1.credit_in_account_currency = flt(0)
				if self.interest_payment > 0:
					row_values2 = doc2.append('accounts', {})
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
					row_values2.credit_in_account_currency = flt(self.interest_payment)

				if flt(self.discount) > 0:
					row_values4 = doc2.append('accounts', {})
					if self.branch == "Garcia's Pawnshop - CC":
						row_values4.account = "4120-001 - Discount - J - CC - MPConso"
					elif self.branch == "Garcia's Pawnshop - GTC":
						row_values4.account = "4120-002 - Discount - J - GTC - MPConso"
					elif self.branch == "Garcia's Pawnshop - MOL":
						row_values4.account = "4120-003 - Discount - J - MOL - MPConso"
					elif self.branch == "Garcia's Pawnshop - POB":
						row_values4.account = "4120-004 - Discount - J - POB - MPConso"
					elif self.branch == "Garcia's Pawnshop - TNZ":
						row_values4.account = "4120-005 - Discount - J - TNZ - MPConso"
					elif self.branch == "Rabie's House":
						row_values4.account = "4120-001 - Discount - J - CC - MPConso"
					row_values4.debit_in_account_currency = flt(self.discount)
					row_values4.credit_in_account_currency = flt(0)

				row_values3 = doc2.append('accounts', {})
				if self.branch == "Garcia's Pawnshop - CC":
					row_values3.account = "4110-001 - Interest on Loans and Advances - J - CC - MPConso"
				elif self.branch == "Garcia's Pawnshop - GTC":
					row_values3.account = "4110-002 - Interest on Loans and Advances - J - GTC - MPConso"
				elif self.branch == "Garcia's Pawnshop - MOL":
					row_values3.account = "4110-003 - Interest on Loans and Advances - J - MOL - MPConso"
				elif self.branch == "Garcia's Pawnshop - POB":
					row_values3.account = "4110-004 - Interest on Loans and Advances - J - POB - MPConso"
				elif self.branch == "Garcia's Pawnshop - TNZ":
					row_values3.account = "4110-005 - Interest on Loans and Advances - J - TNZ - MPConso"
				elif self.branch == "Rabie's House":
					row_values3.account = "4110-001 - Interest on Loans and Advances - J - CC - MPConso"
				row_values3.debit_in_account_currency = flt(0)
				row_values3.credit_in_account_currency = flt(self.advance_interest)

				doc2.save(ignore_permissions=True)
				# doc2.submit()

			elif self.transaction_type == "Redemption" and self.mode_of_payment == "Cash":
				doc2 = frappe.new_doc('Journal Entry')
				doc2.voucher_type = 'Journal Entry'
				doc2.company = 'MP Consolidated'
				doc2.posting_date = self.date_issued
				doc2.reference_doctype = "Provisional Receipt"
				doc2.reference_document = self.name
				doc2.document_status = "Redemption"

				row_values1 = doc2.append('accounts', {})
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
				row_values1.debit_in_account_currency = flt(self.total)
				row_values1.credit_in_account_currency = flt(0)

				if flt(self.interest_payment) > 0:
					row_values2 = doc2.append('accounts', {})
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
					row_values2.credit_in_account_currency = flt(self.interest_payment)

				if flt(self.discount) > 0:
					row_values4 = doc2.append('accounts', {})
					if self.branch == "Garcia's Pawnshop - CC":
						row_values4.account = "4120-001 - Discount - J - CC - MPConso"
					elif self.branch == "Garcia's Pawnshop - GTC":
						row_values4.account = "4120-002 - Discount - J - GTC - MPConso"
					elif self.branch == "Garcia's Pawnshop - MOL":
						row_values4.account = "4120-003 - Discount - J - MOL - MPConso"
					elif self.branch == "Garcia's Pawnshop - POB":
						row_values4.account = "4120-004 - Discount - J - POB - MPConso"
					elif self.branch == "Garcia's Pawnshop - TNZ":
						row_values4.account = "4120-005 - Discount - J - TNZ - MPConso"
					elif self.branch == "Rabie's House":
						row_values4.account = "4120-001 - Discount - J - CC - MPConso"
					row_values4.debit_in_account_currency = flt(self.discount)
					row_values4.credit_in_account_currency = flt(0)

				row_values3 = doc2.append('accounts', {})
				if self.branch == "Garcia's Pawnshop - CC":
					row_values3.account = "1610-001 - Pawned Items Inventory - J - CC - MPConso"
				elif self.branch == "Garcia's Pawnshop - GTC":
					row_values3.account = "1610-002 - Pawned Items Inventory - J - GTC - MPConso"
				elif self.branch == "Garcia's Pawnshop - MOL":
					row_values3.account = "1610-003 - Pawned Items Inventory - J - MOL - MPConso"
				elif self.branch == "Garcia's Pawnshop - POB":
					row_values3.account = "1610-004 - Pawned Items Inventory - J - POB - MPConso"
				elif self.branch == "Garcia's Pawnshop - TNZ":
					row_values3.account = "1610-005 - Pawned Items Inventory - J - TNZ - MPConso"
				elif self.branch == "Rabie's House":
					row_values3.account = "1610-001 - Pawned Items Inventory - J - CC - MPConso"
				row_values3.debit_in_account_currency = flt(0)
				row_values3.credit_in_account_currency = flt(self.principal_amount)

				doc2.save(ignore_permissions=True)
				# doc2.submit()

			elif self.transaction_type == "Amortization" and self.mode_of_payment == "Cash":
				doc2 = frappe.new_doc('Journal Entry')
				doc2.voucher_type = 'Journal Entry'
				doc2.company = 'MP Consolidated'
				doc2.posting_date = self.date_issued
				doc2.reference_doctype = "Provisional Receipt"
				doc2.reference_document = self.name
				doc2.document_status = "Amortization"

				row_values1 = doc2.append('accounts', {})
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
				row_values1.debit_in_account_currency = flt(self.total)
				row_values1.credit_in_account_currency = flt(0)

				if self.interest_payment > 0:
					row_values2 = doc2.append('accounts', {})
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
					row_values2.credit_in_account_currency = flt(self.interest_payment)

				row_values3 = doc2.append('accounts', {})
				if self.branch == "Garcia's Pawnshop - CC":
					row_values3.account = "4110-001 - Interest on Loans and Advances - J - CC - MPConso"
				elif self.branch == "Garcia's Pawnshop - GTC":
					row_values3.account = "4110-002 - Interest on Loans and Advances - J - GTC - MPConso"
				elif self.branch == "Garcia's Pawnshop - MOL":
					row_values3.account = "4110-003 - Interest on Loans and Advances - J - MOL - MPConso"
				elif self.branch == "Garcia's Pawnshop - POB":
					row_values3.account = "4110-004 - Interest on Loans and Advances - J - POB - MPConso"
				elif self.branch == "Garcia's Pawnshop - TNZ":
					row_values3.account = "4110-005 - Interest on Loans and Advances - J - TNZ - MPConso"
				elif self.branch == "Rabie's House":
					row_values3.account = "4110-001 - Interest on Loans and Advances - J - CC - MPConso"
				row_values3.debit_in_account_currency = flt(0)
				row_values3.credit_in_account_currency = flt(self.total)

				doc2.save(ignore_permissions=True)
				# doc2.submit()

			elif self.transaction_type == "Renewal w/ Amortization" and self.mode_of_payment == "Cash":
				doc2 = frappe.new_doc('Journal Entry')
				doc2.voucher_type = 'Journal Entry'
				doc2.company = 'MP Consolidated'
				doc2.posting_date = self.date_issued
				doc2.reference_doctype = "Provisional Receipt"
				doc2.reference_document = self.name
				doc2.document_status = "Renewal w/ Amortization"

				row_values1 = doc2.append('accounts', {})
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
				row_values1.debit_in_account_currency = flt(self.total)
				row_values1.credit_in_account_currency = flt(0)
				
				if self.interest_payment > 0:
					row_values2 = doc2.append('accounts', {})
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
					row_values2.credit_in_account_currency = flt(self.interest_payment)
				
				row_values3 = doc2.append('accounts', {})
				if self.branch == "Garcia's Pawnshop - CC":
					row_values3.account = "4110-001 - Interest on Loans and Advances - J - CC - MPConso"
				elif self.branch == "Garcia's Pawnshop - GTC":
					row_values3.account = "4110-002 - Interest on Loans and Advances - J - GTC - MPConso"
				elif self.branch == "Garcia's Pawnshop - MOL":
					row_values3.account = "4110-003 - Interest on Loans and Advances - J - MOL - MPConso"
				elif self.branch == "Garcia's Pawnshop - POB":
					row_values3.account = "4110-004 - Interest on Loans and Advances - J - POB - MPConso"
				elif self.branch == "Garcia's Pawnshop - TNZ":
					row_values3.account = "4110-005 - Interest on Loans and Advances - J - TNZ - MPConso"
				elif self.branch == "Rabie's House":
					row_values3.account = "4110-001 - Interest on Loans and Advances - J - CC - MPConso"
				row_values3.debit_in_account_currency = flt(0)
				row_values3.credit_in_account_currency = flt(self.advance_interest)

				row_values4 = doc2.append('accounts', {})
				if self.branch == "Garcia's Pawnshop - CC":
					row_values4.account = "1610-001 - Pawned Items Inventory - J - CC - MPConso"
				elif self.branch == "Garcia's Pawnshop - GTC":
					row_values4.account = "1610-002 - Pawned Items Inventory - J - GTC - MPConso"
				elif self.branch == "Garcia's Pawnshop - MOL":
					row_values4.account = "1610-003 - Pawned Items Inventory - J - MOL - MPConso"
				elif self.branch == "Garcia's Pawnshop - POB":
					row_values4.account = "1610-004 - Pawned Items Inventory - J - POB - MPConso"
				elif self.branch == "Garcia's Pawnshop - TNZ":
					row_values4.account = "1610-005 - Pawned Items Inventory - J - TNZ - MPConso"
				elif self.branch == "Rabie's House":
					row_values4.account = "1610-001 - Pawned Items Inventory - J - CC - MPConso"
				row_values4.debit_in_account_currency = flt(0)
				row_values4.credit_in_account_currency = flt(self.additional_amortization)

				if flt(self.discount) > 0:
					row_values4 = doc2.append('accounts', {})
					if self.branch == "Garcia's Pawnshop - CC":
						row_values5.account = "4120-001 - Discount - J - CC - MPConso"
					elif self.branch == "Garcia's Pawnshop - GTC":
						row_values5.account = "4120-002 - Discount - J - GTC - MPConso"
					elif self.branch == "Garcia's Pawnshop - MOL":
						row_values5.account = "4120-003 - Discount - J - MOL - MPConso"
					elif self.branch == "Garcia's Pawnshop - POB":
						row_values5.account = "4120-004 - Discount - J - POB - MPConso"
					elif self.branch == "Garcia's Pawnshop - TNZ":
						row_values5.account = "4120-005 - Discount - J - TNZ - MPConso"
					elif self.branch == "Rabie's House":
						row_values5.account = "4120-001 - Discount - J - CC - MPConso"
					row_values4.debit_in_account_currency = flt(self.discount)
					row_values4.credit_in_account_currency = flt(0)

				doc2.save(ignore_permissions=True)
				# doc2.submit()
				
			elif self.transaction_type == "Interest Payment" and self.mode_of_payment == "Cash":
				doc2 = frappe.new_doc('Journal Entry')
				doc2.voucher_type = 'Journal Entry'
				doc2.company = 'MP Consolidated'
				doc2.posting_date = self.date_issued
				doc2.reference_doctype = "Provisional Receipt"
				doc2.reference_document = self.name
				doc2.document_status = "Interest Payment"

				row_values1 = doc2.append('accounts', {})
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
				row_values1.debit_in_account_currency = flt(self.total)
				row_values1.credit_in_account_currency = flt(0)

				row_values2 = doc2.append('accounts', {})
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
				row_values2.credit_in_account_currency = flt(self.total)

				doc2.save(ignore_permissions=True)
				# doc2.submit()

			# J GCash Transactions	
			elif self.transaction_type == "Renewal" and self.mode_of_payment == "GCash":			
				doc2 = frappe.new_doc('Journal Entry')
				doc2.voucher_type = 'Journal Entry'
				doc2.company = 'MP Consolidated'
				doc2.posting_date = self.date_issued
				doc2.reference_doctype = "Provisional Receipt"
				doc2.reference_document = self.name
				doc2.document_status = "Renewal"

				row_values1 = doc2.append('accounts', {})
				if self.branch == "Garcia's Pawnshop - CC":
					row_values1.account = "1235-001 - Cash in Bank - Eastwest PHP - CC - MPConso"
				elif self.branch == "Garcia's Pawnshop - POB":
					row_values1.account = "1235-004 - Cash in Bank - Eastwest PHP - POB - MPConso"
				elif self.branch == "Garcia's Pawnshop - MOL":
					row_values1.account = "1235-003 - Cash in Bank - Eastwest PHP - MOL - MPConso"
				elif self.branch == "Garcia's Pawnshop - GTC":
					row_values1.account = "1235-002 - Cash in Bank - Eastwest PHP - GTC - MPConso"
				elif self.branch == "Garcia's Pawnshop - TNZ":
					row_values1.account = "1235-005 - Cash in Bank - Eastwest PHP - TNZ - MPConso"
				elif self.branch == "Rabie's House":
					row_values1.account = "1235-001 - Cash in Bank - Eastwest PHP - CC - MPConso"
				row_values1.debit_in_account_currency = (flt(self.total) - (flt(self.total) * 0.02)) + (((flt(self.total) * 0.02) / 1.12) * 0.02)
				row_values1.credit_in_account_currency = flt(0)

				row_values2 = doc2.append('accounts', {})
				if self.branch == "Garcia's Pawnshop - CC":
					row_values2.account = "4122-001 - Discount - GCash - CC - MPConso"
				elif self.branch == "Garcia's Pawnshop - POB":
					row_values2.account = "4122-004 - Discount - GCash - POB - MPConso"
				elif self.branch == "Garcia's Pawnshop - MOL":
					row_values2.account = "4122-003 - Discount - GCash - MOL - MPConso"
				elif self.branch == "Garcia's Pawnshop - GTC":
					row_values2.account = "4122-002 - Discount - GCash - GTC - MPConso"
				elif self.branch == "Garcia's Pawnshop - TNZ":
					row_values2.account = "4122-005 - Discount - GCash - TNZ - MPConso"
				elif self.branch == "Rabie's House":
					row_values2.account = "4122-001 - Discount - GCash - CC - MPConso"
				row_values2.debit_in_account_currency = (flt(self.total) * 0.02)
				row_values2.credit_in_account_currency = flt(0)

				if self.interest_payment > 0:
					row_values3 = doc2.append('accounts', {})
					if self.branch == "Garcia's Pawnshop - CC":
						row_values3.account = "4112-001 - Interest on Past Due Loans - J - CC - MPConso"
					elif self.branch == "Garcia's Pawnshop - GTC":
						row_values3.account = "4112-002 - Interest on Past Due Loans - J - GTC - MPConso"
					elif self.branch == "Garcia's Pawnshop - MOL":
						row_values3.account = "4112-003 - Interest on Past Due Loans - J - MOL - MPConso"
					elif self.branch == "Garcia's Pawnshop - POB":
						row_values3.account = "4112-004 - Interest on Past Due Loans - J - POB - MPConso"
					elif self.branch == "Garcia's Pawnshop - TNZ":
						row_values3.account = "4112-005 - Interest on Past Due Loans - J - TNZ - MPConso"
					elif self.branch == "Rabie's House":
						row_values3.account = "4112-001 - Interest on Past Due Loans - J - CC - MPConso"
					row_values3.debit_in_account_currency = flt(0)
					row_values3.credit_in_account_currency = flt(self.interest_payment)

				if flt(self.discount) > 0:
					row_values6 = doc2.append('accounts', {})
					if self.branch == "Garcia's Pawnshop - CC":
						row_values6.account = "4120-001 - Discount - J - CC - MPConso"
					elif self.branch == "Garcia's Pawnshop - POB":
						row_values6.account = "4120-004 - Discount - J - POB - MPConso"
					elif self.branch == "Garcia's Pawnshop - MOL":
						row_values6.account = "4120-003 - Discount - J - MOL - MPConso"
					elif self.branch == "Garcia's Pawnshop - GTC":
						row_values6.account = "4120-002 - Discount - J - GTC - MPConso"
					elif self.branch == "Garcia's Pawnshop - TNZ":
						row_values6.account = "4120-005 - Discount - J - TNZ - MPConso"
					elif self.branch == "Rabie's House":
						row_values6.account = "4120-001 - Discount - J - CC - MPConso"
					row_values6.debit_in_account_currency = flt(self.discount)
					row_values6.credit_in_account_currency = flt(0)
				
				row_values4 = doc2.append('accounts', {})
				if self.branch == "Garcia's Pawnshop - CC":
					row_values4.account = "4110-001 - Interest on Loans and Advances - J - CC - MPConso"
				elif self.branch == "Garcia's Pawnshop - GTC":
					row_values4.account = "4110-002 - Interest on Loans and Advances - J - GTC - MPConso"
				elif self.branch == "Garcia's Pawnshop - MOL":
					row_values4.account = "4110-003 - Interest on Loans and Advances - J - MOL - MPConso"
				elif self.branch == "Garcia's Pawnshop - POB":
					row_values4.account = "4110-004 - Interest on Loans and Advances - J - POB - MPConso"
				elif self.branch == "Garcia's Pawnshop - TNZ":
					row_values4.account = "4110-005 - Interest on Loans and Advances - J - TNZ - MPConso"
				elif self.branch == "Rabie's House":
					row_values4.account = "4110-001 - Interest on Loans and Advances - J - CC - MPConso"
				row_values4.debit_in_account_currency = flt(0)
				row_values4.credit_in_account_currency = flt(self.advance_interest)
				
				row_values5 = doc2.append('accounts', {})
				if self.branch == "Garcia's Pawnshop - CC":
					row_values5.account = "2315-001 - Withholding Tax Payable - Expanded - CC - MPConso"
				elif self.branch == "Garcia's Pawnshop - GTC":
					row_values5.account = "2315-002 - Withholding Tax Payable - Expanded - GTC - MPConso"
				elif self.branch == "Garcia's Pawnshop - MOL":
					row_values5.account = "2315-003 - Withholding Tax Payable - Expanded - MOL - MPConso"
				elif self.branch == "Garcia's Pawnshop - POB":
					row_values5.account = "2315-004 - Withholding Tax Payable - Expanded - POB - MPConso"
				elif self.branch == "Garcia's Pawnshop - TNZ":
					row_values5.account = "2315-005 - Withholding Tax Payable - Expanded - TNZ - MPConso"
				elif self.branch == "Rabie's House":
					row_values5.account = "2315-001 - Withholding Tax Payable - Expanded - CC - MPConso"
				row_values5.debit_in_account_currency = flt(0)
				row_values5.credit_in_account_currency = ((flt(self.total) * 0.02) / 1.12) * 0.02

				doc2.save(ignore_permissions=True)
				# doc2.submit()

			elif self.transaction_type == "Redemption" and self.mode_of_payment == "GCash":
				doc2 = frappe.new_doc('Journal Entry')
				doc2.voucher_type = 'Journal Entry'
				doc2.company = 'MP Consolidated'
				doc2.posting_date = self.date_issued
				doc2.reference_doctype = "Provisional Receipt"
				doc2.reference_document = self.name
				doc2.document_status = "Redemption"

				row_values1 = doc2.append('accounts', {})
				if self.branch == "Garcia's Pawnshop - CC":
					row_values1.account = "1235-001 - Cash in Bank - Eastwest PHP - CC - MPConso"
				elif self.branch == "Garcia's Pawnshop - POB":
					row_values1.account = "1235-004 - Cash in Bank - Eastwest PHP - POB - MPConso"
				elif self.branch == "Garcia's Pawnshop - MOL":
					row_values1.account = "1235-003 - Cash in Bank - Eastwest PHP - MOL - MPConso"
				elif self.branch == "Garcia's Pawnshop - GTC":
					row_values1.account = "1235-002 - Cash in Bank - Eastwest PHP - GTC - MPConso"
				elif self.branch == "Garcia's Pawnshop - TNZ":
					row_values1.account = "1235-005 - Cash in Bank - Eastwest PHP - TNZ - MPConso"
				elif self.branch == "Rabie's House":
					row_values1.account = "1235-001 - Cash in Bank - Eastwest PHP - CC - MPConso"
				row_values1.debit_in_account_currency = (flt(self.total) - (flt(self.total) * 0.02)) + (((flt(self.total) * 0.02) / 1.12) * 0.02)
				row_values1.credit_in_account_currency = flt(0)

				row_values2 = doc2.append('accounts', {})
				if self.branch == "Garcia's Pawnshop - CC":
					row_values2.account = "4122-001 - Discount - GCash - CC - MPConso"
				elif self.branch == "Garcia's Pawnshop - POB":
					row_values2.account = "4122-004 - Discount - GCash - POB - MPConso"
				elif self.branch == "Garcia's Pawnshop - MOL":
					row_values2.account = "4122-003 - Discount - GCash - MOL - MPConso"
				elif self.branch == "Garcia's Pawnshop - GTC":
					row_values2.account = "4122-002 - Discount - GCash - GTC - MPConso"
				elif self.branch == "Garcia's Pawnshop - TNZ":
					row_values2.account = "4122-005 - Discount - GCash - TNZ - MPConso"
				elif self.branch == "Rabie's House":
					row_values2.account = "4122-001 - Discount - GCash - CC - MPConso"
				row_values2.debit_in_account_currency = (flt(self.total) * 0.02)
				row_values2.credit_in_account_currency = flt(0)

				if self.interest_payment > 0:
					row_values4 = doc2.append('accounts', {})
					if self.branch == "Garcia's Pawnshop - CC":
						row_values4.account = "4112-001 - Interest on Past Due Loans - J - CC - MPConso"
					elif self.branch == "Garcia's Pawnshop - GTC":
						row_values4.account = "4112-002 - Interest on Past Due Loans - J - GTC - MPConso"
					elif self.branch == "Garcia's Pawnshop - MOL":
						row_values4.account = "4112-003 - Interest on Past Due Loans - J - MOL - MPConso"
					elif self.branch == "Garcia's Pawnshop - POB":
						row_values4.account = "4112-004 - Interest on Past Due Loans - J - POB - MPConso"
					elif self.branch == "Garcia's Pawnshop - TNZ":
						row_values4.account = "4112-005 - Interest on Past Due Loans - J - TNZ - MPConso"
					elif self.branch == "Rabie's House":
						row_values4.account = "4112-001 - Interest on Past Due Loans - J - CC - MPConso"
					row_values4.debit_in_account_currency = flt(0)
					row_values4.credit_in_account_currency = flt(self.interest_payment)

				if flt(self.discount) > 0:
					row_values7 = doc2.append('accounts', {})
					if self.branch == "Garcia's Pawnshop - CC":
						row_values7.account = "4120-001 - Discount - J - CC - MPConso"
					elif self.branch == "Garcia's Pawnshop - POB":
						row_values7.account = "4120-004 - Discount - J - POB - MPConso"
					elif self.branch == "Garcia's Pawnshop - MOL":
						row_values7.account = "4120-003 - Discount - J - MOL - MPConso"
					elif self.branch == "Garcia's Pawnshop - GTC":
						row_values7.account = "4120-002 - Discount - J - GTC - MPConso"
					elif self.branch == "Garcia's Pawnshop - TNZ":
						row_values7.account = "4120-005 - Discount - J - TNZ - MPConso"
					elif self.branch == "Rabie's House":
						row_values7.account = "4120-001 - Discount - J - CC - MPConso"
					row_values7.debit_in_account_currency = flt(self.discount)
					row_values7.credit_in_account_currency = flt(0)

				row_values5 = doc2.append('accounts', {})
				if self.branch == "Garcia's Pawnshop - CC":
					row_values5.account = "1610-001 - Pawned Items Inventory - J - CC - MPConso"
				elif self.branch == "Garcia's Pawnshop - GTC":
					row_values5.account = "1610-002 - Pawned Items Inventory - J - GTC - MPConso"
				elif self.branch == "Garcia's Pawnshop - MOL":
					row_values5.account = "1610-003 - Pawned Items Inventory - J - MOL - MPConso"
				elif self.branch == "Garcia's Pawnshop - POB":
					row_values5.account = "1610-004 - Pawned Items Inventory - J - POB - MPConso"
				elif self.branch == "Garcia's Pawnshop - TNZ":
					row_values5.account = "1610-005 - Pawned Items Inventory - J - TNZ - MPConso"
				elif self.branch == "Rabie's House":
					row_values5.account = "1610-001 - Pawned Items Inventory - J - CC - MPConso"
				row_values5.debit_in_account_currency = flt(0)
				row_values5.credit_in_account_currency = flt(self.principal_amount)
				
				row_values6 = doc2.append('accounts', {})
				if self.branch == "Garcia's Pawnshop - CC":
					row_values6.account = "2315-001 - Withholding Tax Payable - Expanded - CC - MPConso"
				elif self.branch == "Garcia's Pawnshop - GTC":
					row_values6.account = "2315-002 - Withholding Tax Payable - Expanded - GTC - MPConso"
				elif self.branch == "Garcia's Pawnshop - MOL":
					row_values6.account = "2315-003 - Withholding Tax Payable - Expanded - MOL - MPConso"
				elif self.branch == "Garcia's Pawnshop - POB":
					row_values6.account = "2315-004 - Withholding Tax Payable - Expanded - POB - MPConso"
				elif self.branch == "Garcia's Pawnshop - TNZ":
					row_values6.account = "2315-005 - Withholding Tax Payable - Expanded - TNZ - MPConso"
				elif self.branch == "Rabie's House":
					row_values6.account = "2315-001 - Withholding Tax Payable - Expanded - CC - MPConso"
				row_values6.debit_in_account_currency = flt(0)
				row_values6.credit_in_account_currency = ((flt(self.total) * 0.02) / 1.12) * 0.02

				doc2.save(ignore_permissions=True)
				# doc2.submit()

			elif self.transaction_type == "Amortization" and self.mode_of_payment == "GCash":
				doc2 = frappe.new_doc('Journal Entry')
				doc2.voucher_type = 'Journal Entry'
				doc2.company = 'MP Consolidated'
				doc2.posting_date = self.date_issued
				doc2.reference_doctype = "Provisional Receipt"
				doc2.reference_document = self.name
				doc2.document_status = "Amortization"

				row_values1 = doc2.append('accounts', {})
				if self.branch == "Garcia's Pawnshop - CC":
					row_values1.account = "1235-001 - Cash in Bank - Eastwest PHP - CC - MPConso"
				elif self.branch == "Garcia's Pawnshop - POB":
					row_values1.account = "1235-004 - Cash in Bank - Eastwest PHP - POB - MPConso"
				elif self.branch == "Garcia's Pawnshop - MOL":
					row_values1.account = "1235-003 - Cash in Bank - Eastwest PHP - MOL - MPConso"
				elif self.branch == "Garcia's Pawnshop - GTC":
					row_values1.account = "1235-002 - Cash in Bank - Eastwest PHP - GTC - MPConso"
				elif self.branch == "Garcia's Pawnshop - TNZ":
					row_values1.account = "1235-005 - Cash in Bank - Eastwest PHP - TNZ - MPConso"
				elif self.branch == "Rabie's House":
					row_values1.account = "1235-001 - Cash in Bank - Eastwest PHP - CC - MPConso"
				row_values1.debit_in_account_currency = (flt(self.total) - (flt(self.total) * 0.02)) + (((flt(self.total) * 0.02) / 1.12) * 0.02)
				row_values1.credit_in_account_currency = flt(0)

				row_values2 = doc2.append('accounts', {})
				if self.branch == "Garcia's Pawnshop - CC":
					row_values2.account = "4122-001 - Discount - GCash - CC - MPConso"
				elif self.branch == "Garcia's Pawnshop - POB":
					row_values2.account = "4122-004 - Discount - GCash - POB - MPConso"
				elif self.branch == "Garcia's Pawnshop - MOL":
					row_values2.account = "4122-003 - Discount - GCash - MOL - MPConso"
				elif self.branch == "Garcia's Pawnshop - GTC":
					row_values2.account = "4122-002 - Discount - GCash - GTC - MPConso"
				elif self.branch == "Garcia's Pawnshop - TNZ":
					row_values2.account = "4122-005 - Discount - GCash - TNZ - MPConso"
				elif self.branch == "Rabie's House":
					row_values2.account = "4122-001 - Discount - GCash - CC - MPConso"
				row_values2.debit_in_account_currency = (flt(self.total) * 0.02)
				row_values2.credit_in_account_currency = flt(0)

				row_values5 = doc2.append('accounts', {})
				if self.branch == "Garcia's Pawnshop - CC":
					row_values5.account = "1610-001 - Pawned Items Inventory - J - CC - MPConso"
				elif self.branch == "Garcia's Pawnshop - GTC":
					row_values5.account = "1610-002 - Pawned Items Inventory - J - GTC - MPConso"
				elif self.branch == "Garcia's Pawnshop - MOL":
					row_values5.account = "1610-003 - Pawned Items Inventory - J - MOL - MPConso"
				elif self.branch == "Garcia's Pawnshop - POB":
					row_values5.account = "1610-004 - Pawned Items Inventory - J - POB - MPConso"
				elif self.branch == "Garcia's Pawnshop - TNZ":
					row_values5.account = "1610-005 - Pawned Items Inventory - J - TNZ - MPConso"
				elif self.branch == "Rabie's House":
					row_values5.account = "1610-001 - Pawned Items Inventory - J - CC - MPConso"
				row_values5.debit_in_account_currency = flt(0)
				row_values5.credit_in_account_currency = flt(self.total)

				row_values6 = doc2.append('accounts', {})
				if self.branch == "Garcia's Pawnshop - CC":
					row_values6.account = "2315-001 - Withholding Tax Payable - Expanded - CC - MPConso"
				elif self.branch == "Garcia's Pawnshop - GTC":
					row_values6.account = "2315-002 - Withholding Tax Payable - Expanded - GTC - MPConso"
				elif self.branch == "Garcia's Pawnshop - MOL":
					row_values6.account = "2315-003 - Withholding Tax Payable - Expanded - MOL - MPConso"
				elif self.branch == "Garcia's Pawnshop - POB":
					row_values6.account = "2315-004 - Withholding Tax Payable - Expanded - POB - MPConso"
				elif self.branch == "Garcia's Pawnshop - TNZ":
					row_values6.account = "2315-005 - Withholding Tax Payable - Expanded - TNZ - MPConso"
				elif self.branch == "Rabie's House":
					row_values6.account = "2315-001 - Withholding Tax Payable - Expanded - CC - MPConso"
				row_values6.debit_in_account_currency = flt(0)
				row_values6.credit_in_account_currency = ((flt(self.total) * 0.02) / 1.12) * 0.02

				doc2.save(ignore_permissions=True)
				# doc2.submit()

			elif self.transaction_type == "Renewal w/ Amortization" and self.mode_of_payment == "GCash":
				doc2 = frappe.new_doc('Journal Entry')
				doc2.voucher_type = 'Journal Entry'
				doc2.company = 'MP Consolidated'
				doc2.posting_date = self.date_issued
				doc2.reference_doctype = "Provisional Receipt"
				doc2.reference_document = self.name
				doc2.document_status = "Renewal w/ Amortization"

				row_values1 = doc2.append('accounts', {})
				if self.branch == "Garcia's Pawnshop - CC":
					row_values1.account = "1235-001 - Cash in Bank - Eastwest PHP - CC - MPConso"
				elif self.branch == "Garcia's Pawnshop - POB":
					row_values1.account = "1235-004 - Cash in Bank - Eastwest PHP - POB - MPConso"
				elif self.branch == "Garcia's Pawnshop - MOL":
					row_values1.account = "1235-003 - Cash in Bank - Eastwest PHP - MOL - MPConso"
				elif self.branch == "Garcia's Pawnshop - GTC":
					row_values1.account = "1235-002 - Cash in Bank - Eastwest PHP - GTC - MPConso"
				elif self.branch == "Garcia's Pawnshop - TNZ":
					row_values1.account = "1235-005 - Cash in Bank - Eastwest PHP - TNZ - MPConso"
				elif self.branch == "Rabie's House":
					row_values1.account = "1235-001 - Cash in Bank - Eastwest PHP - CC - MPConso"
				row_values1.debit_in_account_currency = (flt(self.total) - (flt(self.total) * 0.02)) + (((flt(self.total) * 0.02) / 1.12) * 0.02)
				row_values1.credit_in_account_currency = flt(0)

				row_values2 = doc2.append('accounts', {})
				if self.branch == "Garcia's Pawnshop - CC":
					row_values1.account = "4122-001 - Discount - GCash - CC - MPConso"
				elif self.branch == "Garcia's Pawnshop - POB":
					row_values1.account = "4122-004 - Discount - GCash - POB - MPConso"
				elif self.branch == "Garcia's Pawnshop - MOL":
					row_values1.account = "4122-003 - Discount - GCash - MOL - MPConso"
				elif self.branch == "Garcia's Pawnshop - GTC":
					row_values1.account = "4122-002 - Discount - GCash - GTC - MPConso"
				elif self.branch == "Garcia's Pawnshop - TNZ":
					row_values1.account = "4122-005 - Discount - GCash - TNZ - MPConso"
				elif self.branch == "Rabie's House":
					row_values1.account = "4122-001 - Discount - GCash - CC - MPConso"
				row_values2.debit_in_account_currency = (flt(self.total) * 0.02)
				row_values2.credit_in_account_currency = flt(0)

				if self.interest_payment > 0:
					row_values4 = doc2.append('accounts', {})
					if self.branch == "Garcia's Pawnshop - CC":
						row_values4.account = "4112-001 - Interest on Past Due Loans - J - CC - MPConso"
					elif self.branch == "Garcia's Pawnshop - GTC":
						row_values4.account = "4112-002 - Interest on Past Due Loans - J - GTC - MPConso"
					elif self.branch == "Garcia's Pawnshop - MOL":
						row_values4.account = "4112-003 - Interest on Past Due Loans - J - MOL - MPConso"
					elif self.branch == "Garcia's Pawnshop - POB":
						row_values4.account = "4112-004 - Interest on Past Due Loans - J - POB - MPConso"
					elif self.branch == "Garcia's Pawnshop - TNZ":
						row_values4.account = "4112-005 - Interest on Past Due Loans - J - TNZ - MPConso"
					elif self.branch == "Rabie's House":
						row_values4.account = "4112-001 - Interest on Past Due Loans - J - CC - MPConso"
					row_values4.debit_in_account_currency = flt(0)
					row_values4.credit_in_account_currency = flt(self.interest_payment)

				row_values5 = doc2.append('accounts', {})
				if self.branch == "Garcia's Pawnshop - CC":
					row_values5.account = "1610-001 - Pawned Items Inventory - J - CC - MPConso"
				elif self.branch == "Garcia's Pawnshop - GTC":
					row_values5.account = "1610-002 - Pawned Items Inventory - J - GTC - MPConso"
				elif self.branch == "Garcia's Pawnshop - MOL":
					row_values5.account = "1610-003 - Pawned Items Inventory - J - MOL - MPConso"
				elif self.branch == "Garcia's Pawnshop - POB":
					row_values5.account = "1610-004 - Pawned Items Inventory - J - POB - MPConso"
				elif self.branch == "Garcia's Pawnshop - TNZ":
					row_values5.account = "1610-005 - Pawned Items Inventory - J - TNZ - MPConso"
				elif self.branch == "Rabie's House":
					row_values5.account = "1610-001 - Pawned Items Inventory - J - CC - MPConso"
				row_values5.debit_in_account_currency = flt(0)
				row_values5.credit_in_account_currency = flt(self.additional_amortization)

				row_values6 = doc2.append('accounts', {})
				if self.branch == "Garcia's Pawnshop - CC":
					row_values6.account = "4110-001 - Interest on Loans and Advances - J - CC - MPConso"
				elif self.branch == "Garcia's Pawnshop - GTC":
					row_values6.account = "4110-002 - Interest on Loans and Advances - J - GTC - MPConso"
				elif self.branch == "Garcia's Pawnshop - MOL":
					row_values6.account = "4110-003 - Interest on Loans and Advances - J - MOL - MPConso"
				elif self.branch == "Garcia's Pawnshop - POB":
					row_values6.account = "4110-004 - Interest on Loans and Advances - J - POB - MPConso"
				elif self.branch == "Garcia's Pawnshop - TNZ":
					row_values6.account = "4110-005 - Interest on Loans and Advances - J - TNZ - MPConso"
				elif self.branch == "Rabie's House":
					row_values3.account = "4110-001 - Interest on Loans and Advances - J - CC - MPConso"
				row_values6.credit_in_account_currency = flt(self.advance_interest)

				row_values7 = doc2.append('accounts', {})
				if self.branch == "Garcia's Pawnshop - CC":
					row_values7.account = "2315-001 - Withholding Tax Payable - Expanded - CC - MPConso"
				elif self.branch == "Garcia's Pawnshop - GTC":
					row_values7.account = "2315-002 - Withholding Tax Payable - Expanded - GTC - MPConso"
				elif self.branch == "Garcia's Pawnshop - MOL":
					row_values7.account = "2315-003 - Withholding Tax Payable - Expanded - MOL - MPConso"
				elif self.branch == "Garcia's Pawnshop - POB":
					row_values7.account = "2315-004 - Withholding Tax Payable - Expanded - POB - MPConso"
				elif self.branch == "Garcia's Pawnshop - TNZ":
					row_values7.account = "2315-005 - Withholding Tax Payable - Expanded - TNZ - MPConso"
				elif self.branch == "Rabie's House":
					row_values7.account = "2315-001 - Withholding Tax Payable - Expanded - CC - MPConso"
				row_values7.debit_in_account_currency = flt(0)
				row_values7.credit_in_account_currency = ((flt(self.total) * 0.02) / 1.12) * 0.02

				if flt(self.discount) > 0:
					row_values8 = doc2.append('accounts', {})
					if self.branch == "Garcia's Pawnshop - CC":
						row_values8.account = "4120-001 - Discount - J - CC - MPConso"
					elif self.branch == "Garcia's Pawnshop - GTC":
						row_values8.account = "4120-002 - Discount - J - GTC - MPConso"
					elif self.branch == "Garcia's Pawnshop - MOL":
						row_values8.account = "4120-003 - Discount - J - MOL - MPConso"
					elif self.branch == "Garcia's Pawnshop - POB":
						row_values8.account = "4120-004 - Discount - J - POB - MPConso"
					elif self.branch == "Garcia's Pawnshop - TNZ":
						row_values8.account = "4120-005 - Discount - J - TNZ - MPConso"
					elif self.branch == "Rabie's House":
						row_values8.account == "4120-001 - Discount - J - CC - MPConso"
					row_values8.debit_in_account_currency = flt(self.discount)
					row_values8.credit_in_account_currency = flt(0)

				doc2.save(ignore_permissions=True)
				# doc2.submit()
				
			elif self.transaction_type == "Interest Payment" and self.mode_of_payment == "GCash":
				doc2 = frappe.new_doc('Journal Entry')
				doc2.voucher_type = 'Journal Entry'
				doc2.company = 'MP Consolidated'
				doc2.posting_date = self.date_issued
				doc2.reference_doctype = "Provisional Receipt"
				doc2.reference_document = self.name
				doc2.document_status = "Interest Payment"

				row_values1 = doc2.append('accounts', {})
				if self.branch == "Garcia's Pawnshop - CC":
					row_values1.account = "1235-001 - Cash in Bank - Eastwest PHP - CC - MPConso"
				elif self.branch == "Garcia's Pawnshop - POB":
					row_values1.account = "1235-004 - Cash in Bank - Eastwest PHP - POB - MPConso"
				elif self.branch == "Garcia's Pawnshop - MOL":
					row_values1.account = "1235-003 - Cash in Bank - Eastwest PHP - MOL - MPConso"
				elif self.branch == "Garcia's Pawnshop - GTC":
					row_values1.account = "1235-002 - Cash in Bank - Eastwest PHP - GTC - MPConso"
				elif self.branch == "Garcia's Pawnshop - TNZ":
					row_values1.account = "1235-005 - Cash in Bank - Eastwest PHP - TNZ - MPConso"
				elif self.branch == "Rabie's House":
					row_values1.account = "1235-001 - Cash in Bank - Eastwest PHP - CC - MPConso"
				row_values1.debit_in_account_currency = (flt(self.total) - (flt(self.total) * 0.02)) + (((flt(self.total) * 0.02) / 1.12) * 0.02)
				row_values1.credit_in_account_currency = flt(0)

				row_values2 = doc2.append('accounts', {})
				if self.branch == "Garcia's Pawnshop - CC":
					row_values1.account = "4122-001 - Discount - GCash - CC - MPConso"
				elif self.branch == "Garcia's Pawnshop - POB":
					row_values1.account = "4122-004 - Discount - GCash - POB - MPConso"
				elif self.branch == "Garcia's Pawnshop - MOL":
					row_values1.account = "4122-003 - Discount - GCash - MOL - MPConso"
				elif self.branch == "Garcia's Pawnshop - GTC":
					row_values1.account = "4122-002 - Discount - GCash - GTC - MPConso"
				elif self.branch == "Garcia's Pawnshop - TNZ":
					row_values1.account = "4122-005 - Discount - GCash - TNZ - MPConso"
				elif self.branch == "Rabie's House":
					row_values1.account = "4122-001 - Discount - GCash - CC - MPConso"
				row_values2.debit_in_account_currency = (flt(self.total) * 0.02)
				row_values2.credit_in_account_currency = flt(0)

				row_values4 = doc2.append('accounts', {})
				if self.branch == "Garcia's Pawnshop - CC":
					row_values4.account = "4112-001 - Interest on Past Due Loans - J - CC - MPConso"
				elif self.branch == "Garcia's Pawnshop - GTC":
					row_values4.account = "4112-002 - Interest on Past Due Loans - J - GTC - MPConso"
				elif self.branch == "Garcia's Pawnshop - MOL":
					row_values4.account = "4112-003 - Interest on Past Due Loans - J - MOL - MPConso"
				elif self.branch == "Garcia's Pawnshop - POB":
					row_values4.account = "4112-004 - Interest on Past Due Loans - J - POB - MPConso"
				elif self.branch == "Garcia's Pawnshop - TNZ":
					row_values4.account = "4112-005 - Interest on Past Due Loans - J - TNZ - MPConso"
				elif self.branch == "Rabie's House":
					row_values4.account = "4112-001 - Interest on Past Due Loans - J - CC - MPConso"
				row_values4.debit_in_account_currency = flt(0)
				row_values4.credit_in_account_currency = flt(self.total)

				row_values5 = doc2.append('accounts', {})
				if self.branch == "Garcia's Pawnshop - CC":
					row_values5.account = "2315-001 - Withholding Tax Payable - Expanded - CC - MPConso"
				elif self.branch == "Garcia's Pawnshop - GTC":
					row_values5.account = "2315-002 - Withholding Tax Payable - Expanded - GTC - MPConso"
				elif self.branch == "Garcia's Pawnshop - MOL":
					row_values5.account = "2315-003 - Withholding Tax Payable - Expanded - MOL - MPConso"
				elif self.branch == "Garcia's Pawnshop - POB":
					row_values5.account = "2315-004 - Withholding Tax Payable - Expanded - POB - MPConso"
				elif self.branch == "Garcia's Pawnshop - TNZ":
					row_values5.account = "2315-005 - Withholding Tax Payable - Expanded - TNZ - MPConso"
				elif self.branch == "Rabie's House":
					row_values5.account = "2315-001 - Withholding Tax Payable - Expanded - CC - MPConso"
				row_values5.debit_in_account_currency = flt(0)
				row_values5.credit_in_account_currency = ((flt(self.total) * 0.02) / 1.12) * 0.02

				doc2.save(ignore_permissions=True)
				# doc2.submit()

			# J Bank Transfer Transactions
			elif self.transaction_type == "Renewal" and self.mode_of_payment == "Bank Transfer":
				doc2 = frappe.new_doc('Journal Entry')
				doc2.voucher_type = 'Journal Entry'
				doc2.company = 'MP Consolidated'
				doc2.posting_date = self.date_issued
				doc2.reference_doctype = "Provisional Receipt"
				doc2.reference_document = self.name
				doc2.document_status = "Renewal"

				row_values1 = doc2.append('accounts', {})
				if self.bank == "BDO":
					row_values1.account = "1215-000 - Cash in Bank - BDO SM Ros - Php - MPConso"
				elif self.bank == "BPI":
					row_values1.account = "1205-000 - Cash in Bank - BPI Marquesa - MPConso"
				elif self.bank == "East West Cavite Branch":
					if self.branch == "Garcia's Pawnshop - CC":
						row_values1.account = "1235-001 - Cash in Bank - Eastwest PHP - CC - MPConso"
					elif self.branch == "Garcia's Pawnshop - POB":
						row_values1.account = "1235-004 - Cash in Bank - Eastwest PHP - POB - MPConso"
					elif self.branch == "Garcia's Pawnshop - MOL":
						row_values1.account = "1235-003 - Cash in Bank - Eastwest PHP - MOL - MPConso"
					elif self.branch == "Garcia's Pawnshop - GTC":
						row_values1.account = "1235-002 - Cash in Bank - Eastwest PHP - GTC - MPConso"
					elif self.branch == "Garcia's Pawnshop - TNZ":
						row_values1.account = "1235-005 - Cash in Bank - Eastwest PHP - TNZ - MPConso"
					elif self.branch == "Rabie's House":
						row_values1.account = "1235-001 - Cash in Bank - Eastwest PHP - CC - MPConso"
				row_values1.debit_in_account_currency = flt(self.total)
				row_values1.credit_in_account_currency = flt(0)

				if self.interest_payment > 0:
					row_values2 = doc2.append('accounts', {})
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
					row_values2.credit_in_account_currency = flt(self.interest_payment)

				row_values3 = doc2.append('accounts', {})
				if self.branch == "Garcia's Pawnshop - CC":
					row_values3.account = "4110-001 - Interest on Loans and Advances - J - CC - MPConso"
				elif self.branch == "Garcia's Pawnshop - GTC":
					row_values3.account = "4110-002 - Interest on Loans and Advances - J - GTC - MPConso"
				elif self.branch == "Garcia's Pawnshop - MOL":
					row_values3.account = "4110-003 - Interest on Loans and Advances - J - MOL - MPConso"
				elif self.branch == "Garcia's Pawnshop - POB":
					row_values3.account = "4110-004 - Interest on Loans and Advances - J - POB - MPConso"
				elif self.branch == "Garcia's Pawnshop - TNZ":
					row_values3.account = "4110-005 - Interest on Loans and Advances - J - TNZ - MPConso"
				elif self.branch == "Rabie's House":
					row_values3.account = "4110-001 - Interest on Loans and Advances - J - CC - MPConso"
				row_values3.debit_in_account_currency = flt(0)
				row_values3.credit_in_account_currency = flt(self.advance_interest)

				if flt(self.discount) > 0:
					row_values4 = doc2.append('accounts', {})
					if self.branch == "Garcia's Pawnshop - CC":
						row_values4.account = "4120-001 - Discount - J - CC - MPConso"
					elif self.branch == "Garcia's Pawnshop - GTC":
						row_values4.account = "4120-002 - Discount - J - GTC - MPConso"
					elif self.branch == "Garcia's Pawnshop - MOL":
						row_values4.account = "4120-003 - Discount - J - MOL - MPConso"
					elif self.branch == "Garcia's Pawnshop - POB":
						row_values4.account = "4120-004 - Discount - J - POB - MPConso"
					elif self.branch == "Garcia's Pawnshop - TNZ":
						row_values4.account = "4120-005 - Discount - J - TNZ - MPConso"
					elif self.branch == "Rabie's House":
						row_values4.account = "4120-001 - Discount - J - CC - MPConso"
					row_values4.debit_in_account_currency = flt(self.discount)
					row_values4.credit_in_account_currency = flt(0)

				doc2.save(ignore_permissions=True)
				# doc2.submit()

			elif self.transaction_type == "Redemption" and self.mode_of_payment == "Bank Transfer":
				doc2 = frappe.new_doc('Journal Entry')
				doc2.voucher_type = 'Journal Entry'
				doc2.company = 'MP Consolidated'
				doc2.posting_date = self.date_issued
				doc2.reference_doctype = "Provisional Receipt"
				doc2.reference_document = self.name
				doc2.document_status = "Redemption"

				row_values1 = doc2.append('accounts', {})
				if self.bank == "BDO":
					row_values1.account = "1215-000 - Cash in Bank - BDO SM Ros - Php - MPConso"
				elif self.bank == "BPI":
					row_values1.account = "1205-000 - Cash in Bank - BPI Marquesa - MPConso"
				elif self.bank == "East West Cavite Branch":
					if self.branch == "Garcia's Pawnshop - CC":
						row_values1.account = "1235-001 - Cash in Bank - Eastwest PHP - CC - MPConso"
					elif self.branch == "Garcia's Pawnshop - POB":
						row_values1.account = "1235-004 - Cash in Bank - Eastwest PHP - POB - MPConso"
					elif self.branch == "Garcia's Pawnshop - MOL":
						row_values1.account = "1235-003 - Cash in Bank - Eastwest PHP - MOL - MPConso"
					elif self.branch == "Garcia's Pawnshop - GTC":
						row_values1.account = "1235-002 - Cash in Bank - Eastwest PHP - GTC - MPConso"
					elif self.branch == "Garcia's Pawnshop - TNZ":
						row_values1.account = "1235-005 - Cash in Bank - Eastwest PHP - TNZ - MPConso"
					elif self.branch == "Rabie's House":
						row_values1.account = "1235-001 - Cash in Bank - Eastwest PHP - CC - MPConso"
				row_values1.debit_in_account_currency = flt(self.total)
				row_values1.credit_in_account_currency = flt(0)

				if flt(self.interest_payment) > 0:
					row_values2 = doc2.append('accounts', {})
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
					row_values2.credit_in_account_currency = flt(self.interest_payment)

				row_values3 = doc2.append('accounts', {})
				if self.branch == "Garcia's Pawnshop - CC":
					row_values3.account = "1610-001 - Pawned Items Inventory - J - CC - MPConso"
				elif self.branch == "Garcia's Pawnshop - GTC":
					row_values3.account = "1610-002 - Pawned Items Inventory - J - GTC - MPConso"
				elif self.branch == "Garcia's Pawnshop - MOL":
					row_values3.account = "1610-003 - Pawned Items Inventory - J - MOL - MPConso"
				elif self.branch == "Garcia's Pawnshop - POB":
					row_values3.account = "1610-004 - Pawned Items Inventory - J - POB - MPConso"
				elif self.branch == "Garcia's Pawnshop - TNZ":
					row_values3.account = "1610-005 - Pawned Items Inventory - J - TNZ - MPConso"
				elif self.branch == "Rabie's House":
					row_values3.account = "1610-001 - Pawned Items Inventory - J - CC - MPConso"
				row_values3.debit_in_account_currency = flt(0)
				row_values3.credit_in_account_currency = flt(self.principal_amount)

				if flt(self.discount) > 0:
					row_values4 = doc2.append('accounts', {})
					if self.branch == "Garcia's Pawnshop - CC":
						row_values4.account = "4120-001 - Discount - J - CC - MPConso"
					elif self.branch == "Garcia's Pawnshop - GTC":
						row_values4.account = "4120-002 - Discount - J - GTC - MPConso"
					elif self.branch == "Garcia's Pawnshop - MOL":
						row_values4.account = "4120-003 - Discount - J - MOL - MPConso"
					elif self.branch == "Garcia's Pawnshop - POB":
						row_values4.account = "4120-004 - Discount - J - POB - MPConso"
					elif self.branch == "Garcia's Pawnshop - TNZ":
						row_values4.account = "4120-005 - Discount - J - TNZ - MPConso"
					elif self.branch == "Rabie's House":
						row_values4.account = "4120-001 - Discount - J - CC - MPConso"
					row_values4.debit_in_account_currency = flt(self.discount)
					row_values4.credit_in_account_currency = flt(0)

				doc2.save(ignore_permissions=True)
				# doc2.submit()

			elif self.transaction_type == "Amortization" and self.mode_of_payment == "Bank Transfer":
				doc2 = frappe.new_doc('Journal Entry')
				doc2.voucher_type = 'Journal Entry'
				doc2.company = 'MP Consolidated'
				doc2.posting_date = self.date_issued
				doc2.reference_doctype = "Provisional Receipt"
				doc2.reference_document = self.name
				doc2.document_status = "Amortization"

				row_values1 = doc2.append('accounts', {})
				if self.bank == "BDO":
					row_values1.account = "1215-000 - Cash in Bank - BDO SM Ros - Php - MPConso"
				elif self.bank == "BPI":
					row_values1.account = "1205-000 - Cash in Bank - BPI Marquesa - MPConso"
				elif self.bank == "East West Cavite Branch":
					if self.branch == "Garcia's Pawnshop - CC":
						row_values1.account = "1235-001 - Cash in Bank - Eastwest PHP - CC - MPConso"
					elif self.branch == "Garcia's Pawnshop - POB":
						row_values1.account = "1235-004 - Cash in Bank - Eastwest PHP - POB - MPConso"
					elif self.branch == "Garcia's Pawnshop - MOL":
						row_values1.account = "1235-003 - Cash in Bank - Eastwest PHP - MOL - MPConso"
					elif self.branch == "Garcia's Pawnshop - GTC":
						row_values1.account = "1235-002 - Cash in Bank - Eastwest PHP - GTC - MPConso"
					elif self.branch == "Garcia's Pawnshop - TNZ":
						row_values1.account = "1235-005 - Cash in Bank - Eastwest PHP - TNZ - MPConso"
					elif self.branch == "Rabie's House":
						row_values1.account = "1235-001 - Cash in Bank - Eastwest PHP - CC - MPConso"
				row_values1.debit_in_account_currency = flt(self.total)
				row_values1.credit_in_account_currency = flt(0)
				
				if self.interest_payment > 0:
					row_values2 = doc2.append('accounts', {})
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
					row_values2.credit_in_account_currency = flt(self.interest_payment)

				row_values3 = doc2.append('accounts', {})
				if self.branch == "Garcia's Pawnshop - CC":
					row_values3.account = "1610-001 - Pawned Items Inventory - J - CC - MPConso"
				elif self.branch == "Garcia's Pawnshop - GTC":
					row_values3.account = "1610-002 - Pawned Items Inventory - J - GTC - MPConso"
				elif self.branch == "Garcia's Pawnshop - MOL":
					row_values3.account = "1610-003 - Pawned Items Inventory - J - MOL - MPConso"
				elif self.branch == "Garcia's Pawnshop - POB":
					row_values3.account = "1610-004 - Pawned Items Inventory - J - POB - MPConso"
				elif self.branch == "Garcia's Pawnshop - TNZ":
					row_values3.account = "1610-005 - Pawned Items Inventory - J - TNZ - MPConso"
				elif self.branch == "Rabie's House":
					row_values3.account = "1610-001 - Pawned Items Inventory - J - CC - MPConso"
				row_values3.debit_in_account_currency = flt(0)
				row_values3.credit_in_account_currency = flt(self.total)

				doc2.save(ignore_permissions=True)
				# doc2.submit()

			elif self.transaction_type == "Renewal w/ Amortization" and self.mode_of_payment == "Bank Transfer":
				doc2 = frappe.new_doc('Journal Entry')
				doc2.voucher_type = 'Journal Entry'
				doc2.company = 'MP Consolidated'
				doc2.posting_date = self.date_issued
				doc2.reference_doctype = "Provisional Receipt"
				doc2.reference_document = self.name
				doc2.document_status = "Renewal w/ Amortization"

				row_values1 = doc2.append('accounts', {})
				if self.bank == "BDO":
					row_values1.account = "1215-000 - Cash in Bank - BDO SM Ros - Php - MPConso"
				elif self.bank == "BPI":
					row_values1.account = "1205-000 - Cash in Bank - BPI Marquesa - MPConso"
				elif self.bank == "East West Cavite Branch":
					if self.branch == "Garcia's Pawnshop - CC":
						row_values1.account = "1235-001 - Cash in Bank - Eastwest PHP - CC - MPConso"
					elif self.branch == "Garcia's Pawnshop - POB":
						row_values1.account = "1235-004 - Cash in Bank - Eastwest PHP - POB - MPConso"
					elif self.branch == "Garcia's Pawnshop - MOL":
						row_values1.account = "1235-003 - Cash in Bank - Eastwest PHP - MOL - MPConso"
					elif self.branch == "Garcia's Pawnshop - GTC":
						row_values1.account = "1235-002 - Cash in Bank - Eastwest PHP - GTC - MPConso"
					elif self.branch == "Garcia's Pawnshop - TNZ":
						row_values1.account = "1235-005 - Cash in Bank - Eastwest PHP - TNZ - MPConso"
					elif self.branch == "Rabie's House":
						row_values1.account = "1235-001 - Cash in Bank - Eastwest PHP - CC - MPConso"
				row_values1.debit_in_account_currency = flt(self.total)
				row_values1.credit_in_account_currency = flt(0)
				
				if self.interest_payment > 0:
					row_values2 = doc2.append('accounts', {})
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
					row_values2.credit_in_account_currency = flt(self.interest_payment)

				if self.advance_interest > 0:
					row_values3 = doc2.append('accounts', {})
					if self.branch == "Garcia's Pawnshop - CC":
						row_values3.account = "4110-001 - Interest on Loans and Advances - J - CC - MPConso"
					elif self.branch == "Garcia's Pawnshop - GTC":
						row_values3.account = "4110-002 - Interest on Loans and Advances - J - GTC - MPConso"
					elif self.branch == "Garcia's Pawnshop - MOL":
						row_values3.account = "4110-003 - Interest on Loans and Advances - J - MOL - MPConso"
					elif self.branch == "Garcia's Pawnshop - POB":
						row_values3.account = "4110-004 - Interest on Loans and Advances - J - POB - MPConso"
					elif self.branch == "Garcia's Pawnshop - TNZ":
						row_values3.account = "4110-005 - Interest on Loans and Advances - J - TNZ - MPConso"
					elif self.branch == "Rabie's House":
						row_values3.account = "4110-001 - Interest on Loans and Advances - J - CC - MPConso"
					row_values3.debit_in_account_currency = flt(0)
					row_values3.credit_in_account_currency = flt(self.advance_interest)

				
				row_values4 = doc2.append('accounts', {})
				if self.branch == "Garcia's Pawnshop - CC":
					row_values4.account = "1610-001 - Pawned Items Inventory - J - CC - MPConso"
				elif self.branch == "Garcia's Pawnshop - GTC":
					row_values4.account = "1610-002 - Pawned Items Inventory - J - GTC - MPConso"
				elif self.branch == "Garcia's Pawnshop - MOL":
					row_values4.account = "1610-003 - Pawned Items Inventory - J - MOL - MPConso"
				elif self.branch == "Garcia's Pawnshop - POB":
					row_values4.account = "1610-004 - Pawned Items Inventory - J - POB - MPConso"
				elif self.branch == "Garcia's Pawnshop - TNZ":
					row_values4.account = "1610-005 - Pawned Items Inventory - J - TNZ - MPConso"
				elif self.branch == "Rabie's House":
					row_values4.account = "1610-001 - Pawned Items Inventory - J - CC - MPConso"
				row_values4.debit_in_account_currency = flt(0)
				row_values4.credit_in_account_currency = flt(self.additional_amortization)

				if flt(self.discount) > 0:
					row_values5 = doc2.append('accounts', {})
					if self.branch == "Garcia's Pawnshop - CC":
						row_values5.account = "4120-001 - Discount - J - CC - MPConso"
					elif self.branch == "Garcia's Pawnshop - GTC":
						row_values5.account = "4120-002 - Discount - J - GTC - MPConso"
					elif self.branch == "Garcia's Pawnshop - MOL":
						row_values5.account = "4120-003 - Discount - J - MOL - MPConso"
					elif self.branch == "Garcia's Pawnshop - POB":
						row_values5.account = "4120-004 - Discount - J - POB - MPConso"
					elif self.branch == "Garcia's Pawnshop - TNZ":
						row_values5.account = "4120-005 - Discount - J - TNZ - MPConso"
					elif self.branch == "Rabie's House":
						row_values5.account = "4120-001 - Discount - J - CC - MPConso"
					row_values5.debit_in_account_currency = flt(self.discount)
					row_values5.credit_in_account_currency = flt(0)

				doc2.save(ignore_permissions=True)
				# doc2.submit()

			elif self.transaction_type == "Interest Payment" and self.mode_of_payment == "Bank Transfer":
				doc2 = frappe.new_doc('Journal Entry')
				doc2.voucher_type = 'Journal Entry'
				doc2.company = 'MP Consolidated'
				doc2.posting_date = self.date_issued
				doc2.reference_doctype = "Provisional Receipt"
				doc2.reference_document = self.name
				doc2.document_status = "Interest Payment"

				row_values1 = doc2.append('accounts', {})
				if self.bank == "BDO":
					row_values1.account = "1215-000 - Cash in Bank - BDO SM Ros - Php - MPConso"
				elif self.bank == "BPI":
					row_values1.account = "1205-000 - Cash in Bank - BPI Marquesa - MPConso"
				elif self.bank == "East West Cavite Branch":
					if self.branch == "Garcia's Pawnshop - CC":
						row_values1.account = "1235-001 - Cash in Bank - Eastwest PHP - CC - MPConso"
					elif self.branch == "Garcia's Pawnshop - POB":
						row_values1.account = "1235-004 - Cash in Bank - Eastwest PHP - POB - MPConso"
					elif self.branch == "Garcia's Pawnshop - MOL":
						row_values1.account = "1235-003 - Cash in Bank - Eastwest PHP - MOL - MPConso"
					elif self.branch == "Garcia's Pawnshop - GTC":
						row_values1.account = "1235-002 - Cash in Bank - Eastwest PHP - GTC - MPConso"
					elif self.branch == "Garcia's Pawnshop - TNZ":
						row_values1.account = "1235-005 - Cash in Bank - Eastwest PHP - TNZ - MPConso"
					elif self.branch == "Rabie's House":
						row_values1.account = "1235-001 - Cash in Bank - Eastwest PHP - CC - MPConso"
				row_values1.debit_in_account_currency = flt(self.total)
				row_values1.credit_in_account_currency = flt(0)
				
				row_values2 = doc2.append('accounts', {})
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
				row_values2.credit_in_account_currency = flt(self.total)

				doc2.save(ignore_permissions=True)
				# doc2.submit()

		