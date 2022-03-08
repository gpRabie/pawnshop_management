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

	def on_submit(self):
		if frappe.db.exists('Non Jewelry Batch', self.inventory_tracking_no) != self.inventory_tracking_no:
			new_non_jewelry_batch = frappe.new_doc('Non Jewelry Batch')
			new_non_jewelry_batch.inventory_tracking_no = self.inventory_tracking_no
			items = self.non_jewelry_items
			for i in range(len(items)):
				new_non_jewelry_batch.append('items', {
					"item_no": items[i].item_no,
					"type": items[i].type,
					"brand": items[i].brand,
					"model": items[i].model,
					"model_number": items[i].model_number,
					"suggested_appraisal_value": items[i].suggested_appraisal_value
				})
			new_non_jewelry_batch.save(ignore_permissions=True)	