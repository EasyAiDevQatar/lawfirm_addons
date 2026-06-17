frappe.query_reports["Blacklisted Customer Report"] = {
	filters: [
		{
			fieldname: "customer_name",
			label: __("اسم العميل المحظور"),
			fieldtype: "Data",
		},
		{
			fieldname: "reason",
			label: __("السبب"),
			fieldtype: "Data",
		},
		{
			fieldname: "from_date",
			label: __("من تاريخ (تاريخ الإنشاء)"),
			fieldtype: "Date",
		},
		{
			fieldname: "to_date",
			label: __("إلى تاريخ (تاريخ الإنشاء)"),
			fieldtype: "Date",
		},
	],
};
