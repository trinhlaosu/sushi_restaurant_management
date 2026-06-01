from flask import jsonify, request


def get_json_data():
    return request.get_json() or {}


def data_response(data, status=200):
    return jsonify(data), status


def list_response(items, serializer=None, status=200):
    serializer = serializer or (lambda item: item.to_dict())
    return data_response([serializer(item) for item in items], status)


def success_response(message, status=200, **data):
    payload = {'message': message}
    payload.update(data)
    return data_response(payload, status)


def error_response(message, status=400):
    return data_response({'message': message}, status)


def service_error_response(error, status=400):
    return error_response(str(error), status)
