# Copyright (c) 2022, Rabie Moses Santillan and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import today

class InventoryCount(Document):
	def validate(self):
		if frappe.db.exists("Inventory Count", {"date": today()}) != None:
			frappe.throw(
				title = 'Error',
				msg = 'Data already created in Inventory Count'
			)
