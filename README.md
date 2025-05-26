## Library Management

# 📚  Library Management Sysyem


This is a custom Frappe app designed to manage a library system. It allows you to register library members, issue and return books, track outstanding rental fees, and manage book inventory.

#### User ===> Administartor  
#### Password ===> Amos

#### "Password Remains the same "
---

## 🚀 Features

- Register Library Members (auto-creates a Customer)
- Issue books to members and calculate rent
- Return books, accept payments, and update balances
- Prevent issuing if outstanding balance > 500 KSH or book not available
- Automatically update book quantity
- Track overpayments and show refunds or carry-forward balances
- Shows outstanding fee directly in Library Member list view

![Member](/library_management//screenshot/member.png)

---

## 📦 Installation

1. Clone the app into your Frappe bench:
    ```bash
    cd ~/library-bench/apps
    git clone https://git@github.com:Kiprotich-Amos/Library-Management.git
    ```

2. Install the app:
    ```bash
    bench --site library.local install-app library_management
    ```

3. Run migrations:
    ```bash
    bench --site library.local migrate
    ```

---

## 🧑‍💻 Usage
![Dashboard](/library_management/screenshot/Library.png)


### 📖 Issue Book
- Go to **Transaction**
- Set `Transaction Type` to `Issue`
- Select a `Book` and `Member`
- Set `Issue Date` and `Return Date`
- Rent fee is auto-calculated and added to member’s outstanding

### 🔁 Return Book
- Set `Transaction Type` to `Return`
- Select `Book` and `Member`
- Enter `Amount Paid`
- System updates outstanding balance, handles overpayment, and increases book quantity

Transaction Issue && Return 

![Transaction](/library_management//screenshot/transaction.png)

Invoice Code 
![code](/library_management/screenshot/Invoice%20Code.png)


the code also register New members and create them automaticaly as customers here 
this is how
![customer](/library_management/screenshot/Customer.png)
---

#### License

MIT