# 付钟浩 Alex · 个人网站

纯静态网站，零依赖：一个 CSS、一个 JS、一个生成脚本。可以直接放到 GitHub Pages、Cloudflare Pages，或者阿里云服务器的 nginx。

## 页面

| 路径 | 内容 |
|---|---|
| `index.html` | 首页：首屏、关于我（带命令行小终端）、能力、精选项目、我的网站、最近文章、联系我 |
| `projects/index.html` | 全部项目，可以按公开 / 私有筛选 |
| `projects/*.html` | 8 个项目详情页 |
| `sites/index.html` | 全部在线网站 |
| `blog/index.html`、`blog/*.html` | 文章列表和文章页（左侧有目录） |
| `404.html` | 找不到页面时显示 |

## 怎么改内容

所有文字都在 `build.py` 的上半部分：

| 要改的内容 | 改哪里 |
|---|---|
| 站点信息 | `SITE` |
| 关于我 | `ABOUT` |
| 能力标签 | `SKILLS` |
| 课程 | `COURSES` |
| 项目 | `PROJECTS` |
| 网站 | `SITES` |
| 联系方式 | `CONTACT` |
| 文章 | `POSTS` |

改完运行一次，所有页面就会重新生成：

```bash
python3 build.py
```

- **头像**：把照片存成 `assets/img/avatar.jpg`（也可以是 `.png` 或 `.webp`），重新生成后，首屏的字母头像会换成照片。
- **新增项目**：在 `PROJECTS` 里加一项。`kind` 写 `public` 或 `private`；`home: True` 的会出现在首页。
- **新增文章**：在 `POSTS` 里加一项。正文由几种块组成：`h2` 标题、`p` 段落、`ul` / `ol` 列表、`pre` 代码。段落里支持 `` `代码` ``、`**加粗**`、`[文字](链接)`。

## 本地预览

```bash
python3 -m http.server 8000
```

然后打开 http://localhost:8000/ 。也可以直接双击 `index.html`，所有链接都是相对路径。

## 已有的效果

- 浅色 / 深色两套主题，跟随系统，可以手动切换并记住选择。
- 毛玻璃卡片、角标、颗粒质感、鼠标高光。
- 滚动到位时卡片淡入；系统开了「减少动态效果」时自动关闭动画。
- 首页右侧有进度轨，显示当前读到哪个版块。
- 首页的小终端支持这些命令：`help`、`whoami`、`skills`、`courses`、`projects`、`sites`、`contact`、`theme`、`clear`。
- 页脚显示北京时间。

## 待补

- 头像照片。
- 简历里待确认的数字（学员人数等），确认后补进对应项目。
