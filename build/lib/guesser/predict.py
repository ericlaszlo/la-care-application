import base64
import io
import sys
import numpy as np

from flask import Blueprint
from flask import flash
from flask import jsonify
from flask import render_template
from flask import request

from PIL import Image

from tensorflow import keras


BP = Blueprint('predict', __name__, url_prefix='/')
MODEL = keras.models.load_model('cnn')

@BP.route("/", methods=['POST', 'GET'])
def predict():
    """Render the prediction/home.html template."""

    # Initial call to set up blank canvas.
    drawing_data = ''
    prediction = '?'
    score = '0.000'

    # Set up page with blanks.
    return render_template('predict/home.html',
                           drawing_data=drawing_data,
                           prediction=prediction,
                           score=score)


@BP.route('/background_process', methods=['POST', 'GET'])
def background_process():
    """Process the user entered digit and run it
    through the model.
    """
    prediction = -1
    try:
        drawing_data_original = request.form['drawing_data']
        user_drawn_image = drawing_data_original.split(',')[1]
        message = None
        if len(user_drawn_image) > 0:
            buf = io.BytesIO(base64.b64decode(user_drawn_image))
            img = Image.open(buf)
            img = img.resize([28, 28])

            # Images are transparent, so apply white background.
            corrected_img = Image.new("RGBA", (28, 28), "white")
            corrected_img.paste(img, (0, 0), img)
            corrected_img = np.asarray(corrected_img)

            # Remove color dimensions.
            corrected_img = corrected_img[:, :, 0]
            corrected_img = np.invert(corrected_img)

            # Get shape right for model.
            corrected_img = corrected_img.reshape([-1, 28, 28, 1])

            # Standard-scale the input --> [0, 1]
            corrected_img = \
                    np.asarray(corrected_img,
                               dtype=np.float64)/255.0

            probabilities = MODEL.predict(corrected_img).flatten()
            score = '{0:0.3f}'.format(probabilities.max())

            prediction = int(probabilities.argmax())

    except:
        # Something did not go right. Message is not used but
        # we can plug it in to the return statement if we
        # want to extend this application.
        e = sys.exc_info()[0]
        prediction = e
        score = '0.000'
        message = "Error with prediction, please try again"
        print(e, file=sys.stderr)

    flash(message)

    return jsonify({'prediction':prediction, 'score':score})
