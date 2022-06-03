# Copyright (c) 2021, Rabie Moses Santillan and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class JewelryBatch(Document):
	def before_save(self):
		if frappe.db.exists('Pawn Ticket Jewelry', self.name) == None:
			if self.branch == "Garcia's Pawnshop - CC":
				settings = frappe.get_doc('Pawnshop Naming Series', "Garcia's Pawnshop - CC")
				settings.jewelry_inventory_count += 1
				settings.jewelry_item_count = 1
				settings.save(ignore_permissions=True)
			elif self.branch == "Garcia's Pawnshop - GTC":
				settings = frappe.get_doc('Pawnshop Naming Series', "Garcia's Pawnshop - GTC")
				settings.jewelry_inventory_count += 1
				settings.jewelry_item_count = 1
				settings.save(ignore_permissions=True)
			elif self.branch == "Garcia's Pawnshop - MOL":
				settings = frappe.get_doc('Pawnshop Naming Series', "Garcia's Pawnshop - MOL")
				settings.jewelry_inventory_count += 1
				settings.jewelry_item_count = 1
				settings.save(ignore_permissions=True)
			elif self.branch == "Garcia's Pawnshop - POB":
				settings = frappe.get_doc('Pawnshop Naming Series', "Garcia's Pawnshop - POB")
				settings.jewelry_inventory_count += 1
				settings.jewelry_item_count = 1
				settings.save(ignore_permissions=True)
			elif self.branch == "Garcia's Pawnshop - TNZ":
				settings = frappe.get_doc('Pawnshop Naming Series', "Garcia's Pawnshop - TNZ")
				settings.jewelry_inventory_count += 1
				settings.jewelry_item_count = 1
				settings.save(ignore_permissions=True)
			elif self.branch == "Rabie's House":
				settings = frappe.get_doc('Pawnshop Naming Series', "Rabie's House")
				settings.jewelry_inventory_count += 1
				settings.jewelry_item_count = 1
				settings.save(ignore_permissions=True)
			else:
				print(self.branch)
