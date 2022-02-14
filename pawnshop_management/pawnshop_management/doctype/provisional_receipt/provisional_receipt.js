// Copyright (c) 2022, Rabie Moses Santillan and contributors
// For license information, please see license.txt

frappe.ui.form.on('Provisional Receipt', {
	refresh: function(frm) {
		frm.set_query('pawn_ticket_type', () => {
			return {
				"filters": {
					"name": 
					[
						'in',
						[
							"Pawn Ticket Jewelry", 
							"Pawn Ticket Non Jewelry"
						]
					]
				}
			}
		})

		frm.set_query('pawn_ticket_no', () => {
			return {
				"filters": {
					"workflow_state": "Active"
				}
			}
		})

		frm.add_custom_button('Get Days', () => {
			compute_interest();
		})
	},

	pawn_ticket_no: function(frm){
		if (frm.doc.transaction_type == "Redemption") {
			frm.set_value('total', cur_frm.doc.principal_amount);
		}
	},

	transaction_type: function(frm){
		show_payment_fields(frm);
		if (frm.doc.transaction_type == "Redemption") {
			compute_interest();
		}
		// } else if (frappe.datetime.nowdate() < frappe.datetime.add_days(frm.doc.maturity_date, 2)) {
		// 	if (frm.doc.transaction_type == "Redemption") {
		// 		frm.set_value('total', cur_frm.doc.principal_amount);
		// 		frm.set_df_property('amortization', 'hidden', 1);
		// 		frm.set_df_property('interest_payment', 'hidden', 1);
		// 		frm.set_df_property('additional_amortization', 'hidden', 1);
		// 	} else {
		// 		frm.set_value('total', 0.00);
		// 	}
		// }
	},

	amortization: function(frm){
		frm.set_value('total', parseFloat(frm.doc.total) + parseFloat(frm.doc.amortization))
		frm.refresh_field('total')
	},

	interest_payment: function(frm){
		frm.set_value('total', parseFloat(frm.doc.total) + parseFloat(frm.doc.interest_payment))
		frm.refresh_field('total')
	},

	discount: function(frm){
		frm.set_value('total', parseFloat(frm.doc.total) - parseFloat(frm.doc.discount))
		frm.refresh_field('total')
	},

	additional_amortization: function(frm){
		frm.set_value('total', parseFloat(frm.doc.total) + parseFloat(frm.doc.additional_amortization))
		frm.refresh_field('total')
	}
});

function show_payment_fields(frm) {
	frm.set_df_property('amortization', 'hidden', 0);
	frm.set_df_property('interest_payment', 'hidden', 0);
	frm.set_df_property('additional_amortization', 'hidden', 0);
}


