from textual.widgets import Input, Button, Static, Select, Label
from textual.containers import Container, Horizontal, Vertical
from textual.screen import ModalScreen
from ..database import SessionLocal, Transaction, TransactionType, AccountType, Account
import yaml
import os
import logging

class AddAccountModal(ModalScreen):
    """Modal for adding a new account."""
    
    def compose(self) -> None:
        with Container(id="dialog", classes="account-dialog"):
            yield Static("💳 Add New Account", id="title")
            with Vertical(classes="modal-form"):
                yield Label("Account Name:")
                yield Input(placeholder="e.g., Main Checking", id="account-name")
                yield Label("Account Type:")
                yield Select(
                    [("Cash", AccountType.CASH), 
                     ("Bank Account", AccountType.BANK_ACCOUNT),
                     ("Credit Card", AccountType.CREDIT_CARD),
                     ("Savings", AccountType.SAVINGS)],
                    prompt="Select account type...",
                    id="account-type"
                )
                yield Label("Starting Balance:")
                yield Input(placeholder="0.00", id="starting-balance")
            with Horizontal(id="button-row"):
                yield Button("Add Account", variant="primary", id="add-account")
                yield Button("Cancel", variant="default", id="cancel")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "add-account":
            name = self.query_one("#account-name", Input).value.strip()
            account_type = self.query_one("#account-type", Select).value
            balance_str = self.query_one("#starting-balance", Input).value.strip()
            
            # Validation
            if not name:
                self.notify("Account name is required", severity="error")
                return
                
            if len(name) > 100:
                self.notify("Account name too long (100 char max)", severity="error")
                return
                
            if not account_type:
                self.notify("Please select an account type", severity="error")
                return
            
            try:
                balance = float(balance_str) if balance_str else 0.0
                
                # Validate balance range
                if balance > 999999999 or balance < -999999999:
                    self.notify("Starting balance too large (max ±$999M)", severity="error")
                    return
                    
                # Check for duplicate account names
                db = SessionLocal()
                existing_account = db.query(Account).filter(Account.name == name).first()
                if existing_account:
                    db.close()
                    self.notify("Account name already exists", severity="error")
                    return
                
                new_account = Account(
                    name=name,
                    account_type=account_type,
                    starting_balance=balance
                )
                db.add(new_account)
                db.commit()
                db.close()
                self.app.refresh_data()
                self.notify(f"Account '{name}' created successfully", severity="information")
                self.dismiss()
                
            except ValueError:
                self.notify("Invalid balance format. Please enter a valid number", severity="error")
            except Exception as e:
                self.notify("Failed to create account. Please try again", severity="error")
                
        elif event.button.id == "cancel":
            self.dismiss()

