import smtplib
import argparse
from email.mime.text import MIMEText
from twitter_class import *
from random import choice


def send_mail(user, pwd, to, subject, text):
    msg = MIMEText(text)
    msg['From'] = user
    msg['To'] = to
    msg['Subject'] = subject

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as smtp_server:
            print("[+] Connecting To Mail Server.")
            smtp_server.ehlo()

            print("[+] Starting Encrypted Session.")
            smtp_server.starttls()
            smtp_server.ehlo()

            print("[+] Logging Into Mail Server.")
            smtp_server.login(user, pwd)

            print("[+] Sending Mail.")
            smtp_server.sendmail(user, to, msg.as_string())

        print("[+] Mail Sent Successfully.")

    except Exception as e:
        print(f'[-] Sending Mail Failed.\n'
              f'[-] Exception: {e.__class__.__name__}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        usage='python3 send_spam.py -u TARGET_TWITTER -t TARGET_EMAIL '
              '-l GMAIL_LOGIN -p GMAIL_PASSWORD')
    parser.add_argument('-u', type=str, required=True, metavar='TARGET_TWITTER',
                        help='specify the Twitter handle')
    parser.add_argument('-t', type=str, required=True, metavar='TARGET_EMAIL',
                        help='specify the target email')
    parser.add_argument('-l', type=str, required=True, metavar='GMAIL_LOGIN',
                        help='specify the Gmail login')
    parser.add_argument('-p', type=str, required=True, metavar='GMAIL_PASSWORD',
                        help='specify the Gmail password')

    args = parser.parse_args()
    handle = args.u
    tgt = args.t
    _user = args.l
    _pwd = args.p

    print(f'[+] Fetching tweets from: {str(handle)}')
    spam_tgt = ReconPerson(handle)
    spam_tgt.get_tweets()
    print(f'[+] Fetching interests from: {str(handle)}')
    interests = spam_tgt.find_interests()
    print(f'[+] Fetching location information from: {str(handle)}')
    location = spam_tgt.twitter_locate('mlb-cities.txt')

    spam_msg = f"Dear {tgt}, "

    if location is not None:
        rand_loc = choice(location)
        spam_msg += f"It's me from {rand_loc}. "

    if interests['users'] is not None:
        rand_user = choice(interests['users'])
        spam_msg += f"{rand_user} said to say hello. "

    if interests['hashtags'] is not None:
        rand_hash = choice(interests['hashtags'])
        spam_msg += f"Did you see all the fuss about {rand_hash}? "

    if interests['links'] is not None:
        rand_link = choice(interests['links'])
        spam_msg += f"I really liked your link to: {rand_link}. "

    spam_msg += "Check out my link to http://evil.tgt/malware"
    print(f'[+] Sending Msg: {spam_msg}')

    send_mail(_user, _pwd, tgt, 'Re: Important', spam_msg)
