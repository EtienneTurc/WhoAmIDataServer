import pandas as pd

from helpers.service import is_callback
from helpers.redis_helpers import getData, setData
from services.utils.extract_services import extract_services
from utils import tag_mail
# from services.utils.extractWords import extractWords


@is_callback(["raw/google/mail"])
def google_mail_service(token):
    df = pd.DataFrame()
    # try:
    df = pd.DataFrame(getData(token, "raw.google.mail.received"))
    df['cat'] = df.headers.apply(tag_mail)
    res = extract_services(df)
    setData(token, "toDisplay.amazon.data", res["amazon"])
    setData(token, "toDisplay.amazon.meta.processing.google_mail", False)
    setData(token, "toDisplay.doctolib.data", res["doctolib"])
    setData(token, "toDisplay.lydia.data", res["lydia"])
    setData(token, "toDisplay.lydia.meta.processing.google_mail", False)
    print("data saved to redis")
    # except Exception as exception:
    #     print(exception)
    print("data was print")
