import datetime
repair_orders = []
TAX_RATE = 0.07  
DEFAULT_DISCOUNT = 0.0

def show_menu():
    print("\n====== FixTrack - Repair Management System ======")
    print("1. Book New Repair Order")
    print("2. Generate Bill")
    print("3. Show All Orders")
    print("4. Exit")

def get_valid_date(prompt):
    while True:
        date_input = input(prompt)
        try:
            return datetime.datetime.strptime(date_input, "%Y-%m-%d").date()
        except ValueError:
            print("Invalid date format. Use YYYY-MM-DD.")

def book_repair_order():
    print("\n--- New Repair Order ---")
    customer = input("Customer Name: ").strip()
    device = input("Device Type (e.g., Phone, Laptop): ").strip()
    issue = input("Issue Description: ").strip()
    due_date = get_valid_date("Due Date (YYYY-MM-DD): ")

    order = {
        "id": len(repair_orders) + 1,
        "customer": customer,
        "device": device,
        "issue": issue,
        "due_date": due_date,
        "status": "Pending",
        "parts": [],
        "repair_fee": 0.0,
    }

    repair_orders.append(order)
    print(f"Repair Order #{order['id']} booked successfully.")

def list_orders():
    if not repair_orders:
        print("\nNo repair orders available.")
        return

    print("\n--- All Repair Orders ---")
    for order in repair_orders:
        print(f"ID: {order['id']}, Customer: {order['customer']}, Device: {order['device']}, Status: {order['status']}, Due: {order['due_date']}")

def generate_bill():
    if not repair_orders:
        print("\nNo orders found.")
        return

    try:
        order_id = int(input("\nEnter Repair Order ID: "))
        order = next(o for o in repair_orders if o["id"] == order_id)
    except (ValueError, StopIteration):
        print("Invalid order ID.")
        return

    if order["status"] == "Completed":
        print("Bill already generated for this order.")
        return

    print(f"\nGenerating bill for {order['customer']} (Device: {order['device']})")

    while True:
        part_name = input("Enter replaced part name (or press Enter to finish): ").strip()
        if not part_name:
            break
        try:
            part_cost = float(input(f"Cost of {part_name}: "))
            order["parts"].append({"name": part_name, "cost": part_cost})
        except ValueError:
            print("Invalid cost entered.")

    try:
        order["repair_fee"] = float(input("Enter repair service fee: "))
    except ValueError:
        print("Invalid repair fee, setting to 0.")
        order["repair_fee"] = 0.0

    try:
        discount = float(input("Enter discount amount (optional, default 0): ") or DEFAULT_DISCOUNT)
    except ValueError:
        discount = DEFAULT_DISCOUNT

    part_total = sum(p["cost"] for p in order["parts"])
    subtotal = part_total + order["repair_fee"]
    tax = subtotal * TAX_RATE
    total = subtotal + tax - discount

    order["status"] = "Completed"

    print("\n========== INVOICE ==========")
    print(f"Order ID: {order['id']}")
    print(f"Customer: {order['customer']}")
    print(f"Device: {order['device']}")
    print(f"Issue: {order['issue']}")
    print(f"Due Date: {order['due_date']}")
    print("\n--- Parts Replaced ---")
    if order["parts"]:
        for part in order["parts"]:
            print(f"{part['name']}: ₹{part['cost']:.2f}")
    else:
        print("No parts replaced.")

    print(f"\nRepair Fee: ₹{order['repair_fee']:.2f}")
    print(f"Subtotal: ₹{subtotal:.2f}")
    print(f"Tax (7%): ₹{tax:.2f}")
    print(f"Discount: ₹{discount:.2f}")
    print(f"TOTAL: ₹{total:.2f}")
    print("=============================")

def main():
    while True:
        show_menu()
        choice = input("Enter your choice (1-4): ").strip()
        if choice == "1":
            book_repair_order()
        elif choice == "2":
            generate_bill()
        elif choice == "3":
            list_orders()
        elif choice == "4":
            print("Exiting FixTrack. Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()