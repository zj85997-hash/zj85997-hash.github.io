#!/usr/bin/env python3
"""生成付钟浩 Alex 个人网站的全部静态页面。只用 Python 标准库。

    python3 build.py

改内容：改下面的 SITE、ABOUT、SKILLS、PROJECTS、SITES、POSTS、CONTACT，再运行一次。
头像：把照片存成 assets/img/avatar.jpg（或 .png / .webp），重新生成就会替换首屏的字母头像。
所有链接都是相对路径，生成的文件夹可以直接放到 GitHub Pages、Cloudflare Pages 或任意 nginx。
"""
import html
import json
import os
import re

ROOT = os.path.dirname(os.path.abspath(__file__))
GH = 'https://github.com/zj85997-hash'
BASE_URL = 'https://zj85997-hash.github.io'  # 网站正式地址；买了域名后改这里，sitemap 会跟着变
PAGES = 'https://zj85997-hash.github.io'

# ---------------------------------------------------------------- 站点信息
SITE = {
    'name': '付钟浩 Alex',
    'brand': 'Alex',
    'role': 'AI 培训讲师 · FDE',
    'tagline': '先带学员做出能用的作品，再把它落进业务里。',
    'desc': '付钟浩（Alex），AI 培训讲师、企业 AI 落地讲师（FDE）。企业内训、院校课程共建、青少年与家长 AI 课、AI 落地陪跑。',
    'footer': '付钟浩 Alex · AI 培训讲师 / FDE',
}

ABOUT = [
    '我做 AI 培训，习惯从学员要带走的作品倒推课程：一条短视频、一个落地页、一个智能体，课上就做出来。',
    '2021 年开始做培训：做过支付代理商赋能讲师、直播公司培训经理、新媒体团队经理，把零基础员工带成主播，把新人带成能管团队的组长。'
    '2026 年转做 AI：给高职院校研发 60 课时的 AI 电商课，给青少年主讲 AI 营，给企业老板讲「把 AI 变成经营能力」。',
    '我也是 FDE（前沿部署工程师）：进企业交付 AI 方案，再把实战提炼成能教的方法。所以课上讲的每个案例，都是自己做过的。',
]

SKILLS = [
    ('课程研发', 'book', ['作品倒推', '体系课', '训练营', '工作坊', '讲师手册', '逐字稿', '评价量规']),
    ('授课交付', 'users', ['企业内训', '院校课程', '青少年营地', '家长课', '代理商课', '视频号直播']),
    ('AI 工具', 'sparkle', ['Claude Code', 'Codex', 'Cursor', 'WorkBuddy', '扣子 Coze', '智谱清言', 'DeepSeek', '豆包', '即梦']),
    ('落地方法', 'route', ['FDE 七步链路', '场景打分卡', '方案六件套', '智能体 + 知识库', 'Obsidian 第二大脑', '飞书多维表格']),
]

COURSES = [
    ('《AI 赋能商业实战》', '高职 · 60 课时 / 22 讲 / 720 页'),
    ('VibeCamp 同频造物营', '青少年 · 3.5 天 22 小时 · 已交付 1 期'),
    ('把 AI 变成经营能力', '企业老板 · 2 小时路演版 · 已授课'),
    ('AI 创造实战营 · 家长专场', '家长 · 2 天 16 小时'),
    ('AI 家庭智能体搭建实战营', '家长 · 2 小时 / 2 天 · 模板已开源'),
    ('两小时炼出第二大脑', '一人公司 / 老板 · 120 分钟实操'),
    ('企业 AI 落地沙龙课', 'FDE 学员 · 18 讲，每讲配一个真实案例'),
]

