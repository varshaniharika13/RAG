from app.evaluation.evaluate import run_evaluation


def test_eval_gate_sample_meets_threshold():
    score, report = run_evaluation()
    assert score >= 0.75
    assert report["total"] == 2
