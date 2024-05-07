from models import Session, Customer, Product, customer_product_association

# Start a session to query the database
session = Session()

# Perform a query that joins Customer and Product through the association table
query = session.query(Customer, Product).\
    join(customer_product_association, Customer.id == customer_product_association.c.customer_id).\
    join(Product, Product.id == customer_product_association.c.product_id)

# Fetch the results
results = query.all()

for customer, product in results:
    print(f"Customer: {customer.name}, Product: {product.name}")

# Close the session after operations
session.close()
