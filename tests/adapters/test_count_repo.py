import pytest
from unittest.mock import patch, MagicMock

from counter.adapters.count_repo import CountInMemoryRepo, CountMongoDBRepo, CountMongoDBAtlasRepo
from counter.domain.models import ObjectCount


class TestCountInMemoryRepo:
    def test_read_values_empty(self):
        repo = CountInMemoryRepo()
        assert repo.read_values() == []

    def test_read_values_with_data(self):
        repo = CountInMemoryRepo()
        repo.store = {'cat': ObjectCount('cat', 2), 'dog': ObjectCount('dog', 1)}
        
        # Test reading all values
        values = repo.read_values()
        assert sorted(values, key=lambda x: x.object_class) == [
            ObjectCount('cat', 2), ObjectCount('dog', 1)
        ]
        
        # Test reading specific values
        values = repo.read_values(['cat'])
        assert values == [ObjectCount('cat', 2)]

    def test_update_values_new(self):
        repo = CountInMemoryRepo()
        repo.update_values([ObjectCount('cat', 2), ObjectCount('dog', 1)])
        
        assert repo.store == {'cat': ObjectCount('cat', 2), 'dog': ObjectCount('dog', 1)}

    def test_update_values_existing(self):
        repo = CountInMemoryRepo()
        repo.store = {'cat': ObjectCount('cat', 1)}
        
        repo.update_values([ObjectCount('cat', 2), ObjectCount('dog', 1)])
        
        assert repo.store == {'cat': ObjectCount('cat', 3), 'dog': ObjectCount('dog', 1)}


class TestCountMongoDBRepo:
    @pytest.fixture
    def mongo_client_mock(self):
        with patch('counter.adapters.count_repo.MongoClient') as mock:
            yield mock

    def test_read_values(self, mongo_client_mock):
        # Setup mock
        db_mock = MagicMock()
        collection_mock = MagicMock()
        mongo_client_mock.return_value.__getitem__.return_value = db_mock
        db_mock.counter = collection_mock
        collection_mock.find.return_value = [
            {'object_class': 'cat', 'count': 2},
            {'object_class': 'dog', 'count': 1}
        ]
        
        # Test
        repo = CountMongoDBRepo('localhost', 27017, 'test_db')
        values = repo.read_values()
        
        # Verify
        assert sorted(values, key=lambda x: x.object_class) == [
            ObjectCount('cat', 2), ObjectCount('dog', 1)
        ]
        
        # Test with specific object classes
        collection_mock.find.return_value = [{'object_class': 'cat', 'count': 2}]
        values = repo.read_values(['cat'])
        assert values == [ObjectCount('cat', 2)]

    def test_update_values(self, mongo_client_mock):
        # Setup mock
        db_mock = MagicMock()
        collection_mock = MagicMock()
        mongo_client_mock.return_value.__getitem__.return_value = db_mock
        db_mock.counter = collection_mock
        
        # Test
        repo = CountMongoDBRepo('localhost', 27017, 'test_db')
        repo.update_values([ObjectCount('cat', 2), ObjectCount('dog', 1)])
        
        # Verify
        assert collection_mock.update_one.call_count == 2
        collection_mock.update_one.assert_any_call(
            {'object_class': 'cat'}, {'$inc': {'count': 2}}, upsert=True
        )
        collection_mock.update_one.assert_any_call(
            {'object_class': 'dog'}, {'$inc': {'count': 1}}, upsert=True
        )


class TestCountMongoDBAtlasRepo:
    @pytest.fixture
    def mongo_client_mock(self):
        with patch('counter.adapters.count_repo.MongoClient') as mock:
            yield mock

    def test_read_values(self, mongo_client_mock):
        # Setup mock
        db_mock = MagicMock()
        collection_mock = MagicMock()
        mongo_client_mock.return_value.__getitem__.return_value = db_mock
        db_mock.counter = collection_mock
        collection_mock.find.return_value = [
            {'object_class': 'cat', 'count': 2},
            {'object_class': 'dog', 'count': 1}
        ]
        
        # Test
        repo = CountMongoDBAtlasRepo('mongodb+srv://user:pass@cluster.mongodb.net/', 'test_db')
        values = repo.read_values()
        
        # Verify
        assert sorted(values, key=lambda x: x.object_class) == [
            ObjectCount('cat', 2), ObjectCount('dog', 1)
        ]
        
        # Test with specific object classes
        collection_mock.find.return_value = [{'object_class': 'cat', 'count': 2}]
        values = repo.read_values(['cat'])
        assert values == [ObjectCount('cat', 2)]

    def test_update_values(self, mongo_client_mock):
        # Setup mock
        db_mock = MagicMock()
        collection_mock = MagicMock()
        mongo_client_mock.return_value.__getitem__.return_value = db_mock
        db_mock.counter = collection_mock
        
        # Test
        repo = CountMongoDBAtlasRepo('mongodb+srv://user:pass@cluster.mongodb.net/', 'test_db')
        repo.update_values([ObjectCount('cat', 2), ObjectCount('dog', 1)])
        
        # Verify
        assert collection_mock.update_one.call_count == 2
        collection_mock.update_one.assert_any_call(
            {'object_class': 'cat'}, {'$inc': {'count': 2}}, upsert=True
        )
        collection_mock.update_one.assert_any_call(
            {'object_class': 'dog'}, {'$inc': {'count': 1}}, upsert=True
        )
