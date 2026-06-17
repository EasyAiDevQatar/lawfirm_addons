frappe.provide("lawfirm_addons.print");

lawfirm_addons.print.open_pdf = function (url) {
	if (!url) return;
	window.open(url, "_blank", "noopener");
};

lawfirm_addons.print.set_default_format = function (frm, print_format) {
	if (!frm || !print_format || frm.is_new()) return;
	frm.print_format = print_format;
	if (frm.page && frm.page.print_icon) {
		frm.page.print_icon.attr("data-format", print_format);
	}
};

lawfirm_addons.print.fetch_doctype_format = function (frm) {
	if (!frm || frm.is_new() || !["Sales Invoice", "Payment Entry"].includes(frm.doctype)) {
		return;
	}

	frappe.call({
		method: "lawfirm_addons.lawfirm_addons.api.case_printables.get_doctype_print_format",
		args: {
			doctype: frm.doctype,
			name: frm.docname,
		},
		callback(r) {
			if (r.message && r.message.print_format) {
				lawfirm_addons.print.set_default_format(frm, r.message.print_format);
			}
		},
	});
};
