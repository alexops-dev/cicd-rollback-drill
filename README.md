# CI/CD Rollback Drill

A practical lab for the future tech article for Engineering Blog on Medium Website **TBA**

## Goal

Demonstrate how a deployment can pass a health check while a user-facing operation fails. Detect the failure, restore the previous working release, and verify recovery through the same entry point.

The project uses a fictional product catalog with synthetic data. It runs locally with Docker Compose.

## Current state

Implemented and manually verified:

- A Python API with health and product endpoints.
- A Docker image with configurable release version and failure behavior.
- Stable and candidate containers managed by Docker Compose.
- An Nginx reverse proxy for manually switching traffic between releases.
- A Python probe that verifies the product response and release version.

Traffic switching and rollback are currently manual. The planned next steps are an automated drill controller, recorded results, and a GitHub Actions workflow.

## Architecture

Requests to `http://127.0.0.1:8090` pass through Nginx to the release selected in `proxy/default.conf`.

| Service | Direct local address | Behavior |
|---|---|---|
| Stable (`v1`) | http://127.0.0.1:8080 | Health and product lookup succeed |
| Candidate (`v2`) | http://127.0.0.1:8081 | Health succeeds; product lookup returns HTTP 500 |
| Proxy | http://127.0.0.1:8090 | Forwards requests to the selected release |

Both releases use the same image. The candidate’s `PRODUCT_LOOKUP_FAILS=true` setting deliberately simulates a runtime regression.

## Prerequisites

- Git
- Python 3.14
- Docker with a running engine
- Docker Compose
- curl

The commands below use a macOS or Linux shell.

## Run locally

```bash
git clone https://github.com/alexops-dev/cicd-rollback-drill.git
cd cicd-rollback-drill
python3 -m venv .venv
source .venv/bin/activate
docker compose up --build -d
```

With the proxy pointing to `stable`, verify the product response:

```bash
python scripts/probe.py --expected-version v1
```

Expected output:

```text
PASS: Product 42 is available from v1
```

## Perform the manual rollback drill

1. Edit `proxy/default.conf` and change the destination:

   ```nginx
   proxy_pass http://candidate:8000;
   ```

2. Validate the configuration:

   ```bash
   docker compose exec proxy nginx -t
   ```

3. If validation succeeds, reload Nginx:

   ```bash
   docker compose exec proxy nginx -s reload
   ```

4. Observe the successful health check:

   ```bash
   curl -i http://127.0.0.1:8090/health
   ```

   Expect HTTP 200 with version `v2`.

5. Run the product probe:

   ```bash
   python scripts/probe.py --expected-version v2
   ```

   Expect `FAIL: Product lookup returned HTTP 500` and exit code `1`.

6. Restore the destination in `proxy/default.conf`:

   ```nginx
   proxy_pass http://stable:8000;
   ```

7. Validate and, if successful, reload Nginx using the commands above.

8. Verify recovery:

   ```bash
   python scripts/probe.py --expected-version v1
   ```

   Expect a `PASS` message and exit code `0`.

The probe checks HTTP status, product identity, availability, and release version. To inspect its exit code, run `echo $?` immediately after the probe.

## Inspect and stop

View service status and logs:

```bash
docker compose ps
docker compose logs
```

Stop and remove the Compose containers and network:

```bash
docker compose down
```