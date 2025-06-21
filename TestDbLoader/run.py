import entities_loading
import donation_loading
import overview_loading
import ministerial_load

# 1. Create and populate Entities
entities_loading.full_load_entities()

# 2. Create overview tables
overview_loading.full_load_overview()

# 3. Create ministerial meetings DB
ministerial_load.create_db()
ministerial_load.load_meetings()

# 4. Load specific minister files
ministerial_load.read_meeting_file("ANDREW_HOGGARD", "APROCT24")

# 5. Create and populate Donations database/tables
donation_loading.create_donation_db_and_tables()