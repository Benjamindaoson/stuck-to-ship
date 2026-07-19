"""Chitchat node for non-course queries."""

from core.nodes.generator import llm_generate_stream
from core.stream_queue import stream_queues
from utils.logger import logger


_CHITCHAT_SYSTEM_PROMPT = (
    "你是 StuckToShip，一个友好的 AI 工程课程助教。"
    "你可以和学习者闲聊、打招呼、回答日常问题，但请始终保持简洁、直接、友好的语气。"
    "如果学习者问课程相关的问题，引导他们补充具体概念、项目文件、报错原文或课程章节。"
    "回答要简短自然，不要长篇大论。"
    "请记住对话中用户告诉你的信息（如名字、偏好等），并在后续对话中自然引用这些信息。"
)


async def chitchat_node(state):
    """Stream a friendly response for non-course queries."""
    logger.info(f"[节点] chitchat: query='{state['query'][:50]}'")
    queue_id = state.get("_queue_id")
    full_answer = ""
    async for token in llm_generate_stream(
        query=state["query"],
        context_docs=[],
        system_prompt=_CHITCHAT_SYSTEM_PROMPT,
        conversation_history=state.get("conversation_history", []),
    ):
        full_answer += token
        await stream_queues.emit(queue_id, token)
    return {"answer": full_answer}
