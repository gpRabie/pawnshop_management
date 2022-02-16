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

		frm.add_custom_button('Compute Interest', () => {
			compute_interest(frm);
		})
	},

	pawn_ticket_no: function(frm){
		if (frm.doc.transaction_type == "Redemption") {
			frm.set_value('total', cur_frm.doc.principal_amount);
		}
	},

	transaction_type: function(frm){
		show_payment_fields(frm);
		// if (frm.doc.transaction_type == "Redemption") {
		// 	compute_interest();
		// }
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


function compute_interest(frm) {
	frappe.db.get_doc('Holiday List', 'No Operations').then(function(r){
		var holidays_list = r.holidays;
		var holidays_before_expiry_date = null;
		var holidays_after_expiry_date = null;
		var maturity_month_multiplier = calculate_maturity_date_multiplier(frm);
		var expiry_month_multiplier = calculate_expiry_date_multiplier(frm);
		var temp_maturity_date = cur_frm.doc.maturity_date;
		var temp_expiry_date = cur_frm.doc.expiry_date;
		
		var temp_maturity_date = frappe.datetime.add_months(cur_frm.doc.maturity_date, maturity_month_multiplier - 1)
		var temp_expiry_date = frappe.datetime.add_months(cur_frm.doc.expiry_date, expiry_month_multiplier)
		
		for (let index = 0; index < holidays_list.length; index++) {
			if (holidays_list[index].holiday_date == temp_maturity_date) {
				holidays_before_expiry_date = holidays_list[index].holiday_date
				break
			} else if (holidays_list[index].holiday_date == frappe.datetime.add_days(temp_maturity_date, 1)) {
				holidays_before_expiry_date = holidays_list[index].holiday_date
				break
			} else if (holidays_list[index].holiday_date == frappe.datetime.add_days(temp_maturity_date, 2)) {
				holidays_before_expiry_date = holidays_list[index].holiday_date
				break
			} else if (holidays_list[index].holiday_date == frappe.datetime.add_days(temp_maturity_date, 3)) {
				holidays_before_expiry_date = holidays_list[index].holiday_date
				break
			}
		}

		for (let index = 0; index < holidays_list.length; index++) {
			if (holidays_list[index].holiday_date == temp_expiry_date) {
				holidays_after_expiry_date = holidays_list[index].holiday_date
				break
			} else if (holidays_list[index].holiday_date == frappe.datetime.add_days(temp_expiry_date, 1)) {
				holidays_after_expiry_date = holidays_list[index].holiday_date
				break
			} else if (holidays_list[index].holiday_date == frappe.datetime.add_days(temp_expiry_date, 2)) {
				holidays_after_expiry_date = holidays_list[index].holiday_date
				break
			} else if (holidays_list[index].holiday_date == frappe.datetime.add_days(temp_expiry_date, 3)) {
				holidays_after_expiry_date = holidays_list[index].holiday_date
				break
			}
		}
		console.log(cur_frm.doc.date_loan_granted > cur_frm.doc.expiry_date);
		if (cur_frm.doc.date_loan_granted >= cur_frm.doc.maturity_date && cur_frm.doc.date_loan_granted <= cur_frm.doc.expiry_date) {
			if (holidays_before_expiry_date == temp_maturity_date) {
				console.log("SC1");
				if (cur_frm.doc.date_loan_granted > frappe.datetime.add_days(temp_maturity_date, 3)) {
					let temp_interest = 0.00;
					temp_interest = parseFloat(cur_frm.doc.interest) * maturity_month_multiplier;
					cur_frm.set_value('interest_payment', temp_interest)
					cur_frm.refresh_field('interest_payment')
				}
			} else if (holidays_before_expiry_date == frappe.datetime.add_days(temp_maturity_date, 1)) { //last day  of tawad is saturday
				console.log("SC2");
				if (cur_frm.doc.date_loan_granted > frappe.datetime.add_days(temp_maturity_date, 3)) {
					let temp_interest = 0.00;
					temp_interest = parseFloat(cur_frm.doc.interest) * maturity_month_multiplier;
					cur_frm.set_value('interest_payment', temp_interest)
					cur_frm.refresh_field('interest_payment')
				} 
			} else if (holidays_before_expiry_date == frappe.datetime.add_days(temp_maturity_date, 2)) {
				console.log("SC3");
				if (cur_frm.doc.date_loan_granted > frappe.datetime.add_days(temp_maturity_date, 3)) {
					let temp_interest = 0.00;
					temp_interest = parseFloat(cur_frm.doc.interest) * maturity_month_multiplier;
					cur_frm.set_value('interest_payment', temp_interest)
					cur_frm.refresh_field('interest_payment')
				} 
			} else if (holidays_before_expiry_date == frappe.datetime.add_days(temp_maturity_date, 3)) {
				console.log("SC4")
				if (cur_frm.doc.date_loan_granted > frappe.datetime.add_days(temp_maturity_date, 3)) {
					let temp_interest = 0.00;
					temp_interest = parseFloat(cur_frm.doc.interest) * maturity_month_multiplier;
					cur_frm.set_value('interest_payment', temp_interest)
					cur_frm.refresh_field('interest_payment')
				} 
			} else if(holidays_before_expiry_date != frappe.datetime.add_days(temp_maturity_date, 3) && holidays_before_expiry_date != frappe.datetime.add_days(temp_maturity_date, 2) && holidays_before_expiry_date != frappe.datetime.add_days(temp_maturity_date, 1) && holidays_before_expiry_date != temp_maturity_date){
				console.log("SC5");
				if (cur_frm.doc.date_loan_granted > frappe.datetime.add_days(temp_maturity_date, 2)) {
					let temp_interest = 0.00;
					temp_interest = parseFloat(cur_frm.doc.interest) * maturity_month_multiplier;
					cur_frm.set_value('interest_payment', temp_interest)
					cur_frm.refresh_field('interest_payment')
				}
			}
		} else if (cur_frm.doc.date_loan_granted > cur_frm.doc.expiry_date) {
			console.log(cur_frm.doc.date_loan_granted > cur_frm.doc.expiry_date);
			if (holidays_after_expiry_date == temp_expiry_date) {
				console.log("SC6");
				if (cur_frm.doc.date_loan_granted > frappe.datetime.add_days(temp_expiry_date, 3)) {
					let temp_interest = 0.00;
					temp_interest = (parseFloat(cur_frm.doc.interest) * expiry_month_multiplier) + calculate_interest_before_expiry(frm);
					cur_frm.set_value('interest_payment', temp_interest)
					cur_frm.refresh_field('interest_payment')
				} 
			} else if (holidays_after_expiry_date == frappe.datetime.add_days(temp_expiry_date, 1)) { //last day  of tawad is saturday
				console.log("SC7");
				console.log(cur_frm.doc.date_loan_granted >= temp_expiry_date && cur_frm.doc.date_loan_granted <= frappe.datetime.add_days(temp_expiry_date, 3));
				console.log(temp_expiry_date);
				if (cur_frm.doc.date_loan_granted > frappe.datetime.add_days(temp_expiry_date, 3)) {
					console.log("Hello");
					let temp_interest = 0.00;
					temp_interest = (parseFloat(cur_frm.doc.interest) * expiry_month_multiplier) + calculate_interest_before_expiry(frm);
					cur_frm.set_value('interest_payment', temp_interest)
					cur_frm.refresh_field('interest_payment')
				} else if(cur_frm.doc.date_loan_granted >= temp_expiry_date && cur_frm.doc.date_loan_granted <= frappe.datetime.add_days(temp_expiry_date, 3)){
					console.log("Hi");
					let temp_interest = 0.00; 
					if (frm.doc.date_loan_granted > frappe.datetime.add_days(temp_expiry_date, 3)) {
						temp_interest = parseFloat(cur_frm.doc.interest) * expiry_month_multiplier + calculate_interest_before_expiry(frm); 
						console.log(calculate_interest_before_expiry(frm));
						cur_frm.set_value('interest_payment', temp_interest)
						cur_frm.refresh_field('interest_payment')
					} else if(frm.doc.date_loan_granted > frappe.datetime.add_days(temp_expiry_date, 2)){
						temp_interest = parseFloat(cur_frm.doc.interest) * expiry_month_multiplier + (calculate_interest_before_expiry(frm) - parseFloat(cur_frm.doc.interest));
						console.log(calculate_interest_before_expiry(frm));
						cur_frm.set_value('interest_payment', temp_interest)
						cur_frm.refresh_field('interest_payment')
					} else {
						temp_interest = parseFloat(cur_frm.doc.interest) * expiry_month_multiplier + calculate_interest_before_expiry(frm); 
						console.log(calculate_interest_before_expiry(frm));
						cur_frm.set_value('interest_payment', temp_interest)
						cur_frm.refresh_field('interest_payment')
					}
				}
			} else if (holidays_after_expiry_date == frappe.datetime.add_days(temp_expiry_date, 2)) {
				console.log("SC8");
				if (cur_frm.doc.date_loan_granted > frappe.datetime.add_days(temp_expiry_date, 3)) {
					let temp_interest = 0.00;
					temp_interest = (parseFloat(cur_frm.doc.interest) * expiry_month_multiplier) + calculate_interest_before_expiry(frm);
					cur_frm.set_value('interest_payment', temp_interest)
					cur_frm.refresh_field('interest_payment')
				} else if(cur_frm.doc.date_loan_granted >= temp_expiry_date && cur_frm.doc.date_loan_granted <= frappe.datetime.add_days(temp_expiry_date, 3)){
					let temp_interest = 0.00;
					temp_interest = (parseFloat(cur_frm.doc.interest) * expiry_month_multiplier) + calculate_interest_before_expiry(frm);;
					console.log(temp_interest);
					cur_frm.set_value('interest_payment', temp_interest)
					cur_frm.refresh_field('interest_payment')
				}
			} else if (holidays_after_expiry_date == frappe.datetime.add_days(temp_expiry_date, 3)) {
				console.log("SC9")
				if (cur_frm.doc.date_loan_granted > frappe.datetime.add_days(temp_expiry_date, 3)) {
					let temp_interest = 0.00;
					temp_interest = (parseFloat(cur_frm.doc.interest) * expiry_month_multiplier) + calculate_interest_before_expiry(frm);
					cur_frm.set_value('interest_payment', temp_interest)
					cur_frm.refresh_field('interest_payment')
				} else if(cur_frm.doc.date_loan_granted >= temp_expiry_date && cur_frm.doc.date_loan_granted <= frappe.datetime.add_days(temp_expiry_date, 3)){
					let temp_interest = 0.00;
					temp_interest = (parseFloat(cur_frm.doc.interest) * expiry_month_multiplier) + calculate_interest_before_expiry(frm);;
					console.log(temp_interest);
					cur_frm.set_value('interest_payment', temp_interest)
					cur_frm.refresh_field('interest_payment')
				}
			} else if(holidays_after_expiry_date != frappe.datetime.add_days(temp_expiry_date, 3) && holidays_after_expiry_date != frappe.datetime.add_days(temp_expiry_date, 2) && holidays_after_expiry_date != frappe.datetime.add_days(temp_expiry_date, 1) && holidays_after_expiry_date != temp_expiry_date){
				console.log("SC10");
				console.log(temp_expiry_date);
				console.log(holidays_after_expiry_date)
				if (cur_frm.doc.date_loan_granted > frappe.datetime.add_days(temp_expiry_date, 2)) {
					console.log("Hello");
					let temp_interest = 0.00;
					temp_interest = (parseFloat(cur_frm.doc.interest) * expiry_month_multiplier) + calculate_interest_before_expiry(frm);
					cur_frm.set_value('interest_payment', temp_interest)
					cur_frm.refresh_field('interest_payment')
				} else if(cur_frm.doc.date_loan_granted >= temp_expiry_date && cur_frm.doc.date_loan_granted <= frappe.datetime.add_days(temp_expiry_date, 2)){
					let temp_interest = 0.00;
					temp_interest = (parseFloat(cur_frm.doc.interest) * expiry_month_multiplier) + calculate_interest_before_expiry(frm);;
					console.log(temp_interest);
					cur_frm.set_value('interest_payment', temp_interest)
					cur_frm.refresh_field('interest_payment')
				}
			}
		}
	})
}

function calculate_maturity_date_multiplier(frm) {
	var current_date = frm.doc.date_loan_granted.split("-");
	var maturity_date = frm.doc.maturity_date.split("-");
	var multiplier = 0;
	if (parseInt(current_date[1]) == parseInt(maturity_date[1])) {
		if (parseInt(current_date[2]) > parseInt(maturity_date[2])) {
			multiplier = 1
		}
	} else if (parseInt(current_date[1]) > parseInt(maturity_date[1])) {
		if (parseInt(current_date[2]) > parseInt(maturity_date[2])) {
			multiplier = (parseInt(current_date[1]) - parseInt(maturity_date[1])) + 1
		} else {
			multiplier = (parseInt(current_date[1]) - parseInt(maturity_date[1]))
		}
	}
	return multiplier
}


function calculate_expiry_date_multiplier(frm) {
	var current_date = frm.doc.date_loan_granted.split("-");
	var expiry_date = frm.doc.expiry_date.split("-");
	var multiplier = 0;
	if (parseInt(current_date[1]) == parseInt(expiry_date[1])) {
		if (parseInt(current_date[2]) >= parseInt(expiry_date[2])) {
			multiplier = (parseInt(current_date[1]) - parseInt(expiry_date[1]))
		}
	} else if (parseInt(current_date[1]) > parseInt(expiry_date[1])) {
		if (parseInt(current_date[2]) > parseInt(expiry_date[2])) {
			multiplier = (parseInt(current_date[1]) - parseInt(expiry_date[1])) + 1
		} else {
			multiplier = (parseInt(current_date[1]) - parseInt(expiry_date[1]))
		}
	}

	return multiplier
}

function calculate_interest_before_expiry(frm) {
	let maturity_month_multiplier = calculate_maturity_date_multiplier(frm);
	let temp_interest = 0.00;
	temp_interest = parseFloat(cur_frm.doc.interest) * maturity_month_multiplier;
	return temp_interest
}