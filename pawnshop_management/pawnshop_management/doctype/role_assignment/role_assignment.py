# Copyright (c) 2022, Rabie Moses Santillan and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class RoleAssignment(Document):
	def before_save(self, *args, **kwargs):
		# super().save(*args, **kwargs)
		doc = frappe.get_doc('Role Assignment')
		# print(doc.employee_2)
		if doc.employee_1 != None:
			user1 = frappe.get_doc('User', doc.employee_1)
			user1.role_profile_name = "Cashier"
			user1.save(ignore_permissions=True)

		if doc.employee_2 != None:
			user2 = frappe.get_doc('User', doc.employee_2)
			user2.role_profile_name = "Appraiser"
			user2.save(ignore_permissions=True)
