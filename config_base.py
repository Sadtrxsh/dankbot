cooldown_normal = {
    "beg": 40,
    "search": 30,
    "fish": 45,
    "hunt": 60,
    "meme": 60,
    "gamble": 10,
    "blackjack": 10,
    "dep": 10,
    "withdraw": 10,
    "gift": 20,
    "give": 20,
    "steal": 30,
    "use": 5,
    "balance": 1,
    "trivia": 25,
    "buy": 5
}
cooldown_donator = {
    "beg": 25,
    "search": 20,
    "fish": 30,
    "hunt": 40,
    "meme": 45,
    "gamble": 5,
    "blackjack": 5,
    "dep": 0.5,
    "withdraw": 0.5,
    "gift": 10,
    "give": 10,
    "steal": 10,
    "use": 4,
    "balance": 0.5,
    "trivia": 20,
    "buy": 3
}

config = {
    # bot
    "max_reply_s": 10,
    "retry_on_timeout_s": 10,
    "search_preference": ["tree", "couch", "mailbox", "dresser", "discord", "bed", "attic", "laundromat", "grass", "shoe"],
    "modules": ["beg", "search", "give", "fish", "hunt", "pm"],
    "autodep_mode": "off",
    "autodep_threshold": (2000, 8000),
    "autodep_result": (800, 1600),

    # memer
    "bot_id": 270904126974590976,
    "bot_prefix": "pls"
}