# ---------------------------------------------------------------- 项目
PROJECTS = [
    {
        'slug': 'inflow-fde', 'kind': 'public', 'year': '2026', 'home': True, 'icon': 'cpu',
        'title': 'InFlow FDE 企业 AI 转型操盘台', 'sub': '多 Agent 中台 · 在线演示',
        'text': '总指挥分活、数字员工干活：数字由代码算，退款、结算这类动钱的动作进审批收件箱，每一分 AI 成本都记账。',
        'tags': ['多 Agent', '人机协同', 'DeepSeek', 'Next.js'],
        'demo': PAGES + '/inflow-fde/', 'repo': GH + '/inflow-fde',
        'lead': '给 FDE（驻场 AI 工程师）用的操盘台：诊断企业的工作流，装配一支 Agent 队伍，让它在人的把关下干活。由团队原型 AI-FDE-tool 发展而来，我改名为 InFlow FDE，接着做完并开源。',
        'facts': [('Agent', '总指挥 + 4 部门 + 4 数字员工'), ('演示数据', '3 店铺 · 408 笔订单'), ('页面', '11 个'), ('测试', '18 个')],
        'highlights': [
            '三层分发：老板对总指挥说一句话，任务分到部门、派给数字员工，分派过程和流式产出实时可见。',
            '规矩交给知识库记，算数交给代码算：利润、亏损单、投放漏斗都由代码从订单逐笔算出，模型只负责写结论。',
            '动钱的动作人拍板：退款、结算、预算、改价只进审批收件箱，批准或驳回都写进操作留痕。',
            '成本可解释：每次模型调用逐笔记账、按 Agent 归因；超过每日预算，网关直接拦截。',
            '同一套编排核心跑在服务端（Fastify + SQLite）和浏览器里：没有 Key 就用离线演示模型，在线演示和本地部署算出的数一模一样。',
        ],
        'story': [
            '原型 AI-FDE-tool 已经搭好 monorepo、DeepSeek 网关、成本账本和中台页面。我接手后先把编排抽成服务端和浏览器共用的核心，再补上 4 个数字员工的技能、审批收件箱、预算护栏、设置页和命令行。',
            '演示用一家虚构的三店铺跨境电商，其中一家毛利率最高却在亏钱。利润分析师查出钱漏在达人佣金、投流和退款，提出扣回退款订单上的佣金，等人批准。',
        ],
        'source': ('zj85997-hash/inflow-fde', 'MIT · 18 个测试 · GitHub Actions 自动发布'),
    },
    {
        'slug': 'family-ai-agents', 'kind': 'public', 'year': '2026', 'home': True, 'icon': 'users',
        'title': 'AI 家庭智能体模板包', 'sub': '家长课 · 开源 Prompt 模板',
        'text': '亲子沟通翻译官、家庭学习教练、成长规划师：完整 Prompt 加填好的示例知识库，复制粘贴就能用。',
        'tags': ['Prompt', '扣子 Coze', '智谱清言', '家长课'],
        'demo': PAGES + '/family-ai-agents/', 'repo': GH + '/family-ai-agents',
        'lead': '3 个家庭 AI 助手，每个都配完整的系统提示词和一份填好的示例知识库。这是《AI 家庭智能体搭建实战营》的课后资料包。',
        'facts': [('智能体', '3 个'), ('课程版本', '2 小时 · 2 天'), ('平台', '扣子 · 智谱清言 · 豆包'), ('许可', 'CC BY-NC-SA 4.0')],
        'highlights': [
            '三个 Agent 各管一件事：翻译官管关系，学习教练管能力，成长规划师管方向。',
            '每个 Agent 四件套：系统 Prompt、示例知识库、工作流配置、使用说明。',
            '学习教练按苏格拉底式设计：用三级提示一步步引导，不直接给答案。',
            '网页版一键复制；可对话版填自己的 API Key 直接聊，Key 只存在浏览器里。',
            '示例知识库用同一个虚构的孩子，演示一份家庭档案怎么喂出三个侧重点不同的助手。',
        ],
        'story': [
            '课上讲的 Prompt 都是片段，知识库也只给了模板，家长回家很难自己补齐。所以我把最后一步做完：每个 Agent 都配一套完整 Prompt 和一份填好的示范知识库。',
            '它是 2 小时手机版和 2 天版两门家长课的课后资料，课程框架一起开源。方法论就三条：CMRL 写人设，BISCO 做设计，以及「家庭效果 = 认知 × 工具 × 陪伴」，任何一项为零，结果就是零。',
        ],
        'source': ('zj85997-hash/family-ai-agents', 'CC BY-NC-SA 4.0 · 可署名使用和改编，不可商用'),
    },
    {
        'slug': 'meeting-attendance-skill', 'kind': 'public', 'year': '2026', 'home': True, 'icon': 'calendar',
        'title': '腾讯会议考勤 Skill', 'sub': 'AI Skill · 零依赖 Python',
        'text': '腾讯会议导出表交给 AI，一键出日报和周报；昵称五花八门也能对上人。',
        'tags': ['Python', 'AI Skill', 'Claude Code', '自动化'],
        'demo': PAGES + '/tencent-meeting-attendance-skill/', 'repo': GH + '/tencent-meeting-attendance-skill',
        'lead': '读取腾讯会议的「成员参会概况」导出表，按花名册判定准时、迟到、缺勤、请假，输出日报和周报。可以自己跑命令，也可以装进 AI 工具当 Skill 用。',
        'facts': [('依赖', '零第三方依赖'), ('测试', '16 个'), ('输出', '日报 · 周报'), ('许可', 'MIT')],
        'highlights': [
            '昵称自动对人：括号后缀、英文大小写、手机和平板双设备、家长代入会，都能认到同一个人。',
            '规则可配置：准时线、缺勤线、统计日、每周免罚请假次数，写在花名册里或用命令行参数改。',
            '周报给出每人每天的状态矩阵，外加需关注名单、缺勤名单和全勤名单。',
            '通用化之前，用真实导出表和原脚本逐人比对，700 人次的结果完全一致。',
            '示例数据全部虚构，人名一律用代号。',
        ],
        'story': [
            '线上打卡群每天都要统计谁准时、谁迟到、谁请假。腾讯会议能导出参会表，但昵称五花八门：有人带地区后缀，有人用两台设备，有时是家长代为入会，手工对名单很费时间。',
            '这个 Skill 把规则写清楚交给脚本：花名册是唯一基准，规则可配置，边界精确到秒（06:00:00 算准时，06:00:01 算迟到）。装进 Claude Code 或 WorkBuddy 后，对 AI 说一句「统计今天的考勤」就行。',
        ],
        'source': ('zj85997-hash/tencent-meeting-attendance-skill', 'MIT · 16 个测试 · 零第三方依赖'),
    },
    {
        'slug': 'second-brain-pipeline', 'kind': 'public', 'year': '2026', 'home': False, 'icon': 'layers',
        'title': '第二大脑汇聚管线', 'sub': 'Obsidian · 知识管理',
        'text': '得到、钉钉、飞书、备忘录的笔记汇进 Obsidian，自动分类、自动建目录，一键把真名换成代号。',
        'tags': ['Python', 'Obsidian', '飞书', '钉钉'],
        'demo': PAGES + '/obsidian-second-brain-pipeline/', 'repo': GH + '/obsidian-second-brain-pipeline',
        'lead': '开会录音、课堂转写、飞书方案、随手记的备忘录，汇进同一个 Obsidian 库：按项目线自动分类，自动生成首页和案例目录。',
        'facts': [('来源', '4 个'), ('测试', '15 个'), ('依赖', '零第三方依赖'), ('许可', 'MIT')],
        'highlights': [
            '四个来源：得到大脑、钉钉听记、飞书文档、苹果备忘录。增量采集，中断了重跑会接着来。',
            '分类按顺序匹配：人工指定、标题规则、正文规则，都认不出来的进「待归类」。',
            '默认只新增，不删除、不覆盖；目录页只更新自动生成的那一段，手写内容原样保留。',
            '一键代号化：人名换成 A001、公司换成 P01，导出一份能给别人看的副本，双链不断。',
            '凭据不进代码：登录交给各家官方工具，飞书凭据只读环境变量，证书校验始终开启。',
        ],
        'story': [
            '我的笔记散在四个地方：得到的录音转写、钉钉的会议逐字稿、飞书的方案文档、手机备忘录。所以写了这条管线，把它们汇进同一个 Obsidian 库，现在库里有 2400 多篇。',
            '开源版只取了脚本，凭据和私人数据都去掉了，配置放在仓库外。自带一套虚构的演示数据，不需要任何账号，5 分钟就能跑通整条流程。',
        ],
        'source': ('zj85997-hash/obsidian-second-brain-pipeline', 'MIT · 15 个测试 · 零第三方依赖'),
    },
    {
        'slug': 'hackathon-ops-hub', 'kind': 'public', 'year': '2026', 'home': True, 'icon': 'trophy',
        'title': '潮玩电商 AI 运营中台', 'sub': 'AIY 黑客松铜奖 · 演示站',
        'text': '扣子 Coze 赛道铜奖作品的纯前端复刻：8 个 Agent 在浏览器里跑，补偿、风控、组箱都能现场改输入看结果。',
        'tags': ['AI Agent', '扣子 Coze', '规则引擎', '黑客松'],
        'demo': PAGES + '/chaowan-ai-ops-hub/', 'repo': GH + '/chaowan-ai-ops-hub',
        'lead': 'AIY 黑客松参赛作品，获扣子 Coze 赛道铜奖。原版跑在扣子平台上，赛后我把同一套逻辑用纯前端重写成演示站：数据虚构，断网也能用。',
        'facts': [('奖项', '扣子 Coze 赛道铜奖'), ('Agent', '8 个'), ('知识库', '敏感词 68 · FAQ 31 · 商品 50'), ('测试', '13 个')],
        'highlights': [
            '8 个 Agent：补偿决策、社群风控、数据问答、智能选品、智能组箱、积分兑换、用户画像、智能客服。',
            '规矩交给知识库记，算数交给代码算：补偿规则改一个数字立刻生效；按用户 ID 查数据一律精确查询，不会赔错人。',
            '统一 JSON 输出契约：思考过程逐条可见，置信度低于 0.8 一律转人工。',
            '5 步主演示：社群告警 → 转投诉处理 → 出补偿方案 → 用户画像 → 计入补偿率，AI 只出建议，人点采纳才生效。',
            '测试保证和原版文档的算例一字不差：补偿 ¥32,800、劝退结算 ¥480、组箱成本 ¥2,831 / 毛利 40.02%。',
        ],
        'story': [
            '比赛时这是团队作品，我负责统筹和路演主讲：把业务拆成智能体施工图纸、按四条线分工、写三个版本的路演逐字稿，技术实现由队长负责。',
            '赛后我把 8 个 Agent 的判断逻辑重写成浏览器里的规则引擎，任何人打开网页就能试，不依赖扣子、不需要账号。',
        ],
        'source': ('zj85997-hash/chaowan-ai-ops-hub', 'MIT · 13 个测试 · 零依赖'),
    },
    {
        'slug': 'ai-commerce-curriculum', 'kind': 'private', 'year': '2026', 'home': True, 'icon': 'graduation',
        'title': '《AI 赋能商业实战》体系课', 'sub': '某高职院校 · 校企合作',
        'text': '60 课时、22 讲、720 页课件，每讲都有演示、实操和评价量规；还能压成每天交一个作品的 5 天训练营。',
        'tags': ['课程体系', '校企合作', 'AI 电商', '训练营'],
        'lead': '给一所高职院校从零搭的 AI 电商课程体系：60 课时、22 讲、720 页课件，配校企合作方案。',
        'facts': [('课时', '60'), ('讲数', '22 讲'), ('课件', '720 页'), ('训练营', '5 天')],
        'highlights': [
            '六大模块：AI 认知 → 短视频与短剧 → 电商全链路 → 营销获客 → 行业应用 → 综合实战与就业。',
            '每讲统一环节：学习目标、课前诊断、核心知识、教师演示、学生实操、评价量规、常见错误、课后任务。换任何老师都能照着上。',
            '60 课时可以压成 5 天训练营，每天产出一个成品：带货短视频 → 商品素材包 → 直播话术 → 产品落地页。',
            '配套「课程教学 + 店铺实战 + 基地陪跑」三位一体的校企合作方案和校领导汇报材料。',
        ],
        'story': [
            '我是这套课的总设计，也负责校企合作方案。设计原则只有一条：每一讲先定学员要带走的成品，再倒推讲什么、练什么、怎么评。',
            '交付件包括 22 个可编辑的课件、5 天训练营的讲师框架、校企合作方案和汇报材料。',
        ],
    },
    {
        'slug': 'vibecamp', 'kind': 'private', 'year': '2026', 'home': True, 'icon': 'sparkle',
        'title': 'VibeCamp 同频造物营', 'sub': '青少年 · AI Web Coding',
        'text': '3.5 天带孩子用 WorkBuddy 和 Claude Code 从零做出自己的 App 和游戏，在家长面前路演。',
        'tags': ['青少年', 'Web Coding', '项目制', 'Claude Code'],
        'lead': '青少年 AI 训练营第一期，我是联合创始人和主讲。不讲概念讲作品：3.5 天里，每个孩子都做出自己的作品并上台路演。',
        'facts': [('时长', '3.5 天 · 22 小时'), ('平台', 'WorkBuddy + Claude Code'), ('对象', '青少年'), ('期数', '已交付 1 期')],
        'highlights': [
            '课程路径：环境部署和破冰 → AI 通识 + 情绪转盘 → 贪吃蛇 + 个人项目立项 → 冲刺、路演、结营。',
            '学员作品：游泳训练成绩记录 App、开放世界驾驶游戏、策略游戏，还有最小的学员原创的「异常门」游戏。',
            '结营日请家长到场看作品展示，并邀请外部老师点评。',
            '开课前逐台检查学员电脑环境，备好备用机，应对兼容问题。',
        ],
        'story': [
            '第一天上午就发现，「先讲后做」留不住孩子。中途复盘后，下午改成先上手、后讲解。',
            '课后总结出三条改进方向：少讲多做、全程互动、按水平分层。',
        ],
    },
    {
        'slug': 'ai-business-course', 'kind': 'private', 'year': '2026', 'home': False, 'icon': 'briefcase',
        'title': '把 AI 变成经营能力', 'sub': '企业老板 · 系列课',
        'text': '开场不讲概念，直接现场演示 AI 帮老板找客户、帮 HR 筛简历，再讲怎么把 AI 变成经营能力。',
        'tags': ['企业内训', '逐字稿', '课程体系', '代理商课'],
        'lead': '给企业老板讲的 AI 系列课。我是签约讲师和课程研发，2026 年 7–8 月主讲。',
        'facts': [('路演版', '2 小时'), ('课件', '25 页 + 全篇逐字稿'), ('体系', '初级 · 中级 · 高阶'), ('代理商课', '90–100 分钟')],
        'highlights': [
            '2 小时企业路演版：25 页 PPT 加全篇逐字稿，风格是「脱口秀 + 职场隐喻」。',
            '开场不做自我介绍，直接现场演示获客应用和 HR 智能体，用结果抓住老板。',
            '三级课程体系：初级对话式 AI → 中级智能体搭建与 Web Coding → 高阶企业内训。',
            '代理商培训课按「每 10 分钟一个钩子，每 20 分钟一次互动」设计节奏。',
        ],
        'story': [
            '这门课从结果讲起：先让老板看到 AI 替他干活，再讲背后的方法。逐字稿是一个字一个字写出来的。',
            '配套还写了《AI 通识课程体系设计》、学员手册和面向宝妈的通识课版本。',
        ],
    },
    {
        'slug': 'enterprise-ai-solutions', 'kind': 'private', 'year': '2026', 'home': False, 'icon': 'route',
        'title': '企业 AI 定制方案', 'sub': 'FDE · 3 家企业',
        'text': '为外贸制造企业、资产评估机构、传媒公司交付 AI 方案，提炼出「七步链路」和「场景打分卡」。',
        'tags': ['FDE', 'BRD / PRD', '智能体', '方法论'],
        'lead': '作为 FDE（前沿部署工程师）交付的三份企业 AI 定制方案，以及从中提炼出来、可以教的方法。',
        'facts': [('客户', '3 家'), ('方法', '七步链路'), ('工具', '场景打分卡'), ('交付', '方案六件套')],
        'highlights': [
            '外贸制造企业：AI 化转型全案，含 BRD、PRD、实施计划、架构与技术设计、UI 规范，外加 HR 智能体。',
            '资产评估机构：6 份定制方案，从需求、知识库、数据获取到建库与智能体交付。',
            '传媒公司：智能提词器，从 PRD 做到 MVP 报价、人员分工和开发成本评估。',
            'FDE 七步链路：进企业 → 懂业务 → 梳流程 → 找场景 → 做应用 → 跑结果 → 持续优化。',
            '场景打分卡：耗人程度 × 收入影响 × 数据可得性，十分钟定位第一个该改的环节。',
        ],
        'story': [
            '交付方案的过程本身就是最好的教材。我把三个项目里反复用到的步骤整理成方法，学员拿去就能给企业写一份敢签字的方案。',
        ],
    },
]

