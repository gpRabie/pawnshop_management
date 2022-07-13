// Copyright (c) 2021, Rabie Moses Santillan and contributors
// For license information, please see license.txt

frappe.ui.form.on('Jewelry Items', {
	onload: function(frm) {
		if (frm.is_new()) {
			frm.set_value('main_appraiser', frappe.user_info().fullname);
			frm.disable_save();
		}
	},

	validate: function(frm){
		if (parseFloat(frm.doc.desired_principal) > parseFloat(frm.doc.appraisal_value)) {
			frappe.throw(__('Desired principal is greater than appraisal value'));
		}
	},
	// before_workflow_action: function(frm){
	// 	if (frm.selected_workflow_action === "Collect") { // Change status
	// 		frappe.call({
	// 			method: 'pawnshop_management.pawnshop_management.custom_codes.update_j_batch.update_fields_after_status_change_collect_j_batch',
	// 			args: {
	// 				inventory_tracing_no: String(frm.doc.name)
	// 			},
	// 			callback: function(){
	// 			}
	// 		})
	// 	} else if (frm.selected_workflow_action === "Redeem") {
	// 		frappe.call({
	// 			method: 'pawnshop_management.pawnshop_management.custom_codes.update_j_batch.status_change_date',
	// 			args: {
	// 				inventory_tracing_no: String(frm.doc.name)
	// 			},
	// 			callback: function(){
	// 			}
	// 		})
	// 	} else if (frm.selected_workflow_action === "Review") {
	// 		frappe.call({
	// 			method: 'pawnshop_management.pawnshop_management.custom_codes.update_j_batch.update_fields_after_status_change_review_j_batch',
	// 			args: {
	// 				inventory_tracing_no: String(frm.doc.name)
	// 			},
	// 			callback: function(){

	// 			}
	// 		})
	// 	} else if (frm.selected_workflow_action === "Pull Out") {
	// 		frappe.call({
	// 			method: 'pawnshop_management.pawnshop_management.custom_codes.update_j_batch.update_fields_after_status_change_review_j_batch',
	// 			args: {
	// 				inventory_tracing_no: String(frm.doc.name)
	// 			},
	// 			callback: function(){
	// 				frm.toggle_display(['sizelength', 'selling_price', 'selling_price_per_gram'], frm.doc.workflow_state === 'Pulled Out');
	// 			}
	// 		})
	// 	}
	// },

	refresh: function(frm){
		frm.toggle_display(['sizelength', 'selling_price', 'selling_price_per_gram'], frm.doc.workflow_state === "Pulled Out" || frm.doc.workflow_state === "Scrap" || frm.doc.workflow_state === "On Display" || frm.doc.workflow_state === "Sold")
		frappe.call({
			method: 'pawnshop_management.pawnshop_management.custom_codes.get_ip.get_ip',
			callback: function(data){
				let current_ip = data.message
				frappe.call({
					method: 'pawnshop_management.pawnshop_management.custom_codes.get_ip.get_ip_from_settings',
					callback: (result) => {
						let ip = result.message;
						if (current_ip == ip["cavite_city"]) {
							frm.set_value('branch', "Garcia's Pawnshop - CC");
							frm.refresh_field('branch');
						} else if (current_ip == ip["poblacion"]) {
							frm.set_value('branch', "Garcia's Pawnshop - POB");
							frm.refresh_field('branch');
						} else if (current_ip == ip["molino"]) {
							frm.set_value('branch', "Garcia's Pawnshop - MOL");
							frm.refresh_field('branch');
						} else if (current_ip == ip["gtc"]) {
							frm.set_value('branch', "Garcia's Pawnshop - GTC");
							frm.refresh_field('branch');
						} else if (current_ip == ip["tanza"]) {
							frm.set_value('branch', "Garcia's Pawnshop - TNZ");
							frm.refresh_field('branch');
						} else if (current_ip == ip["rabies_house"]) {
							frm.set_value('branch', "Rabie's House");
							frm.refresh_field('branch');
						}
					}
				})
			}
		})
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
							frm.set_df_property('weight', 'read_only', 1);
							frm.set_df_property('karat', 'read_only', 1);
							frm.set_df_property('karat_category', 'read_only', 1);
							frm.set_df_property('additional_for_stone', 'read_only', 1);
							frm.set_df_property('color', 'read_only', 1);
							frm.set_df_property('colors_if_multi', 'read_only', 1);
							frm.set_df_property('appraisal_value', 'read_only', 1);
							frm.set_df_property('assistant_appraiser', 'read_only', 1);
							frm.set_df_property('comments', 'read_only', 1);
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
	},

	branch: function(frm){
		show_item_no(frm);
	},

	appraisal_value: function(frm){
		frm.set_value('desired_principal', parseFloat(frm.doc.appraisal_value))
		frm.refresh_field('desired_principal')
	}

});