class AddTransactionModal(ModalScreen):
    """Modal for adding a new transaction."""

    def compose(self) -> None:
        with Container(id="dialog"):
            yield Static("📝 Add New Transaction", id="title")
            with Vertical(classes="modal-form"):
                yield Label("Transaction Type:")
                yield Select(
                    [("💰 Income", TransactionType.INCOME),
                     ("💸 Expense", TransactionType.EXPENSE)],
                    prompt="Select transaction type...",
                    id="transaction-type"
                )
                yield Label("Account:")
                yield Select([], prompt="Select account...", id="account-select")
                yield Label("Description:")
                yield Input(placeholder="e.g., Grocery shopping", id="description")
                yield Label("Amount:")
                yield Input(placeholder="0.00", id="amount")
                yield Label("Category:")
                yield Select([], prompt="Select category...", id="category-select")
            with Horizontal(id="button-row"):
                yield Button("Add Transaction", variant="primary", id="add-transaction")
                yield Button("Cancel", variant="default", id="cancel")

    def on_mount(self) -> None:
        # Load accounts for the select dropdown
        db = SessionLocal()
        accounts = db.query(Account).all()
        account_options = [(account.name, account.id) for account in accounts]
        account_select = self.query_one("#account-select", Select)
        account_select.set_options(account_options)
        
        # Load categories from YAML file
        self.load_categories()
        db.close()
    
    def load_categories(self) -> None:
        """Load categories from the YAML file."""
        try:
            # Get the directory of the current file
            current_dir = os.path.dirname(os.path.abspath(__file__))
            categories_file = os.path.join(current_dir, "..", "categories.yaml")
            
            if os.path.exists(categories_file):
                with open(categories_file, 'r') as file:
                    categories_data = yaml.safe_load(file)
                
                # Flatten categories and subcategories into a single list
                category_options = []
                for category in categories_data:
                    category_options.append((category['name'], category['name']))
                    if 'subcategories' in category:
                        for subcategory in category['subcategories']:
                            category_options.append((f"{category['name']} > {subcategory['name']}", f"{category['name']} > {subcategory['name']}"))
                
                self.query_one("#category-select", Select).set_options(category_options)
            else:
                # Fallback to basic categories if file doesn't exist
                basic_categories = [
                    ("Food", "Food"),
                    ("Transport", "Transport"),
                    ("Shopping", "Shopping"),
                    ("Income", "Income"),
                    ("Other", "Other")
                ]
                self.query_one("#category-select", Select).set_options(basic_categories)
        except Exception as e:
            # Fallback to basic categories if there's an error
            basic_categories = [
                ("Food", "Food"),
                ("Transport", "Transport"),
                ("Shopping", "Shopping"),
                ("Income", "Income"),
                ("Other", "Other")
            ]
            self.query_one("#category-select", Select).set_options(basic_categories)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "add-transaction":
            transaction_type = self.query_one("#transaction-type", Select).value
            account_id = self.query_one("#account-select", Select).value
            description = self.query_one("#description", Input).value.strip()
            amount_str = self.query_one("#amount", Input).value.strip()
            category = self.query_one("#category-select", Select).value
            
            # Validation
            if not transaction_type:
                self.notify("Please select a transaction type", severity="error")
                return
                
            if not account_id:
                self.notify("Please select an account", severity="error")
                return
                
            if not description:
                self.notify("Description is required", severity="error")
                return
                
            if len(description) > 200:
                self.notify("Description too long (200 char max)", severity="error")
                return
                
            if not amount_str:
                self.notify("Amount is required", severity="error")
                return
            
            try:
                amount = float(amount_str)
                
                # Validate amount
                if amount <= 0:
                    self.notify("Amount must be greater than zero", severity="error")
                    return
                    
                if amount > 999999999:
                    self.notify("Amount too large (max $999M)", severity="error")
                    return
                
                # Convert Select.BLANK to None for database
                if category == Select.BLANK:
                    category = None
                
                db = SessionLocal()
                new_transaction = Transaction(
                    transaction_type=transaction_type,
                    account_id=account_id,
                    description=description,
                    amount=amount,
                    category=category
                )
                db.add(new_transaction)
                db.commit()
                db.close()
                self.app.refresh_data()
                self.notify("Transaction added successfully", severity="information")
                self.dismiss()
                
            except ValueError:
                self.notify("Invalid amount format. Please enter a valid number", severity="error")
            except Exception as e:
                self.notify("Failed to add transaction. Please try again", severity="error")
                
        elif event.button.id == "cancel":
            self.dismiss()

