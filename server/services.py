from mqtt_wrapper import is_callback


@is_callback(["google/mail", "google/people"])
def mail_service(token):
