
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, DataTable, Static
from textual.containers import Container, Horizontal, Vertical, Grid
from textual.message import Message
from .database import SessionLocal, Transaction, TransactionType, Account
from .components.modals import AddAccountModal, AddTransactionModal, TransferModal
from .components.calendar import CalendarComponent
from .components.categories import CategoryManager
from .components.insights import InsightsGenerator
from textual import work
from pathlib import Path




class InsightsReady(Message):
    """Message sent when insights are ready to be displayed."""
    def __init__(self, content: str):
        super().__init__()
        self.content = content

class ExpenseApp(App):
    # Use Tokyo Night theme for modern styling
    BINDINGS = [
        ("a", "add_account", "Add Account"),
        ("t", "add_transaction", "Add Transaction"),
        ("shift+t", "transfer_money", "Transfer"),
        ("ctrl+t", "toggle_theme", "Theme"),
        ("q", "quit", "Quit"),
        ("left", "expand_accounts", "Expand Accounts"),
        ("right", "expand_transactions", "Expand Transactions"),
        ("r", "reset_layout", "Reset Layout"),
    ]
    
    def __init__(self):
        super().__init__()
        self.category_manager = CategoryManager()
        self.theme_list = ["textual-dark", "textual-light", "nord", "gruvbox", "monokai", "tokyo-night"]
        self.current_theme_index = 2  # Default to Nord theme
    
    CSS_PATH = Path(__file__).parent / "styles.tcss"
    
    def compose(self) -> ComposeResult:
        yield Header()
        
        # Top navigation bar
        yield Horizontal(
            Static("💰 View: Accounts", classes="nav-item"),
            Static("📅 Date: 2025-08-01 - 2025-09-01", classes="nav-item"),
            Static("🗓️ Monthly: < 2025 August >", classes="nav-item"),
            id="nav-bar"
        )
        
        # Main horizontal layout - accounts and transactions side by side
        with Horizontal(id="main-horizontal"):
            yield Container(
                Static("💳 Accounts @= $0.00", classes="panel-header", id="accounts-header"),
                DataTable(id="accounts-table"),
                classes="grid-panel",
                id="accounts-panel"
            )
            
            yield Container(
                Static("📋 Transaction Records", classes="panel-header"),
                DataTable(id="transactions-table"),
                classes="grid-panel",
                id="transactions-panel"
            )
        
        # Full-width insights panel below the grid
        yield Container(
            Static("📊 Financial Insights", classes="insights-title"),
            Static("Loading insights...", classes="insights-display", id="insights-display"),
            classes="insights-panel-full",
            id="insights-panel"
        )
        
        yield Footer()

    def on_mount(self) -> None:
        # Set initial theme based on current_theme_index
        self.theme = self.theme_list[self.current_theme_index]
        
        # Load data
        self.load_data()
        
        # Load insights after a delay to ensure UI is ready
        self.set_timer(1.0, self._load_insights_delayed)

    def load_data(self):
        # Setup table columns
        try:
            accounts_table = self.query_one("#accounts-table", DataTable)
            accounts_table.add_columns("Account", "Type", "Balance")
            
            transactions_table = self.query_one("#transactions-table", DataTable)
            transactions_table.add_columns("Date", "Description", "Amount", "Type", "Category", "Account")
            
        except Exception as e:
            self.log(f"Error setting up tables: {e}")
            self.notify("Failed to initialize tables. Please restart the app", severity="error")
            return
        
        # Load actual data from database
        self.refresh_data()

    def _load_insights_delayed(self):
        """Load insights after a delay - simplest approach."""
        try:
            self.log("Loading insights after delay")
            insights_display = self.query_one("#insights-display", Static)
            
            # Since we confirmed this works outside Textual, let's try it directly
            result = InsightsGenerator.generate_insights()
            self.log(f"Insights loaded successfully, length: {len(result)}")
            
            insights_display.update(result)
            
        except Exception as e:
            self.log(f"Error in delayed insights loading: {e}")
            import traceback
            self.log(f"Full traceback: {traceback.format_exc()}")
            try:
                insights_display = self.query_one("#insights-display", Static)
                insights_display.update(f"Failed to load insights: {str(e)}")
            except:
                pass




    def action_add_account(self) -> None:
        """Show the add account modal."""
        self.push_screen(AddAccountModal())

    def action_add_transaction(self) -> None:
        """Show the add transaction modal."""
        self.push_screen(AddTransactionModal())

    def action_transfer_money(self) -> None:
        """Show the transfer money modal."""
        self.push_screen(TransferModal())

    def on_click(self, event) -> None:
        """Handle clicks on the main sections."""
        # Simplified click handling for the new layout
        clicked_widget = event.control
        
        # Handle specific useful clicks
        if hasattr(clicked_widget, 'id'):
            if clicked_widget.id == "insights-display":
                # Refresh insights when clicked
                try:
                    insights_display = self.query_one("#insights-display", Static)
                    insights_display.update("🔄 Refreshing insights...")
                    self.log("Refreshing insights...")
                    result = InsightsGenerator.generate_insights()
                    self.log(f"Insights refresh successful")
                    insights_display.update(result)
                except Exception as e:
                    self.log(f"Error refreshing insights: {e}")
                    insights_display = self.query_one("#insights-display", Static)
                    insights_display.update("Failed to refresh insights")
            elif clicked_widget.id == "accounts-header":
                # Refresh accounts when header is clicked
                self.refresh_data()





    def refresh_data(self) -> None:
        """Refresh all data from database."""
        try:
            db = SessionLocal()
            
            # Clear and reload accounts table
            accounts_table = self.query_one("#accounts-table", DataTable)
            accounts_table.clear()
            
            # Load real account data
            accounts = db.query(Account).all()
            self.log(f"Found {len(accounts)} accounts in database")
            total_balance = 0
            
            # Prepare all rows at once
            account_rows = []
            for account in accounts:
                # Calculate totals for this account using proper SQLAlchemy syntax
                from sqlalchemy import func
                income_total = db.query(func.sum(Transaction.amount)).filter(
                    Transaction.account_id == account.id,
                    Transaction.transaction_type == TransactionType.INCOME
                ).scalar() or 0
                
                expense_total = db.query(func.sum(Transaction.amount)).filter(
                    Transaction.account_id == account.id,
                    Transaction.transaction_type == TransactionType.EXPENSE
                ).scalar() or 0
                
                # For transfers, we need to calculate incoming and outgoing separately
                # Transfers are stored with both accounts having transactions
                # The amount represents: 
                # - Money leaving the source account (treat as expense)
                # - Money entering the destination account (treat as income)
                
                # Get all transfer transactions for this account
                transfer_transactions = db.query(Transaction).filter(
                    Transaction.account_id == account.id,
                    Transaction.transaction_type == TransactionType.TRANSFER
                ).all()
                
                transfer_net = 0
                for transfer in transfer_transactions:
                    # Find the paired transaction to determine direction
                    if transfer.transfer_pair_id:
                        paired_transaction = db.query(Transaction).filter(
                            Transaction.id == transfer.transfer_pair_id
                        ).first()
                        
                        if paired_transaction:
                            # If the paired transaction is in a different account, 
                            # this is money leaving our account (negative)
                            if paired_transaction.account_id != account.id:
                                # Check if this is the "out" transaction by comparing descriptions
                                if f"Transfer to" in transfer.description:
                                    transfer_net -= transfer.amount  # Money leaving
                                else:
                                    transfer_net += transfer.amount  # Money coming in
                
                # Calculate balance (starting + income - expense + net transfers)
                balance = account.starting_balance + income_total - expense_total + transfer_net
                total_balance += balance
                
                # Add account type and better formatting
                account_type = account.account_type.value if account.account_type else "Unknown"
                account_rows.append([account.name, account_type, f"${balance:.2f}"])
            
            # Add rows to table
            if account_rows:
                for row in account_rows:
                    accounts_table.add_row(*row)
            else:
                accounts_table.add_row("No Accounts", "Unknown", "$0.00")
            
            # Update the accounts header with total balance
            accounts_header = self.query_one("#accounts-header", Static)
            accounts_header.update(f"💳 Accounts @= ${total_balance:.2f}")
            
            # Load all transactions in a single table
            transactions_table = self.query_one("#transactions-table", DataTable)
            transactions_table.clear()
            
            # Get all transactions ordered by date (most recent first)
            all_transactions = db.query(Transaction).order_by(Transaction.date.desc()).all()
            
            # Prepare all rows at once
            transaction_rows = []
            for transaction in all_transactions:
                try:
                    # Get account name
                    account = db.query(Account).filter(Account.id == transaction.account_id).first()
                    account_name = account.name if account else "Unknown"
                    
                    # Format date
                    date_str = transaction.date.strftime("%m/%d")
                    
                    # Format amount with currency and sign
                    amount_str = f"${transaction.amount:.2f}"
                    if transaction.transaction_type == TransactionType.INCOME:
                        amount_str = f"+{amount_str}"
                        type_str = "💰 Income"
                    elif transaction.transaction_type == TransactionType.EXPENSE:
                        amount_str = f"-{amount_str}"
                        type_str = "💸 Expense"
                    elif transaction.transaction_type == TransactionType.TRANSFER:
                        # Determine if this is incoming or outgoing transfer by description
                        if "Transfer to" in transaction.description:
                            amount_str = f"-{amount_str}"
                            type_str = "🔄 Transfer Out"
                        else:
                            amount_str = f"+{amount_str}"
                            type_str = "🔄 Transfer In"
                    
                    # Format category
                    category_str = transaction.category if transaction.category else "Uncategorized"
                    
                    transaction_row = [
                        date_str,
                        transaction.description,
                        amount_str,
                        type_str,
                        category_str,
                        account_name
                    ]
                    transaction_rows.append(transaction_row)
                    
                except Exception as e:
                    self.log(f"Error processing transaction: {e}")  # Remove ID exposure
            
            # Add rows to table
            if transaction_rows:
                for row in transaction_rows:
                    transactions_table.add_row(*row)
            else:
                transactions_table.add_row("--/--", "No Transactions", "$0.00", "📝 None", "No Category", "No Account")
            
            # Refresh the insights with new data
            try:
                insights_display = self.query_one("#insights-display", Static)
                self.log("Updating insights after data refresh...")
                result = InsightsGenerator.generate_insights()
                self.log(f"Insights update successful")
                insights_display.update(result)
            except Exception as e:
                self.log(f"Error updating insights: {e}")
                import traceback
                self.log(f"Insights error traceback: {traceback.format_exc()}")
                insights_display = self.query_one("#insights-display", Static)
                insights_display.update(f"Insights error: {str(e)}")
            
            db.close()
        except Exception as e:
            if 'db' in locals():
                db.close()
            self.log(f"Error refreshing data: {e}")
            self.notify("Failed to load data. Please check database connection", severity="error")

    def action_expand_accounts(self) -> None:
        """Expand the accounts panel"""
        try:
            # Update panel widths to give more space to accounts (50-50 split)
            accounts_panel = self.query_one("#accounts-panel", Container)
            transactions_panel = self.query_one("#transactions-panel", Container)
            accounts_panel.styles.width = "1fr"
            transactions_panel.styles.width = "1fr"
            self.notify("Accounts panel expanded", severity="information")
        except Exception as e:
            self.log(f"Error expanding accounts: {e}")

    def action_expand_transactions(self) -> None:
        """Expand the transactions panel"""
        try:
            # Update panel widths to give more space to transactions (20-80 split)
            accounts_panel = self.query_one("#accounts-panel", Container)
            transactions_panel = self.query_one("#transactions-panel", Container)
            accounts_panel.styles.width = "1fr"
            transactions_panel.styles.width = "4fr"
            self.notify("Transactions panel expanded", severity="information")
        except Exception as e:
            self.log(f"Error expanding transactions: {e}")

    def action_reset_layout(self) -> None:
        """Reset layout to default"""
        try:
            # Reset panel widths to default (accounts 30%, transactions 70%)
            accounts_panel = self.query_one("#accounts-panel", Container)
            transactions_panel = self.query_one("#transactions-panel", Container)
            accounts_panel.styles.width = "3fr"
            transactions_panel.styles.width = "7fr"
            self.notify("Layout reset to default", severity="information")
        except Exception as e:
            self.log(f"Error resetting layout: {e}")

    def action_toggle_theme(self) -> None:
        """Cycle through available themes"""
        self.current_theme_index = (self.current_theme_index + 1) % len(self.theme_list)
        new_theme = self.theme_list[self.current_theme_index]
        self.theme = new_theme
        self.notify(f"Theme changed to: {new_theme.title()}", severity="information")

if __name__ == "__main__":
    app = ExpenseApp()
    app.run()

