"""
Environment setup verification script
检查环境配置和依赖安装状态
"""

import sys
import subprocess
import importlib
from typing import Dict, List, Tuple
import os

def check_python_version() -> bool:
    """检查Python版本"""
    version = sys.version_info
    if version.major == 3 and 9 <= version.minor <= 12:  # Updated to include 3.12
        print(f"✓ Python版本: {version.major}.{version.minor}.{version.micro}")
        if version.minor == 12:
            print("  注意: Python 3.12 可能存在兼容性问题，推荐使用 3.9-3.11")
        return True
    else:
        print(f"✗ Python版本不兼容: {version.major}.{version.minor}.{version.micro}")
        print("  推荐版本: Python 3.9-3.11")
        return False

def check_package_installation() -> Dict[str, bool]:
    """检查包安装状态"""
    required_packages = {
        'numpy': '数值计算库',
        'pandas': '数据处理库',
        'matplotlib': '绘图库',
        'seaborn': '统计绘图库',
        'tqdm': '进度条库',
        'requests': 'HTTP请求库',
        'yaml': 'YAML配置文件支持',
        'h5py': 'HDF5文件支持'
    }
    
    # TensorFlow and librosa checked separately due to potential import issues
    sensitive_packages = {
        'tensorflow': 'TensorFlow深度学习框架',
        'librosa': '音频处理库',
        'sklearn': '机器学习库(scikit-learn)',
    }
    
    results = {}
    print("\n检查Python包安装状态:")
    print("-" * 40)
    
    # Check basic packages first
    for package, description in required_packages.items():
        try:
            if package == 'yaml':
                importlib.import_module('yaml')
            else:
                importlib.import_module(package)
            
            print(f"✓ {package:12} - {description}")
            results[package] = True
        except ImportError:
            print(f"✗ {package:12} - {description} (未安装)")
            results[package] = False
        except Exception as e:
            print(f"⚠ {package:12} - {description} (导入错误: {str(e)[:50]}...)")
            results[package] = False
    
    # Check sensitive packages with better error handling
    for package, description in sensitive_packages.items():
        try:
            if package == 'sklearn':
                import sklearn
                print(f"✓ {package:12} - {description}")
                results[package] = True
            elif package == 'tensorflow':
                # Import tensorflow in a safer way
                import tensorflow as tf
                print(f"✓ {package:12} - {description} (版本: {tf.__version__})")
                results[package] = True
            elif package == 'librosa':
                import librosa
                print(f"✓ {package:12} - {description} (版本: {librosa.__version__})")
                results[package] = True
            else:
                importlib.import_module(package)
                print(f"✓ {package:12} - {description}")
                results[package] = True
        except ImportError as e:
            print(f"✗ {package:12} - {description} (未安装)")
            results[package] = False
        except Exception as e:
            print(f"⚠ {package:12} - {description} (导入错误)")
            print(f"    错误详情: {str(e)[:100]}...")
            results[package] = False
    
    return results

def check_tensorflow_gpu() -> bool:
    """检查TensorFlow GPU支持"""
    try:
        import tensorflow as tf
        gpu_devices = tf.config.list_physical_devices('GPU')
        if gpu_devices:
            print(f"\n✓ GPU支持: 检测到 {len(gpu_devices)} 个GPU设备")
            for i, device in enumerate(gpu_devices):
                print(f"  GPU {i}: {device.name}")
            return True
        else:
            print("\n⚠ GPU支持: 未检测到GPU设备（将使用CPU）")
            return False
    except ImportError:
        print("\n✗ 无法检查GPU支持: TensorFlow未安装")
        return False
    except Exception as e:
        print(f"\n⚠ GPU检查失败: {str(e)}")
        return False

