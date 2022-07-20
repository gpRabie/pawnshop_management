// Copyright (c) 2022, Rabie Moses Santillan and contributors
// For license information, please see license.txt

frappe.ui.form.on('Cash Position Report', {
	refresh: function(frm) {
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
			// frappe.db.get_list('Cash Position Report', {
			// 	fields: ['ending_balance', 'date', 'creation'],
			// 	filters: {
			// 		date: frappe.datetime.add_days(frm.doc.date, -1)
			// 	}
			// }).then(records => {
			// 	let latest_record = records[0]
			// 	for (let index = 0; index < records.length; index++) {
			// 		if (latest_record.creation < records[index].creation) {
			// 			latest_record = records[index]
			// 			console.log(latest_record);
			// 		}
			// 	}
			// 	frm.set_value('beginning_balance', 0.00)
			// 	frm.set_value('beginning_balance', latest_record.ending_balance)
			// 	frm.refresh_field('beginning_balance')
			// })
		}
		// frm.set_value('date', frappe.datetime.now_date())
		// frm.add_custom_button('Test', () => {
		// 	get_provisional_receipts_of_the_day(frm, '2022-02-09');
		// 	get_non_jewelry_of_the_day(frm, '2022-02-27')
		// 	frappe.db.get_list('Cash Position Report', {
		// 		fields: ['ending_balance', 'date', 'creation'],
		// 		filters: {
		// 			date: frm.doc.date
		// 		}
		// 	}).then(records => {
		// 		// for (let index = 0; index < records.length; index++) {
		// 		// 	console.log(records[index]);
		// 		// 	frm.set_value('beginning_balance',records[index].ending_balance);
		// 		// 	frm.refresh_field('beginning_balance');
		// 		// }
		// 		console.log(records[0]);
		// 	})
		// })
	},

	branch: function(frm){
		get_beginning_balance(frm)
		get_provisional_receipts_of_the_day(frm, frm.doc.date);
		get_non_jewelry_of_the_day(frm, frm.doc.date);
		get_gcash_provisional_receipt(frm, frm.doc.date);
		select_naming_series(frm);
		get_jewelry_b_of_the_day(frm, frm.doc.date);
		get_jewelry_a_of_the_day(frm, frm.doc.date);
		get_additional_pawn_records(frm);
		get_additional_redeem(frm);
		get_additional_partial_payment(frm);
	},

	date: function(frm){
		// get_provisional_receipts_of_the_day(frm, frm.doc.date);
		// get_non_jewelry_of_the_day(frm, frm.doc.date)
		// select_naming_series(frm);
		// get_gcash_provisional_receipt(frm, frm.doc.date)
		// frappe.db.get_list('Cash Position Report', {
		// 	fields: ['ending_balance', 'date', 'creation'],
		// 	filters: {
		// 		date: frappe.datetime.add_days(frm.doc.date, -1)
		// 	}
		// }).then(records => {
		// 	let latest_record = records[0]
		// 	for (let index = 0; index < records.length; index++) {
		// 		if (latest_record.creation < records[index].creation) {
		// 			latest_record = records[index]
		// 		}
		// 	}
		// 	frm.set_value('beginning_balance', 0.00)
		// 	frm.set_value('beginning_balance', latest_record.ending_balance)
		// 	frm.refresh_field('beginning_balance')
		// })
	},

	validate: function(frm){
		if (frm.doc.total_cash != frm.doc.ending_balance) {
			frappe.throw("Cash on hand is not equal to the Ending Balance")
		}
	},

	beginning_balance: function(frm){
		frm.set_value('ending_balance', 0.00);
		frm.set_value('ending_balance', calculate_ending_balance());
		frm.refresh_field('ending_balance');
	},

	provisional_receipts: function(frm){
		frm.set_value('total_in', 0.00);
		frm.set_value('total_in', + calculate_total_in());
		frm.refresh_field('total_in');
	},

	selling: function(frm){
		frm.set_value('total_in', 0.00);
		frm.set_value('total_in', + calculate_total_in());
		frm.refresh_field('total_in');
	},

	cash_from_vault: function(frm){
		frm.set_value('total_in', 0.00);
		frm.set_value('total_in', + calculate_total_in());
		frm.refresh_field('total_in');
	},

	jewelry_a: function(frm){
		frm.set_value('total_out', 0.00);
		frm.set_value('total_out', calculate_total_out());
		frm.refresh_field('total_out');
	},

	jewelry_b: function(frm){
		frm.set_value('total_out', 0.00);
		frm.set_value('total_out', calculate_total_out());
		frm.refresh_field('total_out');
	},

	non_jewelry: function(frm){
		frm.set_value('total_out', 0.00);
		frm.set_value('total_out', calculate_total_out());
		frm.refresh_field('total_out');
	},

	agreement_to_sell: function(frm){
		frm.set_value('total_out', 0.00);
		frm.set_value('total_out', calculate_total_out());
		frm.refresh_field('total_out');
	},

	acknowledgement_receipts: function(frm){
		frm.set_value('total_out', 0.00);
		frm.set_value('total_out', calculate_total_out());
		frm.refresh_field('total_out');
	},

	gcash: function(frm){
		frm.set_value('total_out', 0.00);
		frm.set_value('total_out', calculate_total_out());
		frm.refresh_field('total_out');
	},

	bank_transfer: function(frm){
		frm.set_value('total_out', 0.00);
		frm.set_value('total_out', calculate_total_out());
		frm.refresh_field('total_out');
	},

	cash_to_vault: function(frm){
		frm.set_value('total_out', 0.00);
		frm.set_value('total_out', calculate_total_out());
		frm.refresh_field('total_out');
	},

	total_in: function(frm){
		frm.set_value('net_cash', 0.00);
		frm.set_value('net_cash', calculate_net_cash());
		frm.refresh_field('net_cash');
	},
	
	total_out: function(frm){
		frm.set_value('net_cash', 0.00);
		frm.set_value('net_cash', calculate_net_cash());
		frm.refresh_field('net_cash');
	},

	net_cash: function(frm){
		frm.set_value('ending_balance', 0.00);
		frm.set_value('ending_balance', calculate_ending_balance());
		frm.refresh_field('ending_balance');
	},

	one_thousand_php_bills: function(frm){
		total_cash_breakdown(frm);
	},

	five_hundred_php_bills: function(frm){
		total_cash_breakdown(frm);
	},

	two_hundred_php_bills: function(frm){
		total_cash_breakdown(frm);
	},

	one_hundred_php_bills: function(frm){
		total_cash_breakdown(frm);
	},

	fifty_php_bills: function(frm){
		total_cash_breakdown(frm);
	},

	twenty_php_bills: function(frm){
		total_cash_breakdown(frm);
	},

	ten_php_coin: function(frm){
		total_cash_breakdown(frm);
	},

	five_php_coin: function(frm){
		total_cash_breakdown(frm);
	},

	peso_php_coin: function(frm){
		total_cash_breakdown(frm);
	},

	twenty_five_cent_php_coin: function(frm){
		total_cash_breakdown(frm);
	},

	shortage_overage: function(frm){
		total_cash_breakdown(frm);
	}
});

