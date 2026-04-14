export type LearningNodeKind = 'stage' | 'concept'
export type LearningNodeTrack = 'roadmap' | 'knowledge'
export type LearningDifficulty = 'Starter' | 'Intermediate' | 'Advanced'
export type LearningResourceType = 'guide' | 'docs' | 'practice' | 'community'

export interface LearningResource {
  id: string
  title: string
  description: string
  url: string
  type: LearningResourceType
}

export interface LearningNodePosition {
  x: number
  y: number
}

export interface LearningNode {
  id: string
  kind: LearningNodeKind
  track: LearningNodeTrack
  title: string
  shortTitle: string
  tagline: string
  summary: string
  whyItMatters: string
  estimatedTime: string
  difficulty: LearningDifficulty
  stageId: string
  position: LearningNodePosition
  prerequisites: string[]
  connectsTo: string[]
  keyConcepts: string[]
  practiceTasks: string[]
  pitfalls: string[]
  deliverables: string[]
  validation: string[]
  resources: LearningResource[]
}

export interface LearningStage {
  id: string
  order: number
  label: string
  duration: string
  goal: string
  milestone: string
  focusNodeIds: string[]
}

export interface LearningPrinciple {
  id: string
  title: string
  description: string
  emphasis: string
}

export interface LearningAction {
  id: string
  label: string
  helperText: string
  targetNodeId: string
  sectionId: string
}

export interface LearningConnection {
  id: string
  source: string
  target: string
  label: string
  relation: 'sequence' | 'knowledge' | 'apply'
}

export interface LearningOverviewStat {
  label: string
  value: string
  detail: string
}

const resourceCatalog: Record<string, LearningResource> = {
  langchainDocs: {
    id: 'langchainDocs',
    title: 'LangChain 官方文档',
    description: '查概念定义、API 示例和最新的最佳实践。',
    url: 'https://python.langchain.com/',
    type: 'docs'
  },
  langgraphDocs: {
    id: 'langgraphDocs',
    title: 'LangGraph 文档',
    description: '理解状态机、多节点编排和 agent 工作流设计。',
    url: 'https://langchain-ai.github.io/langgraph/',
    type: 'docs'
  },
  chineseGuide: {
    id: 'chineseGuide',
    title: 'LangChain 中文入门指南',
    description: '适合快速建立整体认知和本地实践顺序。',
    url: 'https://github.com/liaokongVFX/LangChain-Chinese-Getting-Started-Guide',
    type: 'guide'
  },
  ragFromScratch: {
    id: 'ragFromScratch',
    title: 'RAG From Scratch',
    description: '按步骤拆解检索、重排、引用与评估流程。',
    url: 'https://github.com/langchain-ai/rag-from-scratch',
    type: 'practice'
  },
  promptGuide: {
    id: 'promptGuide',
    title: 'Prompt Engineering Guide',
    description: '补齐提示词设计模式、评测方法和常见失败类型。',
    url: 'https://www.promptingguide.ai/',
    type: 'guide'
  },
  smithDocs: {
    id: 'smithDocs',
    title: 'LangSmith 文档',
    description: '用于 trace、评估、提示词回放和链路调试。',
    url: 'https://docs.smith.langchain.com/',
    type: 'docs'
  },
  openaiCookbook: {
    id: 'openaiCookbook',
    title: 'OpenAI Cookbook',
    description: '参考模型调用、结构化输出和工具调用范式。',
    url: 'https://cookbook.openai.com/',
    type: 'guide'
  },
  communityHub: {
    id: 'communityHub',
    title: 'BotLearn 社区',
    description: '把你的实践结果沉淀为可复用经验和讨论主题。',
    url: 'https://clawhub.ai',
    type: 'community'
  }
}

const resources = (...ids: Array<keyof typeof resourceCatalog>) => ids.map(id => resourceCatalog[id])

