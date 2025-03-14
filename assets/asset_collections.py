"""Collections are used to populate Furniture and Items with other Items.

See household_items.py for documentation on collections."""
from engine import suits_and_collections as sc
from assets.human import Human
from assets import suits as st


testsuit_c = sc.suit_to_collection(st.iron_armorsuit, Human)
ironsuit_c = sc.suit_to_collection(st.iron_armorsuit, Human)
bronzesuit_c = sc.suit_to_collection(st.bronze_armorsuit, Human)
plainsuit_c = sc.suit_to_collection(st.plainsuit, Human)
weapons_c = sc.suit_to_collection(st.iron_weapons, Human)
