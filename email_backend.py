from django.core.mail.backends.smtp import EmailBackend


class GmailEmailBackend(EmailBackend):

    def open(self):

        if self.connection:
            return False

        connection_params = {
            "local_hostname": "localhost"
        }

        if self.timeout is not None:
            connection_params["timeout"] = self.timeout

        self.connection = self.connection_class(
            self.host,
            self.port,
            **connection_params
        )

        self.connection.ehlo()

        if self.use_tls:
            self.connection.starttls(
                context=self.ssl_context
            )
            self.connection.ehlo()

        if self.username and self.password:
            self.connection.login(
                self.username,
                self.password
            )

        return True