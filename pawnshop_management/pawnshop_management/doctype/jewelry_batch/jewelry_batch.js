// Copyright (c) 2021, Rabie Moses Santillan and contributors
// For license information, please see license.txt

frappe.ui.form.on('Jewelry Batch', {
	refresh: function(frm) {
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
		}
	},

	branch: function(frm){
		get_inventory_batch(frm);
	}

});


function get_inventory_batch(frm) {
	if (frm.doc.branch == "Garcia's Pawnshop - CC") {
		frappe.db.get_value('Pawnshop Naming Series', 'Cavite City Branch',['jewelry_inventory_count'])
		.then(value => {
			let tracking_no = value.message;
			let non_jewelry_count = parseInt(tracking_no.jewelry_inventory_count);
			frm.set_value('inventory_tracking_no', non_jewelry_count + 'J');
		})
	} else if (frm.doc.branch == "Garcia's Pawnshop - GTC") {
		frappe.db.get_value('Pawnshop Naming Series', 'GTC Branch',['jewelry_inventory_count'])
		.then(value => {
			let tracking_no = value.message;
			let non_jewelry_count = parseInt(tracking_no.jewelry_inventory_count);
			frm.set_value('inventory_tracking_no', non_jewelry_count + 'J');
	
		})
	} else if (frm.doc.branch == "Garcia's Pawnshop - MOL") {
		frappe.db.get_value('Pawnshop Naming Series', 'Molino Branch',['jewelry_inventory_count'])
		.then(value => {
			let tracking_no = value.message;
			let non_jewelry_count = parseInt(tracking_no.jewelry_inventory_count);
			frm.set_value('inventory_tracking_no', non_jewelry_count + 'J');
		})
	} else if (frm.doc.branch == "Garcia's Pawnshop - POB") {
		frappe.db.get_value('Pawnshop Naming Series', 'Poblacion Branch',['jewelry_inventory_count'])
		.then(value => {
			let tracking_no = value.message;
			let non_jewelry_count = parseInt(tracking_no.jewelry_inventory_count);
			frm.set_value('inventory_tracking_no', non_jewelry_count + 'J');
		})
	} else if (frm.doc.branch == "Garcia's Pawnshop - TNZ") {
		frappe.db.get_value('Pawnshop Naming Series', 'Tanza Branch',['jewelry_inventory_count'])
		.then(value => {
			let tracking_no = value.message;
			let non_jewelry_count = parseInt(tracking_no.jewelry_inventory_count);
			frm.set_value('inventory_tracking_no', non_jewelry_count + 'J');
		})
	} else if (frm.doc.branch == "Rabie's House") {
		frappe.db.get_value('Pawnshop Naming Series', "Rabie's House",['jewelry_inventory_count'])
		.then(value => {
			let tracking_no = value.message;
			let non_jewelry_count = parseInt(tracking_no.jewelry_inventory_count);
			frm.set_value('inventory_tracking_no', non_jewelry_count + 'J');
		})
	} 
}
