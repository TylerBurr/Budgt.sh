import yaml
import os

class CategoryManager:
    """Manages categories and their colors."""
    
    def __init__(self):
        self.categories_data = self.load_categories()
    
    def load_categories(self):
        """Load categories from the YAML file."""
        try:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            categories_file = os.path.join(current_dir, "..", "categories.yaml")
            
            if os.path.exists(categories_file):
                with open(categories_file, 'r') as file:
                    return yaml.safe_load(file)
            else:
                return []
        except Exception as e:
            return []
    
    def get_category_color(self, category_name):
        """Get the color for a given category."""
        if not self.categories_data:
            return "white"
        
        # Search for the category in main categories
        for category in self.categories_data:
            if category['name'] == category_name:
                return category.get('color', 'white')
            
            # Search in subcategories
            if 'subcategories' in category:
                for subcategory in category['subcategories']:
                    if subcategory['name'] == category_name:
                        return category.get('color', 'white')
        
        return "white"
    
    def get_color_emoji(self, color_name):
        """Convert color name to emoji for display."""
        color_map = {
            'orange_red1': '🟠',
            'grey63': '⚫',
            'cyan': '🔵',
            'dodger_blue3': '🔵',
            'hot_pink': '🟣',
            'green3': '🟢',
            'red3': '🔴',
            'yellow': '🟡',
            'indian_red': '🔴',
            'royal_blue1': '🔵',
            'medium_orchid3': '🟣'
        }
        return color_map.get(color_name, '⚪')
    
    def get_category_options(self):
        """Get all category options for dropdowns."""
        if not self.categories_data:
            return [
                ("Food", "Food"),
                ("Transport", "Transport"),
                ("Shopping", "Shopping"),
                ("Income", "Income"),
                ("Other", "Other")
            ]
        
        category_options = []
        for category in self.categories_data:
            category_options.append((category['name'], category['name']))
            if 'subcategories' in category:
                for subcategory in category['subcategories']:
                    category_options.append((f"{category['name']} > {subcategory['name']}", f"{category['name']} > {subcategory['name']}"))
        
        return category_options
