import os
import os
import tempfile

from src.db import init_db, session_for_url
from src.models import Product
from logistics.models import Store, LogisticsStock, RestockRequest
from importlib import reload


def import_with_url(url):
    os.environ["DATABASE_URL"] = url
    import src.db as sdb
    reload(sdb)
    import logistics.cli as lcli
    import hq.cli as hcli
    reload(lcli)
    reload(hcli)
    return lcli, hcli


def setup_temp_db():
    db_fd, path = tempfile.mkstemp(suffix=".db")
    os.close(db_fd)
    url = f"sqlite:///{path}"
    init_db(url)
    return url


def test_product_sync_and_restock_flow():
    logistics_url = setup_temp_db()
    store1_url = setup_temp_db()
    store2_url = setup_temp_db()

    lcli, hcli = import_with_url(logistics_url)
    LogisticsSession = session_for_url(logistics_url)

    # create stores in logistics DB
    with LogisticsSession() as session:
        session.add_all([
            Store(id=1, name="S1", db_url=store1_url),
            Store(id=2, name="S2", db_url=store2_url),
        ])
        session.commit()

    # add product via HQ sync function
    product = Product(id=1, name="Widget", price=2.0, category="cat", stock=0)
    with LogisticsSession() as session:
        session.add(product)
        session.add(LogisticsStock(product_id=1, quantity=50))
        session.commit()
        stores = session.query(Store).all()
        # copy detached product data
        prod_copy = Product(
            id=product.id,
            name=product.name,
            price=product.price,
            category=product.category,
            stock=product.stock,
        )
    for store in stores:
        hcli.sync_product_to_store(store, prod_copy)

    # verify product exists in both stores
    for url in (store1_url, store2_url):
        StoreSession = session_for_url(url)
        with StoreSession() as s:
            assert s.get(Product, 1) is not None

    # store1 requests restock
    LogisticsSessionLocal = session_for_url(logistics_url)
    with LogisticsSessionLocal() as session:
        req = RestockRequest(store_id=1, product_id=1, quantity=5)
        session.add(req)
        session.commit()
        rid = req.id

    # approve request and propagate
    lcli.approve_request_by_id(rid)

    # check stock updated
    with LogisticsSession() as session:
        stock = session.query(LogisticsStock).first()
        assert stock.quantity == 45
    StoreSession = session_for_url(store1_url)
    with StoreSession() as s:
        prod = s.get(Product, 1)
        assert prod.stock == 5