# ---------------------------------------------------------------- 网站
SITES = [
    {'name': 'InFlow FDE 操盘台', 'sub': '在线演示 · 多 Agent', 'icon': 'cpu', 'home': True,
     'text': '对总指挥说一句话，看任务分到部门、数字员工出报告，再去审批收件箱拍板。',
     'url': PAGES + '/inflow-fde/', 'domain': 'zj85997-hash.github.io/inflow-fde'},
    {'name': '潮玩 AI 运营中台', 'sub': '演示站 · 8 个 Agent', 'icon': 'trophy', 'home': True,
     'text': '黑客松铜奖作品的纯前端复刻：社群风控、补偿决策、组箱定价，打开就能试。',
     'url': PAGES + '/chaowan-ai-ops-hub/', 'domain': 'zj85997-hash.github.io/chaowan-ai-ops-hub'},
    {'name': '家长版 · 一键复制', 'sub': '网页工具', 'icon': 'copy', 'home': True,
     'text': '浏览器打开，点「复制」，把三个家庭智能体粘进扣子、智谱清言、豆包。',
     'url': PAGES + '/family-ai-agents/web/家长版-一键复制.html', 'domain': 'family-ai-agents/web/家长版'},
    {'name': '亲子沟通翻译官', 'sub': '网页工具 · 自带 Key', 'icon': 'message', 'home': True,
     'text': '填上自己的 DeepSeek 或兼容接口的 Key，直接和翻译官对话，Key 只存在浏览器里。',
     'url': PAGES + '/family-ai-agents/web/翻译官-可对话版.html', 'domain': 'family-ai-agents/web/翻译官'},
    {'name': '腾讯会议考勤 Skill', 'sub': '项目主页', 'icon': 'calendar', 'home': True,
     'text': '日报和周报长什么样、30 秒试跑命令，都在这一页。',
     'url': PAGES + '/tencent-meeting-attendance-skill/', 'domain': 'zj85997-hash.github.io/tencent-meeting-…'},
    {'name': '第二大脑汇聚管线', 'sub': '项目主页', 'icon': 'layers', 'home': True,
     'text': '四个来源怎么汇进 Obsidian，5 分钟离线演示怎么跑。',
     'url': PAGES + '/obsidian-second-brain-pipeline/', 'domain': 'zj85997-hash.github.io/obsidian-second-…'},
    {'name': 'AI 家庭智能体模板包', 'sub': '项目主页', 'icon': 'users', 'home': False,
     'text': '三个家庭 AI 助手的介绍页，网页工具的入口也在这里。',
     'url': PAGES + '/family-ai-agents/', 'domain': 'zj85997-hash.github.io/family-ai-agents'},
]

