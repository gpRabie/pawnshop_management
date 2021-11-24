# Copyright (c) 2021, Rabie Moses Santillan and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class JewelryItems(Document):
	def before_save(self):
		naming = self.item_no.split("-")
		doc = frappe.get_doc('Pawnshop Management Settings')
		if self.new_batch == True:
			doc.jewelry_inventory_count = naming[-2]
			doc.jewelry_count = naming[-1]
		else:
			doc.jewelry_count = naming[-1]
		
		doc.save()