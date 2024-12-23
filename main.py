from openai import OpenAI
import subprocess

# Cấu hình API Key
API_KEY = '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'  # Thay bằng API Key thực tế của bạn

# Tạo client OpenAI
client = OpenAI(api_key=API_KEY)

# Hàm gửi mã nguồn đến API của ChatGPT
def send_to_api(code):
    try:
        # Gửi yêu cầu qua client
        completion = client.chat.completions.create(
            model="gpt-4o-mini",  # Mô hình GPT-4o-mini
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {
                    "role": "user",
                    "content": f"Chuyển đổi mã Objective-C sau sang C++ vui lòng viết mỗi code:\n\n{code}"
                }
            ],
            max_tokens=2048  # Bạn có thể điều chỉnh số lượng token tối đa nếu cần
        )

        # Xử lý kết quả trả về và trả lại nội dung
        return completion['choices'][0]['message']['content']
    except Exception as e:
        print(f"Đã xảy ra lỗi: {e}")
        return None

# Hàm chuyển đổi mã C thành WebAssembly và tạo các file wasm, js, html
def compile_to_wasm(input_file):
    try:
        # Sử dụng emcc để biên dịch mã C thành WASM
        output_js = "output.js"
        output_wasm = "output.wasm"
        output_html = "output.html"

        # Biên dịch với emcc
        subprocess.run(
            [
                "emcc",
                input_file,
                "-o", output_html,  # Tạo file HTML
                "-s", "EXPORTED_FUNCTIONS=['_main']",
                "-s", "EXPORTED_RUNTIME_METHODS=['ccall', 'cwrap']"
            ],
            check=True
        )

        print(f"Đã tạo thành công các file: {output_js}, {output_wasm}, {output_html}")
    except subprocess.CalledProcessError as e:
        print(f"Lỗi khi biên dịch WebAssembly: {e}")
    except FileNotFoundError:
        print("emcc không được cài đặt. Hãy đảm bảo bạn đã cài đặt Emscripten và cấu hình đúng.")

# Hàm xử lý file Objective-C, gửi đến API, và ghi vào file C
def process_file(input_file):
    try:
        # Đọc nội dung từ file Objective-C
        with open(input_file, 'r') as file:
            code = file.read()

        # Gửi mã nguồn đến API và nhận kết quả
        result = send_to_api(code)
        
        if result:
            print("Mã C++ đã chuyển đổi từ mã Objective-C:\n")
            print(result)

            # Ghi kết quả vào file main.c
            with open("main.c", "w") as c_file:
                c_file.write(result)
            print("Mã C++ đã được ghi vào file main.c.")

            # Chuyển đổi mã C sang WebAssembly
            compile_to_wasm("main.c")
        else:
            print("Không thể nhận kết quả từ API.")
    except Exception as e:
        print(f"Đã xảy ra lỗi: {e}")

# Thực thi chương trình
input_file = "test/main.m"  # Đường dẫn đến file Objective-C của bạn
process_file(input_file)
