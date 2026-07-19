from __future__ import annotations

import re


PATTERNS = [
    r"ignore (all )?(previous|prior|above) instructions",
    r"disregard (all )?(previous|prior|above) instructions",
    r"reveal (the )?(system|developer) prompt",
    r"print (the )?(system|developer) prompt",
    r"forget (your|the) rules",
    r"override (the )?(system|developer) instructions",
    r"jailbreak",
    r"忽略(之前|以上|所有).*指令",
    r"无视(之前|以上|所有).*指令",
    r"泄露.*(系统|开发者).*提示",
    r"输出.*(系统|开发者).*提示",
]


def detect_prompt_injection(text: str) -> list[str]:
    lowered = text.lower()
    return [pattern for pattern in PATTERNS if re.search(pattern, lowered, re.IGNORECASE)]


def has_prompt_injection(text: str) -> bool:
    return bool(detect_prompt_injection(text))
