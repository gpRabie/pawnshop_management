# Copyright (c) 2022, Rabie Moses Santillan and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class RoleAssignment(Document):
	def before_save(self):
		reset_roles()
		user = frappe.get_doc('User', self.employee)
		if user.role_profile_name == 'Appraiser':
			user.role_profile_name = 'Appraiser/Cashier'
		elif user.role_profile_name == 'Supervisor':
			user.role_profile_name = 'Supervisor/Cashier'
		elif user.role_profile_name == 'Guest':
			user.role_profile_name = 'Cashier'
		user.save(ignore_permissions=True)

	
		

def reset_roles():
	users = frappe.db.get_list('User', pluck='name')
	for i in range(len(users)):
		if users[i] != "Administrator":
			user_role_change = frappe.get_doc('User', users[i])
			if user_role_change.role_profile_name == 'Supervisor/Cashier':
				user_role_change.role_profile_name = 'Supervisor'
			elif user_role_change.role_profile_name == 'Appraiser/Cashier':
				user_role_change.role_profile_name = 'Appraiser'
			elif user_role_change.role_profile_name == 'Cashier':
				user_role_change.role_profile_name = 'Guest'
			user_role_change.save(ignore_permissions=True)
			
