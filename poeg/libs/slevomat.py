import requests
import requests.adapters


class Client:
    """
    apply voucher error codes
    kód 1201 (HTTP status kód 400): nebyl zadán autentizační token nebo kód voucheru,
    kód 1202 (HTTP status kód 403): daný token není v databázi,
    kód 1203 (HTTP status kód 404): voucher s daným kódem neexistuje,
    kód 1204 (HTTP status kód 401): objednávka, na základě které byl voucher vystaven, nebyla zaplacena,
    kód 1205 (HTTP status kód 401): voucher už byl uplatněn,
    kód 1206 (HTTP status kód 401): voucher byl refundován,
    kód 1207 (HTTP status kód 401): objednávka nebo voucher byly stornovány,
    kód 1208 (HTTP status kód 401): akce už byla partnerovi vyúčtovaná; není možné uplatňovat další vouchery,
    kód 1209 (HTTP status kód 401): platnost voucherů této akce ještě nezačala nebo už skončila.
    kód 1211 (HTTP status kód 500): interní chyba serveru
    """

    url_pattern = 'https://www.slevomat.cz/api/voucher%s'

    def __init__(self, token):
        self.token = token
        self.http = requests.Session()

    def check_voucher(self, code):
        return self._get(self.url_pattern % 'check', code)

    def apply_voucher(self, code):
        return self._get(self.url_pattern % 'apply', code)

    def _get(self, url, code):
        params = dict(
            code=code,
            token=self.token,
        )
        r = self.http.get(url, params=params, timeout=3)
        r.raise_for_status()
        return r.json()