function compute_interest() {
	frappe.db.get_doc('Holiday List', 'No Operations').then(function(r){
		var holidays_list = r.holidays;
		var holiday = null;
		var temp_maturity_date = cur_frm.doc.maturity_date
		var multiplier = Math.floor(frappe.datetime.get_day_diff(cur_frm.doc.date_loan_granted, cur_frm.doc.maturity_date)/30)
		var monitor = Math.ceil(frappe.datetime.get_day_diff(cur_frm.doc.date_loan_granted, cur_frm.doc.maturity_date)/30)
		temp_maturity_date = frappe.datetime.add_days(cur_frm.doc.maturity_date, 30 * multiplier);
		console.log(frappe.datetime.add_days(cur_frm.doc.maturity_date, 30 * monitor));
		for (let index = 0; index < holidays_list.length; index++) {
			if (holidays_list[index].holiday_date == temp_maturity_date) {
				holiday = holidays_list[index].holiday_date
				break
			} else if (holidays_list[index].holiday_date == frappe.datetime.add_days(temp_maturity_date, 1)) {
				holiday = holidays_list[index].holiday_date
				break
			} else if (holidays_list[index].holiday_date == frappe.datetime.add_days(temp_maturity_date, 2)) {
				holiday = holidays_list[index].holiday_date
				break
			} else if (holidays_list[index].holiday_date == frappe.datetime.add_days(temp_maturity_date, 3)) {
				holiday = holidays_list[index].holiday_date
				break
			}
		}

		if (holiday == temp_maturity_date) {
			console.log("Hello");
			if (cur_frm.doc.date_loan_granted > frappe.datetime.add_days(temp_maturity_date, 3)) {
				let temp_interest = 0.00;
				temp_interest = parseFloat(cur_frm.doc.interest) * parseFloat(Math.ceil(frappe.datetime.get_day_diff(cur_frm.doc.date_loan_granted, cur_frm.doc.maturity_date)/30))
				cur_frm.set_value('interest_payment', temp_interest)
				cur_frm.refresh_field('interest_payment')
			} else {
				let temp_interest = 0.00;
				temp_interest = parseFloat(cur_frm.doc.interest) * parseFloat(Math.floor(frappe.datetime.get_day_diff(cur_frm.doc.date_loan_granted, cur_frm.doc.maturity_date)/30))
				cur_frm.set_value('interest_payment', temp_interest)
				cur_frm.refresh_field('interest_payment')
			}
		} else if (holiday == frappe.datetime.add_days(temp_maturity_date, 1)) {
			console.log("Hi");
			if (cur_frm.doc.date_loan_granted > frappe.datetime.add_days(temp_maturity_date, 2)) {
				let temp_interest = 0.00;
				temp_interest = parseFloat(cur_frm.doc.interest) * parseFloat(Math.ceil(frappe.datetime.get_day_diff(cur_frm.doc.date_loan_granted, cur_frm.doc.maturity_date)/30))
				cur_frm.set_value('interest_payment', temp_interest)
				cur_frm.refresh_field('interest_payment')
			} else {
				let temp_interest = 0.00;
				temp_interest = parseFloat(cur_frm.doc.interest) * parseFloat(Math.floor(frappe.datetime.get_day_diff(cur_frm.doc.date_loan_granted, cur_frm.doc.maturity_date)/30))
				cur_frm.set_value('interest_payment', temp_interest)
				cur_frm.refresh_field('interest_payment')
			}
		} else if (holiday == frappe.datetime.add_days(temp_maturity_date, 2)) {
			console.log("Bye");
			if (cur_frm.doc.date_loan_granted > frappe.datetime.add_days(temp_maturity_date, 3)) {
				let temp_interest = 0.00;
				temp_interest = parseFloat(cur_frm.doc.interest) * parseFloat(Math.ceil(frappe.datetime.get_day_diff(cur_frm.doc.date_loan_granted, cur_frm.doc.maturity_date)/30))
				cur_frm.set_value('interest_payment', temp_interest)
				cur_frm.refresh_field('interest_payment')
			} else {
				let temp_interest = 0.00;
				temp_interest = parseFloat(cur_frm.doc.interest) * parseFloat(Math.floor(frappe.datetime.get_day_diff(cur_frm.doc.date_loan_granted, cur_frm.doc.maturity_date)/30))
				cur_frm.set_value('interest_payment', temp_interest)
				cur_frm.refresh_field('interest_payment')
			}
		} else if (holiday == frappe.datetime.add_days(temp_maturity_date, 3)) {
			console.log("Welcome")
			if (cur_frm.doc.date_loan_granted > frappe.datetime.add_days(temp_maturity_date, 1)) {
				let temp_interest = 0.00;
				temp_interest = parseFloat(cur_frm.doc.interest) * parseFloat(Math.ceil(frappe.datetime.get_day_diff(cur_frm.doc.date_loan_granted, cur_frm.doc.maturity_date)/30))
				cur_frm.set_value('interest_payment', temp_interest)
				cur_frm.refresh_field('interest_payment')
			} else {
				let temp_interest = 0.00;
				temp_interest = parseFloat(cur_frm.doc.interest) * parseFloat(Math.floor(frappe.datetime.get_day_diff(cur_frm.doc.date_loan_granted, cur_frm.doc.maturity_date)/30))
				cur_frm.set_value('interest_payment', temp_interest)
				cur_frm.refresh_field('interest_payment')
			}
		} else {
			console.log("Thank you");
			if (cur_frm.doc.date_loan_granted > frappe.datetime.add_days(temp_maturity_date, 2)) {
				let temp_interest = 0.00;
				temp_interest = parseFloat(cur_frm.doc.interest) * parseFloat(Math.ceil(frappe.datetime.get_day_diff(cur_frm.doc.date_loan_granted, cur_frm.doc.maturity_date)/30))
				cur_frm.set_value('interest_payment', temp_interest)
				cur_frm.refresh_field('interest_payment')
			} else {
				let temp_interest = 0.00;
				temp_interest = parseFloat(cur_frm.doc.interest) * parseFloat(Math.floor(frappe.datetime.get_day_diff(cur_frm.doc.date_loan_granted, cur_frm.doc.maturity_date)/30))
				cur_frm.set_value('interest_payment', temp_interest)
				cur_frm.refresh_field('interest_payment')
			}
		}
	})
}
