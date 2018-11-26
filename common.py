import re


class Inhibitor():
    def __init__(self):
        self.reset()

    def reset(self):
        self.is_on = False

    def get_test_func(self):
        return self.test_off if self.is_on else self.test_on

    def test(self, s):
        if self.get_test_func()(s):
            self.is_on = not self.is_on
            return 1 if self.is_on else -1
        return 0


class InhibitorHTML(Inhibitor):
    def test_on(self, s):
        return s[0] == '<'

    def test_off(self, s):
        return s[0] == '>'


class InhibitorPercentFormatter(Inhibitor):
    def test_on(self, s):
        return s[0] == '%'

    def test_off(self, s):
        return re.match(r'[^\w\$%]', s[0])


class InhibitorUrl(Inhibitor):
    def test_on(self, s):
        return s.startswith('http')

    def test_off(self, s):
        return re.match(r'[^\w\-_~:/\?#\[\]@!\$&\'\(\)\*\+,;=`\.]', s[0])


class InhibitorUsernamePlaceholder(Inhibitor):
    def test_on(self, s):
        return re.match(r'^un\d', s)

    def test_off(self, s):
        return s[0].isspace()


class InhibitorDesktopFormatter(Inhibitor):
    def test_on(self, s):
        return s[0] == '{'

    def test_off(self, s):
        return s[0] == '}'


class InhibitorMarkdownTag(Inhibitor):
    def test_on(self, s):
        return s[0] == '['

    def test_off(self, s):
        return s[0] == ']'


def multi_sub(subject, subs):
    for pattern, repl in subs:
        subject = re.sub(pattern, repl, subject)
    return subject


def THRASH_SHIT_UP(s):
    return multi_sub(
        s.upper(),
        [
            ('ENGLISH', 'SLAYER'),
            (r'REMOVE\b', 'DELET'),
            (r'DELETE\b', 'DELET'),
            (r'C([IEY])', r'S\1'),
            (r'C([^HV]|\b)', r'K\1'),
            ('U', 'V'),
            ('W', 'VV'),
        ]
    )


def FVCK_SHIT_UP(inhibitors, s):
    output = ''
    # reset all the inhibitors so we can match from a fresh start
    for inhibitor in inhibitors:
        inhibitor.reset()

    # the number of inhibitors that are currently on
    inhibitor_count = 0
    while s:
        reached_end = True
        last_inhibitor_count = inhibitor_count
        # iterate through the remaining string
        for i in range(len(s)):
            # slice from the i-th character to the end
            # test each inhibitor
            for inhibitor in inhibitors:
                inhibitor_count += inhibitor.test(s[i:])

            # if something changed then we haven't reached the end of the string
            if inhibitor_count != last_inhibitor_count:
                # set a flag and break
                reached_end = False
                break

        # if we reached the end, then we need to output the last character of the string
        if reached_end:
            i += 1

        # the new output is everything from the beginning of the string to the i-th char
        # (excluding the character we broke on)
        new_output = s[:i]
        if last_inhibitor_count == 0:
            # if all the inhibitors WERE (ie from the time we started matching) off,
            # then we can THRASH SHIT UP \m/
            new_output = THRASH_SHIT_UP(new_output)
        output += new_output
        # remember the current inhibitor count so we know what to do with the next match
        last_inhibitor_count = inhibitor_count
        # slice away the characters that we added to output
        s = s[i:]
        # if we reached the end of the string without any matches then stop
        if reached_end:
            break

    return output
