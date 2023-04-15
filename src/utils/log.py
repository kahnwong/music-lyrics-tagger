import logging


log = logging.getLogger(__name__)
handler = logging.StreamHandler()

formatter = logging.Formatter("%(asctime)s - [%(levelname)s] - %(name)s - %(message)s")
handler.setFormatter(formatter)
log.addHandler(handler)

log.setLevel(logging.INFO)
