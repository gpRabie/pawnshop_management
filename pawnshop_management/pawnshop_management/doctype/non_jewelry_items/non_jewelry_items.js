// Copyright (c) 2021, Rabie Moses Santillan and contributors
// For license information, please see license.txt

frappe.ui.form.on('Non Jewelry Items', {

	before_save:function(frm){
		// frm.set_value('main_appraiser', frappe.user_info().fullname);
		show_item_no(frm)
	},

	refresh: function(frm){
		frm.set_df_property('assistant_appraiser', 'read_only', 1);
		frm.disable_save();
		frm.set_df_property('disk_type', 'hidden', 1);
		frm.set_df_property('internet_connection_capability', 'hidden', 1);
		frm.set_df_property('bag', 'hidden', 1);
		frm.set_df_property('extra_battery', 'hidden', 1);
		frm.set_df_property('extra_lens', 'hidden', 1);
		frm.add_custom_button('Update Data', function(){
			frappe.call({
				method: 'pawnshop_management.pawnshop_management.custom_codes.import_gadgets_info.update_gadgets_data',
				callback: (r) =>{
					frappe.show_alert({
						message:__('Update Successful'),
						indicator:'green'
					}, 5)
				}
			})
		});

		frm.set_query('brand', function(){
			if (frm.doc.type == "Cellphone") {
				return {
					"filters": {
						"cellphone": 1
					}
				}	
			} else if (frm.doc.type == "Tablet") {
				return {
					"filters": {
						"tablet": 1
					}
				}
			} else if (frm.doc.type == "Laptop") {
				return {
					"filters": {
						"laptop": 1
					}
				}
			} else if (frm.doc.type == "Camera") {
				return {
					"filters": {
						"camera": 1
					}
				}
			}
		});
		frm.set_query('model', function(){
			if (frm.doc.type == "Laptop") {
				if (frm.doc.brand != "Apple") {
					return {
						"filters": {
							"type": frm.doc.type,
							"brand": "",
							"workflow_state": "Accepted"
						}
					}
				} else {
					return {
						"filters": {
							"type": frm.doc.type,
							"brand": frm.doc.brand,
							"workflow_state": "Accepted"
						}
					}
				}
			} else {
				return {
					"filters": {
						"type": frm.doc.type,
						"brand": frm.doc.brand,
						"workflow_state": "Accepted"
					}
				}
			}
		});
		frm.set_query('assistant_appraiser', function() {
			return {
				"filters": {
					"role_profile_name": [
						"in", 
						[
							"Appraiser",
							"Supervisor"
						]
					]
				}
			};
		});
	},


	type: function(frm){
		if (frm.doc.type == "Cellphone") {
			unhide_hidden_fields(frm);
			require_unrequired_fields(frm);
			frm.set_df_property('model', 'label', 'Model');
			frm.set_df_property('model_number', 'label', 'Model Number');
			frm.set_df_property('disk_type', 'reqd', 0);
			frm.set_df_property('disk_type', 'hidden', 1);
			frm.set_df_property('internet_connection_capability', 'reqd', 0);
			frm.set_df_property('internet_connection_capability', 'hidden', 1);
			frm.set_df_property('bag', 'hidden', 1);
			frm.set_df_property('extra_battery', 'hidden', 1);
			frm.set_df_property('extra_lens', 'hidden', 1);
		} else if (frm.doc.type == "Tablet") {
			unhide_hidden_fields(frm);
			require_unrequired_fields(frm);
			frm.set_df_property('model', 'label', 'Model');
			frm.set_df_property('model_number', 'label', 'Model Number');
			frm.set_df_property('disk_type', 'reqd', 0);
			frm.set_df_property('disk_type', 'hidden', 1);
			frm.set_df_property('bag', 'hidden', 1);
			frm.set_df_property('extra_battery', 'hidden', 1);
			frm.set_df_property('extra_lens', 'hidden', 1);
		} else if (frm.doc.type == "Laptop") {
			unhide_hidden_fields();
			require_unrequired_fields(frm);
			frm.set_df_property('model', 'label', 'Processor & Generation');
			frm.set_df_property('model_number', 'label', 'Model Name');
			frm.set_df_property('internet_connection_capability', 'reqd', 0);
			frm.set_df_property('internet_connection_capability', 'hidden', 1);
			frm.set_df_property('charger', 'hidden', 1);
			frm.set_df_property('pin', 'hidden', 1);
			frm.set_df_property('sim_card', 'hidden', 1);
			frm.set_df_property('sd_card', 'hidden', 1);
			frm.set_df_property('bag', 'hidden', 1);
			frm.set_df_property('extra_battery', 'hidden', 1);
			frm.set_df_property('extra_lens', 'hidden', 1);
		} else if (frm.doc.type == "Camera") {
			unhide_hidden_fields();
			require_unrequired_fields(frm);
			frm.set_df_property('model', 'label', 'Model');
			frm.set_df_property('model_number', 'reqd', 0);
			frm.set_value('model_number', "N/A");
			frm.refresh_field('model_number')
			frm.set_df_property('model_number', 'hidden', 1);
			frm.set_df_property('ram', 'reqd', 0);
			frm.set_df_property('ram', 'hidden', 1);
			frm.set_df_property('internal_memory', 'reqd', 0);
			frm.set_df_property('internal_memory', 'hidden', 1);
			frm.set_df_property('disk_type', 'reqd', 0);
			frm.set_df_property('disk_type', 'hidden', 1);
			frm.set_df_property('internet_connection_capability', 'reqd', 0);
			frm.set_df_property('internet_connection_capability', 'hidden', 1);
			frm.set_df_property('charger', 'hidden', 1);
			frm.set_df_property('case', 'hidden', 1);
			frm.set_df_property('box', 'hidden', 1);
			frm.set_df_property('earphones', 'hidden', 1);
			frm.set_df_property('pin', 'hidden', 1);
			frm.set_df_property('manual', 'hidden', 1);
			frm.set_df_property('sim_card', 'hidden', 1);
		}
	},

	brand: function(frm){
		if (frm.doc.type == "Laptop" && frm.doc.brand == "Apple") {
			frm.set_df_property('internal_memory', 'reqd', 0)
			frm.set_df_property('ram', 'reqd', 0);
			frm.refresh_field('ram')
			frm.refresh_field('internal_memory')
		}else if (frm.doc.brand == "Apple") {
			frm.set_df_property('ram', 'reqd', 0);
			frm.refresh_field('ram')
		}
	},

	model:function(frm){
		frappe.db.get_value('Models', frm.doc.model, ['defective', 'minimum', 'maximum']).then(function(r){
			let price_suggestion = r.message;
			if (frm.doc.category == "Maximum") {
				frm.set_value('appraisal_value', price_suggestion.maximum)
				frm.refresh_field('appraisal_value')
			} else if (frm.doc.category == "Minimum") {
				frm.set_value('appraisal_value', price_suggestion.minimum)
				frm.refresh_field('appraisal_value')
			} else {
				frm.set_value('appraisal_value', price_suggestion.defective)
				frm.refresh_field('appraisal_value')
			}
		});
	},

	category: function(frm){
		frappe.db.get_value('Models', frm.doc.model, ['defective', 'minimum', 'maximum']).then(function(r){
			let price_suggestion = r.message;
			if (frm.doc.category == "Maximum") {
				frm.set_value('appraisal_value', price_suggestion.maximum)
				frm.refresh_field('appraisal_value')
			} else if (frm.doc.category == "Minimum") {
				frm.set_value('appraisal_value', price_suggestion.minimum)
				frm.refresh_field('appraisal_value')
			} else {
				frm.set_value('appraisal_value', price_suggestion.defective)
				frm.refresh_field('appraisal_value')
			}
		});
	},

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
							frappe.msgprint({
								title: __('Approved!'),
								indicator: 'green',
								message: __('Appraisal Approved')
							});
							frm.set_df_property('type', 'read_only', 1);
							frm.set_df_property('brand', 'read_only', 1);
							frm.set_df_property('model', 'read_only', 1);
							frm.set_df_property('model_number', 'read_only', 1);
							frm.set_df_property('ram', 'read_only', 1);
							frm.set_df_property('internal_memory', 'read_only', 1);
							frm.set_df_property('disk_type', 'read_only', 1);
							frm.set_df_property('color', 'read_only', 1);
							frm.set_df_property('category', 'read_only', 1);
							frm.set_df_property('charger', 'read_only', 1);
							frm.set_df_property('case_box_or_bag', 'read_only', 1);
							frm.set_df_property('appraisal_value', 'read_only', 1);
							frm.set_df_property('assistant_appraiser', 'read_only', 1);
							frm.set_df_property('comments', 'read_only', 1);
							frm.set_df_property('charger', 'read_only', 1);
							frm.set_df_property('case', 'read_only', 1);
							frm.set_df_property('box', 'read_only', 1);
							frm.set_df_property('earphones', 'read_only', 1);
							frm.set_df_property('others', 'read_only', 1);
							frm.set_df_property('pin', 'read_only', 1);
							frm.set_df_property('manual', 'read_only', 1);
							frm.set_df_property('sim_card', 'read_only', 1);
							frm.set_df_property('sd_card', 'read_only', 1);
							frm.set_df_property('bag', 'read_only', 1);
							frm.set_df_property('extra_battery', 'read_only', 1);
							frm.set_df_property('extra_lens', 'read_only', 1);
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
			frm.set_value('batch_number', non_jewelry_inventory_count)
			frm.set_value('item_no', '1-' + non_jewelry_inventory_count + 'NJ' + '-' + non_jewelry_count)
		},

		error: function(data){
			console.error('Error! Check show_item_no block');
		}
	})
}