# ---------------------------------------------------------------- 现场
# 照片截自课程录像，视频去掉了声音。只选讲台和全场视角：不放观众特写，不放未成年人。
# 每一项：(文件名, 说明, 版式)。文件在 assets/gallery/，-s 结尾的是缩略图；文件名以 -v数字 结尾的是视频。
# 版式：big 占 2×2，wide 占 2×1，tall 占 1×2，空字符串占 1×1。
GALLERY = [
    {
        'id': 'incubator', 'date': '2026.09', 'role': '主讲', 'title': '主理人孵化计划 · 第一期',
        'topic': '《AI 新商业：时代的确定性机遇》',
        'desc': '第一期的开场课：企业怎么用 AI 做新增长，个人怎么做新生意；再讲 FDE 怎么进企业，把散在各处的经验变成能复用的数字员工。',
        'items': [
            ('2026-09-incubator-01', '开场：AI 新商业，时代的确定性机遇', 'big'),
            ('2026-09-incubator-v1', '讲「企业新增长 · 个人新生意」', 'wide'),
            ('2026-09-incubator-02', '讲台边：让 AI 成为企业经营基础设施', ''),
            ('2026-09-incubator-05', '讲 FDE 怎么进企业做落地', ''),
            ('2026-09-incubator-03', '现场举手互动', 'wide'),
            ('2026-09-incubator-v2', '全场举手', ''),
            ('2026-09-incubator-07', '传统经营方式：公司的经验散在各处', ''),
            ('2026-09-incubator-04', '全场视角', 'wide'),
            ('2026-09-incubator-06', '入企业做 FDE：案例拆解', ''),
            ('2026-09-incubator-08', '资料、规则、起步点：经验散在三个地方', ''),
        ],
    },
    {
        'id': 'transform', 'date': '2026.10', 'role': '主讲', 'title': '企业 AI 转型分享会',
        'topic': '《企业 AI 化转型》',
        'desc': '给企业老板讲 AI 转型：从智能工厂、黑灯工厂讲到「人走了，数字员工继续干活」，最后落到自己公司先改哪一步。',
        'items': [
            ('2026-10-transform-04', '人走了，数字员工继续干活', 'big'),
            ('2026-10-transform-01', '开场：企业 AI 化转型', 'tall'),
            ('2026-10-transform-v1', '讲数字员工', ''),
            ('2026-10-transform-02', '智能工厂的生产现场', 'wide'),
            ('2026-10-transform-03', '黑灯工厂：每 1 秒下线一部手机', ''),
            ('2026-10-transform-v2', '讲智能工厂', ''),
            ('2026-10-transform-05', '中国城市 AI 发展格局', ''),
        ],
    },
]
# 首页只放 7 格，拼成 4 列 × 3 行
HOME_GALLERY = [
    ('incubator', '2026-09-incubator-01', 'big'), ('transform', '2026-10-transform-04', 'wide'),
    ('incubator', '2026-09-incubator-v2', ''), ('transform', '2026-10-transform-02', ''),
    ('incubator', '2026-09-incubator-03', 'wide'), ('transform', '2026-10-transform-v2', ''),
    ('incubator', '2026-09-incubator-05', ''),
]

# ---------------------------------------------------------------- 联系
CONTACT = [
    ('联系方式', [
        {'icon': 'message', 'label': '微信', 'value': 'wuweizhijing002', 'copy': True},
        {'icon': 'mail', 'label': '邮箱', 'value': 'zj85997@gmail.com', 'copy': True},
    ]),
    ('主页与社区', [
        {'icon': 'github', 'label': 'GitHub', 'value': 'zj85997-hash', 'url': GH},
        {'icon': 'video', 'label': '视频号', 'value': 'AI实操付老师', 'copy': True},
    ]),
]

# ---------------------------------------------------------------- 文章
POSTS = [
    {
        'slug': 'second-brain-pipeline', 'date': '2026-10-27', 'tags': ['Obsidian', '知识管理', '自动化'],
        'title': '把 2400 篇笔记汇进 Obsidian：我的第二大脑管线',
        'excerpt': '录音转写、会议逐字稿、飞书方案、手机备忘录，散在四个地方谁也找不到。我写了一条管线把它们汇进同一个 Obsidian 库，现在开源了，附 5 分钟离线演示。',
        'blocks': [
            ('h2', '问题：笔记散在四个地方'),
            ('p', '我的笔记来自四个地方：得到大脑的录音转写、钉钉听记的会议逐字稿、飞书的方案文档、手机里的苹果备忘录。每个工具单独都好用，合在一起却是四座孤岛：想找一次课的复盘，得先想起它当时记在哪。'),
            ('p', '所以我写了一条管线，把它们汇进同一个 Obsidian 库。现在库里有 2400 多篇笔记，按项目线分好了类。'),
            ('h2', '思路：先进收件箱，再分类入库'),
            ('p', '整条管线分四步：'),
            ('ol', [
                '**采集**：每个来源先转成统一格式的 Markdown，带标题、日期、来源和 ID。同一条不会重复采集，中断了重跑会接着来。',
                '**分类**：按配置里的规则，把笔记放进「项目线 / 案例」文件夹。',
                '**入库**：默认只新增文件，不删除、不覆盖库里已有的内容。',
                '**目录页**：首页、板块总览、案例时间线自动生成，只更新页面里自动生成的那一段，手写的背景和总结原样保留。',
            ]),
            ('p', '日常只要一条命令：'),
            ('pre', 'python3 -m sbp sync'),
            ('h2', '分类规则怎么写'),
            ('p', '规则写在配置文件里，按这个顺序匹配：先看人工指定的标题，再看标题规则，再看正文前 600 字，都没命中就进「待归类」。'),
            ('pre', '"rules": [\n  {"line": "99-存档", "title": "空白录音|测试录音"},\n  {"line": "01-客户项目", "case": "案例P01-某制造企业·AI培训", "title": "P01|培训考核"}\n]'),
            ('p', '先用 `import --dry-run` 预览每篇会放到哪里，确认没问题再正式入库。'),
            ('h2', '给别人看之前：一键代号化'),
            ('p', '我会把库拿给学员看。为了保护隐私，管线带了一个替换功能：人名换成 A001、公司换成 P01，可以导出一份副本，原库不动。加上 `--rename` 连文件名一起改，正文里的双链也同步改，链接不会断。'),
            ('pre', 'python3 -m sbp replace --out ~/Desktop/可分享版 --rename'),
            ('h2', '安全上的几条底线'),
            ('ul', [
                '代码里没有任何凭据：登录交给各家官方命令行工具，飞书凭据只从环境变量读。',
                '证书校验始终开启。公司网络用自签证书时，指定证书文件，而不是关掉校验。',
                '令牌文件只有自己能读；个人配置、收件箱和库都在 `.gitignore` 里。',
            ]),
            ('h2', '自己试一试'),
            ('pre', 'git clone https://github.com/zj85997-hash/obsidian-second-brain-pipeline.git\ncd obsidian-second-brain-pipeline\npython3 -m sbp demo --out ./sbp-demo'),
            ('p', '用 Obsidian 打开 `sbp-demo/vault`，12 篇虚构笔记已经分好类，不需要任何账号。源码在 [GitHub](https://github.com/zj85997-hash/obsidian-second-brain-pipeline)，MIT 许可。'),
        ],
    },
    {
        'slug': 'attendance-skill', 'date': '2026-10-27', 'tags': ['AI Skill', 'Python', '培训管理'],
        'title': '把腾讯会议考勤交给 AI：一个 Skill 的做法',
        'excerpt': '线上打卡群每天要统计准时、迟到、请假，腾讯会议导出表里的昵称却五花八门。我把判定规则写成一个零依赖的 Skill，AI 和命令行都能用。',
        'blocks': [
            ('h2', '要解决的问题'),
            ('p', '线上打卡群每天都要统计考勤。腾讯会议能导出「成员参会概况」，麻烦在昵称：有人带地区后缀，有人英文大小写不一，有人手机和平板同时入会，有时还是家长代为入会。手工一个个对名单，又慢又容易错。'),
            ('h2', '花名册是唯一基准'),
            ('p', '花名册写四样东西：在册人员、名字映射、规则、排除人员。下面三种情况脚本会自动处理，不用登记：'),
            ('ul', [
                '昵称和规范名完全相同；',
                '只多了括号后缀，比如「A004(三组)」；',
                '只是英文大小写不同，比如「a007」。',
            ]),
            ('p', '其余的变体在映射表里登记一次就行。有人加入、退出、改昵称时，先改花名册，再统计。'),
            ('h2', '规则写清楚，边界精确到秒'),
            ('ul', [
                '**准时线**：首次入会时间不晚于准时线算准时。06:00:00 算准时，06:00:01 就算迟到。',
                '**缺勤线**：晚于缺勤线才入会，算缺勤；可以不设。',
                '**统计日**：不在统计日的导出照样出日报，但标注「仅供参考」，周报不计入。',
                '**每周免罚请假**：每周前 N 次请假不计，超出的次数在周报里按迟到计。',
            ]),
            ('h2', '怎么证明它没算错'),
            ('p', '通用化之前，我用真实的导出表把新脚本和原来的脚本逐人比对，700 人次的结果完全一致。现在仓库里有 16 个测试，示例数据全部虚构，人名一律用代号。'),
            ('h2', '怎么用'),
            ('pre', 'python3 scripts/attendance_stat.py examples/exports/*.xlsx \\\n  --roster examples/roster.example.md --leave-file examples/leaves.example.csv --out out'),
            ('p', '或者把文件夹装进 Claude Code、WorkBuddy 这类 AI 工具，对 AI 说「统计今天的考勤」。源码在 [GitHub](https://github.com/zj85997-hash/tencent-meeting-attendance-skill)，MIT 许可。'),
        ],
    },
]

