        performance_score=round(performance_score, 2),
        usefulness_score=round(usefulness_score, 2),
        ease_of_use_score=round(ease_of_use_score, 2),
        overall_score=round(overall_score, 2),
        strengths=strengths,
        weaknesses=weaknesses,
        recommendations=recommendations
    )


@router.get("/available")
async def get_available_skills():
    """获取可用技能列表"""
    skills_list = []
    for skill_id, config in AVAILABLE_SKILLS.items():
        skills_list.append({
            "id": skill_id,
            "name": config["name"],
            "description": config["description"],
            "version": config["version"],
            "timeout": config["timeout"]
        })
    
    return {
        "skills": skills_list,
        "count": len(skills_list),
        "timestamp": datetime.now().isoformat()
    }


@router.post("/trial", response_model=SkillTrialResponse)
async def start_skill_trial(
    request: SkillTrialRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """开始技能试用"""
    skill_name = request.skill_name
    
    if skill_name not in AVAILABLE_SKILLS:
        raise HTTPException(status_code=404, detail=f"Skill not found: {skill_name}")
    
    skill_config = AVAILABLE_SKILLS[skill_name]
    
    # 创建试用记录
    trial_id = f"trial_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{skill_name}"
    
    trial_record = SkillTrial(
        trial_id=trial_id,
        skill_name=skill_name,
        skill_version=request.skill_version or skill_config["version"],
        parameters=json.dumps(request.parameters),
        status="running",
        started_at=datetime.now(),
        timeout_seconds=request.timeout_seconds
    )
    
    db.add(trial_record)
    db.commit()
    
    # 在后台运行测试
    background_tasks.add_task(
        run_skill_trial_background,
        trial_id,
        skill_config,
        request.parameters,
        db
    )
    
    return SkillTrialResponse(
        trial_id=trial_id,
        skill_name=skill_name,
        status="running",
        started_at=trial_record.started_at,
        estimated_completion=datetime.now().timestamp() + request.timeout_seconds,
        log_path=f"/tmp/skill_trial_{trial_id}.log"
    )


async def run_skill_trial_background(
    trial_id: str,
    skill_config: Dict[str, Any],
    parameters: Dict[str, Any],
    db: Session
):
    """后台运行技能试用"""
    try:
        # 运行技能测试
        test_results = run_skill_test(skill_config, parameters)
        
        # 评估结果
        evaluation = evaluate_skill_results(test_results)
        
        # 创建报告
        report_id = f"report_{trial_id}"
        
        report = SkillReport(
            report_id=report_id,
            trial_id=trial_id,
            skill_name=skill_config["name"],
            skill_version=skill_config["version"],
            status="completed",
            score=evaluation.overall_score,
            metrics=json.dumps(test_results.get("metrics", {})),
            evaluation=json.dumps(evaluation.dict()),
            recommendations=json.dumps(evaluation.recommendations),
            created_at=datetime.now(),
            completed_at=datetime.now()
        )
        
        # 更新试用状态
        trial = db.query(SkillTrial).filter(SkillTrial.trial_id == trial_id).first()
        if trial:
            trial.status = "completed"
            trial.completed_at = datetime.now()
        
        db.add(report)
        db.commit()
        
    except Exception as e:
        # 更新试用状态为失败
        trial = db.query(SkillTrial).filter(SkillTrial.trial_id == trial_id).first()
        if trial:
            trial.status = "failed"
            trial.error_message = str(e)
            trial.completed_at = datetime.now()
            db.commit()


@router.get("/trial/{trial_id}")
async def get_trial_status(trial_id: str, db: Session = Depends(get_db)):
    """获取试用状态"""
    trial = db.query(SkillTrial).filter(SkillTrial.trial_id == trial_id).first()
    
    if not trial:
        raise HTTPException(status_code=404, detail="Trial not found")
    
    return {
        "trial_id": trial.trial_id,
        "skill_name": trial.skill_name,
        "status": trial.status,
        "started_at": trial.started_at,
        "completed_at": trial.completed_at,
        "error_message": trial.error_message
    }


@router.get("/report/{trial_id}")
async def get_trial_report(trial_id: str, db: Session = Depends(get_db)):
    """获取试用报告"""
    report = db.query(SkillReport).filter(SkillReport.trial_id == trial_id).first()
    
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    
    evaluation_data = json.loads(report.evaluation) if report.evaluation else {}
    
    return SkillReportResponse(
        report_id=report.report_id,
        trial_id=report.trial_id,
        skill_name=report.skill_name,
        status=report.status,
        score=report.score,
        metrics=json.loads(report.metrics) if report.metrics else {},
        recommendations=json.loads(report.recommendations) if report.recommendations else [],
        created_at=report.created_at,
        completed_at=report.completed_at
    )


@router.get("/evaluate/{skill_name}")
async def evaluate_skill(skill_name: str):
    """快速评估技能"""
    if skill_name not in AVAILABLE_SKILLS:
        raise HTTPException(status_code=404, detail=f"Skill not found: {skill_name}")
    
    skill_config = AVAILABLE_SKILLS[skill_name]
    
    # 运行快速测试
    test_results = run_skill_test(skill_config, {})
    
    # 评估结果
    evaluation = evaluate_skill_results(test_results)
    
    return {
        "skill": skill_name,
        "version": skill_config["version"],
        "evaluation": evaluation.dict(),
        "test_results": test_results,
        "timestamp": datetime.now().isoformat()
    }


@router.get("/recommendations")
async def get_skill_recommendations():
    """获取技能推荐"""
    recommendations = []
    
    for skill_name, config in AVAILABLE_SKILLS.items():
        # 运行快速评估
        test_results = run_skill_test(config, {})
        evaluation = evaluate_skill_results(test_results)
        
        recommendations.append({
            "skill": skill_name,
            "description": config["description"],
            "score": evaluation.overall_score,
            "suitability": "high" if evaluation.overall_score >= 0.7 else "medium" if evaluation.overall_score >= 0.5 else "low",
            "strengths": evaluation.strengths[:3],
            "best_for": get_skill_use_cases(skill_name)
        })
    
    # 按分数排序
    recommendations.sort(key=lambda x: x["score"], reverse=True)
    
    return {
        "recommendations": recommendations,
        "count": len(recommendations),
        "timestamp": datetime.now().isoformat()
    }


def get_skill_use_cases(skill_name: str) -> List[str]:
    """获取技能适用场景"""
    use_cases = {
        "tech-news-digest": [
            "技术趋势跟踪",
            "内容创作辅助",
            "市场研究",
            "技术学习"
        ],
        "triple-memory": [
            "长期记忆管理",
            "会话上下文保持",
            "用户偏好学习",
            "决策记录"
        ]
    }
    
    return use_cases.get(skill_name, ["通用用途"])


@router.post("/install/{skill_name}")
async def install_skill(skill_name: str):
    """安装技能（模拟）"""
    if skill_name not in AVAILABLE_SKILLS:
        raise HTTPException(status_code=404, detail=f"Skill not found: {skill_name}")
    
    skill_config = AVAILABLE_SKILLS[skill_name]
    
    # 模拟安装过程
    installation_steps = [
        {"step": 1, "action": "下载技能包", "status": "completed"},
        {"step": 2, "action": "验证完整性", "status": "completed"},
        {"step": 3, "action": "安装依赖", "status": "in_progress"},
        {"step": 4, "action": "配置环境", "status": "pending"},
        {"step": 5, "action": "测试功能", "status": "pending"}
    ]
    
    return {
        "skill": skill_name,
        "version": skill_config["version"],
        "status": "installing",
        "installation_steps": installation_steps,
        "estimated_time_seconds": 180,
        "started_at": datetime.now().isoformat()
    }