function get_beginning_balance(frm) {
	frappe.call('pawnshop_management.pawnshop_management.custom_codes.get_latest_cpr.get_latest_cpr', {
		branch: frm.doc.branch
	}).then(record => {
		let beginning_balance = parseFloat(record.message);
		frm.set_value('beginning_balance', 0.00);
		frm.set_value('beginning_balance', beginning_balance);
		frm.refresh_field('beginning_balance');
	})
}

function calculate_total_in() {
	var total_in = parseFloat(cur_frm.doc.provisional_receipts) + parseFloat(cur_frm.doc.selling) + parseFloat(cur_frm.doc.cash_from_vault);
	return total_in;
}

function calculate_total_out(){
	var total_out = parseFloat(cur_frm.doc.jewelry_a) + parseFloat(cur_frm.doc.jewelry_b) + parseFloat(cur_frm.doc.cash_to_vault) + parseFloat(cur_frm.doc.non_jewelry) + parseFloat(cur_frm.doc.agreement_to_sell) + parseFloat(cur_frm.doc.acknowledgement_receipts) + parseFloat(cur_frm.doc.gcash) + parseFloat(cur_frm.doc.bank_transfer);
	return total_out;
}

function calculate_net_cash() {
	var net_cash = calculate_total_in() - calculate_total_out();
	return net_cash;
}

function calculate_ending_balance() {
	var ending_balance = parseFloat(cur_frm.doc.beginning_balance) + calculate_net_cash();
	return ending_balance;
}
function get_provisional_receipts_of_the_day(frm, date_today = null) {
	if (frm.doc.branch == "Rabie's House") {
		frappe.db.get_list('Provisional Receipt', {
			fields: ['total'],
			filters: {
				date_issued: date_today,
				docstatus: 1,
				branch: "Rabie's House"
			}
		}).then(records => {
			let temp_total = 0.00;
			frm.set_value('provisional_receipts', 0.00);
			for (let index = 0; index < records.length; index++) {
				temp_total += parseFloat(records[index].total)
			}
			frm.set_value('provisional_receipts', temp_total);
		})
	} else if (frm.doc.branch == "Garcia's Pawnshop - CC") {
		frappe.db.get_list('Provisional Receipt', {
			fields: ['total'],
			filters: {
				date_issued: date_today,
				docstatus: 1,
				branch: "Garcia's Pawnshop - CC"
			}
		}).then(records => {
			let temp_total = 0.00;
			frm.set_value('provisional_receipts', 0.00);
			for (let index = 0; index < records.length; index++) {
				temp_total += parseFloat(records[index].total)
			}
			frm.set_value('provisional_receipts', temp_total);
			frm.refresh_field('provisional_receipts');
		})
	} else if (frm.doc.branch == "Garcia's Pawnshop - GTC") {
		frappe.db.get_list('Provisional Receipt', {
			fields: ['total'],
			filters: {
				date_issued: date_today,
				docstatus: 1,
				branch: "Garcia's Pawnshop - GTC"
			}
		}).then(records => {
			let temp_total = 0.00;
			frm.set_value('provisional_receipts', 0.00);
			for (let index = 0; index < records.length; index++) {
				temp_total += parseFloat(records[index].total)
			}
			frm.set_value('provisional_receipts', temp_total);
			frm.refresh_field('provisional_receipts');
		})
	} else if (frm.doc.branch == "Garcia's Pawnshop - MOL") {
		frappe.db.get_list('Provisional Receipt', {
			fields: ['total'],
			filters: {
				date_issued: date_today,
				docstatus: 1,
				branch: "Garcia's Pawnshop - MOL"
			}
		}).then(records => {
			let temp_total = 0.00;
			frm.set_value('provisional_receipts', 0.00);
			for (let index = 0; index < records.length; index++) {
				temp_total += parseFloat(records[index].total)
			}
			frm.set_value('provisional_receipts', temp_total);
			frm.refresh_field('provisional_receipts');
		})
	} else if (frm.doc.branch == "Garcia's Pawnshop - POB") {
		frappe.db.get_list('Provisional Receipt', {
			fields: ['total'],
			filters: {
				date_issued: date_today,
				docstatus: 1,
				branch: "Garcia's Pawnshop - POB"
			}
		}).then(records => {
			let temp_total = 0.00;
			frm.set_value('provisional_receipts', 0.00);
			for (let index = 0; index < records.length; index++) {
				temp_total += parseFloat(records[index].total)
			}
			frm.set_value('provisional_receipts', temp_total);
			frm.refresh_field('provisional_receipts');
		})
	} else if (frm.doc.branch == "Garcia's Pawnshop - TNZ") {
		frappe.db.get_list('Provisional Receipt', {
			fields: ['total'],
			filters: {
				date_issued: date_today,
				docstatus: 1,
				branch: "Garcia's Pawnshop - TNZ"
			}
		}).then(records => {
			let temp_total = 0.00;
			frm.set_value('provisional_receipts', 0.00);
			for (let index = 0; index < records.length; index++) {
				temp_total += parseFloat(records[index].total)
			}
			frm.set_value('provisional_receipts', temp_total);
			frm.refresh_field('provisional_receipts');
		})
	}
}

