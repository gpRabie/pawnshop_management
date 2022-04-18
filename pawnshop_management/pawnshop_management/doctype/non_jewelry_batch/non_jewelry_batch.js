// Copyright (c) 2022, Rabie Moses Santillan and contributors
// For license information, please see license.txt

frappe.ui.form.on('Non Jewelry Batch', {
	onload_post_render: function(frm) {
		if (frm.is_new) {
			frappe.call({
				method: 'pawnshop_management.pawnshop_management.custom_codes.get_ip.get_ip',
				callback: function(data){
					let current_ip = data.message
					let branch_ip = {
						"180.195.203.152" : "Garcia's Pawnshop - CC",
						"180.191.232.68" : "Garcia'a Pawnshop - GTC",
						"49.144.100.169" : "Garcia'a Pawnshop - MOL",
						"49.144.9.203" : "Garcia'a Pawnshop - POB",
						"136.158.82.68" : "Garcia'a Pawnshop - TNZ",
						"127.0.0.1" : "Rabie's House"
					}
					frm.set_value('branch', branch_ip[String(current_ip)]);
					frm.refresh_field('branch');
				}
			})
		}

		frappe.db.get_single_value('Pawnshop Management Settings', 'non_jewelry_inventory_count')
			.then(inventory_count => {
				frm.set_query('item_no', 'items', () => {
					return {
						"filters": {
							"batch_number": String(inventory_count)
						}
					}
				})
			})
		frm.fields_dict["items"].grid.grid_buttons.find(".grid-add-row")[0].hidden = true // Hides "Add Row" button of non_jewelry_items table

		frm.add_custom_button('Test', () => {
			console.log(frm.doc.inventory_tracking_no);
			console.log(get_inventory_batch(frm));
		})
	},

	branch: function(frm){
		get_inventory_batch(frm);
	}
});

function get_inventory_batch(frm) {
	if (frm.doc.branch == "Garcia's Pawnshop - CC") {
		frappe.db.get_value('Non Jewelry Naming Series', 'Cavite City Branch',['b_series', 'inventory_count'])
		.then(value => {
			let tracking_no = value.message;
			let non_jewelry_count = parseInt(tracking_no.inventory_count);
			frm.set_value('inventory_tracking_no', non_jewelry_count + 'NJ');
		})
	} else if (frm.doc.branch == "Garcia'a Pawnshop - GTC") {
		frappe.db.get_value('Non Jewelry Naming Series', 'GTC Branch',['b_series', 'inventory_count'])
		.then(value => {
			let tracking_no = value.message;
			let non_jewelry_count = parseInt(tracking_no.inventory_count);
			frm.set_value('inventory_tracking_no', non_jewelry_count + 'NJ');
	
		})
	} else if (frm.doc.branch == "Garcia'a Pawnshop - MOL") {
		frappe.db.get_value('Non Jewelry Naming Series', 'Molino Branch',['b_series', 'inventory_count'])
		.then(value => {
			let tracking_no = value.message;
			let non_jewelry_count = parseInt(tracking_no.inventory_count);
			frm.set_value('inventory_tracking_no', non_jewelry_count + 'NJ');
		})
	} else if (frm.doc.branch == "Garcia'a Pawnshop - POB") {
		frappe.db.get_value('Non Jewelry Naming Series', 'Poblacion Branch',['b_series', 'inventory_count'])
		.then(value => {
			let tracking_no = value.message;
			let non_jewelry_count = parseInt(tracking_no.inventory_count);
			frm.set_value('inventory_tracking_no', non_jewelry_count + 'NJ');
		})
	} else if (frm.doc.branch == "Garcia'a Pawnshop - TNZ") {
		frappe.db.get_value('Non Jewelry Naming Series', 'Tanza Branch',['b_series', 'inventory_count'])
		.then(value => {
			let tracking_no = value.message;
			let non_jewelry_count = parseInt(tracking_no.inventory_count);
			frm.set_value('inventory_tracking_no', non_jewelry_count + 'NJ');
		})
	} else if (frm.doc.branch == "Rabie's House") {
		frappe.db.get_value('Non Jewelry Naming Series', "Rabie's House",['b_series', 'inventory_count'])
		.then(value => {
			let tracking_no = value.message;
			let non_jewelry_count = parseInt(tracking_no.inventory_count);
			frm.set_value('inventory_tracking_no', non_jewelry_count + 'NJ');
		})
	} 
}

// function show_items(frm, doc_table_name = null) {
// 	frm.clear_table('non_jewelry_items');
// 	var temp_principal = 0.00
// 	frappe.db.get_doc("Non Jewelry Batch", frm.doc.inventory_tracking_no).then(function(r){
// 		var item_list = r.items
// 		for (let index = 0; index < item_list.length; index++) {
// 			let childTable = cur_frm.add_child("non_jewelry_items");
// 			childTable.item_no = item_list[index].item_no;
// 			console.log(item_list[index].item_no);
// 			childTable.type = item_list[index].type;
// 			childTable.brand = item_list[index].brand;
// 			childTable.model = item_list[index].model;
// 			childTable.model_number = item_list[index].model_number;
// 			childTable.suggested_appraisal_value = item_list[index].suggested_appraisal_value;
// 			temp_principal += parseFloat(item_list[index].suggested_appraisal_value)
// 		}
// 		cur_frm.refresh_field('non_jewelry_items');
// 		frm.set_value('desired_principal', temp_principal);
// 		frm.refresh_field('desired_principal');
// 	})
// }