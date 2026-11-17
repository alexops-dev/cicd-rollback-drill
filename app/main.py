import json
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer


RELEASE_VERSION = os.getenv("RELEASE_VERSION", "v1")
PRODUCT_LOOKUP_FAILS = os.getenv("PRODUCT_LOOKUP_FAILS", "false") == "true"
PORT = int(os.getenv("PORT", "8000"))
HOST = os.getenv("HOST", "127.0.0.1")

class CatalogHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/health":
            status = 200
            body = {"status": "ok", "version": RELEASE_VERSION}
        elif self.path == "/products/42":
            if PRODUCT_LOOKUP_FAILS:
                status = 500
                body = {
                    "error": "Product lookup unavailable",
                    "version": RELEASE_VERSION,
                }
            else:
                status = 200
                body = {
                    "id": 42,
                    "name": "Demo mechanical keyboard",
                    "available": True,
                    "version": RELEASE_VERSION,
                }
        else:
            status = 404
            body = {"error": "Endpoint not found", "version": RELEASE_VERSION}

        response = json.dumps(body).encode("utf-8")

        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(response)))
        self.end_headers()
        self.wfile.write(response)


if __name__ == "__main__":
    server = ThreadingHTTPServer((HOST, PORT), CatalogHandler)
    print(
        f"Catalog API {RELEASE_VERSION} listening on {HOST}:{PORT}",
        flush=True,
    )

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping Catalog API")
    finally:
        server.server_close()