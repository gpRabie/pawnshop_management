// Copyright (c) 2022, Rabie Moses Santillan and contributors
// For license information, please see license.txt

frappe.ui.form.on('Non Jewelry Batch', {
	onload_post_render: function(frm) {
		if (frm.is_new) {
			frappe.db.get_single_value('Pawnshop Management Settings', 'non_jewelry_inventory_count')
			.then(inventory_count => {
				frm.set_value('inventory_tracking_no', inventory_count + "NJ")
				frm.refresh_field('inventory_tracking_no')
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
	}
});

function get_inventory_batch(frm) {
	var inventory_tracking_no = frm.doc.inventory_tracking_no;
	var batch_number = "";
	for (let index = 0; index < inventory_tracking_no.length; index++) {
		if (!isNaN(inventory_tracking_no[index])) {
			batch_number += inventory_tracking_no[index];
		}
	}
	return batch_number
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