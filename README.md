# Rank List Labeler

Rank List Labeler 是一个在大模型进行 RLHF（基于人类反馈的强化学习）阶段，用于标注排序的工具，旨在帮助用户对生成式模型生成的答案进行排序标注。

## 功能特点
- 提供界面展示当前的查询问题和历史对话
- 支持为生成的答案选择排名
- 自动检测和提示排名冲突
- 将标注的排序结果追加保存到数据集文件中
- 提供数据集页面以查看已标注的数据

## 后续计划

[] 实现 RLAIF ，基于 API 进行自动标注
[] 支持拖动排序

## 安装依赖
- Python 3.x
- 安装依赖包：`pip install -r requirements.txt`

## 使用说明
1. 准备数据集文件：将包含查询问题、历史对话和生成的答案的数据集文件准备为 JSON 格式，格式参见 input_file.json。
2. 运行应用：执行 `bash run.sh` 命令启动应用。
3. 标注排序：在标注页面，依次为每个查询问题的生成答案选择排名，并点击“存储当前排序”按钮保存标注结果。
4. 查看数据集：在数据集页面，可以查看已标注的数据集，包括查询问题、历史对话和生成的答案的排序结果。

## 配置
应用支持一些配置选项，可在 `app.py` 文件中进行修改：
- `MODEL_CONFIG`：模型配置，包括模型名称、设备、数据集文件路径等。
- `RANK_COLOR`：排名颜色列表，用于在界面中显示不同排名的颜色。

## 示例数据集
您可以使用以下 JSON 数据集示例进行测试：
```json
{
    "0": {
        "query": "非常感谢您的建议，我会尽量按照您的建议来做。谢谢！",
        "history": [],
        "response_0": "不客气，我很高兴能够帮助到您。如果您还有其他问题，随时可以向我咨询。祝您好运！",
        "response_1": "不客气，我很高兴能够帮助您。如果您还有其他问题，随时都可以向我咨询。祝您好运！",
        "response_2": "不客气，我很高兴能够帮助您。如果您有任何其他问题，随时都可以向我咨询。祝您好运！",
        "response_3": "不客气，我很高兴能够帮助到您。如果您还有其他问题，随时可以向我咨询。祝您好运！"
    },
    ...
}

## 贡献与许可

致谢：https://github.com/HarderThenHarder/transformers_tasks/tree/main/RLHF

欢迎提供问题反馈、改进建议和贡献代码。请通过 GitHub 提交问题和拉取请求。

本项目基于 MIT License 进行发布和授权。