export const learningStages: LearningStage[] = [
  {
    id: 'stage-foundation',
    order: 1,
    label: '基础入门',
    duration: '1-3 天',
    goal: '搭起运行环境，知道 LangChain 在整个 LLM 应用链路里的位置。',
    milestone: '能够独立跑通第一个 prompt -> model -> output 的最小闭环。',
    focusNodeIds: ['stage-foundation', 'prompt-design', 'chain-workflow']
  },
  {
    id: 'stage-core',
    order: 2,
    label: '核心链路',
    duration: '3-6 天',
    goal: '理解链路拆分、状态管理和工具协作的基本模型。',
    milestone: '可以把一个简单任务拆成多步执行并补充状态。',
    focusNodeIds: ['stage-core', 'memory-state', 'tools-agents']
  },
  {
    id: 'stage-rag',
    order: 3,
    label: 'RAG 实战',
    duration: '5-8 天',
    goal: '掌握文档切分、向量检索、重排和答案引用的关键环节。',
    milestone: '做出一个可验证、可解释的知识库问答 Demo。',
    focusNodeIds: ['stage-rag', 'retrieval', 'rag-system']
  },
  {
    id: 'stage-agent',
    order: 4,
    label: 'Agent 编排',
    duration: '4-7 天',
    goal: '学会把工具、上下文、决策和失败恢复组合成复杂工作流。',
    milestone: '实现一个具备工具调用和简单任务路由能力的 Agent。',
    focusNodeIds: ['stage-agent', 'tools-agents', 'memory-state', 'evaluation-guardrails']
  },
  {
    id: 'stage-production',
    order: 5,
    label: '评估与落地',
    duration: '3-5 天',
    goal: '把 Demo 推进到可观测、可评估、可持续迭代的工程状态。',
    milestone: '完成 trace、评测、回归检查和部署注意事项梳理。',
    focusNodeIds: ['stage-production', 'evaluation-guardrails', 'deployment-observability']
  }
]

