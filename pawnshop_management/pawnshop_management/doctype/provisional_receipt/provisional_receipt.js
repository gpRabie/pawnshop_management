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
			// calculate_maturity_date_interest(frm)
			// console.log(expiry_interest_multiplier(frm));
			console.log(calculate_expiry_date_interest(frm));
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


function calculate_maturity_date_interest(frm) {
	frappe.db.get_doc('Holiday List', 'No Operations').then(function(r){
		var holidays_list = r.holidays;
		var holidays_before_expiry_date = null;
		var temp_maturity_date = maturity_date_of_the_month(frm)
		var current_date = frm.doc.date_loan_granted.split("-");
		var maturity_date = temp_maturity_date
		var multiplier = maturity_interest_multiplier(frm);
		var temp_interest = frm.doc.interest;

		for (let index = 0; index < holidays_list.length; index++) {				// Check if maturity date is a holiday
			if (holidays_list[index].holiday_date == temp_maturity_date.previous_maturity_date) {
				holidays_before_expiry_date = holidays_list[index].holiday_date
				break
			} else if (holidays_list[index].holiday_date == frappe.datetime.add_days(temp_maturity_date.previous_maturity_date, 1)) {
				holidays_before_expiry_date = holidays_list[index].holiday_date
				break
			} else if (holidays_list[index].holiday_date == frappe.datetime.add_days(temp_maturity_date.previous_maturity_date, 2)) {
				holidays_before_expiry_date = holidays_list[index].holiday_date
				break
			} else if (holidays_list[index].holiday_date == frappe.datetime.add_days(temp_maturity_date.previous_maturity_date, 3)) {
				holidays_before_expiry_date = holidays_list[index].holiday_date
				break
			}
		}



		if (frm.doc.date_loan_granted > frm.doc.maturity_date) {
			console.log(temp_maturity_date.previous_maturity_date == holidays_before_expiry_date);
			if (temp_maturity_date.previous_maturity_date == holidays_before_expiry_date) {
				console.log("SC1");
				console.log(frm.doc.date_loan_granted > frappe.datetime.add_days(temp_maturity_date.previous_maturity_date, 3));
				if (frm.doc.date_loan_granted > frappe.datetime.add_days(temp_maturity_date.previous_maturity_date, 3)) {
					console.log(multiplier);
					temp_interest = temp_interest * multiplier;
				} else {
					temp_interest = temp_interest * (multiplier - 1);
					if (temp_interest < 0) {
						temp_interest = 0.00
					}
				}
			} else if (frappe.datetime.add_days(temp_maturity_date.previous_maturity_date, 3) == holidays_before_expiry_date) {
				console.log("SC2");
				if (frm.doc.date_loan_granted > frappe.datetime.add_days(temp_maturity_date.previous_maturity_date, 3)) {
					temp_interest = temp_interest * multiplier;
				} else {
					temp_interest = temp_interest * (multiplier - 1);
					if (temp_interest < 0) {
						temp_interest = 0.00
					}
				}
			} else if (frappe.datetime.add_days(temp_maturity_date.previous_maturity_date, 2) == holidays_before_expiry_date) {
				console.log("SC3");
				if (frm.doc.date_loan_granted > frappe.datetime.add_days(temp_maturity_date.previous_maturity_date, 3)) {
					temp_interest = temp_interest * multiplier;
				} else {
					temp_interest = temp_interest * (multiplier - 1);
					if (temp_interest < 0) {
						temp_interest = 0.00
					}
				}
			} else if (frappe.datetime.add_days(temp_maturity_date.previous_maturity_date, 1) == holidays_before_expiry_date) {
				console.log("SC4");
				if (frm.doc.date_loan_granted > frappe.datetime.add_days(temp_maturity_date.previous_maturity_date, 3)) {
					temp_interest = temp_interest * multiplier;
				} else {
					temp_interest = temp_interest * (multiplier - 1);
					if (temp_interest < 0) {
						temp_interest = 0.00
					}
				}
			} else {
				console.log("SC5");
				if (frm.doc.date_loan_granted > frappe.datetime.add_days(temp_maturity_date.previous_maturity_date, 2)) {
					console.log("SBC1");
					temp_interest = temp_interest * multiplier;
				} else {
					console.log("SCB2");
					temp_interest = temp_interest * (multiplier - 1);
					if (temp_interest < 0) {
						temp_interest = 0.00
					}
				}
			}
		} else {
			temp_interest = 0.00;
		}

		frm.set_value('interest_payment', temp_interest);
		frm.refresh_field('interest_payment');
	});
}

