"""Components package for Budgt.sh TUI application."""

# Import all component classes for easy access
from .weekly_overview import WeeklyOverview
from .top_categories import TopCategories
from .spending_chart import SpendingChart
from .insights import InsightsGenerator

__all__ = [
    'WeeklyOverview',
    'TopCategories', 
    'SpendingChart',
    'InsightsGenerator'
]
