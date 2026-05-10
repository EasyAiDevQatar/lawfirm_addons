#!/usr/bin/env python3
"""Regenerate print_format.json — run from repo: python3 apps/lawfirm_addons/.../_generate_print_formats.py"""
import json
from pathlib import Path
from typing import Optional

HERE = Path(__file__).resolve().parent

BASE_CSS = r"""
.lfa-print { font-family: "Segoe UI", Tahoma, Arial, sans-serif; color: #1a202c; font-size: 11px; }
.lfa-print.rtl { direction: rtl; text-align: right; }
.lfa-letterhead { margin-bottom: 18px; padding-bottom: 14px; border-bottom: 3px solid #1a365d; }
.lfa-letterhead img.lfa-logo { max-height: 72px; max-width: 220px; object-fit: contain; }
.lfa-company-line { font-size: 18px; font-weight: 700; color: #1a365d; letter-spacing: 0.02em; }
.lfa-company-sub { font-size: 11px; color: #4a5568; margin-top: 4px; line-height: 1.5; }
.lfa-doc-title { font-size: 20px; font-weight: 700; color: #1a365d; margin: 12px 0 8px 0; text-align: center; }
.lfa-meta-grid { display: table; width: 100%; border-collapse: collapse; margin: 12px 0; border: 1px solid #cbd5e0; }
.lfa-meta-row { display: table-row; }
.lfa-meta-cell { display: table-cell; padding: 6px 10px; border-bottom: 1px solid #e2e8f0; width: 50%; vertical-align: top; }
.lfa-meta-cell b { color: #2d3748; }
.lfa-meta-full { display: table-cell; padding: 6px 10px; border-bottom: 1px solid #e2e8f0; width: 100%; vertical-align: top; }
.lfa-table { width: 100%; border-collapse: collapse; margin-top: 10px; font-size: 10px; }
.lfa-table th { background: #1a365d; color: #fff; padding: 8px 6px; font-weight: 600; border: 1px solid #1a365d; }
.lfa-table td { padding: 6px; border: 1px solid #cbd5e0; vertical-align: top; }
.lfa-table tr:nth-child(even) td { background: #f7fafc; }
.lfa-totals { margin-top: 14px; width: 100%; max-width: 380px; margin-inline-start: auto; border: 1px solid #cbd5e0; }
.lfa-totals td { padding: 6px 10px; border-bottom: 1px solid #e2e8f0; }
.lfa-totals tr:last-child td { font-weight: 700; font-size: 13px; background: #edf2f7; border-bottom: none; }
.lfa-footer-note { margin-top: 20px; padding-top: 12px; border-top: 1px solid #cbd5e0; font-size: 9px; color: #718096; text-align: center; }
.lfa-lh-embed { margin-bottom: 8px; }
.lfa-letterfoot { margin-top: 20px; padding-top: 14px; border-top: 2px solid #1a365d; font-size: 10px; color: #4a5568; text-align: center; line-height: 1.5; }
.lfa-pe-hero { display: flex; flex-wrap: wrap; gap: 12px; margin: 16px 0; justify-content: center; }
.lfa-pe-card { flex: 1; min-width: 200px; max-width: 320px; border-radius: 10px; padding: 14px 18px; border: 1px solid #bee3f8; background: linear-gradient(160deg, #ebf8ff 0%, #f0fff4 100%); text-align: center; }
.lfa-pe-card .lfa-pe-lbl { font-size: 11px; color: #2c5282; font-weight: 600; }
.lfa-pe-card .lfa-pe-amt { font-size: 24px; font-weight: 800; color: #1a365d; margin-top: 8px; letter-spacing: 0.02em; }
.lfa-pe-badge { display: inline-block; padding: 4px 12px; border-radius: 999px; font-size: 11px; font-weight: 600; background: #1a365d; color: #fff; margin-bottom: 8px; }
.lfa-pe-refs-title { font-size: 12px; font-weight: 700; color: #1a365d; margin: 18px 0 8px 0; }
.lfa-file-ref { font-size: 14px; font-weight: 700; color: #1a365d; text-align: center; margin: 0 0 14px 0; padding: 8px; background: #f7fafc; border: 1px solid #cbd5e0; border-radius: 6px; }
.lfa-section-h { font-size: 12px; font-weight: 700; color: #1a365d; margin: 16px 0 0 0; padding: 8px 10px; background: linear-gradient(90deg, #edf2f7 0%, #f7fafc 100%); border: 1px solid #e2e8f0; border-inline-start: 4px solid #1a365d; }
.lfa-prayer { margin: 0 0 12px 0; padding: 12px; border: 1px solid #e2e8f0; background: #fafafa; font-size: 10px; line-height: 1.55; white-space: pre-wrap; }
.lfa-thumb { max-height: 56px; max-width: 120px; object-fit: contain; vertical-align: middle; border: 1px solid #e2e8f0; border-radius: 4px; }
.lfa-si-banner { display: flex; flex-wrap: wrap; justify-content: space-between; gap: 12px; align-items: flex-start; margin-bottom: 12px; padding: 12px; background: #f7fafc; border: 1px solid #cbd5e0; border-radius: 8px; }
.lfa-si-items-note { font-size: 9px; color: #718096; margin-top: 6px; }
.lfa-report-card { border: 1px solid #cbd5e0; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 14px rgba(26,54,93,0.07); margin-top: 10px; background: #fff; }
.lfa-report-meta { display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px; padding: 10px 14px; background: linear-gradient(90deg, #edf2f7 0%, #f7fafc 100%); border-bottom: 2px solid #1a365d; font-size: 10px; color: #2d3748; }
.lfa-report-meta b { color: #1a365d; }
.lfa-table.lfa-report-table { margin-top: 0; font-size: 9.5px; }
.lfa-table.lfa-report-table th { padding: 9px 7px; font-size: 9px; letter-spacing: 0.02em; }
.lfa-table.lfa-report-table td { padding: 7px; }
"""