export const learningNodes: LearningNode[] = [
  {
    id: 'stage-foundation',
    kind: 'stage',
    track: 'roadmap',
    title: 'Stage 1 · 基础入门',
    shortTitle: '基础入门',
    tagline: '先把最小闭环跑通，再去扩展抽象能力。',
    summary: '从模型调用、prompt 基本结构和输出解析入手，建立 LangChain 学习坐标系。',
    whyItMatters: '如果一开始没有建立“输入、推理、输出、验证”这个最小闭环，后面学链、检索和 Agent 时会只记 API，不理解设计意图。',
    estimatedTime: '1-3 天',
    difficulty: 'Starter',
    stageId: 'stage-foundation',
    position: { x: 40, y: 70 },
    prerequisites: [],
    connectsTo: ['stage-core', 'prompt-design', 'chain-workflow'],
    keyConcepts: ['LangChain 在应用层的位置', 'LLM 调用最小闭环', 'Prompt 输入输出结构'],
    practiceTasks: ['配置模型密钥', '跑通一个问答脚本', '对比不同 Prompt 对输出的影响'],
    pitfalls: ['一开始就追复杂 Agent', '忽略日志和输入输出记录', '把概念学习和代码验证脱节'],
    deliverables: ['最小 Demo 脚本', '环境配置清单', '第一阶段学习笔记'],
    validation: ['能解释 LangChain 与模型 SDK 的区别', '能独立运行并修改最小示例'],
    resources: resources('chineseGuide', 'langchainDocs', 'openaiCookbook')
  },
  {
    id: 'prompt-design',
    kind: 'concept',
    track: 'knowledge',
    title: 'Prompt Design',
    shortTitle: 'Prompt',
    tagline: '把任务边界讲清楚，模型才有稳定输出。',
    summary: '聚焦系统提示、角色约束、结构化输出和 few-shot 示例的组织方式。',
    whyItMatters: 'LangChain 的很多组件本质上都在帮助你更稳定地组织 prompt 和上下文，没有 prompt 设计能力，链路再复杂也很难稳定。',
    estimatedTime: '0.5-1 天',
    difficulty: 'Starter',
    stageId: 'stage-foundation',
    position: { x: 120, y: 320 },
    prerequisites: ['stage-foundation'],
    connectsTo: ['chain-workflow', 'tools-agents'],
    keyConcepts: ['系统提示与任务提示分层', 'Few-shot 示例', '结构化输出约束'],
    practiceTasks: ['写一个固定 JSON 输出的 Prompt', '对比零样本和 few-shot 的差异', '给错误输出增加防呆提示'],
    pitfalls: ['Prompt 太长但没有结构', '没有约束输出格式', '把业务规则散落在代码里'],
    deliverables: ['可复用 Prompt 模板', '输出格式约束示例'],
    validation: ['能让模型稳定返回结构化字段', '能说明 Prompt 调整前后的输出差异'],
    resources: resources('promptGuide', 'langchainDocs', 'openaiCookbook')
  },
  {
    id: 'chain-workflow',
    kind: 'concept',
    track: 'knowledge',
    title: 'Chains And Workflow',
    shortTitle: 'Chains',
    tagline: '把复杂任务拆成一串可观测、可调试的小步骤。',
    summary: '学习如何组合 Prompt、模型、解析器和中间步骤，形成稳定的业务流程。',
    whyItMatters: '很多“模型不稳定”的问题，其实是任务拆分不合理。先学会 workflow，再谈复杂 Agent 才不容易失控。',
    estimatedTime: '1-2 天',
    difficulty: 'Starter',
    stageId: 'stage-foundation',
    position: { x: 340, y: 320 },
    prerequisites: ['stage-foundation', 'prompt-design'],
    connectsTo: ['stage-core', 'memory-state', 'retrieval'],
    keyConcepts: ['Runnable 思维', '步骤拆分', '输出解析与中间状态'],
    practiceTasks: ['做一个“提问 -> 改写 -> 回答 -> 总结”的链路', '为每个步骤记录中间输出', '比较单次调用与多步调用的结果'],
    pitfalls: ['一步塞太多任务', '缺少中间结果检查', '异常处理留在最后才补'],
    deliverables: ['多步骤链路 Demo', '中间状态日志'],
    validation: ['可以清楚说出每一步的输入输出', '出现错误时能快速定位到具体步骤'],
    resources: resources('langchainDocs', 'chineseGuide', 'smithDocs')
  },
  {
    id: 'stage-core',
    kind: 'stage',
    track: 'roadmap',
    title: 'Stage 2 · 核心链路',
    shortTitle: '核心链路',
    tagline: '开始把状态、工具和路由能力接进来。',
    summary: '在工作流基础上引入记忆、工具和任务编排，理解从“链”走向“系统”的变化。',
    whyItMatters: '这一阶段决定你后续是只能写 Demo，还是能搭出更接近真实产品的应用。',
    estimatedTime: '3-6 天',
    difficulty: 'Intermediate',
    stageId: 'stage-core',
    position: { x: 300, y: 70 },
    prerequisites: ['stage-foundation', 'chain-workflow'],
    connectsTo: ['stage-rag', 'memory-state', 'tools-agents'],
    keyConcepts: ['状态显式化', '工具调用边界', '失败恢复'],
    practiceTasks: ['给链路补历史上下文', '为工具调用加输入校验', '把简单流程改成可重试结构'],
    pitfalls: ['把所有状态塞在一个 prompt 里', '没有区分模型能力和工具能力', '失败后没有回退路径'],
    deliverables: ['可复用链路模板', '工具调用 Demo', '状态管理说明'],
    validation: ['可以解释什么时候该用链、什么时候该用 Agent', '能给工具调用增加保护逻辑'],
    resources: resources('langchainDocs', 'langgraphDocs', 'smithDocs')
  },
  {
    id: 'memory-state',
    kind: 'concept',
    track: 'knowledge',
    title: 'Memory And State',
    shortTitle: 'Memory',
    tagline: '把上下文当成状态来管理，而不是临时字符串拼接。',
    summary: '理解对话历史、任务状态、长期记忆和短期上下文的不同职责。',
    whyItMatters: '很多多轮应用的问题都不是“模型太弱”，而是状态管理不清楚，导致上下文污染、重复思考或丢信息。',
    estimatedTime: '1 天',
    difficulty: 'Intermediate',
    stageId: 'stage-core',
    position: { x: 520, y: 500 },
    prerequisites: ['chain-workflow'],
    connectsTo: ['tools-agents', 'evaluation-guardrails'],
    keyConcepts: ['短期上下文', '任务状态', '长期记忆边界'],
    practiceTasks: ['实现一个多轮助手', '把会话状态拆成显示字段', '对比无状态与有状态回答差异'],
    pitfalls: ['把全部历史都喂给模型', '记忆没有过期策略', '业务状态和对话状态混用'],
    deliverables: ['状态字段设计文档', '多轮助手原型'],
    validation: ['能解释每种状态的存储位置和用途', '能控制上下文长度和噪音'],
    resources: resources('langchainDocs', 'langgraphDocs', 'smithDocs')
  },
  {
    id: 'tools-agents',
    kind: 'concept',
    track: 'knowledge',
    title: 'Tools And Agents',
    shortTitle: 'Agents',
    tagline: '让模型不只会回答，还能在边界内行动。',
    summary: '学习工具描述、参数约束、调用回路和 agent 规划模式。',
    whyItMatters: 'Agent 的核心不在“会不会调工具”，而在于如何控制决策成本、失败模式和执行边界。',
    estimatedTime: '1-2 天',
    difficulty: 'Intermediate',
    stageId: 'stage-core',
    position: { x: 760, y: 500 },
    prerequisites: ['prompt-design', 'chain-workflow', 'memory-state'],
    connectsTo: ['stage-agent', 'evaluation-guardrails', 'deployment-observability'],
    keyConcepts: ['工具 schema', '规划与执行', '失败重试与人工兜底'],
    practiceTasks: ['实现带搜索工具的问答代理', '限制工具入参并记录失败案例', '比较单 Agent 与固定链路的优缺点'],
    pitfalls: ['把 Agent 当默认方案', '没有给工具加权限和超时限制', '输出不可追踪'],
    deliverables: ['工具调用 Agent Demo', '失败案例清单'],
    validation: ['能解释工具何时被调用以及为什么失败', '能追踪一次 agent 执行过程'],
    resources: resources('langchainDocs', 'langgraphDocs', 'openaiCookbook')
  },
  {
    id: 'stage-rag',
    kind: 'stage',
    track: 'roadmap',
    title: 'Stage 3 · RAG 实战',
    shortTitle: 'RAG 实战',
    tagline: '进入最常见、也最容易踩坑的企业应用场景。',
    summary: '围绕检索质量、切分策略、引用展示和答案可信度建立完整实践。',
    whyItMatters: 'RAG 是很多 AI 应用的基本盘，但真正难点不在“能搜到”，而在“搜得准、答得稳、可追溯”。',
    estimatedTime: '5-8 天',
    difficulty: 'Intermediate',
    stageId: 'stage-rag',
    position: { x: 560, y: 70 },
    prerequisites: ['stage-core', 'chain-workflow'],
    connectsTo: ['stage-agent', 'retrieval', 'rag-system'],
    keyConcepts: ['文档预处理', '检索链路质量', '引用与可解释性'],
    practiceTasks: ['做一个企业 FAQ 知识库', '测试切分粒度', '比较不同检索结果的答案质量'],
    pitfalls: ['只看生成结果不看召回质量', '没有引用来源', '索引构建和查询链路分离不清'],
    deliverables: ['RAG Demo', '检索效果对比表', '文档切分策略说明'],
    validation: ['能定位回答错误来自召回还是生成', '能展示答案引用来源'],
    resources: resources('ragFromScratch', 'langchainDocs', 'smithDocs')
  },
  {
    id: 'retrieval',
    kind: 'concept',
    track: 'knowledge',
    title: 'Retrieval Fundamentals',
    shortTitle: 'Retrieval',
    tagline: '先把“找对资料”做好，再谈“回答漂亮”。',
    summary: '覆盖切分、Embedding、向量检索、混合检索、重排和上下文压缩。',
    whyItMatters: 'RAG 成败往往由检索阶段决定。召回不准，模型只能在错误材料上继续胡说。',
    estimatedTime: '1-2 天',
    difficulty: 'Intermediate',
    stageId: 'stage-rag',
    position: { x: 660, y: 320 },
    prerequisites: ['chain-workflow'],
    connectsTo: ['rag-system', 'evaluation-guardrails'],
    keyConcepts: ['切分粒度', '召回与精排', '上下文压缩'],
    practiceTasks: ['对比不同 chunk size', '测试 BM25 + 向量混合检索', '记录召回前 5 条的相关性'],
    pitfalls: ['chunk 切太碎或太大', '只关心最终回答不看召回集', '忽略重排'],
    deliverables: ['检索实验记录', 'Embedding 与检索配置清单'],
    validation: ['可以解释为什么某条文档会被召回', '能用数据比较不同检索策略'],
    resources: resources('ragFromScratch', 'langchainDocs', 'openaiCookbook')
  },
  {
    id: 'rag-system',
    kind: 'concept',
    track: 'knowledge',
    title: 'RAG System Design',
    shortTitle: 'RAG',
    tagline: '把检索、生成、引用和评测串成一套业务系统。',
    summary: '从问题改写、检索、重排、答案生成、引用展示到失败回退，建立 RAG 完整链路。',
    whyItMatters: '真正能上线的 RAG 不是一个检索器，而是一套可监控、可调参、可解释的系统工程。',
    estimatedTime: '2-3 天',
    difficulty: 'Intermediate',
    stageId: 'stage-rag',
    position: { x: 900, y: 320 },
    prerequisites: ['retrieval', 'stage-rag'],
    connectsTo: ['stage-agent', 'evaluation-guardrails', 'deployment-observability'],
    keyConcepts: ['问题改写', '引用答案', '失败回退策略'],
    practiceTasks: ['增加引用高亮', '加入无答案判定', '给低置信度结果返回澄清问题'],
    pitfalls: ['所有问题都强行生成答案', '没有无答案分支', '缺少用户反馈闭环'],
    deliverables: ['可解释 RAG 原型', '评估数据样例', '回退策略说明'],
    validation: ['能展示每次回答使用了哪些上下文', '能区分“无答案”和“模型答错”'],
    resources: resources('ragFromScratch', 'smithDocs', 'communityHub')
  },
  {
    id: 'stage-agent',
    kind: 'stage',
    track: 'roadmap',
    title: 'Stage 4 · Agent 编排',
    shortTitle: 'Agent 编排',
    tagline: '开始考虑更复杂的决策、路由和协作。',
    summary: '从单链路过渡到多工具、多步骤和可能存在分支的 agent 工作流。',
    whyItMatters: '这一阶段帮助你判断哪些需求值得用 Agent，哪些应该继续用确定性的 workflow。',
    estimatedTime: '4-7 天',
    difficulty: 'Advanced',
    stageId: 'stage-agent',
    position: { x: 820, y: 70 },
    prerequisites: ['stage-rag', 'tools-agents'],
    connectsTo: ['stage-production', 'tools-agents', 'evaluation-guardrails'],
    keyConcepts: ['任务路由', '多步骤决策', '失败恢复和人工介入'],
    practiceTasks: ['做一个多工具研究助手', '把复杂流程切成 planner / executor / reviewer', '记录不同分支的成功率'],
    pitfalls: ['为了炫技而引入 Agent', '没有可视化 trace', '工具权限边界不清'],
    deliverables: ['多工具 Agent Demo', '执行 trace 样例'],
    validation: ['能复盘 agent 每一步决策', '能量化 agent 比固定流程多带来的价值'],
    resources: resources('langgraphDocs', 'smithDocs', 'communityHub')
  },
  {
    id: 'evaluation-guardrails',
    kind: 'concept',
    track: 'knowledge',
    title: 'Evaluation And Guardrails',
    shortTitle: 'Eval',
    tagline: '让系统不是“看起来能跑”，而是“可持续地跑”。',
    summary: '围绕离线评测、在线监控、提示词回归、输出约束和安全边界做系统化设计。',
    whyItMatters: '没有评测和 guardrails，你很难知道系统是进步了还是退步了，也很难稳定迭代。',
    estimatedTime: '1-2 天',
    difficulty: 'Advanced',
    stageId: 'stage-production',
    position: { x: 1080, y: 500 },
    prerequisites: ['tools-agents', 'retrieval', 'rag-system'],
    connectsTo: ['deployment-observability'],
    keyConcepts: ['离线评测集', 'Trace 与回归', '输出安全约束'],
    practiceTasks: ['为核心场景写评测样本', '监控失败回答类型', '加入输出格式校验'],
    pitfalls: ['只凭主观感觉改 prompt', '没有基线数据', '把安全约束完全交给模型自觉'],
    deliverables: ['评测数据集', '回归检查清单', '安全约束策略'],
    validation: ['能通过样本集验证改动效果', '能快速识别提示词回归'],
    resources: resources('smithDocs', 'langchainDocs', 'openaiCookbook')
  },
  {
    id: 'stage-production',
    kind: 'stage',
    track: 'roadmap',
    title: 'Stage 5 · 评估与落地',
    shortTitle: '评估与落地',
    tagline: '把学习成果沉淀成可交付的工程能力。',
    summary: '收束到评估、观测、部署、性能和反馈闭环，让项目具备上线前的基本成熟度。',
    whyItMatters: '最终产出不是一张思维导图，而是你能把 AI 能力接入真实产品并持续迭代。',
    estimatedTime: '3-5 天',
    difficulty: 'Advanced',
    stageId: 'stage-production',
    position: { x: 1080, y: 70 },
    prerequisites: ['stage-agent', 'evaluation-guardrails'],
    connectsTo: ['deployment-observability'],
    keyConcepts: ['可观测性', '性能成本平衡', '上线前检查'],
    practiceTasks: ['补充 tracing', '整理上线 checklist', '复盘成本与效果'],
    pitfalls: ['只关注功能完成', '没有成本和延迟视角', '没有反馈回流机制'],
    deliverables: ['上线清单', '监控指标表', '学习总结'],
    validation: ['能解释系统的主要风险点', '能给出下一轮优化优先级'],
    resources: resources('smithDocs', 'communityHub', 'langchainDocs')
  },
  {
    id: 'deployment-observability',
    kind: 'concept',
    track: 'knowledge',
    title: 'Deployment And Observability',
    shortTitle: 'Deploy',
    tagline: '把开发期的可见性带到运行期，才能真正迭代。',
    summary: '关注 tracing、成本、延迟、失败监控、用户反馈和版本迭代机制。',
    whyItMatters: 'AI 应用的稳定性不只是服务器不挂，更包括输出质量、成本和用户体验是否可持续。',
    estimatedTime: '1 天',
    difficulty: 'Advanced',
    stageId: 'stage-production',
    position: { x: 1260, y: 320 },
    prerequisites: ['rag-system', 'tools-agents', 'evaluation-guardrails'],
    connectsTo: [],
    keyConcepts: ['监控指标', '成本观测', '版本迭代'],
    practiceTasks: ['记录 token 成本', '对慢请求分层分析', '建立问题反馈归档'],
    pitfalls: ['只有应用日志没有 AI trace', '没有把线上问题回写到评测集', '版本变更缺少对照'],
    deliverables: ['观测面板需求', '上线后优化 backlog'],
    validation: ['能用数据解释性能波动', '能把线上问题转成可复现样例'],
    resources: resources('smithDocs', 'langgraphDocs', 'communityHub')
  }
]

