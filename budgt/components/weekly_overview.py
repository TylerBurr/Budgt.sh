"""Weekly Overview Component for Budgt.sh insights."""


class WeeklyOverview:
    """Component for weekly spending overview with progress bar."""
    
    @staticmethod
    def generate(weekly_expenses, daily_average, target=1000.0):
        """Generate weekly overview component.
        
        Args:
            weekly_expenses (float): Total expenses for the week
            daily_average (float): Average daily spending
            target (float): Weekly spending target
            
        Returns:
            str: Formatted weekly overview content
        """
        try:
            # Calculate progress percentage
            progress_percentage = min((weekly_expenses / target) * 100, 100) if target > 0 else 0
            
            # Create a progress bar for target achievement
            progress_bar_width = 20
            progress_filled = int((progress_percentage / 100) * progress_bar_width)
            progress_bar = "█" * progress_filled + "░" * (progress_bar_width - progress_filled)
            
            overview_content = f"""💰 Weekly Total      ${weekly_expenses:>8.2f}
📅 Daily Average     ${daily_average:>8.2f}
🎯 Target           ${target:>8.2f}
   Progress         {progress_percentage:>6.1f}%
   {progress_bar}"""
            
            return overview_content
            
        except Exception as e:
            return f"""💰 Weekly Total      $0.00
📅 Daily Average     $0.00
🎯 Target           $1000.00
   Progress         0.0%
   ░░░░░░░░░░░░░░░░░░░░
Error: {str(e)}"""
