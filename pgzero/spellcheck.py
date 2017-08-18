from operator import itemgetter

from .game import PGZeroGame, positional_parameters


def distance(a, b):
    """Compute the distance between a and b.

    This is based on Damerau-Levenshtein distance, but we modify the cost
    of some edits, like insertion or removal of '_', or capitalisation changes.

    """
    d = {}
    la = len(a)
    lb = len(b)
    for i in range(la + 1):
        d[i, 0] = i
    for j in range(1, lb + 1):
        d[0, j] = j

    for i, ca in enumerate(a, start=1):
        for j, cb in enumerate(b, start=1):
            cost = int(ca != cb)
            if ca.lower() == cb.lower():
                subst_cost = 0
            else:
                subst_cost = 1.25 * cost
            insertion_cost = 0.7 if cb == '_' else 1.0
            deletion_cost = 0.7 if ca == '_' else 1.0
            d[i, j] = min(
                d[i - 1, j] + deletion_cost,  # deletion
                d[i, j - 1] + insertion_cost,  # insertion
                d[i - 1, j - 1] + subst_cost,  # substitution
            )
            if i > 1 and j > 1 and ca == b[j - 2] and a[i - 2] == cb:
                d[i, j] = min(
                    d[i, j],
                    d[i - 2, j - 2] + cost  # transposition
                )

    return d[la, lb]


def suggest(word, candidates):
    """Suggest good candidates as corrections for the given word.

    Suggestions will be ordered from best to worst.

    """
    candidates_with_score = [(c, distance(word, c)) for c in candidates]
    good_candidates = [(c, d) for c, d in candidates_with_score if d < 2.6]
    good_candidates.sort(key=itemgetter(1))
    # print(word, good_candidates)
    return [c for c, d in good_candidates]


def compare(have, want):
    """Compare a set of names we have (from user input) to those we want.

    This is a greedy algorithm that will take the best answer for each word
    in have in turn.

    """
    want = set(want)
    have = set(have)
    matched = want & have
    want -= matched
    have -= matched
    for w in have:
        suggestions = suggest(w, want)
        if suggestions:
            s = suggestions[0]
            yield w, s
            want.discard(s)


# The list of hooks we support
HOOKS = [
    'draw',
    'update',
] + list(PGZeroGame.EVENT_HANDLERS.values())


# The list of magic module-level constants
CONSTS = [
    'TITLE',
    'WIDTH',
    'HEIGHT',
    'ICON'
]

# Available parameters for each hook
# NB. update() takes one or zero positional parameter but we don't constrain
# the name.
#
# FIXME: These are from the documentation; there could be some missing here
VALID_PARAMS = {
    'on_mouse_down': ['pos', 'button'],
    'on_mouse_up': ['pos', 'button'],
    'on_mouse_move': ['pos', 'buttons', 'rel'],
    'on_key_up': ['key', 'mod'],
    'on_key_down': ['unicode', 'key', 'mod'],
    'draw': [],
    'on_music_end': [],
}


class InvalidParameter(Exception):
    """A parameter to a hook was invalid."""


class SpellCheckResult:
    def warn(self, msg, found, suggestion):
        print(msg.format(
            found=found,
            suggestion=suggestion
        ))

    def error(self, msg, found, suggestion):
        raise InvalidParameter(msg.format(
            found=found,
            suggestion=suggestion
        ))


def spellcheck(namespace, result=SpellCheckResult()):
    """Spell check the names in the given module.

    Where hooks are found, validate their positional parameters and offer
    suggestions where mispelled.

    """
    funcs = {}
    consts = []
    for name, val in namespace.items():
        if callable(val) and not isinstance(val, type):
            funcs[name] = val
        elif isinstance(val, (str, int)):
            consts.append(name)

    for found, suggestion in compare(funcs, HOOKS):
        result.warn(
            "Warning: found function named {found}: "
            "did you mean {suggestion}?",
            found, suggestion
        )

    for found, suggestion in compare(consts, CONSTS):
        result.warn(
            "Warning: found constant named {found}: "
            "did you mean {suggestion}?",
            found, suggestion
        )

    for name, handler in funcs.items():
        try:
            valid = VALID_PARAMS[name]
        except KeyError:
            continue
        else:
            param_names = positional_parameters(handler)
            for param in param_names:
                if param in valid:
                    continue
                suggestions = suggest(param, valid)
                if suggestions:
                    result.error(
                        "%s() hook accepts no parameter {found}; "
                        "did you mean {suggestion}?" % name,
                        param,
                        suggestions[0]
                    )
                else:
                    result.error(
                        "%s() hook accepts no parameter {found}" % name,
                        param, None
                    )
