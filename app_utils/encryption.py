from django.core.mail import send_mail
from django.conf import settings

__encryptKey = {
    "a": "0",
    "b": "1",
    "c": "2",
    "d": "3",
    "e": "4",
    "f": "5",
    "g": "6",
    "h": "7",
    "i": "8",
    "j": "9",
    "k": "z",
    "l": "y",
    "m": "x",
    "n": "w",
    "o": "v",
    "p": "u",
    "q": "t",
    "r": "s",
    "s": "r",
    "t": "q",
    "u": "p",
    "v": "o",
    "w": "n",
    "x": "m",
    "y": "l",
    "z": "k",
    "1": "j",
    "2": "i",
    "3": "h",
    "4": "g",
    "5": "f",
    "6": "e",
    "7": "d",
    "8": "c",
    "9": "b",
    "0": "a",
    "!": "\"",
    "@": "\'",
    "#": "[",
    "$": "]",
    "%": "}",
    "^": "{",
    "&": "^",
    "*": "\\",
    "(": "/",
    ")": ".",
    "_": ",",
    "-": "?",
    "+": ">",
    "=": "<",
    "~": ";",
    "`": ":",
    ":": "`",
    ";": "~",
    "<": "=",
    ">": "+",
    "?": "-",
    ",": "_",
    ".": ")",
    "/": "(",
    "\\": "*",
    "^": "&",
    "{": "^",
    "}": "%",
    "]": "$",
    "[": "#",
    "\'": "@",
    "\"": "!",
}
__decryptKey = {
    "0": "a",
    "1": "b",
    "2": "c",
    "3": "d",
    "4": "e",
    "5": "f",
    "6": "g",
    "7": "h",
    "8": "i",
    "9": "j",
    "z": "k",
    "y": "l",
    "x": "m",
    "w": "n",
    "v": "o",
    "u": "p",
    "t": "q",
    "s": "r",
    "r": "s",
    "q": "t",
    "p": "u",
    "o": "v",
    "n": "w",
    "m": "x",
    "l": "y",
    "k": "z",
    "j": "1",
    "i": "2",
    "h": "3",
    "g": "4",
    "f": "5",
    "e": "6",
    "d": "7",
    "c": "8",
    "b": "9",
    "a": "0",
    "\"": "!",
    "\'": "@",
    "[": "#",
    "]": "$",
    "}": "%",
    "{": "^",
    "^": "&",
    "\\": "*",
    "/": "(",
    ".": ")",
    ",": "_",
    "?": "-",
    ">": "+",
    "<": "=",
    ";": "~",
    ":": "`",
    "`": ":",
    "~": ";",
    "=": "<",
    "+": ">",
    "-": "?",
    "_": ",",
    ")": ".",
    "(": "/",
    "*": "\\",
    "&": "^",
    "^": "{",
    "%": "}",
    "$": "]",
    "#": "[",
    "@": "\'",
    "!": "\"",
}


def encrypt(token: str) -> str:
    data_list = []
    for s in token:
        data_list.append(__encryptKey[s])
    return "".join(data_list)


def decrypt(key: str) -> str:
    data_list = []
    for s in key:
        data_list.append(__decryptKey[s])
    return "".join(data_list)


def sendEmailVerification(first_name: str, url: str, to: str) -> bool:

    result = send_mail("Verify your email for Nitrobills",
                       f"""
Hello from Nitrobills!

You're receiving this email because user {first_name} has given your email address to register an account on Nitrobills.

To confirm this is correct, go to {url}

Thank you for using Nitrobills!
""",
                       settings.EMAIL_HOST_USER,
                       [to])
    return result == 1
