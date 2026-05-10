#!/usr/bin/env python3
"""Regenerate print_format.json — run from repo: python3 apps/lawfirm_addons/.../ _generate_print_formats.py"""
import json
from pathlib import Path

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
"""

# Letter head: Company.default_letter_head, else default Letter Head, else company name + logo + tax
LETTERHEAD = r"""
{% set comp_name = doc.company or frappe.defaults.get_default("Company") %}
{% if comp_name %}
{% set comp = frappe.get_doc("Company", comp_name) %}
{% set _lh_html = "" %}
{% if comp.default_letter_head %}
{% set lh = frappe.get_doc("Letter Head", comp.default_letter_head) %}
{% if lh.source == 'HTML' and lh.content %}
{% set _lh_html = frappe.utils.jinja.render_template(lh.content, {"doc": doc}) %}
{% elif lh.source == 'Image' and lh.image %}
{% set _lh_html = '<div style="text-align:center"><img class="lfa-logo" src="' + lh.image + '" alt="" /></div>' %}
{% endif %}
{% endif %}
{% if not _lh_html %}
{% set _def = frappe.get_all("Letter Head", filters={"disabled": 0, "is_default": 1}, fields=["name"], limit=1) %}
{% if not _def %}{% set _def = frappe.get_all("Letter Head", filters={"disabled": 0}, fields=["name"], limit=1) %}{% endif %}
{% if _def %}
{% set lh2 = frappe.get_doc("Letter Head", _def[0].name) %}
{% if lh2.source == 'HTML' and lh2.content %}
{% set _lh_html = frappe.utils.jinja.render_template(lh2.content, {"doc": doc}) %}
{% elif lh2.source == 'Image' and lh2.image %}
{% set _lh_html = '<div style="text-align:center"><img class="lfa-logo" src="' + lh2.image + '" alt="" /></div>' %}
{% endif %}
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

CASE_META = r"""
<div class="lfa-meta-grid">
<div class="lfa-meta-row"><div class="lfa-meta-cell"><b>عنوان القضية</b><br/>{{ doc.case_title or "—" }}</div><div class="lfa-meta-cell"><b>رقم التسجيل</b><br/>{{ doc.registration_number or "—" }}</div></div>
<div class="lfa-meta-row"><div class="lfa-meta-cell"><b>المادة Matter</b><br/>{{ doc.matter or "—" }}</div><div class="lfa-meta-cell"><b>حالة القضية</b><br/>{{ doc.status or "—" }}</div></div>
<div class="lfa-meta-row"><div class="lfa-meta-cell"><b>المدعي</b><br/>{{ doc.petitioner or "—" }}</div><div class="lfa-meta-cell"><b>المدعى عليه</b><br/>{{ doc.respondent or "—" }}</div></div>
<div class="lfa-meta-row"><div class="lfa-meta-cell"><b>صفة التمثيل</b><br/>{{ doc.representing or "—" }}</div><div class="lfa-meta-cell"><b>تاريخ الجلسة القادمة</b><br/>{{ frappe.utils.formatdate(doc.next_hearing_date) if doc.next_hearing_date else "—" }}</div></div>
<div class="lfa-meta-row"><div class="lfa-meta-cell"><b>اسم العميل</b><br/>{{ doc.customer_name or "—" }}</div><div class="lfa-meta-cell"><b>هاتف / بريد</b><br/>{{ doc.contact_no or "—" }}{% if doc.contact_email %}<br/>{{ doc.contact_email }}{% endif %}</div></div>
<div class="lfa-meta-row"><div class="lfa-meta-cell"><b>الفرع</b><br/>{{ doc.branch or "—" }}</div><div class="lfa-meta-cell"><b>الشركة</b><br/>{{ doc.company or "—" }}</div></div>
<div class="lfa-meta-row"><div class="lfa-meta-cell"><b>تاريخ الإيداع</b><br/>{{ frappe.utils.formatdate(doc.date_of_filing) if doc.date_of_filing else "—" }}</div><div class="lfa-meta-cell"><b>تاريخ التسجيل</b><br/>{{ frappe.utils.formatdate(doc.date_of_registration) if doc.date_of_registration else "—" }}</div></div>
{% if doc.custom_tokeel_no %}<div class="lfa-meta-row"><div class="lfa-meta-full"><b>رقم التوكيل</b><br/>{{ doc.custom_tokeel_no }}</div></div>{% endif %}
</div>
"""


def case_html(title: str, loop: str, include_next_col: bool) -> str:
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
      <th>صفة العميل</th>
      <th>الخصم</th>
      <th>صفة الخصم</th>
      <th>القرار السابق</th>
      <th style="min-width:160px;">قرار الجلسة</th>
      <th>الطلبات</th>
      <th>رقم التوكيل</th>
      <th>مرفق</th>{next_th}
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
      <td>{{{{ row.client_capacity or "" }}}}</td>
      <td>{{{{ row.opponent or "" }}}}</td>
      <td>{{{{ row.opponent_capacity or "" }}}}</td>
      <td>{{{{ row.previous_decision or "" }}}}</td>
      <td style="font-size:10px;">{{{{ row.decision or "" }}}}</td>
      <td>{{{{ row.defense_summary or "" }}}}</td>
      <td>{{{{ row.tokeel_no or "" }}}}</td>
      <td>{{% if row.attachments %}}✓{{% else %}}—{{% endif %}}</td>{next_td}
    </tr>
    {{% endfor %}}
  </tbody>
