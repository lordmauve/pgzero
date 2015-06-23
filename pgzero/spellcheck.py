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
                subst_cost = 0.5 * cost
            else:
                subst_cost = 1.25 * cost
            insertion_cost = 0.7 if cb == '_' else 1.0
            deletion_cost = 0.7 if ca == '_' else 1.0
            d[i, j] = min(
                d[i - 1, j] + deletion_cost,  # deletion
                d[i, j - 1] + insertion_cost,  # insertion
                d[i - 1, j - 1] + subst_cost,  # substitution
            )
            if i > 1 and j > 1 and ca == b[j - 1] and a[i - 1] == cb:
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
    for w in have:
        if w in want:
            want.discard(w)
            continue

        suggestions = suggest(w, want)
        if suggestions:
            s = suggestions[0]
            yield w, s
            want.discard(w)


# The list of hooks we support
HOOKS = [
    'draw',
    'update',
] + list(PGZeroGame.EVENT_HANDLERS.values())


# FIXME: These are from the documentation; there could be some missing here
VALID_PARAMS = {
    'on_mouse_down': ['pos', 'button'],
    'on_mouse_up': ['pos', 'button'],
    'on_mouse_move': ['pos', 'button', 'rel'],
    'on_key_up': ['key', 'mod'],
    'on_key_down': ['unicode', 'key', 'mod'],
    'draw': [],
    'on_music_end': [],
}


class InvalidParameter(Exception):
    """A parameter to a hook was invalid."""


def spellcheck(mod):
    funcs = {}
    for name, val in vars(mod).items():
        if callable(val) and not isinstance(val, type):
            funcs[name] = val

    for found, suggestion in compare(funcs, HOOKS):
        print(
            "Warning: no hook named {found}: "
            "did you mean {suggestion}?".format(
                found=found,
                suggestion=suggestion
            )
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
                    raise InvalidParameter(
                        "%s() hook accepts no parameter %r; "
                        "did you mean %r?" % (
                            name, param, suggestions[0]
                        )
                    )
                else:
                    raise InvalidParameter(
                        "%s() hook accepts no parameter %r" % (
                            name, param
                        )
                    )