function maturity_date_of_the_month(frm) {
	var current_date = frm.doc.date_loan_granted.split("-");
	var maturity_date = frm.doc.maturity_date.split("-");
	var expiry_date = frm.doc.expiry_date.split("-")
	var month_difference = 0;
	var previous_maturity_date = null;
	var current_maturity_date = frm.doc.maturity_date;
	var previous_maturity_date = frm.doc.maturity_date;
	
	if (parseInt(current_date[0]) > parseInt(maturity_date[0])) { //Calculate month difference if maturity date is for next year
		month_difference = Math.abs(parseInt(current_date[1]) - (12 - parseInt(maturity_date[1])));
	} else if(parseInt(current_date[0]) == parseInt(maturity_date[0])){ // Calculate month difference if maturity date is the same year
		month_difference = parseInt(current_date[1]) - parseInt(maturity_date[1]);
		if (month_difference < 0) {
			month_difference = 0;
		}
	}
	
	current_maturity_date = frappe.datetime.add_months(current_maturity_date, month_difference);
	var current_maturity_date_day = current_maturity_date.split("-");

	if (current_date[0] > maturity_date[0]){
		if (current_date[2] > maturity_date[2]) {
			current_maturity_date = frappe.datetime.add_months(frm.doc.maturity_date, month_difference);
			previous_maturity_date = frappe.datetime.add_months(current_maturity_date, -1);
		}
	} else if (condition) {
		if (current_date[1] > maturity_date[1]) {
			if (current_date[2] > current_maturity_date_day[2]) {
				current_maturity_date = frappe.datetime.add_months(frm.doc.maturity_date, month_difference + 1);
				previous_maturity_date = frappe.datetime.add_months(current_maturity_date, -1);
			} else {
				current_maturity_date = frappe.datetime.add_months(frm.doc.maturity_date, month_difference);
				previous_maturity_date = frappe.datetime.add_months(current_maturity_date, -1);
			}
		} else if(current_date[1] == maturity_date[1]){
			if (current_date[2] > current_maturity_date_day[2]) {
				current_maturity_date = frappe.datetime.add_months(frm.doc.maturity_date, month_difference + 1);
				previous_maturity_date = frappe.datetime.add_months(current_maturity_date, -1);
			} 
		} 
	}

	
	if (current_maturity_date > cur_frm.doc.expiry_date) {
		current_maturity_date = frappe.datetime.add_days(current_maturity_date, parseInt(maturity_date[2])*-1)
		current_maturity_date = frappe.datetime.add_days(current_maturity_date, parseInt(expiry_date[2]))
	}
	return {
		'previous_maturity_date': previous_maturity_date,
		'current_maturity_date': current_maturity_date
	}
}


function maturity_interest_multiplier(frm) {
	var temp_maturity_date = maturity_date_of_the_month(frm).previous_maturity_date.split("-");
	var maturity_date = frm.doc.maturity_date.split("-");
	var multiplier = 0;
	var current_date = frm.doc.date_loan_granted.split("-");
	var actual_current_date = frm.doc.date_loan_granted;
	var actual_original_maturity_date = frm.doc.maturity_date;
	
	if (parseInt(temp_maturity_date[0]) > parseInt(maturity_date[0])) {
		console.log("A1");
		multiplier = parseInt(temp_maturity_date[1]) + (12 - parseInt(maturity_date[1]))
	} else if (parseInt(temp_maturity_date[0]) == parseInt(maturity_date[0])) {
		console.log("B1");
		if (parseInt(temp_maturity_date[1]) == parseInt(maturity_date[1])) {
			console.log("B1-1");
			if (actual_current_date > actual_original_maturity_date) {
				console.log("B1-2");
				multiplier = 1;
			} 
		}else if (parseInt(temp_maturity_date[1]) > parseInt(maturity_date[1])) {
			console.log("B2");
			if (actual_current_date > actual_original_maturity_date) {
				console.log("B2-1");
				multiplier = Math.abs(parseInt(temp_maturity_date[1]) - parseInt(maturity_date[1])) + 1;
			} else {
				console.log("B2-2");
				multiplier = Math.abs(parseInt(temp_maturity_date[1]) - parseInt(maturity_date[1]));
			}
		}
	}
	return multiplier;
}

