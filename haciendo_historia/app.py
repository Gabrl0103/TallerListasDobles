from flask import Flask, request, jsonify, render_template
from controllers.history_controller import BrowserHistoryController

app = Flask(__name__, template_folder="views", static_folder="static")

controller = BrowserHistoryController()

controller.add_entry("https://google.com", "Google - Buscador")
controller.add_entry("https://github.com", "GitHub - Hosting de Código")
controller.add_entry("https://stackoverflow.com", "Stack Overflow - Preguntas y Respuestas")
controller.add_entry("https://python.org", "Sitio Oficial de Python")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/history", methods=["GET"])
def get_history():
    reversed_param = request.args.get("reversed", "false").lower() == "true"
    if reversed_param:
        entries = controller.get_all_entries_reversed()
    else:
        entries = controller.get_all_entries()
    return jsonify({"entries": entries, "total": controller.get_length()})


@app.route("/api/history", methods=["POST"])
def add_entry():
    data = request.get_json()
    url = data.get("url", "").strip()
    title = data.get("title", "").strip()
    position = data.get("position", "end")
    index = data.get("index", None)

    if not url or not title:
        return jsonify({"error": "URL and title are required"}), 400

    if position == "start":
        entry = controller.add_entry_at_start(url, title)
    elif position == "index" and index is not None:
        entry = controller.insert_entry(int(index), url, title)
    else:
        entry = controller.add_entry(url, title)

    return jsonify({"message": "Entry added", "entry": entry, "total": controller.get_length()}), 201


@app.route("/api/history/<int:index>", methods=["DELETE"])
def remove_entry(index):
    removed = controller.remove_entry(index)
    if removed is None:
        return jsonify({"error": "Invalid index"}), 404
    return jsonify({"message": "Entry removed", "entry": removed, "total": controller.get_length()})


@app.route("/api/history/search", methods=["GET"])
def search_entry():
    keyword = request.args.get("q", "").strip()
    if not keyword:
        return jsonify({"error": "Search keyword is required"}), 400
    results = controller.search_entry(keyword)
    return jsonify({"results": results, "count": len(results)})


@app.route("/api/history/<int:index>", methods=["GET"])
def get_entry(index):
    entry = controller.get_entry_at(index)
    if entry is None:
        return jsonify({"error": "Invalid index"}), 404
    return jsonify({"entry": entry})


if __name__ == "__main__":
    app.run(debug=True)
