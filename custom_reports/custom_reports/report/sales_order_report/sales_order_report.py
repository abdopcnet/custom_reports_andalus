# Copyright (c) 2025, future_support and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.utils import date_diff, flt, getdate, get_url


# Main report execution function
def execute(filters=None):
	if not filters:
		filters = frappe._dict({})

	validate_filters(filters)
	columns = get_columns()
	conditions = get_conditions(filters)
	data = get_data(conditions, filters)

	if not data:
		frappe.msgprint(_("لا توجد سجلات"))
		return [], []

	# Get payment references separately to avoid incorrect sums
	all_invoices = set()
	for row in data:
		if row.get("sales_invoice_reference"):
			all_invoices.update(row.sales_invoice_reference.split(", "))

	payment_map = get_payment_references(list(all_invoices))

	# Post-process data to add HTML links and payment status
	for row in data:
		# Create attach link
		if row.get("custom_attach"):
			row.custom_attach = f'<a href="{get_url(row.custom_attach)}" target="_blank">{_("عرض الصورة")}</a>'

		# Create links for invoices
		if row.get("sales_invoice_reference"):
			invoices = row.sales_invoice_reference.split(", ")
			links = [f'<a href="/app/sales-invoice/{inv}">{inv}</a>' for inv in invoices]
			row.sales_invoice_reference = ", ".join(links)

		# Add payment references to the row
		row.payment_entry_reference = ""
		if row.get("sales_invoice_reference"):
			invoices_in_row = row.sales_invoice_reference.split(", ")
			payments = set()
			for inv_link in invoices_in_row:
				inv = inv_link.split(">")[1].split("<")[0] # Extract invoice name from link
				if inv in payment_map:
					payments.update(payment_map[inv].split(", "))
			
			payment_links = [f'<a href="/app/payment-entry/{pe}">{pe}</a>' for pe in sorted(list(payments))]
			row.payment_entry_reference = ", ".join(payment_links)

		# Create payment status indicator
		outstanding = row.get("outstanding_amount", 0)
		advance = row.get("advance_paid", 0)

		if outstanding <= 0:
			# Paid
			row.payment_status_indicator = '<div style="text-align: center;"><i class="fa fa-check-circle" style="font-size: 1.2em; color: green;"></i></div>'
		elif advance > 0 and outstanding > 0:
			# Partially Paid
			row.payment_status_indicator = '<div style="text-align: center;"><i class="fa fa-exclamation-circle" style="font-size: 1.2em; color: orange;"></i></div>'
		else:  # Not Paid
			row.payment_status_indicator = '<div style="text-align: center;"><i class="fa fa-times-circle" style="font-size: 1.2em; color: red;"></i></div>'

	return columns, data


# Validate date filters
def validate_filters(filters):
	from_date, to_date = filters.get("from_date"), filters.get("to_date")
	if not from_date or not to_date:
		frappe.throw(_("من تاريخ وإلى تاريخ مطلوبان"))
	if date_diff(to_date, from_date) < 0:
		frappe.throw(_("تاريخ النهاية لا يمكن أن يكون قبل تاريخ البداية"))


# Define report columns
def get_columns():
	return [
		{
			"fieldname": "date",
			"label": _("التاريخ"),
			"fieldtype": "Date",
			"width": 120,
		},
		{
			"fieldname": "sales_order",
			"label": _("رقم الطلب"),
			"fieldtype": "Link",
			"options": "Sales Order",
			"width": 150,
		},
		{
			"fieldname": "delivery_date",
			"label": _("تاريخ التسليم"),
			"fieldtype": "Date",
			"width": 120,
		},
		{
			"fieldname": "status",
			"label": _("الحالة"),
			"fieldtype": "Data",
			"width": 150,
		},
		{
			"fieldname": "payment_status_indicator",
			"label": _("حالة الدفع"),
			"fieldtype": "HTML",
			"width": 100,
		},
		{
			"fieldname": "customer",
			"label": _("العميل"),
			"fieldtype": "Link",
			"options": "Customer",
			"width": 150,
		},
		{
			"fieldname": "contact_mobile",
			"label": _("الموبايل"),
			"fieldtype": "Data",
			"width": 120,
		},
		{
			"fieldname": "custom_order_no",
			"label": _("امر التصنيع الداخلي"),
			"fieldtype": "Data",
			"width": 180,
		},
		{
			"fieldname": "custom_attach",
			"label": _("صورة الطلب"),
			"fieldtype": "HTML",
			"width": 150,
		},
		{
			"fieldname": "total_amount",
			"label": _("الاجمالي"),
			"fieldtype": "Currency",
			"width": 120,
			"options": "Company:company:default_currency",
		},
		{
			"fieldname": "discount_amount",
			"label": _("مبلغ الخصم"),
			"fieldtype": "Currency",
			"width": 120,
			"options": "Company:company:default_currency",
		},
		{
			"fieldname": "billed_amount",
			"label": _("اجمالي المفوتر"),
			"fieldtype": "Currency",
			"width": 120,
			"options": "Company:company:default_currency",
		},
		{
			"fieldname": "pending_amount",
			"label": _("اجمالي غير المفوتر"),
			"fieldtype": "Currency",
			"width": 120,
			"options": "Company:company:default_currency",
		},
		{
			"fieldname": "advance_paid",
			"label": _("المدفوع مقدماً"),
			"fieldtype": "Currency",
			"width": 120,
			"options": "Company:company:default_currency",
		},
		{
			"fieldname": "outstanding_amount",
			"label": _("المتبقي"),
			"fieldtype": "Currency",
			"width": 120,
			"options": "Company:company:default_currency",
		},
		{
			"fieldname": "delay_days",
			"label": _("أيام التأخير"),
			"fieldtype": "Int",
			"width": 120,
		},
		{
			"fieldname": "sales_invoice_reference",
			"label": _("الفاتورة"),
			"fieldtype": "HTML",
			"width": 180,
		},
		{
			"fieldname": "payment_entry_reference",
			"label": _("المحصل"),
			"fieldtype": "HTML",
			"width": 180,
		},
	]


