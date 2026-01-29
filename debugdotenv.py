import os
from dotenv import load_dotenv, find_dotenv

def debug_environment():
    # 1. Kiểm tra xem có tìm thấy file .env nào không
    env_path = find_dotenv()
    if not env_path:
        print("❌ KHÔNG tìm thấy file .env ở bất kỳ thư mục cha nào.")
    else:
        print(f"✅ Đã tìm thấy file .env tại: {env_path}")

    # 2. Thử nạp và kiểm tra kết quả trả về
    # load_dotenv trả về True nếu nạp thành công ít nhất 1 file
    success = load_dotenv(env_path, override=True)
    
    if success:
        print("✅ load_dotenv() báo cáo nạp file thành công.")
    else:
        print("❌ load_dotenv() thất bại (có thể file trống hoặc sai định dạng).")

    # 3. Liệt kê các biến quan trọng
    print("\n--- Kiểm tra giá trị cụ thể ---")
    target_key = "GEMINI_API_KEY"
    value = os.getenv(target_key)
    
    if value:
        # Chỉ in ra 4 ký tự đầu để bảo mật
        print(f"🔑 {target_key}: {value[:4]}**** (Độ dài: {len(value)})")
    else:
        print(f"❌ {target_key}: KHÔNG TỒN TẠI trong môi trường.")

    # 4. (Tùy chọn) In toàn bộ các biến môi trường hiện có để đối soát
    # print("\n--- Tất cả biến môi trường (Cẩn thận khi xem) ---")
    # for k, v in os.environ.items():
    #     print(f"{k}={v}")

if __name__ == "__main__":
    debug_environment()