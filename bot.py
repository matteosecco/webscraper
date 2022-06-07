import smtplib
import csv


class myBot:
    def __init__(self, scraper, var, d, maildata=""):
        """ A myBot object is an object that has internal data, and is able to update
            that data and send the differences by email.
            Each instance can be customized by specifyng a data retriving function with its variables
            
            scraper (function): function that get a list of elements from the internet (for ex a list of properties)
                must return a LIST OF LIST
            var (list): parameters of the 'scraper' function
            d (string): directory to save data externally
            maildata (list): [user, psw, tolist] to send the mail, not sent if left on default """
        print("Creation of the bot")

        # creates object variables
        self.scraper = scraper
        self.vars = var
        self.dir = d
        self.mail = maildata

        # loads saved data
        try:
            with open(d, "r") as f:
                self.saved = list(csv.reader(f))
        # if the data is not saved
        except FileNotFoundError:
            self.saved = self.get()
            self.datawrite(self.saved)

    def get(self):
        """ Downloads the list of elements required through the fuction passed """

        return self.scraper(*self.vars)

    def datawrite(self, data):
        """ Writes a .csv file with the data requested """

        with open(self.dir, "w", newline='') as f:
            csv.writer(f).writerows(data)

    def update(self):
        """ Updates the data saved by downloading new data """
        print("Bot update")

        # new data
        newlist = self.get()

        # difference with the data saved
        diff = [x for x in newlist if x not in self.saved]

        if diff != []:
            # updates internal and external data
            self.saved = diff+self.saved
            self.datawrite(self.saved)

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
                print("New elements found, email sent")
        else:
            print("No new elements found")

