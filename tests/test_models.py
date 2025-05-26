# Module tests for ORM model repr methods.

from src.models import Product, Sale, SaleItem


def test_product_repr():
    """Product __repr__ returns expected format."""
    p = Product(name="TestProd", price=2.5, stock=10, category="TestCat")
    assert "<Product TestProd>" == repr(p)


def test_sale_and_saleitem_repr():
    """Sale and SaleItem __repr__ include IDs."""
    s = Sale()
    # repr should include the sale ID placeholder
    assert repr(s).startswith("<Sale ") and repr(s).endswith(">")
    item = SaleItem(sale_id=1, product_id=2, quantity=3, price=4.0)
    assert "sale=1" in repr(item) and "product=2" in repr(item)
