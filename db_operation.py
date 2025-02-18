from app import app, db
from models import User, Order
from sqlalchemy import text
import pandas as pd
from tabulate import tabulate

def create_tables():
    with app.app_context():
        db.create_all()
        print("Database tables created successfully")

def create_user_dataframe():
    with app.app_context():
        users = User.query.all()
        user_data = []
        
        if users:
            for user in users:
                user_data.append({
                    "ID": user.id,
                    "Full Name": f"{user.first_name} {user.last_name}",
                    "Email": user.email,
                    "Phone": user.phone
                })
            user_df = pd.DataFrame(user_data)
            return user_df
        else:
            print("No users found in the database.")
            return pd.DataFrame()  # Return empty DataFrame if no users

def create_order_dataframe():
    with app.app_context():
        orders = Order.query.all()
        order_data = []
        
        if orders:
            for order in orders:
                order_items = ', '.join([f"{item.product_name}: {item.quantity} x ₹{item.price:.2f}" for item in order.items])
                order_data.append({
                    "Order ID": order.id,
                    "User ID": order.user_id,
                    "Total Amount": f"₹{order.total_amount:.2f}",
                    "Shipping Address": order.shipping_address,
                    "Payment Method": order.payment_method,
                    "Status": order.status,
                    "Created At": order.created_at.strftime("%Y-%m-%d %H:%M:%S"),  # Improved date format
                    "Order Items": order_items
                })
            order_df = pd.DataFrame(order_data)
            return order_df
        else:
            print("No orders found in the database.")
            return pd.DataFrame()  # Return empty DataFrame if no orders

def print_user_dataframe(user_df):
    if not user_df.empty:
        print("\nUser DataFrame:")
        print(tabulate(user_df, headers='keys', tablefmt='grid', showindex=False))
    else:
        print("No users found in the database.")

def print_order_dataframe(order_df):
    if not order_df.empty:
        # Highlight monetary values and format for better readability
        order_df["Total Amount"] = order_df["Total Amount"].apply(lambda x: f"\033[92m{x}\033[0m")  # Green text for amounts
        print("\nOrder DataFrame:")
        print(tabulate(order_df, headers='keys', tablefmt='grid', showindex=False))
    else:
        print("No orders found in the database.")

def clear_database():
    with app.app_context():
        # Get all table names
        inspector = db.inspect(db.engine)
        table_names = inspector.get_table_names()
        
        # Drop all tables
        with db.engine.connect() as connection:
            for table in table_names:
                connection.execute(text(f"DROP TABLE IF EXISTS {table}"))
            connection.commit()
        
        # Recreate all tables
        db.create_all()
        
        print("All data cleared and tables recreated!")

if __name__ == "__main__":
    # Uncomment the function you want to run
    # create_tables()
    #clear_database()
    
    user_df = create_user_dataframe()
    print_user_dataframe(user_df)

    order_df = create_order_dataframe()
    print_order_dataframe(order_df)
