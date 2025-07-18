# Copyright (c) 2025, future_support and contributors
# For license information, please see license.txt

import frappe


def execute(filters=None):
	if not filters:
		filters = {}

	columns = [
		{
			"fieldname": "posting_date",
			"label": "Date",
			"fieldtype": "Date",
			"width": 120
		},
		{
			"fieldname": "owner",
			"label": "User",
			"fieldtype": "Data",
			"width": 150
		},
		{
			"fieldname": "name",
			"label": "Invoice_No",
			"fieldtype": "Link",
			"options": "Sales Invoice",
			"width": 200
		},
		{
			"fieldname": "due_date",
			"label": "due_date",
			"fieldtype": "Date",
			"width": 120
		},
		{
			"fieldname": "customer_name",
			"label": "customer_name",
			"fieldtype": "Link",
			"options": "Customer",
			"width": 200
		},
		{
			"fieldname": "tax_id",
			"label": "tax_id",
			"fieldtype": "Data",
			"width": 165
		},
		{
			"fieldname": "branch",
			"label": "branch",
			"fieldtype": "Link",
			"options": "Branch",
			"width": 100
		},
		{
			"fieldname": "status",
			"label": "Status",
			"fieldtype": "Data",
			"width": 100
		},
		{
			"fieldname": "total_taxes_and_charges",
			"label": "total_taxes",
			"fieldtype": "Currency",
			"width": 140
		}
	]

	# Fetch filters
	from_date = filters.get("from_date")
	to_date = filters.get("to_date")
	status = filters.get("status")
	branch = filters.get("branch")
	customer_name = filters.get("customer_name")


	# SQL query
	query = """
		SELECT
			`tabSales Invoice`.posting_date,
			`tabSales Invoice`.owner,
			`tabSales Invoice`.name,
			`tabSales Invoice`.due_date,
			`tabSales Invoice`.customer_name,
			`tabSales Invoice`.tax_id,
			`tabSales Invoice`.branch,
			`tabSales Invoice`.status,
			SUM(`tabSales Invoice`.`total_taxes_and_charges`) AS total_taxes_and_charges
		FROM
			`tabSales Invoice`
	"""

	# Collect WHERE conditions
	where_conditions = []
	params = {}

	# Apply date range filter for posting_date
	if from_date and to_date:
		where_conditions.append("`tabSales Invoice`.posting_date BETWEEN %(from_date)s AND %(to_date)s")
		params["from_date"] = from_date
		params["to_date"] = to_date
	elif from_date:
		where_conditions.append("`tabSales Invoice`.posting_date >= %(from_date)s")
		params["from_date"] = from_date
	elif to_date:
		where_conditions.append("`tabSales Invoice`.posting_date <= %(to_date)s")
		params["to_date"] = to_date

	if customer_name:
		where_conditions.append("`tabSales Invoice`.customer_name = %(customer_name)s")
		params["customer_name"] = customer_name

	if branch:
		where_conditions.append("`tabSales Invoice`.branch IN %(branch)s")
		params["branch"] = tuple(filters["branch"])

	if status:
		where_conditions.append("`tabSales Invoice`.status IN %(status)s")
		params["status"] = tuple(filters["status"])


	# Add WHERE clause if there are any conditions
	if where_conditions:
		query += " WHERE " + " AND ".join(where_conditions)

	query += """
		GROUP BY
			`tabSales Invoice`.posting_date,
			`tabSales Invoice`.owner,
			`tabSales Invoice`.name,
			`tabSales Invoice`.due_date,
			`tabSales Invoice`.customer_name,
			`tabSales Invoice`.tax_id,
			`tabSales Invoice`.branch,
			`tabSales Invoice`.status
	"""

	# Execute the query
	mydata = frappe.db.sql(query, params, as_dict=True)

	# Return columns and data
	return columns, mydata


