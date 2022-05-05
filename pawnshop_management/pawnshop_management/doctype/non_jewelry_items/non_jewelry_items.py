# Copyright (c) 2021, Rabie Moses Santillan and contributors
# For license information, please see license.txt

# from pydoc import doc
import frappe
from frappe.model.document import Document

class NonJewelryItems(Document):
	def before_save(self):
		if frappe.db.exists('Pawn Ticket Non Jewelry', self.name) == None:
			if self.branch == "Garcia's Pawnshop - CC":
				settings = frappe.get_doc('Non Jewelry Naming Series', "Garcia's Pawnshop - CC")
				settings.item_count += 1
				settings.save(ignore_permissions=True)
			elif self.branch == "Garcia's Pawnshop - GTC":
				settings = frappe.get_doc('Non Jewelry Naming Series', "Garcia'a Pawnshop - GTC")
				settings.item_count += 1
				settings.save(ignore_permissions=True)
			elif self.branch == "Garcia's Pawnshop - MOL":
				settings = frappe.get_doc('Non Jewelry Naming Series', "Garcia'a Pawnshop - MOL")
				settings.item_count += 1
				settings.save(ignore_permissions=True)
			elif self.branch == "Garcia's Pawnshop - POB":
				settings = frappe.get_doc('Non Jewelry Naming Series', "Garcia'a Pawnshop - POB")
				settings.item_count += 1
				settings.save(ignore_permissions=True)
			elif self.branch == "Garcia's Pawnshop - TNZ":
				settings = frappe.get_doc('Non Jewelry Naming Series', "Garcia'a Pawnshop - TNZ")
				settings.item_count += 1
				settings.save(ignore_permissions=True)
			elif self.branch == "Rabie's House":
				settings = frappe.get_doc('Non Jewelry Naming Series', "Rabie's House")
				settings.item_count += 1
				settings.save(ignore_permissions=True)
		