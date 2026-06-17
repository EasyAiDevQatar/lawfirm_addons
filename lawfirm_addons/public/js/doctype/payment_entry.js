frappe.ui.form.on("Payment Entry", {
	refresh(frm) {
		lawfirm_addons.print.fetch_doctype_format(frm);
	},
});
