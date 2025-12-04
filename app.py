from flask import Flask, render_template, request, jsonify
import requests
import re
import os
import logging
from dotenv import load_dotenv

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()
BARCODE_API_KEY = os.getenv("BARCODE_API_KEY")


# UPC/EAN validation function
def is_valid_upc(upc):
    if not upc:
        return True  # UPC is optional
    upc = re.sub(r'[\s-]', '', upc)

    # Validate length
    if len(upc) not in [12, 13] or not upc.isdigit():
        logger.debug(f"UPC {upc} invalid: Length {len(upc)} not 12 or 13, or not all digits")
        return False

    digits = [int(d) for d in upc]
    if len(upc) == 12:  # UPC-A
        odd_sum = sum(digits[::2])
        even_sum = sum(digits[1::2])
        total = odd_sum * 3 + even_sum
        check_digit = (10 - (total % 10)) % 10
        is_valid = check_digit == digits[-1]
        logger.debug(
            f"UPC-A {upc}: odd_sum={odd_sum}, even_sum={even_sum}, total={total}, check_digit={check_digit}, valid={is_valid}")
        return is_valid
    else:  # EAN-13
        even_sum = sum(digits[::2])
        odd_sum = sum(digits[1::2])
        total = even_sum * 3 + odd_sum
        check_digit = (10 - (total % 10)) % 10
        is_valid = check_digit == digits[-1]
        logger.debug(
            f"EAN-13 {upc}: even_sum={even_sum}, odd_sum={odd_sum}, total={total}, check_digit={check_digit}, valid={is_valid}")
        # Allow API call even if checksum fails, as Barcode Lookup API might accept it
        return True


@app.route('/')
def index():
    return render_template('cw.html')


@app.route('/parcel-optimizer')
def parcel_optimizer():
    return render_template('parcel_optimizer.html')


@app.route('/lookup-upc', methods=['POST'])
def lookup_upc():
    try:
        upc = request.json.get('upc') if request.is_json else request.form.get('upc')
        if not upc:
            logger.error("No UPC provided")
            return jsonify({'error': 'UPC code is required'}), 400

        if not is_valid_upc(upc):
            logger.error(f"Invalid UPC code: {upc}")
            return jsonify({'error': 'Invalid UPC code format (must be 12 or 13 digits)'}), 400

        if not BARCODE_API_KEY:
            logger.error("Barcode API key not set")
            return jsonify({'error': 'Barcode API key not set'}), 500

        logger.info(f"Querying Barcode Lookup API for UPC: {upc}")
        url = f"https://api.barcodelookup.com/v3/products?key={BARCODE_API_KEY}&barcode={upc}"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        product = response.json().get("products", [{}])[0]

        if not product.get("title"):
            logger.warning(f"No product found for UPC: {upc}")
            return jsonify({'error': 'No product found for this UPC code'}), 404

        result = {
            "name": product.get("title", ""),
            "brand": product.get("brand", ""),
            "description": product.get("description", ""),
            "manufacturer": product.get("manufacturer", ""),
            "category": product.get("category", ""),
            "image": product.get("images", [""])[0]
        }
        logger.info(f"Successful lookup for UPC {upc}: {result}")
        return jsonify(result)
    except requests.RequestException as e:
        logger.error(f"API request failed for UPC {upc}: {str(e)}")
        return jsonify({'error': f"Barcode Lookup API request failed: {str(e)}"}), 502
    except Exception as e:
        logger.error(f"Unexpected error for UPC {upc}: {str(e)}")
        return jsonify({'error': f"Unexpected error: {str(e)}"}), 500


if __name__ == '__main__':
    app.run(debug=True, port=5001)