# ---------------------------------------------------------------- 图标（24×24 线条图标）
ICONS = {
    'home': '<path d="M3 10.5 12 3l9 7.5V20a1 1 0 0 1-1 1h-5v-6H9v6H4a1 1 0 0 1-1-1z"/>',
    'grid': '<rect x="3.5" y="3.5" width="7" height="7" rx="1.5"/><rect x="13.5" y="3.5" width="7" height="7" rx="1.5"/><rect x="3.5" y="13.5" width="7" height="7" rx="1.5"/><rect x="13.5" y="13.5" width="7" height="7" rx="1.5"/>',
    'globe': '<circle cx="12" cy="12" r="9"/><path d="M3 12h18"/><path d="M12 3a14 14 0 0 1 0 18a14 14 0 0 1 0-18z"/>',
    'pen': '<path d="M4 20h4L19 9a2.83 2.83 0 0 0-4-4L4 16z"/><path d="M13.5 6.5l4 4"/>',
    'moon': '<path d="M20 14.5A8 8 0 0 1 9.5 4a8 8 0 1 0 10.5 10.5z"/>',
    'sun': '<circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.93 4.93l1.41 1.41M17.66 17.66l1.41 1.41M2 12h2M20 12h2M4.93 19.07l1.41-1.41M17.66 6.34l1.41-1.41"/>',
    'sparkle': '<path d="M12 3l1.9 5.1L19 10l-5.1 1.9L12 17l-1.9-5.1L5 10l5.1-1.9z"/><path d="M19 3v4M17 5h4"/>',
    'user': '<circle cx="12" cy="8" r="4"/><path d="M4 21a8 8 0 0 1 16 0"/>',
    'cpu': '<rect x="6" y="6" width="12" height="12" rx="2"/><rect x="9.5" y="9.5" width="5" height="5" rx="1"/><path d="M9 2v4M15 2v4M9 18v4M15 18v4M2 9h4M2 15h4M18 9h4M18 15h4"/>',
    'terminal': '<rect x="3" y="4" width="18" height="16" rx="2"/><path d="M7 9l3 3-3 3"/><path d="M12.5 15H17"/>',
    'layers': '<path d="M12 3 3 8l9 5 9-5z"/><path d="M3 13l9 5 9-5"/>',
    'chev': '<path d="M9 6l6 6-6 6"/>',
    'arrow-ur': '<path d="M7 17 17 7"/><path d="M8 7h9v9"/>',
    'arrow-left': '<path d="M19 12H5"/><path d="M11 6l-6 6 6 6"/>',
    'arrow-down': '<path d="M12 5v14"/><path d="M6 13l6 6 6-6"/>',
    'copy': '<rect x="9" y="9" width="11" height="11" rx="2"/><path d="M5 15V6a2 2 0 0 1 2-2h9"/>',
    'check': '<path d="M5 12.5l4.5 4.5L19 7.5"/>',
    'lock': '<rect x="5" y="11" width="14" height="10" rx="2"/><path d="M8 11V7a4 4 0 0 1 8 0v4"/>',
    'mail': '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3.5 7l8.5 6 8.5-6"/>',
    'message': '<path d="M21 11.5a8.5 8.5 0 0 1-12.3 7.6L3 21l1.9-5.4A8.5 8.5 0 1 1 21 11.5z"/>',
    'book': '<path d="M3 5h6a3 3 0 0 1 3 3v12a2 2 0 0 0-2-2H3z"/><path d="M21 5h-6a3 3 0 0 0-3 3v12a2 2 0 0 1 2-2h7z"/>',
    'graduation': '<path d="M2 9l10-5 10 5-10 5z"/><path d="M6 11v5c3.5 2.2 8.5 2.2 12 0v-5"/><path d="M22 9v5"/>',
    'trophy': '<path d="M8 4h8v5a4 4 0 0 1-8 0z"/><path d="M8 6H5a3 3 0 0 0 3 4.5M16 6h3a3 3 0 0 1-3 4.5"/><path d="M12 13v4M8.5 21h7M10 17h4"/>',
    'users': '<circle cx="9" cy="8" r="3.5"/><path d="M2.5 20a6.5 6.5 0 0 1 13 0"/><path d="M16 4.6a3.5 3.5 0 0 1 0 6.8"/><path d="M18 14.2A6.5 6.5 0 0 1 21.5 20"/>',
    'calendar': '<rect x="3" y="5" width="18" height="16" rx="2"/><path d="M3 10h18M8 3v4M16 3v4"/><path d="M8 14h3M8 17h6"/>',
    'briefcase': '<rect x="3" y="7" width="18" height="13" rx="2"/><path d="M8.5 7V5.5A1.5 1.5 0 0 1 10 4h4a1.5 1.5 0 0 1 1.5 1.5V7"/><path d="M3 12.5h18"/>',
    'route': '<circle cx="6" cy="19" r="2"/><circle cx="18" cy="5" r="2"/><path d="M8 19h7.5a3.5 3.5 0 0 0 0-7h-7a3.5 3.5 0 0 1 0-7H16"/>',
    'video': '<rect x="3" y="6" width="13" height="12" rx="2"/><path d="M16 10.5l5-3v9l-5-3"/>',
    'code': '<path d="M8 8l-4 4 4 4"/><path d="M16 8l4 4-4 4"/><path d="M13.5 5l-3 14"/>',
    'camera': '<path d="M4 8.5h3.2L9 6h6l1.8 2.5H20a1 1 0 0 1 1 1V18a1 1 0 0 1-1 1H4a1 1 0 0 1-1-1V9.5a1 1 0 0 1 1-1z"/><circle cx="12" cy="13.5" r="3.5"/>',
    'play': '<path d="M8.5 5.8v12.4L19 12z"/>',
    'x': '<path d="M6 6l12 12"/><path d="M18 6L6 18"/>',
}
GITHUB_MARK = ('<svg class="i fill" viewBox="0 0 16 16" aria-hidden="true"><path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 '
               '0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 '
               '2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 '
               '2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 '
               '1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0 0 16 8c0-4.42-3.58-8-8-8z"/></svg>')


def icon(name, cls=''):
    if name == 'github':
        return GITHUB_MARK
    return '<svg class="i%s" viewBox="0 0 24 24" aria-hidden="true">%s</svg>' % ((' ' + cls) if cls else '', ICONS[name])


def esc(s):
    return html.escape(str(s), quote=True)


def inline(s):
    """正文里的简单标记：`代码`、**加粗**、[文字](链接)。"""
    s = esc(s)
    s = re.sub(r'`([^`]+)`', r'<code>\1</code>', s)
    s = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', s)
    s = re.sub(r'\[([^\]]+)\]\(([^)\s]+)\)', r'<a href="\2" target="_blank" rel="noopener">\1</a>', s)
    return s


FAVICON = ("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E"
           "%3Crect width='32' height='32' rx='9' fill='%2317171a'/%3E%3Ccircle cx='16' cy='16' r='5' fill='%23fafafa'/%3E%3C/svg%3E")
THEME_BOOT = ("(function(){var d=document.documentElement;d.classList.remove('no-js');try{var t=localStorage.getItem('theme');"
              "if(t!=='light'&&t!=='dark'){t=window.matchMedia&&window.matchMedia('(prefers-color-scheme: dark)').matches?'dark':'light'}"
              "d.setAttribute('data-theme',t)}catch(e){}})();")


def avatar_html(p):
    for ext in ('jpg', 'jpeg', 'png', 'webp'):
        if os.path.exists(os.path.join(ROOT, 'assets', 'img', 'avatar.' + ext)):
            return '<img src="%sassets/img/avatar.%s" alt="付钟浩 Alex">' % (p, ext)
    return '<span class="mono-letter" aria-hidden="true">A</span>'


