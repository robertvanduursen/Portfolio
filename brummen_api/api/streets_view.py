from flask import Flask
from flask import request
from flask import jsonify

def streets():
    """
        List of all the streets in Brummen
        ---
        parameters:
          - name: name
            in: path
            type: string
            required: true
            description: The name to greet.
        responses:
          200:
            description: Your IP address
            schema:
              type: string
        """
    street_names = [
        'prinses beatrixlaan',
        'prinses bernardlaan',

    ]

    return jsonify(street_names)
