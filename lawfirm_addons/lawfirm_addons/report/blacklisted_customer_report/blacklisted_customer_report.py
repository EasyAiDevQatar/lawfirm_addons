import frappe


def execute(filters=None):
	filters = filters or {}
	conditions = []
	values = {}

	if filters.get("customer_name"):
		conditions.append("bcn.customer_name LIKE %(customer_name)s")
		values["customer_name"] = f"%{filters['customer_name']}%"

	if filters.get("reason"):
		conditions.append("bcn.reason LIKE %(reason)s")
		values["reason"] = f"%{filters['reason']}%"

	if filters.get("from_date"):
		conditions.append("DATE(bcn.creation) >= %(from_date)s")
		values["from_date"] = filters["from_date"]

	if filters.get("to_date"):
		conditions.append("DATE(bcn.creation) <= %(to_date)s")
		values["to_date"] = filters["to_date"]

	where_clause = f"WHERE {' AND '.join(conditions)}" if conditions else ""

	columns = [
		{"label": "اسم العميل المحظور", "fieldname": "customer_name", "fieldtype": "Data", "width": 200},
		{"label": "السبب", "fieldname": "reason", "fieldtype": "Small Text", "width": 280},
		{"label": "تاريخ الإنشاء", "fieldname": "creation", "fieldtype": "Datetime", "width": 150},
		{"label": "آخر تعديل", "fieldname": "modified", "fieldtype": "Datetime", "width": 150},
		{"label": "عُدّل بواسطة", "fieldname": "modified_by", "fieldtype": "Link", "options": "User", "width": 140},
	]

	data = frappe.db.sql(
		f"""
		SELECT
			bcn.customer_name,
			bcn.reason,
			bcn.creation,
			bcn.modified,
			bcn.modified_by
		FROM `tabBlacklisted Customer Name` bcn
		{where_clause}
		ORDER BY bcn.customer_name ASC
		""",
		values,
		as_dict=True,
	)

	return columns, data