# Header + optional Letter Head footer (HTML / image) from same Letter Head record as header
LETTERHEAD = r"""
{% set comp_name = doc.company or frappe.defaults.get_default("Company") %}
{% if comp_name %}
{% set comp = frappe.get_doc("Company", comp_name) %}
{% set _lh_html = "" %}
{% set _lh_footer_html = "" %}
{% set active_lh = none %}
{% if comp.default_letter_head %}
{% set active_lh = frappe.get_doc("Letter Head", comp.default_letter_head) %}
{% endif %}
{% if not active_lh %}
{% set _def = frappe.get_all("Letter Head", filters={"disabled": 0, "is_default": 1}, fields=["name"], limit=1) %}
{% if not _def %}{% set _def = frappe.get_all("Letter Head", filters={"disabled": 0}, fields=["name"], limit=1) %}{% endif %}
{% if _def %}{% set active_lh = frappe.get_doc("Letter Head", _def[0].name) %}{% endif %}
{% endif %}
{% if active_lh %}
{% if active_lh.source == 'HTML' and active_lh.content %}
{% set _lh_html = frappe.utils.jinja.render_template(active_lh.content, {"doc": doc}) %}
{% elif active_lh.source == 'Image' and active_lh.image %}
{% set _lh_html = '<div style="text-align:center"><img class="lfa-logo" src="' + active_lh.image + '" alt="" /></div>' %}
{% endif %}
{% if active_lh.footer_source == 'HTML' and active_lh.footer %}
{% set _lh_footer_html = frappe.utils.jinja.render_template(active_lh.footer, {"doc": doc}) %}
{% elif active_lh.footer_source == 'Image' and active_lh.footer_image %}
{% set _lh_footer_html = '<div style="text-align:center"><img src="' + active_lh.footer_image + '" alt="" style="max-height:72px;max-width:100%;object-fit:contain;" /></div>' %}
{% endif %}
{% endif %}
{% if _lh_html %}
<div class="lfa-lh-embed">{{ _lh_html | safe }}</div>
{% else %}
<div style="display:flex;align-items:center;gap:16px;flex-wrap:wrap;">
{% if comp.company_logo %}<img class="lfa-logo" src="{{ comp.company_logo }}" alt="" />{% endif %}
<div style="flex:1;min-width:200px;">
<div class="lfa-company-line">{{ comp.company_name or comp.name }}</div>
<div class="lfa-company-sub">
{% if comp.tax_id %}<span>الرقم الضريبي: {{ comp.tax_id }}</span><br/>{% endif %}
{% if comp.email %}<span>{{ comp.email }}</span>{% endif %}
{% if comp.phone_no %}<span> — {{ comp.phone_no }}</span>{% endif %}
{% if comp.website %}<br/><span>{{ comp.website }}</span>{% endif %}
</div>
</div>
</div>
{% endif %}
{% endif %}
"""

LETTERFOOTER = r"""
{% if _lh_footer_html is defined and _lh_footer_html %}
<div class="lfa-letterfoot">{{ _lh_footer_html | safe }}</div>
{% endif %}
"""

