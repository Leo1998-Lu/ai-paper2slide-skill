import os
import requests
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def fetch_star_history(repo, token):
    headers = {
        "Accept": "application/vnd.github.v3.star+json",
        "Authorization": f"Bearer {token}"
    }
    
    stars = []
    page = 1
    
    # 分页拉取所有的 Star 时间戳
    while True:
        url = f"https://api.github.com/repos/{repo}/stargazers?per_page=100&page={page}"
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        data = response.json()
        if not data:
            break
            
        stars.extend([item['starred_at'] for item in data])
        page += 1
        
    return stars

def plot_history(stars, repo_name):
    # 使用 Pandas 处理时间序列数据
    df = pd.DataFrame(stars, columns=['date'])
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values('date')
    df['stars'] = range(1, len(df) + 1)
    
    # 补充当前时间的数据点，让折线图延伸到“今天”
    current_time = pd.Timestamp.utcnow()
    if not df.empty:
        current_stars = df['stars'].iloc[-1]
        df = pd.concat([df, pd.DataFrame({'date': [current_time], 'stars': [current_stars]})], ignore_index=True)
    
    # 设置绘图风格
    plt.style.use('seaborn-v0_8-whitegrid')
    fig, ax = plt.subplots(figsize=(10, 5), dpi=150)
    
    # 绘制阶梯图或折线图
    ax.plot(df['date'], df['stars'], color='#2ea44f', linewidth=2.5)
    
    # 格式化图表
    ax.set_title(f"Star History of {repo_name}", fontsize=16, pad=15, fontweight='bold')
    ax.set_xlabel("Date", fontsize=12)
    ax.set_ylabel("Stars", fontsize=12)
    
    # 优化时间轴显示
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    plt.xticks(rotation=45)
    
    ax.fill_between(df['date'], df['stars'], color='#2ea44f', alpha=0.1)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    plt.tight_layout()
    plt.savefig("star_history.png")

if __name__ == "__main__":
    # GitHub Actions 会自动注入这两个环境变量
    repo = os.environ.get("GITHUB_REPOSITORY")
    token = os.environ.get("GITHUB_TOKEN")
    
    if not repo or not token:
        raise ValueError("Missing GITHUB_REPOSITORY or GITHUB_TOKEN environment variables.")
        
    print(f"Fetching star history for {repo}...")
    star_dates = fetch_star_history(repo, token)
    print(f"Fetched {len(star_dates)} stars. Generating plot...")
    plot_history(star_dates, repo)
    print("Successfully generated star_history.png")