function expiry_interest_multiplier(frm) {
	var temp_expiry_date = expiry_date(frm).previous_expiry_date.split("-");
	var original_expiry_date = frm.doc.expiry_date;
	var actual_current_date = frm.doc.date_loan_granted;
	var split_current_date = frm.doc.date_loan_granted.split("-")
	var split_original_expiry_date = frm.doc.expiry_date.split("-")
	var multiplier = 0;

	if (parseInt(temp_expiry_date[0]) > parseInt(split_original_expiry_date[0])) {
		console.log("A1");
		multiplier = parseInt(temp_expiry_date[1]) + (12 - parseInt(split_original_expiry_date[1]))
	} else if (parseInt(temp_expiry_date[0]) == parseInt(split_original_expiry_date[0])) {
		console.log("B1");
		if (parseInt(temp_expiry_date[1]) == parseInt(split_original_expiry_date[1])) {
			console.log("B1-1");
			if (actual_current_date > original_expiry_date) {
				console.log("B1-2");
				multiplier = 1;
			} 
		}else if (parseInt(temp_expiry_date[1]) > parseInt(split_original_expiry_date[1])) {
			console.log("B2");
			if (actual_current_date > original_expiry_date) {
				console.log("B2-1");
				multiplier = Math.abs(parseInt(temp_expiry_date[1]) - parseInt(split_original_expiry_date[1])) + 1;
			} else {
				console.log("B2-2");
				multiplier = Math.abs(parseInt(temp_expiry_date[1]) - parseInt(split_original_expiry_date[1]));
			}
		}
	}
	return multiplier
}

function expiry_date(frm) {
	var actual_current_date = frm.doc.date_loan_granted;
	var actual_previous_expiry_date = frm.doc.expiry_date;
	var actual_current_expiry_date = frm.doc.expiry_date;
	var previous_expiry_date = actual_previous_expiry_date.split("-");
	var current_expiry_date = actual_current_expiry_date.split("-");
	var current_date = actual_current_date.split("-");
	var month_difference = 0;
	

	if (actual_current_date > actual_previous_expiry_date) {
		if (parseInt(current_date[0]) > parseInt(previous_expiry_date[0])) {
			month_difference = parseInt(current_date[1]) + (12 - parseInt(previous_expiry_date[1]))
		} else if (parseInt(current_date[0]) == parseInt(previous_expiry_date[0])) {
			month_difference = parseInt(current_date[1]) - parseInt(previous_expiry_date[1]);
			if (month_difference < 0) {
				month_difference = 0;
			}
		}
	}

	if (current_date[0] > previous_expiry_date[0]){
		if (current_date[2] > previous_expiry_date[2]) {
			actual_current_expiry_date = frappe.datetime.add_months(actual_current_expiry_date, month_difference);
			actual_previous_expiry_date = frappe.datetime.add_months(actual_current_expiry_date, -1);
		}
	} else if (current_date[0] == previous_expiry_date[0]) {
		if (current_date[1] > previous_expiry_date[1]) {
			if (current_date[2] > previous_expiry_date[2]) {
				actual_current_expiry_date = frappe.datetime.add_months(actual_current_expiry_date, month_difference + 1);
				actual_previous_expiry_date = frappe.datetime.add_months(actual_current_expiry_date, -1);
			} else {
				actual_current_expiry_date = frappe.datetime.add_months(actual_current_expiry_date, month_difference);
				actual_previous_expiry_date = frappe.datetime.add_months(actual_current_expiry_date, -1);
			}
		} else if(current_date[1] == previous_expiry_date[1]){
			if (current_date[2] > previous_expiry_date[2]) {
				actual_current_expiry_date = frappe.datetime.add_months(actual_current_expiry_date, month_difference + 1);
				actual_previous_expiry_date = frappe.datetime.add_months(actual_current_expiry_date, -1);
			}
		}
	}
	return {
		'previous_expiry_date': actual_previous_expiry_date,
		'current_expiry_date': actual_current_expiry_date
	}
}

