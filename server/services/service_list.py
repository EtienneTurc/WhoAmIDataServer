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

        for service, redis_field, output in extract_services(df_received):
            setData(token, "{}.data".format(redis_field), output)
            setData(token, "{}.meta.processing.google_mail".format(
                redis_field), False)
            print("done processing {},  storing at {}".format(service, redis_field))

        df_sent = pd.DataFrame(getData(token, "raw.google.mail.sent"))

        word_list = getWords(df_sent)

        setData(token, "toDisplay.words.data", word_list)
        setData(token, "toDisplay.words.meta.processing.google_mail", False)

    except Exception as err:
        print(err)

        # faire décorateur pour chaque sous-service pour l'output
