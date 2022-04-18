# Copyright (c) 2022, Rabie Moses Santillan and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class NonJewelryBatch(Document):
	def before_save(self):
		if frappe.db.exists('Pawn Ticket Jewelry', self.name) == None:
			if self.branch == "Garcia's Pawnshop - CC":
				settings = frappe.get_doc('Non Jewelry Naming Series', 'Cavite City Branch')
				settings.inventory_count += 1
				settings.save(ignore_permissions=True)
			elif self.branch == "Garcia'a Pawnshop - GTC":
				settings = frappe.get_doc('Non Jewelry Naming Series', 'GTC Branch')
				settings.inventory_count += 1
				settings.save(ignore_permissions=True)
			elif self.branch == "Garcia'a Pawnshop - MOL":
				settings = frappe.get_doc('Non Jewelry Naming Series', 'Molino Branch')
				settings.inventory_count += 1
				settings.save(ignore_permissions=True)
			elif self.branch == "Garcia'a Pawnshop - POB":
				settings = frappe.get_doc('Non Jewelry Naming Series', 'Poblacion Branch')
				settings.inventory_count += 1
				settings.save(ignore_permissions=True)
			elif self.branch == "Garcia'a Pawnshop - TNZ":
				settings = frappe.get_doc('Non Jewelry Naming Series', 'Tanza Branch')
				settings.inventory_count += 1
				settings.save(ignore_permissions=True)
			elif self.branch == "Rabie's House":
				settings = frappe.get_doc('Non Jewelry Naming Series', "Rabie's House")
				settings.inventory_count += 1
				settings.save(ignore_permissions=True)
