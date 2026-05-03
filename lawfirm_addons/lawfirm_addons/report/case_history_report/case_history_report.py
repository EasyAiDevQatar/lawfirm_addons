import frappe


def execute(filters=None):
	filters = filters or {}
	conditions = ["ch.parentfield = 'case_history'"]
	values = {}

	if filters.get("from_date"):
		conditions.append("ch.business_on_date >= %(from_date)s")
		values["from_date"] = filters["from_date"]

	if filters.get("to_date"):
		conditions.append("ch.business_on_date <= %(to_date)s")
		values["to_date"] = filters["to_date"]

	if filters.get("customer_name"):
		conditions.append("c.customer_name LIKE %(customer_name)s")
		values["customer_name"] = f"%{filters['customer_name']}%"

	if filters.get("case_number"):
		conditions.append("ch.case_number LIKE %(case_number)s")
		values["case_number"] = f"%{filters['case_number']}%"

	where_clause = f"WHERE {' AND '.join(conditions)}" if conditions else ""

	columns = [
		{"label": "رقم الملف", "fieldname": "case_name", "fieldtype": "Link", "options": "Case", "width": 130},
		{"label": "اسم العميل", "fieldname": "customer_name", "fieldtype": "Data", "width": 150},
		{"label": "صفته", "fieldname": "client_capacity", "fieldtype": "Data", "width": 120},
		{"label": "الخصم", "fieldname": "opponent", "fieldtype": "Data", "width": 125},
		{"label": "صفة الخصم", "fieldname": "opponent_capacity", "fieldtype": "Data", "width": 120},
		{"label": "تاريخ الجلسة", "fieldname": "session_date", "fieldtype": "Date", "width": 110},
		{"label": "المحكمة", "fieldname": "court", "fieldtype": "Data", "width": 120},
		{"label": "درجة التقاضي", "fieldname": "litigation_degree", "fieldtype": "Data", "width": 130},
		{"label": "رقم القضية", "fieldname": "case_number", "fieldtype": "Data", "width": 120},
		{"label": "الدائرة", "fieldname": "chamber", "fieldtype": "Data", "width": 80},
		{"label": "موضوع القضية", "fieldname": "case_subject", "fieldtype": "Data", "width": 140},
		{"label": "القرار السابق", "fieldname": "previous_decision", "fieldtype": "Small Text", "width": 150},
		{"label": "قرار الجلسة", "fieldname": "decision", "fieldtype": "Text", "width": 260},
		{"label": "ملخص الوقائع", "fieldname": "facts_summary", "fieldtype": "Small Text", "width": 150},
		{"label": "ملخص الدفاع", "fieldname": "defense_summary", "fieldtype": "Small Text", "width": 150},
		{"label": "ملاحظات المرفقات", "fieldname": "attachments_note", "fieldtype": "Small Text", "width": 150},
	]

	data = frappe.db.sql(
		f"""
		SELECT
			ch.parent AS case_name,
			c.customer_name,
			ch.client_capacity,
			ch.opponent,
			ch.opponent_capacity,
			ch.business_on_date AS session_date,
			ch.court,
			ch.litigation_degree,
			ch.chamber,
			ch.case_number,
			ch.case_subject,
			ch.previous_decision,
			ch.decision,
			ch.facts_summary,
			ch.defense_summary,
			ch.attachments_note
		FROM `tabCase History` ch
		INNER JOIN `tabCase` c ON c.name = ch.parent
		{where_clause}
		ORDER BY ch.business_on_date DESC, ch.modified DESC
		""",
		values,
		as_dict=True,
	)

	return columns, data