CASE_META = r"""
<div class="lfa-file-ref">رقم ملف القضية: {{ doc.name }}</div>
<div class="lfa-section-h">البيانات الأساسية</div>
<div class="lfa-meta-grid">
<div class="lfa-meta-row"><div class="lfa-meta-cell"><b>عنوان القضية</b><br/>{{ doc.case_title or "—" }}</div><div class="lfa-meta-cell"><b>رقم التسجيل</b><br/>{{ doc.registration_number or "—" }}</div></div>
<div class="lfa-meta-row"><div class="lfa-meta-cell"><b>المادة Matter</b><br/>{{ doc.matter or "—" }}</div><div class="lfa-meta-cell"><b>حالة القضية</b><br/>{{ doc.status or "—" }}</div></div>
<div class="lfa-meta-row"><div class="lfa-meta-cell"><b>الخدمة</b><br/>{{ doc.service or "—" }}</div><div class="lfa-meta-cell"><b>حالة التدقيق</b><br/>{{ doc.scrutiny_status or "—" }}</div></div>
<div class="lfa-meta-row"><div class="lfa-meta-cell"><b>المدعي</b><br/>{{ doc.petitioner or "—" }}</div><div class="lfa-meta-cell"><b>المدعى عليه</b><br/>{{ doc.respondent or "—" }}</div></div>
<div class="lfa-meta-row"><div class="lfa-meta-cell"><b>صفة التمثيل</b><br/>{{ doc.representing or "—" }}</div><div class="lfa-meta-cell"><b>تفاصيل التمثيل</b><br/>{{ doc.representation_details or "—" }}</div></div>
<div class="lfa-meta-row"><div class="lfa-meta-cell"><b>اسم العميل</b><br/>{{ doc.customer_name or "—" }}</div><div class="lfa-meta-cell"><b>كود العميل</b><br/>{{ doc.customer or "—" }}</div></div>
<div class="lfa-meta-row"><div class="lfa-meta-cell"><b>رقم الهاتف</b><br/>{{ doc.contact_no or "—" }}</div><div class="lfa-meta-cell"><b>الإيميل</b><br/>{{ doc.contact_email or "—" }}</div></div>
<div class="lfa-meta-row"><div class="lfa-meta-cell"><b>الفرع</b><br/>{{ doc.branch or "—" }}</div><div class="lfa-meta-cell"><b>الشركة</b><br/>{{ doc.company or "—" }}</div></div>
<div class="lfa-meta-row"><div class="lfa-meta-cell"><b>تاريخ الجلسة القادمة</b><br/>{{ frappe.utils.formatdate(doc.next_hearing_date) if doc.next_hearing_date else "—" }}</div><div class="lfa-meta-cell"><b>موقع الملف</b><br/>{{ doc.file_location or "—" }}</div></div>
<div class="lfa-meta-row"><div class="lfa-meta-cell"><b>طبيعة الفصل</b><br/>{{ doc.nature_of_disposal or "—" }}</div><div class="lfa-meta-cell"><b>تاريخ الفصل</b><br/>{{ frappe.utils.formatdate(doc.date_of_disposal) if doc.date_of_disposal else "—" }}</div></div>
</div>
<div class="lfa-section-h">أرقام القضية والإيداع</div>
<div class="lfa-meta-grid">
<div class="lfa-meta-row"><div class="lfa-meta-cell"><b>رقم القضية</b><br/>{{ doc.case_no or "—" }}</div><div class="lfa-meta-cell"><b>سنة القضية</b><br/>{{ doc.case_year or "—" }}</div></div>
<div class="lfa-meta-row"><div class="lfa-meta-cell"><b>رقم الإيداع</b><br/>{{ doc.filing_number or "—" }}</div><div class="lfa-meta-cell"><b>سنة الإيداع</b><br/>{{ doc.filing_year or "—" }}</div></div>
<div class="lfa-meta-row"><div class="lfa-meta-cell"><b>تاريخ الإيداع</b><br/>{{ frappe.utils.formatdate(doc.date_of_filing) if doc.date_of_filing else "—" }}</div><div class="lfa-meta-cell"><b>تاريخ التسجيل</b><br/>{{ frappe.utils.formatdate(doc.date_of_registration) if doc.date_of_registration else "—" }}</div></div>
{% if doc.almeezan_link %}<div class="lfa-meta-row"><div class="lfa-meta-full"><b>الميزان / رابط</b><br/>{{ doc.almeezan_link }}</div></div>{% endif %}
</div>
<div class="lfa-section-h">التوكيل</div>
<div class="lfa-meta-grid">
<div class="lfa-meta-row"><div class="lfa-meta-cell"><b>رقم التوكيل</b><br/>{{ doc.custom_tokeel_no or "—" }}</div><div class="lfa-meta-cell"><b>صورة التوكيل</b><br/>{% if doc.custom_tokeel_image %}<img class="lfa-thumb" src="{{ doc.custom_tokeel_image }}" alt="" />{% else %}—{% endif %}</div></div>
</div>
{% if doc.prayer %}
<div class="lfa-section-h">الدعوى / الطلبات</div>
<div class="lfa-prayer">{{ doc.prayer | striptags }}</div>
{% endif %}
{% if doc.petitioner_details %}
<div class="lfa-section-h">تفاصيل الأطراف — المدعي</div>
<table class="lfa-table">
<thead><tr><th>#</th><th>الترتيب</th><th>الاسم</th><th>العنوان</th><th>المحامي</th></tr></thead>
<tbody>
{% for row in doc.petitioner_details %}
<tr>
<td>{{ loop.index }}</td>
<td>{{ row.rank_of_party or "" }}</td>
<td>{{ row.party_name or "" }}</td>
<td>{{ row.address or "" }}</td>
<td>{{ row.advocate or "" }}</td>
</tr>
{% endfor %}
</tbody>
</table>
{% endif %}
{% if doc.respondent_details %}
<div class="lfa-section-h">تفاصيل الأطراف — المدعى عليه</div>
<table class="lfa-table">
<thead><tr><th>#</th><th>الترتيب</th><th>الاسم</th><th>العنوان</th><th>المحامي</th></tr></thead>
<tbody>
{% for row in doc.respondent_details %}
<tr>
<td>{{ loop.index }}</td>
<td>{{ row.rank_of_party or "" }}</td>
<td>{{ row.party_name or "" }}</td>
<td>{{ row.address or "" }}</td>
<td>{{ row.advocate or "" }}</td>
</tr>
{% endfor %}
</tbody>
</table>
{% endif %}
"""


