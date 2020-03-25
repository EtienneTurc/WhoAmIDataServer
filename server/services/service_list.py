import pandas as pd

from helpers.service import is_callback
from helpers.redis_helpers import getData, setData
from services.utils.extract import extract_services, tag_mail
from services.utils.words import getWords
# from utils import tag_mail


@is_callback(["raw/google/mail"])
def google_mail_service(token):
    print("beginning processing for raw/google/mail")
    try:
        df_received = pd.DataFrame(getData(token, "raw.google.mail.received"))
        df_received['cat'] = df_received.headers.apply(tag_mail)
        res = extract_services(df_received)

        setData(token, "toDisplay.amazon.data", res["amazon"])
        setData(token, "toDisplay.amazon.meta.processing.google_mail", False)

        setData(token, "toDisplay.doctolib.data", res["doctolib"])
        setData(token, "toDisplay.doctolib.meta.processing", False)

        setData(token, "toDisplay.lydia.data", res["lydia"])
        setData(token, "toDisplay.lydia.meta.processing.google_mail", False)

        setData(token, "toDisplay.uberRides.data", res["uber_rides"])
        setData(token, "toDisplay.uberRides.meta.processing.google_mail", False)

        setData(token, "toDisplay.uberBikes.data", res["uber_jump"])
        setData(token, "toDisplay.uberBikes.meta.processing.google_mail", False)

        setData(token, "toDisplay.uberEats.data", res["uber_eats"])
        setData(token, "toDisplay.uberEats.meta.processing.google_mail", False)


        df_sent = pd.DataFrame(getData(token, "raw.google.mail.sent"))

        word_list = getWords(df_sent)

        setData(token, "toDisplay.words.data", word_list)
        setData(token, "toDisplay.words.meta.processing.google_mail", False)

        print(res)
        print(word_list)

    except Exception as err:
        print(err)
