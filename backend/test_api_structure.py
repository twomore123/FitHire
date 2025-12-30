"""Test script to verify API structure"""

from app.main import app

print("✅ FastAPI app loaded successfully")
print(f"\nAvailable routes: {len(app.routes)} routes\n")

for route in app.routes:
    methods = getattr(route, "methods", set())
    path = getattr(route, "path", "N/A")
    if methods and path != "N/A":
        methods_str = ", ".join(sorted(methods))
        print(f"  [{methods_str}] {path}")
