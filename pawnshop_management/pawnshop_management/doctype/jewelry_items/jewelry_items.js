// Copyright (c) 2021, Rabie Moses Santillan and contributors
// For license information, please see license.txt

frappe.ui.form.on('Jewelry Items', {
	onload: function(frm) {
		show_item_no();
		frm.set_value('main_appraiser', frappe.user_info().fullname);
		frm.disable_save();
		// frm.disable_save();
	},

	// refresh: function(frm){
	// 	frm.add_custom_button('Get Password', () => {
	// 		frappe.call({
	// 			method: 'pawnshop_management.pawnshop_management.custom_codes.passwords.check_password',
	// 			args: {
	// 				// doctype: "User",
	// 				// name: "jappraiser@gmail.com"
	// 				user: "gprabiemosessantillan@gmail.com",
	// 				pwd: "wertyou1234"
	// 			},
	// 			callback: function(pwd){
	// 				console.log(pwd.message);
	// 			}
	// 		})
	// 	});
	// },

	assistant_appraiser: function(frm){
		if (frm.doc.assistant_appraiser != null) {
			frappe.prompt({
				label: 'Password',
				fieldname: 'password',
				fieldtype: 'Password'
			}, (password) => {
				frappe.call({
					method: 'pawnshop_management.pawnshop_management.custom_codes.passwords.check_password',
					args: {
						user: String(frm.doc.assistant_appraiser),
						pwd: password.password
					},
					callback: function(usr){
						if (frm.doc.assistant_appraiser == usr.message) {
							frm.set_df_property('type', 'read_only', 1);
							frm.set_df_property('weight', 'read_only', 1);
							frm.set_df_property('karat', 'read_only', 1);
							frm.set_df_property('karat_category', 'read_only', 1);
							frm.set_df_property('additional_for_stone', 'read_only', 1);
							frm.set_df_property('color', 'read_only', 1);
							frm.set_df_property('colors_if_multi', 'read_only', 1);
							frm.set_df_property('appraisal_value', 'read_only', 1);
							frm.enable_save();
						}
					}
				})
			})
		}
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

		// error: function(data){
		// 	console.error('Error! Check show_item_no block');
		// }
	})
}