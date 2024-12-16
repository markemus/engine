"""Collections are used to populate Furniture and Items with other Items."""
from engine import suits_and_collections as sc
from castle.human import Human
from castle import suits as st


testsuit_c = sc.suit_to_collection(st.testsuit, Human)
plainsuit_c = sc.suit_to_collection(st.plainsuit, Human)
weapons_c = sc.suit_to_collection(st.weapons, Human)
