// Copyright (c) 2025, Lawfirm Addons and contributors
// For license information, please see license.txt

frappe.listview_settings['Case'] = {
	refresh: function(listview) {
		// Add button to filter by next_date from Case Sessions
		listview.page.add_inner_button(__("Filter by Next Date"), function() {
			var dialog = new frappe.ui.Dialog({
				title: __("Filter Cases by Next Date"),
				fields: [
					{
						fieldtype: "Date",
						fieldname: "next_date",
						label: __("Next Date"),
						reqd: 1,
						default: frappe.datetime.get_today()
					}
				],
				primary_action_label: __("Apply Filter"),
				primary_action: function(values) {
					// Clear existing filters first
					listview.filter_area.clear(false).then(function() {
						// Add filter for next_date from Case Sessions child table
						listview.filter_area.add([
							["Case Sessions", "next_date", "=", values.next_date]
						]);
					});
					dialog.hide();
				}
			});
			dialog.show();
		});
	}
};

