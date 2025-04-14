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


def test_predictions_endpoint(client, image_path):
    # Load the image from the path resource/boy.jpg
    with open(image_path, 'rb') as f:
        image_data = f.read()
    image = io.BytesIO(image_data)
    
    data = {
        'threshold': '0.5',
        'model_name': 'rfcn',
    }
    data['file'] = (image, 'test.jpg')

    # Make a test request to the predictions endpoint
    response = client.post('/predictions', data=data,
                          content_type='multipart/form-data', buffered=True)

    # Check that the response is valid
    assert response.status_code == 200
    predictions = json.loads(response.data)
    assert isinstance(predictions, list)
    
    # In test environment with FakeObjectDetector, we should get predictions
    # with the expected structure
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


def test_predictions_endpoint_with_threshold(client, image_path):
    # Load the image from the path resource/boy.jpg
    with open(image_path, 'rb') as f:
        image_data = f.read()
    image = io.BytesIO(image_data)
    
    # Test with a high threshold that should filter out predictions
    data = {
        'threshold': '0.999999',  # Very high threshold
        'model_name': 'rfcn',
    }
    data['file'] = (image, 'test.jpg')

    # Make a test request to the predictions endpoint
    response = client.post('/predictions', data=data,
                          content_type='multipart/form-data', buffered=True)

    # Check that the response is valid
    assert response.status_code == 200
    predictions = json.loads(response.data)
    
    # With FakeObjectDetector and a very high threshold, we should get no predictions
    # or only predictions with very high scores
    for prediction in predictions:
        assert prediction['score'] >= 0.999999
