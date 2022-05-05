# Copyright (c) 2022, Rabie Moses Santillan and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class NonJewelryBatch(Document):
	def before_save(self):
		if frappe.db.exists('Pawn Ticket Jewelry', self.name) == None:
			print("hello")
			if self.branch == "Garcia's Pawnshop - CC":
				settings = frappe.get_doc('Non Jewelry Naming Series', "Garcia's Pawnshop - CC")
				settings.inventory_count += 1
				settings.item_count = 1
				settings.save(ignore_permissions=True)
			elif self.branch == "Garcia's Pawnshop - GTC":
				settings = frappe.get_doc('Non Jewelry Naming Series', "Garcia's Pawnshop - GTC")
				settings.inventory_count += 1
				settings.item_count = 1
				settings.save(ignore_permissions=True)
			elif self.branch == "Garcia's Pawnshop - MOL":
				settings = frappe.get_doc('Non Jewelry Naming Series', "Garcia's Pawnshop - MOL")
				settings.inventory_count += 1
				settings.item_count = 1
				settings.save(ignore_permissions=True)
			elif self.branch == "Garcia's Pawnshop - POB":
				settings = frappe.get_doc('Non Jewelry Naming Series', "Garcia's Pawnshop - POB")
				settings.inventory_count += 1
				settings.item_count = 1
				settings.save(ignore_permissions=True)
			elif self.branch == "Garcia's Pawnshop - TNZ":
				settings = frappe.get_doc('Non Jewelry Naming Series', "Garcia's Pawnshop - TNZ")
				settings.inventory_count += 1
				settings.item_count = 1
				settings.save(ignore_permissions=True)
			elif self.branch == "Rabie's House":
				settings = frappe.get_doc('Non Jewelry Naming Series', "Rabie's House")
				settings.inventory_count += 1
				settings.item_count = 1
				settings.save(ignore_permissions=True)
			else:
				print(self.branch)
