import logging
import logging.handlers
import traceback
import re


class Logger:
    def __init__(self, name):
        self.logger = logging.getLogger(name)

    def warning(self, msg, obj: Exception=None):
        self.logger.warning(self.format_message(msg, obj))

    def info(self, msg, obj: Exception=None):
        self.logger.info(self.format_message(msg, obj))

    def error(self, msg, obj: Exception=None):
        self.logger.error(self.format_message(msg, obj))

    def debug(self, msg, obj: Exception=None):
        self.logger.debug(self.format_message(msg, obj))

    def log_chat(self, channel, sender, msg):
        if sender:
            self.info("[%s] %s: %s" % (channel, sender, self.format_chat_message(msg)))
        else:
            self.info("[%s] %s" % (channel, self.format_chat_message(msg)))

    def log_tell(self, direction, sender, msg):
        self.info("%s %s: %s" % (direction.capitalize(), sender, self.format_chat_message(msg)))

    def format_chat_message(self, msg):
        msg = re.sub("<a\s+href=\".+?[^\\\\]\">", "[link]", msg, 0, re.UNICODE | re.DOTALL)
        msg = re.sub("<a\s+href='.+?'>", "[link]", msg, 0, re.UNICODE | re.DOTALL)
        msg = re.sub("<font\s+.+?>", "", msg, 0, re.UNICODE)
        msg = re.sub("</font>", "", msg, 0, re.UNICODE)
        msg = re.sub("</a>", "[/link]", msg, 0, re.UNICODE)
        return msg

    def format_message(self, msg, obj):
        if obj:
            return msg + "\n" + traceback.format_exc()
        else:
            return msg
