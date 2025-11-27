import torch
import sys
import os

def print_header(title):
    print(f"\n{'='*10} {title} {'='*10}")

print_header("環境基本資訊")
print(f"Python Version: {sys.version.split()[0]}")
try:
    print(f"PyTorch Version: {torch.__version__}")
    print(f"CUDA Version (PyTorch build): {torch.version.cuda}")
    print(f"CUDNN Version: {torch.backends.cudnn.version()}")
except Exception as e:
    print(f"PyTorch Basic Info Error: {e}")

print_header("CUDA 連線測試")
if torch.cuda.is_available():
    print("✅ CUDA is available!")
    try:
        device_count = torch.cuda.device_count()
        print(f"GPU Count: {device_count}")
        for i in range(device_count):
            name = torch.cuda.get_device_name(i)
            cap = torch.cuda.get_device_capability(i)
            print(f"GPU {i}: {name}")
            print(f" -> Compute Capability: {cap[0]}.{cap[1]}")
            
            # 關鍵檢查：Blackwell 架構通常是 10.0 或 9.x，檢查 PyTorch 是否支援
            arch_list = torch.cuda.get_arch_list()
            print(f" -> PyTorch Supported Archs: {arch_list}")
            
    except Exception as e:
        print(f"❌ Error getting device info: {e}")
else:
    print("❌ CUDA is NOT available. (Driver issue or Docker mapping issue)")

print_header("核心運算測試 (Kernel Check)")
# 這是最重要的一步，會直接觸發 'no kernel image' 錯誤
if torch.cuda.is_available():
    try:
        print("嘗試在 GPU 上建立 Tensor...")
        x = torch.tensor([1.0, 2.0]).cuda()
        print("嘗試進行乘法運算...")
        y = x * 2
        print(f"✅ 計算成功！結果: {y}")
        print("🎉 恭喜！PyTorch 與這張顯卡相容！")
    except RuntimeError as e:
        print(f"❌ 嚴重錯誤 (Kernel Error):")
        print(e)
        print("\n[分析] 這代表 PyTorch 沒有包含這張顯卡的指令集。")
        print("解決方案：必須升級 PyTorch 到 Nightly 版本，或更換 CUDA 版本。")
    except Exception as e:
        print(f"❌ 未知錯誤: {e}")

print_header("OnnxRuntime 檢查")
try:
    import onnxruntime as ort
    print(f"OnnxRuntime Version: {ort.__version__}")
    providers = ort.get_available_providers()
    print(f"Available Providers: {providers}")
    
    if 'CUDAExecutionProvider' in providers:
        print("✅ CUDAExecutionProvider 存在列表內")
        try:
            # 嘗試初始化，這會檢查 .so 檔 (libcublasLt 等) 是否存在
            sess_opt = ort.SessionOptions()
            print("✅ SessionOptions 初始化成功 (依賴庫正常)")
        except Exception as e:
            print(f"❌ 初始化失敗 (可能是 CUDA/CUDNN 版本不匹配): {e}")
    else:
        print("❌ 警告: CUDAExecutionProvider 不在列表內 (可能只能用 CPU)")
except ImportError:
    print("❌ OnnxRuntime 未安裝")