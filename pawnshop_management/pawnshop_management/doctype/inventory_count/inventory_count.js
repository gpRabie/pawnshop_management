// Copyright (c) 2022, Rabie Moses Santillan and contributors
// For license information, please see license.txt

frappe.ui.form.on('Inventory Count', {
	// refresh: function(frm) {
	// 	let is_allowed = frappe.user_roles.includes('Administrator');
	// 	frm.toggle_enable(['date', 'branch'], is_allowed);
	// 	if (frm.is_new()) {
	// 		frappe.call({
	// 			method: 'pawnshop_management.pawnshop_management.custom_codes.get_ip.get_ip',
	// 			callback: function(data){
	// 				let current_ip = data.message
	// 				frappe.call({
	// 					method: 'pawnshop_management.pawnshop_management.custom_codes.get_ip.get_ip_from_settings',
	// 					callback: (result) => {
	// 						let ip = result.message;
	// 						if (current_ip == ip["cavite_city"]) {
	// 							frm.set_value('branch', "Garcia's Pawnshop - CC");
	// 							frm.refresh_field('branch');
	// 						} else if (current_ip == ip["poblacion"]) {
	// 							frm.set_value('branch', "Garcia's Pawnshop - POB");
	// 							frm.refresh_field('branch');
	// 						} else if (current_ip == ip["molino"]) {
	// 							frm.set_value('branch', "Garcia's Pawnshop - MOL");
	// 							frm.refresh_field('branch');
	// 						} else if (current_ip == ip["gtc"]) {
	// 							frm.set_value('branch', "Garcia's Pawnshop - GTC");
	// 							frm.refresh_field('branch');
	// 						} else if (current_ip == ip["tanza"]) {
	// 							frm.set_value('branch', "Garcia's Pawnshop - TNZ");
	// 							frm.refresh_field('branch');
	// 						} else if (current_ip == ip["rabies_house"]) {
	// 							frm.set_value('branch', "Rabie's House");
	// 							frm.refresh_field('branch');
	// 						}
	// 					}
	// 				})
	// 			}
	// 		})


	// 	}
	// },

	// branch: function(frm){
	// 	get_jewelry_a_count(frm)
	// 	get_jewelry_b_count(frm)
	// 	get_jewelry_nj_count(frm)
	// }
});

// function get_jewelry_a_count(frm) {
// 	let in_count_of_the_day = frappe.db.count('Pawn Ticket Jewelry', {'date_loan_granted': frm.doc.date ,'item_series': 'A', 'workflow_state': 'Active', 'branch': frm.doc.branch})
// 	let renewed_count_of_the_day = frappe.db.count('Pawn Ticket Jewelry', {'change_status_date': frm.doc.date, 'workflow_state': 'Renewed', 'item_series': 'A', 'branch': frm.doc.branch})
// 	let in_count = in_count_of_the_day - renewed_count_of_the_day
// 	let out_count = frappe.db.count('Pawn Ticket Jewelry', {'change_status_date': frm.doc.date, 'workflow_state': 'Redeemed', 'item_series': 'A', 'branch': frm.doc.branch})
// 	let pulled_out_of_the_day = frappe.db.count('Pawn Ticket Jewelry', {'date_loan_granted': frm.doc.date, 'item_series': 'A', 'workflow_state': 'Pulled Out', 'branch': frm.doc.branch})
// 	let returned_of_the_day = frappe.db.count('Pawn Ticket Jewelry', {'date_loan_granted': frm.doc.date, 'item_series': 'A', 'workflow_state': 'Returned', 'branch': frm.doc.branch})
// 	let total_active = frappe.db.count('Pawn Ticket Jewelry', {'date_loan_granted': ['<=', frm.doc.date], 'item_series': 'A', 'workflow_state': ['in', ['Active', 'Expired']], 'branch': frm.doc.branch})
// 	let total_expired = frappe.db.count('Pawn Ticket Jewelry', {'date_loan_granted': ['<=', frm.doc.date], 'item_series': 'A', 'workflow_state': 'Expired', 'branch': frm.doc.branch})
// 	frm.set_value('out_count_a', out_count)
// 	frm.set_value('in_count_a', in_count)
// 	frm.set_value('returned_a', returned_of_the_day)
// 	frm.set_value('pulled_out_a', pulled_out_of_the_day)
// 	frm.set_value('total_a', total_active + total_expired + returned_of_the_day - pulled_out_of_the_day)
// }

