"""Entry point for store CLI (delegates to view layer)."""

from .store import views

if __name__ == "__main__":
    views.main()