# Build SQL conditions from filters
def get_conditions(filters):
	conditions = ""
	if filters.get("from_date") and filters.get("to_date"):
		conditions += " AND `tabSales Order`.transaction_date BETWEEN %(from_date)s AND %(to_date)s"

	if filters.get("company"):
		conditions += " AND `tabSales Order`.company = %(company)s"

	if filters.get("branch"):
		conditions += " AND `tabSales Order`.branch = %(branch)s"

	if filters.get("status"):
		conditions += " AND `tabSales Order`.status IN %(status)s"

	return conditions


# Fetch main data from the database
def get_data(conditions, filters):
	data = frappe.db.sql(
		f"""
		SELECT
			`tabSales Order`.transaction_date AS date,
			`tabSales Order`.name AS sales_order,
			`tabSales Order`.delivery_date,
			`tabSales Order`.status,
			`tabSales Order`.customer,
			`tabSales Order`.contact_mobile,
			`tabSales Order`.custom_order_no,
			`tabSales Order`.custom_attach,
			`tabSales Order`.base_grand_total AS total_amount,
			`tabSales Order`.discount_amount,
			SUM(`tabSales Order Item`.billed_amt * IFNULL(`tabSales Order`.conversion_rate, 1)) AS billed_amount,
			SUM(`tabSales Order Item`.base_amount - (`tabSales Order Item`.billed_amt * IFNULL(`tabSales Order`.conversion_rate, 1))) AS pending_amount,
			`tabSales Order`.advance_paid,
			(`tabSales Order`.base_grand_total - `tabSales Order`.advance_paid) AS outstanding_amount,
			CASE
				WHEN `tabSales Order`.delivery_date < CURDATE() AND `tabSales Order`.status NOT IN ('Completed', 'Closed', 'Cancelled')
				THEN DATEDIFF(CURDATE(), `tabSales Order`.delivery_date)
				ELSE 0
			END AS delay_days,
			GROUP_CONCAT(DISTINCT `tabSales Invoice Item`.parent SEPARATOR ', ') as sales_invoice_reference
		FROM
			`tabSales Order`
		LEFT JOIN `tabSales Order Item` ON `tabSales Order Item`.parent = `tabSales Order`.name
		LEFT JOIN `tabSales Invoice Item` ON `tabSales Invoice Item`.so_detail = `tabSales Order Item`.name AND `tabSales Invoice Item`.docstatus = 1
		WHERE
			`tabSales Order`.docstatus = 1
			AND `tabSales Order`.status NOT IN ('Stopped', 'On Hold')
			{conditions}
		GROUP BY
			`tabSales Order`.name
		ORDER BY
			`tabSales Order`.transaction_date DESC
	""",
		filters,
		as_dict=1,
	)
	return data


# Fetch payment entry references for given invoices
def get_payment_references(invoice_list):
	if not invoice_list:
		return {}

	payment_map = {}
	references = frappe.get_all(
		"Payment Entry Reference",
		filters={"reference_doctype": "Sales Invoice", "reference_name": ("in", invoice_list)},
		fields=["reference_name", "parent"],
	)

	for ref in references:
		if ref.reference_name not in payment_map:
			payment_map[ref.reference_name] = set()
		payment_map[ref.reference_name].add(ref.parent)

	for invoice, payments in payment_map.items():
		payment_map[invoice] = ", ".join(sorted(list(payments)))

	return payment_map
