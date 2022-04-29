// Copyright (c) 2022, Rabie Moses Santillan and contributors
// For license information, please see license.txt

frappe.ui.form.on('Non Jewelry Batch', {
	onload_post_render: function(frm) {
		if (frm.is_new) {
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
								frm.set_value('branch', "Garcia'a Pawnshop - POB");
								frm.refresh_field('branch');
							} else if (current_ip == ip["molino"]) {
								frm.set_value('branch', "Garcia'a Pawnshop - MOL");
								frm.refresh_field('branch');
							} else if (current_ip == ip["gtc"]) {
								frm.set_value('branch', "Garcia'a Pawnshop - GTC");
								frm.refresh_field('branch');
							} else if (current_ip == ip["tanza"]) {
								frm.set_value('branch', "Garcia'a Pawnshop - TNZ");
								frm.refresh_field('branch');
							} else if (current_ip == ip["rabies_house"]) {
								frm.set_value('branch', "Rabie's House");
								frm.refresh_field('branch');
							}
						}
					})
				}
			})
		}

		frappe.call({
			method: 'pawnshop_management.pawnshop_management.custom_codes.get_ip.get_ip_from_settings'
		}).then(result => {
			let branch_ip_settings = result.message;
			frappe.call({
				method: 'pawnshop_management.pawnshop_management.custom_codes.get_ip.get_ip'
			}).then(ip => {
				if (ip.message == branch_ip_settings["rabies_house"] || ip.message == branch_ip_settings["rabies_house"]) {
					frappe.db.get_value('Non Jewelry Naming Series', "Rabie's House", 'inventory_count')
					.then(r =>{
						let inventory_count = r.message.inventory_count
						frm.set_query('item_no', 'non_jewelry_items', function(){
							return {
								filters: {
									batch_number: String(inventory_count),
									branch: "Rabie's House"
								}
							}
						})
					})
				} else if (ip.message == branch_ip_settings["cavite_city"]) {
					frappe.db.get_value('Non Jewelry Naming Series', "Garcia's Pawnshop - CC", 'inventory_count')
					.then(r =>{
						let inventory_count = r.message.inventory_count
						frm.set_query('item_no', 'non_jewelry_items', function(){
							return {
								filters: {
									batch_number: String(inventory_count),
									branch: "Garcia's Pawnshop - CC"
								}
							}
						})
					})
				} else if (ip.message == branch_ip_settings["gtc"]) {
					frappe.db.get_value('Non Jewelry Naming Series', "Garcia'a Pawnshop - GTC", 'inventory_count')
					.then(r =>{
						let inventory_count = r.message.inventory_count
						frm.set_query('item_no', 'non_jewelry_items', function(){
							return {
								filters: {
									batch_number: String(inventory_count),
									branch: "Garcia'a Pawnshop - GTC"
								}
							}
						})
					})
				} else if(ip.message == branch_ip_settings["molino"]) {
					frappe.db.get_value('Non Jewelry Naming Series', "Garcia'a Pawnshop - MOL", 'inventory_count')
					.then(r =>{
						let inventory_count = r.message.inventory_count
						frm.set_query('item_no', 'non_jewelry_items', function(){
							return {
								filters: {
									batch_number: String(inventory_count),
									branch: "Garcia'a Pawnshop - MOL"
								}
							}
						})
					})
				} else if (ip.message == branch_ip_settings["poblacion"]) {
					frappe.db.get_value('Non Jewelry Naming Series', "Garcia'a Pawnshop - POB", 'inventory_count')
					.then(r =>{
						let inventory_count = r.message.inventory_count
						frm.set_query('item_no', 'non_jewelry_items', function(){
							return {
								filters: {
									batch_number: String(inventory_count),
									branch: "Garcia'a Pawnshop - POB"
								}
							}
						})
					})
				} else if (ip.message == branch_ip_settings["tanza"]) {
					frappe.db.get_value('Non Jewelry Naming Series', "Garcia'a Pawnshop - TNZ", 'inventory_count')
					.then(r =>{
						let inventory_count = r.message.inventory_count
						frm.set_query('item_no', 'non_jewelry_items', function(){
							return {
								filters: {
									batch_number: String(inventory_count),
									branch: "Garcia'a Pawnshop - TNZ"
								}
							}
						})
					})
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