import random as rn
import itertools as iter
import json
import sqlite3
from datetime import datetime


class SakClass(object):
    """Setting up all letters and store them in the list"""

    def __init__(self):
        letters = {'Α': [12, 1], 'Β': [1, 8], 'Γ': [2, 4], 'Δ': [2, 4], 'Ε': [8, 1],
                   'Ζ': [1, 10], 'Η': [7, 1], 'Θ': [1, 10], 'Ι': [8, 1], 'Κ': [4, 2],
                   'Λ': [3, 3], 'Μ': [3, 3], 'Ν': [6, 1], 'Ξ': [1, 10], 'Ο': [9, 1],
                   'Π': [4, 2], 'Ρ': [5, 2], 'Σ': [7, 1], 'Τ': [8, 1], 'Υ': [4, 2],
                   'Φ': [1, 8], 'Χ': [1, 8], 'Ψ': [1, 10], 'Ω': [3, 3]
                   }
        alphabet = list(dict.keys(letters))
        self.all_letters = []
        for i in range(len(letters)):
            for j in range(letters[alphabet[i]][0]):
                self.all_letters.append(alphabet[i])

    def randomize_sak(self) -> None:
        """
        Ανακατεύει τα γράμματα στο σακουλάκι
        :return: None
        """
        rn.shuffle(self.all_letters)

    def get_letters(self) -> list:
        """
        Βγάζει 7 γράμματα από το σακουλάκι
        :return: list 7 γράμματα
        """
        sample = rn.sample(self.all_letters, 7)
        return sample

    def put_back_letters(self, letter) -> None:
        self.all_letters.append(letter)

    def remove_letter(self, letter) -> None:
        """
        Αφαιρεί το γράμμα από το σακουλάκι
        :param letter: Γράμμα
        :return:
        """
        self.all_letters.remove(letter)


class Player(object):
    """
    Η βασική κλάση που αντιπροσωπεύει τους παίκτες του παιχνιδιού. Περιέχει τα βασικά attributes που κληρονομούνται
    από τις κλάσεις Human και Computer
    """

    def __init__(self, sack):
        """
        Αρχικοποιεί τις μεταβλητές score και give_up. Το score κρατάει σκορ κατα την διάρκεια του παιχνιδιού ενώ το
        give_up ενημερώνει αν ο χρήστης ή ο υπολογιστής παραιτήθηκε
        :param sack: Το σακουλάκι του παιχνιδιού
        """
        self.sack = sack
        self.score = 0
        self.give_up = False

    def __repr__(self):
        # Χρήσιμο σε περιβάλλον debugging
        return '%s + %s' % (self.score, self.give_up)


class Human(Player):
    """Η κλάση που παίζει ο χρήστης. Κληρονομεί τη βασική Player"""

    def __init__(self, sack):
        super().__init__(sack)

    def __repr__(self):
        return '%s + %s' % (self.score, self.give_up)

    def play(self) -> None:
        """
        Ο αλγόριθμος που παίει ο παίκτης
        :return: None
        """
        print("------------------------------------------------------------------------")
        print("ΕΙΝΑΙ Η ΣΕΙΡΑ ΣΟΥ! ΓΡΑΜΜΑΤΑ ΣΤΟ ΣΑΚΟΥΛΑΚΙ " + str(len(self.sack.all_letters)))
        letters = self.sack.get_letters()
        print(letters)
        word = input("Δώσε τη λέξη: ")
        # Αν ο παίκτης πατήσει '' τότε το παιχνίδι σταματάει και ο πάικτης χάνει
        # Όταν ο παίκτης παραιτείται το σκόρ του είναι πάντα -1
        if word == 'q':
            self.give_up = True
            self.score = -1
            return
        # Αν ο παίκτης πατήσει 'p' τελειώνει ο γύρος του με πόντους 0
        if word == 'p':
            return
        # If player plays a 1 letter word the turn must end
        if len(word) < 2:
            print("Η ΛΕΞΗ ΠΡΕΠΕΙ ΝΑ ΕΧΕΙ ΠΕΡΙΣΣΟΤΕΡΑ Η 2 ΓΡΑΜΜΑΤΑ")
            return
        word_tuple = tuple(word)
        p = list(iter.permutations(letters, len(word)))  # all possible combinations
        is_accepted = False
        for i in range(len(p)):
            if word_tuple in p:
                is_accepted = True
                break
            else:
                print("ΑΚΥΡΗ ΛΕΞΗ! ΣΥΝΟΛΟ: " + str(self.score))
                return
        if is_accepted:
            exists = False
            with open('worddic.json', 'r') as f:
                word_dict = json.load(f)
                if word in word_dict:
                    exists = True
                    self.score += word_dict[word]
                    # Remove the valid letters from sak if and only if word is valid
                    for i in word:
                        self.sack.remove_letter(i)
                    print("ΤΕΛΕΙΑ! ΠΟΝΤΟΙ: " + str(word_dict[word]) + " ΣΥΝΟΛΟ: " + str(self.score))
                else:
                    print("Η ΛΕΞΗ ΔΕΝ ΥΠΑΡΧΕΙ ΣΤΟ ΛΕΞΙΚΟ ΣΥΝΟΛΟ: " + str(self.score))


