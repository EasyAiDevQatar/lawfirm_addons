import frappe
from frappe import _


def validate(doc, method=None):
	"""التحقق من أن اسم العميل غير موجود في قائمة الأسماء المحظورة"""
	if not doc.customer_name:
		return
	
	# تحويل الاسم إلى حالة صغيرة للمقارنة (يدعم العربي والإنجليزي)
	customer_name_normalized = doc.customer_name.strip().lower()
	customer_name_parts = customer_name_normalized.split()
	
	# التحقق من أن الاسم ثنائي أو ثلاثي
	if len(customer_name_parts) < 2 or len(customer_name_parts) > 3:
		# إذا كان الاسم أقل من ثنائي أو أكثر من ثلاثي، لا نتحقق من القائمة المحظورة
		return
	
	# البحث في القائمة المحظورة باستخدام مقارنة غير حساسة لحالة الأحرف
	blacklisted_names = frappe.get_all(
		"Blacklisted Customer Name",
		fields=["name", "customer_name", "reason"],
		limit_page_length=0
	)
	
	for blacklisted in blacklisted_names:
		blacklisted_name = blacklisted.customer_name.strip()
		blacklisted_name_normalized = blacklisted_name.lower()
		blacklisted_parts = blacklisted_name_normalized.split()
		
		# التحقق من أن الاسم المحظور ثنائي أو ثلاثي أيضاً
		if len(blacklisted_parts) >= 2 and len(blacklisted_parts) <= 3:
			# مقارنة غير حساسة لحالة الأحرف (يدعم العربي والإنجليزي)
			if blacklisted_name_normalized == customer_name_normalized:
				reason = blacklisted.reason
				
				error_message = _(
					"اسم العميل '{0}' مسجل في قائمة الأسماء المحظورة ولا يمكن التعامل معه."
				).format(doc.customer_name)
				
				if reason:
					error_message += " " + _("السبب: {0}").format(reason)
				
				frappe.throw(error_message)