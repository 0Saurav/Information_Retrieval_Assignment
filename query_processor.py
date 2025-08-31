from flask import Flask, request
import pickle, csv, string
from collections import defaultdict

app = Flask(__name__)

# -------------------------
# Load publications & index
# -------------------------
def load_publications(csv_path):
    publications = []
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            publications.append(row)
    return publications

def load_index(filepath="data/inverted_index.pkl"):
    with open(filepath, "rb") as f:
        return pickle.load(f)

def preprocess(text):
    text = text.lower()
    text = text.translate(str.maketrans("", "", string.punctuation))
    stopwords = {"the","and","of","in","on","for","a","an","with","to"}
    return [w for w in text.split() if w not in stopwords]

def search(query, publications, inverted_index):
    query_words = preprocess(query)
    scores = defaultdict(int)

    for word in query_words:
        if word in inverted_index:
            for pub_idx in inverted_index[word]:
                scores[pub_idx] += 1

    ranked_pub_indices = sorted(scores.keys(), key=lambda x: scores[x], reverse=True)
    results = [publications[idx] for idx in ranked_pub_indices]

    # Debug info in terminal
    print(f"[DEBUG] Query: {query}")
    print(f"[DEBUG] Preprocessed words: {query_words}")
    print(f"[DEBUG] Found {len(results)} results")

    return results

# -------------------------
# Web App
# -------------------------
csv_path = r"E:\Information_Retrieval_Assignment\data\publications.csv"
publications = load_publications(csv_path)
inverted_index = load_index()

@app.route("/", methods=["GET"])
def home():
    query = request.args.get("q", "")
    results = []

    if query:
        results = search(query, publications, inverted_index)

    html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>Publication Search</title>
        <!-- Bootstrap CSS -->
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    </head>
    <body class="bg-light">
        <div class="container py-5">
            <div class="card shadow-lg p-4">
                <h1 class="mb-4 text-center text-primary">Publication Search</h1>
                <form method="get" class="d-flex mb-4">
                    <input type="text" class="form-control me-2" name="q" value="{0}" placeholder="Enter search query">
                    <button type="submit" class="btn btn-primary">Search</button>
                </form>
                <hr>
    """.format(query)

    if query:
        if results:
            html += """
            <h3 class="text-success">Results ({0})</h3>
            <table class="table table-bordered table-striped mt-3">
                <thead class="table-dark">
                    <tr>
                        <th>#</th>
                        <th>Title</th>
                        <th>Authors</th>
                        <th>Link</th>
                    </tr>
                </thead>
                <tbody>
            """.format(len(results))
            for i, pub in enumerate(results, start=1):
                html += f"""
                <tr>
                    <td>{i}</td>
                    <td>{pub['title']}</td>
                    <td>{pub['authors']}</td>
                    <td><a href="{pub['link']}" target="_blank" class="btn btn-sm btn-outline-primary">View</a></td>
                </tr>
                """
            html += "</tbody></table>"
        else:
            html += "<p class='text-danger'><i>No results found.</i></p>"

    html += """
            </div>
        </div>
        <!-- Bootstrap JS -->
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    </body>
    </html>
    """
    return html

if __name__ == "__main__":
    app.run(debug=True)
