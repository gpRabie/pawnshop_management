// Copyright (c) 2022, Rabie Moses Santillan and contributors
// For license information, please see license.txt

frappe.ui.form.on('Role Assignment', {
	refresh: function(frm) {
		frm.add_custom_button('Change Role', () => {
			frappe.call({
				method: 'pawnshop_management.pawnshop_management.custom_codes.role_change.change_role',
				args: {
					email: frm.doc.employee
				},
				callback: (r) => {
					console.log(frappe.user_roles);
				},
				error: (r) => {
					console.log("Error");
				}
			})
		})
	}
});