function get_jewelry_a_of_the_day(frm, date_today=null) {
	frappe.db.get_list('Pawn Ticket Jewelry', {
		fields: ['net_proceeds'],
		filters: {
			date_loan_granted: date_today,
			item_series: 'A',
			branch: frm.doc.branch,
			old_pawn_ticket: '',
			docstatus: 1
		}
	}).then(records => {
		let temp_total = 0.00;
		frm.set_value('jewelry_a', 0.00);
		for (let index = 0; index < records.length; index++) {
			temp_total += parseFloat(records[index].net_proceeds)
		}
		frm.set_value('jewelry_a', temp_total);
		frm.refresh_field('jewelry_a');
	})
}

function get_jewelry_b_of_the_day(frm, date_today=null) {
	frappe.db.get_list('Pawn Ticket Jewelry', {
		fields: ['net_proceeds'],
		filters: {
			date_loan_granted: date_today,
			item_series: 'B',
			branch: frm.doc.branch,
			old_pawn_ticket: '',
			docstatus: 1
		}
	}).then(records => {
		let temp_total = 0.00;
		frm.set_value('jewelry_b', 0.00);
		for (let index = 0; index < records.length; index++) {
			temp_total += parseFloat(records[index].net_proceeds)
		}
		frm.set_value('jewelry_b', temp_total);
	})
}

function get_non_jewelry_of_the_day(frm, date_today=null) {
	if (frm.doc.branch == "Rabie's House") {
		frappe.db.get_list('Pawn Ticket Non Jewelry', {
			fields: ['net_proceeds'],
			filters: {
				date_loan_granted: date_today,
				branch: "Rabie's House",
				old_pawn_ticket: ''
			}
		}).then(records => {
			let temp_total = 0.00;
			frm.set_value('non_jewelry', 0.00);
			for (let index = 0; index < records.length; index++) {
				temp_total += parseFloat(records[index].net_proceeds)
			}
			frm.set_value('non_jewelry', temp_total);
			frm.refresh_field('non_jewelry');
		})
	} else if (frm.doc.branch == "Garcia's Pawnshop - CC") {
		frappe.db.get_list('Pawn Ticket Non Jewelry', {
			fields: ['net_proceeds'],
			filters: {
				date_loan_granted: date_today,
				branch: "Garcia's Pawnshop - CC"
			}
		}).then(records => {
			let temp_total = 0.00;
			frm.set_value('non_jewelry', 0.00);
			for (let index = 0; index < records.length; index++) {
				temp_total += parseFloat(records[index].net_proceeds)
			}
			frm.set_value('non_jewelry', temp_total);
			frm.refresh_field('non_jewelry');
		})
	} else if (frm.doc.branch == "Garcia's Pawnshop - GTC") {
		frappe.db.get_list('Pawn Ticket Non Jewelry', {
			fields: ['net_proceeds'],
			filters: {
				date_loan_granted: date_today,
				branch: "Garcia's Pawnshop - GTC"
			}
		}).then(records => {
			let temp_total = 0.00;
			frm.set_value('non_jewelry', 0.00);
			for (let index = 0; index < records.length; index++) {
				temp_total += parseFloat(records[index].net_proceeds)
			}
			frm.set_value('non_jewelry', temp_total);
			frm.refresh_field('non_jewelry');
		})
	} else if (frm.doc.branch == "Garcia's Pawnshop - MOL") {
		frappe.db.get_list('Pawn Ticket Non Jewelry', {
			fields: ['net_proceeds'],
			filters: {
				date_loan_granted: date_today,
				branch: "Garcia's Pawnshop - MOL"
			}
		}).then(records => {
			let temp_total = 0.00;
			frm.set_value('non_jewelry', 0.00);
			for (let index = 0; index < records.length; index++) {
				temp_total += parseFloat(records[index].net_proceeds)
			}
			frm.set_value('non_jewelry', temp_total);
			frm.refresh_field('non_jewelry');
		})
	} else if (frm.doc.branch == "Garcia's Pawnshop - POB") {
		frappe.db.get_list('Pawn Ticket Non Jewelry', {
			fields: ['net_proceeds'],
			filters: {
				date_loan_granted: date_today,
				branch: "Garcia's Pawnshop - POB"
			}
		}).then(records => {
			let temp_total = 0.00;
			frm.set_value('non_jewelry', 0.00);
			for (let index = 0; index < records.length; index++) {
				temp_total += parseFloat(records[index].net_proceeds)
			}
			frm.set_value('non_jewelry', temp_total);
			frm.refresh_field('non_jewelry');
		})
	} else if (frm.doc.branch == "Garcia's Pawnshop - TNZ") {
		frappe.db.get_list('Pawn Ticket Non Jewelry', {
			fields: ['net_proceeds'],
			filters: {
				date_loan_granted: date_today,
				branch: "Garcia's Pawnshop - TNZ"
			}
		}).then(records => {
			let temp_total = 0.00;
			frm.set_value('non_jewelry', 0.00);
			for (let index = 0; index < records.length; index++) {
				temp_total += parseFloat(records[index].net_proceeds)
			}
			frm.set_value('non_jewelry', temp_total);
			frm.refresh_field('non_jewelry');
		})
	}
}

