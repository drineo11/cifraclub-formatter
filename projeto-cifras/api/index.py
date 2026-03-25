from flask import Flask, request, send_file, jsonify
import sys
import os
import io
import logging
import json
from datetime import datetime
from urllib.parse import urlparse

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from lib.cifra_logic import get_cifra_content, generate_docx_bytes

app = Flask(__name__)

logger = logging.getLogger(__name__)


def validate_url(url: str) -> tuple:
    """Validate URL is from cifraclub.com.br and has valid scheme."""
    if not url:
        return False, "URL é obrigatória"
    try:
        parsed = urlparse(url)
        if parsed.scheme not in ["http", "https"]:
            return False, "URL deve usar http:// ou https://"
        if "cifraclub.com.br" not in parsed.netloc:
            return False, "URL deve ser do Cifra Club (cifraclub.com.br)"
        return True, ""
    except Exception:
        return False, "URL inválida"


@app.route("/api/generate", methods=["POST"])
def generate():
    start_time = datetime.now()
    request_id = int(start_time.timestamp())

    url = request.json.get("url", "") if request.json else ""
    format_type = request.json.get("format", "pdf") if request.json else "pdf"

    logger.info(
        json.dumps(
            {
                "request_id": request_id,
                "event": "request_received",
                "url": url[:80] + "..." if len(url) > 80 else url,
                "format": format_type,
            }
        )
    )

    is_valid, error_msg = validate_url(url)
    if not is_valid:
        logger.warning(
            json.dumps(
                {
                    "request_id": request_id,
                    "event": "validation_error",
                    "error": error_msg,
                }
            )
        )
        return jsonify({"error": error_msg}), 400

    target_key_index = None
    if "#" in url:
        parts = url.split("#")
        url = parts[0]
        fragment = parts[1]
        for param in fragment.split("&"):
            if param.startswith("key="):
                try:
                    target_key_index = int(param.split("=")[1])
                except:
                    pass

    try:
        title, artist, key, lines = get_cifra_content(url, target_key_index)

        safe_title = "".join(
            [c for c in title if c.isalpha() or c.isdigit() or c == " "]
        ).rstrip()
        safe_artist = "".join(
            [c for c in artist if c.isalpha() or c.isdigit() or c == " "]
        ).rstrip()
        filename = f"{safe_title}_{safe_artist}".replace(" ", "_")

        if format_type == "docx":
            docx_bytes = generate_docx_bytes(title, artist, key, lines)
            logger.info(
                json.dumps(
                    {
                        "request_id": request_id,
                        "event": "success",
                        "title": title,
                        "format": "docx",
                        "duration_seconds": (
                            datetime.now() - start_time
                        ).total_seconds(),
                    }
                )
            )
            return send_file(
                io.BytesIO(docx_bytes),
                mimetype="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                as_attachment=True,
                download_name=f"{filename}.docx",
            )
        else:
            logger.warning(
                json.dumps(
                    {
                        "request_id": request_id,
                        "event": "invalid_format",
                        "format": format_type,
                    }
                )
            )
            return jsonify({"error": "Formato inválido. Use 'pdf' ou 'docx'."}), 400

    except Exception as e:
        error_str = str(e)
        logger.error(
            json.dumps(
                {
                    "request_id": request_id,
                    "event": "error",
                    "error": error_str,
                    "duration_seconds": (datetime.now() - start_time).total_seconds(),
                }
            )
        )
        return jsonify({"error": error_str}), 500


if __name__ == "__main__":
    app.run(port=5328)
