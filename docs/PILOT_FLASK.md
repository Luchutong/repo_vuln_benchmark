# 首个核验样本：Flask / CVE-2023-30861

状态：NEEDS_REVIEW，未进入正式 Catalog。候选别名为 GHSA-m2qf-hxjv-5gpq / CVE-2023-30861 / PYSEC-2023-62。

已保存 CNA CVE 记录、OSV 响应、两条上游修复的完整元数据/差异、两个正式 release、版本比较和脆弱/修复源码少量片段。CNA 源直接给出 CVSS 3.1 分数 7.5 及向量，不由模型补造。

2.3.1 tag 经 annotated tag 解引用到 721abdc3810057269503a72d2db80fb826f3c85c。根因候选定位在该 SHA 的 src/flask/sessions.py:347–365：只有 session.accessed 时添加 Vary，刷新 cookie 的路径可能发出 Set-Cookie 而缺少 Vary。此判断来自公告与补丁/源码的静态交叉检查，仍受应用配置及代理缓存条件约束。

版本比较确认：2.3.1→2.3.2 包含 70f906c51ce49c485f1d355703e9cc3386b1cc2b；2.2.4→2.2.5 包含 afd63b16170b7c047f5758eb910c416511e9c965。不能根据 commit 的出现顺序或 release.target_commitish 直接猜测分支。上游补丁增加 test_session_refresh_vary；本轮没有执行该测试。

尚缺指定 SHA 的全语言盘点、可构建/依赖核验、隔离红绿测试或 B 级证据完整复核、第二位独立审核者和人工抽查；也未完成跨所有历史分支的首次修复版本证明。不得填 A/B 通过，不得把拟选 SHA 写成正式评测快照。

机器可读证据及文件哈希：runs/jobs/pilot_flask_CVE-2023-30861.json。后续先完成 Flask 仓库准入、语言普查及独立审核，再决定是否向九张正式表写入数据。