class Computer(Player):
    """Η κλάση που παίζει ο υπολογιστής. Κληρονομεί τη βασική Player"""

    def __init__(self, sack):
        super().__init__(sack)

    def __repr__(self):
        return '%s + %s' % (self.score, self.give_up)

    def play(self, level: str) -> None:
        """
        Παίζει ο υπολογιστής ανάλογα με τον αλγόριθμο που του δώσαμε
        :param level: Επίπεδο δυσκολίας (αλγόριθμος) ανάμεσα σε Min Max Fail
        :return: None
        """
        print("------------------------------------------------------------------------")
        print("ΕΙΝΑΙ Η ΣΕΙΡΑ ΤΟΥ ΥΠΟΛΟΓΙΣΤΗ! ΓΡΑΜΜΑΤΑ ΣΤΟ ΣΑΚΟΥΛΑΚΙ " + str(len(self.sack.all_letters)))
        if level == "max":
            try:
                words = self.load_all_possible_words(self.sack.get_letters())
                final_word = self.max_algorithm(words)
                for i in final_word[0]:
                    self.sack.remove_letter(i)
                self.score += final_word[1]

                print("ΛΕΞΗ: " + str(final_word[0]) + " ΠΟΝΤΟΙ: " + str(final_word[1]) + " ΣΥΝΟΛΟ: " + str(self.score))
            except ValueError as err:
                print("Ο ΥΠΟΛΟΓΙΣΤΗΣ ΔΕΝ ΜΠΟΡΕΣΕ ΝΑ ΒΡΕΙ ΛΕΞΗ! ΚΕΡΔΙΣΕΣ ΤΗΝ ΠΑΡΤΙΔΑ")
                self.score = -1
                self.give_up = True
        elif level == "fail":
            try:
                words = self.load_all_possible_words(self.sack.get_letters())
                final_word = self.fail_algorithm(words)
                for i in final_word[0]:
                    self.sack.remove_letter(i)
                self.score += final_word[1]

                print("ΛΕΞΗ: " + str(final_word[0]) + " ΠΟΝΤΟΙ: " + str(final_word[1]) + " ΣΥΝΟΛΟ: " + str(self.score))
            except ValueError as err:
                print("Ο ΥΠΟΛΟΓΙΣΤΗΣ ΔΕΝ ΜΠΟΡΕΣΕ ΝΑ ΒΡΕΙ ΛΕΞΗ! ΚΕΡΔΙΣΕΣ ΤΗΝ ΠΑΡΤΙΔΑ")
                self.score = -1
                self.give_up = True
        elif level == "min":
            try:
                words = self.load_all_possible_words(self.sack.get_letters())
                final_word = self.min_algorithm(words)
                for i in final_word[0]:
                    self.sack.remove_letter(i)
                self.score += final_word[1]

                print("ΛΕΞΗ: " + str(final_word[0]) + " ΠΟΝΤΟΙ: " + str(final_word[1]) + " ΣΥΝΟΛΟ: " + str(self.score))
            except ValueError as err:
                print("Ο ΥΠΟΛΟΓΙΣΤΗΣ ΔΕΝ ΜΠΟΡΕΣΕ ΝΑ ΒΡΕΙ ΛΕΞΗ! ΚΕΡΔΙΣΕΣ ΤΗΝ ΠΑΡΤΙΔΑ")
                self.score = -1
                self.give_up = True

    @staticmethod
    def max_algorithm(words: dict) -> tuple:
        """
        Ο υπολογιστής πάντα βρίσκει την λέξη με το μαγαλύτερο σκορ
        :param words: dict Όλες οι πιθανές λέξεις που μπορεί να παίξει από το λεξικό
        :return: tuple επιστρέψει ένα tuple με την λέξη και τους πόντους της
        """
        if len(words) == 0:
            raise ValueError("No words")
        words_list = []
        points = 0
        for word in words:
            if words[word] > points:
                points = words[word]
        for word in words:
            if words[word] == points:
                words_list.append(word)
        if len(words_list) == 0:
            raise ValueError("No words in dictionary")
        if len(words_list) == 1:
            final_word = (words_list[0], points)
            return final_word
        if len(words_list) > 1:
            final = rn.choice(words_list)
            final_word = (final, points)
            return final_word

    @staticmethod
    def min_algorithm(words: dict) -> tuple:
        """
        Ο υπολογιστής πάντα βρίσκει την λέξη με το μικρότερο σκορ
        :param words: dict Όλες οι πιθανές λέξεις που μπορεί να πάιξει από το λεξικό
        :return: tuple επιστρέψει ένα tuple με την λέξη και τους πόντους της
        """
        if len(words) == 0:
            raise ValueError("No words in dictionary")
        words_list = []
        points = 200  # Random high value word
        for word in words:
            if words[word] < points:
                points = words[word]
        for word in words:
            if words[word] == points:
                words_list.append(word)

        if len(words_list) == 1:
            final_word = (words_list[0], points)
            return final_word
        if len(words_list) > 1:
            final = rn.choice(words_list)
            final_word = (final, points)
            return final_word

    @staticmethod
    def fail_algorithm(words: dict) -> tuple:
        """
        Ο υπολογιστής προσπαθεί να προσομοιώσει την ανθρώπινη συμπεριφορά.
        :param words: dict Όλες οι πιθανές λέξεις που μπορεί να πάιξει από το λεξικό
        :return: tuple επιστρέψει ένα tuple με την λέξη και τους πόντους της
        """

        # Σε αυτόν τον αλγόριθμο θα προσπαθήσουμε να μιμηθούμε πως παίζει το παίχτης Υποθέτουμε ότι όσο πιο πολλά
        # γράμματα έχει η λέξη τόσο πιο δύσκολο είναι να την βρει. Άρα  το ευκολότερο είναι να δώσει μια λέξη με 2
        # γράμματα όμως και εδώ υπάρχει πρόβλημα. Το να βρεις μια λέξη με 2 γράμματα είναι αρκετά εύκολο και συνήθως ο
        # παίκτης θα προσπαθήσει να βρει μια πιο δύσκολη με περισσότερα γράμματα. Οπότε προσπαθώντας να προσομοιώσουμε
        # την ανθρώπινη λογική θα πρέπει να υπολογίσουμε τις πιθανότητες. Ορίζοντας σαν την μικρότερη πιθανότητα να
        # είναι λέξη με 7 ή με 2 γράμματα έχουμε την παρακάτω λίστα

        chances = [7, 2, 6, 6, 3, 3, 5, 5, 5, 4, 4, 4]

        # Διαλέγουμε μία επιλογή με περισσότερες πιθανότητητες να έχει λέξη με 4 ή 5 γραμματα

        choice = rn.choice(chances)
        # breakpoint()

        # βρίσκουμε όλες τις λέξεις με {{choice}} γράμματα

        words_list = []
        while True:
            for word in words:
                if len(word) == choice:
                    words_list.append(word)
                else:
                    continue
            if not words_list:
                for i in chances:
                    if i == choice:
                        chances.remove(i)
                if len(chances) == 0:
                    raise ValueError("Cant find word")
                choice = rn.choice(chances)
            else:
                break

        if len(words_list) == 1:
            final_word = (words_list[0], words[words_list[0]])
            return final_word
        if len(words_list) > 1:
            temp = rn.choice(words_list)
            final_word = (temp, words[temp])
            return final_word

    @staticmethod
    def load_all_possible_words(letters: list) -> dict:
        """
        Αποθηκεύει στο λεξικό όλες τις λέξεις που προκύπτουν από τον συνδιασμό των γραμμάτων
        :param letters: 7 γράμματα από το σακουλάκι
        :return: dict Όλες τις λέξεις που προκύπτουν από τα 7 γράμματα (letters)
        """
        print(letters)
        st_list = []
        words = {}
        n = 7

        while n >= 2:
            p = list(iter.permutations(letters, n))
            for i in p:
                st_list.append("".join(i))
            with open('worddic.json', 'r') as f:
                word_dict = json.load(f)
                for word in st_list:
                    if word in word_dict:
                        words[word] = word_dict[word]
                    else:
                        continue
            n = n - 1
        return words


