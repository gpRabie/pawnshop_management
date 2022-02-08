// Copyright (c) 2022, Rabie Moses Santillan and contributors
// For license information, please see license.txt

frappe.ui.form.on('Pawn Ticket Non Jewelry', {
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
		if (frm.is_new()) {
			show_tracking_no(frm);
			frm.set_value('date_loan_granted', frappe.datetime.nowdate())
		}
		frm.fields_dict["non_jewelry_items"].grid.grid_buttons.find(".grid-add-row")[0].innerHTML = "Add Item"	//Change "Add Row" button of jewelry_items table into "Add Item"
		frappe.call({
			method: 'frappe.client.get_value',
			args: {
				'doctype': 'Pawnshop Management Settings',
				'fieldname': 'non_jewelry_inventory_count'
			},
			callback: function(r){
				let inventory_count = r.message
				frm.set_query('item_no', 'non_jewelry_items', function(){
					return {
						"filters": {
							"batch_number": String(parseInt(inventory_count.non_jewelry_inventory_count)),
						}
					};
				});
			}
		})

		frm.add_custom_button('Test', () => {
			frappe.call({
				method: 'pawnshop_management.pawnshop_management.custom_codes.update_pawn_ticket.update_pawn_tickets',
				callback: function(data){
					console.log(data.message);
				}
			})
		})
	},

	date_loan_granted: function(frm){
		let default_maturity_date = frappe.datetime.add_days(frm.doc.date_loan_granted, 30);
		frm.set_value('maturity_date', default_maturity_date);

		let defaul_expiry_date = frappe.datetime.add_days(frm.doc.date_loan_granted, 120);
		frm.set_value('expiry_date', defaul_expiry_date);
	},

	desired_principal: function(frm, cdt, cdn) {
		show_tracking_no(frm);
		frm.refresh_fields('pawn_ticket');
		set_item_interest(frm)
	},

	inventory_tracking_no: function(frm, cdt, cdn){
		// get_items(frm.doc.inventory_tracking_no);
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
	}	
});


function show_tracking_no(frm){ //Sets inventory tracking number
	frappe.call({
		method: 'frappe.client.get_value',
		args: {
			'doctype': 'Pawnshop Management Settings',
			'fieldname': [
				'b_series_current_count',
				'non_jewelry_inventory_count',
			]
		},

		callback: function(value){
			let tracking_no = value.message;
			let non_jewelry_count = parseInt(tracking_no.non_jewelry_inventory_count);
			let new_ticket_no = parseInt(tracking_no.b_series_current_count);
			frm.set_value('pawn_ticket', new_ticket_no + frm.doc.item_series);
			frm.set_value('inventory_tracking_no', non_jewelry_count + 'NJ');
			frm.refresh_field('pawn_ticket');
		},

		error: function(value){
			console.error('Error! Check show_tracking_no block');
		}
	});
	
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

// function get_items(inventory_no) {
// 	frappe.db.get_doc('Non Jewelry Batch', inventory_no).then(function(r){
// 		item_list = r.items
// 		for (let index = 0; index < array.length; index++) {
			
			
// 		}
// 	})
// }