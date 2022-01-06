// Copyright (c) 2021, Rabie Moses Santillan and contributors
// For license information, please see license.txt

frappe.ui.form.on('Non Jewelry Items', {
	onload: function(frm) {
		show_item_no();
		frm.set_value('main_appraiser', frappe.user_info().fullname);
		frm.disable_save();
	},

	refresh: function(frm){
		frm.add_custom_button('Update Data', function(){
			frappe.call({
				method: 'pawnshop_management.pawnshop_management.custom_codes.import_gadgets_info.update_gadgets_data',
				callback: (r) =>{
					console.log(r.message);
				}
			})
		})
		frm.set_query('model', function(){
			return {
				"filters": {
					"type": frm.doc.type,
					"brand": frm.doc.brand
				}
			}
		});
		frm.set_query('assistant_appraiser', function() {
			return {
				"filters": {
					"role_profile_name": "Assistant Appraiser"
				}
			};
		});
	},

	assitant_appraiser: function(frm){
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
							frappe.msgprint({
								title: __('Approved!'),
								indicator: 'green',
								message: __('Appraisal Approved')
							});
							frm.set_df_property('type', 'read_only', 1);
							frm.set_df_property('weight', 'read_only', 1);
							frm.set_df_property('karat', 'read_only', 1);
							frm.set_df_property('karat_category', 'read_only', 1);
							frm.set_df_property('additional_for_stone', 'read_only', 1);
							frm.set_df_property('color', 'read_only', 1);
							frm.set_df_property('colors_if_multi', 'read_only', 1);
							frm.set_df_property('appraisal_value', 'read_only', 1);
							frm.set_df_property('assistant_appraiser', 'read_only', 1);
							frm.enable_save();
						} else {
							frm.set_value('assistant_appraiser', null);
							frm.refresh_field('assistant_appraiser');
							frappe.msgprint({
								title: __('Password Invalid'),
								indicator: 'red',
								message: __(usr.message)
							});
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
				'non_jewelry_inventory_count',
				'non_jewelry_count'
			]
		},

		callback: function(data) {
			let non_jewelry_inventory_count = parseInt(data.message.non_jewelry_inventory_count);
			let non_jewelry_count = parseInt(data.message.non_jewelry_count)
			non_jewelry_count++
			non_jewelry_inventory_count++
			
			cur_frm.set_value('item_no', '1-' + non_jewelry_inventory_count + 'NJ' + '-' + non_jewelry_count)
		},

		error: function(data){
			console.error('Error! Check show_item_no block');
		}
	})
}