# ---------------------------------------------------------------- 页面骨架
def nav(p, active):
    items = [('home', '首页', 'index.html'), ('grid', '项目', 'projects/index.html'), ('camera', '现场', 'gallery/index.html'),
             ('globe', '网站', 'sites/index.html'), ('pen', '博客', 'blog/index.html')]
    links = ''.join('<a href="%s%s"%s>%s<span>%s</span></a>' % (
        p, href, ' class="active" aria-current="page"' if label == active else '', icon(ic), label) for ic, label, href in items)
    return ('<header class="site-nav"><div class="container"><div class="bar">'
            '<a class="brand" href="%sindex.html"><span class="brand-dot"></span>%s</a>'
            '<nav class="nav-links" aria-label="主导航">%s</nav>'
            '<div class="nav-tools"><a class="icon-btn" href="%s" target="_blank" rel="noopener" aria-label="GitHub">%s</a>'
            '<button class="icon-btn theme-btn" type="button" data-theme-toggle aria-label="切换深浅色">%s%s</button></div>'
            '</div></div></header>') % (p, esc(SITE['brand']), links, GH, icon('github'), icon('moon', 'moon'), icon('sun', 'sun'))


def footer():
    return ('<footer class="site-foot"><div class="container">'
            '<span class="left"><span class="brand-dot"></span>%s</span>'
            '<span class="right">北京时间 <span data-clock>--:--:--</span> · © 2026</span>'
            '</div></footer>') % esc(SITE['footer'])


def page(title, desc, body, p, active, after=''):
    return '''<!DOCTYPE html>
<html lang="zh-CN" class="no-js" data-theme="light">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>%(title)s</title>
<meta name="description" content="%(desc)s">
<meta property="og:title" content="%(title)s">
<meta property="og:description" content="%(desc)s">
<meta property="og:type" content="website">
<meta name="theme-color" content="#e0e3ea">
<link rel="icon" href="%(fav)s">
<script>%(boot)s</script>
<link rel="stylesheet" href="%(p)sassets/css/style.css">
</head>
<body>
%(nav)s
<main class="container">
%(body)s
</main>
%(footer)s
%(after)s<script src="%(p)sassets/js/main.js" defer></script>
</body>
</html>
''' % {'title': esc(title), 'desc': esc(desc), 'fav': FAVICON, 'boot': THEME_BOOT, 'p': p,
       'nav': nav(p, active), 'body': body, 'footer': footer(), 'after': after}


def eyebrow(num, ic, label):
    return '<div class="eyebrow"><span class="num">%s</span><span class="sep">/</span>%s<span>%s</span></div>' % (num, icon(ic), label)


def section(sid, rail, num, ic, label, title, desc, inner):
    return ('<section class="section" id="%s" data-rail="%s">%s<h2>%s</h2>%s%s</section>'
            % (sid, rail, eyebrow(num, ic, label), title, ('<p class="desc">%s</p>' % desc) if desc else '', inner))


def tags_html(tags):
    return '<div class="tags">%s</div>' % ''.join('<span class="tag">%s</span>' % esc(t) for t in tags)


def badge(kind, full=False):
    text = ('公开项目' if full else '公开') if kind == 'public' else ('私有项目' if full else '私有')
    return '<span class="badge%s">%s</span>' % ('' if kind == 'public' else ' private', text)


def project_card(pr, idx, total, p):
    detail = '%sprojects/%s.html' % (p, pr['slug'])
    if pr['kind'] == 'public':
        actions = ('<a class="btn solid sm" href="%s">查看详情%s</a>'
                   '<a class="btn ghost sm" href="%s" target="_blank" rel="noopener">%s演示站</a>') % (detail, icon('chev'), pr['demo'], icon('globe'))
    else:
        actions = '<a class="btn sm" href="%s">查看简介%s</a>' % (detail, icon('chev'))
    return ('<article class="project-card glass corners gx reveal" data-kind="%s">'
            '<div class="pc-head"><span class="icon-tile">%s</span><span class="pc-meta"><span>%02d / %02d</span>%s<span>%s</span></span></div>'
            '<h3><a href="%s">%s</a></h3><p class="sub">%s</p><p class="text">%s</p>%s<div class="pc-actions">%s</div></article>'
            ) % (pr['kind'], icon(pr['icon']), idx, total, badge(pr['kind']), pr['year'], detail, esc(pr['title']),
                 esc(pr['sub']), esc(pr['text']), tags_html(pr['tags']), actions)


def site_card(s):
    return ('<a class="site-card glass corners gx reveal" href="%s" target="_blank" rel="noopener">'
            '<div class="sc-head"><span class="icon-tile">%s</span><span class="round-btn">%s</span></div>'
            '<h3>%s</h3><p class="sub">%s</p><p class="text">%s</p><div class="domain">%s<span>%s</span></div></a>'
            ) % (esc(s['url']), icon(s['icon']), icon('arrow-ur'), esc(s['name']), esc(s['sub']), esc(s['text']), icon('globe'), esc(s['domain']))


def post_card(post, p):
    return ('<a class="post-card glass gx reveal" href="%sblog/%s.html"><div class="post-meta"><span>%s</span><span>%s</span></div>'
            '<h3>%s</h3><p>%s</p></a>') % (p, post['slug'], post['date'], esc('，'.join(post['tags'])), esc(post['title']), esc(post['excerpt']))


def more_btn(href, text):
    return '<a class="btn btn-more" href="%s">%s%s</a>' % (href, text, icon('chev'))


def gallery_event(eid):
    return next(e for e in GALLERY if e['id'] == eid)


def gallery_tile(event, slug, cap, span, p):
    g = p + 'assets/gallery/'
    label = '%s · %s' % (event['title'], cap)
    cls = ('tile ' + span).strip()
    if re.search(r'-v\d+$', slug):
        return ('<button class="%s is-video" type="button" data-type="video" data-full="%s%s.mp4" data-poster="%s%s.jpg" data-cap="%s" aria-label="播放视频：%s">'
                '<video muted loop playsinline preload="none" poster="%s%s-s.jpg" data-src="%s%s.mp4" aria-hidden="true"></video>'
                '<span class="play-badge">%s</span><span class="tile-cap">%s</span></button>'
                ) % (cls, g, slug, g, slug, esc(label), esc(cap), g, slug, g, slug, icon('play', 'fill'), esc(cap))
    return ('<button class="%s" type="button" data-type="img" data-full="%s%s.jpg" data-cap="%s" aria-label="看大图：%s">'
            '<img src="%s%s-s.jpg" alt="%s" loading="lazy" decoding="async"><span class="tile-cap">%s</span></button>'
            ) % (cls, g, slug, esc(label), esc(cap), g, slug, esc(cap), esc(cap))


def lightbox():
    return ('<dialog class="lightbox" aria-label="大图浏览"><figure class="lb-stage"><img class="lb-img" alt="">'
            '<video class="lb-video" muted loop playsinline controls></video></figure>'
            '<div class="lb-bar"><span class="lb-cap"></span><span class="lb-count"></span></div>'
            '<button class="lb-btn lb-prev" type="button" aria-label="上一张">%s</button>'
            '<button class="lb-btn lb-next" type="button" aria-label="下一张">%s</button>'
            '<button class="lb-btn lb-close" type="button" aria-label="关闭">%s</button></dialog>\n'
            ) % (icon('arrow-left'), icon('chev'), icon('x'))


def gallery_counts():
    videos = sum(1 for e in GALLERY for it in e['items'] if re.search(r'-v\d+$', it[0]))
    photos = sum(len(e['items']) for e in GALLERY) - videos
    return photos, videos


