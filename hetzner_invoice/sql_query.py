search_duplicate = (
    "SELECT * FROM invoices WHERE type = %s AND description = %s AND id "
    "= %s AND invoice_nr = %s "
)
update_record = (
    "UPDATE invoices SET start_date = %s, end_date = %s, quantity = %s, price= %s, last_updated "
    "= %s WHERE type = %s AND description = %s AND id "
    "= %s AND invoice_nr = % "
)
insert_record = (
    "INSERT INTO invoices "
    "(type, description, start_date, end_date, quantity, unit_price, price, cores, memory, disk, "
    "price_monthly, role, id, environment, invoice_nr, last_updated) "
    "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
)
