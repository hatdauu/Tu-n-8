

# import json

# # Đọc file JSON gốc
# file_path = r"D:\Document\HọcThayThe\Chuyên đề 2\Tuần 8\file_dulieuchuan.json"
# with open(file_path, "r", encoding="utf-8") as file:
#     data = json.load(file)

# # Trích xuất nội dung content
# contents = [{"id": idx + 1, "content": entry["content"]} for idx, entry in enumerate(data) if "content" in entry]

# # Lưu vào file JSON mới
# new_file_path = r"D:\Document\HọcThayThe\Chuyên đề 2\Tuần 8\dulieutaosinh.json"
# with open(new_file_path, "w", encoding="utf-8") as new_file:
#     json.dump(contents, new_file, ensure_ascii=False, indent=4)

# print(f"Dữ liệu đã được lưu vào: {new_file_path}")
