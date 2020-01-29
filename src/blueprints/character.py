from flask import (
	Blueprint, g, redirect, render_template, request, session, url_for
)

from ..db import get_db, query_db

from auth import login_required

bp = Blueprint('character', __name__, url_prefix='/character')

# Register
@bp.route('/<int:char_id>', methods=('GET', 'POST'))
@login_required
def register(char_id):
	return