# Copyright (c) 2022, Rabie Moses Santillan and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class RoleAssignment(Document):
	def before_save(self, *args, **kwargs):
		if self.employee != None:
			user = frappe.get_doc('User', self.employee)
			if self.role == "Cashier":
				user.role_profile_name = "Cashier"
				user.save(ignore_permissions=True)
			elif self.role == "Appraiser":
				user.role_profile_name = "Appraiser"
				user.save(ignore_permissions=True)
