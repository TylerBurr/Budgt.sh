from ..database import SessionLocal, Transaction, TransactionType
from datetime import datetime, timedelta
from sqlalchemy import func
from rich.console import Console

# Import individual component classes
from .weekly_overview import WeeklyOverview
from .spending_chart import SpendingChart


class InsightsGenerator:
    """Main insights generator that orchestrates all components."""
    
    @staticmethod
    def generate_insights():
        """Generate modular insights using individual components."""
        try:
            # Simple database session
            db = SessionLocal()
            
            # Basic initialization
            end_date = datetime.now()
            week_start = end_date - timedelta(days=7)
            
            # Get weekly expense data
            weekly_expenses = db.query(func.sum(Transaction.amount)).filter(
                Transaction.transaction_type == TransactionType.EXPENSE,
                Transaction.date >= week_start
            ).scalar() or 0
            
            # Calculate daily average
            daily_average = weekly_expenses / 7 if weekly_expenses > 0 else 0
            
            # Get daily trend data
            daily_data = []
            dates = []
            amounts = []
            
            for i in range(7):
                date = end_date - timedelta(days=i)
                day_start = date.replace(hour=0, minute=0, second=0, microsecond=0)
                day_end = day_start + timedelta(days=1)
                
                daily_expense = db.query(func.sum(Transaction.amount)).filter(
                    Transaction.transaction_type == TransactionType.EXPENSE,
                    Transaction.date >= day_start,
                    Transaction.date < day_end
                ).scalar() or 0
                
                daily_data.append((date.strftime('%m/%d'), daily_expense))
                dates.append(date.strftime('%m/%d'))
                amounts.append(daily_expense)
            
            # Close database early
            db.close()
            
            # Reverse to show oldest to newest
            daily_data.reverse()
            dates.reverse()
            amounts.reverse()
            
            # Generate components
            overview_content = WeeklyOverview.generate(weekly_expenses, daily_average)
            trend_content = SpendingChart.generate(daily_data, amounts, dates)
            
            # Create manual layout
            overview_lines = overview_content.split('\n') if overview_content else ["No data"]
            trend_lines = trend_content.split('\n') if trend_content else ["No data"]
            
            max_lines = max(len(overview_lines), len(trend_lines)) if overview_lines and trend_lines else 5
            result_lines = []
            
            # Box headers
            overview_header = "┌─ Weekly Overview " + "─" * 26 + "┐"
            trend_header = "┌─ Spending Trend " + "─" * 67 + "┐"
            result_lines.append(overview_header + " " + trend_header)
            
            # Content lines
            for i in range(max_lines + 2):
                # Overview side
                if i == 0 or i == max_lines + 1:
                    overview_line = "│" + " " * 44 + "│"
                elif i - 1 < len(overview_lines):
                    content = overview_lines[i - 1]
                    if len(content) > 42:
                        content = content[:39] + "..."
                    overview_line = "│ " + content.ljust(42) + " │"
                else:
                    overview_line = "│" + " " * 44 + "│"
                
                # Trend side
                if i == 0 or i == max_lines + 1:
                    trend_line = "│" + " " * 84 + "│"
                elif i - 1 < len(trend_lines):
                    content = trend_lines[i - 1]
                    if len(content) > 82:
                        content = content[:79] + "..."
                    trend_line = "│ " + content.ljust(82) + " │"
                else:
                    trend_line = "│" + " " * 84 + "│"
                
                result_lines.append(overview_line + " " + trend_line)
            
            # Box footers
            overview_footer = "└" + "─" * 44 + "┘"
            trend_footer = "└" + "─" * 84 + "┘"
            result_lines.append(overview_footer + " " + trend_footer)
            
            return "\n".join(result_lines)
            
        except Exception as e:
            return f"""┌─ Weekly Overview ──────────────────────────┐ ┌─ Spending Trend ───────────────────────────────────────────────────────────┐
│                                            │ │                                                                               │
│ 💰 Weekly Total      $0.00                 │ │  Error: {str(e)[:60]}...                                                     │
│ 📅 Daily Average     $0.00                 │ │                                                                               │
│ 🎯 Target           $1000.00               │ │  Please check your database connection.                                      │
│    Progress          0.0%                  │ │                                                                               │
│    ░░░░░░░░░░░░░░░░░░░░                    │ │                                                                               │
│                                            │ │                                                                               │
└────────────────────────────────────────────┘ └───────────────────────────────────────────────────────────────────────────────┘"""
