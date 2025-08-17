"""Spending Chart Component for Budgt.sh insights."""

from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.align import Align
from rich import box
import plotext as plt


class SpendingChart:
    """Component for a clean and beautiful spending trend chart."""
    
    @staticmethod
    def generate(daily_data, amounts, date_labels):
        """Generate spending chart component using plotext line chart.
        
        Args:
            daily_data (list): List of tuples (date_str, amount)
            amounts (list): List of daily spending amounts
            date_labels (list): List of date labels for x-axis
            
        Returns:
            str: Formatted plotext line chart
        """
        return SpendingChart._create_clean_chart(amounts, date_labels)
    
    @staticmethod
    def _create_clean_chart(amounts, date_labels):
        """Create a compact line graph using plotext for the insights panel.
        
        Args:
            amounts (list): List of daily spending amounts
            date_labels (list): List of date labels
            
        Returns:
            str: Compact plotext line graph output
        """
        try:
            # Use sample data if no real data
            if not amounts or all(a == 0 for a in amounts):
                amounts = [120, 50, 85, 200, 150, 90, 180]
                date_labels = [f"{i+10:02d}" for i in range(7)]
            
            # Limit to last 7 days to keep compact
            amounts = amounts[-7:]
            date_labels = date_labels[-7:] if date_labels else [f"{i+10:02d}" for i in range(7)]
            
            # Create proper line plot using plotext
            plt.clear_data()
            plt.clear_figure()
            
            # Set up the plot dimensions to fit properly without overflow
            plt.plotsize(85, 12)
            
            # Create x values (day indices)
            x_values = list(range(len(amounts)))
            
            # Create smooth line plot with interpolation
            plt.plot(x_values, amounts, color="cyan", marker="fhd")
            
            # Remove all labels and decorations for clean look
            plt.title("")
            plt.xlabel("")
            plt.ylabel("")
            
            # Add some basic axis information for better readability
            day_numbers = [date_label.split('/')[-1] if '/' in date_label else date_label for date_label in date_labels]
            if len(day_numbers) == len(x_values):
                plt.xticks(x_values, day_numbers)
            
            # Show some y-axis values for context
            max_amount = max(amounts) if amounts else 1
            min_amount = min(amounts) if amounts else 0
            plt.ylim(min_amount * 0.9, max_amount * 1.1)
            
            # Apply theme - try different options:
            # Available themes: "clear", "dark", "matrix", "pro", "sahara", "retro"
            plt.theme("clear")  # You can change this to any theme
            plt.grid(True, True)  # Add light grid for better readability
            plt.frame(True)  # Keep frame for structure
            
            # Get the clean plot output
            plot_output = plt.build()
            
            # Keep the full plotext output for better user experience
            # Just trim any excessive empty lines
            lines = plot_output.split('\n')
            while lines and not lines[-1].strip():
                lines.pop()
            plot_output = '\n'.join(lines)
            
            # Create summary info without header (panel will provide title)
            total_spending = sum(amounts)
            avg_spending = total_spending / len(amounts) if amounts else 0
            summary = f"Total: ${total_spending:.0f} | Avg: ${avg_spending:.0f}"
            
            # Create day labels
            day_labels = " ".join([date_label.split('/')[-1] if '/' in date_label else date_label for date_label in date_labels])
            
            # Build the clean output
            result = plot_output + "\n" 
            result += f"Days: {day_labels}\n"
            result += f"{summary}"
            
            return result
            
        except Exception as e:
            # Display the actual error instead of fallback
            return f"Chart Error: {str(e)}"

