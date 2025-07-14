from typing import Optional, List
from fastapi import APIRouter, Header
from fastapi.responses import JSONResponse, FileResponse
import os
import jesse.helpers as jh
from jesse.services import auth as authenticator

router = APIRouter(prefix="/strategy-docs", tags=["Strategy Documentation"])

# 策略文档数据 - 用自然语言描述各个策略
STRATEGY_DOCS = {
    "BuyHold": {
        "name": "买入持有策略",
        "description": "这是一个简单的买入并持有策略。在第一根K线时买入，然后一直持有到结束。适合长期看好某个资产的投资者。",
        "logic": "1. 检查是否已有持仓\n2. 如果没有持仓，则在当前价格买入\n3. 持有到策略结束",
        "parameters": {
            "qty": "买入数量，默认为1"
        },
        "risk_level": "低",
        "suitable_market": "牛市或长期上涨趋势",
        "ai_prompt": "创建一个买入持有策略：在第一根K线买入指定数量的资产，然后持有到结束。使用self.buy()方法买入，检查self.position.qty来判断是否已有持仓。"
    },
    "RSIStrategy": {
        "name": "RSI相对强弱指标策略", 
        "description": "基于RSI指标的均值回归策略。当RSI低于30时买入（超卖），当RSI高于70时卖出（超买）。",
        "logic": "1. 计算14周期RSI指标\n2. RSI < 30且无持仓时买入\n3. RSI > 70且有持仓时卖出",
        "parameters": {
            "rsi_period": "RSI计算周期，默认14",
            "oversold_threshold": "超卖阈值，默认30", 
            "overbought_threshold": "超买阈值，默认70"
        },
        "risk_level": "中",
        "suitable_market": "震荡市场",
        "ai_prompt": "创建RSI策略：使用ta.rsi(self.candles, period=14)计算RSI。当RSI<30且无持仓时买入，当RSI>70且有持仓时卖出。在should_long()中返回RSI<30的条件，在should_short()中返回RSI>70的条件。"
    },
    "SmartHold": {
        "name": "智能持有策略",
        "description": "改进版的买入持有策略，加入了简单的风险控制。会在价格大幅下跌时止损，在合适时机重新买入。",
        "logic": "1. 初始买入\n2. 监控价格变化\n3. 价格下跌超过阈值时止损\n4. 价格回升时重新买入",
        "parameters": {
            "stop_loss_pct": "止损百分比，默认10%",
            "reentry_pct": "重新买入阈值，默认5%"
        },
        "risk_level": "中低",
        "suitable_market": "波动较大的市场",
        "ai_prompt": "创建智能持有策略：初始买入后，如果价格下跌超过10%则止损卖出，如果价格从低点回升5%则重新买入。使用self.average_entry_price跟踪平均买入价格。"
    },
    "moveAverage": {
        "name": "移动平均线策略",
        "description": "基于移动平均线的趋势跟踪策略。使用快速和慢速移动平均线的交叉信号来决定买卖时机。",
        "logic": "1. 计算快速MA（如5日）和慢速MA（如20日）\n2. 快线上穿慢线时买入（金叉）\n3. 快线下穿慢线时卖出（死叉）",
        "parameters": {
            "fast_period": "快速MA周期，默认5",
            "slow_period": "慢速MA周期，默认20"
        },
        "risk_level": "中",
        "suitable_market": "趋势性市场",
        "ai_prompt": "创建移动平均线策略：计算快速MA和慢速MA，当快线上穿慢线时买入，下穿时卖出。使用ta.sma(self.candles, period)计算移动平均线。在should_long()中检查金叉条件，在should_short()中检查死叉条件。"
    },
    "trendstrate": {
        "name": "趋势策略",
        "description": "综合多个技术指标判断趋势方向的策略。结合移动平均线、RSI、MACD等指标来确认趋势。",
        "logic": "1. 计算多个技术指标\n2. 综合判断趋势方向\n3. 趋势向上时买入\n4. 趋势向下时卖出",
        "parameters": {
            "ma_period": "移动平均线周期",
            "rsi_period": "RSI周期",
            "trend_strength": "趋势强度阈值"
        },
        "risk_level": "中高",
        "suitable_market": "明确趋势的市场",
        "ai_prompt": "创建趋势策略：结合移动平均线、RSI、MACD等多个指标判断趋势。当多个指标都显示上涨趋势时买入，显示下跌趋势时卖出。使用ta.sma(), ta.rsi(), ta.macd()等函数计算指标。"
    }
}

