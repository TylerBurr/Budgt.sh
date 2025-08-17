"""Top Categories Component for Budgt.sh insights."""


class TopCategories:
    """Component for top spending categories with visual bars."""
    
    @staticmethod
    def generate(category_expenses):
        """Generate top categories component.
        
        Args:
            category_expenses (list): List of tuples (category_name, amount)
            
        Returns:
            str: Formatted categories content with visual bars
        """
        try:
            if not category_expenses:
                return """📊 Categories
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
No categorized expenses this week"""
            
            total_categorized = sum(amount for _, amount in category_expenses)
            
            categories_content = """📊 Top Categories This Week
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Category                      Amount    Perc  Visual
"""
            
            # Show top 10 categories
            for category, amount in category_expenses[:10]:
                percentage = (amount / total_categorized) * 100 if total_categorized > 0 else 0
                
                # Get category icon and display name
                icon, display_name = TopCategories._get_category_info(category)
                
                # Ensure display name fits nicely
                if len(display_name) > 20:
                    display_name = display_name[:17] + "..."
                
                # Create visual bar with proper spacing
                bar_width = 15
                filled_blocks = int((percentage / 100) * bar_width)
                visual_bar = "█" * filled_blocks + "░" * (bar_width - filled_blocks)
                
                categories_content += f"{icon} {display_name:<22} ${amount:>4.0f} {percentage:>3.0f}% {visual_bar}\n"
            
            return categories_content.rstrip()  # Remove trailing newline
            
        except Exception as e:
            return f"""📊 Categories
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Error loading categories: {str(e)}"""

    @staticmethod
    def _get_category_info(category):
        """Get icon and display name for a category.
        
        Args:
            category (str): Category name from database
            
        Returns:
            tuple: (icon, display_name)
        """
        category_lower = category.lower()
        
        # Category matching with icons
        if any(word in category_lower for word in ['food', 'grocery', 'restaurant', 'dining']):
            return "🍎", "Food & Dining"
        elif any(word in category_lower for word in ['vehicle', 'fuel', 'gas', 'petrol']):
            return "⛽", "Vehicle > Fuel"
        elif any(word in category_lower for word in ['transport', 'car', 'uber', 'taxi', 'bus', 'train']):
            return "🚗", "Transportation"
        elif any(word in category_lower for word in ['electronic', 'tech', 'communication', 'phone', 'internet']):
            return "📱", "Electronics"
        elif any(word in category_lower for word in ['health', 'medical', 'doctor', 'pharmacy']):
            return "🏥", "Healthcare"
        elif any(word in category_lower for word in ['entertainment', 'movie', 'music', 'game']):
            return "🎬", "Entertainment"
        elif any(word in category_lower for word in ['shopping', 'retail', 'store', 'clothes']):
            return "🛍️", "Shopping"
        elif any(word in category_lower for word in ['utility', 'bill', 'electric', 'water', 'rent']):
            return "🔌", "Utilities"
        else:
            # Keep original category name for better accuracy
            display_name = category if len(category) <= 20 else category[:17] + "..."
            return "💰", display_name