function calculate_expiry_date_interest(frm) {
	frappe.db.get_doc('Holiday List', 'No Operations').then(function(r){
		var holidays_list = r.holidays;
		var holidays_before_expiry_date = null;
		var initial_interest = parseFloat(frm.doc.interest) * 3;
		var temp_expiry_date = expiry_date(frm)
		var multiplier = expiry_interest_multiplier(frm);
		var temp_interest = frm.doc.interest

		for (let index = 0; index < holidays_list.length; index++) {
			
			if (holidays_list[index].holiday_date == temp_expiry_date.previous_expiry_date) {
				holidays_before_expiry_date = holidays_list[index].holiday_date
				break
			} else if (holidays_list[index].holiday_date == frappe.datetime.add_days(temp_expiry_date.previous_expiry_date, 1)) {
				holidays_before_expiry_date = holidays_list[index].holiday_date
				break
			} else if (holidays_list[index].holiday_date == frappe.datetime.add_days(temp_expiry_date.previous_expiry_date, 2)) {
				holidays_before_expiry_date = holidays_list[index].holiday_date
				break
			} else if (holidays_list[index].holiday_date == frappe.datetime.add_days(temp_expiry_date.previous_expiry_date, 3)) {
				holidays_before_expiry_date = holidays_list[index].holiday_date
				break
			}
		}
		//console.log(holidays_list[index].holiday_date);

		if (frm.doc.date_loan_granted > frm.doc.expiry_date) {
			if (temp_expiry_date.previous_expiry_date == holidays_before_expiry_date) {
				console.log("A1");
				if (frm.doc.date_loan_granted > frappe.datetime.add_days(temp_expiry_date.previous_expiry_date, 3)) {
					temp_interest = initial_interest + (temp_interest * multiplier);
				} else {
					multiplier = multiplier - 1;
					if (multiplier < 0) {
						multiplier = 0;
					}
					temp_interest = initial_interest + (temp_interest * (multiplier));
				}
			} else if(frappe.datetime.add_days(temp_expiry_date.previous_expiry_date, 3) == holidays_before_expiry_date){
				console.log("B1");
				if (frm.doc.date_loan_granted > frappe.datetime.add_days(temp_expiry_date.previous_expiry_date, 3)) {
					temp_interest = initial_interest + (temp_interest * multiplier);
				} else {
					multiplier = multiplier - 1;
					if (multiplier < 0) {
						multiplier = 0;
					}
					temp_interest = initial_interest + (temp_interest * (multiplier));
				}
			} else if (frappe.datetime.add_days(temp_expiry_date.previous_expiry_date, 2) == holidays_before_expiry_date) {
				console.log("C1");
				if (frm.doc.date_loan_granted > frappe.datetime.add_days(temp_expiry_date.previous_expiry_date, 3)) {
					temp_interest = initial_interest + (temp_interest * multiplier);
				} else {
					multiplier = multiplier - 1;
					if (multiplier < 0) {
						multiplier = 0;
					}
					temp_interest = initial_interest + (temp_interest * (multiplier));
				}
			} else if (frappe.datetime.add_days(temp_expiry_date.previous_expiry_date, 1) == holidays_before_expiry_date) {
				console.log("D1");
				if (frm.doc.date_loan_granted > frappe.datetime.add_days(temp_expiry_date.previous_expiry_date, 3)) {
					console.log("D1-1");
					console.log(multiplier);
					temp_interest = initial_interest + (temp_interest * multiplier);
				} else {
					multiplier = multiplier - 1;
					console.log("D1-2");
					if (multiplier < 0) {
						multiplier = 0;
					}
					temp_interest = initial_interest + (temp_interest * (multiplier));
				}
			} else {
				console.log(temp_expiry_date.previous_expiry_date);
				console.log(multiplier);
				console.log("E1");
				if (frm.doc.date_loan_granted > frappe.datetime.add_days(temp_expiry_date.previous_expiry_date, 2)) {
					console.log("E1-1");
					temp_interest = initial_interest + (temp_interest * (multiplier));
				} else {
					multiplier = multiplier - 1;
					console.log("E1-2");
					console.log(multiplier);
					if (multiplier < 0) {
						multiplier = 0;
					}
					temp_interest = initial_interest + (temp_interest * (multiplier));
				}
			}
		} else {
			temp_interest = initial_interest;
		}
		frm.set_value('interest_payment', temp_interest)
		frm.refresh_field('interest_payment')
	});
}