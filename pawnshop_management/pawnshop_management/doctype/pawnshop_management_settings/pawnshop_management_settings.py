# Copyright (c) 2021, Rabie Moses Santillan and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class PawnshopManagementSettings(Document):
	@frappe.whitelist()
	def reset_jewelry_count(self):
		self.jewelry_count = 0

	@frappe.whitelist()
	def reset_non_jewelry_count(self):
		self.non_jewelry_count = 0