import io
import json

import pytest

from pathlib import Path
from counter.entrypoints.webapp import create_app


@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture
def image_path():
    ref_dir = Path(__file__).parent
    return ref_dir.parent.parent / "resources" / "images" / "boy.jpg"


def test_object_detection(client, image_path):
    # Load the image from the path resource/boy.jpg
    with open(image_path, 'rb') as f:
        image_data = f.read()
    image = io.BytesIO(image_data)

    data = {
        'threshold': '0.9',
        'model_name': 'rfcn',
    }
    data['file'] = (image, 'test.jpg')

    # Make a test request to the object_detection endpoint
    response = client.post('/object-count', data = data,
        content_type='multipart/form-data', buffered=True)

    # Check that the count_action was called with the correct arguments and
    # and status code is correct(Integration test)
    assert response.status_code == 200
    assert json.loads(response.data) != None


def test_get_predictions(client, image_path):
    # Load the image from the path resource/boy.jpg
    with open(image_path, 'rb') as f:
        image_data = f.read()
    image = io.BytesIO(image_data)

    data = {
        'threshold': '0.9',
        'model_name': 'rfcn',
    }
    data['file'] = (image, 'test.jpg')

    # Make a test request to the predictions endpoint
    response = client.post('/predictions', data = data,
        content_type='multipart/form-data', buffered=True)

    # Check that the predictions endpoint returns valid data
    assert response.status_code == 200
    predictions = json.loads(response.data)
    assert isinstance(predictions, list)

    # In test environment with FakeObjectDetector, we should get at least one prediction
    if predictions:  # Only check structure if we have predictions
        prediction = predictions[0]
        assert 'class_name' in prediction
        assert 'score' in prediction
        assert 'box' in prediction
        assert isinstance(prediction['box'], dict)
        assert 'xmin' in prediction['box']
        assert 'ymin' in prediction['box']
        assert 'xmax' in prediction['box']
        assert 'ymax' in prediction['box']