// Copyright (c) 2022, Rabie Moses Santillan and contributors
// For license information, please see license.txt

frappe.ui.form.on('Pawn Ticket Non Jewelry', {
	before_workflow_action: function(frm){
		if (frm.selected_workflow_action === "Collect") { // Change status
			frappe.call({
				method: 'pawnshop_management.pawnshop_management.custom_codes.update_pawn_ticket.update_fields_after_status_change_collect_pawn_ticket',
				args: {
					pawn_ticket_type: "Pawn Ticket Non Jewelry",
					pawn_ticket_no: String(frm.doc.pawn_ticket),
					inventory_tracking_no: String(frm.doc.inventory_tracking_no)
				},
				callback: function(){
					frm.refresh_field('change_status_date');
				}
			})
		} else if (frm.selected_workflow_action === "Redeem") {
			frappe.call({
				method: 'pawnshop_management.pawnshop_management.custom_codes.update_pawn_ticket.update_fields_after_status_change_redeem_pawn_ticket',
				args: {
					pawn_ticket_type: "Pawn Ticket Non Jewelry",
					pawn_ticket_no: String(frm.doc.pawn_ticket),
					inventory_tracking_no: String(frm.doc.inventory_tracking_no)
				},
				callback: function(){
					frm.refresh_field('change_status_date');
				}
			})
		} else if (frm.selected_workflow_action === "Review") {
			frappe.call({
				method: 'pawnshop_management.pawnshop_management.custom_codes.update_pawn_ticket.update_fields_after_status_change_review_pawn_ticket',
				args: {
					pawn_ticket_type: "Pawn Ticket Non Jewelry",
					pawn_ticket_no: String(frm.doc.pawn_ticket),
					inventory_tracking_no: String(frm.doc.inventory_tracking_no)
				},
				callback: function(){
					frm.refresh_field('change_status_date')
				}
			})
		} else if (frm.selected_workflow_action === "Collect") {
			frappe.call({
				method: 'pawnshop_management.pawnshop_management.custom_codes.update_pawn_ticket.update_fields_after_status_change_collect_pawn_ticket',
				args: {
					pawn_ticket_type: "Pawn Ticket Non Jewelry",
					pawn_ticket_no: String(frm.doc.pawn_ticket),
					inventory_tracking_no: String(frm.doc.inventory_tracking_no)
				},
				callback: function(){
					frm.refresh_field('change_status_date')
				}
			})
		} else if (frm.selected_workflow_action === "Pull Out") {
			frappe.call({
				method: 'pawnshop_management.pawnshop_management.custom_codes.update_pawn_ticket.update_fields_after_status_change_pull_out_pawn_ticket',
				args: {
					pawn_ticket_type: "Pawn Ticket Non Jewelry",
					pawn_ticket_no: String(frm.doc.pawn_ticket),
					inventory_tracking_no: String(frm.doc.inventory_tracking_no)
				},
				callback: function(){
					frm.refresh_field('change_status_date')
				}
			})
		} 
	},

	validate: function(frm, cdt, cdn){
		var temp_principal = 0.0;
		$.each(frm.doc.non_jewelry_items, function(index, item){
			temp_principal += parseFloat(item.suggested_appraisal_value);
		});

		if (frm.doc.desired_principal > temp_principal) {
			frappe.throw(__('Desired Principal is greater than the total value of items'));
		}
	},
	after_save: function(frm){
		frm.set_df_property('customers_tracking_no', 'read_only', 1);
	},

	refresh: function(frm){
		frm.fields_dict["non_jewelry_items"].grid.grid_buttons.find(".grid-add-row")[0].style.visibility = "hidden";
		if (frm.is_new()) {
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
		frm.fields_dict["non_jewelry_items"].grid.grid_buttons.find(".grid-add-row")[0].innerHTML = "Add Item"	//Change "Add Row" button of jewelry_items table into "Add Item"

		frm.add_custom_button('Skip Pawn Ticket No', () => {
			frappe.call('pawnshop_management.pawnshop_management.custom_codes.update_pawn_ticket.increment_b_series',{
				branch: frm.doc.branch
			}).then(r => {
				show_tracking_no(frm)
			})
		})
		
		frappe.call({
			method: 'pawnshop_management.pawnshop_management.custom_codes.get_ip.get_ip_from_settings'
		}).then(result => {
			let branch_ip_settings = result.message;
			frappe.call({
				method: 'pawnshop_management.pawnshop_management.custom_codes.get_ip.get_ip'
			}).then(ip => {
				if (ip.message == branch_ip_settings["rabies_house"] || ip.message == branch_ip_settings["rabies_house"]) {
					frappe.db.get_value('Pawnshop Naming Series', "Rabie's House", 'inventory_count')
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
					frappe.db.get_value('Pawnshop Naming Series', "Garcia's Pawnshop - CC", 'inventory_count')
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
					frappe.db.get_value('Pawnshop Naming Series', "Garcia's Pawnshop - GTC", 'inventory_count')
					.then(r =>{
						let inventory_count = r.message.inventory_count
						frm.set_query('item_no', 'non_jewelry_items', function(){
							return {
								filters: {
									batch_number: String(inventory_count),
									branch: "Garcia's Pawnshop - GTC"
								}
							}
						})
					})
				} else if(ip.message == branch_ip_settings["molino"]) {
					frappe.db.get_value('Pawnshop Naming Series', "Garcia's Pawnshop - MOL", 'inventory_count')
					.then(r =>{
						let inventory_count = r.message.inventory_count
						frm.set_query('item_no', 'non_jewelry_items', function(){
							return {
								filters: {
									batch_number: String(inventory_count),
									branch: "Garcia's Pawnshop - MOL"
								}
							}
						})
					})
				} else if (ip.message == branch_ip_settings["poblacion"]) {
					frappe.db.get_value('Pawnshop Naming Series', "Garcia's Pawnshop - POB", 'inventory_count')
					.then(r =>{
						let inventory_count = r.message.inventory_count
						frm.set_query('item_no', 'non_jewelry_items', function(){
							return {
								filters: {
									batch_number: String(inventory_count),
									branch: "Garcia's Pawnshop - POB"
								}
							}
						})
					})
				} else if (ip.message == branch_ip_settings["tanza"]) {
					frappe.db.get_value('Pawnshop Naming Series', "Garcia's Pawnshop - TNZ", 'inventory_count')
					.then(r =>{
						let inventory_count = r.message.inventory_count
						frm.set_query('item_no', 'non_jewelry_items', function(){
							return {
								filters: {
									batch_number: String(inventory_count),
									branch: "Garcia's Pawnshop - TNZ"
								}
							}
						})
					})
				}
			})
		})
	},

	branch: function(frm){
		show_tracking_no(frm);
		if (frm.is_new() && frm.doc.amended_from == null) {
			frm.set_value('date_loan_granted', frappe.datetime.nowdate())
		}
	},

	date_loan_granted: function(frm){
		let default_maturity_date = frappe.datetime.add_days(frm.doc.date_loan_granted, 30);
		frm.set_value('maturity_date', default_maturity_date);

		let defaul_expiry_date = frappe.datetime.add_days(frm.doc.date_loan_granted, 90);
		frm.set_value('expiry_date', defaul_expiry_date);
	},

	desired_principal: function(frm, cdt, cdn) {
		show_tracking_no(frm);
		frm.refresh_fields('pawn_ticket');
		set_item_interest(frm)
	},

	inventory_tracking_no: function(frm, cdt, cdn){
		set_total_appraised_amount(frm, cdt, cdn);
	},

	customers_tracking_no: function(frm){
		show_tracking_no(frm)
	},

	amended_from: function(frm){
		show_tracking_no(frm)
	}

});

frappe.ui.form.on('Non Jewelry List', {
	item_no: function(frm, cdt, cdn){
		let table_length = parseInt(frm.doc.non_jewelry_items.length)
		if (frm.doc.non_jewelry_items.length > 1) {
			for (let index = 0; index < table_length - 1; index++) {
				if (frm.doc.non_jewelry_items[table_length-1].item_no == frm.doc.non_jewelry_items[index].item_no) {
					frm.doc.non_jewelry_items.pop(table_length-1);
					frm.refresh_field('jewelry_items');
					frappe.msgprint({
						title:__('Notification'),
						indicator:'red',
						message: __('Added item is already in the list. Item removed.')
					});
					set_total_appraised_amount(frm, cdt, cdn);
				}
			}
		}	
	},

	suggested_appraisal_value: function(frm, cdt, cdn){
		set_total_appraised_amount(frm,cdt, cdn);
	},

	non_jewelry_items_remove: function(frm, cdt, cdn){
		set_total_appraised_amount(frm, cdt, cdn);
		frm.fields_dict["non_jewelry_items"].grid.grid_buttons.find(".grid-add-row")[0].style.visibility = "visible";
	},

	non_jewelry_items_add: function(frm, cdt, cdn){
		frm.fields_dict["non_jewelry_items"].grid.grid_buttons.find(".grid-add-row")[0].style.visibility = "hidden";
	}
});


function show_tracking_no(frm){ //Sets inventory tracking number
	if (frm.doc.branch == "Garcia's Pawnshop - CC") {
		if (frm.doc.amended_from == null) {
			frappe.db.get_value('Pawnshop Naming Series', "Garcia's Pawnshop - CC",['b_series', 'inventory_count'])
			.then(value => {
				let tracking_no = value.message;
				let non_jewelry_count = parseInt(tracking_no.inventory_count);
				let new_ticket_no = parseInt(tracking_no.b_series);
				frm.set_value('pawn_ticket', "1-"+ new_ticket_no + frm.doc.item_series);
				frm.set_value('inventory_tracking_no', "1-"+ non_jewelry_count + 'NJ');
				frm.refresh_field('pawn_ticket');
			})
		} else {
			var previous_pt = frm.doc.amended_from      //Naming for the next document created of amend
			if (count_dash_characters(previous_pt) < 2) {
				frm.set_value('pawn_ticket', frm.doc.amended_from + "-1");
				frm.refresh_field('pawn_ticket');
			} else {
				var index_of_last_dash_caharacter = previous_pt.lastIndexOf("-")
				var current_amend_count = index_of_last_dash_caharacter.slice(index_of_last_dash_caharacter, -1)
				frm.set_value('pawn_ticket', frm.doc.amended_from + "-" + parseInt(current_amend_count) + 1);
				frm.refresh_field('pawn_ticket');
			}
		}
	} else if (frm.doc.branch == "Garcia's Pawnshop - GTC") {
		if (frm.doc.amended_from == null){
			frappe.db.get_value('Pawnshop Naming Series',"Garcia's Pawnshop - GTC",['b_series', 'inventory_count'])
			.then(value => {
				let tracking_no = value.message;
				let non_jewelry_count = parseInt(tracking_no.inventory_count);
				let new_ticket_no = parseInt(tracking_no.b_series);
				frm.set_value('pawn_ticket', "4-"+ new_ticket_no + frm.doc.item_series);
				frm.set_value('inventory_tracking_no', "4-" + non_jewelry_count + 'NJ');
				frm.refresh_field('pawn_ticket');
			})
		} else {
			var previous_pt = frm.doc.amended_from      //Naming for the next document created of amend
			if (count_dash_characters(previous_pt) < 2) {
				frm.set_value('pawn_ticket', frm.doc.amended_from + "-1");
				frm.refresh_field('pawn_ticket');
			} else {
				var index_of_last_dash_caharacter = previous_pt.lastIndexOf("-")
				var current_amend_count = index_of_last_dash_caharacter.slice(index_of_last_dash_caharacter, -1)
				frm.set_value('pawn_ticket', frm.doc.amended_from + "-" + parseInt(current_amend_count) + 1);
				frm.refresh_field('pawn_ticket');
			}
		}
		
	} else if (frm.doc.branch == "Garcia's Pawnshop - MOL") {
		if (frm.doc.amended_from == null) {
			frappe.db.get_value('Pawnshop Naming Series', "Garcia's Pawnshop - MOL",['b_series', 'inventory_count'])
			.then(value => {
				let tracking_no = value.message;
				let non_jewelry_count = parseInt(tracking_no.inventory_count);
				let new_ticket_no = parseInt(tracking_no.b_series);
				frm.set_value('pawn_ticket', "6-" +new_ticket_no + frm.doc.item_series);
				frm.set_value('inventory_tracking_no', "6-" + non_jewelry_count + 'NJ');
				frm.refresh_field('pawn_ticket');
			})
		} else {
			var previous_pt = frm.doc.amended_from      //Naming for the next document created of amend
			if (count_dash_characters(previous_pt) < 2) {
				frm.set_value('pawn_ticket', frm.doc.amended_from + "-1");
				frm.refresh_field('pawn_ticket');
			} else {
				var index_of_last_dash_caharacter = previous_pt.lastIndexOf("-")
				var current_amend_count = index_of_last_dash_caharacter.slice(index_of_last_dash_caharacter, -1)
				frm.set_value('pawn_ticket', frm.doc.amended_from + "-" + parseInt(current_amend_count) + 1);
				frm.refresh_field('pawn_ticket');
			}
		}
		
	} else if (frm.doc.branch == "Garcia's Pawnshop - POB") {
		if (frm.doc.amended_from == null) {
			frappe.db.get_value('Pawnshop Naming Series', "Garcia's Pawnshop - POB",['b_series', 'inventory_count'])
			.then(value => {
				let tracking_no = value.message;
				let non_jewelry_count = parseInt(tracking_no.inventory_count);
				let new_ticket_no = parseInt(tracking_no.b_series);
				frm.set_value('pawn_ticket', "3-" + new_ticket_no + frm.doc.item_series);
				frm.set_value('inventory_tracking_no', "3-"+ non_jewelry_count + 'NJ');
				frm.refresh_field('pawn_ticket');
			})
		} else {
			var previous_pt = frm.doc.amended_from      //Naming for the next document created of amend
			if (count_dash_characters(previous_pt) < 2) {
				frm.set_value('pawn_ticket', frm.doc.amended_from + "-1");
				frm.refresh_field('pawn_ticket');
			} else {
				var index_of_last_dash_caharacter = previous_pt.lastIndexOf("-")
				var current_amend_count = index_of_last_dash_caharacter.slice(index_of_last_dash_caharacter, -1)
				frm.set_value('pawn_ticket', frm.doc.amended_from + "-" + parseInt(current_amend_count) + 1);
				frm.refresh_field('pawn_ticket');
			}
		}
	} else if (frm.doc.branch == "Garcia's Pawnshop - TNZ") {
		if (frm.doc.amended_from == null) {
			frappe.db.get_value('Pawnshop Naming Series', "Garcia's Pawnshop - TNZ",['b_series', 'inventory_count'])
			.then(value => {
				let tracking_no = value.message;
				let non_jewelry_count = parseInt(tracking_no.inventory_count);
				let new_ticket_no = parseInt(tracking_no.b_series);
				frm.set_value('pawn_ticket', "5-"+ new_ticket_no + frm.doc.item_series);
				frm.set_value('inventory_tracking_no', "5-" + non_jewelry_count + 'NJ');
				frm.refresh_field('pawn_ticket');
			})
		} else {
			var previous_pt = frm.doc.amended_from      //Naming for the next document created of amend
			if (count_dash_characters(previous_pt) < 2) {
				frm.set_value('pawn_ticket', frm.doc.amended_from + "-1");
				frm.refresh_field('pawn_ticket');
			} else {
				var index_of_last_dash_caharacter = previous_pt.lastIndexOf("-")
				var current_amend_count = index_of_last_dash_caharacter.slice(index_of_last_dash_caharacter, -1)
				frm.set_value('pawn_ticket', frm.doc.amended_from + "-" + parseInt(current_amend_count) + 1);
				frm.refresh_field('pawn_ticket');
			}
		}
	} else if (frm.doc.branch == "Rabie's House") {
		if (frm.doc.amended_from == null) {
			console.log(frm.doc.amended_from);
			frappe.db.get_value('Pawnshop Naming Series', "Rabie's House",['b_series', 'inventory_count'])
			.then(value => {
				let tracking_no = value.message;
				let non_jewelry_count = parseInt(tracking_no.inventory_count);
				let new_ticket_no = parseInt(tracking_no.b_series);
				frm.set_value('pawn_ticket', "20-"+ new_ticket_no + frm.doc.item_series);
				frm.set_value('inventory_tracking_no', "20-" + non_jewelry_count + 'NJ');
				frm.refresh_field('pawn_ticket');
			})
		} else {
			var previous_pt = String(frm.doc.amended_from);      //Naming for the next document created of amend
			console.log(count_dash_characters(previous_pt));
			if (count_dash_characters(previous_pt) < 2) {
				console.log("Hi");
				frm.set_value('pawn_ticket', frm.doc.amended_from + "-1");
				frm.refresh_field('pawn_ticket');
			} else {
				console.log("Hello");
				var index_of_last_dash_caharacter = parseInt(frm.doc.amended_from.lastIndexOf("-"))
				var current_amend_count = frm.doc.amended_from.substr((index_of_last_dash_caharacter + 1))
				var original_pt = frm.doc.amended_from.slice(0, parseInt(index_of_last_dash_caharacter))

				frm.set_value('pawn_ticket', original_pt + "-" + (parseInt(current_amend_count) + 1));
				frm.refresh_field('pawn_ticket');
			}
		}
	} 
	
}

function set_total_appraised_amount(frm, cdt, cdn) { 			// Calculate Principal Amount
	let temp_principal = 0.00;
	$.each(frm.doc.non_jewelry_items, function(index, item){
		temp_principal += parseFloat(item.suggested_appraisal_value);
	});
	frm.set_value('desired_principal', temp_principal);
	set_item_interest(frm)
	return temp_principal
}

function set_item_interest(frm) {
	var principal = parseFloat(frm.doc.desired_principal);
	var interest = 0.00;
	var net_proceeds = 0.00;
	frappe.db.get_single_value('Pawnshop Management Settings', 'gadget_interest_rate').then(value => {
		interest = parseFloat(value)/100 * principal;
		frm.set_value('interest', interest);
		net_proceeds = principal - interest;
		frm.set_value('net_proceeds', net_proceeds)
	});
}

function null_checker(number) {
	if (number == null) {
		number = 0;
	}
	return parseInt(number)
}

function count_dash_characters(string) {
	var dash_character_count = 0
	for (let index = 0; index < string.length; index++) {
		if (string[index] == "-") {
			dash_character_count++
		}
	}
	return dash_character_count
}