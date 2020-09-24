from models.store import StoreModel
from tests.unit.unit_base_test import UnitBaseTest


class StoreTest(UnitBaseTest):
    def test_create_store(self):
        store = StoreModel('Store Test')
        self.assertEqual(store.name, 'Store Test',
                         "The name os the store after de creation does not equal to the constructor argument.")
        self.assertIsNone(store.id,
                          "The id of 'test_store' did not None as expected.")
