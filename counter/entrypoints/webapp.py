from io import BytesIO

from flask import Flask, request, jsonify

from counter import config
from counter.domain.models import Prediction

def create_app():

    app = Flask(__name__)

    count_action = config.get_count_action()

    @app.route('/object-count', methods=['POST'])
    def object_detection():

        threshold = float(request.form.get('threshold', 0.5))
        uploaded_file = request.files['file']
        model_name = request.form.get('model_name', "rfcn")
        image = BytesIO()
        uploaded_file.save(image)
        count_response = count_action.execute(image, threshold)
        return jsonify(count_response)

    @app.route('/predictions', methods=['POST'])
    def get_predictions():
        threshold = float(request.form.get('threshold', 0.5))
        uploaded_file = request.files['file']
        model_name = request.form.get('model_name', "rfcn")
        image = BytesIO()
        uploaded_file.save(image)

        # Get the raw predictions from the object detector
        image.seek(0)  # Reset file pointer to beginning
        predictions = count_action._CountDetectedObjects__object_detector.predict(image)

        # Filter predictions based on threshold
        valid_predictions = [p for p in predictions if p.score >= threshold]

        # Convert predictions to serializable format
        result = [{
            'class_name': p.class_name,
            'score': p.score,
            'box': {
                'xmin': p.box.xmin,
                'ymin': p.box.ymin,
                'xmax': p.box.xmax,
                'ymax': p.box.ymax
            }
        } for p in valid_predictions]

        return jsonify(result)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run('0.0.0.0', debug=True)
