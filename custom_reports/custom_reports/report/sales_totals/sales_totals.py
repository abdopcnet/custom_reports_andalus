# Copyright (c) 2025, future_support and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.query_builder.functions import Sum


def execute(filters=None):
	if not filters:
		filters = frappe._dict({})

	columns = get_columns()
	data = get_data(filters)
	return columns, data


def get_columns():
	return [
		{
			"fieldname": "branch",
			"label": _("الفرع"),
			"fieldtype": "Link",
			"options": "Branch",
			"width": 150,
		},
		{
			"fieldname": "status",
			"label": _("الحالة"),
			"fieldtype": "Select",
			"width": 150,
		},
		{
			"fieldname": "net_total",
			"label": _("صافي الإجمالي"),
			"fieldtype": "Currency",
			"width": 150,
		},
		{
			"fieldname": "total_taxes_and_charges",
			"label": _("إجمالي الضرائب"),
			"fieldtype": "Currency",
			"width": 150,
		},
		{
			"fieldname": "discount_amount",
			"label": _("مبلغ الخصم"),
			"fieldtype": "Currency",
			"width": 150,
		},
		{
			"fieldname": "grand_total",
			"label": _("المجموع الكلي"),
			"fieldtype": "Currency",
			"width": 150,
		},
	]


def get_data(filters):
	si = frappe.qb.DocType("Sales Invoice")
	query = (
		frappe.qb.from_(si)
		.select(
			si.branch,
			si.status,
			Sum(si.net_total).as_("net_total"),
			Sum(si.total_taxes_and_charges).as_("total_taxes_and_charges"),
			Sum(si.discount_amount).as_("discount_amount"),
			Sum(si.grand_total).as_("grand_total"),
		)
		.where(si.docstatus == 1)
		.where(si.status.notin(["Cancelled", "Draft"]))
		.groupby(si.branch, si.status)
	)

	query = get_conditions(filters, query, si)

	return query.run(as_dict=True)


def get_conditions(filters, query, si):
	if filters.get("from_date") and filters.get("to_date"):
		query = query.where(si.posting_date.between(filters.get("from_date"), filters.get("to_date")))

	if filters.get("branch"):
		branch_list = filters.get("branch")
		if isinstance(branch_list, list) and branch_list:
			query = query.where(si.branch.isin(branch_list))

	if filters.get("status"):
		status_list = filters.get("status")
		if isinstance(status_list, list) and status_list:
			query = query.where(si.status.isin(status_list))

	return query