import frappe


def execute(filters=None):
	filters = filters or {}
	conditions = ["cs.parentfield = 'case_sessions'"]
	values = {}

	if filters.get("from_date"):
		conditions.append("cs.next_date >= %(from_date)s")
		values["from_date"] = filters["from_date"]

	if filters.get("to_date"):
		conditions.append("cs.next_date <= %(to_date)s")
		values["to_date"] = filters["to_date"]

	if filters.get("customer_name"):
		conditions.append("c.customer_name LIKE %(customer_name)s")
		values["customer_name"] = f"%{filters['customer_name']}%"

	if filters.get("case_number"):
		conditions.append("cs.case_number LIKE %(case_number)s")
		values["case_number"] = f"%{filters['case_number']}%"

	where_clause = f"WHERE {' AND '.join(conditions)}" if conditions else ""

	columns = [
		{"label": "رقم الملف", "fieldname": "file_number", "fieldtype": "Link", "options": "Case", "width": 130},
		{"label": "اسم العميل", "fieldname": "customer_name", "fieldtype": "Data", "width": 160},
		{"label": "صفته", "fieldname": "client_capacity", "fieldtype": "Data", "width": 110},
		{"label": "الخصم", "fieldname": "opponent", "fieldtype": "Data", "width": 120},
		{"label": "صفة الخصم", "fieldname": "opponent_capacity", "fieldtype": "Data", "width": 120},
		{"label": "تاريخ الجلسة", "fieldname": "session_date", "fieldtype": "Date", "width": 110},
		{"label": "المحكمة", "fieldname": "court", "fieldtype": "Data", "width": 120},
		{"label": "درجة التقاضي", "fieldname": "litigation_degree", "fieldtype": "Data", "width": 100},
		{"label": "رقم القضية", "fieldname": "case_number", "fieldtype": "Data", "width": 110},
		{"label": "الدائرة", "fieldname": "chamber", "fieldtype": "Data", "width": 75},
		{"label": "موضوع القضية", "fieldname": "case_subject", "fieldtype": "Data", "width": 130},
		{"label": "القرار السابق", "fieldname": "previous_decision", "fieldtype": "Small Text", "width": 140},
		{"label": "قرار الجلسة", "fieldname": "decision", "fieldtype": "Text", "width": 240},
		{"label": "تاريخ الجلسة القادمة", "fieldname": "next_date", "fieldtype": "Date", "width": 115},
	]

	data = frappe.db.sql(
		f"""
		SELECT
			cs.parent AS file_number,
			c.customer_name,
			cs.client_capacity,
			cs.opponent,
			cs.opponent_capacity,
			cs.business_on_date AS session_date,
			cs.court,
			cs.litigation_degree,
			cs.case_number,
			cs.chamber,
			cs.case_subject,
			cs.previous_decision,
			cs.decision,
			cs.next_date
		FROM `tabCase Sessions` cs
		INNER JOIN `tabCase` c ON c.name = cs.parent
		{where_clause}
		ORDER BY cs.next_date DESC, cs.modified DESC
		""",
		values,
		as_dict=True,
	)

	return columns, data