def case_html(title: str, loop: str, include_next_col: bool, table_heading: str = "البيانات التفصيلية للجلسات") -> str:
    next_th = "\n      <th>تاريخ الجلسة القادمة</th>" if include_next_col else ""
    next_td = (
        '\n      <td style="font-weight:600;">{{ frappe.utils.formatdate(row.next_date, "dd-mm-yyyy") if row.next_date else "" }}</td>'
        if include_next_col
        else ""
    )
    return f"""<style>{BASE_CSS}</style>
<div class="lfa-print rtl">
<div class="lfa-letterhead">{LETTERHEAD}</div>
<div class="lfa-doc-title">{title}</div>
{CASE_META}
<div class="lfa-section-h">{table_heading}</div>
<table class="lfa-table">
  <thead>
    <tr>
      <th>#</th>
      <th>تاريخ الجلسة الأولى</th>
      <th>المحكمة</th>
      <th>الدرجة</th>
      <th>المسلسل</th>
      <th>رقم القضية</th>
      <th>الدائرة</th>
      <th>موضوع القضية</th>
      <th>مكان الجلسة</th>
      <th>مكان الحضور</th>
      <th>اسم العميل (الصف)</th>
      <th>صفة العميل</th>
      <th>الخصم</th>
      <th>صفة الخصم</th>
      <th>القرار السابق</th>
      <th style="min-width:140px;">قرار الجلسة</th>
      <th>الطلبات</th>
      <th>رقم التوكيل</th>
      <th>مرفق</th>
      <th>صورة التوكيل</th>
      <th>الوكيل</th>{next_th}
    </tr>
  </thead>
  <tbody>
    {{% for row in {loop} %}}
    <tr>
      <td>{{{{ loop.index }}}}</td>
      <td style="font-weight:600;">{{{{ frappe.utils.formatdate(row.business_on_date, "dd-mm-yyyy") if row.business_on_date else "" }}}}</td>
      <td>{{{{ row.court or "" }}}}</td>
      <td>{{{{ row.litigation_degree or "" }}}}</td>
      <td>{{{{ row.registration_no or "" }}}}</td>
      <td>{{{{ row.case_number or "" }}}}</td>
      <td>{{{{ row.chamber or "" }}}}</td>
      <td>{{{{ row.case_subject or "" }}}}</td>
      <td>{{{{ row.case_location or "" }}}}</td>
      <td>{{{{ row.attendance_location or "" }}}}</td>
      <td>{{{{ row.client or "" }}}}</td>
      <td>{{{{ row.client_capacity or "" }}}}</td>
      <td>{{{{ row.opponent or "" }}}}</td>
      <td>{{{{ row.opponent_capacity or "" }}}}</td>
      <td>{{{{ row.previous_decision or "" }}}}</td>
      <td style="font-size:9px;">{{{{ row.decision or "" }}}}</td>
      <td style="font-size:9px;">{{{{ row.defense_summary or "" }}}}</td>
      <td>{{{{ row.tokeel_no or "" }}}}</td>
      <td>{{% if row.attachments %}}✓{{% else %}}—{{% endif %}}</td>
      <td>{{% if row.tokeel_image %}}✓{{% else %}}—{{% endif %}}</td>
      <td>{{{{ row.agent or "" }}}}</td>{next_td}
    </tr>
    {{% endfor %}}
  </tbody>
</table>
{LETTERFOOTER}
<div class="lfa-footer-note">وثيقة مولدة آلياً — {{{{ doc.name }}}} — {{{{ frappe.utils.nowdate() }}}}</div>
</div>"""


# Client-side (microtemplate) format for Query Reports — same context as print_grid.html
REPORT_GRID_JS = (
    r"""<style>"""
    + BASE_CSS
    + r"""</style>
<div class="lfa-print rtl">
<div class="lfa-report-card">
{% if title %}
<div class="lfa-doc-title" style="margin-top:0;padding:14px 14px 8px 14px;background:#fff;">{{ title }}</div>
{% endif %}
<div class="lfa-report-meta">
{% if report %}
<span><b>{{ __("Report") }}:</b> {{ report.report_name }}</span>
{% endif %}
<span><b>{{ __("Printed on") }}</b> {{ frappe.datetime.now_datetime() }}</span>
</div>
{% if subtitle %}
<div style="padding:10px 14px;font-size:10px;background:#fafafa;border-bottom:1px solid #e2e8f0;">{{ subtitle }}</div>
{% endif %}
<table class="lfa-table lfa-report-table">
<thead>
<tr>
<th> # </th>
{% for col in columns %}
{% if col.name && col._id !== "_check" %}
<th
{% if col.minWidth %}
style="min-width: {{ col.minWidth }}px"
{% endif %}
{% if frappe.model.is_numeric_field(col.fieldtype) %}
class="text-right"
{% endif %}
>{{ __(col.name) }}</th>
{% endif %}
{% endfor %}
</tr>
</thead>
<tbody>
{% for row in data %}
<tr>
<td>{% if row.bold == 1 %}<strong>{% endif %}<span>{{ row._index + 1 }}</span>{% if row.bold == 1 %}</strong>{% endif %}</td>
{% for col in columns %}
{% if col.name && col._id !== "_check" %}
{% var value = col.fieldname ? row[col.fieldname] : row[col.id] %}
{% var longest_word = cstr(value).split(' ').reduce((longest, word) => word.length > longest.length ? word : longest, ''); %}
<td {% if row.bold == 1 %} style="font-weight: bold" {% endif %} {% if longest_word.length > 45 %} class="overflow-wrap-anywhere" {% endif %}>
<span {% if col._index == 0 %} style="padding-left: {%= cint(row.indent) * 2 %}em" {% endif %}>
{% format_data = row.is_total_row && ["Currency", "Float"].includes(col.fieldtype) ? data[0] : row %}
{% if (row.is_total_row && col._index == 0) { %}
{{ __("Total") }}
{% } else { %}
{{ col.formatter ? col.formatter(row._index, col._index, value, col, format_data, true) : col.format ? col.format(value, row, col, format_data) : col.docfield ? frappe.format(value, col.docfield) : value }}
{% } %}
</span>
</td>
{% endif %}
{% endfor %}
</tr>
{% endfor %}
</tbody>
</table>
<div class="lfa-footer-note" style="margin:0;padding:10px 14px;border-top:1px solid #e2e8f0;background:#f8fafc;">وثيقة مولدة من النظام</div>
</div>
</div>"""
)