function unhide_hidden_fields(frm) {
	frm.set_df_property('model_number', 'hidden', 0);
	frm.set_df_property('ram', 'hidden', 0);
	frm.set_df_property('internal_memory', 'hidden', 0);
	frm.set_df_property('disk_type', 'hidden', 0);
	frm.set_df_property('internet_connection_capability', 'hidden', 0);
	frm.set_df_property('charger', 'hidden', 0);
	frm.set_df_property('case', 'hidden', 0);
	frm.set_df_property('box', 'hidden', 0);
	frm.set_df_property('earphones', 'hidden', 0);
	frm.set_df_property('pin', 'hidden', 0);
	frm.set_df_property('manual', 'hidden', 0);
	frm.set_df_property('sim_card', 'hidden', 0);
	frm.set_df_property('sd_card', 'hidden', 0);
	frm.set_df_property('bag', 'hidden', 0);
	frm.set_df_property('extra_battery', 'hidden', 0);
	frm.set_df_property('extra_lens', 'hidden', 0);
}

function require_unrequired_fields(frm) {
	frm.set_df_property('model_number', 'reqd', 1);
	frm.set_df_property('ram', 'reqd', 1);
	frm.set_df_property('internal_memory', 'reqd', 1);
	frm.set_df_property('disk_type', 'reqd', 1);
	frm.set_df_property('internet_connection_capability', 'reqd', 1);
}