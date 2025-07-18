# Copyright (c) 2025, future_support and contributors
# For license information, please see license.txt

import frappe
from frappe import _, msgprint
from frappe.query_builder.custom import ConstantColumn


def execute(filters=None):
	if not filters:
		filters = frappe._dict({})

	invoice_list = get_invoices(filters)
	columns = get_columns()
	
	if not invoice_list:
		msgprint(_("لا توجد سجلات"))
		return columns, []

	data = get_data(invoice_list)
	
	# Apply integration_status filter if provided
	if filters.get("integration_status"):
		integration_status_list = filters.get("integration_status")
		if isinstance(integration_status_list, list):
			data = [row for row in data if row.get("integration_status") in integration_status_list]

	return columns, data


def get_columns():
	return [
		{
			"fieldname": "posting_date",
			"label": _("التاريخ"),
			"fieldtype": "Date",
			"width": 120
		},
		{
			"fieldname": "owner",
			"label": _("المستخدم"),
			"fieldtype": "Data",
			"width": 150
		},
		{
			"fieldname": "name",
			"label": _("الفاتورة"),
			"fieldtype": "Link",
			"options": "Sales Invoice",
			"width": 200
		},
		{
			"fieldname": "customer_name",
			"label": _("العميل"),
			"fieldtype": "Data",
			"width": 200
		},
		{
			"fieldname": "contact_mobile",
			"label": _("الجوال"),
			"fieldtype": "Data",
			"width": 150
		},
		{
			"fieldname": "custom_vat_registration_number",
			"label": _("الرقم الضريبي"),
			"fieldtype": "Data",
			"width": 180
		},
		{
			"fieldname": "value",
			"label": _("السجل التجاري"),
			"fieldtype": "Data",
			"width": 120
		},
		{
			"fieldname": "branch",
			"label": _("الفرع"),
			"fieldtype": "Link",
			"options": "Branch",
			"width": 120
		},
		{
			"fieldname": "integration_status",
			"label": _("حالة الفاتورة الالكترونية"),
			"fieldtype": "Data",
			"width": 120
		},
		{
			"fieldname": "status",
			"label": _("الحالة"),
			"fieldtype": "Select",
			"width": 120
		},
		{
			"fieldname": "due_date",
			"label": _("تاريخ الاستحقاق"),
			"fieldtype": "Date",
			"width": 120
		},
		{
			"fieldname": "total_qty",
			"label": _("إجمالي الكمية"),
			"fieldtype": "Currency",
			"width": 120
		},
		{
			"fieldname": "total",
			"label": _("الإجمالي"),
			"fieldtype": "Currency",
			"width": 120
		},
		{
			"fieldname": "additional_discount_percentage",
			"label": _("نسبة الخصم"),
			"fieldtype": "Currency",
			"width": 120
		},
		{
			"fieldname": "discount_amount",
			"label": _("مبلغ الخصم"),
			"fieldtype": "Currency",
			"width": 120
		},
		{
			"fieldname": "net_total",
			"label": _("الصافي"),
			"fieldtype": "Currency",
			"width": 120
		},
		{
			"fieldname": "total_taxes_and_charges",
			"label": _("الضرائب"),
			"fieldtype": "Currency",
			"width": 120
		},
		{
			"fieldname": "grand_total",
			"label": _("الإجمالي"),
			"fieldtype": "Currency",
			"width": 120
		},
		{
			"fieldname": "outstanding_amount",
			"label": _("المتبقي"),
			"fieldtype": "Currency",
			"width": 120
		}
	]


def get_invoices(filters):
	"""Get sales invoices using query builder like sales_register.py"""
	si = frappe.qb.DocType("Sales Invoice")
	query = (
		frappe.qb.from_(si)
		.select(
			ConstantColumn("Sales Invoice").as_("doctype"),
			si.name,
			si.posting_date,
			si.customer,
			si.customer_name,
			si.owner,
			si.contact_mobile,
			si.branch,
			si.status,
			si.due_date,
			si.total_qty,
			si.total,
			si.net_total,
			si.total_taxes_and_charges,
			si.grand_total,
			si.discount_amount,
			si.additional_discount_percentage,
			si.outstanding_amount,
			si.company,
		)
		.where(si.docstatus == 1)
		.where(si.status.notin(["Cancelled", "Draft"]))
	)

	query = get_conditions(filters, query, "Sales Invoice")

	from frappe.desk.reportview import build_match_conditions
	query, params = query.walk()
	match_conditions = build_match_conditions("Sales Invoice")

	if match_conditions:
		query += f" AND {match_conditions}"

	query += " ORDER BY posting_date DESC, name DESC"

	return frappe.db.sql(query, params, as_dict=True)