class Game(object):
    """
    Η βασική κλάση του παιχνιδιού. Περιέχει όλα τα αντικείμενα που χρειάζονται για να ξεκινήσει, να τρέξει και να
    τελειώσει ομαλά μια παρτίδα. Δημιουργεί αντικείμενα από τις κλάσεις  Human, Computer και SakClass.
    """

    def __init__(self):
        self.sak = SakClass()
        self.human = None
        self.computer = None
        self.rounds = 0
        self.level = None

    def setup(self, level: str) -> None:
        """
        Προετοιμάζει την παρτίδα θέτοντας τις σωστές τιμές στις μεταβλητές
        :param level: Το επίπεδο δυσκολίας του παιχνιδιού
        :return: None
        """
        self.human = Human(self.sak)
        self.computer = Computer(self.sak)
        self.human.score = 0
        self.computer.score = 0
        self.level = level

    def run(self) -> None:
        """
        Τρέχει την παρτίδα και σε κάθε γύρο ανακατεύει το σακουλάκι
        :return: None
        """
        while not self.check_end():
            self.human.play()
            # Αν ο παίχτης πατήσει 'q' το παιχνίδι πρέπει να σταματήσει χωρίς να πάιξει ο υπολογιστής
            if self.check_end():
                break
            self.sak.randomize_sak()
            self.computer.play(self.level)
            self.sak.randomize_sak()
            # Μετράει τους γύρους
            self.rounds += 1

        self.end()

    def check_end(self) -> bool:
        """
        Τσεκάρει πότε το παιχνίδι πρέπει να τελειώσει σύμφωνα με τα παρακάτω κριτήρια
        :return: bool (True) αν το παιχνίδι πρέπει να σταματήσει
        """
        # Το παιχνίδι τελειώνει όταν στο σακουλάκι μείνουν λιγότερα από 7 γράμματα
        if len(self.sak.all_letters) < 7:
            return True
        if self.human.give_up:
            return True
        if self.computer.give_up:
            return True
        return False

    def end(self) -> None:
        """
        Εμφανίζει όλα τα στοιχεία (σκορ, γύρους) και ανακηρύσσει τον νικητή. Στο τέλος αποθηκεύει το αποτέλεσμα στη
        βάση δεδομένων
        :return: None
        """
        # Count starts at 0 so,
        rounds = self.rounds + 1

        if self.human.score > self.computer.score:
            print("------------------------------------------------------------------------")
            print("ΣΥΓΧΑΡΗΤΗΡΙΑ ΚΕΡΔΙΣΕΣ!")
            print("Your score:     " + str(self.human.score))
            print("Computer score:  " + str(self.computer.score))
            print("Γύροι του παίκτηκαν: " + str(self.rounds))
            self.save_scores(self.human.score, self.computer.score, True, rounds)
            # Reset the rounds
            self.rounds = 0
        elif self.human.score == self.computer.score:
            print("------------------------------------------------------------------------")
            print("ΤΟ ΠΑΙΧΝΙΔΙ ΗΡΘΕ ΙΣΟΠΑΛΙΑ")
            print("Your score:     " + str(self.human.score))
            print("Computer score:  " + str(self.computer.score))
            print("Γύροι του πάικτηκαν: " + str(rounds))
            self.save_scores(self.human.score, self.computer.score, False, rounds)
            # Reset the rounds
            self.rounds = 0
        else:
            print("------------------------------------------------------------------------")
            print("ΔΥΣΤΥΧΩΣ ΕΧΑΣΕΣ")
            print("Your score:     " + str(self.human.score))
            print("Computer score:  " + str(self.computer.score))
            print("Γύροι του πάικτηκαν: " + str(rounds))
            self.save_scores(self.human.score, self.computer.score, False, rounds)
            # Reset the rounds
            self.rounds = 0

    @staticmethod
    def save_scores(human_score: int, computer_score: int, human_won: bool, rounds: int) -> None:
        """
        Εκτελεί τις απαραίτητες ενέργειες ώστε να αποθηκεύσει τα δεδομένα στην βάση. Ανοίγει μια καινούργια σύνδεση με
        τη βάση και ελέγχει αν υπάρχει κανένα πρόβλημα
        :param human_score: Τελικό σκορ του παίκτη
        :param computer_score: Τελικό σκορ του υπολογιστή
        :param human_won: Αν κέρδισε ο παίκτης
        :param rounds: Πόσοι γύροι παίκτηκαν
        :return: None
        """
        connection = None
        #  Formatted timestamp
        now = datetime.utcnow().strftime("%d %b %Y  %H:%M")
        try:
            connection = sqlite3.connect('database.db')
            cursor = connection.cursor()
            cursor.execute('INSERT INTO score(human_score, computer_score, human_won, rounds, date) '
                           'VALUES(?, ?, ?, ?, ?)',
                           (human_score, computer_score, human_won, rounds, now))
            connection.commit()
            print("Game Saved")
        except sqlite3.DatabaseError as err:
            print(err)
        except sqlite3.Error as err:
            print(err)
        else:
            connection.close()