class TransferModal(ModalScreen):
    """Modal for transferring money between accounts."""

    def compose(self) -> None:
        with Container(id="dialog"):
            yield Static("🔄 Transfer Money", id="title")
            with Vertical(classes="modal-form"):
                yield Label("From Account:")
                yield Select([], prompt="Select source account...", id="from-account-select")
                yield Label("To Account:")
                yield Select([], prompt="Select destination account...", id="to-account-select")
                yield Label("Amount:")
                yield Input(placeholder="0.00", id="transfer-amount")
                yield Label("Description (optional):")
                yield Input(placeholder="e.g., Transfer to savings", id="transfer-description")
            with Horizontal(id="button-row"):
                yield Button("Transfer", variant="primary", id="transfer-money")
                yield Button("Cancel", variant="default", id="cancel")

    def on_mount(self) -> None:
        # Load accounts for both dropdowns
        db = SessionLocal()
        accounts = db.query(Account).all()
        account_options = [(account.name, account.id) for account in accounts]
        
        self.query_one("#from-account-select", Select).set_options(account_options)
        self.query_one("#to-account-select", Select).set_options(account_options)
        
        db.close()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "transfer-money":
            from_account_id = self.query_one("#from-account-select", Select).value
            to_account_id = self.query_one("#to-account-select", Select).value
            amount_str = self.query_one("#transfer-amount", Input).value.strip()
            description = self.query_one("#transfer-description", Input).value.strip()
            
            # Validate inputs
            if not from_account_id:
                self.notify("Please select a source account", severity="error")
                return
                
            if not to_account_id:
                self.notify("Please select a destination account", severity="error")
                return
                
            if not amount_str:
                self.notify("Transfer amount is required", severity="error")
                return
                
            if from_account_id == to_account_id:
                self.notify("Cannot transfer to the same account", severity="error")
                return
            
            # Validate description length if provided
            if description and len(description) > 200:
                self.notify("Description too long (200 char max)", severity="error")
                return
                
            try:
                amount = float(amount_str)
                
                if amount <= 0:
                    self.notify("Transfer amount must be positive", severity="error")
                    return
                    
                if amount > 999999999:
                    self.notify("Transfer amount too large (max $999M)", severity="error")
                    return
                    
                # Set default description if empty
                if not description:
                    description = "Account transfer"
                
                # Perform the transfer
                self.perform_transfer(from_account_id, to_account_id, amount, description)
                
            except ValueError:
                self.notify("Invalid amount format. Please enter a valid number", severity="error")
                
        elif event.button.id == "cancel":
            self.dismiss()
    
    def perform_transfer(self, from_account_id: int, to_account_id: int, amount: float, description: str) -> None:
        """Perform the actual transfer between accounts."""
        db = SessionLocal()
        try:
            # Get account names for description
            from_account = db.query(Account).filter(Account.id == from_account_id).first()
            to_account = db.query(Account).filter(Account.id == to_account_id).first()
            
            if not from_account or not to_account:
                self.notify("One or both accounts not found", severity="error")
                return
            
            # Create two transactions: one expense (from account) and one income (to account)
            # They will be linked via transfer_pair_id
            
            # Transaction 1: Expense from source account
            transfer_out = Transaction(
                transaction_type=TransactionType.TRANSFER,
                account_id=from_account_id,
                description=f"Transfer to {to_account.name}: {description}",
                amount=amount,
                category="Transfer"
            )
            
            # Transaction 2: Income to destination account  
            transfer_in = Transaction(
                transaction_type=TransactionType.TRANSFER,
                account_id=to_account_id,
                description=f"Transfer from {from_account.name}: {description}",
                amount=amount,
                category="Transfer"
            )
            
            # Add both transactions
            db.add(transfer_out)
            db.add(transfer_in)
            db.flush()  # This assigns IDs to the transactions
            
            # Link them together via transfer_pair_id
            transfer_out.transfer_pair_id = transfer_in.id
            transfer_in.transfer_pair_id = transfer_out.id
            
            # Commit the transaction
            db.commit()
            
            # Refresh the main app data
            self.app.refresh_data()
            
            # Close the modal
            self.dismiss()
            
            # Show success message
            self.notify(f"Transferred ${amount:.2f} from {from_account.name} to {to_account.name}", severity="information")
            
        except Exception as e:
            db.rollback()
            # Log the detailed error but show user-friendly message
            logging.error("Transfer operation failed", exc_info=False)
            self.notify("Transfer failed. Please try again", severity="error")
        finally:
            db.close()