</table>
<div class="lfa-footer-note">وثيقة مولدة آلياً — {{{{ doc.name }}}} — {{{{ frappe.utils.nowdate() }}}}</div>
</div>"""


SI_BLOCK = rf"""<style>{BASE_CSS}</style>
<div class="lfa-print rtl">
<div class="lfa-letterhead">{LETTERHEAD}</div>
<div style="display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:12px;margin-bottom:8px;">
<div class="lfa-doc-title" style="margin:0;text-align:right;flex:1;">__SI_TITLE__</div>
<div style="text-align:left;font-size:12px;min-width:180px;">
{{% if doc.custom_invoice_type %}}<div><b>نوع الفاتورة:</b> {{{{ doc.custom_invoice_type }}}}</div>{{% endif %}}
<div><b>رقم الفاتورة:</b> {{{{ doc.name }}}}</div>
<div><b>التاريخ:</b> {{{{ frappe.utils.formatdate(doc.posting_date) }}}}</div>
{{% if doc.due_date %}}<div><b>تاريخ الاستحقاق:</b> {{{{ frappe.utils.formatdate(doc.due_date) }}}}</div>{{% endif %}}
</div>
</div>
<div class="lfa-meta-grid">
<div class="lfa-meta-row"><div class="lfa-meta-cell"><b>العميل</b><br/>{{{{ doc.customer_name or doc.customer }}}}</div><div class="lfa-meta-cell"><b>الشركة</b><br/>{{{{ doc.company }}}}</div></div>
<div class="lfa-meta-row"><div class="lfa-meta-cell"><b>عنوان الفوترة</b><br/>{{{{ doc.address_display or doc.customer_address or "—" }}}}</div><div class="lfa-meta-cell"><b>شروط الدفع</b><br/>{{{{ doc.payment_terms_template or "—" }}}}</div></div>
{{% if doc.matter %}}<div class="lfa-meta-row"><div class="lfa-meta-cell"><b>المادة Matter</b><br/>{{{{ doc.matter }}}}</div><div class="lfa-meta-cell"><b>مركز التكلفة</b><br/>{{{{ doc.cost_center or "—" }}}}</div></div>{{% endif %}}
{{% if doc.tax_id %}}<div class="lfa-meta-row"><div class="lfa-meta-full"><b>الرقم الضريبي للعميل</b><br/>{{{{ doc.tax_id }}}}</div></div>{{% endif %}}
</div>
{{% if doc.terms %}}<div style="margin:10px 0;padding:8px;background:#f7fafc;border:1px solid #e2e8f0;font-size:10px;"><b>الشروط والأحكام</b><br/>{{{{ doc.terms | striptags }}}}</div>{{% endif %}}
<table class="lfa-table">
<thead><tr><th>#</th><th>البند</th><th>الوصف</th><th>الكمية</th><th>سعر الوحدة</th><th>قالب الضريبة</th><th>المبلغ</th></tr></thead>
<tbody>
{{% for it in doc.items %}}
<tr>
<td>{{{{ loop.index }}}}</td>
<td>{{{{ it.item_code or "" }}}}</td>
<td>{{{{ it.description or "" }}}}</td>
<td>{{{{ it.qty }}}}</td>
<td>{{{{ frappe.utils.fmt_money(it.rate or 0, currency=doc.currency) }}}}</td>
<td>{{{{ it.item_tax_template or "—" }}}}</td>
<td>{{{{ frappe.utils.fmt_money(it.amount or 0, currency=doc.currency) }}}}</td>
</tr>
{{% endfor %}}
</tbody>
</table>
<table class="lfa-totals">
<tr><td>المجموع قبل الضريبة</td><td>{{{{ frappe.utils.fmt_money(doc.net_total or 0, currency=doc.currency) }}}}</td></tr>
{{% if doc.total_taxes_and_charges %}}<tr><td>إجمالي الضريبة</td><td>{{{{ frappe.utils.fmt_money(doc.total_taxes_and_charges or 0, currency=doc.currency) }}}}</td></tr>{{% endif %}}
<tr><td>الإجمالي الكلي</td><td>{{{{ frappe.utils.fmt_money(doc.grand_total or 0, currency=doc.currency) }}}}</td></tr>
</table>
{{% if doc.in_words %}}<div style="margin-top:10px;font-style:italic;font-size:11px;">{{{{ doc.in_words }}}}</div>{{% endif %}}
<div class="lfa-footer-note">{{{{ doc.name }}}} — {{{{ frappe.utils.nowdate() }}}}</div>
</div>"""

PE_BLOCK = rf"""<style>{BASE_CSS}</style>
<div class="lfa-print rtl">
<div class="lfa-letterhead">{LETTERHEAD}</div>
<div class="lfa-doc-title">__PE_TITLE__</div>
<div class="lfa-meta-grid">
<div class="lfa-meta-row"><div class="lfa-meta-cell"><b>رقم السند</b><br/>{{{{ doc.name }}}}</div><div class="lfa-meta-cell"><b>التاريخ</b><br/>{{{{ frappe.utils.formatdate(doc.posting_date) }}}}</div></div>
<div class="lfa-meta-row"><div class="lfa-meta-cell"><b>نوع الدفع</b><br/>{{{{ doc.payment_type }}}}</div><div class="lfa-meta-cell"><b>طريقة الدفع</b><br/>{{{{ doc.mode_of_payment or "—" }}}}</div></div>
<div class="lfa-meta-row"><div class="lfa-meta-cell"><b>نوع الطرف</b><br/>{{{{ doc.party_type }}}}</div><div class="lfa-meta-cell"><b>الطرف</b><br/>{{{{ doc.party_name or doc.party }}}}</div></div>
<div class="lfa-meta-row"><div class="lfa-meta-cell"><b>من حساب</b><br/>{{{{ doc.paid_from or "—" }}}}</div><div class="lfa-meta-cell"><b>إلى حساب</b><br/>{{{{ doc.paid_to or "—" }}}}</div></div>
<div class="lfa-meta-row"><div class="lfa-meta-cell"><b>المبلغ المدفوع</b><br/>{{{{ frappe.utils.fmt_money(doc.paid_amount or 0, currency=doc.paid_from_account_currency or doc.company_currency) }}}}</div><div class="lfa-meta-cell"><b>المبلغ المستلم</b><br/>{{{{ frappe.utils.fmt_money(doc.received_amount or 0, currency=doc.paid_to_account_currency or doc.company_currency) }}}}</div></div>
{{% if doc.custom_matter %}}<div class="lfa-meta-row"><div class="lfa-meta-full"><b>المادة</b><br/>{{{{ doc.custom_matter }}}}</div></div>{{% endif %}}
{{% if doc.remarks %}}<div class="lfa-meta-row"><div class="lfa-meta-full"><b>ملاحظات</b><br/>{{{{ doc.remarks }}}}</div></div>{{% endif %}}
</div>
{{% if doc.references %}}
<table class="lfa-table">
<thead><tr><th>#</th><th>نوع المرجع</th><th>المرجع</th><th>المبلغ المخصص</th></tr></thead>
<tbody>
{{% for r in doc.references %}}
<tr>
<td>{{{{ loop.index }}}}</td>
<td>{{{{ r.reference_doctype or "" }}}}</td>
<td>{{{{ r.reference_name or "" }}}}</td>
<td>{{{{ frappe.utils.fmt_money(r.allocated_amount or 0, currency=doc.company_currency) }}}}</td>
</tr>
{{% endfor %}}
</tbody>
</table>
{{% endif %}}
<div class="lfa-footer-note">{{{{ doc.name }}}} — {{{{ frappe.utils.nowdate() }}}}</div>
</div>"""


def main():
    out = []
    for name, dt, html in [
        ("Case Sessions Print", "Case", case_html("تقرير جدول الجلسات — الجلسات الحالية", "doc.case_sessions", True)),
        ("Case History Print", "Case", case_html("تقرير جدول الجلسات — السجل التاريخي", "doc.case_history", False)),
        ("Case Sessions Report Print", "Case", case_html("تقرير الجلسات — نسخة مطبوعة", "doc.case_sessions", True)),
        ("Case History Report Print", "Case", case_html("تقرير السجل — نسخة مطبوعة", "doc.case_history", False)),
        ("Sales Invoice - فاتورة رسوم دعوى", "Sales Invoice", SI_BLOCK.replace("__SI_TITLE__", "فاتورة رسوم دعوى")),
        ("Sales Invoice - فاتورة اتعاب", "Sales Invoice", SI_BLOCK.replace("__SI_TITLE__", "فاتورة اتعاب")),
        ("Payment Entry - استلام مبلغ عن فاتورة رسوم دعوى", "Payment Entry", PE_BLOCK.replace("__PE_TITLE__", "سند قبض / دفع — رسوم دعوى")),
        ("Payment Entry - استلام مبلغ عن فاتورة اتعاب", "Payment Entry", PE_BLOCK.replace("__PE_TITLE__", "سند قبض / دفع — اتعاب")),
    ]:
        out.append(
            {
                "creation": "2026-05-10 12:00:00.000000",
                "custom_format": 1,
                "default_print_language": None,
                "disabled": 0,
                "doc_type": dt,
                "docstatus": 0,
                "doctype": "Print Format",
                "font": "Default",
                "idx": 0,
                "line_breaks": 0,
                "modified": "2026-05-10 14:30:00.000000",
                "modified_by": "Administrator",
                "module": "Lawfirm Addons",
                "name": name,
                "owner": "Administrator",
                "print_format_builder": 0,
                "print_format_type": "Jinja",
                "raw_printing": 0,
                "show_section_headings": 0,
                "standard": "No",
                "html": html,
                "css": BASE_CSS.strip(),
            }
        )
    path = HERE / "print_format.json"
    path.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print("Wrote", path)


if __name__ == "__main__":
    main()
