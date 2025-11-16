import frappe
from frappe import _


def validate(doc, method=None):
	"""التحقق من أن اسم العميل غير موجود في قائمة الأسماء المحظورة"""
	if doc.customer_name:
		blacklisted = frappe.db.exists(
			"Blacklisted Customer Name",
			{"customer_name": doc.customer_name}
		)
		
		if blacklisted:
			reason = frappe.db.get_value(
				"Blacklisted Customer Name",
				blacklisted,
				"reason"
			)
			
			error_message = _(
				"اسم العميل '{0}' مسجل في قائمة الأسماء المحظورة ولا يمكن التعامل معه."
			).format(doc.customer_name)
			
			if reason:
				error_message += " " + _("السبب: {0}").format(reason)
			
			frappe.throw(error_message)