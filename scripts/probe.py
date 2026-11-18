import argparse
import json
import sys
from urllib.error import HTTPError, URLError
from urllib.request import urlopen

"""
The probe checks the HTTP status, product identity,
availability, and release version. 
Its exit code lets automation act on the result 
— 0 means verification passed, 
and 1 means it failed.

python scripts/probe.py --expected-version v1
python scripts/probe.py --expected-version v2
"""

def main():
    parser = argparse.ArgumentParser(
        description="Verify the product response through the proxy."
    )
    parser.add_argument("--expected-version", required=True)
    args = parser.parse_args()

    url = "http://127.0.0.1:8090/products/42"

    try:
        with urlopen(url, timeout=3) as response:
            status = response.status
            product = json.load(response)
    except HTTPError as error:
        print(f"FAIL: Product lookup returned HTTP {error.code}")
        return 1
    except (URLError, TimeoutError, OSError) as error:
        print(f"FAIL: Could not complete product lookup: {error}")
        return 1
    except (ValueError, UnicodeDecodeError) as error:
        print(f"FAIL: Invalid JSON response: {error}")
        return 1

    if not isinstance(product, dict):
        print("FAIL: Expected a JSON object")
        return 1

    if (
        status != 200
        or product.get("id") != 42
        or product.get("available") is not True
        or product.get("version") != args.expected_version
    ):
        print(f"FAIL: Unexpected product response: {product}")
        return 1

    print(f"PASS: Product 42 is available from {args.expected_version}")
    return 0


if __name__ == "__main__":
    sys.exit(main())