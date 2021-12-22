// Copyright (c) 2021, Rabie Moses Santillan and contributors
// For license information, please see license.txt

frappe.ui.form.on('Jewelry Items', {
	onload: function(frm) {
		show_item_no();
		frm.set_value('main_appraiser', frappe.user_info().fullname);
		// frm.disable_save();
	},

	refresh: function(frm){
		frm.add_custom_button('Get Password', () => {
			frappe.call({
				method: 'pawnshop_management.pawnshop_management.custom_codes.passwords.validate_user',
				args: {
					doctype: "User",
					name: "jappraiser@gmail.com"
				},
				callback: function(pwd){
					console.log(pwd.message);
				}
			})
		});
	},

	assistant_appraiser: function(frm){
		frappe.prompt({
			label: 'Password',
			fieldname: 'password',
			fieldtype: 'Password'
		}, (password) => {
			console.log(password);
			frappe.call({
				method: 'pawnshop_management.pawnshop_management.custom_codes.passwords.get_password',
				args: {
					usr: frm.doc.assistant_appraiser,
					password: password
				},
				callback: function(pwd){
					console.log(pwd);
				}
			})
		})
	}

});

function show_item_no(frm) {
	frappe.call({
		method: 'frappe.client.get_value',
		args: {
			'doctype': 'Pawnshop Management Settings',
			'fieldname': [
				'jewelry_inventory_count',
				'jewelry_count'
			]
		},

		callback: function(data) {
			let jewelry_inventory_count = parseInt(data.message.jewelry_inventory_count);
			let jewelry_count = parseInt(data.message.jewelry_count)
			jewelry_count++
			jewelry_inventory_count++
			cur_frm.set_value('batch_number', jewelry_inventory_count)
			cur_frm.set_value('item_no', '1-' + jewelry_inventory_count + '-' + jewelry_count)
		},

		error: function(data){
			console.error('Error! Check show_item_no block');
		}
	})
}