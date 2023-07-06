from services_api.api.LKP import ApiLKP
from services_api.api.boxberry_billing import Billing
from services_api.api.cdek import Cdek
from services_api.api.cdek_box import CdekBox
from services_api.api.dpd import Dpd
from services_api.api.pochta import Pochta
from services_api.api.sberlogistic import Sberlogistic


class Parser:
    api_lkp = ApiLKP()
    billing = Billing()
    cdek = Cdek()
    cdek_box = CdekBox()
    dpd = Dpd()
    pochta = Pochta()
    sberlogistic = Sberlogistic()