SI_BLOCK = rf"""<style>{BASE_CSS}</style>
<div class="lfa-print rtl">
<div class="lfa-letterhead">{LETTERHEAD}</div>
<div class="lfa-si-banner">
<div style="flex:1;min-width:200px;">
<div class="lfa-doc-title" style="margin:0;text-align:right;">__SI_TITLE__</div>
<div style="font-size:11px;margin-top:6px;color:#4a5568;">{{{{ doc.name }}}}</div>
</div>
<div style="text-align:left;font-size:11px;min-width:200px;line-height:1.6;">
{{% if doc.custom_invoice_type %}}<div><b>نوع الفاتورة:</b> {{{{ doc.custom_invoice_type }}}}</div>{{% endif %}}
<div><b>تاريخ الفاتورة:</b> {{{{ frappe.utils.formatdate(doc.posting_date) }}}}</div>
{{% if doc.due_date %}}<div><b>الاستحقاق:</b> {{{{ frappe.utils.formatdate(doc.due_date) }}}}</div>{{% endif %}}
{{% if doc.po_no %}}<div><b>أمر شراء:</b> {{{{ doc.po_no }}}}{{% if doc.po_date %}} — {{{{ frappe.utils.formatdate(doc.po_date) }}}}{{% endif %}}</div>{{% endif %}}
</div>
</div>
<div class="lfa-section-h">العميل والفوترة</div>
<div class="lfa-meta-grid">
<div class="lfa-meta-row"><div class="lfa-meta-cell"><b>اسم العميل</b><br/>{{{{ doc.customer_name or doc.customer }}}}</div><div class="lfa-meta-cell"><b>كود العميل</b><br/>{{{{ doc.customer or "—" }}}}</div></div>
<div class="lfa-meta-row"><div class="lfa-meta-cell"><b>الشركة</b><br/>{{{{ doc.company }}}}</div><div class="lfa-meta-cell"><b>العملة</b><br/>{{{{ doc.currency or "—" }}}}</div></div>
<div class="lfa-meta-row"><div class="lfa-meta-cell"><b>عنوان الفوترة</b><br/>{{{{ doc.address_display or doc.customer_address or "—" }}}}</div><div class="lfa-meta-cell"><b>عنوان الشحن / التسليم</b><br/>{{{{ doc.shipping_address or doc.dispatch_address or "—" }}}}</div></div>
<div class="lfa-meta-row"><div class="lfa-meta-cell"><b>اسم جهة الاتصال</b><br/>{{{{ doc.contact_display or doc.contact_person or "—" }}}}</div><div class="lfa-meta-cell"><b>شروط الدفع</b><br/>{{{{ doc.payment_terms_template or "—" }}}}</div></div>
<div class="lfa-meta-row"><div class="lfa-meta-cell"><b>رقم الهاتف</b><br/>{{{{ doc.contact_mobile or (frappe.db.get_value("Customer", doc.customer, "mobile_no") if doc.customer else "") or (frappe.db.get_value("Customer", doc.customer, "phone_no") if doc.customer else "") or "—" }}}}</div><div class="lfa-meta-cell"><b>الإيميل</b><br/>{{{{ doc.contact_email or (frappe.db.get_value("Customer", doc.customer, "email_id") if doc.customer else "") or "—" }}}}</div></div>
<div class="lfa-meta-row"><div class="lfa-meta-cell"><b>قائمة الأسعار</b><br/>{{{{ doc.selling_price_list or "—" }}}}</div><div class="lfa-meta-cell"><b>مكان التوريد / الإقليم</b><br/>{{{{ doc.place_of_supply or doc.territory or "—" }}}}</div></div>
{{% if doc.matter %}}<div class="lfa-meta-row"><div class="lfa-meta-cell"><b>المادة Matter</b><br/>{{{{ doc.matter }}}}</div><div class="lfa-meta-cell"><b>المشروع / مركز التكلفة</b><br/>{{{{ doc.project or "—" }}}} — {{{{ doc.cost_center or "—" }}}}</div></div>{{% endif %}}
{{% if doc.tax_id %}}<div class="lfa-meta-row"><div class="lfa-meta-full"><b>الرقم الضريبي للعميل</b><br/>{{{{ doc.tax_id }}}}</div></div>{{% endif %}}
</div>
{{% if doc.terms %}}<div class="lfa-section-h">الشروط والأحكام</div><div class="lfa-prayer" style="white-space:normal;">{{{{ doc.terms | striptags }}}}</div>{{% endif %}}
<div class="lfa-section-h">بنود الفاتورة</div>
<table class="lfa-table">
<thead><tr><th>#</th><th>الكود</th><th>اسم البند</th><th>الوصف</th><th>الكمية</th><th>الوحدة</th><th>سعر القائمة</th><th>الخصم</th><th>السعر</th><th>الضريبة</th><th>صافي</th><th>الإجمالي</th></tr></thead>
<tbody>
{{% for it in doc.items %}}
<tr>
<td>{{{{ loop.index }}}}</td>
<td>{{{{ it.item_code or "" }}}}</td>
<td style="font-size:9px;">{{{{ it.item_name or "" }}}}</td>
<td style="font-size:9px;">{{{{ it.description or "" }}}}</td>
<td>{{{{ it.qty }}}}</td>
<td>{{{{ it.uom or it.stock_uom or "" }}}}</td>
<td>{{{{ frappe.utils.fmt_money(it.price_list_rate or 0, currency=doc.currency) }}}}</td>
<td>{{{{ frappe.utils.fmt_money(it.discount_amount or 0, currency=doc.currency) }}}}</td>
<td>{{{{ frappe.utils.fmt_money(it.rate or 0, currency=doc.currency) }}}}</td>
<td>{{{{ it.item_tax_template or "—" }}}}</td>
<td>{{{{ frappe.utils.fmt_money(it.net_amount or it.amount or 0, currency=doc.currency) }}}}</td>
<td>{{{{ frappe.utils.fmt_money(it.amount or 0, currency=doc.currency) }}}}</td>
</tr>
{{% endfor %}}
</tbody>
</table>
{{% if doc.taxes %}}
<div class="lfa-section-h">تفاصيل الضريبة</div>
<table class="lfa-table">
<thead><tr><th>#</th><th>الوصف</th><th>المعدل</th><th>المبلغ</th></tr></thead>
<tbody>
{{% for tx in doc.taxes %}}
<tr>
<td>{{{{ loop.index }}}}</td>
<td>{{{{ tx.description or tx.account_head or "" }}}}</td>
<td>{{{{ tx.rate or "" }}}}</td>
<td>{{{{ frappe.utils.fmt_money(tx.tax_amount or 0, currency=doc.currency) }}}}</td>
</tr>
{{% endfor %}}
</tbody>
</table>
{{% endif %}}
<table class="lfa-totals">
<tr><td>إجمالي الكميات / المجموع</td><td>{{{{ frappe.utils.fmt_money(doc.total or 0, currency=doc.currency) }}}}</td></tr>
<tr><td>مجموع الخصومات</td><td>{{{{ frappe.utils.fmt_money(doc.discount_amount or 0, currency=doc.currency) }}}}</td></tr>
<tr><td>المجموع قبل الضريبة</td><td>{{{{ frappe.utils.fmt_money(doc.net_total or 0, currency=doc.currency) }}}}</td></tr>
{{% if doc.total_taxes_and_charges %}}<tr><td>إجمالي الضريبة</td><td>{{{{ frappe.utils.fmt_money(doc.total_taxes_and_charges or 0, currency=doc.currency) }}}}</td></tr>{{% endif %}}
<tr><td>الإجمالي الكلي</td><td>{{{{ frappe.utils.fmt_money(doc.grand_total or 0, currency=doc.currency) }}}}</td></tr>
{{% if doc.rounding_adjustment %}}<tr><td>تعديل التقريب</td><td>{{{{ frappe.utils.fmt_money(doc.rounding_adjustment or 0, currency=doc.currency) }}}}</td></tr>{{% endif %}}
{{% if doc.rounded_total %}}<tr><td>المستحق بعد التقريب</td><td>{{{{ frappe.utils.fmt_money(doc.rounded_total or 0, currency=doc.currency) }}}}</td></tr>{{% endif %}}
</table>
{{% if doc.in_words %}}<div style="margin-top:12px;font-style:italic;font-size:11px;border-top:1px solid #e2e8f0;padding-top:8px;"><b>المبلغ كتابة:</b> {{{{ doc.in_words }}}}</div>{{% endif %}}
{LETTERFOOTER}
<div class="lfa-footer-note">{{{{ doc.name }}}} — {{{{ frappe.utils.nowdate() }}}}</div>
</div>"""

