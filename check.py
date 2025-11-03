import random
import numpy as np
from textwrap import fill


CONGRATS_MSGS = (
    "Great job! 👾",
    "Well done! 🎉",
    "All good! 🤝",
    "Nice job! 🥳",
    "Great! 👌",
    "You are doing fine! ✌️",
    "Yeah! 😎",
    "Everything correct! 🤓",
    "Awesome! 💯",
    "Fantastic! 🚀",
    "Execellent! ✨",
)


def check_solution(test_values, global_vars=None):
    """Run a list of tests by comparing values. `test_values` is a list of tuples, where each tuple
    is one test.

    Parameters are:
    value_actual, value_expected, error_message, test_func, mode

    See `check_equal()` for details.

    """
    errors_ocurred = 0

    for test_value in test_values:
        if not check_equal(*test_value, global_vars=global_vars):
            errors_ocurred += 1
            print("\n")

    if errors_ocurred:
        plural_s = "s" if errors_ocurred > 1 else ""
        print(
            f"❌ {errors_ocurred} error{plural_s} occured! Please "
            "check the error messages above and your solution!"
        )
    else:
        # choose a reproducible random congrats message
        random.seed(str(test_values))
        congrats_msg = random.choice(CONGRATS_MSGS)

        # special casing for space invador exercise
        if "space_invader" in str(test_values):
            congrats_msg = CONGRATS_MSGS[0]

        print(f"✅ {len(test_values)} tests passed. {congrats_msg}")


def check_equal(
    value_actual, value_expected, error_message=None, test_func=None, mode=None, global_vars=None
):
    """Checks if `value_actual` matches `value_expected`. Returns True if it does or False
    otherwise.  Also Prints an error message if values do not match, but does not raise an
    exception.

    value_actual : any type or str
        if a str object is passed, it will be used for the error message and evaluated using
        global_vars
    value_expected : any type
        value compared to value_actual
    error_message : str
        printed if given, otherwise value_actual is used if of type str
    test_func : callable or str
        A function with two parameters, may return True, see `mode`.
        Default: try to round `value_actual` and use equality.
    mode : str
        one of "check" or "compare": "check" expects `test_func` to raise an exception,
        "compare" expects it to return True or False
    global_vars : dict
        a dict as returned by `globals()` to be passed to `eval()`

    """
    if not error_message:
        if not isinstance(value_actual, str):
            raise ValueError("no error message given, but value_actual is not of type str")
        error_message = f"invalid result for {value_actual}"

    if global_vars is not None and isinstance(value_actual, str):
        try:
            value_actual = eval(value_actual, global_vars)
        except NameError:
            value_actual = "undefined"

    # XXX mode is ignored if test_func is None
    if test_func is None:
        value_actual
        test_func = lambda x, y: (hasattr(x, "__round__") and (round(x, 2) == y)) or (x == y)
        mode = "compare"

    if mode == "compare":
        if not test_func(value_actual, value_expected):
            print("⚠️ Error:", fill(error_message, width=79))
            print(" Expected value: ", value_expected)
            print(" Actual value:   ", value_actual)
            return False
    elif mode == "check":
        try:
            test_func(value_actual, value_expected)
        except AssertionError as e:
            print("⚠️ Error:", fill(error_message, width=79))
            print(str(e).strip())
            return False
    else:
        raise ValueError(f"invalid test mode: {mode}")

    return True
