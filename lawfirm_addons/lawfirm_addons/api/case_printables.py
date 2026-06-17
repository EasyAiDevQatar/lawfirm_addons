import json
from urllib.parse import quote

import frappe
from frappe import _
from frappe.utils.pdf import get_pdf


SI_PRINT_FORMATS = {
	"fees": "Sales Invoice - فاتورة رسوم دعوى",
	"professional": "Sales Invoice - فاتورة اتعاب",
}

PE_PRINT_FORMATS = {
	"fees": "Payment Entry - استلام مبلغ عن فاتورة رسوم دعوى",
	"professional": "Payment Entry - استلام مبلغ عن فاتورة اتعاب",
}

CASE_REPORTS = [
	{
		"report_name": "Case Sessions Report",
		"label": "تقرير جدول الجلسات",
		"print_format": "Case Sessions Report Print",
	},
	{
		"report_name": "Case History Report",
		"label": "تقرير السجل التاريخي",
		"print_format": "Case History Report Print",
	},
	{
		"report_name": "Blacklisted Customer Report",
		"label": "تقرير العملاء المحظورين",
		"print_format": "Blacklisted Customer Report Print",
	},
]


def _invoice_print_category(invoice_type: str | None) -> str:
	name = (invoice_type or "").strip()
	if not name:
		return "fees"
	if "اتعاب" in name or "أتعاب" in name:
		return "professional"
	return "fees"


def resolve_sales_invoice_print_format(doc) -> str:
	category = _invoice_print_category(doc.get("custom_invoice_type"))
	return SI_PRINT_FORMATS[category]


def resolve_payment_entry_print_format(doc) -> str:
	title = (doc.get("title") or "").strip()
	if "اتعاب" in title or "أتعاب" in title:
		return PE_PRINT_FORMATS["professional"]

	for row in doc.get("references") or []:
		if row.reference_doctype != "Sales Invoice" or not row.reference_name:
			continue
		invoice_type = frappe.db.get_value(
			"Sales Invoice", row.reference_name, "custom_invoice_type"
		)
		if _invoice_print_category(invoice_type) == "professional":
			return PE_PRINT_FORMATS["professional"]

	return PE_PRINT_FORMATS["fees"]


def _print_pdf_url(doctype: str, name: str, print_format: str) -> str:
	return frappe.utils.get_url(
		"/api/method/frappe.utils.print_format.download_pdf"
		f"?doctype={quote(doctype)}"
		f"&name={quote(name)}"
		f"&format={quote(print_format)}"
	)


def _case_report_filters(case) -> dict:
	filters = {}
	if case.get("customer_name"):
		filters["customer_name"] = case.customer_name
	if case.get("case_no"):
		filters["case_number"] = case.case_no
	return filters


def _blacklisted_report_filters(case) -> dict:
	filters = {}
	if case.get("customer_name"):
		filters["customer_name"] = case.customer_name
	return filters


def _user_can_access_case(case_name: str) -> bool:
	if frappe.has_permission("Case", "read", case_name):
		return True

	if frappe.session.user == "Guest":
		return False

	return bool(
		frappe.db.exists(
			"ToDo",
			{
				"allocated_to": frappe.session.user,
				"reference_type": "Case",
				"reference_name": case_name,
				"status": ("!=", "Cancelled"),
			},
		)
	)


