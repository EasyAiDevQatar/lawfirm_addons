frappe.query_reports["Case Sessions Report"] = {
	filters: [
		{
			fieldname: "customer_name",
			label: __("اسم العميل"),
			fieldtype: "Data",
		},
		{
			fieldname: "case_number",
			label: __("رقم القضية"),
			fieldtype: "Data",
		},
		{
			fieldname: "from_date",
			label: __("من تاريخ (الجلسة القادمة)"),
			fieldtype: "Date",
		},
		{
			fieldname: "to_date",
			label: __("إلى تاريخ (الجلسة القادمة)"),
			fieldtype: "Date",
		},
	],
};
