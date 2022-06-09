# Copyright (c) 2022, Rabie Moses Santillan and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class PawnTicketJewelry(Document):
	def before_save(self):
		if frappe.db.exists('Pawn Ticket Jewelry', self.name) == None:
			if self.amended_from == None:
				if self.branch == "Garcia's Pawnshop - CC":
					settings = frappe.get_doc('Pawnshop Naming Series', "Garcia's Pawnshop - CC")
					if self.item_series == 'A':
						settings.a_series += 1
					elif self.item_series == 'B':
						settings.b_series += 1
					settings.save(ignore_permissions=True)
				elif self.branch == "Garcia's Pawnshop - GTC":
					settings = frappe.get_doc('Pawnshop Naming Series', "Garcia's Pawnshop - GTC")
					if self.item_series == 'A':
						settings.a_series += 1
					elif self.item_series == 'B':
						settings.b_series += 1
					settings.save(ignore_permissions=True)
				elif self.branch == "Garcia's Pawnshop - MOL":
					settings = frappe.get_doc('Pawnshop Naming Series', "Garcia's Pawnshop - MOL")
					if self.item_series == 'A':
						settings.a_series += 1
					elif self.item_series == 'B':
						settings.b_series += 1
					settings.save(ignore_permissions=True)
				elif self.branch == "Garcia's Pawnshop - POB":
					settings = frappe.get_doc('Pawnshop Naming Series', "Garcia's Pawnshop - POB")
					if self.item_series == 'A':
						settings.a_series += 1
					elif self.item_series == 'B':
						settings.b_series += 1
					settings.save(ignore_permissions=True)
				elif self.branch == "Garcia's Pawnshop - TNZ":
					settings = frappe.get_doc('Pawnshop Naming Series', "Garcia's Pawnshop - TNZ")
					if self.item_series == 'A':
						settings.a_series += 1
					elif self.item_series == 'B':
						settings.b_series += 1
					settings.save(ignore_permissions=True)
				elif self.branch == "Rabie's House":
					settings = frappe.get_doc('Pawnshop Naming Series', "Rabie's House")
					if self.item_series == 'A':
						settings.a_series += 1
					elif self.item_series == 'B':
						settings.b_series += 1
					settings.save(ignore_permissions=True)

	def on_submit(self):
		if frappe.db.exists('Jewelry Batch', self.inventory_tracking_no) != self.inventory_tracking_no: #Copies Items table from pawnt ticket to non jewelry batch doctype
			new_jewelry_batch = frappe.new_doc('Jewelry Batch')
			new_jewelry_batch.inventory_tracking_no = self.inventory_tracking_no
			new_jewelry_batch.branch = self.branch
			items = self.jewelry_items
			for i in range(len(items)):
				new_jewelry_batch.append('items', {
					"item_no": items[i].item_no,
					"type": items[i].type,
					"karat_category": items[i].karat_category,
					"karat": items[i].karat,
					"weight": items[i].total_weight,
					"color": items[i].color,
					"colors_if_multi": items[i].colors_if_multi,
					"additional_for_stone": items[i].additional_for_stone,
					"suggested_appraisal_value": items[i].suggested_appraisal_value,
					"desired_principal": items[i].desired_principal,
					"comments": items[i].comments
				})
			new_jewelry_batch.save(ignore_permissions=True)

	def before_cancel(self):
		name = frappe.db.get_value('Journal Entry', {'reference_document': self.name, "document_status": "Active"}, 'name')
		frappe.db.set_value('Journal Entry', name, 'docstatus', 2)
		frappe.db.commit()