function total_cash_breakdown(frm) {
	let total_cash_breakdown = 0.00
	let thousand_bill = parseFloat(frm.doc.one_thousand_php_bills);
	let five_hundred_bill = parseFloat(frm.doc.five_hundred_php_bills);
	let two_hundred_bill = parseFloat(frm.doc.two_hundred_php_bills);
	let one_hundred_bill = parseFloat(frm.doc.one_hundred_php_bills);
	let fifty_bill = parseFloat(frm.doc.fifty_php_bills);
	let twenty_bill = parseFloat(frm.doc.twenty_php_bills);
	let ten_peso_coin = parseFloat(frm.doc.ten_php_coin);
	let five_peso_coin = parseFloat(frm.doc.five_php_coin);
	let one_peso_coin = parseFloat(frm.doc.peso_php_coin);
	let twenty_five_cents = parseFloat(frm.doc.twenty_five_cent_php_coin);
	total_cash_breakdown = thousand_bill + five_hundred_bill + two_hundred_bill + one_hundred_bill + fifty_bill + twenty_bill + ten_peso_coin + five_peso_coin + one_peso_coin + twenty_five_cents;

	let ending_balance = parseFloat(frm.doc.ending_balance);
	let shortage_overage = 0.00;
	if (total_cash_breakdown != ending_balance) {
		if (total_cash_breakdown > ending_balance) {
			shortage_overage = total_cash_breakdown - ending_balance;
			frm.set_value('shortage_overage', shortage_overage);
			frm.refresh_field('shortage_overage');
			total_cash_breakdown = total_cash_breakdown + shortage_overage
		} else if (total_cash_breakdown < ending_balance) {
			shortage_overage = total_cash_breakdown - ending_balance;
			frm.set_value('shortage_overage', shortage_overage);
			frm.refresh_field('shortage_overage');
			total_cash_breakdown = total_cash_breakdown + shortage_overage
		} 
	} else {
		frm.set_value('shortage_overage', 0.00);
		frm.refresh_field('shortage_overage');
	}

	

	frm.set_value('total_cash', total_cash_breakdown);
	frm.refresh_field('total_cash');
}


function select_naming_series(frm) { //Select naming series with regards to the branch
	if (frm.doc.branch == "Rabie's House") {
		frm.set_value('naming_series', "No.20-.######")
	} else if (frm.doc.branch == "Garcia's Pawnshop - CC") {
		frm.set_value('naming_series', "No.1-.######")
	} else if (frm.doc.branch == "Garcia's Pawnshop - GTC") {
		frm.set_value('naming_series', "No.4-.######")
	} else if (frm.doc.branch == "Garcia's Pawnshop - MOL") {
		frm.set_value('naming_series', "No.6-.######")
	} else if (frm.doc.branch == "Garcia's Pawnshop - POB") {
		frm.set_value('naming_series', "No.3-.######")
	} else if (frm.doc.branch == "Garcia's Pawnshop - TNZ") {
		frm.set_value('naming_series', "No.5-.######")
	}
}


function get_gcash_provisional_receipt(frm, date_today = null) {
	if (frm.doc.branch == "Rabie's House") {
		frappe.db.get_list('Provisional Receipt', {
			fields: ['total'],
			filters: {
				date_issued: date_today,
				docstatus: 1,
				branch: "Rabie's House",
				mode_of_payment: "GCash"
			}
		}).then(records => {
			let temp_total = 0.00;
			frm.set_value('gcash', 0.00);
			for (let index = 0; index < records.length; index++) {
				temp_total += parseFloat(records[index].total)
			}
			frm.set_value('gcash', temp_total);
			frm.refresh_field('gcash');
		})
	} else if (frm.doc.branch == "Garcia's Pawnshop - TNZ") {
		frappe.db.get_list('Provisional Receipt', {
			fields: ['total'],
			filters: {
				date_issued: date_today,
				docstatus: 1,
				branch: "Garcia's Pawnshop - TNZ",
				mode_of_payment: "GCash"
			}
		}).then(records => {
			let temp_total = 0.00;
			frm.set_value('gcash', 0.00);
			for (let index = 0; index < records.length; index++) {
				temp_total += parseFloat(records[index].total)
			}
			frm.set_value('gcash', temp_total);
			frm.refresh_field('gcash');
		})
	} else if (frm.doc.branch == "Garcia's Pawnshop - POB") {
		frappe.db.get_list('Provisional Receipt', {
			fields: ['total'],
			filters: {
				date_issued: date_today,
				docstatus: 1,
				branch: "Garcia's Pawnshop - POB",
				mode_of_payment: "GCash"
			}
		}).then(records => {
			let temp_total = 0.00;
			frm.set_value('gcash', 0.00);
			for (let index = 0; index < records.length; index++) {
				temp_total += parseFloat(records[index].total)
			}
			frm.set_value('gcash', temp_total);
			frm.refresh_field('gcash');
		})
	} else if (frm.doc.branch == "Garcia's Pawnshop - MOL") {
		frappe.db.get_list('Provisional Receipt', {
			fields: ['total'],
			filters: {
				date_issued: date_today,
				docstatus: 1,
				branch: "Garcia's Pawnshop - MOL",
				mode_of_payment: "GCash"
			}
		}).then(records => {
			let temp_total = 0.00;
			frm.set_value('gcash', 0.00);
			for (let index = 0; index < records.length; index++) {
				temp_total += parseFloat(records[index].total)
			}
			frm.set_value('gcash', temp_total);
			frm.refresh_field('gcash');
		})
	} else if (frm.doc.branch == "Garcia's Pawnshop - GTC") {
		frappe.db.get_list('Provisional Receipt', {
			fields: ['total'],
			filters: {
				date_issued: date_today,
				docstatus: 1,
				branch: "Garcia's Pawnshop - GTC",
				mode_of_payment: "GCash"
			}
		}).then(records => {
			let temp_total = 0.00;
			frm.set_value('gcash', 0.00);
			for (let index = 0; index < records.length; index++) {
				temp_total += parseFloat(records[index].total)
			}
			frm.set_value('gcash', temp_total);
			frm.refresh_field('gcash');
		})
	} else if (frm.doc.branch == "Garcia's Pawnshop - CC") {
		frappe.db.get_list('Provisional Receipt', {
			fields: ['total'],
			filters: {
				date_issued: date_today,
				docstatus: 1,
				branch: "Garcia's Pawnshop - CC",
				mode_of_payment: "GCash"
			}
		}).then(records => {
			let temp_total = 0.00;
			frm.set_value('gcash', 0.00);
			for (let index = 0; index < records.length; index++) {
				temp_total += parseFloat(records[index].total)
			}
			frm.set_value('gcash', temp_total);
			frm.refresh_field('gcash');
		})
	}
}

