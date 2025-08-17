CSS_STYLES = """
/* Modern Rich-inspired styling with vibrant colors */
#nav-bar {
    height: 1;
    padding: 0;
    background: #1a1b26;
    border-bottom: solid #7aa2f7;
}

.nav-item {
    margin-right: 2;
    text-style: bold;
    color: #c0caf5;
    background: #24283b;
    padding: 0 1;
}

.nav-item:hover {
    color: #7aa2f7;
    background: #414868;
}

#main-content {
    height: 1fr;
    margin: 1;
    background: #1a1b26;
}

#left-panel, #right-panel {
    border: round #7aa2f7;
    padding: 1;
    margin: 0 1;
    height: 1fr;
    background: #24283b;
}

#accounts-table, #transactions-table {
    height: 8;
    min-height: 8;
    max-height: 15;
    background: #1a1b26;
    border: round #7aa2f7;
    margin: 1;
}

#left-panel:focus-within, #right-panel:focus-within {
    border: thick #bb9af7;
}

.panel-header {
    text-style: bold;
    color: #7aa2f7;
    padding-bottom: 1;
    border-bottom: solid #7aa2f7;
    margin-bottom: 1;
    background: #414868;
    text-align: center;
}

.panel-header:hover {
    color: #bb9af7;
    border-bottom: solid #bb9af7;
}

.sub-panel-header {
    text-style: bold;
    color: #9ece6a;
    padding-bottom: 1;
    margin-bottom: 1;
    background: #2a2f41;
}

.period-navigation {
    text-align: center;
    color: #9ece6a;
    margin: 1 0;
    text-style: bold;
}

.calendar-grid {
    color: #c0caf5;
    margin: 1 0;
    text-align: center;
}

#calendar-panel {
    border: round #9ece6a;
    padding: 1;
    margin: 1;
    height: 15;
    background: #24283b;
}

#calendar-panel:focus-within {
    border: thick #bb9af7;
}

#income-summary {
    color: #9ece6a;
    text-style: bold;
    margin: 1 0;
    background: #2a2f41;
    padding: 0 1;
}

#expense-summary {
    color: #f7768e;
    text-style: bold;
    margin: 1 0;
    background: #2a2f41;
    padding: 0 1;
}

#insights-panel {
    border: round #f7768e;
    padding: 1;
    margin: 1;
    height: 20;
    background: #24283b;
}

#insights-panel:focus-within {
    border: thick #bb9af7;
}

.insights-title {
    text-style: bold;
    color: #f7768e;
    border-bottom: solid #f7768e;
    margin-bottom: 1;
    padding-bottom: 1;
    text-align: center;
    background: #414868;
}

.insights-display {
    color: #c0caf5;
    background: #1a1b26;
    padding: 1;
    border: none;
}

/* Modal styling */
#dialog {
    border: thick #7aa2f7;
    background: #24283b;
    padding: 2;
    width: 60;
    height: auto;
}

#title {
    text-align: center;
    text-style: bold;
    color: #7aa2f7;
    margin-bottom: 2;
    background: #414868;
    padding: 1;
}

#button-row {
    margin-top: 2;
}

#button-row Button {
    margin: 0 1;
    text-style: bold;
}

#button-row Button.-primary {
    background: #7aa2f7;
    color: #1a1b26;
    border: none;
}

#button-row Button.-secondary {
    background: #414868;
    color: #c0caf5;
    border: solid #7aa2f7;
}
"""