PE_BLOCK = rf"""<style>{BASE_CSS}</style>
<div class="lfa-print rtl">
<div class="lfa-letterhead">{LETTERHEAD}</div>
<div class="lfa-file-ref" style="margin-bottom:10px;">سند الدفع: {{{{ doc.name }}}}</div>
<div class="lfa-doc-title" style="margin-bottom:4px;">__PE_TITLE__</div>
<div style="text-align:center;">
<span class="lfa-pe-badge">{{{{ doc.payment_type }}}}</span>
{{% if doc.status %}}<span class="lfa-pe-badge" style="background:#4a5568;margin-inline-start:8px;">{{{{ doc.status }}}}</span>{{% endif %}}
</div>
<div class="lfa-pe-hero">
<div class="lfa-pe-card">
<div class="lfa-pe-lbl">المبلغ المدفوع (من الحساب)</div>
<div class="lfa-pe-amt">{{{{ frappe.utils.fmt_money(doc.paid_amount or 0, currency=doc.paid_from_account_currency or doc.company_currency) }}}}</div>
<div style="font-size:10px;color:#718096;margin-top:6px;">{{{{ doc.paid_from or "" }}}}</div>
{{% if doc.source_exchange_rate and doc.source_exchange_rate != 1 %}}<div style="font-size:9px;margin-top:4px;">سعر الصرف: {{{{ doc.source_exchange_rate }}}}</div>{{% endif %}}
</div>
<div class="lfa-pe-card">
<div class="lfa-pe-lbl">المبلغ المستلم (إلى الحساب)</div>
<div class="lfa-pe-amt">{{{{ frappe.utils.fmt_money(doc.received_amount or 0, currency=doc.paid_to_account_currency or doc.company_currency) }}}}</div>
<div style="font-size:10px;color:#718096;margin-top:6px;">{{{{ doc.paid_to or "" }}}}</div>
{{% if doc.target_exchange_rate and doc.target_exchange_rate != 1 %}}<div style="font-size:9px;margin-top:4px;">سعر الصرف: {{{{ doc.target_exchange_rate }}}}</div>{{% endif %}}
</div>
</div>
<div class="lfa-section-h">بيانات السند</div>
<div class="lfa-meta-grid">
<div class="lfa-meta-row"><div class="lfa-meta-cell"><b>تاريخ الترحيل</b><br/>{{{{ frappe.utils.formatdate(doc.posting_date) }}}}</div><div class="lfa-meta-cell"><b>طريقة الدفع</b><br/>{{{{ doc.mode_of_payment or "—" }}}}</div></div>
<div class="lfa-meta-row"><div class="lfa-meta-cell"><b>الشركة</b><br/>{{{{ doc.company or "—" }}}}</div><div class="lfa-meta-cell"><b>العملة الشركة</b><br/>{{{{ doc.company_currency or "—" }}}}</div></div>
<div class="lfa-meta-row"><div class="lfa-meta-cell"><b>مرجع الدفع</b><br/>{{{{ doc.reference_no or "—" }}}}</div><div class="lfa-meta-cell"><b>تاريخ المرجع</b><br/>{{{{ frappe.utils.formatdate(doc.reference_date) if doc.reference_date else "—" }}}}</div></div>
{{% if doc.clearance_date %}}<div class="lfa-meta-row"><div class="lfa-meta-cell"><b>تاريخ التسوية</b><br/>{{{{ frappe.utils.formatdate(doc.clearance_date) }}}}</div><div class="lfa-meta-cell"><b>البنك</b><br/>{{{{ doc.bank or "—" }}}}</div></div>{{% endif %}}
{{% if doc.bank_account_no %}}<div class="lfa-meta-row"><div class="lfa-meta-full"><b>رقم الحساب البنكي</b><br/>{{{{ doc.bank_account_no }}}}</div></div>{{% endif %}}
</div>
<div class="lfa-section-h">الطرف والحسابات</div>
<div class="lfa-meta-grid">
<div class="lfa-meta-row"><div class="lfa-meta-cell"><b>نوع الطرف</b><br/>{{{{ doc.party_type or "—" }}}}</div><div class="lfa-meta-cell"><b>الطرف</b><br/>{{{{ doc.party or "—" }}}}</div></div>
<div class="lfa-meta-row"><div class="lfa-meta-cell"><b>اسم الطرف</b><br/>{{{{ doc.party_name or "—" }}}}</div><div class="lfa-meta-cell"><b>حساب الطرف البنكي</b><br/>{{{{ doc.party_bank_account or "—" }}}}</div></div>
<div class="lfa-meta-row"><div class="lfa-meta-cell"><b>رقم الهاتف</b><br/>{{% if doc.contact_person %}}{{{{ frappe.db.get_value("Contact", doc.contact_person, "mobile_no") or frappe.db.get_value("Contact", doc.contact_person, "phone") or "—" }}}}{{% elif doc.party_type == "Customer" and doc.party %}}{{{{ frappe.db.get_value("Customer", doc.party, "mobile_no") or frappe.db.get_value("Customer", doc.party, "phone_no") or "—" }}}}{{% elif doc.party_type == "Supplier" and doc.party %}}{{{{ frappe.db.get_value("Supplier", doc.party, "mobile_no") or "—" }}}}{{% else %}}—{{% endif %}}</div><div class="lfa-meta-cell"><b>الإيميل</b><br/>{{% if doc.contact_email %}}{{{{ doc.contact_email }}}}{{% elif doc.contact_person %}}{{{{ frappe.db.get_value("Contact", doc.contact_person, "email_id") or "—" }}}}{{% elif doc.party_type == "Customer" and doc.party %}}{{{{ frappe.db.get_value("Customer", doc.party, "email_id") or "—" }}}}{{% elif doc.party_type == "Supplier" and doc.party %}}{{{{ frappe.db.get_value("Supplier", doc.party, "email_id") or "—" }}}}{{% else %}}—{{% endif %}}</div></div>
<div class="lfa-meta-row"><div class="lfa-meta-cell"><b>حساب الدفع (البنك)</b><br/>{{{{ doc.bank_account or "—" }}}}</div><div class="lfa-meta-cell"><b>المشروع / مركز التكلفة</b><br/>{{{{ doc.project or "—" }}}} — {{{{ doc.cost_center or "—" }}}}</div></div>
</div>
{{% if doc.title %}}<div class="lfa-meta-grid" style="margin-top:8px;"><div class="lfa-meta-row"><div class="lfa-meta-full"><b>البيان / العنوان</b><br/>{{{{ doc.title }}}}</div></div></div>{{% endif %}}
{{% if doc.custom_matter %}}<div class="lfa-meta-grid"><div class="lfa-meta-row"><div class="lfa-meta-full"><b>المادة Matter</b><br/>{{{{ doc.custom_matter }}}}</div></div></div>{{% endif %}}
{{% if doc.remarks %}}<div class="lfa-meta-grid"><div class="lfa-meta-row"><div class="lfa-meta-full"><b>ملاحظات</b><br/>{{{{ doc.remarks }}}}</div></div></div>{{% endif %}}
{{% if doc.references %}}
<div class="lfa-section-h">ملخص المبلغ</div>
<div class="lfa-meta-grid">
<div class="lfa-meta-row"><div class="lfa-meta-full"><b>إجمالي المبلغ</b><br/>{{{{ frappe.utils.fmt_money(doc.total_allocated_amount or 0, currency=doc.company_currency) }}}}</div></div>
</div>
<div class="lfa-pe-refs-title">تخصيص على الفواتير والمستندات</div>
<table class="lfa-table">
<thead><tr><th style="width:36px;">#</th><th>نوع المستند</th><th>رقم المستند</th><th>المبلغ</th></tr></thead>
<tbody>
{{% for r in doc.references %}}
<tr>
<td>{{{{ loop.index }}}}</td>
<td>{{{{ r.reference_doctype or "" }}}}</td>
<td>{{{{ r.reference_name or "" }}}}</td>
<td style="font-weight:600;">{{{{ frappe.utils.fmt_money(r.allocated_amount or 0, currency=doc.company_currency) }}}}</td>
</tr>
{{% endfor %}}
</tbody>
</table>
{{% endif %}}
{{% if doc.in_words %}}<div style="margin-top:10px;font-size:11px;font-style:italic;"><b>المبلغ كتابة:</b> {{{{ doc.in_words }}}}</div>{{% endif %}}
{LETTERFOOTER}
<div class="lfa-footer-note">{{{{ doc.name }}}} — {{{{ frappe.utils.nowdate() }}}}</div>
</div>"""


