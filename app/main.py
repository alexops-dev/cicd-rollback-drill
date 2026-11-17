import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer


class CatalogHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/health":
            status = 200
            body = {"status": "ok", "version": "v1"}
        elif self.path == "/products/42":
            status = 200
            body = {
                "id": 42,
                "name": "Demo mechanical keyboard",
                "available": True,
                "version": "v1",
            }
        else:
            status = 404
            body = {"error": "Endpoint not found"}

        response = json.dumps(body).encode("utf-8")

        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(response)))
        self.end_headers()
        self.wfile.write(response)


if __name__ == "__main__":
    server = ThreadingHTTPServer(("127.0.0.1", 8000), CatalogHandler)
    print("Catalog API running at http://127.0.0.1:8000", flush=True)

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping Catalog API")
    finally:
        server.server_close()