export const learningConnections: LearningConnection[] = [
  { id: 'c1', source: 'stage-foundation', target: 'stage-core', label: '阶段推进', relation: 'sequence' },
  { id: 'c2', source: 'stage-core', target: 'stage-rag', label: '进入实战', relation: 'sequence' },
  { id: 'c3', source: 'stage-rag', target: 'stage-agent', label: '复杂编排', relation: 'sequence' },
  { id: 'c4', source: 'stage-agent', target: 'stage-production', label: '工程化落地', relation: 'sequence' },
  { id: 'c5', source: 'stage-foundation', target: 'prompt-design', label: '建立 Prompt 基线', relation: 'apply' },
  { id: 'c6', source: 'stage-foundation', target: 'chain-workflow', label: '最小 workflow', relation: 'apply' },
  { id: 'c7', source: 'prompt-design', target: 'chain-workflow', label: '提示设计进入链路', relation: 'knowledge' },
  { id: 'c8', source: 'chain-workflow', target: 'memory-state', label: '引入状态', relation: 'knowledge' },
  { id: 'c9', source: 'chain-workflow', target: 'retrieval', label: '加入检索步骤', relation: 'knowledge' },
  { id: 'c10', source: 'memory-state', target: 'tools-agents', label: '多轮与工具协作', relation: 'knowledge' },
  { id: 'c11', source: 'stage-core', target: 'tools-agents', label: '阶段重点', relation: 'apply' },
  { id: 'c12', source: 'stage-rag', target: 'retrieval', label: '检索基础', relation: 'apply' },
  { id: 'c13', source: 'retrieval', target: 'rag-system', label: '构建 RAG 闭环', relation: 'knowledge' },
  { id: 'c14', source: 'stage-rag', target: 'rag-system', label: '阶段重点', relation: 'apply' },
  { id: 'c15', source: 'rag-system', target: 'evaluation-guardrails', label: '用评测稳住质量', relation: 'knowledge' },
  { id: 'c16', source: 'tools-agents', target: 'evaluation-guardrails', label: '观测 Agent 风险', relation: 'knowledge' },
  { id: 'c17', source: 'stage-agent', target: 'tools-agents', label: '编排能力', relation: 'apply' },
  { id: 'c18', source: 'stage-production', target: 'evaluation-guardrails', label: '评估先行', relation: 'apply' },
  { id: 'c19', source: 'evaluation-guardrails', target: 'deployment-observability', label: '上线与监控', relation: 'knowledge' },
  { id: 'c20', source: 'stage-production', target: 'deployment-observability', label: '落地能力', relation: 'apply' }
]