@router.get("/")
async def get_strategy_docs_page():
    """返回策略文档页面"""
    # 返回策略文档的HTML页面
    return FileResponse(f"{os.path.dirname(os.path.dirname(__file__))}/static/strategy-docs.html")

@router.get("/list")
async def get_strategy_list(authorization: Optional[str] = Header(None)) -> JSONResponse:
    """获取所有策略文档列表"""
    if not authenticator.is_valid_token(authorization):
        return authenticator.unauthorized_response()
    
    strategy_list = []
    for key, doc in STRATEGY_DOCS.items():
        strategy_list.append({
            "id": key,
            "name": doc["name"],
            "description": doc["description"],
            "risk_level": doc["risk_level"],
            "suitable_market": doc["suitable_market"]
        })
    
    return JSONResponse({
        "status": "success",
        "data": strategy_list
    })

@router.get("/detail/{strategy_id}")
async def get_strategy_detail(strategy_id: str, authorization: Optional[str] = Header(None)) -> JSONResponse:
    """获取特定策略的详细文档"""
    if not authenticator.is_valid_token(authorization):
        return authenticator.unauthorized_response()
    
    if strategy_id not in STRATEGY_DOCS:
        return JSONResponse({
            "status": "error",
            "message": f"策略 {strategy_id} 不存在"
        }, status_code=404)
    
    return JSONResponse({
        "status": "success",
        "data": STRATEGY_DOCS[strategy_id]
    })

@router.post("/save")
async def save_strategy_description(
    strategy_data: dict,
    authorization: Optional[str] = Header(None)
) -> JSONResponse:
    """保存策略描述到strategtxt目录"""
    if not authenticator.is_valid_token(authorization):
        return authenticator.unauthorized_response()

    try:
        name = strategy_data.get("name", "").strip()
        description = strategy_data.get("description", "").strip()

        if not name or not description:
            return JSONResponse({
                "status": "error",
                "message": "策略名称和描述不能为空"
            }, status_code=400)

        # 创建strategtxt目录
        strategtxt_dir = os.path.join(os.getcwd(), "strategtxt")
        os.makedirs(strategtxt_dir, exist_ok=True)

        # 保存策略描述文件
        file_path = os.path.join(strategtxt_dir, f"{name}.txt")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(f"策略名称: {name}\n")
            f.write(f"创建时间: {jh.now_to_timestamp()}\n")
            f.write(f"状态: 待生成\n")
            f.write(f"描述:\n{description}\n")

        return JSONResponse({
            "status": "success",
            "message": f"策略描述已保存到 {file_path}",
            "data": {
                "name": name,
                "file_path": file_path
            }
        })

    except Exception as e:
        return JSONResponse({
            "status": "error",
            "message": f"保存失败: {str(e)}"
        }, status_code=500)

@router.post("/generate")
async def generate_strategy_from_description(
    strategy_data: dict,
    authorization: Optional[str] = Header(None)
) -> JSONResponse:
    """根据自然语言描述生成策略代码（预留接口）"""
    if not authenticator.is_valid_token(authorization):
        return authenticator.unauthorized_response()

    try:
        name = strategy_data.get("name", "").strip()
        description = strategy_data.get("description", "").strip()

        if not name or not description:
            return JSONResponse({
                "status": "error",
                "message": "策略名称和描述不能为空"
            }, status_code=400)

        # 更新strategtxt文件状态
        strategtxt_dir = os.path.join(os.getcwd(), "strategtxt")
        file_path = os.path.join(strategtxt_dir, f"{name}.txt")

        if os.path.exists(file_path):
            with open(file_path, "a", encoding="utf-8") as f:
                f.write(f"\n生成请求时间: {jh.now_to_timestamp()}\n")
                f.write("状态: 已加入AI生成队列\n")

        # 这里预留给AI生成策略的接口
        # TODO: 实现AI生成队列和策略代码生成

        return JSONResponse({
            "status": "success",
            "message": "策略已加入AI生成队列",
            "data": {
                "name": name,
                "description": description,
                "queue_position": 1,  # 模拟队列位置
                "estimated_time": "3-5分钟"
            }
        })

    except Exception as e:
        return JSONResponse({
            "status": "error",
            "message": f"生成请求失败: {str(e)}"
        }, status_code=500)

