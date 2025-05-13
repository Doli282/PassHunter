"""Routes and views for the search blueprint."""
from flask import request, render_template, abort

from app.tools.opensearch import Client
from app.web.search import bp

@bp.route('/search', methods=['GET'])
def search() -> str:
    """
    Search in OpenSearch
    """
    query = request.args.get('q', '')
    count = -1
    matches = {}
    if query:
        try:
            client = Client()
            count, matches = client.search_term(query)
        except Exception:
            abort(500)
    return render_template('search/search.html', query=query, count=count, results=matches)