frappe.ui.form.on('Jewelry Karat List', {
	karat: function(frm, cdt, cdn){
		console.log(frm.doc.karats.length);
		if (frm.doc.karats.length> 1) {
			frm.set_value('karat', 'Multiple Karat');
			frm.refresh_field('karat')
		} else {
			frm.set_value('karat', frm.doc.karats[0].karat);
			frm.refresh_field('karat')
		}
	},

	weight: function(frm, cdt, cdn){
		set_total_weight(frm, cdt, cdn)
	}
});

function set_total_weight(frm, cdt, cdn) {
	let total_weight = 0.00;
	$.each(frm.doc.karats, function(index, item){
		total_weight += parseFloat(item.weight);
	});
	frm.set_value('total_weight', total_weight)
	frm.refresh_field('total_weight')
}

function show_item_no(frm) {
	if (frm.doc.branch == "Garcia's Pawnshop - CC") {
		frappe.db.get_value('Pawnshop Naming Series', "Garcia's Pawnshop - CC",['jewelry_item_count', 'jewelry_inventory_count'])
		.then(value => {
			let non_jewelry_inventory_count = parseInt(value.message.jewelry_inventory_count);
			let non_jewelry_count = parseInt(value.message.jewelry_item_count)
			frm.set_value('batch_number', non_jewelry_inventory_count)
			frm.set_value('item_no', '1-' + non_jewelry_inventory_count + 'J' + '-' + non_jewelry_count)
			
		})
	} else if (frm.doc.branch == "Garcia's Pawnshop - GTC") {
		frappe.db.get_value('Pawnshop Naming Series', "Garcia's Pawnshop - GTC",['jewelry_item_count', 'jewelry_inventory_count'])
		.then(value => {
			let non_jewelry_inventory_count = parseInt(value.message.jewelry_inventory_count);
			let non_jewelry_count = parseInt(value.message.jewelry_item_count)
			frm.set_value('batch_number', non_jewelry_inventory_count)
			frm.set_value('item_no', '4-' + non_jewelry_inventory_count + 'J' + '-' + non_jewelry_count)
		})
	} else if (frm.doc.branch == "Garcia's Pawnshop - MOL") {
		frappe.db.get_value('Pawnshop Naming Series', "Garcia's Pawnshop - MOL",['jewelry_item_count', 'jewelry_inventory_count'])
		.then(value => {
			let non_jewelry_inventory_count = parseInt(value.message.jewelry_inventory_count);
			let non_jewelry_count = parseInt(value.message.jewelry_item_count)
			frm.set_value('batch_number', non_jewelry_inventory_count)
			frm.set_value('item_no', '6-' + non_jewelry_inventory_count + 'J' + '-' + non_jewelry_count)
		})
	} else if (frm.doc.branch == "Garcia's Pawnshop - POB") {
		frappe.db.get_value('Pawnshop Naming Series', "Garcia's Pawnshop - POB",['jewelry_item_count', 'jewelry_inventory_count'])
		.then(value => {
			let non_jewelry_inventory_count = parseInt(value.message.jewelry_inventory_count);
			let non_jewelry_count = parseInt(value.message.jewelry_item_count)
			frm.set_value('batch_number', non_jewelry_inventory_count)
			frm.set_value('item_no', '3-' + non_jewelry_inventory_count + 'J' + '-' + non_jewelry_count)
		})
	} else if (frm.doc.branch == "Garcia's Pawnshop - TNZ") {
		frappe.db.get_value('Pawnshop Naming Series', "Garcia's Pawnshop - TNZ",['jewelry_item_count', 'jewelry_inventory_count'])
		.then(value => {
			let non_jewelry_inventory_count = parseInt(value.message.jewelry_inventory_count);
			let non_jewelry_count = parseInt(value.message.jewelry_item_count)
			frm.set_value('batch_number', non_jewelry_inventory_count)
			frm.set_value('item_no', '5-' + non_jewelry_inventory_count + 'J' + '-' + non_jewelry_count)
		})
	} else if (frm.doc.branch == "Rabie's House") {
		frappe.db.get_value('Pawnshop Naming Series', "Rabie's House",['jewelry_item_count', 'jewelry_inventory_count'])
		.then(value => {
			let non_jewelry_inventory_count = parseInt(value.message.jewelry_inventory_count);
			let non_jewelry_count = parseInt(value.message.jewelry_item_count)
			frm.set_value('batch_number', non_jewelry_inventory_count)
			frm.set_value('item_no', '20-' + non_jewelry_inventory_count + 'J' + '-' + non_jewelry_count)
		})
	} 
}