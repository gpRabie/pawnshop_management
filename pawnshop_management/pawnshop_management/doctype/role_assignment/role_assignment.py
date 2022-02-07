# Copyright (c) 2022, Rabie Moses Santillan and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class RoleAssignment(Document):
	def before_save(self):
		reset_roles()
		select_cashier(self.employee)
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
			user = frappe.get_doc('User', users[i])
			if user.role_profile_name == 'Supervisor/Cashier':
				user.role_profile_name = 'Supervisor'
			elif user.role_profile_name == 'Appraiser/Cashier':
				user.role_profile_name = 'Appraiser'
			elif user.role_profile_name == 'Cashier':
				user.role_profile_name = 'Guest'
			user.save(ignore_permissions=True)
			

def select_cashier(email=None):
	if email != None:
		# u = frappe.get_doc('User', email)
		# u.append('roles',{
		# 	"doctype": "Has Role",
		# 	"role":"Pawnshop Cashier"
		# })
		# u.save(ignore_permissions=True)
		user_role = frappe.get_doc("User", email)
		user_role.add_roles("Pawnshop Cashier")
		user_role.save(ignore_permissions=True)
