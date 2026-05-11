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
	onload: function (query_report) {
		if (query_report.__lfa_force_custom_print_template) return;
		query_report.__lfa_force_custom_print_template = true;

		const get_columns_for_custom_print = function (print_settings, custom_format) {
			if (print_settings?.columns?.length) {
				return this.get_visible_columns().filter((column) =>
					print_settings.columns.includes(column.fieldname)
				);
			}
			return custom_format ? this.columns : this.get_visible_columns();
		};

		query_report.print_report = async function (print_settings) {
			const filters_html = this.get_filters_html_for_print();
			const landscape = print_settings.orientation == "Landscape";
			const custom_format = await this.get_custom_format(print_settings);
			const columns = get_columns_for_custom_print.call(this, print_settings, custom_format);
			const template = custom_format || "print_grid";

			this.make_access_log("Print", "PDF");
			frappe.render_grid({
				template,
				title: __(this.report_name),
				subtitle: print_settings?.include_filters ? filters_html : null,
				print_settings: print_settings,
				landscape: landscape,
				filters: this.get_filter_values(),
				data: this.get_data_for_print(),
				columns,
				original_data: this.data,
				report: this,
				can_use_smaller_font: this.report_doc.is_standard === "Yes" && custom_format ? 0 : 1,
			});
		};

		query_report.pdf_report = async function (print_settings) {
			const base_url = frappe.urllib.get_base_url();
			const print_css = frappe.boot.print_css;
			const landscape = print_settings.orientation == "Landscape";
			const custom_format = await this.get_custom_format(print_settings);
			const columns = get_columns_for_custom_print.call(this, print_settings, custom_format);
			const data = this.get_data_for_print();
			const applied_filters = this.get_filter_values();
			const filters_html = this.get_filters_html_for_print();
			const template = custom_format || "print_grid";

			const content = frappe.render_template(template, {
				title: __(this.report_name),
				subtitle: print_settings?.include_filters ? filters_html : null,
				filters: applied_filters,
				data: data,
				original_data: this.data,
				columns: columns,
				report: this,
				print_settings: print_settings,
			});

			const html = frappe.render_template("print_template", {
				title: __(this.report_name),
				content: content,
				base_url: base_url,
				print_css: print_css,
				print_settings: print_settings,
				landscape: landscape,
				columns: columns,
				lang: frappe.boot.lang,
				layout_direction: frappe.utils.is_rtl() ? "rtl" : "ltr",
				can_use_smaller_font: this.report_doc.is_standard === "Yes" && custom_format ? 0 : 1,
			});

			let filter_values = [],
				name_len = 0;
			for (var key of Object.keys(applied_filters)) {
				name_len = name_len + applied_filters[key].toString().length;
				if (name_len > 200) break;
				filter_values.push(applied_filters[key]);
			}

			if (filter_values.length) {
				print_settings.report_name = `${__(this.report_name)}_${filter_values.join("_")}.pdf`;
			} else {
				print_settings.report_name = `${__(this.report_name)}.pdf`;
			}
			frappe.render_pdf(html, print_settings);
		};
	},
};
