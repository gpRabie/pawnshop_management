// Copyright (c) 2022, Rabie Moses Santillan and contributors
// For license information, please see license.txt

frappe.ui.form.on('Loyalty Card', {
	// refresh: function(frm) {
	// 	frm.add_custom_button('Add/Subtract Points', () => {
	// 		frappe.prompt({
	// 			label: 'Add/Subtract Points',
	// 			fielname: 'points_addition_subtraction',
	// 			fieldtype: 'Float'
	// 		}, (value) => {
	// 			frm.add_child('points_movement', {
	// 				date: frappe.utils.today(),
	// 				business_line: 'Pawnshop',
	// 				pts_movement: value.points_addition_subtraction,
	// 				encoder: frappe.session.user
	// 			})
	// 		})
	// 	})
	// }
});
