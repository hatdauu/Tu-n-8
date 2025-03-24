import json
from rouge_score import rouge_scorer

def load_json(file_path):
    """Đọc file JSON và xử lý lỗi nếu có."""
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"❌ Lỗi: Không tìm thấy tệp {file_path}")
        return []
    except json.JSONDecodeError:
        print(f"❌ Lỗi: Tệp {file_path} không đúng định dạng JSON")
        return []

def calculate_rouge_scores(reference_file, generated_file):
    """Tính điểm ROUGE giữa câu trả lời tham chiếu và câu trả lời sinh ra."""
    reference_data = load_json(reference_file)
    generated_data = load_json(generated_file)

    if not reference_data or not generated_data:
        print("❌ Dữ liệu không hợp lệ, dừng chương trình!")
        return []

    scorer = rouge_scorer.RougeScorer(["rouge1", "rouge2", "rougeL"], use_stemmer=True)
    scores = []

    for ref, gen in zip(reference_data, generated_data):
        ref_qa_pairs = ref.get("qa_pairs", [])
        gen_qa_pairs = gen.get("qa_pairs", [])

        for ref_pair, gen_pair in zip(ref_qa_pairs, gen_qa_pairs):
            ref_answer = ref_pair.get("answer", "").strip()
            gen_answer = gen_pair.get("answer", "").strip()
            
            if not ref_answer or not gen_answer:
                continue  

            score = scorer.score(ref_answer, gen_answer)
            scores.append(score)

    return scores

def calculate_avg_rouge(scores):
    """Tính trung bình ROUGE-1, ROUGE-2, ROUGE-L."""
    total_scores = {
        "rouge1": {"precision": 0, "recall": 0, "fmeasure": 0},
        "rouge2": {"precision": 0, "recall": 0, "fmeasure": 0},
        "rougeL": {"precision": 0, "recall": 0, "fmeasure": 0}
    }
    count = len(scores)

    for score in scores:
        for key in total_scores.keys():
            total_scores[key]["precision"] += score[key].precision
            total_scores[key]["recall"] += score[key].recall
            total_scores[key]["fmeasure"] += score[key].fmeasure

    avg_scores = {
        key: {metric: value / count for metric, value in total_scores[key].items()} if count > 0 else None
        for key in total_scores.keys()
    }

    return avg_scores

def save_scores_with_avg(scores, output_file="rouge_scores.txt"):
    """Lưu điểm ROUGE vào tệp, bao gồm cả trung bình."""
    avg_scores = calculate_avg_rouge(scores)

    with open(output_file, "w", encoding="utf-8") as file:
        for idx, score in enumerate(scores):
            file.write(f"QA Pair {idx + 1}:\n")
            file.write(f"ROUGE-1: {score['rouge1']}\n")
            file.write(f"ROUGE-2: {score['rouge2']}\n")
            file.write(f"ROUGE-L: {score['rougeL']}\n")
            file.write("-" * 40 + "\n")

        file.write("\n📊 **Trung bình ROUGE Scores:**\n")
        for key in avg_scores.keys():
            file.write(f"✅ {key.upper()} Precision: {avg_scores[key]['precision']:.4f}, "
                       f"Recall: {avg_scores[key]['recall']:.4f}, "
                       f"F1: {avg_scores[key]['fmeasure']:.4f}\n")

    print(f"✅ Kết quả đã lưu vào {output_file}")

# Chạy hàm chính với đường dẫn file
reference_file = "file_dulieuchuan.json"
generated_file = "dulieuoutput.json"

scores = calculate_rouge_scores(reference_file, generated_file)
if scores:
    save_scores_with_avg(scores, "rouge_scores.txt")
