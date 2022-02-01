# Copyright (c) 2022, Rabie Moses Santillan and contributors
# For license information, please see license.txt

from hashlib import new
import frappe
from frappe.model.document import Document

class PawnTicketNonJewelry(Document):
	def before_save(self):
		if frappe.db.exists('Pawn Ticket Jewelry', self.name) == None:
			settings = frappe.get_doc('Pawnshop Management Settings')
			settings.non_jewelry_inventory_count += 1
			settings.b_series_current_count += 1
			settings.non_jewelry_count = 1
			settings.save(ignore_permissions=True)

	def on_submit(self):
		if self.transaction_type == "New":
			new_batch = frappe.new_doc('Non Jewelry Batch')
			new_batch.inventory_tracking_no = self.inventory_tracking_no

			for item in self.get('non_jewelry_items'):
				new_batch.append('items', {
					"item_no": item.item_no
				})
			new_batch.save()