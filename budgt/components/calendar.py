from datetime import datetime, timedelta

class CalendarComponent:
    """Calendar component for displaying monthly calendar."""
    
    @staticmethod
    def generate_calendar():
        """Generate a complete calendar grid for the current month."""
        now = datetime.now()
        current_month = now.month
        current_year = now.year
        
        # Get the first day of the month
        first_day = datetime(current_year, current_month, 1)
        
        # Get the last day of the month
        if current_month == 12:
            last_day = datetime(current_year + 1, 1, 1) - timedelta(days=1)
        else:
            last_day = datetime(current_year, current_month + 1, 1) - timedelta(days=1)
        
        # Calculate the starting day (previous month's days to fill first week)
        start_date = first_day - timedelta(days=first_day.weekday())
        
        # Generate complete calendar grid
        calendar_lines = []
        
        # Add month and year header
        month_names = [
            "January", "February", "March", "April", "May", "June",
            "July", "August", "September", "October", "November", "December"
        ]
        calendar_lines.append(f"{month_names[current_month - 1]} {current_year}")
        
        # Add day headers with proper spacing
        calendar_lines.append("S  M  T  W  T  F  S")
        
        current_date = start_date
        week_count = 0
        max_weeks = 6  # Maximum weeks to display (covers all possible month layouts)
        
        while week_count < max_weeks and current_date <= last_day + timedelta(days=6):
            week_line = ""
            for day in range(7):
                if current_date.month == current_month:
                    # Current month
                    if current_date.day == now.day:
                        # Today - highlight with orange
                        week_line += f"[orange]{current_date.day:2d}[/orange] "
                    else:
                        week_line += f"{current_date.day:2d} "
                else:
                    # Other month - dimmed
                    week_line += f"[dim]{current_date.day:2d}[/dim] "
                current_date += timedelta(days=1)
            
            calendar_lines.append(week_line.rstrip())
            week_count += 1
            
            # Stop if we've shown the last day of the month and completed the week
            if current_date > last_day and (current_date - timedelta(days=1)).weekday() == 6:
                break
        
        calendar_text = "\n".join(calendar_lines)
        return calendar_text
