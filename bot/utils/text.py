from aiogram.utils.markdown import html_decoration


def escape_html(text: str | None) -> str:
    if not text:
        return "User"
    return html_decoration.quote(text)