# ---------------------------------------------------------------- 首页
def build_home():
    p = ''
    public = [x for x in PROJECTS if x['kind'] == 'public']
    stats = [(str(len(PROJECTS)), '项目'), (str(len(public)), '公开项目'), (str(len(SITES)), '上线网站'), ('10+', '课程研发')]
    hero = ('<section class="hero glass corners gx reveal" id="top" data-rail="开始"><div class="hero-top"><div>'
            '<span class="kicker">%s Hello</span><h1>%s</h1><p class="role">%s</p><p class="tagline">%s</p>'
            '<div class="actions"><a class="btn" href="#contact">%s微信联系</a>'
            '<a class="btn" href="%s" target="_blank" rel="noopener">%sGitHub</a>'
            '<a class="btn ghost" href="#work">看看项目%s</a></div></div>'
            '<div class="avatar-wrap"><div class="avatar">%s</div></div></div>'
            '<div class="stats">%s</div></section>'
            '<div class="scroll-cue">向下探索%s</div>'
            ) % (icon('sparkle'), esc(SITE['name']), esc(SITE['role']), esc(SITE['tagline']), icon('message'), GH, icon('github'),
                 icon('chev'), avatar_html(p), ''.join('<div><b>%s</b><span>%s</span></div>' % s for s in stats), icon('arrow-down'))

    term_data = {
        'commands': [('help', '看看有哪些命令'), ('whoami', '我是谁'), ('skills', '能力标签'), ('courses', '代表课程'),
                     ('projects', '项目列表'), ('sites', '在线网站'), ('contact', '怎么联系我'), ('theme', '切换深浅色'), ('clear', '清屏')],
        'whoami': '付钟浩（Alex）· AI 培训讲师 / FDE · 深圳。' + SITE['tagline'],
        'skills': [(g[0], g[2]) for g in SKILLS],
        'courses': COURSES,
        'projects': [(x['title'], x['sub'], 'projects/%s.html' % x['slug']) for x in PROJECTS],
        'sites': [(s['name'], s['url']) for s in SITES],
        'contact': [(c['label'], c.get('value', '')) for _, items in CONTACT for c in items],
    }
    chips = ''.join('<button class="chip" type="button" data-cmd="%s">%s</button>' % (c, c)
                    for c in ('help', 'whoami', 'skills', 'courses', 'projects', 'sites', 'contact', 'theme'))
    about = ('<div class="about"><div class="about-card glass corners gx reveal">%s</div>'
             '<div class="term glass gx reveal" id="term"><div class="term-head"><span class="who">%s alex@site</span><small>命令可输入，也可点选</small></div>'
             '<div class="term-out" aria-live="polite"><div class="line muted">输入 <b>help</b> 查看命令清单，也可以直接点下面的命令。</div></div>'
             '<div class="term-foot"><label class="term-input">$ <input type="text" placeholder="help" aria-label="输入命令" autocomplete="off" spellcheck="false"></label>'
             '<div class="chips">%s</div></div></div></div>'
             ) % (''.join('<p%s>%s</p>' % (' class="lead"' if i == 0 else '', esc(t)) for i, t in enumerate(ABOUT)), icon('terminal'), chips)
    skills = '<div class="grid c2">%s</div>' % ''.join(
        '<div class="skill-card glass gx reveal"><h3>%s%s</h3>%s</div>' % (icon(ic), esc(name), tags_html(tags)) for name, ic, tags in SKILLS)
    home_projects = [x for x in PROJECTS if x['home']]
    work = '<div class="grid c3">%s</div>%s' % (
        ''.join(project_card(x, PROJECTS.index(x) + 1, len(PROJECTS), p) for x in home_projects), more_btn('projects/index.html', '全部项目'))
    sites = '<div class="grid c3">%s</div>%s' % (''.join(site_card(s) for s in SITES if s['home']), more_btn('sites/index.html', '全部网站'))
    journal = '<div class="grid c2">%s</div>%s' % (''.join(post_card(x, p) for x in POSTS[:2]), more_btn('blog/index.html', '全部文章'))
    groups = []
    for label, items in CONTACT:
        row = []
        for c in items:
            val = esc(c.get('value', ''))
            todo = '【' in c.get('value', '')
            inner = '%s<span class="k">%s</span><span class="val%s">%s</span>' % (icon(c['icon']), esc(c['label']), ' todo' if todo else '', val)
            if c.get('url'):
                row.append('<a class="contact-item no-copy" href="%s" target="_blank" rel="noopener">%s</a>' % (c['url'], inner))
            elif c.get('copy') and not todo:
                row.append('<span class="contact-item">%s<button class="copy-btn" type="button" data-copy="%s" aria-label="复制 %s">%s</button></span>'
                           % (inner, val, esc(c['label']), icon('copy')))
            else:
                row.append('<span class="contact-item no-copy">%s</span>' % inner)
        groups.append('<div class="contact-group"><div class="label">%s</div><div class="contact-row">%s</div></div>' % (esc(label), ''.join(row)))
    contact = '<div class="contact-card glass corners reveal">%s</div>' % ''.join(groups)

    body = hero
    body += section('about', '关于', '01', 'user', 'About', '关于我', None, about)
    body += section('skills', '能力', '02', 'cpu', 'Skills', '能力', '下面这些标签，都来自真正交付过的课程和项目。', skills)
    body += section('work', '项目', '03', 'grid', 'Work', '精选项目',
                    '课程和项目一起算，一共 %d 个：公开的能看演示和源码，客户和团队项目只放简介。' % len(PROJECTS), work)
    photos, videos = gallery_counts()
    live = '<div class="mosaic home-mosaic reveal">%s</div>%s' % (
        ''.join(gallery_tile(gallery_event(eid), slug, next(c for s2, c, _ in gallery_event(eid)['items'] if s2 == slug), span, p)
                for eid, slug, span in HOME_GALLERY), more_btn('gallery/index.html', '全部现场'))
    body += section('live', '现场', '04', 'camera', 'On Site', '授课现场',
                    '讲过的课，现场是这样的：%d 场、%d 张照片、%d 段视频，都截自课程录像。点开看大图。' % (len(GALLERY), photos, videos), live)
    body += section('sites', '网站', '05', 'globe', 'Sites', '我的网站', '长期在线的页面和小工具，点开就能用。', sites)
    body += section('journal', '文章', '06', 'pen', 'Journal', '最近文章', '项目背后的做法和复盘，写给想自己动手的人。', journal)
    body += section('contact', '联系', '07', 'mail', 'Contact', '联系我', '企业内训、院校课程共建、营地与家长课、AI 落地陪跑，都可以聊。', contact)
    after = lightbox() + '<script type="application/json" id="term-data">%s</script>\n' % json.dumps(term_data, ensure_ascii=False).replace('</', '<\\/')
    return page('%s · %s' % (SITE['name'], SITE['role']), SITE['desc'], body, p, '首页', after)


# ---------------------------------------------------------------- 项目列表与详情
def build_projects_index():
    p = '../'
    pub = sum(1 for x in PROJECTS if x['kind'] == 'public')
    pri = len(PROJECTS) - pub
    body = ('<div class="page-head"><a class="back" href="../index.html">%s返回首页</a><h1>项目</h1>'
            '<p class="desc">一共 %d 个：%d 个公开（可以看演示和源码），%d 个私有（只放简介，细节可以联系我聊）。</p></div>'
            '<div class="filters" role="tablist"><button type="button" class="on" data-filter="all">全部 <span>%d</span></button>'
            '<button type="button" data-filter="public">公开 <span>%d</span></button><button type="button" data-filter="private">私有 <span>%d</span></button></div>'
            '<div class="grid c3">%s</div>'
            ) % (icon('arrow-left'), len(PROJECTS), pub, pri, len(PROJECTS), pub, pri,
                 ''.join(project_card(x, i + 1, len(PROJECTS), p) for i, x in enumerate(PROJECTS)))
    return page('项目 · ' + SITE['name'], '付钟浩 Alex 的课程与项目：%d 个公开，%d 个私有。' % (pub, pri), body, p, '项目')


