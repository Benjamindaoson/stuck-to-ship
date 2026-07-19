__all__ = ["RAGASEvaluator", "EvalDatasetBuilder", "run_evaluation"]


def __getattr__(name):
    if name == "RAGASEvaluator":
        from evaluation.ragas_evaluator import RAGASEvaluator

        return RAGASEvaluator
    if name == "EvalDatasetBuilder":
        from evaluation.dataset_builder import EvalDatasetBuilder

        return EvalDatasetBuilder
    if name == "run_evaluation":
        from evaluation.pipeline import run_evaluation

        return run_evaluation
    raise AttributeError(name)