function get_bank_transfer_provisional_receipt(frm, date_today = null) {
	if (frm.doc.branch == "Rabie's House") {
		frappe.db.get_list('Provisional Receipt', {
			fields: ['total'],
			filters: {
				date_issued: date_today,
				docstatus: 1,
				branch: "Rabie's House",
				mode_of_payment: "Bank Transfer"
			}
		}).then(records => {
			let temp_total = 0.00;
			frm.set_value('bank_transfer', 0.00);
			for (let index = 0; index < records.length; index++) {
				temp_total += parseFloat(records[index].total)
			}
			frm.set_value('gcash', temp_total);
			frm.refresh_field('bank_transfer');
		})
	} else if (frm.doc.branch == "Garcia's Pawnshop - TNZ") {
		frappe.db.get_list('Provisional Receipt', {
			fields: ['total'],
			filters: {
				date_issued: date_today,
				docstatus: 1,
				branch: "Garcia's Pawnshop - TNZ",
				mode_of_payment: "Bank Transfer"
			}
		}).then(records => {
			let temp_total = 0.00;
			frm.set_value('bank_transfer', 0.00);
			for (let index = 0; index < records.length; index++) {
				temp_total += parseFloat(records[index].total)
			}
			frm.set_value('bank_transfer', temp_total);
			frm.refresh_field('bank_transfer');
		})
	} else if (frm.doc.branch == "Garcia's Pawnshop - POB") {
		frappe.db.get_list('Provisional Receipt', {
			fields: ['total'],
			filters: {
				date_issued: date_today,
				docstatus: 1,
				branch: "Garcia's Pawnshop - POB",
				mode_of_payment: "Bank Transfer"
			}
		}).then(records => {
			let temp_total = 0.00;
			frm.set_value('bank_transfer', 0.00);
			for (let index = 0; index < records.length; index++) {
				temp_total += parseFloat(records[index].total)
			}
			frm.set_value('bank_transfer', temp_total);
			frm.refresh_field('bank_transfer');
		})
	} else if (frm.doc.branch == "Garcia's Pawnshop - MOL") {
		frappe.db.get_list('Provisional Receipt', {
			fields: ['total'],
			filters: {
				date_issued: date_today,
				docstatus: 1,
				branch: "Garcia's Pawnshop - MOL",
				mode_of_payment: "Bank Transfer"
			}
		}).then(records => {
			let temp_total = 0.00;
			frm.set_value('bank_transfer', 0.00);
			for (let index = 0; index < records.length; index++) {
				temp_total += parseFloat(records[index].total)
			}
			frm.set_value('bank_transfer', temp_total);
			frm.refresh_field('bank_transfer');
		})
	} else if (frm.doc.branch == "Garcia's Pawnshop - GTC") {
		frappe.db.get_list('Provisional Receipt', {
			fields: ['total'],
			filters: {
				date_issued: date_today,
				docstatus: 1,
				branch: "Garcia's Pawnshop - GTC",
				mode_of_payment: "Bank Transfer"
			}
		}).then(records => {
			let temp_total = 0.00;
			frm.set_value('bank_transfer', 0.00);
			for (let index = 0; index < records.length; index++) {
				temp_total += parseFloat(records[index].total)
			}
			frm.set_value('bank_transfer', temp_total);
			frm.refresh_field('bank_transfer');
		})
	} else if (frm.doc.branch == "Garcia's Pawnshop - CC") {
		frappe.db.get_list('Provisional Receipt', {
			fields: ['total'],
			filters: {
				date_issued: date_today,
				docstatus: 1,
				branch: "Garcia's Pawnshop - CC",
				mode_of_payment: "Bank Transfer"
			}
		}).then(records => {
			let temp_total = 0.00;
			frm.set_value('bank_transfer', 0.00);
			for (let index = 0; index < records.length; index++) {
				temp_total += parseFloat(records[index].total)
			}
			frm.set_value('bank_transfer', temp_total);
			frm.refresh_field('bank_transfer');
		})
	}
}

