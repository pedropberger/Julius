
# Configuration for data collection
YEARS = ["2025"]  # Limited for testing - change to ["2024", "2025"] for full collection
MONTHS = [11, 12]  # Limited for testing - change to [1,2,3,4,5,6,7,8,9,10,11,12] for full collection

# Extended configuration for comprehensive collection
# Uncomment the lines below for full historical collection
# YEARS = [str(year) for year in range(2015, 2026)]
# MONTHS = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

# Rate limiting configuration (seconds)
REQUEST_DELAY = 1.0  # Delay between individual requests
MUNICIPALITY_DELAY = 5.0  # Delay between municipalities

# Retry configuration
MAX_RETRIES = 3
TIMEOUT_SECONDS = 30

# Logging configuration
LOG_LEVEL = "INFO"  # DEBUG, INFO, WARNING, ERROR
