// Copyright (c) 2022, Rabie Moses Santillan and contributors
// For license information, please see license.txt

frappe.ui.form.on('Loyalty Card', {
	onload: function(frm){
		frm.set_query('customer_tracking_no', () => {
			return {
				filters: {
					"loyalty_program": undefined
				}
			}
		})
	},

	refresh: function(frm){
		frm.add_custom_button('Test', () => {
			frappe.call('pawnshop_management.pawnshop_management.custom_codes.test.get_loyalty_program')
			.then(r => {
				console.log(r.message);
			})
		})
		frm.add_custom_button('Add Points', () => {
			frappe.prompt([
				{
					label: 'Add Points',
					fieldname: 'add_points',
					fieldtype: 'Float'
				},

				{
					label: 'Business Line',
					fieldname: 'business',
					fieldtype: 'Select',
					options: [
						"Pawnshop",
						"Forex",
						"Money Changer"
					]
				},

				{
					label: 'Transaction',
					fieldname: 'business_transaction',
					fieldtype: 'Select',
					options: [
						"",
						"Sangla",
						"Renewal",
						"Redemption",
						"Interest Payment",
						"Renewal w/ Amortization"
					]
				}
			], (values) => {
				let current_points = frm.doc.points;
				current_points += values.add_points;
				frm.set_value('points', current_points)
				frm.add_child('points_movement', {
					date: frappe.datetime.nowdate(),
					business_line: values.business,
					transaction: values.business_transaction,
					pts_movement: "+" + values.add_points,
					encoder: frappe.session.user
				})
			})
		})


		frm.add_custom_button('Subtract Points', () => {
			frappe.prompt([
				{
					label: 'Subtract Points',
					fieldname: 'subtract_points',
					fieldtype: 'Float'
				},

				{
					label: 'Business Line',
					fieldname: 'business',
					fieldtype: 'Select',
					options: [
						"Pawnshop",
						"Forex",
						"Money Changer"
					]
				},

				{
					label: 'Transaction',
					fieldname: 'business_transaction',
					fieldtype: 'Select',
					options: [
						"",
						"Sangla",
						"Renewal",
						"Redemption",
						"Interest Payment",
						"Renewal w/ Amortization"
					]
				}
			], (values) => {
				let current_points = frm.doc.points;
				current_points -= values.subtract_points;
				frm.set_value('points', current_points)
				frm.add_child('points_movement', {
					date: frappe.datetime.nowdate(),
					business_line: values.business,
					transaction: values.business_transaction,
					pts_movement: "-" + values.subtract_points,
					encoder: frappe.session.user
				})
			})
		})
	}
});
frappe.ui.form.on('Loyalty Card History', {
	points_movement_add(frm, cdt, cdn){
		frm.add_child('points_movement', {
			date: frappe.datetime.nowdate(),
			encoder: frappe.session.user
		})
		// let data = frm.doc.points_movement
		// console.log(data);
		// for (let index = 0; index < data.length; index++) {
		// 	data[index].date = frappe.datetime.nowdate();
		// 	console.log(frappe.datetime.nowdate());
		// 	dataencoder = frappe.session.user;
		// 	console.log(frappe.session.user);
		// }
		// frm.refresh_field('points_movement');
	}
})