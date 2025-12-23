import frappe
from frappe import _


def validate(doc, method=None):
	"""التحقق من أن اسم الـ Lead غير موجود في قائمة الأسماء المحظورة"""
	if not doc.lead_name:
		return
	
	# تحويل الاسم إلى حالة صغيرة للمقارنة (يدعم العربي والإنجليزي)
	lead_name_normalized = doc.lead_name.strip().lower()
	lead_name_parts = lead_name_normalized.split()
	
	# التحقق من أن الاسم ثنائي أو ثلاثي
	if len(lead_name_parts) < 2 or len(lead_name_parts) > 3:
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
			# التحقق من التطابق: إذا تطابق الاسمان تماماً أو تطابقت أول جزئين
			is_match = False
			
			# إذا كانا بنفس الطول، تحقق من التطابق الكامل
			if len(blacklisted_parts) == len(lead_name_parts):
				if blacklisted_name_normalized == lead_name_normalized:
					is_match = True
			# إذا كان أحدهما ثنائي والآخر ثلاثي، تحقق من تطابق أول جزئين
			elif len(blacklisted_parts) == 2 and len(lead_name_parts) == 3:
				if blacklisted_parts[0] == lead_name_parts[0] and blacklisted_parts[1] == lead_name_parts[1]:
					is_match = True
			elif len(blacklisted_parts) == 3 and len(lead_name_parts) == 2:
				if blacklisted_parts[0] == lead_name_parts[0] and blacklisted_parts[1] == lead_name_parts[1]:
					is_match = True
			
			if is_match:
				reason = blacklisted.reason
				
				error_message = _(
					"اسم الـ Lead '{0}' مسجل في قائمة الأسماء المحظورة ولا يمكن التعامل معه."
				).format(doc.lead_name)
				
				if reason:
					error_message += " " + _("السبب: {0}").format(reason)
				
				frappe.throw(error_message)

