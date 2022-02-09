# Copyright (c) 2022, Rabie Moses Santillan and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class ProvisionalReceipt(Document):
	def before_submit(self):
		if self.transaction_type == "Redemption":
			doc = frappe.get_doc('Pawn Ticket Non Jewelry', self.pawn_ticket_no)
			doc.workflow_state = "Redeemed"
			doc.save()
			frappe.db.commit()