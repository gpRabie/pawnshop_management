# Copyright (c) 2022, Rabie Moses Santillan and contributors
# For license information, please see license.txt

from datetime import datetime
from frappe.utils import add_to_date
import frappe
from frappe.model.document import Document

class ProvisionalReceipt(Document):
	def before_submit(self):
		if self.transaction_type == "Redemption":
			frappe.db.set_value(self.pawn_ticket_type, self.pawn_ticket_no, 'workflow_state', 'Redeemed')
			frappe.db.commit()

	def on_submit(self):
		if self.transaction_type == "Renewal": # Create New Pawn Ticket
			previous_pawn_ticket = frappe.get_doc(self.pawn_ticket_type, self.pawn_ticket_no)
			new_pawn_ticket = frappe.new_doc(self.pawn_ticket_type)
			new_pawn_ticket.pawn_ticket = self.new_pawn_ticket_no
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
						"brand": previous_items[i].brand,
						"model": previous_items[i].model,
						"model_number": previous_items[i].model_number,
						"suggested_appraisal_value": previous_items[i].suggested_appraisal_value
					})
			new_pawn_ticket.desired_principal = previous_pawn_ticket.desired_principal
			new_pawn_ticket.interest = previous_pawn_ticket.interest
			new_pawn_ticket.net_proceeds = previous_pawn_ticket.net_proceeds

			new_pawn_ticket.save(ignore_permissions=True)
			new_pawn_ticket.submit()

