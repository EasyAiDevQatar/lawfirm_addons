(function () {
	if (frappe.__lfa_report_print_patches) {
		return;
	}
	frappe.__lfa_report_print_patches = true;

	const LFA_CASE_REPORTS = [
		"Case History Report",
		"Case Sessions Report",
		"Blacklisted Customer Report",
	];

	function lfa_is_case_report(query_report) {
		return !!(query_report && LFA_CASE_REPORTS.includes(query_report.report_name));
	}

	function lfa_stash_pick_columns(print_settings) {
		if (
			!print_settings ||
			!cint(print_settings.pick_columns) ||
			!Array.isArray(print_settings.columns) ||
			!print_settings.columns.length
		) {
			return;
		}
		print_settings._lfa_picked_columns = print_settings.columns.slice();
		delete print_settings.columns;
	}

	function lfa_restore_pick_columns(print_settings) {
		if (!print_settings || !print_settings._lfa_picked_columns) {
			return;
		}
		print_settings.columns = print_settings._lfa_picked_columns;
		delete print_settings._lfa_picked_columns;
	}

	function lfa_columns_for_print(query_report, print_settings, custom_format, fallback) {
		if (print_settings && print_settings._lfa_picked_columns) {
			const picked = print_settings._lfa_picked_columns;
			return query_report
				.get_visible_columns()
				.filter((column) => picked.includes(column.fieldname));
		}

		if (lfa_is_case_report(query_report) && custom_format) {
			return query_report.get_visible_columns();
		}

		return fallback();
	}

	const _get_columns_for_print = frappe.views.QueryReport.prototype.get_columns_for_print;
	frappe.views.QueryReport.prototype.get_columns_for_print = function (print_settings, custom_format) {
		return lfa_columns_for_print(this, print_settings, custom_format, () =>
			_get_columns_for_print.call(this, print_settings, custom_format)
		);
	};

	async function lfa_with_pick_columns(query_report, print_settings, print_fn) {
		if (!lfa_is_case_report(query_report)) {
			return print_fn();
		}

		lfa_stash_pick_columns(print_settings);
		try {
			return await print_fn();
		} finally {
			lfa_restore_pick_columns(print_settings);
		}
	}

	const _print_report = frappe.views.QueryReport.prototype.print_report;
	frappe.views.QueryReport.prototype.print_report = async function (print_settings) {
		return lfa_with_pick_columns(this, print_settings, () =>
			_print_report.call(this, print_settings)
		);
	};

	const _pdf_report = frappe.views.QueryReport.prototype.pdf_report;
	frappe.views.QueryReport.prototype.pdf_report = async function (print_settings) {
		return lfa_with_pick_columns(this, print_settings, () =>
			_pdf_report.call(this, print_settings)
		);
	};
})();