@frappe.whitelist()
def get_case_printable_documents(case_name: str):
	if not case_name or not frappe.db.exists("Case", case_name):
		frappe.throw(_("Case not found"))

	if not _user_can_access_case(case_name):
		frappe.throw(_("Not permitted"), frappe.PermissionError)

	case = frappe.get_doc("Case", case_name)
	documents = []

	if case.matter:
		for inv in frappe.get_all(
			"Sales Invoice",
			filters={"matter": case.matter, "docstatus": ("!=", 2)},
			fields=["name", "custom_invoice_type", "posting_date", "grand_total", "docstatus"],
			order_by="posting_date desc",
		):
			print_format = resolve_sales_invoice_print_format(inv)
			documents.append(
				{
					"kind": "doctype",
					"doctype": "Sales Invoice",
					"name": inv.name,
					"label": inv.name,
					"subtitle": inv.custom_invoice_type or _("Sales Invoice"),
					"print_format": print_format,
					"print_url": _print_pdf_url("Sales Invoice", inv.name, print_format),
				}
			)

	pe_filters = {"docstatus": ("!=", 2)}
	if case.customer:
		pe_filters["party_type"] = "Customer"
		pe_filters["party"] = case.customer
	elif case.matter:
		pe_filters["custom_matter"] = case.matter
	else:
		pe_filters = None

	if pe_filters:
		for pe in frappe.get_all(
			"Payment Entry",
			filters=pe_filters,
			fields=["name", "title", "posting_date", "paid_amount", "docstatus"],
			order_by="posting_date desc",
			limit=50,
		):
			pe_doc = frappe.get_doc("Payment Entry", pe.name)
			print_format = resolve_payment_entry_print_format(pe_doc)
			documents.append(
				{
					"kind": "doctype",
					"doctype": "Payment Entry",
					"name": pe.name,
					"label": pe.name,
					"subtitle": pe.title or _("Payment Entry"),
					"print_format": print_format,
					"print_url": _print_pdf_url("Payment Entry", pe.name, print_format),
				}
			)

	report_filters = _case_report_filters(case)
	for report in CASE_REPORTS[:2]:
		documents.append(
			{
				"kind": "report",
				"report_name": report["report_name"],
				"label": report["label"],
				"subtitle": report["report_name"],
				"print_format": report["print_format"],
				"filters": report_filters,
				"print_url": _report_pdf_url(report["report_name"], report_filters),
			}
		)

	blacklisted_filters = _blacklisted_report_filters(case)
	documents.append(
		{
			"kind": "report",
			"report_name": "Blacklisted Customer Report",
			"label": CASE_REPORTS[2]["label"],
			"subtitle": "Blacklisted Customer Report",
			"print_format": CASE_REPORTS[2]["print_format"],
			"filters": blacklisted_filters,
			"print_url": _report_pdf_url("Blacklisted Customer Report", blacklisted_filters),
		}
	)

	return {"documents": documents}


def _report_pdf_url(report_name: str, filters: dict | None) -> str:
	return frappe.utils.get_url(
		"/api/method/lawfirm_addons.lawfirm_addons.api.case_printables.download_report_pdf"
		f"?report_name={quote(report_name)}"
		f"&filters={quote(json.dumps(filters or {}))}"
	)


@frappe.whitelist()
def download_report_pdf(report_name: str, filters: str | None = None):
	filters_dict = json.loads(filters) if filters else {}
	if report_name not in {r["report_name"] for r in CASE_REPORTS}:
		frappe.throw(_("Report not allowed"))

	if not frappe.has_permission("Report", "read", report_name):
		frappe.throw(_("Not permitted"), frappe.PermissionError)

	from frappe.desk.query_report import run

	columns, data = run(report_name, filters_dict)
	html = frappe.render_template(
		"lawfirm_addons/templates/lfa_report_print.html",
		{
			"title": report_name,
			"report_name": report_name,
			"columns": columns,
			"data": data,
			"filters": filters_dict,
		},
	)

	frappe.local.response.filename = f"{report_name}.pdf"
	frappe.local.response.filecontent = get_pdf(html)
	frappe.local.response.type = "download"


@frappe.whitelist()
def get_doctype_print_format(doctype: str, name: str):
	if doctype not in ("Sales Invoice", "Payment Entry"):
		frappe.throw(_("Not supported"))

	if not frappe.has_permission(doctype, "read", name):
		frappe.throw(_("Not permitted"), frappe.PermissionError)

	doc = frappe.get_doc(doctype, name)
	if doctype == "Sales Invoice":
		print_format = resolve_sales_invoice_print_format(doc)
	else:
		print_format = resolve_payment_entry_print_format(doc)

	return {
		"print_format": print_format,
		"print_url": _print_pdf_url(doctype, name, print_format),
	}
