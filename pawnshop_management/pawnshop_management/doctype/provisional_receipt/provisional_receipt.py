# Copyright (c) 2022, Rabie Moses Santillan and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class ProvisionalReceipt(Document):
	def before_submit(self):
		if self.transaction_type == "Redemption":
			frappe.db.set_value('Pawn Ticket Non Jewelry', self.pawn_ticket_no, 'workflow_state', 'Redeemed')
			frappe.db.commit()