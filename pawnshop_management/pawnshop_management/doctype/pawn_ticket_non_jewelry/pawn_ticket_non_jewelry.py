# Copyright (c) 2022, Rabie Moses Santillan and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class PawnTicketNonJewelry(Document):
	def before_save(self):
		if frappe.db.exists('Pawn Ticket Non Jewelry', self.name) == None:
			settings = frappe.get_doc('Pawnshop Management Settings')
			# settings.non_jewelry_inventory_count += 1
			settings.b_series_current_count += 1
			# settings.non_jewelry_count = 1
			settings.save(ignore_permissions=True)