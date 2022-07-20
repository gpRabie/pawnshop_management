# Copyright (c) 2022, Rabie Moses Santillan and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class LoyaltyCard(Document):
	def after_save(self):
		if frappe.db.exists("Customer", self.customer_tracking_no) == self.customer_tracking_no:
			doc = frappe.get_doc('Customer', self.customer_tracking_no)
			doc.loyalty_program = "MPFS Loyalty Program"
			doc.save(ignore_permissions=True)