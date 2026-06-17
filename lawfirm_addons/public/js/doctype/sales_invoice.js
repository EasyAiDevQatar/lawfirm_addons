frappe.ui.form.on("Sales Invoice", {
	refresh(frm) {
		lawfirm_addons.print.fetch_doctype_format(frm);
	},
	custom_invoice_type() {
		lawfirm_addons.print.fetch_doctype_format(frm);
	},
});
