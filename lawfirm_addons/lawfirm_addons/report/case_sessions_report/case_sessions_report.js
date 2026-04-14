frappe.query_reports["Case Sessions Report"] = {
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
			label: __("From Date (Next Session)"),
			fieldtype: "Date",
		},
		{
			fieldname: "to_date",
			label: __("To Date (Next Session)"),
			fieldtype: "Date",
		},
	],
};
