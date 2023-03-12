
from flask import Flask, jsonify, render_template, redirect, request, make_response


class Utils:
    @staticmethod
    def SuccessResponse(data, message):
        return make_response(jsonify(
            {"data": data, "message": message, "success": True}), 200)

    @staticmethod
    def ErrorResponse(message):
        return make_response(jsonify(
            {"message": message, "success": False}), 500)

    @staticmethod
    def NotFoundResponse(data, message):
        return make_response(jsonify(
            {"data": data, "message": message, "success": False}), 404)

    @staticmethod
    def UnauthorizedResponse(data):
        return make_response(jsonify(
            {"data": data, "message": 'unauthorized', "success": False}), 401)

    @staticmethod
    def BadRequestResponse(message):
        return make_response(jsonify(
            {"data": {}, "message": message, "success": False}), 400)
