from flask import Flask, jsonify, request
from src.domain.repositories import CounterRepository
from src.domain.exceptions import InvalidCounterOperationError
from src.application.use_cases import (
    IncrementCounterUseCase,
    GetCounterUseCase,
    ResetCounterUseCase,
    GetAllCountersUseCase
)


def create_app(repository: CounterRepository) -> Flask:
    app = Flask(__name__)
    
    increment_use_case = IncrementCounterUseCase(repository)
    get_counter_use_case = GetCounterUseCase(repository)
    reset_use_case = ResetCounterUseCase(repository)
    get_all_use_case = GetAllCountersUseCase(repository)
    
    @app.route("/health")
    def health():
        return jsonify({"status": "healthy"})
    
    @app.route("/api/v1/counters/<name>", methods=["GET"])
    def get_counter(name):
        counter = get_counter_use_case.execute(name)
        return jsonify({
            "name": counter.name,
            "value": counter.value
        })
    
    @app.route("/api/v1/counters/<name>/increment", methods=["POST"])
    def increment_counter(name):
        data = request.get_json() or {}
        amount = data.get("amount", 1)
        
        try:
            new_value = increment_use_case.execute(name, amount)
            return jsonify({
                "name": name,
                "value": new_value
            })
        except InvalidCounterOperationError as e:
            return jsonify({"error": str(e)}), 400
    
    @app.route("/api/v1/counters/<name>/reset", methods=["POST"])
    def reset_counter(name):
        reset_use_case.execute(name)
        return jsonify({
            "name": name,
            "value": 0
        })
    
    @app.route("/api/v1/counters", methods=["GET"])
    def get_all_counters():
        counters = get_all_use_case.execute()
        counters_data = {
            name: {"name": counter.name, "value": counter.value}
            for name, counter in counters.items()
        }
        return jsonify({"counters": counters_data})
    
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"error": "Not found"}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({"error": "Internal server error"}), 500
    
    return app