export const learningPrinciples: LearningPrinciple[] = [
  {
    id: 'principle-verify',
    title: '每学一个点，立刻验证',
    description: '把概念转换成一个最小代码实验，优先获得真实反馈，而不是继续堆阅读量。',
    emphasis: '防止“知道名词，但不会落地”。'
  },
  {
    id: 'principle-trace',
    title: '任何复杂链路都要可追踪',
    description: '无论是 RAG 还是 Agent，都要能看到输入、过程、输出和失败原因。',
    emphasis: '后期定位问题时，trace 比直觉更重要。'
  },
  {
    id: 'principle-system',
    title: '把能力当系统而不是 API',
    description: '学习重点不只是调用组件，而是理解输入约束、状态边界、失败恢复和评估机制。',
    emphasis: '这决定你写的是 Demo 还是产品。'
  }
]

export const learningActions: LearningAction[] = [
  {
    id: 'action-start-rag',
    label: '从 RAG 系统设计开始',
    helperText: '适合已经了解基础概念、想快速进入高价值场景。',
    targetNodeId: 'rag-system',
    sectionId: 'learning-map'
  },
  {
    id: 'action-build-basics',
    label: '回到基础入门',
    helperText: '适合第一次接触 LangChain，需要先建立完整坐标系。',
    targetNodeId: 'stage-foundation',
    sectionId: 'learning-map'
  },
  {
    id: 'action-open-resources',
    label: '查看资料与验证清单',
    helperText: '用于补资料、找 Demo 和对照阶段产出。',
    targetNodeId: 'stage-production',
    sectionId: 'learning-resources'
  }
]

