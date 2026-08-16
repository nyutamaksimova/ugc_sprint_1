from flask import Blueprint, current_app, jsonify, request
from werkzeug.exceptions import RequestEntityTooLarge

from src.core.auth import require_user
from src.services.producer import KafkaUnavailableError
from src.models.schemas import BatchValidationError, validate_batch, validate_event


bp = Blueprint("analytics", __name__)


@bp.get("/health")
def health():
    return {"status": "ok"}


@bp.post("/api/v1/events")
@require_user
def create_event(user_id: str):
    data = request.get_json(silent=True)
    if data is None:
        return jsonify(code="bad_request", message="JSON body is required"), 400
    try:
        event = validate_event(data)
    except ValueError as error:
        return jsonify(code="validation_error", errors=[{"index": 0, "errors": [str(error)]}]), 422
    return _publish([event], user_id)


@bp.post("/api/v1/events/batch")
@require_user
def create_batch(user_id: str):
    data = request.get_json(silent=True)
    if data is None:
        return jsonify(code="bad_request", message="JSON body is required"), 400
    try:
        events = validate_batch(data)
    except BatchValidationError as error:
        return jsonify(code="validation_error", errors=error.errors), 422
    return _publish(events, user_id)


def _publish(events: list[dict], user_id: str):
    try:
        current_app.extensions["event_producer"].publish(events, user_id)
    except KafkaUnavailableError:
        return jsonify(code="kafka_unavailable", message="Kafka is unavailable"), 503
    return jsonify(status="accepted", count=len(events)), 202


def register_error_handlers(app) -> None:
    @app.errorhandler(RequestEntityTooLarge)
    def request_too_large(_: RequestEntityTooLarge):
        return jsonify(code="payload_too_large", message="Request body exceeds 1 MiB"), 413
