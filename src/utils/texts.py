import os
from dataclasses import dataclass
from typing import Dict

import yaml

_LOCALES_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'locales')


def load_locale(lang='en') -> Dict:
    with open(os.path.join(_LOCALES_DIR, f'{lang}.yml'), 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


_ = load_locale('en')


@dataclass(frozen=True)
class Messages:
    START = _['messages']['start']
    HELP = _['messages']['help']
    LOADING = _['messages']['loading']
    NO_EMOJI = _['messages']['no_emoji']
    NO_ANIMATED_STICKER = _['messages']['no_animated_sticker']
    SUCCESS_TGS_ONLY = _['messages']['success_tgs_only']
    ERROR = _['messages']['error']
    INVALID_INPUT = _['messages']['invalid_input']
    PROCESSING_FAILED = _['messages']['processing_failed']


@dataclass(frozen=True)
class LogMessages:
    CONVERSION_ERROR = _['log']['conversion_error']


@dataclass(frozen=True)
class Buttons:
    GITHUB = _['buttons']['github']
    GITHUB_URL = _['buttons']['github_url']
    DEVELOPER = _['buttons']['developer']
    DEVELOPER_URL = _['buttons']['developer_url']
    PREVIEW = _['buttons']['preview']
