def calculate_average(sales):
    if not sales:
        return 0
    return sum(sales) / len(sales)


def format_sales_data(sales_data):
    formatted_data = []
    for sale in sales_data:
        formatted_data.append(
            {
                "employee": sale.get("employee"),
                "product": sale.get("product"),
                "store": sale.get("store"),
                "amount": sale.get("amount"),
                "date": sale.get("date").isoformat() if sale.get("date") else None,
            }
        )
    return formatted_data


def validate_date_range(start_date, end_date):
    if start_date > end_date:
        raise ValueError("Start date must be before end date.")
    return True