function get_additional_pawn_records(frm) {
	if (frm.doc.branch == "Rabie's House") {
		frappe.db.get_list('Pawn Ticket Jewelry', {
			fields: ['net_proceeds'],
			filters: {
				branch: "Rabie's House",
				docstatus: 1
			}
		}).then(records => {
			let temp_total = 0.00;
			frm.set_value('additional_pawn', 0.00);
			for (let index = 0; index < records.length; index++) {
				temp_total += parseFloat(records[index].net_proceeds);
			}
			get_additional_pawn_records_nj(frm, temp_total)
		})
	} else if (frm.doc.branch == "Garcia's Pawnshop - TNZ") {
		frappe.db.get_list('Pawn Ticket Jewelry', {
			fields: ['net_proceeds'],
			filters: {
				branch: "Garcia's Pawnshop - TNZ",
				docstatus: 1
			}
		}).then(records => {
			let temp_total = 0.00;
			frm.set_value('additional_pawn', 0.00);
			for (let index = 0; index < records.length; index++) {
				temp_total += parseFloat(records[index].net_proceeds);
			}
			get_additional_pawn_records_nj(frm, temp_total)
		})
	} else if (frm.doc.branch == "Garcia's Pawnshop - POB") {
		frappe.db.get_list('Pawn Ticket Jewelry', {
			fields: ['net_proceeds'],
			filters: {
				branch: "Garcia's Pawnshop - POB",
				docstatus: 1
			}
		}).then(records => {
			let temp_total = 0.00;
			frm.set_value('additional_pawn', 0.00);
			for (let index = 0; index < records.length; index++) {
				temp_total += parseFloat(records[index].net_proceeds);
			}
			get_additional_pawn_records_nj(frm, temp_total)
		})
	} else if (frm.doc.branch == "Garcia's Pawnshop - MOL") {
		frappe.db.get_list('Pawn Ticket Jewelry', {
			fields: ['net_proceeds'],
			filters: {
				branch: "Garcia's Pawnshop - MOL",
				docstatus: 1
			}
		}).then(records => {
			let temp_total = 0.00;
			frm.set_value('additional_pawn', 0.00);
			for (let index = 0; index < records.length; index++) {
				temp_total += parseFloat(records[index].net_proceeds);
			}
			get_additional_pawn_records_nj(frm, temp_total)
		})
	} else if (frm.doc.branch == "Garcia's Pawnshop - GTC") {
		frappe.db.get_list('Pawn Ticket Jewelry', {
			fields: ['net_proceeds'],
			filters: {
				branch: "Garcia's Pawnshop - GTC",
				docstatus: 1
			}
		}).then(records => {
			let temp_total = 0.00;
			frm.set_value('additional_pawn', 0.00);
			for (let index = 0; index < records.length; index++) {
				temp_total += parseFloat(records[index].net_proceeds);
			}
			get_additional_pawn_records_nj(frm, temp_total)
		})
	} else if (frm.doc.branch == "Garcia's Pawnshop - CC") {
		frappe.db.get_list('Pawn Ticket Jewelry', {
			fields: ['net_proceeds'],
			filters: {
				branch: "Garcia's Pawnshop - CC",
				docstatus: 1
			}
		}).then(records => {
			let temp_total = 0.00;
			frm.set_value('additional_pawn', 0.00);
			for (let index = 0; index < records.length; index++) {
				temp_total += parseFloat(records[index].net_proceeds);
			}
			get_additional_pawn_records_nj(frm, temp_total)
		})
	}
}

function get_additional_pawn_records_nj(frm, j_temp_total) {
	if (frm.doc.branch == "Rabie's House") {
		frappe.db.get_list('Pawn Ticket Non Jewelry', {
			fields: ['net_proceeds'],
			filters: {
				branch: "Rabie's House",
				docstatus: 1
			}
		}).then(records_nj => {
			let nj_temp_total = 0.00;
			let total = 0.00;
			for (let index = 0; index < records_nj.length; index++) {
				nj_temp_total += records_nj[index].net_proceeds;
			}
			total = j_temp_total + nj_temp_total;
			frm.set_value('additional_pawn', total);
			frm.refresh_field('additional_pawn');
		})
	} else if (frm.doc.branch == "Garcia's Pawnshop - TNZ") {
		frappe.db.get_list('Pawn Ticket Non Jewelry', {
			fields: ['net_proceeds'],
			filters: {
				branch: "Garcia's Pawnshop - TNZ",
				docstatus: 1
			}
		}).then(records_nj => {
			let nj_temp_total = 0.00;
			let total = 0.00;
			for (let index = 0; index < records_nj.length; index++) {
				nj_temp_total += records_nj[index].net_proceeds;
			}
			total = j_temp_total + nj_temp_total;
			frm.set_value('additional_pawn', total);
			frm.refresh_field('additional_pawn');
		})
	} else if (frm.doc.branch == "Garcia's Pawnshop - POB") {
		frappe.db.get_list('Pawn Ticket Non Jewelry', {
			fields: ['net_proceeds'],
			filters: {
				branch: "Garcia's Pawnshop - POB",
				docstatus: 1
			}
		}).then(records_nj => {
			let nj_temp_total = 0.00;
			let total = 0.00;
			for (let index = 0; index < records_nj.length; index++) {
				nj_temp_total += records_nj[index].net_proceeds;
			}
			total = j_temp_total + nj_temp_total;
			frm.set_value('additional_pawn', total);
			frm.refresh_field('additional_pawn');
		})
	} else if (frm.doc.branch == "Garcia's Pawnshop - MOL") {
		frappe.db.get_list('Pawn Ticket Non Jewelry', {
			fields: ['net_proceeds'],
			filters: {
				branch: "Garcia's Pawnshop - MOL",
				docstatus: 1
			}
		}).then(records_nj => {
			let nj_temp_total = 0.00;
			let total = 0.00;
			for (let index = 0; index < records_nj.length; index++) {
				nj_temp_total += records_nj[index].net_proceeds;
			}
			total = j_temp_total + nj_temp_total;
			frm.set_value('additional_pawn', total);
			frm.refresh_field('additional_pawn');
		})
	} else if (frm.doc.branch == "Garcia's Pawnshop - GTC") {
		frappe.db.get_list('Pawn Ticket Non Jewelry', {
			fields: ['net_proceeds'],
			filters: {
				branch: "Garcia's Pawnshop - GTC",
				docstatus: 1
			}
		}).then(records_nj => {
			let nj_temp_total = 0.00;
			let total = 0.00;
			for (let index = 0; index < records_nj.length; index++) {
				nj_temp_total += records_nj[index].net_proceeds;
			}
			total = j_temp_total + nj_temp_total;
			frm.set_value('additional_pawn', total);
			frm.refresh_field('additional_pawn');
		})
	} else if (frm.doc.branch == "Garcia's Pawnshop - CC") {
		frappe.db.get_list('Pawn Ticket Non Jewelry', {
			fields: ['net_proceeds'],
			filters: {
				branch: "Garcia's Pawnshop - CC",
				docstatus: 1
			}
		}).then(records_nj => {
			let nj_temp_total = 0.00;
			let total = 0.00;
			for (let index = 0; index < records_nj.length; index++) {
				nj_temp_total += records_nj[index].net_proceeds;
			}
			total = j_temp_total + nj_temp_total;
			frm.set_value('additional_pawn', total);
			frm.refresh_field('additional_pawn');
		})
	}
	
}