class Score(object):
    """
    Η κλάση παρουσιάζει τα στατιστικά του παίκτη στην κεντρική καρτέλα ΣΚΟΡ του παιχνιδιού
    """

    def __init__(self):
        connection = None
        try:
            connection = sqlite3.connect('database.db')
            cursor = connection.cursor()
            temp = cursor.execute('SELECT * FROM score')
            self.data = temp.fetchall()
        except sqlite3.DatabaseError as err:
            print(err)
        except sqlite3.Error as err:
            print(err)
        else:
            connection.close()

    def print_all(self) -> None:
        """
        Εμφανίζει στην κονσόλα όλα τα προηγούμενα παιχνίδια, το σκορ καθώς και την ημερομηνία-ώρα που παίχτηκε
        :return: None
        """
        for el in self.data:
            print("ΠΑΙΚΤΗΣ " + str(el[1]) + " - " + str(el[2]) + " Η/Υ" + " ΣΤΙΣ " + el[5])

    def won_rate(self) -> float:
        """
        Υπολογίζει το ποσοστό νικών/ηττών %
        :return: float Ποσοστό
        """
        won_games = 0
        total_games = len(self.data)
        for el in self.data:
            if el[3] == 1:
                won_games += 1
            else:
                continue
        try:
            won_rate = (won_games / total_games) * 100
        except ZeroDivisionError:
            won_rate = 0
        return won_rate

    def calculate_average(self) -> float:
        """
        Υπολογίζει το μέσο όρο πόντων του παίκτη ανά παιχνίδι
        :return: float Ποσοστό
        """
        sum = 0
        count = len(self.data)
        for el in self.data:
            sum += el[1]
        try:
            avg = sum / count
        except ZeroDivisionError:
            avg = 0
        return avg

    def best_score(self) -> int:
        """
        Υπολογίζει το καλύτερο σκόρ του πάικτη από όλες τις παρτίδες
        :return: int High Score
        """
        best_score = 0
        for el in self.data:
            if el[1] > best_score:
                best_score = el[1]
            else:
                continue
        return best_score
