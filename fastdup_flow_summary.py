def get_fastdup_flow_summary():
    """
    Returns a textual summary of the core processing flow of fastdup.
    Extracted to avoid complex third-party library dependencies and nested references.
    """
    summary = """
# Fastdup 核心处理全流程

fastdup 的整体执行流程主要分为四个核心阶段：

1. **初始化 (`fastdup.create`)**
   - **入口文件**: `fastdup_create.py` (`create` 函数)
   - **核心动作**: 初始化并返回一个 `Fastdup` 对象（该对象继承自 `FastdupController`）。
   - **详细步骤**: 设置工作目录 (`work_dir`) 和输入数据目录 (`input_dir`)。如果没有提供 `work_dir`，默认会创建一个名为 'work_dir' 的文件夹。

2. **执行调用 (`Fastdup.run`)**
   - **入口文件**: `engine.py` (`Fastdup` 类的 `run` 方法)
   - **核心动作**: 封装核心的执行过程。
   - **详细步骤**: 配置默认的分析参数（例如：距离度量 distance='cosine', 聚类阈值 cc_threshold=0.96, 离群值百分比 outlier_percentile=0.05）。收集这些参数并调用父类的 `run` 方法 (`FastdupController.run`)。

3. **核心调度控制 (`FastdupController.run`)**
   - **入口文件**: `fastdup_controller.py` (`FastdupController` 类的 `run` 方法)
   - **核心动作**: 这是在 C++ 引擎运行前后的主要业务控制逻辑。
   - **详细步骤**:
     - **a. 参数准备 (`_init_run`)**: 验证输入，推断数据类型（image 图像, bbox 边界框, crop 裁剪图），准备运行模式，并创建或清空输出文件夹。
     - **b. 参数配置 (`set_fastdup_kwargs`)**: 编译所有的 fastdup 参数，并格式化 `turi_param` 字符串，用于将配置项传递给底层的 C++ 引擎。
     - **c. 输入格式化 (`_set_fastdup_input`)**: 将输入目录或标注文件整理成 C++ 引擎能读取的格式（通常会生成一个临时的 CSV 文件）。
     - **d. C++ 引擎执行 (`fastdup.run(...)`)**: **这是真正的计算核心。** 它调用底层的 C++ 扩展二进制库，执行特征提取 (feature extraction)、最近邻查找 (nearest neighbors)、相似度图生成 (similarity graph)、连通分量分析 (connected components) 以及图像统计计算。
     - **e. 后处理映射 (`_create_img_mapping`)**: 读取 C++ 生成的 `atrain_mapping.csv` 和 `atrain_bad_files.csv`，将系统内部的 fastdup 数字 ID 映射回用户原始的文件名和标注信息。
     - **f. 标注数据扩充 (`_expand_annot_df` 和 `_index_annot_df`)**: 将原始的用户标注与 C++ 的结果合并。处理裁剪图映射，标记损坏的文件，并对每项数据进行状态标记（如 'VALID' 或 'MISSING_IMAGE'）。
     - **g. 保存产物 (`_save_artifacts`)**: 存储配置 JSON，并将最终的映射和标注信息序列化 (pickle)，以便后续的快速加载读取。

4. **结果获取 (例如 `similarity()`, `outliers()`, `connected_components()`)**
   - **入口文件**: `fastdup_controller.py`
   - **核心动作**: 对 C++ 引擎输出的结果 CSV 进行懒加载 (Lazy loading) 和数据合并。
   - **详细步骤**: 像 `similarity()` 这类方法，会读取底层的 CSV 结果文件（如 `similarity.csv`），将它们与用户的标注数据帧和截图数据帧合并，最终返回结构化的 pandas DataFrame 给用户。
"""
    return summary.strip()

if __name__ == "__main__":
    print(get_fastdup_flow_summary())
