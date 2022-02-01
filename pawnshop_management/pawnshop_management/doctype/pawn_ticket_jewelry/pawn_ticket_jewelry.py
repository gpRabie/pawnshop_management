# Copyright (c) 2022, Rabie Moses Santillan and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class PawnTicketJewelry(Document):
	def before_save(self):
		if frappe.db.exists('Pawn Ticket Jewelry', self.name) == None:
			settings = frappe.get_doc('Pawnshop Management Settings')
			settings.jewelry_inventory_count += 1
			settings.jewelry_count = 1
			if self.item_series == 'A':
				settings.a_series_current_count += 1
			elif self.item_series == 'B':
				settings.b_series_current_count += 1
			settings.save(ignore_permissions=True)

