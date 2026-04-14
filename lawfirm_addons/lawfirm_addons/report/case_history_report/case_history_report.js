frappe.query_reports["Case History Report"] = {
	filters: [
		{
			fieldname: "customer_name",
			label: __("Customer Name"),
			fieldtype: "Data",
		},
		{
			fieldname: "case_number",
			label: __("Case Number"),
			fieldtype: "Data",
		},
		{
			fieldname: "from_date",
			label: __("From Date (Session Date)"),
			fieldtype: "Date",
		},
		{
			fieldname: "to_date",
			label: __("To Date (Session Date)"),
			fieldtype: "Date",
		},
	],
};
