// Copyright (c) 2016, Rabie Moses Santillan and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["NJ End of the Day Repor"] = {
	"filters": [
		{
			fieldname: "branch",
			label: __("Branch"),
			fieldtype: "Select",
			options: [
				"Garcia's Pawnshop - CC", 
				"Garcia's Pawnshop - GTC", 
				"Garcia's Pawnshop - MOL",
				"Garcia's Pawnshop - POB",
				"Garcia's Pawnshop - TNZ",
				"Rabie's House"
			]
		},

		{
			fieldname: "date_loan_granted",
			label: __("Date Loan Granted"),
			fieldtype: "Date"
		}
	]
};
