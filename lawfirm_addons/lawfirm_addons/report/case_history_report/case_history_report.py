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
		{"label": "المسلسل", "fieldname": "serial_no", "fieldtype": "Data", "width": 90},
		{"label": "ملف القضية", "fieldname": "case_name", "fieldtype": "Link", "options": "Case", "width": 120},
		{"label": "اسم العميل (المادة)", "fieldname": "customer_name", "fieldtype": "Data", "width": 140},
		{"label": "العميل", "fieldname": "row_client", "fieldtype": "Data", "width": 120},
		{"label": "صفته", "fieldname": "client_capacity", "fieldtype": "Data", "width": 100},
		{"label": "الخصم", "fieldname": "opponent", "fieldtype": "Data", "width": 110},
		{"label": "صفة الخصم", "fieldname": "opponent_capacity", "fieldtype": "Data", "width": 100},
		{"label": "تاريخ أول جلسة", "fieldname": "session_date", "fieldtype": "Date", "width": 100},
		{"label": "مكان الجلسة", "fieldname": "case_location", "fieldtype": "Data", "width": 110},
		{"label": "مكان الحضور", "fieldname": "attendance_location", "fieldtype": "Data", "width": 110},
		{"label": "المحكمة", "fieldname": "court", "fieldtype": "Data", "width": 110},
		{"label": "درجة التقاضي", "fieldname": "litigation_degree", "fieldtype": "Data", "width": 90},
		{"label": "رقم القضية", "fieldname": "case_number", "fieldtype": "Data", "width": 100},
		{"label": "الدائرة", "fieldname": "chamber", "fieldtype": "Data", "width": 70},
		{"label": "موضوع القضية", "fieldname": "case_subject", "fieldtype": "Data", "width": 120},
		{"label": "القرار السابق", "fieldname": "previous_decision", "fieldtype": "Small Text", "width": 130},
		{"label": "قرار الجلسة", "fieldname": "decision", "fieldtype": "Text", "width": 240},
		{"label": "الطلبات", "fieldname": "defense_summary", "fieldtype": "Small Text", "width": 120},
		{"label": "رقم التوكيل", "fieldname": "tokeel_no", "fieldtype": "Data", "width": 90},
		{"label": "مرفق", "fieldname": "has_attach", "fieldtype": "Data", "width": 50},
		{"label": "صورة توكيل", "fieldname": "has_tokeel_img", "fieldtype": "Data", "width": 55},
		{"label": "الوكيل", "fieldname": "agent", "fieldtype": "Data", "width": 90},
	]

	data = frappe.db.sql(
		f"""
		SELECT
			ch.registration_no AS serial_no,
			ch.parent AS case_name,
			c.customer_name,
			ch.client AS row_client,
			ch.client_capacity,
			ch.opponent,
			ch.opponent_capacity,
			ch.business_on_date AS session_date,
			ch.case_location,
			ch.attendance_location,
			ch.court,
			ch.litigation_degree,
			ch.chamber,
			ch.case_number,
			ch.case_subject,
			ch.previous_decision,
			ch.decision,
			ch.defense_summary,
			ch.tokeel_no,
			CASE
				WHEN (ch.attachments IS NOT NULL AND ch.attachments != '')
					OR (ch.additional_attachments IS NOT NULL AND ch.additional_attachments != '')
				THEN '✓' ELSE '' END AS has_attach,
			CASE WHEN ch.tokeel_image IS NOT NULL AND ch.tokeel_image != '' THEN '✓' ELSE '' END AS has_tokeel_img,
			ch.agent
		FROM `tabCase History` ch
		INNER JOIN `tabCase` c ON c.name = ch.parent
		{where_clause}
		ORDER BY ch.business_on_date DESC, ch.modified DESC
		""",
		values,
		as_dict=True,
	)

	return columns, data