function get_additional_redeem(frm) {
	if (frm.doc.branch == "Rabie's House") {
		frappe.db.get_list('Provisional Receipt', {
			fields: ['total', 'additional_amortization', 'transaction_type'],
			filters: {
				transaction_type: [
					'in',
					[
						'Redemption',
						'Renewal',
						'Interest Payment',
						'Renewal w/ Amortization'
					]
				],
				branch: "Rabie's House",
				docstatus: 1
			}
		}).then(records_pr => {
			let temp_total = 0.00;
			frm.set_value('additional_redeem', 0.00);
			for (let index = 0; index < records_pr.length; index++) {
				if (records_pr[index].transaction_type != "Renewal w/ Amortization") {
					temp_total += parseFloat(records_pr[index].total)
				} else {
					temp_total += parseFloat(records_pr[index].total) - parseFloat(records_pr[index].additional_amortization)
				}
			}
			frm.set_value('additional_redeem', temp_total);
			frm.refresh_field('additional_redeem');
		})
	} else if (frm.doc.branch == "Garcia's Pawnshop - TNZ") {
		frappe.db.get_list('Provisional Receipt', {
			fields: ['total', 'additional_amortization', 'transaction_type'],
			filters: {
				transaction_type: [
					'in',
					[
						'Redemption',
						'Renewal',
						'Interest Payment',
						'Renewal w/ Amortization'
					]
				],
				branch: "Garcia's Pawnshop - TNZ",
				docstatus: 1
			}
		}).then(records_pr => {
			let temp_total = 0.00;
			frm.set_value('additional_redeem', 0.00);
			for (let index = 0; index < records_pr.length; index++) {
				if (records_pr[index].transaction_type != "Renewal w/ Amortization") {
					temp_total += parseFloat(records_pr[index].total)
				} else {
					temp_total += parseFloat(records_pr[index].total) - parseFloat(records_pr[index].additional_amortization)
				}
			}
			frm.set_value('additional_redeem', temp_total);
			frm.refresh_field('additional_redeem');
		})
	} else if ("Garcia's Pawnshop - POB") {
		frappe.db.get_list('Provisional Receipt', {
			fields: ['total', 'additional_amortization', 'transaction_type'],
			filters: {
				transaction_type: [
					'in',
					[
						'Redemption',
						'Renewal',
						'Interest Payment',
						'Renewal w/ Amortization'
					]
				],
				branch: "Garcia's Pawnshop - POB",
				docstatus: 1
			}
		}).then(records_pr => {
			let temp_total = 0.00;
			frm.set_value('additional_redeem', 0.00);
			for (let index = 0; index < records_pr.length; index++) {
				if (records_pr[index].transaction_type != "Renewal w/ Amortization") {
					temp_total += parseFloat(records_pr[index].total)
				} else {
					temp_total += parseFloat(records_pr[index].total) - parseFloat(records_pr[index].additional_amortization)
				}
			}
			frm.set_value('additional_redeem', temp_total);
			frm.refresh_field('additional_redeem');
		})
	} else if (frm.doc.branch == "Garcia's Pawnshop - MOL") {
		frappe.db.get_list('Provisional Receipt', {
			fields: ['total', 'additional_amortization', 'transaction_type'],
			filters: {
				transaction_type: [
					'in',
					[
						'Redemption',
						'Renewal',
						'Interest Payment',
						'Renewal w/ Amortization'
					]
				],
				branch: "Garcia's Pawnshop - MOL",
				docstatus: 1
			}
		}).then(records_pr => {
			let temp_total = 0.00;
			frm.set_value('additional_redeem', 0.00);
			for (let index = 0; index < records_pr.length; index++) {
				if (records_pr[index].transaction_type != "Renewal w/ Amortization") {
					temp_total += parseFloat(records_pr[index].total)
				} else {
					temp_total += parseFloat(records_pr[index].total) - parseFloat(records_pr[index].additional_amortization)
				}
			}
			frm.set_value('additional_redeem', temp_total);
			frm.refresh_field('additional_redeem');
		})
	} else if (frm.doc.branch == "Garcia's Pawnshop - GTC") {
		frappe.db.get_list('Provisional Receipt', {
			fields: ['total', 'additional_amortization', 'transaction_type'],
			filters: {
				transaction_type: [
					'in',
					[
						'Redemption',
						'Renewal',
						'Interest Payment',
						'Renewal w/ Amortization'
					]
				],
				branch: "Garcia's Pawnshop - GTC",
				docstatus: 1
			}
		}).then(records_pr => {
			let temp_total = 0.00;
			frm.set_value('additional_redeem', 0.00);
			for (let index = 0; index < records_pr.length; index++) {
				if (records_pr[index].transaction_type != "Renewal w/ Amortization") {
					temp_total += parseFloat(records_pr[index].total)
				} else {
					temp_total += parseFloat(records_pr[index].total) - parseFloat(records_pr[index].additional_amortization)
				}
			}
			frm.set_value('additional_redeem', temp_total);
			frm.refresh_field('additional_redeem');
		})
	} else if (frm.doc.branch == "Garcia's Pawnshop - CC") {
		frappe.db.get_list('Provisional Receipt', {
			fields: ['total', 'additional_amortization', 'transaction_type'],
			filters: {
				transaction_type: [
					'in',
					[
						'Redemption',
						'Renewal',
						'Interest Payment',
						'Renewal w/ Amortization'
					]
				],
				branch: "Garcia's Pawnshop - CC",
				docstatus: 1
			}
		}).then(records_pr => {
			let temp_total = 0.00;
			frm.set_value('additional_redeem', 0.00);
			for (let index = 0; index < records_pr.length; index++) {
				if (records_pr[index].transaction_type != "Renewal w/ Amortization") {
					temp_total += parseFloat(records_pr[index].total)
				} else {
					temp_total += parseFloat(records_pr[index].total) - parseFloat(records_pr[index].additional_amortization)
				}
			}
			frm.set_value('additional_redeem', temp_total);
			frm.refresh_field('additional_redeem');
		})
	}
}