def pf_record(
    name: str,
    html: str,
    *,
    doc_type: Optional[str] = None,
    print_format_for: str = "DocType",
    report: Optional[str] = None,
    print_format_type: str = "Jinja",
):
    row = {
        "creation": "2026-05-10 12:00:00.000000",
        "custom_format": 1,
        "default_print_language": None,
        "disabled": 0,
        "docstatus": 0,
        "doctype": "Print Format",
        "font": "Default",
        "idx": 0,
        "line_breaks": 0,
        "modified": "2026-05-10 16:00:00.000000",
        "modified_by": "Administrator",
        "module": "Lawfirm Addons",
        "name": name,
        "owner": "Administrator",
        "print_format_builder": 0,
        "print_format_type": print_format_type,
        "print_format_for": print_format_for,
        "raw_printing": 0,
        "show_section_headings": 0,
        "standard": "No",
        "html": html,
        "css": BASE_CSS.strip(),
    }
    if doc_type:
        row["doc_type"] = doc_type
    if report:
        row["report"] = report
    return row


def main():
    out = [
        pf_record(
            "Case Sessions Print",
            case_html(
                "تقرير جدول الجلسات — الجلسات الحالية",
                "doc.case_sessions",
                True,
                "جدول الجلسات الحالية (جميع البيانات)",
            ),
            doc_type="Case",
        ),
        pf_record(
            "Case History Print",
            case_html(
                "تقرير جدول الجلسات — السجل التاريخي",
                "doc.case_history",
                False,
                "جدول السجل التاريخي (جميع البيانات)",
            ),
            doc_type="Case",
        ),
        # doc_type required on some Frappe versions during fixture import even for print_format_for=Report.
        pf_record(
            "Case Sessions Report Print",
            REPORT_GRID_JS,
            doc_type="Case",
            print_format_for="Report",
            report="Case Sessions Report",
            print_format_type="JS",
        ),
        pf_record(
            "Case History Report Print",
            REPORT_GRID_JS,
            doc_type="Case",
            print_format_for="Report",
            report="Case History Report",
            print_format_type="JS",
        ),
        pf_record(
            "Sales Invoice - فاتورة رسوم دعوى",
            SI_BLOCK.replace("__SI_TITLE__", "فاتورة رسوم دعوى"),
            doc_type="Sales Invoice",
        ),
        pf_record(
            "Sales Invoice - فاتورة اتعاب",
            SI_BLOCK.replace("__SI_TITLE__", "فاتورة اتعاب"),
            doc_type="Sales Invoice",
        ),
        pf_record(
            "Payment Entry - استلام مبلغ عن فاتورة رسوم دعوى",
            PE_BLOCK.replace("__PE_TITLE__", "سند قبض / دفع — رسوم دعوى"),
            doc_type="Payment Entry",
        ),
        pf_record(
            "Payment Entry - استلام مبلغ عن فاتورة اتعاب",
            PE_BLOCK.replace("__PE_TITLE__", "سند قبض / دفع — اتعاب"),
            doc_type="Payment Entry",
        ),
    ]
    path = HERE / "print_format.json"
    path.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print("Wrote", path)


if __name__ == "__main__":
    main()