def build_project(pr, i):
    p = '../'
    prev_pr = PROJECTS[i - 1] if i > 0 else None
    next_pr = PROJECTS[i + 1] if i + 1 < len(PROJECTS) else None
    head = ('<a class="back" href="index.html">%s返回项目列表</a>'
            '<div class="detail-badges">%s<span>%s</span><span>%s</span></div><h1>%s</h1><p class="lead">%s</p>'
            ) % (icon('arrow-left'), badge(pr['kind'], True), pr['year'], esc(pr['sub']), esc(pr['title']), esc(pr['lead']))
    if pr['kind'] == 'public':
        head += ('<div class="actions" style="display:flex;gap:12px;flex-wrap:wrap"><a class="btn solid" href="%s" target="_blank" rel="noopener">%s访问演示站</a>'
                 '<a class="btn" href="%s" target="_blank" rel="noopener">%s在 GitHub 打开%s</a></div>'
                 ) % (pr['demo'], icon('globe'), pr['repo'], icon('github'), icon('arrow-ur'))
    head += '<div class="facts">%s</div>' % ''.join('<div><span>%s</span><b>%s</b></div>' % (esc(k), esc(v)) for k, v in pr['facts'])
    if pr['kind'] == 'private':
        head += '<div class="private-note">%s这是一个私有项目：资料不公开，这里只放简介。想了解细节或看演示，直接联系我。</div>' % icon('lock')
    body = '<div class="page-head detail">%s</div>' % head
    body += section('highlights', '要点', '01', 'sparkle', 'Highlights', '项目要点', None,
                    '<div class="list-card glass corners reveal"><ul class="dash-list">%s</ul></div>' % ''.join('<li>%s</li>' % esc(h) for h in pr['highlights']))
    body += section('story', '细节', '02', 'pen', 'Story', '细节', None,
                    '<div class="story-card glass corners reveal">%s</div>' % ''.join('<p>%s</p>' % esc(s) for s in pr['story']))
    if pr['kind'] == 'public':
        repo, meta = pr['source']
        body += section('source', '源码', '03', 'code', 'Source', '源码', '代码、示例和测试都在 GitHub。',
                        ('<div class="source-card glass corners reveal"><div><div class="repo">%s%s</div><div class="repo-meta">%s</div></div>'
                         '<a class="btn" href="%s" target="_blank" rel="noopener">在 GitHub 查看%s</a></div>') % (icon('github'), esc(repo), esc(meta), pr['repo'], icon('arrow-ur')))
    body += '<div class="detail-tags">%s</div>' % tags_html(pr['tags'])
    pager = '<div class="pager">'
    pager += ('<a class="glass gx prev" href="%s.html"><small>%s上一个</small><b>%s</b></a>' % (prev_pr['slug'], icon('arrow-left'), esc(prev_pr['title']))) if prev_pr else '<span></span>'
    pager += ('<a class="glass gx next" href="%s.html"><small>下一个%s</small><b>%s</b></a>' % (next_pr['slug'], icon('chev'), esc(next_pr['title']))) if next_pr else '<span></span>'
    body += pager + '</div>'
    return page('%s · %s' % (pr['title'], SITE['name']), pr['lead'], body, p, '项目')


# ---------------------------------------------------------------- 现场
def build_gallery():
    p = '../'
    photos, videos = gallery_counts()
    filters = '<button type="button" class="on" data-filter="all">全部 <span>%d</span></button>' % len(GALLERY)
    filters += ''.join('<button type="button" data-filter="%s">%s <span>%s</span></button>' % (e['id'], esc(e['title'].split(' · ')[0]), e['date'])
                       for e in GALLERY)
    events = ''
    for e in GALLERY:
        nv = sum(1 for it in e['items'] if re.search(r'-v\d+$', it[0]))
        events += ('<section class="event glass corners reveal" id="%s" data-kind="%s"><div class="event-head">'
                   '<div class="event-meta"><span class="date">%s</span><span>%s</span><span>%d 张照片 · %d 段视频</span></div>'
                   '<h2>%s</h2><p class="topic">%s</p><p class="desc">%s</p></div><div class="mosaic">%s</div></section>'
                   ) % (e['id'], e['id'], e['date'], esc(e['role']), len(e['items']) - nv, nv, esc(e['title']), esc(e['topic']), esc(e['desc']),
                        ''.join(gallery_tile(e, slug, cap, span, p) for slug, cap, span in e['items']))
    body = ('<div class="page-head"><a class="back" href="../index.html">%s返回首页</a><h1>授课现场</h1>'
            '<p class="desc">截自课程录像：%d 场课、%d 张照片、%d 段静音短视频。点开看大图，左右键翻页。更多课程的现场陆续补上。</p></div>'
            '<div class="filters" role="tablist">%s</div><div class="events">%s</div>'
            ) % (icon('arrow-left'), len(GALLERY), photos, videos, filters, events)
    return page('授课现场 · ' + SITE['name'], '付钟浩 Alex 的授课现场：企业 AI 转型分享会、主理人孵化计划等课程的照片和视频。', body, p, '现场', lightbox())


# ---------------------------------------------------------------- 网站、文章
def build_sites_index():
    p = '../'
    body = ('<div class="page-head"><a class="back" href="../index.html">%s返回首页</a><h1>网站</h1>'
            '<p class="desc">长期在线、点开就能用的页面和工具，一共 %d 个。</p></div><div class="grid c3" style="margin-top:34px">%s</div>'
            ) % (icon('arrow-left'), len(SITES), ''.join(site_card(s) for s in SITES))
    return page('网站 · ' + SITE['name'], '付钟浩 Alex 的在线页面和工具。', body, p, '网站')


def build_blog_index():
    p = '../'
    body = ('<div class="page-head"><a class="back" href="../index.html">%s返回首页</a><h1>博客</h1>'
            '<p class="desc">项目背后的做法和复盘，一共 %d 篇。</p></div><div class="grid c2" style="margin-top:34px">%s</div>'
            ) % (icon('arrow-left'), len(POSTS), ''.join(post_card(x, p) for x in POSTS))
    return page('博客 · ' + SITE['name'], '付钟浩 Alex 的文章：项目背后的做法和复盘。', body, p, '博客')


def reading_minutes(post):
    n = 0
    for kind, val in post['blocks']:
        n += sum(len(v) for v in val) if isinstance(val, list) else len(val)
    return max(1, round(n / 400))


def build_post(post):
    p = '../'
    toc, prose, k = [], [], 0
    for kind, val in post['blocks']:
        if kind == 'h2':
            k += 1
            hid = 's%d' % k
            toc.append('<a href="#%s">%s</a>' % (hid, esc(val)))
            prose.append('<h2 id="%s">%s</h2>' % (hid, esc(val)))
        elif kind == 'p':
            prose.append('<p>%s</p>' % inline(val))
        elif kind in ('ul', 'ol'):
            prose.append('<%s>%s</%s>' % (kind, ''.join('<li>%s</li>' % inline(x) for x in val), kind))
        elif kind == 'pre':
            prose.append('<pre><code>%s</code></pre>' % esc(val))
    body = ('<div class="page-head"><a class="back" href="index.html">%s返回博客</a></div>'
            '<div class="article-layout"><aside class="toc"><div class="kicker">On this page</div>%s</aside>'
            '<article class="article glass corners"><div class="post-meta"><span>%s</span><span>约 %d 分钟</span><span>%s</span></div>'
            '<h1>%s</h1><div class="prose">%s</div></article></div>'
            ) % (icon('arrow-left'), ''.join(toc), post['date'], reading_minutes(post), esc('，'.join(post['tags'])), esc(post['title']), ''.join(prose))
    return page('%s · %s' % (post['title'], SITE['name']), post['excerpt'], body, p, '博客')


def build_404():
    body = ('<div class="page-head" style="text-align:center;margin-top:120px"><div class="kicker">404</div><h1>这一页不存在</h1>'
            '<p class="desc">链接可能写错了，或者页面已经搬家。</p><p style="margin-top:26px"><a class="btn solid" href="/">%s回到首页</a></p></div>') % icon('arrow-left')
    # 404 页会出现在任意深度的地址下，所以用根路径引用样式和链接
    return page('页面不存在 · ' + SITE['name'], '页面不存在', body, '/', '')


# ---------------------------------------------------------------- 输出
def write(rel, text):
    path = os.path.join(ROOT, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(text)
    return rel


def main():
    out = [write('index.html', build_home()), write('projects/index.html', build_projects_index()),
           write('gallery/index.html', build_gallery()), write('sites/index.html', build_sites_index()),
           write('blog/index.html', build_blog_index()), write('404.html', build_404())]
    for i, pr in enumerate(PROJECTS):
        out.append(write('projects/%s.html' % pr['slug'], build_project(pr, i)))
    for post in POSTS:
        out.append(write('blog/%s.html' % post['slug'], build_post(post)))
    pages = [r for r in out if r != '404.html']
    write('sitemap.xml', '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n%s</urlset>\n'
          % ''.join('  <url><loc>%s/%s</loc></url>\n' % (BASE_URL, '' if r == 'index.html' else r) for r in pages))
    write('robots.txt', 'User-agent: *\nAllow: /\nSitemap: %s/sitemap.xml\n' % BASE_URL)
    open(os.path.join(ROOT, '.nojekyll'), 'w').close()
    print('生成 %d 个页面：' % len(out))
    for rel in out:
        print('  ' + rel)


if __name__ == '__main__':
    main()
