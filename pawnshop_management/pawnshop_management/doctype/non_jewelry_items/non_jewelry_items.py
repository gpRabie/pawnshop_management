# Copyright (c) 2021, Rabie Moses Santillan and contributors
# For license information, please see license.txt

# from pydoc import doc
import frappe
from frappe.model.document import Document

class NonJewelryItems(Document):
	def before_save(self):
		doc = frappe.get_doc('Pawnshop Management Settings')
		doc.non_jewelry_count += 1
		doc.save(ignore_permissions=True)