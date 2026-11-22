import builtins
import arabic_reshaper
from bidi.algorithm import get_display


def format_farsi(text: str) -> str:
    """
    متن فارسی را برای نمایش صحیح در ترمینال (بخصوص VS Code/Cursor) آماده می‌کند.
    """
    reshaped_text = arabic_reshaper.reshape(text)
    return get_display(reshaped_text)


# ذخیره‌ی نسخه اصلی print برای جلوگیری از حلقه بینهایت
if not hasattr(builtins, "_original_print"):
    builtins._original_print = print

def custom_print(*args, **kwargs):
    """هر متنی که قرار است چاپ شود را اول اصلاح می‌کند، بعد چاپ می‌کند."""
    new_args = []
    for arg in args:
        if isinstance(arg, str):
            reshaped_text = arabic_reshaper.reshape(arg)
            bidi_text = get_display(reshaped_text)
            new_args.append(bidi_text)
        else:
            new_args.append(arg)
    return builtins._original_print(*new_args, **kwargs)

# جایگزین کردن print در کل پروژه
builtins.print = custom_print
