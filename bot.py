import smtplib
import csv


class myBot:
    def __init__(self, scraper, varlist: list, d: str, maildata: str =""):
        """ A myBot is an object that has an internal data, and is able to update
            that data using the update coming from the function 'scraper'.
            Each instance can be customized by specifyng a data retriving function with its variables.
            The bot goes on internet when the instance is created only if the data is not present
            otherwise it waits for an update call.
            
            scraper: function that get a list of elements from the internet (for ex a list of properties)
                must return a LIST OF LIST
            varlist: parameters of the 'scraper' function
            d: directory to save data externally
            maildata: [user, psw, tolist] to send the mail, not sent if left on default """
        
        # creates object variables
        self.scraper = scraper
        self.vars = varlist
        self.dir = d
        self.mail = maildata

        # loads saved data
        try:
            with open(d, "r") as f:
                self.saved = list(csv.reader(f))
        # if the data is not saved, a new file is created
        except FileNotFoundError:
            self.saved = self._get()
            self._datawrite(self.saved)
        
    def _get(self) -> None:
        """ Downloads the list of elements required through the fuction passed """

        return self.scraper(*self.vars)

    def _datawrite(self, data: str) -> None:
        """ Writes a .csv file with the data requested """

        with open(self.dir, "w", newline='') as f:
            csv.writer(f).writerows(data)

    def update(self) -> bool:
        """ Updates the data saved by downloading new data """
        
        # gathers the new data using the provided function
        newlist = self._get()

        # difference with the data saved
        diff = [x for x in newlist if x not in self.saved]

        if diff != []:
            # updates internal and external data
            self.saved = diff+self.saved
            self._datawrite(self.saved)

            if self.mail != "":
                # creates the body
                body = "Subject: Nuovi elementi trovati\n\nNuovi elementi trovati dal bot con specifiche:"
                for el in self.vars:
                    body += " " + str(el)
                body += "\n\n"
                for el in diff:
                    body += " ".join(el) + "\n"

                # sends the email
                server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
                server.ehlo()
                server.login(self.mail[0], self.mail[1])
                server.sendmail(self.mail[0], self.mail[2], body.encode("utf-8"))
                server.close()
                return True
        else:
            return False
