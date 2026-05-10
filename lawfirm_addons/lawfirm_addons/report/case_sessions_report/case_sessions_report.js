frappe.query_reports["Case Sessions Report"] = {
	/** Used when Print/PDF runs without picking a Print Format (avoids default plain grid). */
	async get_pdf_format(query_report, custom_format) {
		if (custom_format) return custom_format;
		const format_name = "Case Sessions Report Print";
		const r = await frappe.db.get_value(
			"Print Format",
			{ name: format_name, disabled: 0 },
			["html", "css"]
		);
		if (r?.message?.html) {
			const css = r.message.css || "";
			return `<style>${css}</style>${r.message.html}`;
		}
		return null;
	},
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
