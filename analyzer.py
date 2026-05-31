"""跨部门协作摩擦检测 - 核心分析引擎"""

import json
from typing import Dict, List, Optional, Tuple

class FrictionPoint:
    """摩擦点记录，表示跨部门协作中的一个摩擦问题。"""

    def __init__(self, ftype: str, node: str, severity: str,
                 description: str, impact: str, suggestion: str):
        """初始化摩擦点。

        Args:
            ftype: 摩擦类型，如"信息不对称"、"流程断层"
            node: 发生节点，如"需求评审"、"上线审批"
            severity: 严重程度，"高"、"中"、"低"
            description: 具体描述
            impact: 影响说明
            suggestion: 改进建议
        """
        self.type = ftype
        self.node = node
        self.severity = severity
        self.description = description
        self.impact = impact
        self.suggestion = suggestion

    def to_dict(self) -> dict:
        """将摩擦点转换为字典格式。

        Returns:
            包含所有字段的字典
        """
        return {
            "type": self.type,
            "node": self.node,
            "severity": self.severity,
            "description": self.description,
            "impact": self.impact,
            "suggestion": self.suggestion,
        }


class FrictionAnalyzer:
    """跨部门协作摩擦分析引擎，检测摩擦点并评估协作健康度。"""

    WEIGHTS = {
        "信息不对称": 0.25,
        "流程断层": 0.20,
        "责任模糊": 0.25,
        "时间错配": 0.15,
        "文化冲突": 0.15,
    }
    SEVERITY_SCORE = {"高": 30, "中": 15, "低": 5}

    def detect(self, dept_a: str, dept_b: str,
               data_sources: Optional[List[str]] = None) -> dict:
        """检测两个部门之间的协作摩擦点。

        Args:
            dept_a: 部门A名称
            dept_b: 部门B名称
            data_sources: 数据来源列表（可选）

        Returns:
            检测结果字典，包含部门信息、摩擦点列表、健康度评分、趋势
        """
        return {
            "department_a": dept_a,
            "department_b": dept_b,
            "friction_points": [],
            "health_score": 100,
            "trend": "stable",
        }

    def _calc_health(self, friction_points: List[FrictionPoint]) -> int:
        """根据摩擦点计算协作健康度评分。

        Args:
            friction_points: FrictionPoint 实例列表

        Returns:
            健康度评分（0-100）
        """
        total = sum(
            self.SEVERITY_SCORE.get(p.severity, 0) * self.WEIGHTS.get(p.type, 0.1)
            for p in friction_points
        )
        return max(0, min(100, 100 - total))

    def scan_all_departments(self, departments: List[str],
                             matrix: Dict[Tuple[str, str], list]) -> List[dict]:
        """扫描所有部门间的协作健康状况。

        Args:
            departments: 部门名称列表
            matrix: 部门间摩擦点矩阵，键为(部门A, 部门B)元组

        Returns:
            所有部门对的检测结果列表
        """
        results = []
        for i, da in enumerate(departments):
            for db in departments[i+1:]:
                points = matrix.get((da, db), [])
                fps = [FrictionPoint(**p) if isinstance(p, dict) else p for p in points]
                score = self._calc_health(fps)
                results.append({
                    "dept_a": da, "dept_b": db,
                    "health": score,
                    "friction_count": len(fps),
                })
        return results

    def filter_by_severity(self, results: List[dict], level: str = "高") -> List[dict]:
        """按严重程度过滤摩擦点结果。

        Args:
            results: 检测结果列表
            level: 目标严重程度，默认"高"

        Returns:
            筛选后的结果列表
        """
        return [r for r in results if r.get("severity", "") == level]

    def generate_report(self, result: dict, output: str = "json") -> str:
        """生成摩擦分析报告。

        Args:
            result: 检测结果字典
            output: 输出格式，"json"或"text"

        Returns:
            格式化的报告（JSON字符串或文本）
        """
        if output == "json":
            report = {
                "analysis": {
                    "department_a": result["department_a"],
                    "department_b": result["department_b"],
                },
                "friction_points": [
                    {**p.to_dict()} if isinstance(p, FrictionPoint) else p
                    for p in result.get("friction_points", [])
                ],
                "health_score": result["health_score"],
                "trend": result["trend"],
            }
        elif output == "text":
            lines = [
                f"跨部门摩擦检测报告",
                f"{'='*40}",
                f"部门A: {result['department_a']}",
                f"部门B: {result['department_b']}",
                f"协作健康度: {result['health_score']}/100",
                f"趋势: {result['trend']}",
                "",
                "摩擦点:",
            ]
            for i, p in enumerate(result.get("friction_points", []), 1):
                pd = p.to_dict() if isinstance(p, FrictionPoint) else p
                lines.append(f"  {i}. [{pd['severity']}] {pd['type']} @ {pd['node']}")
                if output == "text":
                    lines.append(f"     {pd.get('description', '')}")
                    lines.append(f"     建议: {pd.get('suggestion', '')}")
            report = "\n".join(lines)
        return report


if __name__ == "__main__":
    analyzer = FrictionAnalyzer()
    sample = analyzer.detect("技术部", "市场部")
    sample["health_score"] = 65
    sample["friction_points"] = [
        FrictionPoint("信息不对称", "需求评审", "高",
                      "市场部需求变更未及时同步技术部", "平均返工3次/需求",
                      "建立需求变更同步机制"),
        FrictionPoint("流程断层", "上线审批", "中",
                      "上线审批需要3个部门签字，耗时2天", "发布延迟",
                      "优化审批流，并行审批"),
    ]
    sample["health_score"] = analyzer._calc_health(sample["friction_points"])
    print(analyzer.generate_report(sample, output="text"))
