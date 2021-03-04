import requests
from sys import argv
from hashlib import sha1
from termcolor import colored


class PasswordChecker:
    def __init__(self):
        self.pass_list = argv[1:]
        if not self.pass_list:
            print(colored(f'Please provide args!!!\nEg. ', 'red') + colored(f'python3 ', 'green') + colored(f'{argv[0]} password123 PASSWORD 123456789', 'white'))

    def get_responce(self, hash5):
        """
        This function sends partial password of yours to server and retrieve the response from the server
        :param hash5:
        :return:
        """
        url = f'https://api.pwnedpasswords.com/range/{hash5}'
        response = requests.get(url)
        response_tuple = (response_list.split(':') for response_list in response.text.splitlines())
        return response_tuple

    def get_sha1(self, password):
        """
        This function converts given string to sha1 hash string
        :param password:
        :return:
        """
        encoded_password = password.encode('utf-8')
        sha1_password = sha1(encoded_password).hexdigest().upper()
        return sha1_password

    def split_hash(self, hash_value):
        """
        This function splits the given string and returns 2 data (First 5 char, Remaining char)
        :param hash_value:
        :return:
        """
        head, tail = hash_value[:5], hash_value[5:]
        return head, tail

    def check_password(self, response_tuple, actual_hash):
        """
        This function check the password from the tuple of lists and return number of occurrences
        :param response_tuple:
        :param actual_hash:
        :return:
        """
        for hash_data, count in response_tuple:
            if hash_data == actual_hash:
                return count

    def start_checking(self):
        """
        This function will start verifying you password from the database
        :return:
        """
        for passwd in self.pass_list:
            sha1_passwd = self.get_sha1(passwd)
            first5char, remaining_char = self.split_hash(sha1_passwd)
            response_tuple = self.get_responce(first5char)
            count = self.check_password(response_tuple, remaining_char)
            if count:
                print(colored(f'[-] Password: ', 'red') + colored(passwd, 'yellow') + colored(f' found ', 'red') + colored(count, 'yellow') + colored(f' times --> ', 'red') + colored(f'Password is not secure', on_color='on_red'))
            else:
                print(colored(f'[+] Password: ', 'green') + colored(passwd, 'yellow') + colored(' is unique --> ', 'green') + colored('Password is secure', on_color='on_green'))


pa = PasswordChecker()
pa.start_checking()