export const learningOverviewStats: LearningOverviewStat[] = [
  {
    label: '学习阶段',
    value: String(learningStages.length),
    detail: '从基础入门到评估落地，按真实项目节奏推进。'
  },
  {
    label: '关键知识节点',
    value: String(learningNodes.filter(node => node.kind === 'concept').length),
    detail: '覆盖 Prompt、Workflow、RAG、Agent、评测与部署。'
  },
  {
    label: '验证维度',
    value: '6+',
    detail: '每个节点都配套实践任务、产出物、风险点和验证方式。'
  },
  {
    label: '推荐资源',
    value: String(Object.keys(resourceCatalog).length),
    detail: '把官方文档、实践仓库和社区入口收束到一份视图里。'
  }
]

export const learningResources = Object.values(resourceCatalog)

export const learningMapMeta = {
  title: 'LangChain 知识地图与学习路线',
  subtitle: '把核心概念、阶段目标、实践任务和验证方式串成一张可以交互的学习地图。',
  description:
    '这张地图同时回答两个问题：LangChain 的能力结构是什么，以及你应该按什么顺序把它学成真正可交付的工程能力。',
  recommendedNodeId: 'rag-system'
}

export const defaultSelectedNodeId = learningMapMeta.recommendedNodeId

export const learningNodeMap = Object.fromEntries(learningNodes.map(node => [node.id, node] as const))
export const learningStageMap = Object.fromEntries(learningStages.map(stage => [stage.id, stage] as const))

export const getLearningNode = (nodeId: string) => learningNodeMap[nodeId]

export const getStageForNode = (node: LearningNode) => learningStageMap[node.stageId]
