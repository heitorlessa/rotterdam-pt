import requests
from tests import utils


def test_collect_payment(payment_api):
    endpoint = f"{payment_api}/collect"
    transaction = utils.build_fake_collect_payment_request()

    ret = requests.post(url=endpoint, data=transaction)
    ret.raise_for_status()
