"""Tests for ItemCollection."""

from dialoguekit.core.recsys.item_collection import ItemCollection

ITEM_CSV_FILE = "tests/data/movielens-20m-sample/movies.csv"


def test_empty_collection():
    item_collection = ItemCollection()
    assert item_collection.num_items() == 0


def test_load_items_csv():
    item_collection = ItemCollection()
    item_collection.load_items_csv(ITEM_CSV_FILE, ["ID", "NAME", "genres"])
    # Checks the number of items.
    assert item_collection.num_items() == 1000
    # Checks some specific items.
    item_6 = item_collection.get_item("6")
    assert item_6.name == "Heat (1995)"
    assert item_6.get_property("genres") == "Action|Crime|Thriller"
    item_1016 = item_collection.get_item("1016")
    assert item_1016.name == "Shaggy Dog, The (1959)"
    assert item_1016.get_property("genres") == "Children|Comedy"
