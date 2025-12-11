from flask import Blueprint
from my_project.auth.controller.aggregate_controller import aggregate_column

aggregate_bp = Blueprint('aggregate', __name__)

aggregate_bp.route('/aggregate', methods=['GET'])(aggregate_column)
