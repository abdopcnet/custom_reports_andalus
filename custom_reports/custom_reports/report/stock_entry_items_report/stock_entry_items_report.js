// Copyright (c) 2025, future_support and contributors
// For license information, please see license.txt

frappe.query_reports["Stock Entry Items Report"] = {
    "filters": [
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
            "fieldname": "from_date",
            "label": "From Date",
            "fieldtype": "Date"
        },
        {
            "fieldname": "to_date",
            "label": "To Date",
            "fieldtype": "Date"
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
            "fieldtype": "Link",
            "options": "Item"
        },
        {
            "fieldname": "item_group",
            "label": "Item Group",
            "fieldtype": "Link",
            "options": "Item Group"
        }
    ]
}