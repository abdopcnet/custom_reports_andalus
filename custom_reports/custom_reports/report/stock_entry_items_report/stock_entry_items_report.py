import frappe

# Copyright (c) 2025, future_support and contributors
# For license information, please see license.txt
# stock_entry_items_report.py

columns = [
    {
        "fieldname": "parent",
        "label": "Document",
        "fieldtype": "Link",
        "options": "Stock Entry"
    },
    {
        "fieldname": "modified_by",
        "label": "User",
        "fieldtype": "Link",
        "options": "User"
    },
    {
        "fieldname": "modified_date",
        "label": "Modified Date",
        "fieldtype": "Date"
    },
    {
        "fieldname": "actual_qty",
        "label": "Actual Qty",
        "fieldtype": "Float"
    },
    {
        "fieldname": "barcode",
        "label": "Barcode",
        "fieldtype": "Data"
    },
    {
        "fieldname": "s_warehouse",
        "label": "Source Warehouse",
        "fieldtype": "Link",
        "options": "Warehouse"
    },
    {
        "fieldname": "t_warehouse",
        "label": "Target Warehouse",
        "fieldtype": "Link",
        "options": "Warehouse"
    },
    {
        "fieldname": "item_code",
        "label": "Item Code",
        "fieldtype": "Data"
    },
    {
        "fieldname": "item_name",
        "label": "Item Name",
        "fieldtype": "Data"
    },
    {
        "fieldname": "item_group",
        "label": "Item Group",
        "fieldtype": "Link",
        "options": "Item Group"
    },
    {
        "fieldname": "qty",
        "label": "Qty",
        "fieldtype": "Float"
    },
    {
        "fieldname": "transfer_qty",
        "label": "Transfer Qty",
        "fieldtype": "Float"
    },
    {
        "fieldname": "uom",
        "label": "UOM",
        "fieldtype": "Link",
        "options": "UOM"
    },
    {
        "fieldname": "conversion_factor",
        "label": "Conversion Factor",
        "fieldtype": "Float"
    },
    {
        "fieldname": "stock_uom",
        "label": "Stock UOM",
        "fieldtype": "Link",
        "options": "UOM"
    },
    {
        "fieldname": "basic_rate",
        "label": "Basic Rate",
        "fieldtype": "Currency"
    },
    {
        "fieldname": "valuation_rate",
        "label": "Valuation Rate",
        "fieldtype": "Currency"
    },
    {
        "fieldname": "amount",
        "label": "Amount",
        "fieldtype": "Currency"
    }
]

def execute(filters=None):
    # Build the query dynamically
    query = """
        SELECT 
            parent, 
            modified_by, 
            DATE(modified) AS modified_date, 
            actual_qty, 
            barcode, 
            s_warehouse, 
            t_warehouse, 
            item_code, 
            item_name, 
            item_group, 
            qty, 
            transfer_qty, 
            uom, 
            conversion_factor, 
            stock_uom, 
            basic_rate, 
            valuation_rate, 
            amount 
        FROM 
            `tabStock Entry Detail` 
        WHERE 
            parenttype = 'Stock Entry' 
            AND docstatus = 1
    """

    # Initialize filter conditions and parameters
    where_conditions = []
    params = {}

    # Handle filters dynamically
    if filters:
        if filters.get("parent"):
            where_conditions.append("parent = %(parent)s")
            params["parent"] = filters.get("parent")
        if filters.get("modified_by"):
            where_conditions.append("modified_by = %(modified_by)s")
            params["modified_by"] = filters.get("modified_by")
        if filters.get("from_date"):
            where_conditions.append("DATE(modified) >= %(from_date)s")
            params["from_date"] = filters.get("from_date")
        if filters.get("to_date"):
            where_conditions.append("DATE(modified) <= %(to_date)s")
            params["to_date"] = filters.get("to_date")
        if filters.get("s_warehouse"):
            where_conditions.append("s_warehouse = %(s_warehouse)s")
            params["s_warehouse"] = filters.get("s_warehouse")
        if filters.get("t_warehouse"):
            where_conditions.append("t_warehouse = %(t_warehouse)s")
            params["t_warehouse"] = filters.get("t_warehouse")
        if filters.get("item_code"):
            where_conditions.append("item_code = %(item_code)s")
            params["item_code"] = filters.get("item_code")
        if filters.get("item_group"):
            where_conditions.append("item_group = %(item_group)s")
            params["item_group"] = filters.get("item_group")

    # Apply WHERE clause if any conditions exist
    if where_conditions:
        query += " AND " + " AND ".join(where_conditions)

    # Always sort by modified_date ascending
    query += " ORDER BY modified_date ASC"

    # Execute query
    data = frappe.db.sql(query, params, as_dict=True)

    return columns, data
