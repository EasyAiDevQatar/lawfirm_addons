import frappe
from frappe import _


def validate(doc, method=None):
	"""التحقق من أن اسم العميل غير موجود في قائمة الأسماء المحظورة"""
	if not doc.customer_name:
		return
	
	# تقسيم الاسم إلى أجزاء
	name_parts = doc.customer_name.strip().split()
	
	# التحقق من أن الاسم ثلاثي فقط (أول، وسط، آخر)
	if len(name_parts) != 3:
		# إذا كان الاسم ثنائي أو أقل/أكثر، لا نتحقق من القائمة المحظورة
		return
	
	# تحويل الاسم الثلاثي إلى حالة صغيرة للمقارنة
	customer_name_lower = doc.customer_name.strip().lower()
	
	# البحث في القائمة المحظورة باستخدام مقارنة غير حساسة لحالة الأحرف
	blacklisted_names = frappe.get_all(
		"Blacklisted Customer Name",
		fields=["name", "customer_name", "reason"],
		limit_page_length=0
	)
	
	for blacklisted in blacklisted_names:
		blacklisted_name = blacklisted.customer_name.strip()
		blacklisted_parts = blacklisted_name.split()
		
		# التحقق من أن الاسم المحظور ثلاثي أيضاً
		if len(blacklisted_parts) == 3:
			# مقارنة غير حساسة لحالة الأحرف
			if blacklisted_name.lower() == customer_name_lower:
				reason = blacklisted.reason
				
				error_message = _(
					"اسم العميل '{0}' مسجل في قائمة الأسماء المحظورة ولا يمكن التعامل معه."
				).format(doc.customer_name)
				
				if reason:
					error_message += " " + _("السبب: {0}").format(reason)
				
				frappe.throw(error_message)