def check_audio_support() -> bool:
    """检查音频处理支持"""
    try:
        import librosa
        import soundfile
        print("\n✓ 音频处理: librosa和soundfile已安装")
        
        # 检查ffmpeg
        try:
            result = subprocess.run(['ffmpeg', '-version'], 
                                  capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                print("✓ FFmpeg: 已安装并可用")
                return True
            else:
                print("⚠ FFmpeg: 命令执行失败")
                return False
        except (subprocess.TimeoutExpired, FileNotFoundError):
            print("⚠ FFmpeg: 未安装或不在PATH中")
            print("  请参考README.md安装FFmpeg")
            return False
            
    except ImportError as e:
        print(f"\n✗ 音频处理支持不完整: {e}")
        return False
    except Exception as e:
        print(f"\n⚠ 音频处理检查失败: {str(e)}")
        return False

def get_package_versions() -> Dict[str, str]:
    """获取包版本信息"""
    packages = ['numpy', 'pandas', 'matplotlib', 'tensorflow', 'librosa']
    versions = {}
    
    print("\n包版本信息:")
    print("-" * 30)
    
    for package in packages:
        try:
            module = importlib.import_module(package)
            version = getattr(module, '__version__', 'Unknown')
            versions[package] = version
            print(f"{package:12}: {version}")
        except ImportError:
            versions[package] = 'Not installed'
            print(f"{package:12}: 未安装")
        except Exception as e:
            versions[package] = f'Error: {str(e)[:20]}...'
            print(f"{package:12}: 检查失败")
    
    return versions

def provide_installation_suggestions(failed_packages: List[str]):
    """提供安装建议"""
    if not failed_packages:
        return
    
    print(f"\n安装建议:")
    print("=" * 50)
    
    # Check for Python 3.12 specific issues
    if sys.version_info.minor == 12:
        print("Python 3.12 兼容性说明:")
        print("  某些包可能与Python 3.12存在兼容性问题")
        print("  建议使用Python 3.9-3.11，或等待包更新")
        print()
    
    if 'tensorflow' in failed_packages:
        print("安装TensorFlow:")
        print("  pip install tensorflow>=2.16.0")
        print("  如果失败，尝试: pip install tensorflow --upgrade")
        print()
    
    if 'librosa' in failed_packages or 'soundfile' in failed_packages:
        print("安装音频处理库:")
        print("  pip install librosa soundfile")
        print()
    
    if len(failed_packages) > 2:
        print("批量安装所有依赖:")
        print("  pip install --upgrade pip")
        print("  pip install -r requirements.txt")
        print()
        print("或使用conda:")
        print("  conda env create -f environment.yml")
        print("  conda activate esc50_classification")

def check_project_structure():
    """检查项目结构"""
    expected_dirs = ['code', 'data', 'models', 'results', 'plots']
    print(f"\n项目结构检查:")
    print("-" * 30)
    
    for directory in expected_dirs:
        if os.path.exists(directory):
            print(f"✓ {directory}/ 目录存在")
        else:
            print(f"⚠ {directory}/ 目录不存在（将自动创建）")
            try:
                os.makedirs(directory, exist_ok=True)
                print(f"  已创建 {directory}/ 目录")
            except Exception as e:
                print(f"  创建失败: {str(e)}")

def main():
    """主检查函数"""
    print("=" * 60)
    print("环境声音分类系统 - 环境检查")
    print("=" * 60)
    
    # 检查Python版本
    python_ok = check_python_version()
    
    # 检查项目结构
    check_project_structure()
    
    # 检查包安装
    try:
        package_results = check_package_installation()
    except Exception as e:
        print(f"包检查过程中出现错误: {str(e)}")
        package_results = {}
    
    # 获取版本信息
    try:
        versions = get_package_versions()
    except Exception as e:
        print(f"版本检查过程中出现错误: {str(e)}")
        versions = {}
    
    # 检查GPU支持
    gpu_ok = check_tensorflow_gpu()
    
    # 检查音频支持
    audio_ok = check_audio_support()
    
    # 统计结果
    failed_packages = [pkg for pkg, status in package_results.items() if not status]
    total_packages = len(package_results)
    success_packages = total_packages - len(failed_packages)
    
    print(f"\n" + "=" * 60)
    print("检查结果汇总:")
    print("=" * 60)
    print(f"Python版本: {'✓' if python_ok else '✗'}")
    print(f"包安装状态: {success_packages}/{total_packages} 成功")
    print(f"GPU支持: {'✓' if gpu_ok else '⚠'}")
    print(f"音频处理: {'✓' if audio_ok else '⚠'}")
    
    if failed_packages:
        print(f"\n未安装的包: {', '.join(failed_packages)}")
        provide_installation_suggestions(failed_packages)
    else:
        print("\n🎉 所有依赖都已正确安装！")
        print("可以开始使用环境声音分类系统了。")
    
    print(f"\n运行示例:")
    print("  python -m code.main --model_type simple_cnn --download_dataset")

if __name__ == "__main__":
    main()
