import pandas as pd
from evaluate import load

def evaluate_sim(pred_list, gt_list, truncate_pred=True, truncate_gt=False):
    if truncate_pred:
        pred_list_truncated = [pred.lstrip("\n").split("\n")[0].strip() for pred in pred_list]
        pred_list = pred_list_truncated
    if truncate_gt:
        gt_list_truncated = [gt.lstrip("\n").split("\n")[0].strip() for gt in gt_list]
        gt_list = gt_list_truncated

    bleu = load("bleu")
    rouge = load("rouge")
    bertscore = load("bertscore")
    bleu_results = bleu.compute(predictions=pred_list, references=gt_list)
    rouge_results = rouge.compute(predictions=pred_list, references=gt_list)
    bertscore_results = bertscore.compute(predictions=pred_list, references=gt_list, lang="en")
    p, r, f1 = [bertscore_results[k] for k in ["precision", "recall", "f1"]]
    evs = [
        bleu_results["bleu"],
        *[rouge_results[k] for k in ["rouge1", "rouge2", "rougeL", "rougeLsum"]],
        sum(p) / len(p),
        sum(r) / len(r),
        sum(f1) / len(f1),
    ]
    metrics = {metric_name: evs[i] for i, metric_name in enumerate(
        ["bleu", "rouge1", "rouge2", "rougeL", "rougeLsum", "bertscore_precision", "bertscore_recall", "bertscore_f1"]
    )}
    print(",".join([f"{ii * 100:.2f}" for ii in evs]))

    return metrics

# 加载xlsx文件
df = pd.read_excel("repo1.xlsx")

# 假设'language'是预测列，'response'是真实列
pred_list = df['response'].tolist()
gt_list = df['language'].tolist()

# 调用函数
metrics = evaluate_sim(pred_list, gt_list)

print(metrics)
