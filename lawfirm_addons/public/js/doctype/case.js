frappe.ui.form.on('Case', {
	refresh: function(frm) {
		frm.add_custom_button(__('View Attachments'), function() {
			const url = `/document-reader?case=${encodeURIComponent(frm.doc.name)}`;
			window.open(url, '_blank');
		}, __('Actions'));
	}
});