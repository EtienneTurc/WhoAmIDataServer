import pandas as pd

from helpers.service import is_callback
from helpers.redis_helpers import getData, setData
from services.utils.extract_services import extract_services
from services.utils.extract_words import getWords
from utils import tag_mail


@is_callback(["raw/google/mail"])
def google_mail_service(token):
    print("beginning processing for raw/google/mail")
    df = pd.DataFrame()
    # try:
    df = pd.DataFrame(getData(token, "raw.google.mail.received"))
    df['cat'] = df.headers.apply(tag_mail)
    res = extract_services(df)

    setData(token, "toDisplay.amazon.data", res["amazon"])
    setData(token, "toDisplay.amazon.meta.processing.google_mail", False)

    setData(token, "toDisplay.doctolib.data", res["doctolib"])
    setData(token, "toDisplay.doctolib.meta.processing", False)

    setData(token, "toDisplay.lydia.data", res["lydia"])
    setData(token, "toDisplay.lydia.meta.processing.google_mail", False)

    setData(token, "toDisplay.uberRides.data", res["uber_rides"])
    setData(token, "toDisplay.uberRides.meta.processing.google_mail", False)

    setData(token, "toDisplay.uberBikes.data", res["uber_bicycle"])
    setData(token, "toDisplay.uberBikes.meta.processing.google_mail", False)

    setData(token, "toDisplay.uberEats.data", res["uber_eats"])
    setData(token, "toDisplay.uberEats.meta.processing.google_mail", False)

    word_list = getWords(df)

    setData(token, "toDisplay.words.data", word_list)
    setData(token, "toDisplay.words.meta.processing.google_mail", False)

    print(res)
    print(word_list)