// function get_jewelry_b_count(frm) {
// 	let in_count_of_the_day = frappe.db.count('Pawn Ticket Jewelry', {'date_loan_granted': frm.doc.date ,'item_series': 'B', 'workflow_state': 'Active', 'branch': frm.doc.branch})
// 	let renewed_count_of_the_day = frappe.db.count('Pawn Ticket Jewelry', {'change_status_date': frm.doc.date, 'workflow_state': 'Renewed', 'item_series': 'B', 'branch': frm.doc.branch})
// 	let in_count = in_count_of_the_day - renewed_count_of_the_day
// 	let out_count = frappe.db.count('Pawn Ticket Jewelry', {'change_status_date': frm.doc.date, 'workflow_state': 'Redeemed', 'item_series': 'B', 'branch': frm.doc.branch})
// 	let pulled_out_of_the_day = frappe.db.count('Pawn Ticket Jewelry', {'date_loan_granted': frm.doc.date, 'item_series': 'B', 'workflow_state': 'Pulled Out', 'branch': frm.doc.branch})
// 	let returned_of_the_day = frappe.db.count('Pawn Ticket Jewelry', {'date_loan_granted': frm.doc.date, 'item_series': 'B', 'workflow_state': 'Returned', 'branch': frm.doc.branch})
// 	let total_active = frappe.db.count('Pawn Ticket Jewelry', {'date_loan_granted': ['<=', frm.doc.date], 'item_series': 'B', 'workflow_state': ['in', ['Active', 'Expired']], 'branch': frm.doc.branch})
// 	let total_expired = frappe.db.count('Pawn Ticket Jewelry', {'date_loan_granted': ['<=', frm.doc.date], 'item_series': 'B', 'workflow_state': 'Expired', 'branch': frm.doc.branch})
// 	frm.set_value('out_count_b', out_count)
// 	frm.set_value('in_count_b', in_count)
// 	frm.set_value('returned_b', returned_of_the_day)
// 	frm.set_value('pulled_out_b', pulled_out_of_the_day)
// 	frm.set_value('total_b', total_active + total_expired + returned_of_the_day - pulled_out_of_the_day)
// }

// function get_jewelry_nj_count(frm) {
// 	let in_count_of_the_day = frappe.db.count('Pawn Ticket Non Jewelry', {'date_loan_granted': frm.doc.date , 'workflow_state': 'Active', 'branch': frm.doc.branch})
// 	let renewed_count_of_the_day = frappe.db.count('Pawn Ticket Non Jewelry', {'change_status_date': frm.doc.date, 'workflow_state': 'Renewed', 'branch': frm.doc.branch})
// 	let in_count = in_count_of_the_day - renewed_count_of_the_day
// 	let out_count = frappe.db.count('Pawn Ticket Non Jewelry', {'change_status_date': frm.doc.date, 'workflow_state': 'Redeemed', 'branch': frm.doc.branch})
// 	let pulled_out_of_the_day = frappe.db.count('Pawn Ticket Non Jewelry', {'date_loan_granted': frm.doc.date, 'workflow_state': 'Pulled Out', 'branch': frm.doc.branch})
// 	let returned_of_the_day = frappe.db.count('Pawn Ticket Non Jewelry', {'date_loan_granted': frm.doc.date, 'workflow_state': 'Returned', 'branch': frm.doc.branch})
// 	let total_active = frappe.db.count('Pawn Ticket Non Jewelry', {'date_loan_granted': ['<=', frm.doc.date], 'workflow_state': ['in', ['Active', 'Expired']], 'branch': frm.doc.branch})
// 	let total_expired = frappe.db.count('Pawn Ticket Non Jewelry', {'date_loan_granted': ['<=', frm.doc.date], 'workflow_state': 'Expired', 'branch': frm.doc.branch})
// 	frm.set_value('out_count_nj', out_count)
// 	frm.set_value('in_count_nj', in_count)
// 	frm.set_value('returned_nj', returned_of_the_day)
// 	frm.set_value('pulled_out_nj', pulled_out_of_the_day)
// 	frm.set_value('total_nj', total_active + total_expired + returned_of_the_day - pulled_out_of_the_day)
// }