@router.get("/list")
async def get_strategy_list(authorization: Optional[str] = Header(None)) -> JSONResponse:
    """获取策略列表"""
    if not authenticator.is_valid_token(authorization):
        return authenticator.unauthorized_response()

    try:
        strategtxt_dir = os.path.join(os.getcwd(), "strategtxt")
        strategies = []

        if os.path.exists(strategtxt_dir):
            for filename in os.listdir(strategtxt_dir):
                if filename.endswith('.txt'):
                    file_path = os.path.join(strategtxt_dir, filename)
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()

                        # 解析文件内容
                        lines = content.split('\n')
                        strategy_info = {
                            'name': filename[:-4],  # 去掉.txt扩展名
                            'description': '',
                            'status': '待编辑',
                            'file_path': file_path
                        }

                        # 解析文件内容
                        in_description = False
                        desc_lines = []

                        for i, line in enumerate(lines):
                            line = line.strip()

                            if line.startswith('策略名称:'):
                                strategy_info['name'] = line.split(':', 1)[1].strip()
                            elif line.startswith('描述:'):
                                in_description = True
                                # 如果描述在同一行
                                desc_part = line.split(':', 1)[1].strip()
                                if desc_part:
                                    desc_lines.append(desc_part)
                            elif in_description:
                                # 检查是否到了描述结束
                                if line.startswith(('状态:', '生成请求时间:', '创建时间:', '参数设置:', '适用市场:', '风险等级:')):
                                    in_description = False
                                    strategy_info['description'] = '\n'.join(desc_lines).strip()
                                elif line:  # 非空行才添加
                                    desc_lines.append(line)
                            elif line.startswith('状态:'):
                                status = line.split(':', 1)[1].strip()
                                if '已加入AI生成队列' in status or '生成中' in status:
                                    strategy_info['status'] = '生成中'
                                elif '待生成' in status:
                                    strategy_info['status'] = '待生成'
                                elif '已完成' in status:
                                    strategy_info['status'] = '已完成'
                                else:
                                    strategy_info['status'] = status

                        # 如果描述还在收集中，完成收集
                        if in_description and desc_lines:
                            strategy_info['description'] = '\n'.join(desc_lines).strip()

                        strategies.append(strategy_info)

                    except Exception as e:
                        print(f"读取策略文件 {filename} 失败: {e}")
                        continue

        # 按创建时间排序（最新的在前）
        strategies.sort(key=lambda x: os.path.getmtime(x['file_path']), reverse=True)

        return JSONResponse({
            "status": "success",
            "data": strategies
        })

    except Exception as e:
        return JSONResponse({
            "status": "error",
            "message": f"获取策略列表失败: {str(e)}"
        }, status_code=500)

@router.get("/list-files")
async def list_strategy_files(authorization: Optional[str] = Header(None)) -> JSONResponse:
    """获取strategtxt目录下的策略文件列表"""
    if not authenticator.is_valid_token(authorization):
        return authenticator.unauthorized_response()

    try:
        strategtxt_dir = os.path.join(os.getcwd(), "strategtxt")

        if not os.path.exists(strategtxt_dir):
            return JSONResponse({
                "status": "success",
                "data": []
            })

        files = []
        for filename in os.listdir(strategtxt_dir):
            if filename.endswith('.txt'):
                file_path = os.path.join(strategtxt_dir, filename)
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()

                files.append({
                    "name": filename[:-4],  # 去掉.txt后缀
                    "filename": filename,
                    "content": content,
                    "modified_time": os.path.getmtime(file_path)
                })

        return JSONResponse({
            "status": "success",
            "data": files
        })

    except Exception as e:
        return JSONResponse({
            "status": "error",
            "message": f"获取文件列表失败: {str(e)}"
        }, status_code=500)
