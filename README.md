# 跨部门协作摩擦检测

> 自动识别跨部门协作中的沟通障碍、流程瓶颈和责任模糊点

---

## 核心功能

### 1. 协作节点分析

识别部门间协作的关键节点：
- 信息传递节点
- 决策审批节点
- 资源调配节点
- 进度同步节点

### 2. 摩擦类型检测

| 类型 | 特征 | 检测方法 |
|------|------|----------|
| **信息不对称** | 一方掌握关键信息，另一方缺失 | 信息流向追踪 |
| **流程断层** | 两个部门流程衔接处缺失明确规则 | 流程图缺口分析 |
| **责任模糊** | 任务归属不明，出现推诿或重复 | 责任矩阵扫描 |
| **时间错配** | 周期不同步，造成等待或延误 | 时间线对比 |
| **文化冲突** | 工作风格差异导致沟通障碍 | 术语/习惯差异分析 |

### 3. 检测报告生成

```json
{
  "department_a": "技术部",
  "department_b": "市场部",
  "friction_points": [
    {
      "type": "信息不对称",
      "node": "需求评审",
      "severity": "高",
      "description": "市场部需求变更未及时同步技术部",
      "impact": "平均返工3次/需求",
      "suggestion": "建立需求变更同步机制"
    }
  ],
  "health_score": 65,
  "trend": "下降"
}
```

---

## 使用方法

### 基础用法

```python
from analyzer import FrictionAnalyzer

# 初始化分析器
analyzer = FrictionAnalyzer()

# 分析两个部门
result = analyzer.detect(
    dept_a="技术部",
    dept_b="产品部",
    data_sources=["会议记录", "工单系统", "沟通记录"]
)

# 生成报告
report = analyzer.generate_report(result)
```

### 批量检测

```python
# 检测所有部门组合
all_pairs = analyzer.scan_all_departments()

# 输出高风险组合
high_risk = analyzer.filter_by_severity(all_pairs, level="高")
```

---

## 数据输入

| 数据类型 | 用途 | 采集建议 |
|----------|------|----------|
| 会议记录 | 分析沟通质量 | 自动转录 |
| 工单流转 | 追踪责任路径 | Jira/飞书API |
| 邮件/消息 | 识别信息延迟 | 权限内采样 |
| 项目文档 | 检查流程衔接 | Git/文档库 |
| 时间日志 | 对比周期差异 | 项目管理工具 |

---

## 指标体系

### 协作健康度评分

```
健康度 = 100 - Σ(摩擦点严重度 × 权重)

权重：
- 信息不对称：0.25
- 流程断层：0.20
- 责任模糊：0.25
- 时间错配：0.15
- 文化冲突：0.15
```

### 关键指标

| 指标 | 计算 | 目标 |
|------|------|------|
| 信息同步延迟 | 平均同步时间 | < 24小时 |
| 流程衔接完整率 | 明确节点/总节点 | > 90% |
| 责任归属清晰率 | 明确归属/总任务 | > 95% |
| 周期匹配度 | 同步次数/总协作 | > 80% |

---

## 输出格式

### 可视化报告

- 部门关系热力图
- 摩擦点分布雷达图
- 时间线瓶颈图
- 责任矩阵缺口图

### 导出格式

- PDF完整报告
- Excel数据表
- JSON原始数据
- PPT汇报版

---

## 应用场景

| 场景 | 用法 |
|------|------|
| 组织诊断 | 定期扫描，识别隐患 |
| 新团队磨合 | 监测新组合的协作磨合过程 |
| 流程优化前测 | 定位优化重点 |
| 合并/拆分评估 | 评估组织调整影响 |

---

## 配置示例

```yaml
# config.yaml
departments:
  - 技术部
  - 产品部
  - 市场部
  - 运营部

thresholds:
  severity_high: 70
  severity_medium: 40
  severity_low: 20

alerts:
  enable: true
  channels: ["email", "飞书"]

schedule:
  frequency: "weekly"
  report_to: "管理层"
```

---

## 技术架构

```
跨部门协作摩擦检测/
├── analyzer.py          # 核心分析引擎（含 FrictionPoint、FrictionAnalyzer）
├── README.md
├── requirements.txt
└── tests/
    └── test_analyzer.py
```

---

## 安装

本项目为示例代码，可直接使用：

```bash
git clone https://github.com/yourname/friction-detector.git
cd friction-detector
# analyzer.py 可直接运行或导入使用
python analyzer.py
```

---

> 版本：1.0.0 | 更新：2025-05-29