function get_additional_partial_payment(frm) {
	if (frm.doc.branch == "Rabie's House") {
		frappe.db.get_list('Provisional Receipt', {
			fields: ['total'],
			filters:{
				branch: "Rabie's House",
				transaction_type: 'Interest Payment',
				docstatus: 1
			}
		}).then(records_pr => {
			console.log(records_pr);
			let temp_total = 0.00;
			frm.set_value('additional_partial_payment', 0.00);
			for (let index = 0; index < records_pr.length; index++) {
				temp_total += parseFloat(records_pr[index].total);
			}
			frm.set_value('additional_partial_payment', temp_total);
			frm.refresh_field('additional_partial_payment');
		})
	} else if (frm.doc.branch == "Garcia's Pawnshop - TNZ") {
		frappe.db.get_list('Provisional Receipt', {
			fields: ['total'],
			filters:{
				branch: "Garcia's Pawnshop - TNZ",
				transaction_type: 'Interest Payment',
				docstatus: 1
			}
		}).then(records_pr => {
			let temp_total = 0.00;
			frm.set_value('additional_partial_payment', 0.00);
			for (let index = 0; index < records_pr.length; index++) {
				temp_total += parseFloat(records_pr[index].total);
			}
			frm.set_value('additional_partial_payment', temp_total);
			frm.refresh_field('additional_partial_payment');
		})
	} else if (frm.doc.branch == "Garcia's Pawnshop - POB") {
		frappe.db.get_list('Provisional Receipt', {
			fields: ['total'],
			filters:{
				branch: "Garcia's Pawnshop - POB",
				transaction_type: 'Interest Payment',
				docstatus: 1
			}
		}).then(records_pr => {
			let temp_total = 0.00;
			frm.set_value('additional_partial_payment', 0.00);
			for (let index = 0; index < records_pr.length; index++) {
				temp_total += parseFloat(records_pr[index].total);
			}
			frm.set_value('additional_partial_payment', temp_total);
			frm.refresh_field('additional_partial_payment');
		})
	} else if ("Garcia's Pawnshop - MOL") {
		frappe.db.get_list('Provisional Receipt', {
			fields: ['total'],
			filters:{
				branch: "Garcia's Pawnshop - MOL",
				transaction_type: 'Interest Payment',
				docstatus: 1
			}
		}).then(records_pr => {
			let temp_total = 0.00;
			frm.set_value('additional_partial_payment', 0.00);
			for (let index = 0; index < records_pr.length; index++) {
				temp_total += parseFloat(records_pr[index].total);
			}
			frm.set_value('additional_partial_payment', temp_total);
			frm.refresh_field('additional_partial_payment');
		})
	} else if ("Garcia's Pawnshop - GTC") {
		frappe.db.get_list('Provisional Receipt', {
			fields: ['total'],
			filters:{
				branch: "Garcia's Pawnshop - GTC",
				transaction_type: 'Interest Payment',
				docstatus: 1
			}
		}).then(records_pr => {
			console.log(records_pr);
			let temp_total = 0.00;
			frm.set_value('additional_partial_payment', 0.00);
			for (let index = 0; index < records_pr.length; index++) {
				temp_total += parseFloat(records_pr[index].total);
			}
			frm.set_value('additional_partial_payment', temp_total);
			frm.refresh_field('additional_partial_payment');
		})
	} else if ("Garcia's Pawnshop - CC") {
		frappe.db.get_list('Provisional Receipt', {
			fields: ['total'],
			filters:{
				branch: "Garcia's Pawnshop - CC",
				transaction_type: 'Interest Payment'
			}
		}).then(records_pr => {
			let temp_total = 0.00;
			frm.set_value('additional_partial_payment', 0.00);
			for (let index = 0; index < records_pr.length; index++) {
				temp_total += parseFloat(records_pr[index].total);
			}
			frm.set_value('additional_partial_payment', temp_total);
			frm.refresh_field('additional_partial_payment');
		})
	}
	
}