def get_conditions(filters, query, doctype):
	"""Apply filters to query like sales_register.py"""
	parent_doc = frappe.qb.DocType(doctype)
	
	if filters.get("from_date") and filters.get("to_date"):
		query = query.where(parent_doc.posting_date.between(filters.get("from_date"), filters.get("to_date")))
	elif filters.get("from_date"):
		query = query.where(parent_doc.posting_date >= filters.get("from_date"))
	elif filters.get("to_date"):
		query = query.where(parent_doc.posting_date <= filters.get("to_date"))

	if filters.get("customer_name"):
		query = query.where(parent_doc.customer_name == filters.get("customer_name"))

	if filters.get("status"):
		status_list = filters.get("status")
		if isinstance(status_list, list):
			query = query.where(parent_doc.status.isin(status_list))

	if filters.get("branch"):
		branch_list = filters.get("branch")
		if isinstance(branch_list, list):
			query = query.where(parent_doc.branch.isin(branch_list))

	return query


def get_data(invoice_list):
	"""Process invoice data to get additional details"""
	if not invoice_list:
		return []

	# Get customer details
	customers = list(set(d.customer for d in invoice_list))
	customer_details = get_customer_details(customers)
	
	# Get integration status
	integration_status_map = get_integration_status_map([inv.name for inv in invoice_list])

	data = []
	for inv in invoice_list:
		customer_info = customer_details.get(inv.customer, {})
		
		row = {
			"posting_date": inv.posting_date,
			"owner": inv.owner,
			"name": inv.name,
			"customer_name": inv.customer_name,
			"contact_mobile": inv.contact_mobile,
			"custom_vat_registration_number": customer_info.get("custom_vat_registration_number"),
			"value": customer_info.get("commercial_registration_numbers", ""),
			"branch": inv.branch,
			"integration_status": integration_status_map.get(inv.name, ""),
			"status": inv.status,
			"due_date": inv.due_date,
			"total_qty": inv.total_qty,
			"total": inv.total,
			"additional_discount_percentage": inv.additional_discount_percentage,
			"discount_amount": inv.discount_amount,
			"net_total": inv.net_total,
			"total_taxes_and_charges": inv.total_taxes_and_charges,
			"grand_total": inv.grand_total,
			"outstanding_amount": inv.outstanding_amount,
		}
		data.append(row)

	return data


def get_customer_details(customers):
	"""Get customer details including VAT registration and commercial registration numbers"""
	if not customers:
		return {}

	customer_details = {}
	
	# Get basic customer details
	customer_data = frappe.db.sql("""
		SELECT name, custom_vat_registration_number
		FROM `tabCustomer`
		WHERE name IN ({})
	""".format(", ".join(["%s"] * len(customers))), customers, as_dict=True)
	
	for customer in customer_data:
		customer_details[customer.name] = {
			"custom_vat_registration_number": customer.custom_vat_registration_number
		}

	# Get commercial registration numbers
	commercial_reg_data = frappe.db.sql("""
		SELECT parent, GROUP_CONCAT(DISTINCT value SEPARATOR ', ') AS commercial_registration_numbers
		FROM `tabAdditional Buyer IDs`
		WHERE parent IN ({})
		GROUP BY parent
	""".format(", ".join(["%s"] * len(customers))), customers, as_dict=True)
	
	for reg_data in commercial_reg_data:
		if reg_data.parent in customer_details:
			customer_details[reg_data.parent]["commercial_registration_numbers"] = reg_data.commercial_registration_numbers

	return customer_details


def get_integration_status_map(invoice_list):
	"""Get integration status for invoices"""
	if not invoice_list:
		return {}

	integration_data = frappe.db.sql("""
		SELECT sales_invoice, integration_status
		FROM `tabSales Invoice Additional Fields`
		WHERE sales_invoice IN ({})
	""".format(", ".join(["%s"] * len(invoice_list))), invoice_list, as_dict=True)

	integration_status_map = {}
	for data in integration_data:
		integration_status_map[data.sales_invoice] = data.integration_status

	return integration_status_map
