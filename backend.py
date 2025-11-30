import json
import os
from datetime import datetime
import random
import time
import uuid

USERS_FILE = "users.json"
SCORES_FILE = "user_scores.json"


def load_json(filename):
    if not os.path.exists(filename):
        return {}
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def save_json(filename, data):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


class JumbleGame:
    def __init__(self):
        self.WORDS = {
            "easy": {
                "tca": "cat",
                "hgint": "night",
                "nus": "sun",
                "koob": "book",
                "niar": "rain",
                "hsif": "fish",
                "pihs": "ship",
                "llab": "ball",
                "onom": "moon",
                "rmoo": "room",
                "rac": "car",
                "nep": "pen",
                "puc": "cup",
                "oehs": "shoe",
                "kcik": "kick",
                "sraw": "wars",
                "gift": "gift",
                "elppa": "apple",
                "mraf": "farm",
                "etre": "tree",
                "eshuo": "house",
                "drbi": "bird",
                "irtd": "dirt",
                "htea": "heat",
                "gnir": "ring",
                "albte": "table",
                "arkp": "park",
                "hcta": "chat",
                "yohne": "honey",
                "enh": "hen",
                "lkim": "milk",
                "frie": "fire",
                "rood": "door",
                "nechcik": "chicken",
                "elbatt": "battle",
                "rewofl": "flower",
                "olehl": "hello",
                "renocr": "corner",
                "cnael": "clean",
                "ylno": "only",
                "ung": "gun",
                "nemow": "women",
                "sdih": "dish",
                "sueom": "mouse",
                "drac": "card",
                "panl": "plan",
                "gins": "sing",
                "ngmorin": "morning",
                "enpicl": "pencil",
                "wodniw": "window"
            },
            "medium": {
                "albnetk": "blanket",
                "elciycb": "bicycle",
                "ehteatr": "theater",
                "ipcture": "picture",
                "vafsetil": "festival",
                "tcharee": "teacher",
                "lbraryi": "library",
                "ospitalh": "hospital",
                "otagcte": "cottage",
                "alrnten": "lantern",
                "alstcip": "plastic",
                "eapymnt": "payment",
                "cosuin": "cousin",
                "ebsiwte": "website",
                "hlotsec": "clothes",
                "rjuonal": "journal",
                "ctuainutnop": "punctuation",
                "ssproapt": "passport",
                "ripoatr": "airport",
                "satarndd": "standard",
                "treomupc": "computer",
                "dtsentu": "student",
                "gnienree": "engineer",
                "cceneis": "science",
                "arctrpo": "carport",
                "sialem": "emails",
                "pohtneele": "telephone",
                "solhoc": "school",
                "ubnemr": "number",
                "grpmaro": "program",
                "roldw": "world",
                "ncese": "scene",
                "tekwrno": "network",
                "ulrooc": "colour",
                "aereth": "heater",
                "girneo": "region",
                "tnnitree": "internet",
                "tfsoawre": "software",
                "sytems": "systems",
                "civrese": "service",
                "sreus": "users",
                "kban": "bank",
                "tnaurtesra": "restaurant",
                "dcitrore": "director",
                "camare": "camera",
                "noitazinagro": "organization",
                "niatmrofo": "formation",
                "ecadutoin": "education",
                "noitacilppa": "application",
                "noitacude": "education"
            },
            "hard": {
                "psnicououcs": "conspicuous",
                "cmseaelliouans": "miscellaneous",
                "nsuitneraieoq": "questionnaire",
                "dezrvouens": "rendezvous",
                "akeidliocospe": "kaleidoscope",
                "potojuxisnita": "juxtaposition",
                "cnoisseuron": "connoisseur",
                "iuqnstsetailne": "quintessential",
                "ubracurceay": "bureaucracy",
                "ysdcrasiniyo": "idiosyncrasy",
                "monoaptooeai": "onomatopoeia",
                "sesipuedalainq": "sesquipedalian",
                "cothymodi": "dichotomy",
                "psoperiaucis": "perspicacious",
                "inextrcabeli": "inextricable",
                "minganomaous": "magnanimous",
                "ubiuqtiuos": "ubiquitous",
                "anchrnotiacis": "anachronistic",
                "fedrbabgsalte": "flabbergasted",
                "lrteebgienl": "belligerent",
                "tpeihoycr": "hypocrite",
                "cotrdntinaciod": "contradiction",
                "enigmatci": "enigmatic",
                "ionecshoni": "incohesion",
                "yphsolihpo": "philosophy",
                "yctism": "mystic",
                "yrtilerb": "terribly",
                "roueprsi": "superior",
                "liatbiliy": "liability",
                "noitacmmunico": "communication",
                "gnisesd": "designs",
                "arheircyh": "hierarchy",
                "rpeetulap": "perpetual",
                "decoarted": "decorated",
                "ialzanteroi": "rationalize",
                "fpeulorusp": "purposeful",
                "lesoitnao": "isolation",
                "nciivonte": "invention",
                "tlihfuaf": "faithful",
                "rrceeta": "retrace",
                "dnetuts": "student",
                "ctfaula": "factual",
                "ralvbnleue": "vulnerable",
                "nlacianfi": "financial",
                "liotpioc": "politic",
                "icnceove": "conceive",
                "erpduor": "prouder",
                "yrtotihua": "authority",
                "ctceaaur": "accurate",
                "nvisenoi": "envision",
                "lasooppr": "proposal"
            }
        }

        self.name = None
        self.level = None
        self.total_words = 0
        self.word_pairs = []
        self.index = 0
        self.score = 0
        self.start_time = None
        self.time_taken_list = []
        self.user_correct_list = []
        self.history = []
        self.session_id = None
        self.hint_stage = 0
        self.logged_in_user = None

    def register_user(self, username: str, password: str):
        username = (username or "").strip()
        password = password or ""
        if not username or not password:
            return False, "Enter username and password."

        users = load_json(USERS_FILE)
        if username in users:
            return False, "User already exists!"

        users[username] = {"password": password}
        save_json(USERS_FILE, users)
        return True, "Registration successful! Please login."

    def login_user(self, username: str, password: str):
        username = (username or "").strip()
        password = password or ""
        if not username or not password:
            return False, "Enter username and password."

        users = load_json(USERS_FILE)
        if username not in users:
            return False, "User does not exist."

        if users[username]["password"] != password:
            return False, "Incorrect password."

        self.logged_in_user = username
        if self.name is None:
            self.name = username.title()
        return True, "Login successful!"

    def start_new_game(self, player_name: str, level: str, total_words: int):
        level = level.lower().strip()
        if level not in self.WORDS:
            raise ValueError("Invalid level")

        self.name = (player_name or "").title().strip()
        self.level = level
        self.total_words = max(1, min(total_words, 50))

        words_list = list(self.WORDS[self.level].items())
        if self.total_words > len(words_list):
            random.shuffle(words_list)
            chosen = words_list[:self.total_words]
        else:
            keys = list(self.WORDS[self.level].keys())
            sampled = random.sample(keys, self.total_words)
            chosen = [(k, self.WORDS[self.level][k]) for k in sampled]

        self.word_pairs = chosen
        self.index = 0
        self.score = 0
        self.start_time = time.time()
        self.time_taken_list = []
        self.user_correct_list = []
        self.history = []
        self.session_id = str(uuid.uuid4())
        self.hint_stage = 0

    def current_jumbled(self):
        if self.index < len(self.word_pairs):
            return self.word_pairs[self.index][0]
        return None

    def _current_correct(self):
        if self.index < len(self.word_pairs):
            return self.word_pairs[self.index][1]
        return None

    def get_hint(self):
        correct = self._current_correct()
        if correct is None:
            return None

        if self.hint_stage == 0:
            self.hint_stage = 1
            return correct[0:1]
        elif self.hint_stage == 1:
            self.hint_stage = 2
            return correct[2:3] if len(correct) >= 3 else ""
        else:
            return None

    def submit_answer(self, user_answer: str):
        correct_answer = self._current_correct()
        jumbled = self.current_jumbled()
        if correct_answer is None:
            return {"error": "No active word"}

        end_time = time.time()
        time_taken = end_time - (self.start_time or end_time)
        self.time_taken_list.append(time_taken)

        user_answer = (user_answer or "").lower().strip()
        correct_low = correct_answer.lower().strip()

        points = 0
        result_text = ""
        user_result = None

        if self.hint_stage == 0:
            if user_answer == correct_low and time_taken <= 5:
                user_result = True
                points = 10
                result_text = "Correct Answer!! (fast)"
            elif user_answer == correct_low and time_taken > 5:
                user_result = True
                points = 7
                result_text = "Correct Answer!! (slow)"
            elif user_answer == "":
                user_result = None
                points = 0
                result_text = f"{self.name} you quit this word."
            elif user_answer != correct_low:
                user_result = False
                points = -5
                result_text = "Wrong Answer!!"
        elif self.hint_stage == 1:
            if user_answer == correct_low:
                user_result = True
                points = 3
                result_text = "Correct Answer!! (after 1 hint)"
            elif user_answer == "":
                user_result = None
                points = 0
                result_text = f"{self.name} you quit this word."
            else:
                user_result = False
                points = -7
                result_text = "Wrong Answer!! (after 1 hint)"
        elif self.hint_stage >= 2:
            if user_answer == correct_low:
                user_result = True
                points = 2
                result_text = "Correct Answer!! (after 2 hints)"
            elif user_answer == "":
                user_result = None
                points = 0
                result_text = f"{self.name} you quit this word."
            else:
                user_result = False
                points = -10
                result_text = "Wrong Answer!! (after 2 hints)"

        if user_result is True:
            self.user_correct_list.append(correct_answer)

        self.score += points

        rec = {
            "index": self.index + 1,
            "jumbled": jumbled,
            "correct": correct_answer,
            "given": user_answer,
            "time_taken": round(time_taken, 3),
            "points": points,
            "result": result_text
        }
        self.history.append(rec)

        self.index += 1
        self.hint_stage = 0
        self.start_time = time.time()

        return {
            "user_result": user_result,
            "points": points,
            "correct_answer": correct_answer,
            "time_taken": round(time_taken, 3),
            "message": result_text,
            "history_record": rec
        }

    def is_over(self):
        return self.index >= len(self.word_pairs)

    def average_time(self):
        if not self.time_taken_list:
            return 0.0
        return sum(self.time_taken_list) / len(self.time_taken_list)

    def accuracy_percent(self):
        if self.total_words == 0:
            return 0.0
        return (len(self.user_correct_list) / self.total_words) * 100.0

    def save_scores_to_file(self):
        if self.logged_in_user is None:
            return False

        scores = load_json(SCORES_FILE)
        if self.logged_in_user not in scores:
            scores[self.logged_in_user] = []

        scores[self.logged_in_user].append({
            "level": self.level,
            "total_words": self.total_words,
            "score": self.score,
            "accuracy": round(self.accuracy_percent(), 2),
            "avg_time": round(self.average_time(), 3),
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

        save_json(SCORES_FILE, scores)
        return True

    def get_previous_scores(self):
        if self.logged_in_user is None:
            return []
        scores = load_json(SCORES_FILE)
        return scores.get(self.logged_in_user, [])