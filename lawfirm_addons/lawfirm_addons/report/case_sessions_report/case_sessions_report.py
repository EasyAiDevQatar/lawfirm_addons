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
		{"label": "File Number", "fieldname": "file_number", "fieldtype": "Link", "options": "Case", "width": 130},
		{"label": "Customer Name", "fieldname": "customer_name", "fieldtype": "Data", "width": 160},
		{"label": "Client Capacity", "fieldname": "client_capacity", "fieldtype": "Data", "width": 110},
		{"label": "Opponent", "fieldname": "opponent", "fieldtype": "Data", "width": 120},
		{"label": "Opponent Capacity", "fieldname": "opponent_capacity", "fieldtype": "Data", "width": 120},
		{"label": "Session Date", "fieldname": "session_date", "fieldtype": "Date", "width": 110},
		{"label": "Court", "fieldname": "court", "fieldtype": "Data", "width": 120},
		{"label": "Litigation Degree", "fieldname": "litigation_degree", "fieldtype": "Data", "width": 100},
		{"label": "Case Number", "fieldname": "case_number", "fieldtype": "Data", "width": 110},
		{"label": "Chamber", "fieldname": "chamber", "fieldtype": "Data", "width": 75},
		{"label": "Case Subject", "fieldname": "case_subject", "fieldtype": "Data", "width": 130},
		{"label": "Previous Decision", "fieldname": "previous_decision", "fieldtype": "Small Text", "width": 140},
		{"label": "Session Decision", "fieldname": "decision", "fieldtype": "Text", "width": 240},
		{"label": "Next Session Date", "fieldname": "next_date", "fieldtype": "Date", "width": 115},
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
